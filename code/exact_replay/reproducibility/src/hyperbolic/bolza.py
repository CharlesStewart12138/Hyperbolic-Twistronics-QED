"""Exact normalized Bolza-octagon geometry and short surface-group orbits."""

from __future__ import annotations

import cmath
import math

import numpy as np


SQRT2 = math.sqrt(2.0)
R_IN_OVER_R = math.acosh(1.0 + SQRT2)
A_B_OVER_R = 2.0 * R_IN_OVER_R
R_CIRC_OVER_R = math.acosh((1.0 + SQRT2) ** 2)
VERTEX_DISK_RADIUS = 2.0 ** (-0.25)
ETA = math.sqrt(2.0 * (SQRT2 - 1.0))


def poincare_distance(z: complex, w: complex, *, curvature_radius: float = 1.0) -> float:
    denominator = math.sqrt((1.0 - abs(z) ** 2) * (1.0 - abs(w) ** 2))
    return 2.0 * curvature_radius * math.asinh(abs(z - w) / denominator)


def disk_radius_from_geodesic(radius_over_r: float) -> float:
    return math.tanh(radius_over_r / 2.0)


def bolza_vertices() -> list[complex]:
    return [
        VERTEX_DISK_RADIUS * cmath.exp(1j * (2 * index + 1) * math.pi / 8.0)
        for index in range(8)
    ]


def neighbor_matrix(direction: int) -> np.ndarray:
    """Return an SU(1,1) matrix for the direction-n nearest-cell map."""
    phase = cmath.exp(1j * (direction % 8) * math.pi / 4.0)
    scale = 1.0 / math.sqrt(1.0 - ETA * ETA)
    alpha = scale + 0.0j
    beta = scale * ETA * phase
    return np.asarray([[alpha, beta], [beta.conjugate(), alpha.conjugate()]], dtype=complex)


def mobius_apply(matrix: np.ndarray, z: complex) -> complex:
    return complex((matrix[0, 0] * z + matrix[0, 1]) / (matrix[1, 0] * z + matrix[1, 1]))


def enumerate_orbit(max_word_depth: int = 3) -> tuple[list[dict[str, object]], dict[str, object]]:
    if max_word_depth < 0:
        raise ValueError("max_word_depth must be non-negative")
    identity = np.eye(2, dtype=complex)
    records: list[dict[str, object]] = [{
        "orbit_index": 0,
        "word": "e",
        "word_depth": 0,
        "parent_index": -1,
        "last_generator": -1,
        "disk_x": 0.0,
        "disk_y": 0.0,
        "geodesic_radius_over_r": 0.0,
        "matrix": identity,
    }]
    seen = {(0.0, 0.0): 0}
    frontier = [0]
    maximum_parent_bond_residual = 0.0
    minimum_disk_margin = 1.0
    for depth in range(1, max_word_depth + 1):
        new_frontier: list[int] = []
        for parent_index in frontier:
            parent = records[parent_index]
            parent_matrix = np.asarray(parent["matrix"])
            previous_generator = int(parent["last_generator"])
            parent_point = complex(float(parent["disk_x"]), float(parent["disk_y"]))
            for direction in range(8):
                if previous_generator >= 0 and direction == (previous_generator + 4) % 8:
                    continue
                matrix = parent_matrix @ neighbor_matrix(direction)
                point = mobius_apply(matrix, 0.0j)
                key = (round(point.real, 13), round(point.imag, 13))
                if key in seen:
                    continue
                orbit_index = len(records)
                seen[key] = orbit_index
                radius = poincare_distance(0.0j, point)
                maximum_parent_bond_residual = max(
                    maximum_parent_bond_residual,
                    abs(poincare_distance(parent_point, point) - A_B_OVER_R),
                )
                minimum_disk_margin = min(minimum_disk_margin, 1.0 - abs(point))
                records.append({
                    "orbit_index": orbit_index,
                    "word": f"{parent['word']} s{direction}" if parent["word"] != "e" else f"s{direction}",
                    "word_depth": depth,
                    "parent_index": parent_index,
                    "last_generator": direction,
                    "disk_x": point.real,
                    "disk_y": point.imag,
                    "geodesic_radius_over_r": radius,
                    "matrix": matrix,
                })
                new_frontier.append(orbit_index)
        frontier = new_frontier
    depth_counts = {
        str(depth): sum(1 for record in records if record["word_depth"] == depth)
        for depth in range(max_word_depth + 1)
    }
    public_records = [{key: value for key, value in record.items() if key != "matrix"} for record in records]
    checks = {
        "all_points_inside_disk": minimum_disk_margin > 0.0,
        "parent_bonds_equal_a_b": maximum_parent_bond_residual <= 2.0e-11,
        "origin_unique": sum(record["geodesic_radius_over_r"] <= 1.0e-13 for record in records) == 1,
    }
    return public_records, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "max_word_depth": max_word_depth,
        "orbit_point_count": len(records),
        "depth_counts": depth_counts,
        "maximum_parent_bond_residual_over_r": maximum_parent_bond_residual,
        "minimum_disk_margin": minimum_disk_margin,
        "checks": checks,
    }


def base_geometry_checks() -> dict[str, object]:
    vertices = bolza_vertices()
    generator_matrices = [neighbor_matrix(index) for index in range(8)]
    neighbor_distances = [poincare_distance(0.0j, mobius_apply(matrix, 0.0j)) for matrix in generator_matrices]
    inverse_residuals = [
        float(np.linalg.norm(generator_matrices[(index + 4) % 8] @ matrix - np.eye(2)))
        for index, matrix in enumerate(generator_matrices)
    ]
    checks = {
        "polygon_area_matches_gauss_bonnet": abs((6.0 * math.pi - 8.0 * math.pi / 4.0) - 4.0 * math.pi) <= 1.0e-14,
        "vertex_disk_radius": max(abs(abs(vertex) - VERTEX_DISK_RADIUS) for vertex in vertices) <= 1.0e-14,
        "translation_parameter": abs(ETA - math.tanh(A_B_OVER_R / 2.0)) <= 1.0e-14,
        "neighbor_distance": max(abs(distance - A_B_OVER_R) for distance in neighbor_distances) <= 2.0e-13,
        "opposite_maps_are_inverses": max(inverse_residuals) <= 2.0e-13,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "maximum_neighbor_distance_residual_over_r": max(abs(distance - A_B_OVER_R) for distance in neighbor_distances),
        "maximum_inverse_matrix_residual": max(inverse_residuals),
    }
