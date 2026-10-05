"""Validate the authoritative full 903-row re-audit artifacts."""

import csv
import json
from pathlib import Path


ROOT = Path("data/production/quotient_reaudit_geometric_shell_final")


def test_final_reaudit_artifacts_are_complete() -> None:
    with (ROOT / "candidates_geometric_shell_reaudit.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with (ROOT / "rejection_log.csv").open(encoding="utf-8", newline="") as handle:
        rejections = list(csv.DictReader(handle))
    assert len(rows) == len({row["candidate_id"] for row in rows}) == 903
    assert len(rejections) == 903
    assert all(row["RQA11"] == "True" for row in rows)
    assert not any(row["accept_reject"] == "ACCEPT" for row in rows)


def test_final_summary_classifies_first_failures_exactly() -> None:
    summary = json.loads((ROOT / "REAUDIT_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["accepted_count"] == 0
    assert summary["rejected_count"] == 903
    assert summary["first_failed_gate_counts"] == {"RQA04": 62, "RQA12": 645, "RQA13": 196}
    assert summary["presentation_B3_injective_count"] == 60
    assert summary["geometric_B3_injective_count"] == 196
