#!/usr/bin/env python3
"""Derive the V3 split-heavy repair scope without mutating the V2 plan."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(r"D:\work\revise")
OLD_PLAN = ROOT / "production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
OUTDIR = ROOT / "production_code/escalations/degree24_v3_repair"
KEYS_OUT = OUTDIR / "DEG24_SPLIT_HEAVY_KEYS_V3.tsv"
SAMPLES_OUT = OUTDIR / "DEG24_MANIFEST_REPRODUCIBILITY_SAMPLE_KEYS_V3.tsv"
SUMMARY_OUT = OUTDIR / "DEG24_SPLIT_HEAVY_SCOPE_V3.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_work() -> dict[int, list[dict[str, int]]]:
    grouped: dict[int, list[dict[str, int]]] = defaultdict(list)
    for line in OLD_PLAN.read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if not fields or fields[0] != "WORK":
            continue
        values = {fields[i]: fields[i + 1] for i in range(2, len(fields), 2)}
        row = {
            "shard": int(fields[1]),
            "key": int(values["KEY"]),
            "first": int(values["ALPHA_FIRST"]),
            "last": int(values["ALPHA_LAST"]),
            "order": int(values["ORDER"]),
            "class_units": int(values["CLASS_UNITS"]),
            "raw_pairs": int(values["RAW_PAIRS"]),
        }
        if row["last"] - row["first"] + 1 != row["class_units"]:
            raise ValueError(f"bad class interval: {row}")
        if row["order"] * row["class_units"] != row["raw_pairs"]:
            raise ValueError(f"bad raw identity: {row}")
        grouped[row["key"]].append(row)
    return grouped


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    grouped = parse_work()
    affected = {key: sorted(rows, key=lambda row: (row["first"], row["last"]))
                for key, rows in grouped.items() if len(rows) > 1}
    if len(affected) != 806:
        raise ValueError(f"expected 806 split-heavy keys, found {len(affected)}")

    summaries = []
    for key, rows in sorted(affected.items()):
        expected = 1
        for row in rows:
            if row["first"] != expected:
                raise ValueError(f"V2 interval gap/overlap for 24T{key}: expected {expected}, got {row['first']}")
            expected = row["last"] + 1
        orders = {row["order"] for row in rows}
        if len(orders) != 1:
            raise ValueError(f"order mismatch for 24T{key}")
        summaries.append({
            "key": key,
            "order": orders.pop(),
            "old_class_units": expected - 1,
            "old_raw_pairs": sum(row["raw_pairs"] for row in rows),
            "old_segment_count": len(rows),
            "old_shards": ",".join(str(row["shard"]) for row in rows),
        })

    with KEYS_OUT.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)

    by_classes = sorted(summaries, key=lambda row: (row["old_class_units"], row["key"]))
    by_order = sorted(summaries, key=lambda row: (row["order"], row["key"]))
    sample_roles = [
        ("smallest_class_count", by_classes[0]),
        ("median_class_count", by_classes[len(by_classes) // 2]),
        ("largest_group_order", by_order[-1]),
        ("highest_class_count", by_classes[-1]),
        ("shard208_regression", next(row for row in summaries if row["key"] == 13493)),
    ]
    with SAMPLES_OUT.open("x", encoding="utf-8", newline="") as handle:
        fieldnames = ["role", *summaries[0].keys()]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for role, row in sample_roles:
            writer.writerow({"role": role, **row})

    summary = {
        "schema": "DEG24_SPLIT_HEAVY_REPAIR_SCOPE_V3",
        "source_plan": OLD_PLAN.relative_to(ROOT).as_posix(),
        "source_plan_sha256": sha256(OLD_PLAN),
        "affected_split_heavy_keys": len(summaries),
        "old_split_heavy_class_units": sum(row["old_class_units"] for row in summaries),
        "old_split_heavy_raw_pairs": sum(row["old_raw_pairs"] for row in summaries),
        "old_split_heavy_work_segments": sum(row["old_segment_count"] for row in summaries),
        "key_registry": KEYS_OUT.relative_to(ROOT).as_posix(),
        "key_registry_sha256": sha256(KEYS_OUT),
        "sample_registry": SAMPLES_OUT.relative_to(ROOT).as_posix(),
        "sample_registry_sha256": sha256(SAMPLES_OUT),
    }
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
