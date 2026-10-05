"""Exact finite-quotient identities that do not require a chosen quotient."""

from __future__ import annotations

import math


def quotient_identity(*, coincidence_index: int, cover_degree: int, orbitals_per_layer: int = 1, primitive_genus: int = 2) -> dict[str, int | float]:
    if coincidence_index < 1 or cover_degree < 1 or orbitals_per_layer < 1:
        raise ValueError("indices, cover degree, and orbital count must be positive")
    common_genus = 1 + coincidence_index * (primitive_genus - 1)
    exact_cell_orbitals = 2 * orbitals_per_layer * coincidence_index
    device_dimension = exact_cell_orbitals * cover_degree
    return {
        "coincidence_index": coincidence_index,
        "cover_degree": cover_degree,
        "primitive_genus": primitive_genus,
        "common_genus": common_genus,
        "exact_cell_area_over_r2": 4.0 * math.pi * coincidence_index,
        "exact_cell_orbitals": exact_cell_orbitals,
        "device_dimension": device_dimension,
    }


def embedded_disk_dimension_lower_bound(*, coincidence_index: int, injectivity_radius_over_r: float, orbitals_per_layer: int = 1) -> float:
    common_cell_area_over_r2 = 4.0 * math.pi * coincidence_index
    embedded_disk_area_over_r2 = 2.0 * math.pi * (math.cosh(injectivity_radius_over_r) - 1.0)
    return 2.0 * orbitals_per_layer * coincidence_index * embedded_disk_area_over_r2 / common_cell_area_over_r2
