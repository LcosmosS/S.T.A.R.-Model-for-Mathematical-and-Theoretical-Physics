import sys, os, csv, json, argparse, time
from joblib import Parallel, delayed
from sageall import EllipticCurve, pari

# ----------------------------------------------------------------------
# Submodule paths
# ----------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ECDATA_ROOT = os.path.join(REPO_ROOT, "data", "ecdata")
LMFDB_ROOT  = os.path.join(REPO_ROOT, "data", "lmfdb")

# ----------------------------------------------------------------------
# PARI defaults for each worker
# ----------------------------------------------------------------------
def init_pari():
    pari.default('two_seconds', 10**9)
    pari.default('primelimit', 10**7)
    pari.default('seriesprecision', 50)

# ----------------------------------------------------------------------
# Load Cremona ecdata
# ----------------------------------------------------------------------
def load_cremona(label):
    import re
    m = re.match(r"(\d+)([a-z]+)(\d+)", label)
    if not m:
        return None
    N, iso, num = m.groups()

    path = os.path.join(ECDATA_ROOT, N, iso, f"{label}")
    if not os.path.exists(path):
        return None

    data = {}
    with open(path) as f:
        for line in f:
            if line.startswith("a-invariants"):
                parts = line.split(":")[1].strip().split()
                data["ainvs"] = list(map(int, parts))
            elif line.startswith("conductor"):
                data["conductor"] = int(line.split(":")[1])
            elif line.startswith("torsion"):
                data["torsion"] = int(line.split(":")[1])
            elif line.startswith("tamagawa"):
                data["tamagawa"] = int(line.split(":")[1])

    return data if "ainvs" in data else None

# ----------------------------------------------------------------------
# Load LMFDB JSON
# ----------------------------------------------------------------------
def load_lmfdb(label):
    import re
    m = re.match(r"(\d+)([a-z]+)(\d+)", label)
    if not m:
        return None
    N, iso, num = m.groups()

    json_path = os.path.join(
        LMFDB_ROOT, "elliptic_curves", N, iso, f"{label}.json"
    )
    if not os.path.exists(json_path):
        return None

    with open(json_path) as f:
        j = json.load(f)

    return {
        "ainvs": j["ainvs"],
        "conductor": j["conductor"],
        "torsion": j["torsion_order"],
        "tamagawa": j.get("tamagawa_product"),
        "rank_lmfdb": j.get("rank"),
    }

# ----------------------------------------------------------------------
# Unified loader
# ----------------------------------------------------------------------
def load_curve_data(label):
    d = load_cremona(label)
    if d is not None:
        return d
    return load_lmfdb(label)

# ----------------------------------------------------------------------
# Compute invariants for a single label
# ----------------------------------------------------------------------
def compute_one(label):
    init_pari()

    row = {
        "label": label,
        "conductor": None,
        "discriminant": None,
        "j_invariant": None,
        "omega_real": None,
        "torsion_order": None,
        "tamagawa_product": None,
        "rank_algebraic": None,
        "rank_analytic_pari": None,
        "selmer2_rank_pari": None,
        "sha_order": None,
        "heegner_height": None,
        "error": None,
    }

    # Load from submodules
    data = load_curve_data(label)
    if data is None:
        row["error"] = "Curve not found in ecdata or lmfdb"
        return row

    # Construct curve
    try:
        E = EllipticCurve(data["ainvs"])
    except Exception as e:
        row["error"] = f"EllipticCurve init failed: {e}"
        return row

    # Basic invariants
    try: row["conductor"] = int(E.conductor())
    except: pass

    try: row["discriminant"] = int(E.discriminant())
    except: pass

    try: row["j_invariant"] = int(E.j_invariant())
    except: pass

    try: row["omega_real"] = float(E.period_lattice().real_period())
    except: pass

    try: row["torsion_order"] = int(E.torsion_order())
    except: pass

    try: row["tamagawa_product"] = int(E.tamagawa_product())
    except: pass

    try: row["rank_algebraic"] = int(E.rank())
    except: pass

    # Analytic rank via PARI
    try:
        gE = pari(E)
        rdata = gE.ellrankinit()
        row["rank_analytic_pari"] = int(gE.ellrank(rdata))
    except Exception as e:
        row["rank_analytic_pari"] = None
        row["error"] = f"analytic rank error: {e}"

    # 2-Selmer rank
    try:
        row["selmer2_rank_pari"] = int(E.selmer_rank(2))
    except:
        pass

    # Sha
    try:
        sha = E.sha()
        if sha is not None:
            row["sha_order"] = int(sha.order())
    except:
        pass

    # Heegner height
    try:
        gens = E.gens()
        if gens:
            row["heegner_height"] = float(E.height(gens[0]))
    except:
        pass

    return row

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()

    # Load labels
    labels = []
    with open(args.labels_file) as f:
        reader = csv.DictReader(f)
        for r in reader:
            labels.append(r["label"].strip())

    print(f"Loaded {len(labels)} labels")

    # Prepare output
    out_path = args.output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fieldnames = [
        "label",
        "conductor",
        "discriminant",
        "j_invariant",
        "omega_real",
        "torsion_order",
        "tamagawa_product",
        "rank_algebraic",
        "rank_analytic_pari",
        "selmer2_rank_pari",
        "sha_order",
        "heegner_height",
        "error",
    ]

    write_header = not os.path.exists(out_path)

    t0 = time.time()
    processed = 0

    with open(out_path, "a", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        # Parallel processing in batches
        for i in range(0, len(labels), args.batch_size):
            batch = labels[i:i+args.batch_size]
            results = Parallel(n_jobs=args.workers, backend="loky")(
                delayed(compute_one)(lab) for lab in batch
            )
            writer.writerows(results)
            fout.flush()
            processed += len(batch)
            dt = time.time() - t0
            print(f"[{processed}/{len(labels)}] processed in {dt:.1f}s")

    print(f"Done. Total time: {time.time()-t0:.1f}s")
    print(f"Output written to {out_path}")

if __name__ == "__main__":
    main()
