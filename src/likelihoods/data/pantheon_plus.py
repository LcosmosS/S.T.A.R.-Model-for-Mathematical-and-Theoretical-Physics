"""
Pantheon+ Full Dataset Loader
"""
from pathlib import Path
import pandas as pd

def load_pantheon_plus():
    raw_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    dat_file = raw_dir / "pantheon_plus.dat"
    
    if dat_file.exists():
        df = pd.read_csv(dat_file, delim_whitespace=True, comment='#')
        
        # Standardize column names
        if 'mu_err' in df.columns and 'sigma_mu' not in df.columns:
            df = df.rename(columns={'mu_err': 'sigma_mu'})
        
        # Return as dict (matching PLANCK_2015 style)
        return df.to_dict('index')   # or 'records' — test both if needed
    
    # Placeholder fallback
    print("Warning: Using Pantheon+ placeholder")
    return {
        0: {"z": 0.01, "mu": 32.5, "sigma_mu": 0.08},
        1: {"z": 0.05, "mu": 35.0, "sigma_mu": 0.10},
        2: {"z": 0.1,  "mu": 37.8, "sigma_mu": 0.12},
        3: {"z": 0.5,  "mu": 42.5, "sigma_mu": 0.18},
        4: {"z": 1.0,  "mu": 44.8, "sigma_mu": 0.22},
    }

PANTHEON_PLUS_FULL = load_pantheon_plus()
