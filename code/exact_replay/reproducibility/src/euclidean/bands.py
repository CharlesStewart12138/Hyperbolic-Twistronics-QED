"""Parameter-free normalized folded bands for exact square CSL cells."""

from __future__ import annotations

import math

import numpy as np


def standard_mbz_path(p: int, q: int, sigma: int, *, points_per_segment: int) -> list[dict[str, float | int | str]]:
    if points_per_segment < 2:
        raise ValueError("points_per_segment must be at least two")
    g1 = 2.0 * np.pi * np.asarray([p, q], dtype=float) / sigma
    g2 = 2.0 * np.pi * np.asarray([-q, p], dtype=float) / sigma
    special = [
        ("Gamma", np.zeros(2)),
        ("X", 0.5 * g1),
        ("M", 0.5 * (g1 + g2)),
        ("Gamma", np.zeros(2)),
    ]
    records = []
    path_distance = 0.0
    point_index = 0
    for segment_index, ((start_label, start), (end_label, end)) in enumerate(zip(special, special[1:])):
        fractions = np.linspace(0.0, 1.0, points_per_segment, endpoint=True)
        if segment_index:
            fractions = fractions[1:]
        prior = None
        for fraction in fractions:
            coordinate = (1.0 - fraction) * start + fraction * end
            if prior is not None:
                path_distance += float(np.linalg.norm(coordinate - prior))
            elif records:
                previous_coordinate = np.asarray([records[-1]["kx_a"], records[-1]["ky_a"]])
                path_distance += float(np.linalg.norm(coordinate - previous_coordinate))
            records.append({
                "point_index": point_index,
                "segment_index": segment_index,
                "segment": f"{start_label}-{end_label}",
                "segment_fraction": float(fraction),
                "kx_a": float(coordinate[0]),
                "ky_a": float(coordinate[1]),
                "path_distance_ka": path_distance,
            })
            prior = coordinate
            point_index += 1
    return records


def monolayer_energy_over_t(momentum: np.ndarray) -> float:
    return float(-2.0 * (np.cos(momentum[0]) + np.cos(momentum[1])))


def folded_w0_bands(
    *,
    p: int,
    q: int,
    sigma: int,
    angle_radians: float,
    points_per_segment: int,
) -> tuple[list[dict[str, float | int | str]], dict[str, object]]:
    path = standard_mbz_path(p, q, sigma, points_per_segment=points_per_segment)
    g1 = 2.0 * np.pi * np.asarray([p, q], dtype=float) / sigma
    rotation_inverse = np.asarray([
        [math.cos(angle_radians), math.sin(angle_radians)],
        [-math.sin(angle_radians), math.cos(angle_radians)],
    ])
    rows = []
    maximum_trace_residual = 0.0
    for point in path:
        momentum = np.asarray([point["kx_a"], point["ky_a"]], dtype=float)
        layer_values: dict[int, list[float]] = {1: [], 2: []}
        for branch in range(sigma):
            layer_one_value = monolayer_energy_over_t(momentum + branch * g1)
            layer_two_value = monolayer_energy_over_t(rotation_inverse @ (momentum + branch * g1))
            layer_values[1].append(layer_one_value)
            layer_values[2].append(layer_two_value)
            for layer, value in ((1, layer_one_value), (2, layer_two_value)):
                rows.append({
                    **point,
                    "layer": layer,
                    "folded_branch": branch,
                    "energy_over_t": value,
                    "interlayer_coupling_over_t": 0.0,
                    "scope": "EXACT_W0_FOLDING_CONTROL",
                })
        maximum_trace_residual = max(
            maximum_trace_residual,
            abs(sum(layer_values[1])),
            abs(sum(layer_values[2])),
        )
    energy_values = [float(row["energy_over_t"]) for row in rows]
    expected_rows = len(path) * 2 * sigma
    checks = {
        "row_count": len(rows) == expected_rows,
        "energy_bounds": min(energy_values) >= -4.0 - 1.0e-12 and max(energy_values) <= 4.0 + 1.0e-12,
        "folded_trace_zero": maximum_trace_residual <= 1.0e-10,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    return rows, {
        "status": "PASS" if not failed else "FAIL",
        "path_point_count": len(path),
        "band_count_per_point": 2 * sigma,
        "row_count": len(rows),
        "maximum_folded_trace_residual": maximum_trace_residual,
        "checks": checks,
        "failed_checks": failed,
    }
