

# **Arithmetic–Cosmic Structure Conjecture (ACSC) — Reproducible Pipeline**
---
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LcosmosS/Arithmetic-Cosmic-Structure-Conjecture-ACSC-.git/HEAD)
---
This repository contains the full computational framework for testing the **Arithmetic–Cosmic Structure Conjecture (ACSC)**: a proposed structural correspondence between the arithmetic invariants of elliptic curves over ℚ and the large‑scale topology of cosmic structure.

The code, data pipeline, and documentation here implement the preregistered falsification protocol described in the manuscript *“The Arithmetic–Cosmic Structure Conjecture (ACSC)”*. All steps—from data ingestion to projection, quantile alignment, TDA computation, null models, and statistical testing—are fully reproducible.

---

## **1. Overview**

The ACSC asserts that after applying a stable, rank‑normalized projection 

𝛟_prime : E → ℝ3 

to elliptic curves E/ℚ, and aligning the resulting point cloud to observational cosmic data via a non‑linear quantile transform, the persistent homology of the arithmetic cloud approximates that of the cosmic web with bounded error.

This repository provides:

- A complete implementation of the projection family (primary + alternatives)  
- Quantile alignment tools  
- TDA pipeline (GUDHI/Ripser)  
- Null models A–D  
- Statistical tests and decision rules  
- Ablation and robustness experiments  
- Reproducible environment (Dockerfile, requirements, notebooks)

---

## **2. Repository Structure**

```
acsc/
│
├── data/
│   ├── arithmetic/              # Cremona/LMFDB exports & Sage tables
│   ├── cosmic/                  # SDSS/DESI volume-limited samples
│   └── derived/                 # Projected clouds, aligned clouds, diagrams
│
├── acsc/
│   ├── __init__.py
│   ├── projection.py            # Φ_primary, PTD, MCJ implementations
│   ├── quantile.py              # Non-linear quantile transformer
│   ├── tda_pipeline.py          # VR complexes, persistence diagrams
│   ├── statistics.py            # W2 distances, p-values, BH correction
│   ├── null_models.py           # Null-A, Null-B, Null-C, Null-D
│   ├── robustness.py            # Subsampling, jitter, parameter sweeps
│   └── utils.py                 # I/O, logging, reproducibility helpers
│
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_projection.ipynb
│   ├── 03_quantile_alignment.ipynb
│   ├── 04_tda_analysis.ipynb
│   ├── 05_null_models.ipynb
│   ├── 06_statistics.ipynb
│   └── 07_robustness.ipynb
│
├── tests/
│   ├── test_projection.py
│   ├── test_quantile.py
│   ├── test_tda.py
│   └── test_statistics.py
│
├── Dockerfile
├── requirements.txt
├── LICENSE
└── README.md
```

---

## **3. Data Requirements**

### **Arithmetic Data**
- Source: Cremona/LMFDB or SageMath tables  
- Pre‑registered bound:  N ≤ N_max  
- Must include **full isogeny classes**  
- Required invariants:  
   Delta (Δ), N, r, R, Omega (𝛀), T

### **Cosmic Data**
- Source: SDSS or DESI  
- Must be **volume‑limited** and in **comoving coordinates**  
- Pre‑register survey, cuts, and volume

---

## **4. Projection Maps**

### **Primary Projection (𝛟_prime)**  
Implements the rank‑normalized spherical projection described in the manuscript, including:

- Radial coordinate  
  
  V_E = V_0 ⋅ T_E log(𝛀_E/2\π) R_E^(1/max(1,r_E)) exp(𝜳_r(E))
  
  
- Angular coordinates  
  
  \theta_E = \mathrm{mod}(\log_{10}|\Delta_E|, 2\pi), \quad
  
  \phi_E = \mathrm{mod}(\pi \log_{10} N_E, \pi)
  

### **Alternative Projections**
- **PTD**: \((\log|\Delta|, \log\Omega, \log(1+|E(\mathbb{Q})_{\mathrm{tors}}|))\)  
- **MCJ**: \((\log N, \log j(E), \log(1+R))\)

All constants (e.g., \(V_0\), \(N_{\max}\), scaling factors) must be pre‑registered.

---

## **5. Domain Alignment (Quantile Transform)**

Implements the coordinate‑wise non‑linear quantile alignment:

1. Fit empirical CDFs \(F_j^{\mathrm{cosmo}}\) on the cosmic cloud  
2. Fit empirical CDFs \(F_j^{\mathrm{arith}}\) on the arithmetic cloud  
3. Transform each coordinate via  
   \[
   p_j \mapsto (F_j^{\mathrm{cosmo}})^{-1}(F_j^{\mathrm{arith}}(p_j))
   \]

This step ensures marginal distributions match, isolating **structural** differences.

---

## **6. Topological Data Analysis**

- Vietoris–Rips complexes (GUDHI or Ripser)  
- Pre‑registered filtration range \([\varepsilon_{\min}, \varepsilon_{\max}]\)  
- Compute persistence diagrams \(D_k\) for \(k = 0,1,2\)  
- Primary metric: **2‑Wasserstein distance** \(W_2(D_k(P), D_k(M))\)

### **Topological Locked Scale**
Choose one (pre‑registered):

- Fixed: \(\varepsilon_* = 25.0\) Mpc  
- Adaptive: median k‑NN distance of cosmic data

---

## **7. Null Models**

Implemented nulls:

- **Null‑A**: Uniform random points  
- **Null‑B**: Permuted invariants (e.g., shuffle \(r_E\))  
- **Null‑C**: Alternative projections (PTD, MCJ)  
- **Null‑D**: Poisson process matched to cosmic density

Each null is run with \(m \ge 50\) repetitions.

---

## **8. Statistical Testing**

For each homological degree \(k\):

- Compute observed \(W_k^{\mathrm{obs}}\)  
- Compute empirical null distributions  
- One‑sided p‑value:  
  \[
  p_{k,j} = \frac{1 + \#\{i : W_{k,j}(i) \le W_k^{\mathrm{obs}}\}}{m+1}
  \]
- Multiple testing correction: **Benjamini–Hochberg (FDR 0.05)**

### **Decision Rule (Falsification)**

Support ACSC if:

- \(W_k^{\mathrm{obs}} < \varepsilon_k\) for all \(k\)  
- For at least one null model, \(p_{1,j} < 0.01\) after correction  

Otherwise: **fail to reject H₀** (ACSC falsified for this Φ and dataset).

---

## **9. Robustness & Ablation**

Includes:

- Subsample stability  
- Gaussian jitter tests  
- Parameter sweeps over \(N_{\max}, \Delta_{\max}, \alpha\)  
- Ablation of invariants (e.g., remove \(R_E\) or Ψ_r)  
- Cross‑survey validation (SDSS → DESI)

All robustness criteria are pre‑specified.

---

## **10. Reproducibility**

This repository includes:

- **Dockerfile** with pinned versions  
- `requirements.txt`  
- All scripts and notebooks needed to reproduce figures and tables  
- Random seeds and manifest of all inputs  
- Instructions for running the full pipeline end‑to‑end

---

## **11. Quick Start**

### **Build the environment**
```
docker build -t acsc .
docker run -it --rm -v $PWD:/workspace acsc
```

### **Run the full pipeline**
```
python -m acsc.run_all --config configs/default.yaml
```

### **Or explore interactively**
Open JupyterLab inside the container:
```
jupyter lab --ip=0.0.0.0 --allow-root
```

---

## **12. Citation**

If you use this code, please cite the ACSC manuscript:

> “The Arithmetic–Cosmic Structure Conjecture (ACSC).”  
> *Manuscript in preparation.*

---

## **13. License**

MIT License 

---

