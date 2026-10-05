"""Momentum-quantization path for a flux-threaded cycle."""

from __future__ import annotations

import math


def analytic_cycle_spectrum(
    size: int,
    *,
    diagonal: float,
    hopping: float,
    total_flux: float,
) -> list[float]:
    if size < 3:
        raise ValueError("size must be at least three")
    values = []
    for mode in range(size):
        wave_number = (2.0 * math.pi * mode + total_flux) / size
        values.append(diagonal + 2.0 * hopping * math.cos(wave_number))
    return sorted(values)


def analytic_spectral_observables(eigenvalues: list[float], *, heat_time: float) -> dict[str, float]:
    size = len(eigenvalues)
    minimum = min(eigenvalues)
    maximum = max(eigenvalues)
    return {
        "minimum": minimum,
        "maximum": maximum,
        "bandwidth": maximum - minimum,
        "mean": math.fsum(eigenvalues) / size,
        "second_moment": math.fsum(value * value for value in eigenvalues) / size,
        "heat_trace": math.fsum(math.exp(-heat_time * value) for value in eigenvalues) / size,
    }
