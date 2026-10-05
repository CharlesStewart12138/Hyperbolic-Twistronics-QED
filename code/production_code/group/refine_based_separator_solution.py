"""Refine the exact cardinality-one separator by minimum actual image order."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "production" / "quotient_separator"


def main() -> None:
    with (OUT / "candidate_kernel_counts.csv").open(encoding="utf-8", newline="") as handle:
        counts = list(csv.DictReader(handle))
    v3 = {
        record["candidate_id"]: record
        for record in (
            json.loads(line)
            for line in (ROOT / "data" / "production" / "quotient_search_v3" / "candidates_v3.jsonl").read_text(encoding="utf-8").splitlines()
            if line
        )
    }
    covers = []
    for row in counts:
        if int(row["kernel_elements"]) != 0:
            continue
        record = v3.get(row["candidate_id"])
        if record is None or record.get("exact_core_order") is None:
            raise AssertionError(f"complete cover lacks exact image order: {row['candidate_id']}")
        covers.append({
            "column": int(row["column_index"]),
            "candidate_id": row["candidate_id"],
            "actual_image_order": int(record["exact_core_order"]),
        })
    if not covers:
        raise AssertionError("no cardinality-one cover")
    covers.sort(key=lambda item: (item["actual_image_order"], item["column"]))
    selected = covers[0]
    solution_path = OUT / "based_separator_solution.json"
    solution = json.loads(solution_path.read_text(encoding="utf-8"))
    solution["raw_first_cardinality_one_column"] = solution["selected_columns"][0]
    solution["cardinality_one_cover_count"] = len(covers)
    solution["selection_objective"] = [
        "minimum separator count",
        "minimum exact actual image order among minimum-count covers",
        "minimum column index as deterministic final tie-break",
    ]
    solution["selected_columns"] = [selected["column"]]
    solution["selected_candidate_ids"] = [selected["candidate_id"]]
    solution["selected_actual_image_order"] = selected["actual_image_order"]
    solution["solution_status"] = "OPTIMAL_CARDINALITY_AND_IMAGE_ORDER_WITHIN_CARDINALITY_ONE"
    solution["all_cardinality_one_covers"] = covers
    solution_path.write_text(json.dumps(solution, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cardinality_one_covers": len(covers), "selected": selected}, indent=2))


if __name__ == "__main__":
    main()
