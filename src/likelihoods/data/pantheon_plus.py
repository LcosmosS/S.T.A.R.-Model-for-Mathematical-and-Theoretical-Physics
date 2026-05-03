"""
Pantheon+ Loader 
"""
from pathlib import Path
import pandas as pd

def load_pantheon_plus():
    raw_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    dat_file = raw_dir / "pantheon_plus.dat"
    
    if dat_file.exists():
        # Read Pantheon+ .dat format (space-separated, header on first line)
        df = pd.read_csv(dat_file, delim_whitespace=True, comment='#', header=0)
        
        # Standardize to what the pipeline expects
        df = df.rename(columns={
            'zHD': 'z',
            'm_b_corr': 'mu',
            'm_b_corr_err_DIAG': 'sigma_mu',
            'MU_SH0ES': 'mu',           # alternative
            'MU_SH0ES_ERR_DIAG': 'sigma_mu'
        })
        
        # Ensure required columns
        if 'z' not in df.columns:
            df['z'] = df.get('zHD', df.get('zCMB', 0.0))
        if 'mu' not in df.columns:
            df['mu'] = df.get('m_b_corr', df.get('MU_SH0ES', 0.0))
        if 'sigma_mu' not in df.columns:
            df['sigma_mu'] = df.get('m_b_corr_err_DIAG', df.get('MU_SH0ES_ERR_DIAG', 0.15))
        
        print(f"Loaded real Pantheon+ with {len(df)} supernovae")
        return df.to_dict('index')   # dict format required by pipeline
    
    # Placeholder fallback
    print("Using Pantheon+ placeholder")
    return {
        0: {"z": 0.01, "mu": 32.5, "sigma_mu": 0.08},
        1: {"z": 0.05, "mu": 35.0, "sigma_mu": 0.10},
        2: {"z": 0.1,  "mu": 37.8, "sigma_mu": 0.12},
    }

PANTHEON_PLUS_FULL = load_pantheon_plus()
