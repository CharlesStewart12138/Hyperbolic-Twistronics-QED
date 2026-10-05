"""Krylov time evolution and probability diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse.linalg import expm_multiply


@dataclass(frozen=True)
class TimeTrace:
    times: np.ndarray
    states: np.ndarray
    norm_residual: float


def evolve(hamiltonian, initial: np.ndarray, times: np.ndarray) -> TimeTrace:
    grid = np.asarray(times, dtype=float)
    if grid.ndim != 1 or grid.size < 2 or not np.allclose(np.diff(grid), np.diff(grid)[0]):
        raise ValueError("expm_multiply path requires an equally spaced 1D time grid")
    psi = np.asarray(initial, dtype=complex)
    psi /= np.linalg.norm(psi)
    states = expm_multiply(-1j * hamiltonian, psi, start=float(grid[0]), stop=float(grid[-1]), num=grid.size, endpoint=True)
    norms = np.sum(np.abs(states) ** 2, axis=1)
    return TimeTrace(grid, states, float(np.max(np.abs(norms - 1.0))))

