import os
import re

# Path to repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ECDATA_ROOT = os.path.join(REPO_ROOT, "data", "ecdata")

LABEL_RE = re.compile(r"(\d+)([a-z]+)(\d+)$")


def extract_labels_from_ecdata():
    """
    Walk data/ecdata/<N>/<iso>/<label>
    and collect all valid Cremona labels.
    """
    labels = []

    for N in sorted(
        os.listdir(ECDATA_ROOT), key=lambda x: int(x) if x.isdigit() else x
    ):
        N_path = os.path.join(ECDATA_ROOT, N)
        if not os.path.isdir(N_path):
            continue

        for iso in sorted(os.listdir(N_path)):
            iso_path = os.path.join(N_path, iso)
            if not os.path.isdir(iso_path):
                continue

            for fname in sorted(os.listdir(iso_path)):
                # Expect filenames like "11a1", "37b2", etc.
                if LABEL_RE.match(fname):
                    labels.append(fname)

    return labels


def main():
    labels = extract_labels_from_ecdata()

    # Sort lexicographically for reproducibility
    labels = sorted(labels)

    # Print first 1000 labels
    for L in labels[:1000]:
        print(L)


if __name__ == "__main__":
    main()
