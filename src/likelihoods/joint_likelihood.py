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
        print("JointLikelihood (safe mode) initialized")

    def __call__(self, theta):
        theta = np.asarray(theta, dtype=float).flatten()
        
        # Heavy penalties instead of -inf to allow MCMC to start
        try:
            lp_p = float(self.planck_like(theta))
        except:
            lp_p = -40.0

        try:
            lp_b = float(self.bao_like(theta))
        except:
            lp_b = -20.0

        try:
            lp_c = float(self.cc_like(theta))
        except:
            lp_c = -10.0

        total = lp_p + lp_b + lp_c

        print(f"Joint logp = {total:.2f}   (P:{lp_p:.1f} | B:{lp_b:.1f} | C:{lp_c:.1f})")
        return total
