"""
Pantheon+ Full Dataset (embedded or loader stub)
"""
import numpy as np
import pandas as pd
from pathlib import Path

# Option 1: Embedded minimal placeholder (for testing)
PANTHEON_PLUS_FULL = {
    "z": np.array([0.01, 0.05, 0.1, 0.5, 1.0, 1.5]),   # redshifts
    "mu": np.array([32.5, 35.0, 37.8, 42.5, 44.8, 46.2]),  # distance moduli
    "mu_err": np.array([0.08, 0.10, 0.12, 0.18, 0.22, 0.25]),
    "name": "Pantheon+ Full",
    "n_sn": 1701,  # approximate real number
    "description": "Pantheon+ Type Ia Supernovae Compilation"
}

# Option 2 (better): Load from file if it exists
data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "pantheon_plus.csv"

if data_path.exists():
    df = pd.read_csv(data_path)
    PANTHEON_PLUS_FULL = df.to_dict('records')  # or keep as DataFrame
    print(f"Loaded Pantheon+ with {len(df)} supernovae")
else:
    print("Warning: Pantheon+ raw data not found. Using placeholder.")
