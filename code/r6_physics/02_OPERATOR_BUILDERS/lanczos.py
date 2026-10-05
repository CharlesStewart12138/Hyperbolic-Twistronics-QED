"""Deterministic Lanczos tridiagonalization and Ritz diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.sparse.linalg import LinearOperator

from matvec import linear_operator


@dataclass(frozen=True)
class LanczosResult:
    alpha: np.ndarray
    beta: np.ndarray
    ritz_values: np.ndarray
    residual: float


def tridiagonalize(operator, start: np.ndarray, steps: int, reorthogonalize: bool = True) -> LanczosResult:
    op = linear_operator(operator)
    q = np.asarray(start, dtype=np.complex128).copy()
    q /= np.linalg.norm(q)
    previous = np.zeros_like(q)
    beta_previous = 0.0
    basis: list[np.ndarray] = []
    alpha: list[float] = []
    beta: list[float] = []
    residual = 0.0
    for index in range(min(int(steps), op.shape[0])):
        z = op @ q - beta_previous * previous
        a = float(np.vdot(q, z).real)
        z -= a * q
        if reorthogonalize:
            for old in basis:
                z -= np.vdot(old, z) * old
        b = float(np.linalg.norm(z))
        basis.append(q.copy())
        alpha.append(a)
        residual = b
        if b < 1e-13 or index + 1 == min(int(steps), op.shape[0]):
            break
        beta.append(b)
        previous, q = q, z / b
        beta_previous = b
    diag = np.asarray(alpha)
    off = np.asarray(beta[: max(0, len(alpha) - 1)])
    ritz = eigh_tridiagonal(diag, off, eigvals_only=True) if len(diag) else np.empty(0)
    return LanczosResult(diag, off, ritz, residual)


def edge_estimates(operator, steps: int = 64, seed: int = 20260903) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    start = rng.normal(size=operator.shape[0])
    result = tridiagonalize(operator, start, steps)
    return float(result.ritz_values[0]), float(result.ritz_values[-1])

