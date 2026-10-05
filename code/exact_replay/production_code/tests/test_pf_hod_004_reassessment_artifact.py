import json
from pathlib import Path

from production_code.hodge.hodge_root_budget import REQUIRED_CURRENT_INPUTS


def test_reassessment_artifact_has_no_false_root() -> None:
    record = json.loads(
        Path("production_code/hodge/PF_HOD_004_REASSESSMENT.json").read_text(encoding="utf-8")
    )
    assert record["status"] == "Blocked"
    assert record["required_current_inputs"] == list(REQUIRED_CURRENT_INPUTS)
    assert "PF-KER-005" in record["blocked_dependencies"]
    assert "theta_H" not in record
    assert "root_interval" not in record

