import json
import math
from pathlib import Path

from production_code.kernel.observable_tail_budget import deterministic_reassessment_record


def test_frozen_json_matches_deterministic_reassessment() -> None:
    path = Path("production_code/kernel/PF_KER_005_CANONICAL_TAILS.json")
    frozen = json.loads(path.read_text(encoding="utf-8"))
    computed = deterministic_reassessment_record()
    assert frozen["task_id"] == computed["task_id"]
    assert frozen["scope"] == computed["scope"]
    assert frozen["status"] == "Blocked"
    assert frozen["production_cutoff_closes"] is False
    for actual, expected in zip(frozen["selected_tail_rows_per_abs_w"], computed["selected_tail_rows_per_abs_w"]):
        assert actual["first_omitted_shell"] == expected["first_omitted_shell"]
        for key in (
            "c0_per_abs_w",
            "c1_coordinate_per_abs_w",
            "c1_hodge_per_abs_w",
            "c2_coordinate_per_abs_w",
            "c2_hodge_per_abs_w",
        ):
            assert math.isclose(actual[key], expected[key], rel_tol=2e-15)

