"""Unit tests for the 903-candidate geometric-shell re-audit."""

from pathlib import Path

from production_code.group.quotient_reaudit_geometric_shell import (
    GEOMETRIC_B3,
    STANDARD_B3,
    audit_candidate,
    load_candidate_specs,
)


INPUT = Path("data/production/quotient_search_v2")


def test_inventory_reconstructs_all_903_candidates() -> None:
    specs = load_candidate_specs(INPUT)
    assert len(specs) == 903
    assert len({row["candidate_id"] for row in specs}) == 903


def test_both_radius_three_balls_have_457_elements() -> None:
    assert len(STANDARD_B3) == 457
    assert len(GEOMETRIC_B3) == 457


def test_first_candidate_is_reaudited_on_physical_shell() -> None:
    record = audit_candidate(load_candidate_specs(INPUT)[0])
    assert record["physical_shell"] == "S8_GEOMETRIC"
    assert record["checks"]["RQA09"] is True
    assert record["checks"]["RQA11"] is True
    assert record["checks"]["RQA12"] is False
    assert record["accept_reject"] == "REJECT"
    assert record["hyperbolic_geometric"]["word_bound_promoted_to_geometric"] is False


def test_every_rqa_column_is_explicit() -> None:
    record = audit_candidate(load_candidate_specs(INPUT)[2])
    assert list(record["checks"]) == [f"RQA{i:02d}" for i in range(1, 21)]
    assert record["standard_presentation_B3"]["word_injectivity_radius"] in {"<=3", ">3"}
    assert record["physical_geometric_B3"]["word_injectivity_radius"] in {"<=3", ">3"}
