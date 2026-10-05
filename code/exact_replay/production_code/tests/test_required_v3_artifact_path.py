import json
from pathlib import Path


def test_directive_v3_path_contains_complete_summary() -> None:
    directory = Path("data/production/quotient_search_v3")
    expected = {
        "candidates_v3.csv",
        "candidates_v3.jsonl",
        "b3_survivors.csv",
        "rejection_log.csv",
        "V3_SUMMARY.json",
    }
    assert expected.issubset({path.name for path in directory.iterdir()})
    summary = json.loads((directory / "V3_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["candidate_count"] == 279
    assert summary["b3_survivor_count"] == 203
    assert summary["production_survivor_count"] == 0

