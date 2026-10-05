from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_forecast_precedes_and_withholds_large_run() -> None:
    record = json.loads((ROOT / "production_code/hodge/CM_047_NP_M7_STREAM_RESOURCE_FORECAST.json").read_text(encoding="utf-8"))
    assert record["forecast_precedes_large_calculation"] is True
    assert record["large_calculation_executed"] is False
    assert record["resource_targets"]["target_peak_rss_bytes"] == 16 * 1024**3
    assert record["resource_targets"]["hard_peak_rss_ceiling_bytes"] == 48 * 1024**3
    assert record["preflight_gate"]["authorized_to_launch"] is False


def test_blocker_is_exact_group_partition_not_ram() -> None:
    record = json.loads((ROOT / "production_code/hodge/CM_047_NP_M7_STREAM_PREFLIGHT.json").read_text(encoding="utf-8"))
    assert record["classification"] == "BLOCKED_MISSING_PROOF_COMPLETE_CANONICAL_GROUP_PARTITION"
    assert record["blocked_is_resource_failure"] is False
    assert record["exact_evidence"]["surface_relator_matrix_is_exact_identity"] is True
    assert record["exact_evidence"]["bounded_canonical_engine_maximum_certified_word_depth"] < record["exact_evidence"]["radius_6_exact_geometric_ball_largest_minimum_word_depth"]
    assert record["minimal_release_task"] == "CM-GRP-EXT-001"
    assert record["m8_released"] is False
