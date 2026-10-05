from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_word_ball_cannot_cover_frozen_geometric_m6_ball() -> None:
    check = json.loads((ROOT / "production_code/hodge/CM_047_NP_M7_REGISTRY_SCOPE_CHECK.json").read_text(encoding="utf-8"))
    required = check["required_scientific_domain"]
    supplied = check["provided_CM_GRP_EXT_001_domain"]
    assert supplied["elements_including_identity"] < required["frozen_m6_elements_including_identity"]
    assert required["frozen_m6_largest_minimum_physical_word_length"] > 7
    assert check["mathematical_relation"]["provided_registry_can_contain_frozen_m6_domain"] is False


def test_scope_mismatch_hard_stops_m7_and_m8() -> None:
    check = json.loads((ROOT / "production_code/hodge/CM_047_NP_M7_REGISTRY_SCOPE_CHECK.json").read_text(encoding="utf-8"))
    assert check["classification"] == "BLOCKED_INPUT_SCOPE_MISMATCH"
    assert check["large_tensor_calculation_started"] is False
    assert check["minimum_new_dependency"] == "CM-GRP-GEO7-001"
    assert check["m8_released"] is False
