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
        """theta must be parameter vector"""
        theta = np.asarray(theta, dtype=float).flatten()
        
        try:
            logp_planck = self.planck_like(theta)   # pass theta, not model
            logp_bao    = self.bao_like(theta)
            logp_cc     = self.cc_like(theta)
            
            total = logp_planck + logp_bao + logp_cc
            
            print(f"  Planck: {logp_planck:.4f} | BAO: {logp_bao:.4f} | CC: {logp_cc:.4f} | Total: {total:.4f}")
            return total if np.isfinite(total) else -np.inf
            
        except Exception as e:
            print(f"JointLikelihood ERROR: {e}")
            return -np.inf
