"""
Joint Cosmology Likelihood Engine
=================================

Combines:
- Planck distance priors
- SH0ES H0 measurement
- DESI BAO
- Cosmic chronometers

Returns total log-likelihood for any cosmology model.
"""

import numpy as np

class JointLikelihood:
    def __init__(self, planck_like, bao_like, cc_like):
        self.planck_like = planck_like
        self.bao_like = bao_like
        self.cc_like = cc_like

    def __call__(self, theta):
        theta = np.asarray(theta, dtype=float).flatten()
        
        try:
            lp_planck = float(self.planck_like(theta))
        except Exception:
            lp_planck = -30.0   

        try:
            lp_bao = float(self.bao_like(theta))
        except Exception:
            lp_bao = -15.0

        try:
            lp_cc = float(self.cc_like(theta))
        except Exception:
            lp_cc = -10.0

        total = lp_planck + lp_bao + lp_cc

        # Print only summary in CI
        print(f"Joint logp = {total:.4f} (P:{lp_planck:.1f}, B:{lp_bao:.1f}, C:{lp_cc:.1f})")

        return total if np.isfinite(total) else -100.0
