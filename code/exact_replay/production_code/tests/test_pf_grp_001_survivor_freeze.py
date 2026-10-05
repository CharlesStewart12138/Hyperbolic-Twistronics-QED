"""Validate the zero-survivor production freeze decision."""

import json
from pathlib import Path


ROOT = Path("data/production/quotient_reaudit_geometric_shell_final")


def test_zero_survivors_means_no_production_quotient() -> None:
    summary = json.loads((ROOT / "REAUDIT_SUMMARY.json").read_text(encoding="utf-8"))
    decision = json.loads((ROOT / "NO_QUOTIENT_FROZEN.json").read_text(encoding="utf-8"))
    assert summary["accepted_count"] == 0
    assert decision["status"] == "NO_QUOTIENT_FROZEN"
    assert decision["group_quotient_json_created"] is False
    assert decision["smoke_hamiltonian_status"].startswith("SKIPPED_CONDITION_FALSE")
    assert not (ROOT / "group_quotient.json").exists()
