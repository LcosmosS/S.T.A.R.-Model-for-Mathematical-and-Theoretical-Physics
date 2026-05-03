from __future__ import annotations
import numpy as np
import sympy as sp
from scipy.integrate import quad


class Cosmology:
    """
    Cosmology engine with pluggable symbolic H(z).

    H_expr : str
        Sympy-compatible expression for H(z) (units: km/s/Mpc).
    params : dict
        Numeric parameter values used in H_expr.
    """

    c = 299792.458  # Lightspeed in km/s

    def __init__(self, H_expr: str, params: dict):
        self.H_expr = H_expr
        self.params = params.copy() if params is not None else {}

        # symbolic variable and expression
        z = sp.symbols("z")
        try:
            self.H_sym = sp.sympify(H_expr)
        except Exception as e:
            raise ValueError(f"Failed to parse H_expr {H_expr!r}: {e}")

        # lambdify: (z, *params) -> numeric
        try:
            self.H = sp.lambdify((z, *self.params.keys()), self.H_sym, modules=["numpy"])
        except Exception as e:
            raise RuntimeError(f"Failed to lambdify H_expr: {e}")

    def H_of_z(self, z):
        """Evaluate H(z) numerically for scalar or array-like z."""
        try:
            vals = self.H(z, *self.params.values())
        except Exception as e:
            raise RuntimeError(f"H(z) evaluation error at z={z!r}: {e}")

        # Convert to numpy array for checks
        vals_arr = np.asarray(vals)

        # If lambdify returned an object array with Ellipsis or None, fail clearly
        if vals_arr.dtype == object:
            # try to detect Ellipsis or None inside
            if np.any([v is Ellipsis or v is None for v in vals_arr.ravel()]):
                raise RuntimeError("H(z) evaluation returned Ellipsis or None; check symbolic expression and params.")
        # Ensure numeric
        try:
            vals_float = vals_arr.astype(float)
        except Exception:
            raise RuntimeError("H(z) did not produce numeric values; check expression and parameter types.")

        return vals_float

    def _comoving_scalar(self, zi: float) -> float:
        """Compute comoving distance for a single scalar zi."""
        if not np.isfinite(zi):
            raise ValueError(f"Invalid redshift z={zi!r}; must be finite.")
        if zi < 0:
            raise ValueError(f"Invalid redshift z={zi!r}; must be non-negative.")

        def integrand(zp):
            try:
                Hz = self.H_of_z(zp)
            except Exception as e:
                raise RuntimeError(f"H(z) evaluation failed at z={zp}: {e}")

            # H_of_z returns numpy scalar/array; ensure scalar
            Hz_val = np.asarray(Hz).ravel()[0]
            if not np.isfinite(Hz_val):
                raise RuntimeError(f"H(z) is not finite at z={zp}: {Hz_val!r}")
            if Hz_val <= 0.0:
                raise RuntimeError(f"H(z) must be positive; got {Hz_val!r} at z={zp}")
            return self.c / float(Hz_val)

        try:
            result, err = quad(integrand, 0.0, float(zi), limit=200)
        except Exception as e:
            raise RuntimeError(f"Integration of 1/H(z) failed for z={zi}: {e}")

        if not np.isfinite(result):
            raise RuntimeError(f"Integration produced non-finite result for z={zi}: {result!r}")

        return float(result)

    def comoving_distance(self, z):
        """
        Dc(z) = c * ∫_0^z dz' / H(z').
        Accepts scalar or array-like z. Returns float for scalar input or np.ndarray for array input.
        """
        # Convert input to numpy array
        try:
            z_arr = np.asarray(z)
        except Exception as e:
            raise TypeError(f"Could not convert z to array-like: {e}")

        # Scalar input
        if z_arr.ndim == 0:
            return self._comoving_scalar(float(z_arr))

        # Array input: compute elementwise (preserve shape)
        flat = z_arr.ravel()
        out = np.empty_like(flat, dtype=float)
        for i, zi in enumerate(flat):
            out[i] = self._comoving_scalar(float(zi))
        return out.reshape(z_arr.shape)

    def luminosity_distance(self, z):
        """
        DL(z) = (1+z) * Dc(z).
        Accepts scalar or array-like z and returns same shape as input.
        """
        Dc = self.comoving_distance(z)
        z_arr = np.asarray(z)
        try:
            DL = (1.0 + z_arr) * Dc
        except Exception as e:
            raise RuntimeError(f"Failed to compute luminosity distance for z={z!r}: {e}")

        # Validate positive distances
        if np.any(np.asarray(DL) <= 0):
            raise RuntimeError("Luminosity distance must be positive to compute distance modulus.")
        return DL

    def angular_diameter_distance(self, z):
        """DA = Dc / (1+z)."""
        Dc = self.comoving_distance(z)
        z_arr = np.asarray(z)
        try:
            DA = Dc / (1.0 + z_arr)
        except Exception as e:
            raise RuntimeError(f"Failed to compute angular diameter distance for z={z!r}: {e}")
        return DA

    def distance_modulus(self, z):
        """μ = 5 log10(DL / 10 pc). DL in Mpc."""
        DL_Mpc = self.luminosity_distance(z)
        DL_pc = DL_Mpc * 1e6
        # final validation
        if np.any(np.asarray(DL_pc) <= 0):
            raise RuntimeError("Luminosity distance must be positive to compute distance modulus.")
        return 5.0 * (np.log10(DL_pc) - 1.0)
