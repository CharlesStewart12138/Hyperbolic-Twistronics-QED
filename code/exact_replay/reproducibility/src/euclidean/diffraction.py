"""Rigid square-bilayer reciprocal peaks and exact splitting diagnostics."""

from __future__ import annotations

import math

import numpy as np


FIRST_SHELL = np.asarray(((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)))


def rigid_first_shell_peaks(angle_radians: float) -> list[dict[str, float | int | str]]:
    rotation = np.asarray([
        [math.cos(angle_radians), -math.sin(angle_radians)],
        [math.sin(angle_radians), math.cos(angle_radians)],
    ])
    rows = []
    for layer, vectors in ((1, FIRST_SHELL), (2, (rotation @ FIRST_SHELL.T).T)):
        for peak_index, vector in enumerate(vectors):
            rows.append({
                "layer": layer,
                "peak_index": peak_index,
                "qx_a_over_2pi": float(vector[0]),
                "qy_a_over_2pi": float(vector[1]),
                "ideal_relative_intensity": 1.0,
                "scope": "RIGID_UNIT_FORM_FACTOR_IDEAL_PEAK",
            })
    return rows


def diffraction_metrics(
    *,
    angle_radians: float,
    sigma: int | None,
    n: int | None,
    divisor: int | None,
) -> dict[str, float | int | str | None]:
    split_normalized = 2.0 * abs(math.sin(angle_radians / 2.0))
    record: dict[str, float | int | str | None] = {
        "angle_radians": angle_radians,
        "angle_degrees": math.degrees(angle_radians),
        "first_shell_split_a_over_2pi": split_normalized,
        "beat_length_over_a": 1.0 / split_normalized,
        "sigma": sigma,
        "mbz_reciprocal_magnitude_a_over_2pi": None if sigma is None else 1.0 / math.sqrt(sigma),
        "split_to_mbz_ratio": None,
        "supercell_to_beat_length_ratio": None,
        "scope": "EXACT_RIGID_DIFFRACTION_GEOMETRY",
    }
    if sigma is not None and n is not None and divisor is not None:
        exact_ratio = 2.0 * n / math.sqrt(divisor)
        record["split_to_mbz_ratio"] = exact_ratio
        record["supercell_to_beat_length_ratio"] = exact_ratio
    return record


def c8_union_residual() -> float:
    peaks = rigid_first_shell_peaks(math.pi / 4.0)
    points = np.asarray([[row["qx_a_over_2pi"], row["qy_a_over_2pi"]] for row in peaks])
    rotation = np.asarray([
        [math.cos(math.pi / 4.0), -math.sin(math.pi / 4.0)],
        [math.sin(math.pi / 4.0), math.cos(math.pi / 4.0)],
    ])
    rotated = (rotation @ points.T).T
    return float(max(np.min(np.linalg.norm(points - point, axis=1)) for point in rotated))
