"""
Paper Figures Pipeline
======================

Automatically generates all figures needed for a cosmology paper:
- Hubble diagram
- H(z) comparison
- Distance modulus comparison
- Residuals
- Corner plot
- Parameter constraints table
"""

from __future__ import annotations
import pandas as pd
import numpy as np

from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology
from src.visualization.paper_figures import (
    plot_hubble_diagram, plot_Hz, plot_residuals
)
from src.visualization.joint_corner_plot import plot_joint_corner
from src.analysis.star_constraints_table import summarize_chain, to_markdown_table


class PaperFiguresPipeline:
    def __init__(self, chain, param_names, H_expr, data_paths):
        """
        data_paths: dict with keys:
            - planck
            - bao
            - cc
        """
        self.chain = chain
        self.param_names = param_names
        self.H_expr = H_expr
        self.data_paths = data_paths

    def best_fit_model(self):
        params = dict(zip(self.param_names, self.chain.mean(axis=0)))
        return SymbolicCosmology(self.H_expr, params)

    def lcdm_model(self):
        return Cosmology(
            "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
            {"H0": 67.4, "Ωm": 0.315, "ΩΛ": 0.685}
        )

    def run(self, output_dir="paper_figures"):
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Load Planck data
        planck_data = self.data_paths["planck"]
        if isinstance(planck_data, str):
            df_planck = pd.read_csv(planck_data)
        else:
            df_planck = pd.DataFrame(planck_data))

        # Build models
        star = self.best_fit_model()
        lcdm = self.lcdm_model()

        # Generate figures
        plot_hubble_diagram(df_planck, lcdm, star)
        plot_Hz([lcdm, star], ["ΛCDM", "S.T.A.R."])
        plot_residuals(df_planck, lcdm, star)

        # Corner plot
        plot_joint_corner(self.chain, self.param_names,
                          save_path=f"{output_dir}/corner_plot.png")

        # Constraints table
        df_constraints = summarize_chain(self.chain, self.param_names)
        with open(f"{output_dir}/constraints.md", "w") as f:
            f.write(to_markdown_table(df_constraints))

        return df_constraints
