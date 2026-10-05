"""Build the exact finite-map manifest for based separator evaluation.

The output contains the image of every S8_GEOMETRIC generator in each base
S4/S5/S6 map.  Practical-core membership is recovered exactly by combining
the base-kernel decision over a complete C8 orbit and the frozen parity bit.
The 24 cumulative v3 columns are represented as intersections of their two
registered parent cores.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.quotient_search_v2 import S4_IDENTITY, S4_TABLE, base_s4_candidate, V2Seed
from production_code.group.quotient_search_v3_geometric import base_candidate, symmetric_group_data


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "data" / "production" / "quotient_reaudit_geometric_shell_final" / "candidates_geometric_shell_reaudit.jsonl"
V3 = ROOT / "data" / "production" / "quotient_search_v3" / "candidates_v3.jsonl"
OUTPUT = ROOT / "data" / "production" / "quotient_separator" / "candidate_manifest.tsv"


def geometric_images(candidate) -> list[int]:
    return [candidate.evaluate_word(GEOMETRIC_TO_STANDARD_WORD[i]) for i in range(8)]


def main() -> None:
    v2_records = [json.loads(line) for line in V2.read_text(encoding="utf-8").splitlines() if line]
    v3_records = [json.loads(line) for line in V3.read_text(encoding="utf-8").splitlines() if line]
    rows: list[dict[str, object]] = []

    for record in v2_records:
        seed = V2Seed(record["candidate_id"], tuple(record["base_generator_indices"]))
        candidate = base_s4_candidate(seed)
        if candidate.identity != S4_IDENTITY or candidate.multiplication_table != S4_TABLE:
            raise AssertionError("S4 registry drift")
        rows.append({
            "candidate_id": record["candidate_id"],
            "family": "V2_S4_CORE",
            "degree": 4,
            "identity": candidate.identity,
            "images": geometric_images(candidate),
            "parent_left": -1,
            "parent_right": -1,
        })

    for record in v3_records:
        if "parents" in record:
            rows.append({
                "candidate_id": record["candidate_id"],
                "family": record["family"],
                "degree": 0,
                "identity": -1,
                "images": [-1] * 8,
                "parent_left_id": record["parents"][0],
                "parent_right_id": record["parents"][1],
            })
            continue
        degree = int(record["base_group"][1:])
        data = symmetric_group_data(degree)
        images = tuple(int(value) for value in record["base_generator_indices"])
        candidate = base_candidate(data, record["candidate_id"], images)
        rows.append({
            "candidate_id": record["candidate_id"],
            "family": record["family"],
            "degree": degree,
            "identity": candidate.identity,
            "images": geometric_images(candidate),
            "parent_left": -1,
            "parent_right": -1,
        })

    ids = {str(row["candidate_id"]): index for index, row in enumerate(rows)}
    if len(ids) != len(rows):
        raise AssertionError("duplicate candidate ID")
    for row in rows:
        if "parent_left_id" in row:
            row["parent_left"] = ids[str(row.pop("parent_left_id"))]
            row["parent_right"] = ids[str(row.pop("parent_right_id"))]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = ["column_index", "candidate_id", "family", "degree", "identity"] + [f"g{i}" for i in range(8)] + ["parent_left", "parent_right"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, dialect="excel-tab")
        writer.writeheader()
        for index, row in enumerate(rows):
            writer.writerow({
                "column_index": index,
                "candidate_id": row["candidate_id"],
                "family": row["family"],
                "degree": row["degree"],
                "identity": row["identity"],
                **{f"g{i}": row["images"][i] for i in range(8)},
                "parent_left": row["parent_left"],
                "parent_right": row["parent_right"],
            })

    singles = sum(int(row["degree"]) > 0 for row in rows)
    composites = len(rows) - singles
    print(json.dumps({
        "output": str(OUTPUT),
        "candidates": len(rows),
        "v2": len(v2_records),
        "v3": len(v3_records),
        "single_base_maps": singles,
        "composite_columns": composites,
    }, indent=2))


if __name__ == "__main__":
    main()
