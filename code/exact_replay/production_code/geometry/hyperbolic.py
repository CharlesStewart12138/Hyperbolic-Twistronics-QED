"""Exact Poincare-disk metric and geodesic distance.

MANUSCRIPT SOURCE:
Equation: Eqs. (44)–(45), with the distance identities used in Eqs. (46)–(56).
Section: Genus-two regular-octagon/Bolza-surface lattice.
Model scope: curvature K=-1/R^2 on the open unit disk.
"""

from __future__ import annotations

from math import asinh, atanh, isfinite


def _radius(R: float) -> float:
    value = float(R)
    if not isfinite(value) or value <= 0.0:
        raise ValueError("R must be finite and strictly positive")
    return value


def _disk_point(z: complex, name: str) -> complex:
    value = complex(z)
    if not isfinite(value.real) or not isfinite(value.imag) or abs(value) >= 1.0:
        raise ValueError(f"{name} must lie in the open Poincare disk")
    return value


def gaussian_curvature(R: float) -> float:
    """Return K=-R^-2.

    MANUSCRIPT SOURCE:
    Equation: Eq. (44).
    Section: Bolza-surface lattice.
    Model scope: constant negative curvature.
    """

    radius = _radius(R)
    return -1.0 / radius**2


def metric_conformal_factor(z: complex, R: float) -> float:
    """Return 2R/(1-|z|^2), whose square multiplies dx^2+dy^2.

    MANUSCRIPT SOURCE:
    Equation: Eq. (45).
    Section: Poincare-disk metric.
    Model scope: local tangent norm at z.
    """

    point = _disk_point(z, "z")
    return 2.0 * _radius(R) / (1.0 - abs(point) ** 2)


def metric_tensor(z: complex, R: float) -> tuple[tuple[float, float], tuple[float, float]]:
    factor2 = metric_conformal_factor(z, R) ** 2
    return ((factor2, 0.0), (0.0, factor2))


def distance(z: complex, w: complex, R: float) -> float:
    """Return the exact Poincare geodesic distance.

    Uses the stable identity
    d(z,w)=2R asinh(|z-w|/sqrt((1-|z|^2)(1-|w|^2))).

    MANUSCRIPT SOURCE:
    Equation: metric Eq. (45) and distance identities supporting Eqs. (46)–(56).
    Section: Poincare-disk geometry.
    Model scope: exact hyperbolic separation, not graph distance.
    """

    left = _disk_point(z, "z")
    right = _disk_point(w, "w")
    radius = _radius(R)
    denominator = ((1.0 - abs(left) ** 2) * (1.0 - abs(right) ** 2)) ** 0.5
    return 2.0 * radius * asinh(abs(left - right) / denominator)


def radial_distance(z: complex, R: float) -> float:
    """Return d(0,z)=2R atanh(|z|)."""

    point = _disk_point(z, "z")
    return 2.0 * _radius(R) * atanh(abs(point))

