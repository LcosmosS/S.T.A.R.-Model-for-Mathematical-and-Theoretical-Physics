"""
Symbolic Regression Integration for Cosmology
=============================================

This module integrates symbolic regression models with the Cosmology engine.
It accepts a sympy expression or a string expression for H(z), and wraps it
into a Cosmology instance.

Used to test alternative expansion histories and Hubble tension resolutions.
"""

from __future__ import annotations
import sympy as sp
from src.physics.cosmology import Cosmology
import numpy as np

class SymbolicCosmology:
    """
    Wraps a symbolic regression model into a Cosmology engine.

    Parameters
    ----------
    H_expr : str or sympy.Expr
        Symbolic expression for H(z).
    params : dict
        Parameter dictionary for the expression.
    """

    def __init__(self, H_expr, params):
        if isinstance(H_expr, sp.Expr):
            H_expr = str(H_expr)

        self.H_expr = H_expr
        self.params = params

        self.cosmo = Cosmology(H_expr, params)

    def H(self, z):
    Hz = self._H_func(z)

    # Clamp negative sqrt arguments
    Hz = np.where(np.isfinite(Hz), Hz, np.nan)
    Hz = np.where(Hz < 0, np.nan, Hz)

    # Replace NaNs with a large penalty value
    Hz = np.where(np.isnan(Hz), 1e12, Hz)

    return Hz

    def distance_modulus(self, z):
        return self.cosmo.distance_modulus(z)

    def comoving_distance(self, z):
        return self.cosmo.comoving_distance(z)

    def luminosity_distance(self, z):
        return self.cosmo.luminosity_distance(z)

# ---------------------------------------------------------
    # Planck compressed likelihood support
    # ---------------------------------------------------------

    def ombh2(self):
        # If user did not include Ωb explicitly, assume 0.0224 (Planck)
        if "Ωb" in self.params:
            return self.params["Ωb"] * (self.params["H0"] / 100)**2
        return 0.0224  # fallback

    def comoving_distance(self, z):
        # Numerical integral of c/H(z)
        zs = np.linspace(0, z, 200)
        Hz = np.array([self.H(zi) for zi in zs])
        return np.trapz(299792.458 / Hz, zs)

    def sound_horizon(self):
        # Approximate r_s at drag epoch (Planck 2018)
        return 147.1  # Mpc

    def R(self):
        z_star = 1089.0
        r = self.comoving_distance(z_star)
        Om = self.params["Ωm"]
        H0 = self.params["H0"]
        return np.sqrt(Om) * H0 * r / 299792.458

    def lA(self):
        z_star = 1089.0
        r = self.comoving_distance(z_star)
        rs = self.sound_horizon()
        return np.pi * r / rs
