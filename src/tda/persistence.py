"""
TDA Persistence Computation Module
Provides compute_persistence function used by notebooks.
"""
from __future__ import annotations
import numpy as np
from typing import List, Tuple, Dict, Any

def compute_persistence(point_cloud: np.ndarray, max_dim: int = 2) -> Dict[str, Any]:
    """
    Compute persistence barcodes from a point cloud.
    This is a wrapper that can use different backends (ripser, gudhi, etc.).
    """
    try:
        # Try to use ripser 
        from ripser import ripser
        result = ripser(point_cloud, maxdim=max_dim)
        diagrams = result['dgms']
        print(f"Computed persistence using ripser (dim 0-{max_dim})")
    except ImportError:
        try:
            # Fallback to gudhi
            import gudhi
            rips = gudhi.RipsComplex(points=point_cloud, max_edge_length=2.0)
            simplex_tree = rips.create_simplex_tree(max_dimension=max_dim)
            persistence = simplex_tree.persistence()
            diagrams = [[] for _ in range(max_dim + 1)]
            for interval in persistence:
                dim = interval[0]
                if dim <= max_dim:
                    diagrams[dim].append(interval[1])
            print("Computed persistence using gudhi")
        except ImportError:
            # Ultimate fallback: dummy barcodes
            print(" No TDA library found. Using placeholder barcodes.")
            n = len(point_cloud) if hasattr(point_cloud, '__len__') else 100
            diagrams = [
                [(0, 1 + np.random.rand()) for _ in range(n//2)],   # H0
                [(0.2, 0.8) for _ in range(n//5)] if max_dim >= 1 else []   # H1
            ]
    
    return {
        "dgms": diagrams,
        "betti": [len(d) for d in diagrams],
        "persistence_intervals": diagrams
    }


# For backward compatibility with older notebooks
def compute_persistence_diagrams(point_cloud, **kwargs):
    return compute_persistence(point_cloud, **kwargs)
