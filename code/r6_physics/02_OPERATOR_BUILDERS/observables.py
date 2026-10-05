"""Spectral and dynamical observables used by all four R6 programs."""

from __future__ import annotations

import numpy as np


def gaussian_ldos(eigenvalues: np.ndarray, eigenvectors: np.ndarray, index: int, energy: np.ndarray, eta: float) -> np.ndarray:
    weights = np.abs(eigenvectors[index, :]) ** 2
    delta = np.asarray(energy)[:, None] - np.asarray(eigenvalues)[None, :]
    kernel = np.exp(-0.5 * (delta / eta) ** 2) / (np.sqrt(2.0 * np.pi) * eta)
    return kernel @ weights


def spectral_moments(hamiltonian, index: int, orders: int = 8) -> np.ndarray:
    vector = np.zeros(hamiltonian.shape[0], dtype=complex)
    vector[index] = 1.0
    state = vector.copy()
    result = [1.0]
    for _ in range(1, int(orders) + 1):
        state = hamiltonian @ state
        result.append(float(np.vdot(vector, state).real))
    return np.asarray(result)


def eigensystem_summary(eigenvalues: np.ndarray, eigenvectors: np.ndarray, sites_per_layer: int) -> dict[str, float]:
    vals = np.asarray(eigenvalues)
    vecs = np.asarray(eigenvectors)
    probabilities = np.abs(vecs) ** 2
    ipr = np.sum(probabilities**2, axis=0)
    lower, upper = vecs[:sites_per_layer], vecs[sites_per_layer:]
    coherence = 2.0 * np.abs(np.sum(np.conjugate(lower) * upper, axis=0))
    center = int(np.argmin(np.abs(vals)))
    return {
        "edge_min": float(vals[0]),
        "edge_max": float(vals[-1]),
        "gap_zero": float(2.0 * np.min(np.abs(vals))),
        "bandwidth": float(vals[-1] - vals[0]),
        "ipr_zero": float(ipr[center]),
        "coherence_zero": float(coherence[center]),
        "second_moment_global": float(np.mean(vals**2)),
    }


def dynamical_observables(states: np.ndarray, initial: np.ndarray, radii: np.ndarray, sites_per_layer: int) -> dict[str, np.ndarray]:
    probability = np.abs(states) ** 2
    initial_normalized = np.asarray(initial, dtype=complex) / np.linalg.norm(initial)
    survival = np.abs(states @ np.conjugate(initial_normalized)) ** 2
    lower = probability[:, :sites_per_layer]
    upper = probability[:, sites_per_layer:]
    radial = np.concatenate([radii, radii])
    mean_radius = probability @ radial
    second = probability @ (radial**2)
    participation = 1.0 / np.maximum(np.sum(probability**2, axis=1), 1e-300)
    imbalance = np.sum(lower, axis=1) - np.sum(upper, axis=1)
    entropy = -np.sum(np.where(probability > 0, probability * np.log(np.maximum(probability, 1e-300)), 0.0), axis=1)
    return {
        "survival": survival,
        "return_probability": probability[:, int(np.argmax(np.abs(initial_normalized)))],
        "mean_radius": mean_radius,
        "mean_square_radius": second,
        "participation": participation,
        "layer_imbalance": imbalance,
        "entropy": entropy,
    }


def smoothness_residual(theta: np.ndarray, values: np.ndarray) -> np.ndarray:
    return np.abs(np.gradient(values, theta))

