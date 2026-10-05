"""Shared sparse and matrix-free linear-algebra helpers."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, aslinearoperator


def linear_operator(value: sp.spmatrix | LinearOperator) -> LinearOperator:
    return value if isinstance(value, LinearOperator) else aslinearoperator(value)


def explicit_action_residual(matrix: sp.spmatrix, operator: LinearOperator, seed: int = 20260901) -> float:
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=matrix.shape[1]) + 1j * rng.normal(size=matrix.shape[1])
    reference = matrix @ vector
    trial = operator @ vector
    return float(np.linalg.norm(reference - trial) / max(np.linalg.norm(reference), 1e-300))


def hermiticity_probe(operator: LinearOperator, probes: int = 4, seed: int = 20260902) -> float:
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(probes):
        x = rng.normal(size=operator.shape[0]) + 1j * rng.normal(size=operator.shape[0])
        y = rng.normal(size=operator.shape[0]) + 1j * rng.normal(size=operator.shape[0])
        lhs = np.vdot(x, operator @ y)
        rhs = np.vdot(operator @ x, y)
        worst = max(worst, abs(lhs - rhs) / max(abs(lhs), abs(rhs), 1.0))
    return float(worst)

