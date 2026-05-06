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

from __future__ import annotations
import numpy as np


class JointLikelihood:
    def __init__(self, planck_like, bao_like, cc_like):
        self.planck_like = planck_like
        self.bao_like = bao_like
        self.cc_like = cc_like
        print("JointLikelihood initialized with:")
        print(f"  - Planck: {type(planck_like)}")
        print(f"  - BAO:    {type(bao_like)}")
        print(f"  - CC:     {type(cc_like)}")

    def __call__(self, theta):
        """Compute total log-posterior with diagnostics"""
        try:
            H0, Om, OL, a, b = theta

            # Individual likelihoods
            logp_planck = self.planck_like(theta)
            logp_bao = self.bao_like(theta)
            logp_cc = self.cc_like(theta)

            total = logp_planck + logp_bao + logp_cc

            # === DIAGNOSTICS ===
            print(f"theta = [{H0:.3f}, {Om:.4f}, {OL:.4f}, {a:.5f}, {b:.5f}]")
            print(f"  Planck logp = {logp_planck:.4f}")
            print(f"  BAO    logp = {logp_bao:.4f}")
            print(f"  CC     logp = {logp_cc:.4f}")
            print(f"  TOTAL  logp = {total:.4f}")

            if not np.isfinite(total):
                print("  → WARNING: Non-finite posterior detected!")
                print(f"     Planck finite? {np.isfinite(logp_planck)}")
                print(f"     BAO finite?    {np.isfinite(logp_bao)}")
                print(f"     CC finite?     {np.isfinite(logp_cc)}")

            return total

        except Exception as e:
            print(f"ERROR in JointLikelihood: {e}")
            return -np.inf

    def log_likelihood(self, model):
        lp = self.planck_shoes.log_likelihood(model)
        lb = self.desi_bao.log_likelihood(model)
        lc = self.cc.log_likelihood(model)
        return lp + lb + lc
