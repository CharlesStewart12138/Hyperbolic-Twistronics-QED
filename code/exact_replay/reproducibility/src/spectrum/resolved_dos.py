"""Deterministic Lorentzian and resolved-DOS helpers."""

from __future__ import annotations

import numpy as np


def lorentzian_density(
    grid: np.ndarray,
    atoms: np.ndarray,
    weights: np.ndarray,
    eta: float,
    *,
    chunk_size: int = 128,
) -> np.ndarray:
    if eta <= 0.0:
        raise ValueError("eta must be positive")
    if atoms.ndim != 1 or weights.ndim != 1 or atoms.size != weights.size:
        raise ValueError("atoms and weights must be equal-length vectors")
    result = np.empty_like(grid, dtype=float)
    for start in range(0, grid.size, chunk_size):
        stop = min(start + chunk_size, grid.size)
        differences = grid[start:stop, None] - atoms[None, :]
        kernels = eta / (np.pi * (differences * differences + eta * eta))
        result[start:stop] = kernels @ weights
    return result


def convolve_grid_density(
    output_grid: np.ndarray,
    input_grid: np.ndarray,
    density: np.ndarray,
    eta: float,
    *,
    chunk_size: int = 128,
) -> np.ndarray:
    if input_grid.ndim != 1 or density.ndim != 1 or input_grid.size != density.size:
        raise ValueError("input grid and density must be equal-length vectors")
    quadrature = np.empty_like(input_grid)
    quadrature[1:-1] = 0.5 * (input_grid[2:] - input_grid[:-2])
    quadrature[0] = 0.5 * (input_grid[1] - input_grid[0])
    quadrature[-1] = 0.5 * (input_grid[-1] - input_grid[-2])
    return lorentzian_density(output_grid, input_grid, quadrature * density, eta, chunk_size=chunk_size)


def normalize_on_grid(grid: np.ndarray, density: np.ndarray) -> tuple[np.ndarray, float]:
    mass = float(np.trapz(density, grid))
    if not np.isfinite(mass) or mass <= 0.0:
        raise ValueError("density has non-positive grid mass")
    return density / mass, mass


def exact_resolved_weights(vectors: np.ndarray, *, target_mask: np.ndarray) -> dict[str, np.ndarray]:
    dimension = vectors.shape[0]
    if dimension % 2:
        raise ValueError("bilayer dimension must be even")
    single = dimension // 2
    layer_1 = np.sum(np.abs(vectors[:single, :]) ** 2, axis=0) / dimension
    layer_2 = np.sum(np.abs(vectors[single:, :]) ** 2, axis=0) / dimension
    even_amplitudes = (vectors[:single, :] + vectors[single:, :]) / np.sqrt(2.0)
    odd_amplitudes = (vectors[:single, :] - vectors[single:, :]) / np.sqrt(2.0)
    even_weight = np.sum(np.abs(even_amplitudes) ** 2, axis=0) / single
    odd_weight = np.sum(np.abs(odd_amplitudes) ** 2, axis=0) / single
    target_weight = target_mask.astype(float) / float(np.count_nonzero(target_mask))
    return {
        "global": np.full(dimension, 1.0 / dimension),
        "layer_1": layer_1,
        "layer_2": layer_2,
        "local_layer_1_origin": np.abs(vectors[0, :]) ** 2,
        "local_layer_2_origin": np.abs(vectors[single, :]) ** 2,
        "layer_even_projector": even_weight,
        "layer_odd_projector": odd_weight,
        "target_root_projector": target_weight,
    }
