"""Chebyshev kernel-polynomial estimators with Jackson damping."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse.linalg import LinearOperator

from matvec import linear_operator


@dataclass(frozen=True)
class KPMResult:
    energy: np.ndarray
    density: np.ndarray
    moments: np.ndarray
    order: int
    probes: int
    bounds: tuple[float, float]


def jackson_kernel(order: int) -> np.ndarray:
    n = np.arange(order, dtype=float)
    denominator = order + 1.0
    return ((order - n + 1.0) * np.cos(np.pi * n / denominator) + np.sin(np.pi * n / denominator) / np.tan(np.pi / denominator)) / denominator


def chebyshev_moments(operator, vectors: np.ndarray, order: int, bounds: tuple[float, float]) -> np.ndarray:
    op = linear_operator(operator)
    lo, hi = map(float, bounds)
    center, radius = 0.5 * (hi + lo), 0.5 * (hi - lo) * 1.001
    if radius <= 0:
        raise ValueError("invalid spectral bounds")

    def scaled(v):
        return (op @ v - center * v) / radius

    states = np.atleast_2d(np.asarray(vectors, dtype=np.complex128))
    moments = np.empty((states.shape[0], int(order)), dtype=float)
    for row, vector in enumerate(states):
        vector = vector / np.linalg.norm(vector)
        t0 = vector.copy()
        moments[row, 0] = float(np.vdot(vector, t0).real)
        if order == 1:
            continue
        t1 = scaled(t0)
        moments[row, 1] = float(np.vdot(vector, t1).real)
        for n in range(2, int(order)):
            t2 = 2.0 * scaled(t1) - t0
            moments[row, n] = float(np.vdot(vector, t2).real)
            t0, t1 = t1, t2
    return moments


def reconstruct_density(moments: np.ndarray, bounds: tuple[float, float], points: int = 1000) -> tuple[np.ndarray, np.ndarray]:
    mu = np.mean(np.atleast_2d(moments), axis=0)
    order = len(mu)
    lo, hi = map(float, bounds)
    center, radius = 0.5 * (hi + lo), 0.5 * (hi - lo) * 1.001
    x = np.linspace(-0.999999, 0.999999, int(points))
    theta = np.arccos(x)
    kernel = jackson_kernel(order)
    series = kernel[0] * mu[0] + 2.0 * np.sum((kernel[1:] * mu[1:])[:, None] * np.cos(np.arange(1, order)[:, None] * theta[None, :]), axis=0)
    density = np.maximum(series / (np.pi * np.sqrt(1.0 - x*x) * radius), 0.0)
    energy = center + radius * x
    return energy, density


def local_kpm(operator, indices: list[int], order: int, bounds: tuple[float, float], points: int = 1000) -> KPMResult:
    vectors = np.zeros((len(indices), operator.shape[0]), dtype=float)
    vectors[np.arange(len(indices)), np.asarray(indices, dtype=int)] = 1.0
    moments = chebyshev_moments(operator, vectors, order, bounds)
    energy, density = reconstruct_density(moments, bounds, points)
    return KPMResult(energy, density, moments, int(order), len(indices), tuple(map(float, bounds)))

