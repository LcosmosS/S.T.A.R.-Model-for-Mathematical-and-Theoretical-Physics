"""
Cosmic Chronometer Likelihood
=============================

Gaussian likelihood for H(z) measurements from cosmic chronometers.
"""

from __future__ import annotations
import numpy as np
import pandas as pd


class CosmicChronometers:
    """
    Cosmic Chronometer H(z) likelihood.

    Supports:
    - embedded Python dictionaries (your CI-safe data modules)
    - pandas DataFrames (legacy CSV workflows)

    Provides:
    - strict validation
    - vectorized Gaussian log-likelihood
    - numerical stability checks
    - API compatibility with DESIBAO and PlanckSH0ESJointLikelihood
    """

    def __init__(self, data):
        """
        Parameters
        ----------
        data : dict or pandas.DataFrame
            Must contain keys/columns: "z", "H", "sigma".
        """
        self.z, self.H, self.sigma = self._parse_and_validate(data)

    # ------------------------------------------------------------------
    # Parsing + Validation
    # ------------------------------------------------------------------
    def _parse_and_validate(self, data):
        # Accept dict or DataFrame
        if isinstance(data, dict):
            try:
                z = np.asarray(data["z"], dtype=float)
                H = np.asarray(data["H"], dtype=float)
                sigma = np.asarray(data["sigma"], dtype=float)
            except KeyError as e:
                raise KeyError(f"Missing required key in CC data: {e}")
        elif isinstance(data, pd.DataFrame):
            for key in ["z", "H", "sigma"]:
                if key not in data.columns:
                    raise KeyError(f"Missing required column '{key}' in CC DataFrame")
            z = data["z"].to_numpy(dtype=float)
            H = data["H"].to_numpy(dtype=float)
            sigma = data["sigma"].to_numpy(dtype=float)
        else:
            raise TypeError(
                "CosmicChronometers data must be a dict or pandas.DataFrame"
            )

        # Shape validation
        if not (z.shape == H.shape == sigma.shape):
            raise ValueError(
                f"Shape mismatch: z {z.shape}, H {H.shape}, sigma {sigma.shape}"
            )

        # Finite values
        if not np.all(np.isfinite(z)):
            raise ValueError("Non-finite values detected in CC redshifts z")
        if not np.all(np.isfinite(H)):
            raise ValueError("Non-finite values detected in CC H(z) measurements")
        if not np.all(np.isfinite(sigma)):
            raise ValueError("Non-finite values detected in CC uncertainties sigma")

        # Positive uncertainties
        if np.any(sigma <= 0):
            raise ValueError("All CC sigma values must be strictly positive")

        return z, H, sigma

    # ------------------------------------------------------------------
    # Log-likelihood
    # ------------------------------------------------------------------
    def log_likelihood(self, model):
        """
        Gaussian log-likelihood:

            -0.5 * sum( ((H_obs - H_model) / sigma)^2 )

        Parameters
        ----------
        model : SymbolicCosmology or compatible object
            Must implement H(z_array) -> array of predicted H(z).

        Returns
        -------
        float
        """
        # Vectorized model prediction
        H_model = np.asarray(model.H(self.z), dtype=float)

        if H_model.shape != self.H.shape:
            raise ValueError(
                f"Model.H(z) returned shape {H_model.shape}, expected {self.H.shape}"
            )

        # Numerical stability: ensure finite predictions
        if not np.all(np.isfinite(H_model)):
            raise ValueError("Model returned non-finite H(z) values")

        # Residuals
        resid = (self.H - H_model) / self.sigma

        # Gaussian log-likelihood
        chi2 = np.sum(resid * resid)
        return -0.5 * chi2

    # ------------------------------------------------------------------
    # Optional helper for debugging / consistency
    # ------------------------------------------------------------------
    @property
    def ndata(self):
        """Number of CC data points."""
        return self.z.size

    def __repr__(self):
        return f"CosmicChronometers(ndata={self.ndata})"
