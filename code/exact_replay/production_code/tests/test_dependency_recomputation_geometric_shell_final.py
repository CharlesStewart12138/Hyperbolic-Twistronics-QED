import csv
import json
from pathlib import Path


def test_final_dependency_record_has_zero_active_tasks() -> None:
    record = json.loads(
        Path("production_code/group/DEPENDENCY_RECOMPUTATION_GEOMETRIC_SHELL_FINAL.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["master_task_count"] == 239
    assert record["final_status_counts"] == {
        "Done": 47,
        "Fixed": 45,
        "Deferred": 15,
        "Blocked": 30,
        "Not Started": 102,
        "In Progress": 0,
    }
    assert record["excel_formula_errors"] == 0
    assert record["master_parameter_mismatches"] == 0
    assert record["main_tex_modified"] is False


def test_local_and_quotient_scopes_do_not_cross_block() -> None:
    record = json.loads(
        Path("production_code/group/DEPENDENCY_RECOMPUTATION_GEOMETRIC_SHELL_FINAL.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["local"]["closed"] == ["PF-HOD-001", "PF-HOD-002"]
    assert "PF-GRP-001" not in record["local"]["real_blockers"]
    assert "PF-GRP-001" in record["finite_quotient"]["real_blockers"]
    assert record["full_bulk"]["released"] is False


def test_csv_contains_formal_nonperturbative_item() -> None:
    with Path("production_code/group/DEPENDENCY_RECOMPUTATION_GEOMETRIC_SHELL_FINAL.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = {row["task_id"]: row for row in csv.DictReader(handle)}
    assert rows["CM-047-NP"]["workbook_status"] == "Blocked"
    assert rows["CM-047-NP"]["scope"] == "LOCAL"
    assert rows["CM-045"]["dependency_state"] == "READY"

