"""Immutable output checks for PF-GRP-001-PRODUCT-PRODUCTION-V2."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"


def certificate() -> dict:
    return json.loads((GROUP / "PF_GRP_001_PRODUCT_PRODUCTION_V2_CERTIFICATE.json").read_text(encoding="utf-8"))


def test_scientific_negative_closes_computational_task_without_promotion() -> None:
    record = certificate()
    assert record["task_status"] == "Done"
    assert record["promotion_to_production"] is False
    assert record["scientific_classification"] == "FULLY_ADMISSIBLE_NOT_NUMERICALLY_TRACTABLE_ON_CURRENT_HOST"


def test_all_mathematical_quotient_gates_pass() -> None:
    gates = certificate()["mathematical_gates"]
    assert gates["order_N"] == 11_943_936
    assert all(value == "PASS" for key, value in gates.items() if key != "order_N")


def test_only_injectivity_certified_cutoffs_are_called_quotient_degrees() -> None:
    support = certificate()["exact_zero_twist_support"]
    assert support["certified_quotient_row_degree"] == {"2.5": 473, "3.0": 2_185}
    assert support["universal_cover_cutoff_to_count"]["3.5"] == 9_977
    assert support["primary_minimum_abs_cosh_gap"] > 70


def test_resource_failure_is_complete_work_not_storage_only() -> None:
    record = certificate()
    bound = record["primary_resource_lower_bound"]
    assert record["host_resource_gate"]["compact_primary_block_fits_alone"] is True
    assert bound["primary_grid_stream_bytes"] > 5_000_000_000_000_000_000
    assert record["decisive_work_bounds"]["stream_years_at_hypothetical_10_GB_per_second"] > 17.7
    assert record["operator_implementation"]["first_shell_shortcut"] is False
    assert record["operator_implementation"]["same_label_shortcut"] is False
