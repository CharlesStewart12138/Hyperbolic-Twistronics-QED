"""Cross-tower convergence comparisons for independently nested cycle covers."""

from __future__ import annotations

import numpy as np

from convergence.finite_cover import cycle_eigenvalues, infinite_line_heat_trace


def audit_cross_tower(
    *,
    tower_a_sizes: list[int],
    tower_b_sizes: list[int],
    heat_times: list[float],
    diagonal: float,
    hopping: float,
    final_relative_tolerance: float,
    monotonic_slack: float,
    triangle_slack: float,
) -> dict[str, object]:
    if len(tower_a_sizes) != len(tower_b_sizes) or len(tower_a_sizes) < 3:
        raise ValueError("tower size lists must have the same length of at least three")
    for label, sizes in (("tower_a", tower_a_sizes), ("tower_b", tower_b_sizes)):
        if sorted(set(sizes)) != sizes:
            raise ValueError(f"{label} sizes must be unique and increasing")
        if any(fine % coarse != 0 for coarse, fine in zip(sizes, sizes[1:])):
            raise ValueError(f"{label} must be a nested divisibility tower")
    records: list[dict[str, float | int]] = []
    maximum_a_errors: list[float] = []
    maximum_b_errors: list[float] = []
    maximum_cross_differences: list[float] = []
    checks: dict[str, bool] = {}
    for level, (size_a, size_b) in enumerate(zip(tower_a_sizes, tower_b_sizes)):
        values_a = cycle_eigenvalues(size_a, diagonal=diagonal, hopping=hopping)
        values_b = cycle_eigenvalues(size_b, diagonal=diagonal, hopping=hopping)
        level_a_errors = []
        level_b_errors = []
        level_cross = []
        for time in heat_times:
            exact = infinite_line_heat_trace(time, diagonal=diagonal, hopping=hopping)
            trace_a = float(np.mean(np.exp(-time * values_a)))
            trace_b = float(np.mean(np.exp(-time * values_b)))
            error_a = abs(trace_a - exact) / abs(exact)
            error_b = abs(trace_b - exact) / abs(exact)
            cross_difference = abs(trace_a - trace_b) / abs(exact)
            triangle_bound = error_a + error_b
            triangle_pass = cross_difference <= triangle_bound + triangle_slack
            checks[f"level_{level}_time_{time:g}_triangle_bound"] = bool(triangle_pass)
            level_a_errors.append(error_a)
            level_b_errors.append(error_b)
            level_cross.append(cross_difference)
            records.append({
                "level": level,
                "tower_a_size": size_a,
                "tower_b_size": size_b,
                "heat_time": time,
                "infinite_heat_trace": exact,
                "tower_a_heat_trace": trace_a,
                "tower_b_heat_trace": trace_b,
                "tower_a_relative_error": error_a,
                "tower_b_relative_error": error_b,
                "cross_tower_relative_difference": cross_difference,
                "triangle_relative_bound": triangle_bound,
                "triangle_bound_pass": bool(triangle_pass),
            })
        maximum_a_errors.append(max(level_a_errors))
        maximum_b_errors.append(max(level_b_errors))
        maximum_cross_differences.append(max(level_cross))
    checks["tower_a_error_monotone"] = bool(
        all(current <= previous + monotonic_slack for previous, current in zip(maximum_a_errors, maximum_a_errors[1:]))
    )
    checks["tower_b_error_monotone"] = bool(
        all(current <= previous + monotonic_slack for previous, current in zip(maximum_b_errors, maximum_b_errors[1:]))
    )
    checks["cross_tower_difference_monotone"] = bool(
        all(current <= previous + monotonic_slack for previous, current in zip(maximum_cross_differences, maximum_cross_differences[1:]))
    )
    checks["tower_a_final_accuracy"] = bool(maximum_a_errors[-1] <= final_relative_tolerance)
    checks["tower_b_final_accuracy"] = bool(maximum_b_errors[-1] <= final_relative_tolerance)
    checks["cross_tower_final_agreement"] = bool(maximum_cross_differences[-1] <= final_relative_tolerance)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "tower_a_sizes": tower_a_sizes,
        "tower_b_sizes": tower_b_sizes,
        "heat_times": heat_times,
        "maximum_tower_a_relative_errors": maximum_a_errors,
        "maximum_tower_b_relative_errors": maximum_b_errors,
        "maximum_cross_tower_relative_differences": maximum_cross_differences,
        "records": records,
        "checks": checks,
        "failed_checks": failed,
    }
