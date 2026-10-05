"""Real-space dense-matrix path for a flux-threaded cycle."""

from __future__ import annotations

import numpy as np


def dense_cycle_spectrum(
    size: int,
    *,
    diagonal: float,
    hopping: float,
    total_flux: float,
) -> np.ndarray:
    if size < 3:
        raise ValueError("size must be at least three")
    matrix = np.zeros((size, size), dtype=complex)
    np.fill_diagonal(matrix, diagonal)
    for site in range(size - 1):
        matrix[site, site + 1] = hopping
        matrix[site + 1, site] = hopping
    matrix[size - 1, 0] = hopping * np.exp(1j * total_flux)
    matrix[0, size - 1] = hopping * np.exp(-1j * total_flux)
    return np.linalg.eigvalsh(matrix)


def dense_spectral_observables(eigenvalues: np.ndarray, *, heat_time: float) -> dict[str, float]:
    values = np.asarray(eigenvalues, dtype=float)
    return {
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
        "bandwidth": float(np.max(values) - np.min(values)),
        "mean": float(np.mean(values)),
        "second_moment": float(np.mean(values * values)),
        "heat_trace": float(np.mean(np.exp(-heat_time * values))),
    }
