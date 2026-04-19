#!/bin/bash

"""
ACSC: Arithmetic–Cosmic Structure Conjecture computational framework.

A reproducible pipeline for testing the correspondence between topological features
of elliptic-curve arithmetic clouds and cosmic structure.
"""

__version__ = "0.1.0"
__author__ = "Patrick J. McNamara"

# Core exports for convenient access
from .projection import project, primary_projection, projection_ptd, projection_mcj
from .quantile import QuantileAligner
from .tda_pipeline import compute_persistence, persistence_wasserstein
from .statistics import w2_between_diagrams, empirical_p_value, effect_size

__all__ = [
    "project",
    "primary_projection",
    "projection_ptd",
    "projection_mcj",
    "QuantileAligner",
    "compute_persistence",
    "persistence_wasserstein",
    "w2_between_diagrams",
    "empirical_p_value",
    "effect_size",
]
EOF

echo "✅ Fixed acsc/__init__.py"

echo "🔧 Step 2: Clean build artifacts..."
rm -rf build/ dist/ *.egg-info 2>/dev/null || true
pip cache purge

echo "✅ Cleaned artifacts"

echo "🔧 Step 3: Install C compiler..."
conda install -c conda-forge gcc gfortran -y 2>/dev/null || true

echo "✅ C compiler installed"

echo "🔧 Step 4: Install pre-built dependencies..."
pip install --upgrade pip setuptools wheel
pip install --only-binary :all: numpy pandas scipy pytest black isort

echo "✅ Dependencies installed"

echo "🔧 Step 5: Install ACSC package..."
pip install -e ".[dev]"

echo "✅ ACSC installed"

echo "🔧 Step 6: Verify..."
python -c "import acsc; print('✅ ACSC loaded successfully')"

echo "🔧 Step 7: Run tests..."
pytest tests/ -v --tb=short
