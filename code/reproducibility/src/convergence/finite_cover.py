"""Finite-cycle cover convergence against infinite-line analytic limits."""

from __future__ import annotations

import math

import numpy as np
from scipy.special import iv


def cycle_eigenvalues(size: int, *, diagonal: float, hopping: float) -> np.ndarray:
    if size < 3:
        raise ValueError("cycle size must be at least three")
    modes = 2.0 * np.pi * np.arange(size, dtype=float) / size
    return diagonal + 2.0 * hopping * np.cos(modes)


def infinite_line_heat_trace(time: float, *, diagonal: float, hopping: float) -> float:
    if time <= 0.0:
        raise ValueError("time must be positive")
    return float(np.exp(-time * diagonal) * iv(0, 2.0 * time * abs(hopping)))


def infinite_line_centered_moment(order: int, *, hopping: float) -> float:
    if order < 0:
        raise ValueError("order must be nonnegative")
    if order % 2:
        return 0.0
    half = order // 2
    return float(math.comb(order, half) * hopping**order)


def audit_finite_cover(
    *,
    cover_sizes: list[int],
    heat_times: list[float],
    diagonal: float,
    hopping: float,
    max_centered_moment_order: int,
    exact_moment_tolerance: float,
    final_heat_relative_tolerance: float,
    monotonic_slack: float,
) -> dict[str, object]:
    if sorted(set(cover_sizes)) != cover_sizes or len(cover_sizes) < 3:
        raise ValueError("cover_sizes must contain at least three unique increasing sizes")
    if max_centered_moment_order >= min(cover_sizes):
        raise ValueError("moment order must stay below every cycle length to exclude wrapping walks")
    heat_records: list[dict[str, float | int]] = []
    moment_records: list[dict[str, float | int]] = []
    maximum_heat_errors: list[float] = []
    checks: dict[str, bool] = {}
    for size in cover_sizes:
        eigenvalues = cycle_eigenvalues(size, diagonal=diagonal, hopping=hopping)
        centered = eigenvalues - diagonal
        heat_errors = []
        for time in heat_times:
            finite_value = float(np.mean(np.exp(-time * eigenvalues)))
            exact_value = infinite_line_heat_trace(time, diagonal=diagonal, hopping=hopping)
            absolute_error = abs(finite_value - exact_value)
            relative_error = absolute_error / abs(exact_value)
            heat_errors.append(relative_error)
            heat_records.append({
                "cover_size": size,
                "injectivity_radius_edges": size // 2,
                "heat_time": time,
                "finite_heat_trace": finite_value,
                "infinite_heat_trace": exact_value,
                "absolute_error": absolute_error,
                "relative_error": relative_error,
            })
        maximum_heat_errors.append(max(heat_errors))
        for order in range(max_centered_moment_order + 1):
            finite_moment = float(np.mean(np.power(centered, order)))
            exact_moment = infinite_line_centered_moment(order, hopping=hopping)
            error = abs(finite_moment - exact_moment)
            passed = error <= exact_moment_tolerance
            checks[f"cover_{size}_moment_{order}"] = bool(passed)
            moment_records.append({
                "cover_size": size,
                "order": order,
                "finite_centered_moment": finite_moment,
                "infinite_centered_moment": exact_moment,
                "absolute_error": error,
                "pass": bool(passed),
            })
    checks["maximum_heat_error_monotone"] = bool(
        all(current <= previous + monotonic_slack for previous, current in zip(maximum_heat_errors, maximum_heat_errors[1:]))
    )
    checks["final_heat_accuracy"] = bool(maximum_heat_errors[-1] <= final_heat_relative_tolerance)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "cover_sizes": cover_sizes,
        "heat_times": heat_times,
        "maximum_heat_relative_errors": maximum_heat_errors,
        "heat_records": heat_records,
        "moment_records": moment_records,
        "checks": checks,
        "failed_checks": failed,
    }
