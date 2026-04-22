

# **Arithmetic–Cosmic Structure Conjecture (ACSC) 
---
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LcosmosS/Arithmetic-Cosmic-Structure-Conjecture-ACSC-.git/HEAD) 
---

Author: Patrick J. McNamara

Date: Beginning in March 2025 - Present

Keywords: Number Theory, Cosmology, Persistent Homology, Elliptic Curves, Symbolic Regression, Mathematical Physics

Overview
This repository serves as the foundational archive for The Arithmetic–Cosmic Structure Conjecture (ACSC). It houses the complete 166-page theoretical monograph, which proposes a profound structural symmetry: that the topological blueprint of the large-scale universe is mathematically predetermined by the arithmetic invariants of elliptic curves over the rational numbers Q.

This work suggests that the universe operates as a "Symbolic Field," where physical constants and geometric realities emerge not by chance or anthropic selection, but by strict number-theoretic necessity.

The Core Conjecture
At the heart of the ACSC is the proposition of a metric-preserving correspondence between arithmetic classes of elliptic curves (E) and the topological classes of cosmic structures (M 
cosmo
​
 ).

Let E denote the set of isomorphism classes of elliptic curves over Q. We propose a projection:

Φ:E⟶M 
cosmo
​
 
assigning to each curve a point in a 3‑manifold M 
cosmo
​
 ⊂R 
3
  representing the large‑scale topology of observed cosmic structure.

The conjecture posits that the projected point cloud Φ(E) reconstructs the persistent homology of M 
cosmo
​
  with an error bound of W 
2
​
 (D(Φ(E)),D(M 
cosmo
​
 ))<ϵ, where ϵ<10 
−2
 .

The ACSC Trilogy Architecture
This repository contains the Foundational Theory of a broader three-part research program. To fully contextualize this work, reviewers and researchers should reference the complete trilogy:

ACSC - Theory (This Repository): The Foundational Monograph (166 pages). Establishes the core theoretical correspondence, the projection map Φ, and the category theory frameworks unifying arithmetic and cosmology.

ECC - Dynamics (Repository Link): The Entropy Cohomology Conjecture. Provides the mechanistic theory and cohomological conservation laws (dω=0) that make the ACSC correspondence dynamically necessary rather than accidental.

S.T.A.R. - Empirical (Repository Link): Arithmetic Invariants and Cosmological Geometry in Cartography. The empirical validation of the theory, demonstrating a 0.9864 R 
2
  correlation using symbolic regression and introducing the Global-to-Local Mapping Paradox Correction Theory (GLMPCT).

Repository Structure

```bash
Arithmetic-Cosmic-Structure-Conjecture-ACSC/
├── README.md
├── LICENSE
├── CITATION.cff
├── acsc/                          # Core Python package
│   ├── __init__.py
│   ├── core.py                    # Complexity-14 filter, scarcity functions
│   ├── validation.py              # Rank consistency, statistics
│   └── utils.py
├── data/
│   ├── raw/
│   │   ├── cremona_raw_parsed.csv
│   │   └── lmfdb_raw_parsed.csv
│   └── processed/
│       ├── cremona_3selmer_full_pari.csv
│       ├── lmfdb_3selmer_full_pari.csv
│       └── acsc_final_combined.csv
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_complexity14_filter.ipynb
│   └── 03_acsc_statistics.ipynb
├── scripts/
│   ├── generate_raw.py
│   ├── compute_3selmer_full_pari.py
│   └── acsc_validation_batch.py
├── results/
│   ├── figures/
│   │   └── acsc_scarcity_plot.png
│   └── tables/
├── docker/
│   └── Dockerfile
├── requirements.txt
└── pyproject.toml                 # or setup.py

/manuscript: Contains the full 166-page ACSC Monograph (PDF) and the original LaTeX source files for complete transparency and peer-review verification.

/theory-verification: Includes foundational data subsets (from LMFDB and Cremona databases) and the persistent homology barcode scripts utilized to define the arithmetic point clouds.

/docs: High-resolution diagrams, including the "Cosmic-Arithmetic Map," visually demonstrating the translation of rank and regulator into cosmic voids and filaments.

Reproducibility Statement
Transparency and empirical reproducibility are core tenets of this research program. The theoretical projections defined in this monograph are computationally verified in the accompanying S.T.A.R. repository. The R 
2
 =0.9864 predictive parity on synthetic cosmic structures was achieved using a v3.1 leakage-free pipeline. Researchers are encouraged to review the .tex formulations in the /manuscript folder here, and execute the data pipelines provided in the S.T.A.R. repository to independently verify the projection mappings.

Citation
If you utilize the theoretical frameworks, projection operators, or data pipelines established in this program, please cite the monograph as follows:

McNamara, P. J. (2025). The Arithmetic–Cosmic Structure Conjecture. GitHub Repository. https://github.com/LcosmosS/Arithmetic-Cosmic-Structure-Conjecture-ACSC
### How to Reproduce

```bash
# 1. Clone and install
git clone https://github.com/LcosmosS/Arithmetic-Cosmic-Structure-Conjecture-ACSC.git
cd Arithmetic-Cosmic-Structure-Conjecture-ACSC
pip install -r requirements.txt

# 2. Run the full ACSC validation (batching + incremental save)
python scripts/acsc_validation_full_batch.py

@misc{mcnamara2025acsc,
  author = {Patrick J. McNamara - ORCiD: 0009-0002-8978-5563},
  title = {Arithmetic--Cosmic Structure Conjecture (ACSC)},
  year = {2025},
  howpublished = {\url{https://github.com/LcosmosS/Arithmetic-Cosmic-Structure-Conjecture-ACSC}},
  note = {Part of the S.T.A.R. Program for Theoretical Physics}
}
