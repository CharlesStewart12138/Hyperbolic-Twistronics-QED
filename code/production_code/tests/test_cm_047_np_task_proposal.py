import json
from pathlib import Path


def test_nonperturbative_root_task_is_formally_scoped_and_blocked() -> None:
    record = json.loads(
        Path("production_code/hodge/CM_047_NP_TASK_PROPOSAL.json").read_text(encoding="utf-8")
    )
    assert record["task_id"] == "CM-047-NP"
    assert record["status"] == "Blocked"
    assert {"PF-KER-005", "PF-HOD-004"}.issubset(record["dependencies"])
    assert record["scalar_root_equation"] == "b_infinity(theta,K)-2*t/w=0"
    assert "abs(q_infinity-q1)<q1 persistence premise" in record["forbidden"]
    assert "physical-flatness seeding" in record["forbidden"]


def test_direct_tensor_root_is_not_replaced_by_trace() -> None:
    record = json.loads(
        Path("production_code/hodge/CM_047_NP_TASK_PROPOSAL.json").read_text(encoding="utf-8")
    )
    assert record["tensor_root_equation"] == "2*t*C_S-w*B_infinity(theta,K)=0"
    assert "trace-only tensor root" in record["forbidden"]

