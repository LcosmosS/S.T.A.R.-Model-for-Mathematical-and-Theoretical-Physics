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

def load_pantheon_plus():
    raw_dir = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
    dat_file = raw_dir / "pantheon_plus.csv"

    if not dat_file.exists():
        # Safe placeholder (dict of lists) so imports never fail
        return {
            "z": [],
            "mu": [],
            "sigma_mu": []
        }

    # Read with first line as header
    df = pd.read_csv(dat_file, delim_whitespace=True, comment='#', header=0)

    # Map to expected names
    rename_map = {
        "zHD": "z",
        "zCMB": "z",
        "m_b_corr": "mu",
        "MU_SH0ES": "mu",
        "m_b_corr_err_DIAG": "sigma_mu",
        "MU_SH0ES_ERR_DIAG": "sigma_mu",
        "dmu": "sigma_mu"
    }
    df = df.rename(columns=rename_map)

    # Force required columns (use available alternatives)
    if "z" not in df.columns:
        df["z"] = df.get("zHD", df.get("zCMB"))
    if "mu" not in df.columns:
        df["mu"] = df.get("m_b_corr", df.get("MU_SH0ES"))
    if "sigma_mu" not in df.columns:
        df["sigma_mu"] = df.get("m_b_corr_err_DIAG", df.get("MU_SH0ES_ERR_DIAG"))

    # Keep only required columns and drop rows with missing values
    df = df[["z", "mu", "sigma_mu"]].dropna()

    # Convert to lists (dict-of-lists) — 
    return {
        "z": df["z"].astype(float).tolist(),
        "mu": df["mu"].astype(float).tolist(),
        "sigma_mu": df["sigma_mu"].astype(float).tolist()
    }

# Module-level export used by the rest of the codebase
PANTHEON_PLUS_FULL = load_pantheon_plus()



