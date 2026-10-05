from __future__ import annotations

import json
from pathlib import Path

from production_code.group.global_systole_direct_pilot import (
    IDENTITY_STATE,
    canonical_phi8_dihedral,
    finite_images,
    finite_order,
    multiply_state,
)


ROOT = Path(__file__).resolve().parents[2]


def test_physical_generator_images_have_exact_registered_inverses() -> None:
    images = finite_images()
    for index in range(4):
        assert multiply_state(images[index], images[index + 4]) == IDENTITY_STATE
        assert multiply_state(images[index + 4], images[index]) == IDENTITY_STATE


def test_finite_image_orders_divide_s4_product_exponent() -> None:
    assert all(12 % finite_order(image) == 0 for image in finite_images())


def test_c8_dihedral_canonicalization_is_unique_for_sample_orbit() -> None:
    word = (0, 1, 3, 2)
    orbit = []
    inverse = tuple((value + 4) % 8 for value in reversed(word))
    for source in (word, inverse):
        for rotation in range(len(source)):
            rotated = source[rotation:] + source[:rotation]
            for shift in range(8):
                orbit.append(tuple((value + shift) % 8 for value in rotated))
    normalized = []
    for candidate in orbit:
        offset = candidate[0]
        shifted = tuple((value - offset) % 8 for value in candidate)
        if canonical_phi8_dihedral(shifted):
            normalized.append(shifted)
    assert len(set(normalized)) == 1


def test_resource_forecast_blocks_both_infeasible_complete_routes() -> None:
    forecast = json.loads((ROOT / "production_code/group/GLOBAL_DIRECT_RESOURCE_FORECAST.json").read_text(encoding="utf-8"))
    assert forecast["forecast_precedes_any_large_new_enumeration"] is True
    assert forecast["decision"]["large_axis_to_base_cell_flood_authorized"] is False
    assert forecast["decision"]["raw_length_110_enumeration_authorized"] is False
    assert forecast["large_search_estimates"]["axis_to_base_cell_flood"]["memory_fit_against_total_physical"] is False


def test_terminal_certificate_does_not_promote_unexhausted_search() -> None:
    certificate = json.loads((ROOT / "production_code/group/GLOBAL_SYSTOLE_DIRECT_CERTIFICATE.json").read_text(encoding="utf-8"))
    assert certificate["global_direct_search_attempted"] is True
    assert certificate["proof_exhaustion"] is False
    assert certificate["classification"] == "GLOBAL-UNRESOLVED"
    assert certificate["existing_quotient_promotion"].startswith("DENIED")
    assert certificate["main_tex_modified"] is False
