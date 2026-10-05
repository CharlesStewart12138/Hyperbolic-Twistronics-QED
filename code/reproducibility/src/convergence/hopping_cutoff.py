"""Long-range hopping-cutoff convergence with analytic tail bounds."""

from __future__ import annotations

import numpy as np


def exact_dispersion(
    wave_number: np.ndarray,
    *,
    diagonal: float,
    hopping_scale: float,
    decay_ratio: float,
) -> np.ndarray:
    """Evaluate the infinite-range geometric-hopping dispersion."""
    if not 0.0 < decay_ratio < 1.0:
        raise ValueError("decay_ratio must lie in (0, 1)")
    phase = np.exp(1j * np.asarray(wave_number))
    series = phase / (1.0 - decay_ratio * phase)
    return diagonal + 2.0 * hopping_scale * np.real(series)


def truncated_dispersion(
    wave_number: np.ndarray,
    *,
    cutoff: int,
    diagonal: float,
    hopping_scale: float,
    decay_ratio: float,
) -> np.ndarray:
    if cutoff < 1:
        raise ValueError("cutoff must be positive")
    distances = np.arange(1, cutoff + 1, dtype=float)
    amplitudes = hopping_scale * np.power(decay_ratio, distances - 1.0)
    return diagonal + 2.0 * np.cos(np.outer(np.asarray(wave_number), distances)) @ amplitudes


def uniform_tail_bound(*, cutoff: int, hopping_scale: float, decay_ratio: float) -> float:
    return float(2.0 * abs(hopping_scale) * decay_ratio**cutoff / (1.0 - decay_ratio))


def audit_hopping_cutoff(
    *,
    cutoffs: list[int],
    wave_number_count: int,
    diagonal: float,
    hopping_scale: float,
    decay_ratio: float,
    final_max_tolerance: float,
    bound_slack: float,
) -> dict[str, object]:
    if sorted(set(cutoffs)) != cutoffs or len(cutoffs) < 3:
        raise ValueError("cutoffs must contain at least three unique increasing values")
    if wave_number_count < 32:
        raise ValueError("wave_number_count must be at least 32")
    wave_numbers = 2.0 * np.pi * np.arange(wave_number_count, dtype=float) / wave_number_count
    exact = exact_dispersion(
        wave_numbers,
        diagonal=diagonal,
        hopping_scale=hopping_scale,
        decay_ratio=decay_ratio,
    )
    exact_bandwidth = float(np.max(exact) - np.min(exact))
    records: list[dict[str, float | int]] = []
    checks: dict[str, bool] = {}
    maximum_errors: list[float] = []
    for cutoff in cutoffs:
        approximation = truncated_dispersion(
            wave_numbers,
            cutoff=cutoff,
            diagonal=diagonal,
            hopping_scale=hopping_scale,
            decay_ratio=decay_ratio,
        )
        difference = approximation - exact
        maximum_error = float(np.max(np.abs(difference)))
        rms_error = float(np.sqrt(np.mean(difference * difference)))
        tail_bound = uniform_tail_bound(
            cutoff=cutoff,
            hopping_scale=hopping_scale,
            decay_ratio=decay_ratio,
        )
        bandwidth = float(np.max(approximation) - np.min(approximation))
        checks[f"cutoff_{cutoff}_respects_tail_bound"] = bool(maximum_error <= tail_bound + bound_slack)
        maximum_errors.append(maximum_error)
        records.append({
            "cutoff": cutoff,
            "maximum_dispersion_error": maximum_error,
            "rms_dispersion_error": rms_error,
            "uniform_tail_bound": tail_bound,
            "tail_bound_margin": tail_bound - maximum_error,
            "truncated_bandwidth": bandwidth,
            "exact_bandwidth": exact_bandwidth,
            "bandwidth_absolute_error": abs(bandwidth - exact_bandwidth),
        })
    checks["maximum_error_monotone"] = bool(
        all(current <= previous + bound_slack for previous, current in zip(maximum_errors, maximum_errors[1:]))
    )
    checks["final_maximum_accuracy"] = bool(maximum_errors[-1] <= final_max_tolerance)
    checks["final_certified_tail"] = bool(records[-1]["uniform_tail_bound"] <= final_max_tolerance)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "records": records,
        "checks": checks,
        "failed_checks": failed,
        "exact_bandwidth": exact_bandwidth,
    }
