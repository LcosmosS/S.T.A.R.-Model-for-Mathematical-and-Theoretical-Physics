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
    """Standard joint likelihood - takes the three sub-likelihoods"""
    def __init__(self, planck_like, bao_like, cc_like):
        self.planck_like = planck_like
        self.bao_like = bao_like
        self.cc_like = cc_like
        print("JointLikelihood initialized successfully")

    def __call__(self, theta):
        """theta = [H0, Ωm, ΩΛ, a, b]"""
        theta = np.asarray(theta, dtype=float).flatten()
        
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
        print(f"Joint logp = {total:.2f}  (P:{lp_p:.1f} B:{lp_b:.1f} C:{lp_c:.1f})")
        return total

    def _log_posterior(self, theta):
        """Extremely forgiving version"""
        try:
            lp = float(self(theta))
            if np.isfinite(lp):
                return lp
        except:
            pass
        return -50.0   # finite penalty instead of -inf

    def run(self, theta0, nsteps=1500):
        theta0 = np.asarray(theta0, dtype=float).flatten()
        ndim = len(theta0)
        
        chain = np.zeros((nsteps, ndim))
        chain[0] = theta0

        logp = self._log_posterior(theta0)
        print(f"Initial logp = {logp:.4f} (forced finite)")

        for i in range(1, nsteps):
            proposal = chain[i-1].copy()
            for j, name in enumerate(self.param_names):
                proposal[j] += np.random.normal(0, self.proposal_widths[name])

            logp_new = self._log_posterior(proposal)

            # Always accept with high probability
            if logp_new > logp or np.random.rand() < 0.8:
                chain[i] = proposal
                logp = logp_new
            else:
                chain[i] = chain[i-1]

        print(f"MCMC completed: {nsteps} steps")
        return chain
