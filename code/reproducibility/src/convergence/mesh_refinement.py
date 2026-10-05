"""Periodic representation-domain mesh-refinement diagnostics."""

from __future__ import annotations

import numpy as np
from scipy.special import iv


def periodic_observable(
    coordinate_x: np.ndarray,
    coordinate_y: np.ndarray,
    *,
    beta: float,
    gamma: float,
    coupling: float,
    phase_x: float,
    phase_y: float,
) -> np.ndarray:
    """Evaluate a smooth, non-band-limited observable on a two-torus."""
    reduced_x = coordinate_x - phase_x
    reduced_y = coordinate_y - phase_y
    envelope = np.exp(beta * np.cos(reduced_x) + gamma * np.cos(reduced_y))
    return envelope * (1.0 + coupling * np.cos(reduced_x + reduced_y))


def exact_periodic_average(*, beta: float, gamma: float, coupling: float) -> float:
    """Return the exact normalized two-torus average of ``periodic_observable``."""
    return float(iv(0, beta) * iv(0, gamma) + coupling * iv(1, beta) * iv(1, gamma))


def mesh_average(
    resolution: int,
    *,
    origin_fraction: float,
    beta: float,
    gamma: float,
    coupling: float,
    phase_x: float,
    phase_y: float,
) -> float:
    """Compute the normalized periodic trapezoidal rule on an N x N mesh."""
    if resolution < 2:
        raise ValueError("resolution must be at least two")
    if not 0.0 <= origin_fraction < 1.0:
        raise ValueError("origin_fraction must lie in [0, 1)")
    axis = 2.0 * np.pi * (np.arange(resolution, dtype=float) + origin_fraction) / resolution
    coordinate_x, coordinate_y = np.meshgrid(axis, axis, indexing="ij")
    values = periodic_observable(
        coordinate_x,
        coordinate_y,
        beta=beta,
        gamma=gamma,
        coupling=coupling,
        phase_x=phase_x,
        phase_y=phase_y,
    )
    return float(np.mean(values))


def audit_mesh_refinement(
    *,
    levels: list[int],
    origin_fractions: list[float],
    beta: float,
    gamma: float,
    coupling: float,
    phase_x: float,
    phase_y: float,
    final_relative_tolerance: float,
    final_origin_agreement_tolerance: float,
    minimum_contractions: int,
    required_reduction_factor: float,
) -> dict[str, object]:
    """Audit accuracy, contraction, and mesh-origin stability across refinements."""
    if sorted(set(levels)) != levels or len(levels) < 3:
        raise ValueError("levels must contain at least three unique increasing resolutions")
    if len(origin_fractions) < 2:
        raise ValueError("at least two mesh origins are required")
    exact = exact_periodic_average(beta=beta, gamma=gamma, coupling=coupling)
    records: list[dict[str, float | int]] = []
    errors_by_origin: dict[str, list[float]] = {}
    final_values: list[float] = []
    checks: dict[str, bool] = {}
    for origin_fraction in origin_fractions:
        label = f"origin_{origin_fraction:g}"
        errors: list[float] = []
        values: list[float] = []
        previous = None
        for resolution in levels:
            value = mesh_average(
                resolution,
                origin_fraction=origin_fraction,
                beta=beta,
                gamma=gamma,
                coupling=coupling,
                phase_x=phase_x,
                phase_y=phase_y,
            )
            absolute_error = abs(value - exact)
            relative_error = absolute_error / abs(exact)
            values.append(value)
            errors.append(relative_error)
            records.append({
                "origin_fraction": origin_fraction,
                "resolution": resolution,
                "point_count": resolution * resolution,
                "mesh_average": value,
                "exact_average": exact,
                "absolute_error": absolute_error,
                "relative_error": relative_error,
                "successive_absolute_difference": None if previous is None else abs(value - previous),
            })
            previous = value
        contractions = sum(current <= prior for prior, current in zip(errors, errors[1:]))
        checks[f"{label}_final_accuracy"] = bool(errors[-1] <= final_relative_tolerance)
        checks[f"{label}_contraction_count"] = bool(contractions >= minimum_contractions)
        checks[f"{label}_total_reduction"] = bool(errors[-1] <= errors[0] * required_reduction_factor)
        errors_by_origin[label] = errors
        final_values.append(values[-1])
    final_origin_spread = float((max(final_values) - min(final_values)) / abs(exact))
    checks["final_mesh_origin_agreement"] = bool(final_origin_spread <= final_origin_agreement_tolerance)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "exact_average": exact,
        "levels": levels,
        "origin_fractions": origin_fractions,
        "final_origin_relative_spread": final_origin_spread,
        "errors_by_origin": errors_by_origin,
        "records": records,
        "checks": checks,
        "failed_checks": failed,
    }

