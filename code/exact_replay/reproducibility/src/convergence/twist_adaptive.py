"""Adaptive periodic twist-grid refinement for avoided-crossing minima."""

from __future__ import annotations

import math

import numpy as np


TWO_PI = 2.0 * np.pi


def avoided_crossing_gap(
    theta: np.ndarray | float,
    *,
    center: float,
    coupling: float,
    twist_offset: float,
) -> np.ndarray:
    """Return the gap of a two-level periodic avoided-crossing fixture."""
    mass = np.cos(np.asarray(theta) - twist_offset) - center
    return 2.0 * np.sqrt(mass * mass + coupling * coupling)


def exact_gap_minima(*, center: float, twist_offset: float) -> np.ndarray:
    if not -1.0 < center < 1.0:
        raise ValueError("center must lie strictly between -1 and 1")
    root = math.acos(center)
    return np.mod(np.asarray([twist_offset + root, twist_offset - root]), TWO_PI)


def periodic_distance_to_set(angle: float, references: np.ndarray) -> float:
    delta = np.abs(np.asarray(references) - angle)
    return float(np.min(np.minimum(delta, TWO_PI - delta)))


def uniform_minimum(
    point_count: int,
    *,
    center: float,
    coupling: float,
    twist_offset: float,
) -> tuple[float, float]:
    points = TWO_PI * np.arange(point_count, dtype=float) / point_count
    values = avoided_crossing_gap(
        points, center=center, coupling=coupling, twist_offset=twist_offset
    )
    index = int(np.argmin(values))
    return float(points[index]), float(values[index])


def adaptive_twist_refinement(
    *,
    initial_resolution: int,
    refinement_rounds: int,
    refine_fraction: float,
    center: float,
    coupling: float,
    twist_offset: float,
) -> dict[str, object]:
    """Refine lowest-energy periodic intervals while preserving every prior point."""
    if initial_resolution < 4 or refinement_rounds < 1:
        raise ValueError("initial_resolution must be >=4 and refinement_rounds positive")
    if not 0.0 < refine_fraction <= 0.5:
        raise ValueError("refine_fraction must lie in (0, 0.5]")
    if coupling <= 0.0:
        raise ValueError("coupling must be positive")
    points = TWO_PI * np.arange(initial_resolution, dtype=float) / initial_resolution
    references = exact_gap_minima(center=center, twist_offset=twist_offset)
    exact_value = 2.0 * coupling
    records: list[dict[str, float | int]] = []
    for round_index in range(refinement_rounds + 1):
        points = np.sort(np.unique(np.mod(points, TWO_PI)))
        values = avoided_crossing_gap(
            points, center=center, coupling=coupling, twist_offset=twist_offset
        )
        best_index = int(np.argmin(values))
        best_angle = float(points[best_index])
        best_value = float(values[best_index])
        uniform_angle, uniform_value = uniform_minimum(
            len(points), center=center, coupling=coupling, twist_offset=twist_offset
        )
        records.append({
            "round": round_index,
            "adaptive_point_count": len(points),
            "adaptive_min_angle": best_angle,
            "adaptive_min_gap": best_value,
            "adaptive_value_error": best_value - exact_value,
            "adaptive_angle_error": periodic_distance_to_set(best_angle, references),
            "uniform_min_angle_same_count": uniform_angle,
            "uniform_min_gap_same_count": uniform_value,
            "uniform_value_error_same_count": uniform_value - exact_value,
            "uniform_angle_error_same_count": periodic_distance_to_set(uniform_angle, references),
        })
        if round_index == refinement_rounds:
            break
        next_points = np.roll(points, -1)
        widths = np.mod(next_points - points, TWO_PI)
        next_values = np.roll(values, -1)
        interval_priority = 0.5 * (values + next_values)
        refine_count = max(2, int(math.ceil(refine_fraction * len(points))))
        chosen = np.argsort(interval_priority, kind="stable")[:refine_count]
        midpoints = np.mod(points[chosen] + 0.5 * widths[chosen], TWO_PI)
        points = np.concatenate([points, midpoints])
    return {
        "records": records,
        "final_points": [float(value) for value in points],
        "exact_minimum_gap": exact_value,
        "exact_minimum_angles": [float(value) for value in references],
    }


def audit_twist_refinement(
    *,
    initial_resolution: int,
    refinement_rounds: int,
    refine_fraction: float,
    center: float,
    coupling: float,
    twist_offset: float,
    final_value_tolerance: float,
    final_angle_tolerance: float,
    uniform_improvement_factor: float,
) -> dict[str, object]:
    result = adaptive_twist_refinement(
        initial_resolution=initial_resolution,
        refinement_rounds=refinement_rounds,
        refine_fraction=refine_fraction,
        center=center,
        coupling=coupling,
        twist_offset=twist_offset,
    )
    records = result["records"]
    final = records[-1]
    value_errors = [float(record["adaptive_value_error"]) for record in records]
    checks = {
        "nested_value_monotonicity": bool(all(current <= previous + 1e-15 for previous, current in zip(value_errors, value_errors[1:]))),
        "final_value_accuracy": bool(float(final["adaptive_value_error"]) <= final_value_tolerance),
        "final_angle_accuracy": bool(float(final["adaptive_angle_error"]) <= final_angle_tolerance),
        "adaptive_beats_equal_count_uniform_value": bool(
            float(final["adaptive_value_error"])
            <= uniform_improvement_factor * float(final["uniform_value_error_same_count"])
        ),
        "adaptive_beats_equal_count_uniform_angle": bool(
            float(final["adaptive_angle_error"])
            <= uniform_improvement_factor * float(final["uniform_angle_error_same_count"])
        ),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    result.update({
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed_checks": failed,
    })
    return result
