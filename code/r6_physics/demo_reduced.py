"""Reduced, data-free R6 demonstration of the non-Bloch bilayer operator."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parent
BUILDERS = ROOT / "02_OPERATOR_BUILDERS"
if str(BUILDERS) not in sys.path:
    sys.path.insert(0, str(BUILDERS))

from geometry import OrbitPatch
from local_operator import ScalarBilayerParameters, build_local_bilayer, schur_row_sum_bound
from observables import spectral_moments
from qa import sparse_hermiticity_defect
from time_evolution import evolve


def reduced_patch() -> OrbitPatch:
    """Return a deterministic nine-site disk patch for source-only checks.

    This fixture exercises the R6 operator construction without pretending to
    replace the exact Bolza universal-cover registry used in production runs.
    """
    count = 8
    radius = 0.32
    ring = radius * np.exp(2j * np.pi * np.arange(count) / count)
    coordinates = np.concatenate((np.asarray([0.0 + 0.0j]), ring))
    rows: list[int] = []
    cols: list[int] = []
    for index in range(1, count + 1):
        nxt = 1 + (index % count)
        for left, right in ((0, index), (index, 0), (index, nxt), (nxt, index)):
            rows.append(left)
            cols.append(right)
    adjacency = sp.coo_matrix(
        (np.ones(len(rows)), (rows, cols)), shape=(count + 1, count + 1)
    ).tocsr()
    adjacency.data[:] = 1.0
    return OrbitPatch(
        depth=1,
        coordinates=coordinates,
        radii_over_a=np.concatenate((np.asarray([0.0]), np.ones(count))),
        word_depths=np.concatenate((np.asarray([0], dtype=np.int16), np.ones(count, dtype=np.int16))),
        words=((),) + tuple((f"g{index}",) for index in range(count)),
        adjacency=adjacency,
        center=0,
    )


def main() -> int:
    patch = reduced_patch()
    parameters = ScalarBilayerParameters(
        theta=0.137,
        omega_over_omega_ref=0.01,
        lambda_perp_over_a=0.20,
    )
    model = build_local_bilayer(patch, parameters)
    eigenvalues = np.linalg.eigvalsh(model.hamiltonian.toarray())
    initial = np.zeros(model.dimension)
    initial[0] = 1.0
    trace = evolve(model.hamiltonian, initial, np.linspace(0.0, 1.0, 5))
    payload = {
        "mode": "reduced-source-only",
        "sites_per_layer": model.sites_per_layer,
        "hilbert_dimension": model.dimension,
        "hermiticity_defect": sparse_hermiticity_defect(model.hamiltonian),
        "schur_row_sum_bound": schur_row_sum_bound(patch, parameters),
        "spectral_min": float(eigenvalues[0]),
        "spectral_max": float(eigenvalues[-1]),
        "second_local_moment": float(spectral_moments(model.hamiltonian, 0, orders=2)[2]),
        "time_norm_residual": trace.norm_residual,
        "production_claim": False,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
