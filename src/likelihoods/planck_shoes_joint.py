"""
Planck + SH0ES Joint Likelihood
===============================

Combines:
- Planck 2018 compressed distance priors
- SH0ES H0 measurement

Used to constrain cosmological models and quantify Hubble tension.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from src.physics.symbolic_cosmology import SymbolicCosmology


class PlanckSH0ESJointLikelihood:
    def __init__(self, planck_csv, H0_shoes=73.04, sigma_shoes=1.04):
        """
        Parameters
        ----------
        planck_csv : str
            Path to Planck distance priors CSV
        H0_shoes : float
            SH0ES central H0 value
        sigma_shoes : float
            SH0ES uncertainty
        """
        self.planck = pd.read_csv(planck_csv)
        self.H0_shoes = H0_shoes
        self.sigma_shoes = sigma_shoes

    def log_likelihood_planck(self, model):
        z = self.planck["z"].values
        mu_obs = self.planck["mu"].values
        sigma = self.planck["sigma_mu"].values

        mu_model = np.array([model.distance_modulus(zi) for zi in z])
        chi2 = np.sum(((mu_obs - mu_model) / sigma)**2)
        return -0.5 * chi2

    def log_likelihood_shoes(self, model):
        H0_model = model.H(0)
        return -0.5 * ((H0_model - self.H0_shoes) / self.sigma_shoes)**2

    def log_likelihood(self, model):
        return self.log_likelihood_planck(model) + self.log_likelihood_shoes(model)
