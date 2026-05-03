"""
Paper-Ready Cosmology Figures
=============================

Generates:
- Hubble diagram
- H(z) curves
- Distance modulus curves
- Residuals
- Posterior corner plots
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def _ensure_outdir(output_dir):
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

def plot_hubble_diagram(df, lcdm, star, output_dir=None):
    """
    Plot distance modulus vs redshift and save to output_dir if provided.
    Signature: plot_hubble_diagram(df, lcdm, star, output_dir=None)
    """
    _ensure_outdir(output_dir)

    z = np.array(df["z"])
    mu_obs = np.array(df["mu"])
    sigma = np.array(df["sigma_mu"])

    # Compute model distance moduli
    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    plt.figure(figsize=(10, 6))
    plt.errorbar(z, mu_obs, yerr=sigma, fmt=".", label="Pantheon+", alpha=0.6)
    plt.plot(z, mu_lcdm, label="ΛCDM", color="C1")
    plt.plot(z, mu_star, label="S.T.A.R.", color="C2", linestyle="--")
    plt.xscale("log")
    plt.xlabel("z")
    plt.ylabel("Distance modulus μ")
    plt.legend()
    plt.tight_layout()

    if output_dir:
        outpath = os.path.join(output_dir, "hubble_diagram.png")
        plt.savefig(outpath, dpi=200)
    plt.close()


def plot_residuals(df, lcdm, star, output_dir=None):
    """
    Plot residuals (data - model) for ΛCDM and S.T.A.R.
    Signature: plot_residuals(df, lcdm, star, output_dir=None)
    """
    _ensure_outdir(output_dir)

    z = np.array(df["z"])
    mu_obs = np.array(df["mu"])
    sigma = np.array(df["sigma_mu"])

    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    res_lcdm = mu_obs - mu_lcdm
    res_star = mu_obs - mu_star

    plt.figure(figsize=(10, 4))
    plt.errorbar(z, res_lcdm, yerr=sigma, fmt=".", label="Data - ΛCDM", alpha=0.6)
    plt.errorbar(z, res_star, yerr=sigma, fmt=".", label="Data - S.T.A.R.", alpha=0.6)
    plt.xscale("log")
    plt.axhline(0, color="k", lw=0.8)
    plt.xlabel("z")
    plt.ylabel("Residual μ (mag)")
    plt.legend()
    plt.tight_layout()

    if output_dir:
        outpath = os.path.join(output_dir, "residuals.png")
        plt.savefig(outpath, dpi=200)
    plt.close()


def plot_Hz(models, labels, output_dir=None):
    """
    Plot H(z) for a list of model objects over a redshift grid.
    Signature: plot_Hz(models, labels, output_dir=None)
    """
    _ensure_outdir(output_dir)

    zgrid = np.linspace(0.001, 2.5, 300)
    plt.figure(figsize=(8, 5))
    for model, lab in zip(models, labels):
        Hz = np.array([model.H(z) for z in zgrid])
        plt.plot(zgrid, Hz, label=lab)
    plt.xlabel("z")
    plt.ylabel("H(z) [km/s/Mpc]")
    plt.legend()
    plt.tight_layout()

    if output_dir:
        outpath = os.path.join(output_dir, "Hz_comparison.png")
        plt.savefig(outpath, dpi=200)
    plt.close()
