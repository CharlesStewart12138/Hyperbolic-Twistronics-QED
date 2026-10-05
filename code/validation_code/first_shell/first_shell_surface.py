"""Exact centered surface-group first-shell positive control.

MANUSCRIPT SOURCE:
Equation: Eqs. (634)–(640).
Section: Direct answer to Question 7, centered surface-group control.
Model scope: validation first-shell scalar-commutant class only.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

REGISTERED_Q1 = 0.007124099762028338
REGISTERED_ADJACENCY_NORM = 8.0


def _validation(run_type: str) -> None:
    if run_type != "validation":
        raise ValueError("first-shell surface model is validation-only")


def _positive(value: float, name: str) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and strictly positive")
    return result


def _adjacency(matrix: ArrayLike) -> NDArray[np.complex128]:
    result = np.asarray(matrix, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError("A_S must be square")
    if not np.allclose(result, result.conj().T, rtol=0.0, atol=1e-13):
        raise ValueError("A_S must be Hermitian")
    return result


def q1_matrix(A_S: ArrayLike, q1: float, *, run_type: str) -> NDArray[np.complex128]:
    """Return Q1=I+q1*A_S in the declared first-shell control."""

    _validation(run_type)
    adjacency = _adjacency(A_S)
    coefficient = _positive(q1, "q1")
    return np.eye(adjacency.shape[0], dtype=np.complex128) + coefficient*adjacency


def parity_blocks(A_S: ArrayLike, t: float, w: float, q1: float, *, run_type: str) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    """Return H_±=±wI+(-t±wq1)A_S exactly."""

    _validation(run_type)
    adjacency = _adjacency(A_S)
    hopping = _positive(t, "t")
    coupling = _positive(w, "w")
    coefficient = _positive(q1, "q1")
    identity = np.eye(adjacency.shape[0], dtype=np.complex128)
    plus = coupling*identity + (-hopping+coupling*coefficient)*adjacency
    minus = -coupling*identity + (-hopping-coupling*coefficient)*adjacency
    return plus, minus


def root(t: float, q1: float, *, run_type: str) -> float:
    _validation(run_type)
    return _positive(t, "t") / _positive(q1, "q1")


def gap_lower_bound(t: float, q1: float, adjacency_norm: float, *, run_type: str) -> float:
    """Return g*=2t(q1^-1-||A_S||), requiring strict positivity."""

    _validation(run_type)
    hopping = _positive(t, "t")
    coefficient = _positive(q1, "q1")
    norm = float(adjacency_norm)
    if not isfinite(norm) or norm < 0.0:
        raise ValueError("adjacency_norm must be finite and nonnegative")
    gap = 2.0*hopping*(1.0/coefficient-norm)
    if gap <= 0.0:
        raise ValueError("first-shell root is not isolated")
    return gap


def registered_validation_certificate(*, run_type: str) -> dict[str, float]:
    """Return the manuscript's registered dimensionless validation numbers."""

    _validation(run_type)
    return {
        "q1": REGISTERED_Q1,
        "adjacency_norm": REGISTERED_ADJACENCY_NORM,
        "w_star_over_t": root(1.0, REGISTERED_Q1, run_type=run_type),
        "g_star_over_t": gap_lower_bound(1.0, REGISTERED_Q1, REGISTERED_ADJACENCY_NORM, run_type=run_type),
    }

