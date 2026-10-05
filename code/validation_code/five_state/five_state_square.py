"""Exact equal-amplitude square five-state theorem control.

MANUSCRIPT SOURCE:
Equation: Eqs. (605)–(633).
Section: Exact no-go theorem for the minimal first-star model.
Model scope: validation only; never a production Euclidean Hamiltonian.
"""

from __future__ import annotations

from math import isfinite, sqrt

import numpy as np
from numpy.typing import NDArray

LOWER_BOUND = 4.0 * sqrt(2.0) - 5.0
ALPHA_MIN_SQUARED = (1.0 + sqrt(2.0)) / 8.0


def _validation(run_type: str) -> None:
    if run_type != "validation":
        raise ValueError("square five-state model is validation-only")


def _alpha(alpha: float) -> float:
    value = float(alpha)
    if not isfinite(value) or value < 0.0:
        raise ValueError("alpha must be finite and nonnegative")
    return value


def hamiltonian(px: float, py: float, alpha: float, *, run_type: str) -> NDArray[np.float64]:
    """Return Eq. (609)'s exact 5x5 dimensionless Hamiltonian."""

    _validation(run_type)
    coupling = _alpha(alpha)
    x, y = float(px), float(py)
    if not all(isfinite(value) for value in (x, y)):
        raise ValueError("momentum components must be finite")
    d0 = x*x + y*y
    diagonal = [d0, d0+1+2*x, d0+1-2*x, d0+1+2*y, d0+1-2*y]
    matrix = np.diag(diagonal).astype(float)
    matrix[0, 1:] = coupling
    matrix[1:, 0] = coupling
    return matrix


def r_alpha(alpha: float, *, run_type: str) -> float:
    _validation(run_type)
    coupling = _alpha(alpha)
    return sqrt(1.0 + 16.0*coupling*coupling)


def point_spectrum(alpha: float, *, run_type: str) -> tuple[float, float, float, float, float]:
    """Return ((1-r)/2,1,1,1,(1+r)/2) at p=0."""

    r = r_alpha(alpha, run_type=run_type)
    return ((1.0-r)/2.0, 1.0, 1.0, 1.0, (1.0+r)/2.0)


def curvature_coefficient(alpha: float, *, run_type: str) -> float:
    """Return c_square=(r^2-r+2)/(r(r+1)), exact in alpha."""

    r = r_alpha(alpha, run_type=run_type)
    return (r*r-r+2.0)/(r*(r+1.0))


def no_root_certificate(alpha: float, *, run_type: str) -> dict[str, float | bool]:
    """Evaluate the exact positive lower-bound certificate."""

    coefficient = curvature_coefficient(alpha, run_type=run_type)
    return {"c_square": coefficient, "lower_bound": LOWER_BOUND, "root_exists": False, "bound_residual": coefficient-LOWER_BOUND}

