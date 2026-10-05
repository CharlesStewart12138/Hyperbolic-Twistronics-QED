from pathlib import Path

from production_code.group.quotient_search_v2 import (
    V2_SEEDS,
    audit_seed,
    base_s4_candidate,
    core_generators,
    exact_core_order,
    rotate_signature,
)


ARCHIVE = Path("data/production/universal_cover/ball_radius_6_exact.jsonl.gz")


def test_exact_core_orders_are_reproducible() -> None:
    assert [exact_core_order(base_s4_candidate(seed)) for seed in V2_SEEDS] == [4608, 331776, 165888]


def test_core_has_well_defined_order_eight_rotation() -> None:
    base = base_s4_candidate(V2_SEEDS[1])
    images = core_generators(base)
    assert any(rotate_signature(images[token]) != images[token] for token in images)
    for image in images.values():
        rotated = image
        for _ in range(8):
            rotated = rotate_signature(rotated)
        assert rotated == image


def test_v2_audits_keep_failed_candidates() -> None:
    records = [audit_seed(seed, ARCHIVE) for seed in V2_SEEDS]
    assert all(record["checks"]["Q-01_surface_relation_exact"] for record in records)
    assert all(record["checks"]["Q-09_phi8_descends"] for record in records)
    assert all(record["accept_reject"] == "REJECT" for record in records)
    assert all(record["first_failed_gate"] is not None for record in records)

