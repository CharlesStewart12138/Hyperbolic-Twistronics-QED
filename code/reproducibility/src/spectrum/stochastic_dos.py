"""KPM and SLQ estimators with explicit random generators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.linalg
import scipy.sparse


@dataclass(frozen=True)
class SpectralScaling:
    lower: float
    upper: float
    center: float
    radius: float


def scale_hermitian(
    matrix: np.ndarray | scipy.sparse.spmatrix,
    *,
    lower: float,
    upper: float,
) -> tuple[scipy.sparse.csr_matrix, SpectralScaling]:
    """Affinely scale a Hermitian matrix into the interval [-1, 1]."""

    if not np.isfinite(lower) or not np.isfinite(upper) or not lower < upper:
        raise ValueError("finite spectral bounds must satisfy lower < upper")
    sparse_matrix = scipy.sparse.csr_matrix(matrix)
    if sparse_matrix.shape[0] != sparse_matrix.shape[1]:
        raise ValueError("matrix must be square")
    center = 0.5 * (lower + upper)
    radius = 0.5 * (upper - lower)
    identity = scipy.sparse.identity(sparse_matrix.shape[0], dtype=sparse_matrix.dtype, format="csr")
    scaled = (sparse_matrix - center * identity) * (1.0 / radius)
    return scaled.tocsr(), SpectralScaling(lower, upper, center, radius)


def _random_probe(rng: np.random.Generator, size: int, complex_probe: bool) -> np.ndarray:
    if complex_probe:
        phases = rng.integers(0, 4, size=size)
        vector = np.choose(phases, [1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j, 0.0 - 1.0j])
    else:
        vector = 2.0 * rng.integers(0, 2, size=size).astype(float) - 1.0
    return vector / np.sqrt(size)


def _jackson_coefficients(moment_count: int) -> np.ndarray:
    if moment_count < 2:
        raise ValueError("moment_count must be at least 2")
    indices = np.arange(moment_count, dtype=float)
    denominator = moment_count + 1.0
    angles = np.pi * indices / denominator
    return (
        (moment_count - indices + 1.0) * np.cos(angles)
        + np.sin(angles) / np.tan(np.pi / denominator)
    ) / denominator


def kpm_density(
    scaled_matrix: scipy.sparse.spmatrix,
    scaling: SpectralScaling,
    *,
    moment_count: int,
    probe_count: int,
    rng: np.random.Generator,
    grid_size: int = 1001,
) -> dict[str, np.ndarray | float | int]:
    """Estimate normalized DOS with stochastic Chebyshev moments and Jackson damping."""

    matrix = scipy.sparse.csr_matrix(scaled_matrix)
    size = matrix.shape[0]
    if matrix.shape[1] != size:
        raise ValueError("scaled_matrix must be square")
    if moment_count < 4 or probe_count < 1 or grid_size < 101:
        raise ValueError("insufficient KPM moment, probe, or grid count")
    moments = np.zeros(moment_count, dtype=float)
    complex_probe = np.iscomplexobj(matrix.data)
    for _ in range(probe_count):
        probe = _random_probe(rng, size, complex_probe)
        t_previous = probe
        moments[0] += float(np.vdot(probe, t_previous).real)
        t_current = matrix @ probe
        moments[1] += float(np.vdot(probe, t_current).real)
        for order in range(2, moment_count):
            t_next = 2.0 * (matrix @ t_current) - t_previous
            moments[order] += float(np.vdot(probe, t_next).real)
            t_previous, t_current = t_current, t_next
    moments /= probe_count

    x_grid = np.linspace(-0.9995, 0.9995, grid_size)
    jackson = _jackson_coefficients(moment_count)
    series = np.full_like(x_grid, jackson[0] * moments[0])
    t_previous_grid = np.ones_like(x_grid)
    t_current_grid = x_grid.copy()
    series += 2.0 * jackson[1] * moments[1] * t_current_grid
    for order in range(2, moment_count):
        t_next_grid = 2.0 * x_grid * t_current_grid - t_previous_grid
        series += 2.0 * jackson[order] * moments[order] * t_next_grid
        t_previous_grid, t_current_grid = t_current_grid, t_next_grid
    density_x = series / (np.pi * np.sqrt(1.0 - x_grid * x_grid))
    energy_grid = scaling.center + scaling.radius * x_grid
    density_energy = np.maximum(density_x / scaling.radius, 0.0)
    mass_before_normalization = float(np.trapz(density_energy, energy_grid))
    if not np.isfinite(mass_before_normalization) or mass_before_normalization <= 0.0:
        raise RuntimeError("KPM density has non-positive or non-finite mass")
    density_energy /= mass_before_normalization
    return {
        "energy": energy_grid,
        "density": density_energy,
        "moments": moments,
        "jackson_coefficients": jackson,
        "mass_before_normalization": mass_before_normalization,
        "moment_count": moment_count,
        "probe_count": probe_count,
    }


def _lanczos_tridiagonal(
    matrix: scipy.sparse.csr_matrix,
    initial: np.ndarray,
    depth: int,
    breakdown_tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    size = matrix.shape[0]
    depth = min(depth, size)
    basis: list[np.ndarray] = []
    diagonal: list[float] = []
    off_diagonal: list[float] = []
    previous = np.zeros(size, dtype=initial.dtype)
    current = initial / np.linalg.norm(initial)
    previous_beta = 0.0
    for step in range(depth):
        basis.append(current.copy())
        candidate = matrix @ current - previous_beta * previous
        alpha = float(np.vdot(current, candidate).real)
        candidate = candidate - alpha * current
        for vector in basis:
            candidate = candidate - np.vdot(vector, candidate) * vector
        diagonal.append(alpha)
        beta = float(np.linalg.norm(candidate))
        if step == depth - 1 or beta <= breakdown_tolerance:
            break
        off_diagonal.append(beta)
        previous, current = current, candidate / beta
        previous_beta = beta
    return np.asarray(diagonal), np.asarray(off_diagonal)


def slq_quadrature(
    scaled_matrix: scipy.sparse.spmatrix,
    scaling: SpectralScaling,
    *,
    depth: int,
    probe_count: int,
    rng: np.random.Generator,
    breakdown_tolerance: float = 1.0e-14,
) -> dict[str, np.ndarray | float | int]:
    """Return normalized SLQ atoms and weights using full reorthogonalization."""

    matrix = scipy.sparse.csr_matrix(scaled_matrix)
    size = matrix.shape[0]
    if matrix.shape[1] != size:
        raise ValueError("scaled_matrix must be square")
    if depth < 2 or probe_count < 1:
        raise ValueError("SLQ depth must be at least 2 and probe_count positive")
    complex_probe = np.iscomplexobj(matrix.data)
    all_atoms: list[np.ndarray] = []
    all_weights: list[np.ndarray] = []
    realized_depths: list[int] = []
    for _ in range(probe_count):
        probe = _random_probe(rng, size, complex_probe)
        diagonal, off_diagonal = _lanczos_tridiagonal(matrix, probe, depth, breakdown_tolerance)
        values, vectors = scipy.linalg.eigh_tridiagonal(diagonal, off_diagonal, check_finite=True)
        weights = np.square(np.abs(vectors[0, :])) / probe_count
        all_atoms.append(scaling.center + scaling.radius * values)
        all_weights.append(weights)
        realized_depths.append(len(diagonal))
    atoms = np.concatenate(all_atoms)
    weights = np.concatenate(all_weights)
    mass_before_normalization = float(np.sum(weights))
    weights /= mass_before_normalization
    return {
        "atoms": atoms,
        "weights": weights,
        "mass_before_normalization": mass_before_normalization,
        "probe_count": probe_count,
        "requested_depth": depth,
        "minimum_realized_depth": min(realized_depths),
        "maximum_realized_depth": max(realized_depths),
    }


def cdf_from_density(energy: np.ndarray, density: np.ndarray) -> np.ndarray:
    if energy.ndim != 1 or density.ndim != 1 or energy.size != density.size:
        raise ValueError("energy and density must be one-dimensional arrays of equal length")
    increments = 0.5 * (density[1:] + density[:-1]) * np.diff(energy)
    cdf = np.concatenate(([0.0], np.cumsum(increments)))
    if cdf[-1] <= 0.0:
        raise ValueError("density integral is not positive")
    return np.clip(cdf / cdf[-1], 0.0, 1.0)


def cdf_from_atoms(grid: np.ndarray, atoms: np.ndarray, weights: np.ndarray) -> np.ndarray:
    order = np.argsort(atoms)
    sorted_atoms = atoms[order]
    cumulative = np.cumsum(weights[order])
    indices = np.searchsorted(sorted_atoms, grid, side="right")
    result = np.zeros_like(grid, dtype=float)
    positive = indices > 0
    result[positive] = cumulative[indices[positive] - 1]
    return np.clip(result, 0.0, 1.0)
