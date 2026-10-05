from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "local_full_kernel"


def test_m7_resource_gate_precedes_and_blocks_exact_ball() -> None:
    forecast = json.loads((DATA / "EXACT_BALL7_TENSOR_RESOURCE_FORECAST.json").read_text(encoding="utf-8"))
    assert forecast["forecast_precedes_exact_radius_7_enumeration"] is True
    assert forecast["decision"]["exact_complete_ball_m7_authorized"] is False
    assert forecast["m7_forecast"]["estimated_peak_working_set_bytes"] > forecast["host"]["total_physical_memory_bytes"]


def test_historical_m7_absence_is_preserved_and_current_stream_is_complete() -> None:
    historical = json.loads((DATA / "EXACT_BALL7_TENSOR_PARTIAL.pre_stream.status.json").read_text(encoding="utf-8"))
    current = json.loads((DATA / "EXACT_BALL7_TENSOR_PARTIAL.status.json").read_text(encoding="utf-8"))
    assert historical["created"] is False
    assert historical["status"] == "RESOURCE_GATED_NOT_EXECUTED"
    assert historical["m6_overwritten"] is False
    assert current["created"] is True
    assert current["status"] == "COMPLETE"
    assert current["m6_overwritten"] is False


def test_directed_conditional_tail_is_sharper_than_m6() -> None:
    m7 = json.loads((DATA / "EXACT_BALL7_TENSOR_TAIL.json").read_text(encoding="utf-8"))
    m6 = json.loads((DATA / "EXACT_BALL6_TENSOR_TAIL.json").read_text(encoding="utf-8"))
    assert Decimal(m7["C0_per_abs_w_upper_directed"]) > 0
    assert Decimal(m7["C1_coordinate_per_abs_w_upper_directed"]) > 0
    assert Decimal(m7["coordinate_trace_C2_upper_directed"]) < Decimal(m6["coordinate_trace_C2_upper_directed"])
    assert Decimal(m7["coordinate_trace_C2_upper_directed"]) < 48
    assert m7["certified_rational_coordinate_trace_upper"] == 48
    assert "integer 48" in m7["rounding_contract"]


def test_reassessment_retains_m6_and_does_not_invent_m7_sectors() -> None:
    record = json.loads((ROOT / "production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.json").read_text(encoding="utf-8"))
    assert record["m6_baseline_retained"] is True
    assert record["m7"]["complete_exact_ball"] is False
    assert record["m7"]["beta_minus_partial_interval"] is None
    assert record["m7"]["certified_common_root_intersection"] is None
    assert record["tail_sharpening_relative_to_m6"]["root_interval_improved"] is False


def test_terminal_tensor_classification_and_m8_gate() -> None:
    record = json.loads((ROOT / "production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.json").read_text(encoding="utf-8"))
    assert record["terminal_classification"] == "TENSOR-UNRESOLVED"
    assert record["m7_completed"] is False
    assert record["m8_released"] is False
    assert record["m8_completed"] is False


def test_no_scalar_or_manuscript_promotion() -> None:
    record = json.loads((ROOT / "production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.json").read_text(encoding="utf-8"))
    assert record["scalar_route_authorized"] is False
    assert record["physical_parameters_retuned"] is False
    assert record["main_tex_modified"] is False
