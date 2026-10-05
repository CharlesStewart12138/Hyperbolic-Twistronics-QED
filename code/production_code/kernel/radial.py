"""Exact exponential full-distance interlayer kernel and derivatives.

MANUSCRIPT SOURCE:
Equation: Eq. (101), T(D)=w exp[-(D-h)/lambda_perp].
Section: synthetic hyperbolic twist and interlayer hopping.
Model scope: production all-pair radial hopping; no shell truncation here.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _parameters(w: float, h: float, lambda_perp: float) -> tuple[float, float, float]:
    values = (float(w), float(h), float(lambda_perp))
    if not all(isfinite(value) for value in values):
        raise ValueError("w, h and lambda_perp must be finite")
    if values[0] <= 0.0 or values[1] < 0.0 or values[2] <= 0.0:
        raise ValueError("require w>0, h>=0 and lambda_perp>0")
    return values


def _distance(D: ArrayLike, h: float) -> NDArray[np.float64]:
    result = np.asarray(D, dtype=float)
    if np.any(~np.isfinite(result)) or np.any(result < h):
        raise ValueError("every product-space distance must be finite and D>=h")
    return result


def _native(value: NDArray[np.float64]) -> float | NDArray[np.float64]:
    return float(value) if value.ndim == 0 else value


@dataclass(frozen=True)
class RadialEvaluation:
    value: Any
    first_distance_derivative: Any
    second_distance_derivative: Any


@dataclass(frozen=True)
class ChainEvaluation:
    value: Any
    first_derivative: Any
    second_derivative: Any


def evaluate(D: ArrayLike, w: float, h: float, lambda_perp: float) -> RadialEvaluation:
    """Return T, dT/dD and d2T/dD2 analytically."""

    amplitude, vertical, decay = _parameters(w, h, lambda_perp)
    distance = _distance(D, vertical)
    value = amplitude*np.exp(-(distance-vertical)/decay)
    return RadialEvaluation(_native(value), _native(-value/decay), _native(value/decay**2))


def chain_derivatives(D: ArrayLike, D_first: ArrayLike, D_second: ArrayLike, w: float, h: float, lambda_perp: float) -> ChainEvaluation:
    """Return T, dT/dx and d2T/dx2 for any geometry coordinate x.

    The exact chain rule is T_x=-(T/lambda)D_x and
    T_xx=T[(D_x/lambda)^2-D_xx/lambda].
    """

    radial = evaluate(D, w, h, lambda_perp)
    value = np.asarray(radial.value, dtype=float)
    first_distance = np.asarray(D_first, dtype=float)
    second_distance = np.asarray(D_second, dtype=float)
    try:
        value, first_distance, second_distance = np.broadcast_arrays(value, first_distance, second_distance)
    except ValueError as error:
        raise ValueError("D, D_first and D_second must be broadcast-compatible") from error
    if np.any(~np.isfinite(first_distance)) or np.any(~np.isfinite(second_distance)):
        raise ValueError("distance derivatives must be finite")
    decay = float(lambda_perp)
    first = -value*first_distance/decay
    second = value*((first_distance/decay)**2-second_distance/decay)
    return ChainEvaluation(_native(value), _native(first), _native(second))

