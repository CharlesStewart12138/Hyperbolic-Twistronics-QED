"""Ideal reciprocal support and explicit finite-window diffraction.

MANUSCRIPT SOURCE:
Equations: diffraction Eqs. (552)–(600) and release-Q6 window convolution.
Section: Fourier transform and diffraction.
Model scope: rigid square bilayer; calibrated form factors/windows stay external.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi, sin
from typing import Callable, Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


WindowTransform = Callable[[NDArray[np.float64]], ArrayLike]


@dataclass(frozen=True)
class ReciprocalPeak:
    layer: int
    indices: tuple[int, int]
    q: tuple[float, float]
    form_factor: complex = 1.0+0.0j


def _rotation(theta: float) -> NDArray[np.float64]:
    angle = float(theta)
    if not isfinite(angle):
        raise ValueError("theta must be finite")
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


def reciprocal_peaks(
    theta: float,
    *,
    maximum_index: int,
    a: float = 1.0,
    form_factors: tuple[complex, complex] = (1.0+0.0j, 1.0+0.0j),
) -> tuple[ReciprocalPeak, ...]:
    """Return layer-resolved peaks of Lambda* and R_theta Lambda* in a square index box."""

    if isinstance(maximum_index, bool) or not isinstance(maximum_index, int) or maximum_index < 0:
        raise ValueError("maximum_index must be a nonnegative integer")
    spacing = float(a)
    if not isfinite(spacing) or spacing <= 0.0:
        raise ValueError("a must be finite and positive")
    if len(form_factors) != 2 or not all(np.isfinite(value) for value in form_factors):
        raise ValueError("two finite layer form factors are required")
    rotate = _rotation(theta)
    scale = 2.0*pi/spacing
    result: list[ReciprocalPeak] = []
    for h in range(-maximum_index, maximum_index+1):
        for k in range(-maximum_index, maximum_index+1):
            base = scale*np.array([h, k], dtype=float)
            rotated = rotate@base
            result.append(ReciprocalPeak(1, (h, k), (float(base[0]), float(base[1])), complex(form_factors[0])))
            result.append(ReciprocalPeak(2, (h, k), (float(rotated[0]), float(rotated[1])), complex(form_factors[1])))
    return tuple(result)


def first_shell_splitting(theta: float, *, a: float = 1.0) -> float:
    """Return Delta q_1=(4*pi/a)|sin(theta/2)|."""

    spacing = float(a)
    angle = float(theta)
    if not isfinite(spacing) or spacing <= 0.0 or not isfinite(angle):
        raise ValueError("a must be positive and theta finite")
    return (4.0*pi/spacing)*abs(sin(angle/2.0))


def rectangular_window_transform(delta_q: NDArray[np.float64], *, lengths_over_a: tuple[float, float]) -> NDArray[np.float64]:
    """Fourier transform of a centered rectangular observation window."""

    values = np.asarray(delta_q, dtype=float)
    if values.shape[-1:] != (2,) or np.any(~np.isfinite(values)):
        raise ValueError("delta_q must have final dimension two and finite entries")
    lx, ly = (float(lengths_over_a[0]), float(lengths_over_a[1]))
    if not isfinite(lx) or not isfinite(ly) or lx <= 0.0 or ly <= 0.0:
        raise ValueError("window lengths must be finite and positive")
    return lx*ly*np.sinc(values[..., 0]*lx/(2.0*pi))*np.sinc(values[..., 1]*ly/(2.0*pi))


def gaussian_window_transform(delta_q: NDArray[np.float64], *, sigma_over_a: float) -> NDArray[np.float64]:
    """Fourier transform of exp(-r^2/(2 sigma^2)), including its area."""

    values = np.asarray(delta_q, dtype=float)
    sigma = float(sigma_over_a)
    if values.shape[-1:] != (2,) or np.any(~np.isfinite(values)) or not isfinite(sigma) or sigma <= 0.0:
        raise ValueError("require finite two-dimensional delta_q and positive sigma")
    return 2.0*pi*sigma*sigma*np.exp(-0.5*sigma*sigma*np.sum(values*values, axis=-1))


def windowed_amplitude(
    q_over_inverse_a: ArrayLike,
    peaks: Iterable[ReciprocalPeak],
    window_transform: WindowTransform,
    *,
    layer_2_displacement_over_a: tuple[float, float] = (0.0, 0.0),
    a: float = 1.0,
) -> NDArray[np.complex128] | complex:
    """Evaluate the finite-window comb convolution without inventing a window."""

    q = np.asarray(q_over_inverse_a, dtype=float)
    scalar = q.shape == (2,)
    if q.shape[-1:] != (2,) or np.any(~np.isfinite(q)):
        raise ValueError("q must have final dimension two and finite entries")
    spacing = float(a)
    displacement = np.asarray(layer_2_displacement_over_a, dtype=float)
    if not isfinite(spacing) or spacing <= 0.0 or displacement.shape != (2,) or np.any(~np.isfinite(displacement)):
        raise ValueError("a and layer-2 displacement must be finite, with a>0")
    amplitude = np.zeros(q.shape[:-1], dtype=complex)
    count = 0
    for peak in peaks:
        peak_q = np.asarray(peak.q, dtype=float)
        broadened = np.asarray(window_transform(q-peak_q), dtype=complex)
        if broadened.shape != amplitude.shape or np.any(~np.isfinite(broadened)):
            raise ValueError("window transform returned an invalid shape or nonfinite value")
        phase = np.exp(-1j*np.dot(peak_q, displacement)) if peak.layer == 2 else 1.0+0.0j
        amplitude += peak.form_factor*phase*broadened/(spacing*spacing)
        count += 1
    if count == 0:
        raise ValueError("at least one reciprocal peak is required")
    return complex(amplitude) if scalar else amplitude


def windowed_intensity(*args, **kwargs) -> NDArray[np.float64] | float:
    amplitude = windowed_amplitude(*args, **kwargs)
    intensity = np.abs(amplitude)**2
    return float(intensity) if np.ndim(intensity) == 0 else np.asarray(intensity, dtype=float)


def normalized_structure_factor(q_over_inverse_a: ArrayLike, positions_over_a: ArrayLike, weights: ArrayLike | None = None) -> NDArray[np.float64] | float:
    """Compute |sum_j f_j exp(-i q.r_j)|^2/sum_j |f_j|^2."""

    q = np.asarray(q_over_inverse_a, dtype=float)
    positions = np.asarray(positions_over_a, dtype=float)
    if q.shape[-1:] != (2,) or positions.ndim != 2 or positions.shape[1] != 2:
        raise ValueError("q and positions must be two-dimensional Cartesian arrays")
    if positions.shape[0] == 0 or np.any(~np.isfinite(q)) or np.any(~np.isfinite(positions)):
        raise ValueError("positions must be nonempty and all coordinates finite")
    factors = np.ones(positions.shape[0], dtype=complex) if weights is None else np.asarray(weights, dtype=complex)
    if factors.shape != (positions.shape[0],) or np.any(~np.isfinite(factors)):
        raise ValueError("weights must contain one finite value per position")
    phases = np.exp(-1j*np.einsum("...d,jd->...j", q, positions))
    amplitude = np.einsum("...j,j->...", phases, factors)
    normalization = float(np.sum(np.abs(factors)**2))
    if normalization == 0.0:
        raise ValueError("weights cannot all vanish")
    result = np.abs(amplitude)**2/normalization
    return float(result) if np.ndim(result) == 0 else np.asarray(result, dtype=float)
