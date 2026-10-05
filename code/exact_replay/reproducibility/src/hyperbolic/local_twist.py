"""Exact local hyperbolic twist displacement and effective moire geometry."""

from __future__ import annotations

import math

from reproducibility.src.hyperbolic.bolza import disk_radius_from_geodesic, poincare_distance


def twist_displacement_over_r(radius_over_r: float, theta: float) -> float:
    return 2.0 * math.asinh(abs(math.sin(theta / 2.0)) * math.sinh(radius_over_r))


def moire_geometry(*, a_over_r: float, theta: float, orbitals_per_layer: int = 1) -> dict[str, float | int | str]:
    sine = abs(math.sin(theta / 2.0))
    if sine == 0.0:
        return {
            "theta_radians": theta,
            "half_angle_sine": sine,
            "chi": math.inf,
            "moire_radius_over_r": math.inf,
            "effective_area_over_r2": math.inf,
            "effective_bilayer_count": math.inf,
            "registry_threshold_residual_over_r": 0.0,
            "status": "ALIGNED_LIMIT",
        }
    chi = math.sinh(a_over_r / 2.0) / sine
    radius = math.asinh(chi)
    area = 2.0 * math.pi * (math.sqrt(1.0 + chi * chi) - 1.0)
    primitive_area = 4.0 * math.pi
    count = 2.0 * orbitals_per_layer * area / primitive_area
    residual = abs(twist_displacement_over_r(radius, theta) - a_over_r)
    return {
        "theta_radians": theta,
        "half_angle_sine": sine,
        "chi": chi,
        "moire_radius_over_r": radius,
        "effective_area_over_r2": area,
        "effective_bilayer_count": count,
        "registry_threshold_residual_over_r": residual,
        "status": "PASS" if residual <= 2.0e-12 else "FAIL",
    }


def displacement_disk_crosscheck(radius_over_r: float, theta: float) -> float:
    disk_radius = disk_radius_from_geodesic(radius_over_r)
    z = complex(disk_radius, 0.0)
    rotated = z * complex(math.cos(theta), math.sin(theta))
    direct = poincare_distance(z, rotated)
    return abs(direct - twist_displacement_over_r(radius_over_r, theta))
