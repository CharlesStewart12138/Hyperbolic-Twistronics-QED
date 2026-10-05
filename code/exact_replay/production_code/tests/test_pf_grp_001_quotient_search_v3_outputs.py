"""Validate the complete v3 geometric-shell search artifacts."""

import csv
import json
from pathlib import Path


ROOT = Path("data/production/quotient_search_v3_geometric")


def test_v3_outputs_have_complete_unique_inventory() -> None:
    with (ROOT / "candidates_v3.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    with (ROOT / "b3_survivors.csv").open(encoding="utf-8", newline="") as handle:
        survivors = list(csv.DictReader(handle))
    assert len(rows) == len({row["candidate_id"] for row in rows}) == 279
    assert len(survivors) == 203
    assert all(row["exact_core_order"] for row in survivors)
    assert all(row["option_B_127_156_certified"] == "False" for row in rows)


def test_v3_summary_covers_new_families_without_old_no_go() -> None:
    summary = json.loads((ROOT / "V3_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["new_nonabelian_degrees"] == [5, 6]
    assert summary["family_counts"]["CUMULATIVE_S5_S6_CORE_INTERSECTION"] == 24
    assert summary["b3_survivor_count"] == 203
    assert summary["production_survivor_count"] == 0
    assert summary["standard_shell_no_go_used"] is False
