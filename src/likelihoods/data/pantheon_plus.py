"""
Pantheon+ loader and module export.
Produces PANTHEON_PLUS_FULL as a dict of lists:
{
  "z": [...],
  "mu": [...],
  "sigma_mu": [...]
}
"""

from pathlib import Path
import pandas as pd
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def _find_repo_root(start_path: Path) -> Path:
    """
    Walk upward from start_path and return the first directory that looks like the repo root.
    Looks for .git, pyproject.toml, setup.cfg, or README.md as markers.
    Falls back to parents[3] if nothing is found.
    """
    markers = {".git", "pyproject.toml", "setup.cfg", "README.md", "README.rst", "README.md"}
    for parent in [start_path] + list(start_path.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent
    # conservative fallback: go up 3 levels from module (handles src/likelihoods/data)
    try:
        return start_path.parents[3]
    except IndexError:
        return start_path.resolve().parents[-1]

def load_pantheon_plus():
    # compute repo root relative to this file
    module_file = Path(__file__).resolve()
    repo_root = _find_repo_root(module_file.parent)
    csv_path = repo_root / "data" / "processed" / "pantheon_plus.csv"

    if not csv_path.exists():
        # helpful debug message for CI logs
        logger.warning("Pantheon+ CSV not found at %s", csv_path)
        # also log the repo_root and a short listing to help debugging
        try:
            listing = [p.name for p in (repo_root / "data").iterdir()]
        except Exception:
            listing = None
        logger.debug("Repo root resolved to %s; data/ listing: %s", repo_root, listing)
        raise FileNotFoundError(f"Pantheon+ CSV not found at {csv_path}")

    # load CSV as before (example using pandas)
    import pandas as pd
    df = pd.read_csv(csv_path)
    return df

    # Read as a comma-separated CSV 
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error("Failed to read Pantheon+ CSV: %s", e)
        return {"z": [], "mu": [], "sigma_mu": []}

    # If the CSV uses different column names, try to normalize
    rename_map = {
        "zHD": "z", "zCMB": "z", "zHEL": "z",
        "m_b_corr": "mu", "MU_SH0ES": "mu",
        "m_b_corr_err_DIAG": "sigma_mu", "MU_SH0ES_ERR_DIAG": "sigma_mu",
        "dmu": "sigma_mu"
    }
    df = df.rename(columns=rename_map)

    # If headerless CSV was written, try to recover first three columns
    if not set(["z", "mu", "sigma_mu"]).issubset(df.columns):
        # If the first three columns exist, assume they are z, mu, sigma_mu
        if df.shape[1] >= 3 and all(c.startswith("Unnamed") for c in df.columns[:3]):
            df = df.iloc[:, :3]
            df.columns = ["z", "mu", "sigma_mu"]

    # Keep only required columns if present
    if not set(["z", "mu", "sigma_mu"]).issubset(df.columns):
        logger.error("Pantheon+ CSV missing required columns. Available: %s", list(df.columns))
        return {"z": [], "mu": [], "sigma_mu": []}

    df = df[["z", "mu", "sigma_mu"]].copy()

    # Coerce to numeric and drop invalid rows
    for col in ["z", "mu", "sigma_mu"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    before = len(df)
    df = df.dropna().reset_index(drop=True)
    after = len(df)
    if after < before:
        logger.info("Dropped %d rows with non-numeric or missing values from Pantheon+ CSV", before - after)

    # Final sanity checks
    if df.empty:
        logger.error("Pantheon+ CSV contains no valid numeric rows after cleaning.")
        return {"z": [], "mu": [], "sigma_mu": []}

    return {
        "z": df["z"].astype(float).tolist(),
        "mu": df["mu"].astype(float).tolist(),
        "sigma_mu": df["sigma_mu"].astype(float).tolist()
    }

# Module-level export used by the rest of the codebase
PANTHEON_PLUS_FULL = load_pantheon_plus()
