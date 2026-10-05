#!/usr/bin/env python3
"""Extract the three fresh-process ordinal-844 representatives for exact V3 class mapping."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
OUTPUT = BASE / "DEG24_SHARD208_ORDINAL844_FORENSIC_ROWS_V3.g"
RUNS = (
    ("FRESH_SEED_1", 1, BASE / "DEG24_SHARD208_FORENSIC_RUN01_V3.tsv"),
    ("FRESH_SEED_12345", 12345, BASE / "DEG24_SHARD208_FORENSIC_RUN02_V3.tsv"),
    ("FRESH_SEED_987654321", 987654321, BASE / "DEG24_SHARD208_FORENSIC_RUN03_V3.tsv"),
)


def gap_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite {OUTPUT}")
    records = []
    for run_id, seed, path in RUNS:
        rows = list(csv.reader(path.open(encoding="utf-8"), delimiter="\t"))
        matches = [row for row in rows if len(row) == 9 and row[0] == "CLASS" and row[1] == "844"]
        if len(matches) != 1:
            raise ValueError(f"expected one ordinal-844 row: {path}")
        row = matches[0]
        images = [[int(value) for value in image.split(",")] for image in row[4].split(";")]
        if len(images) != 4 or any(len(image) != 24 for image in images):
            raise ValueError(f"bad representative serialization: {path}")
        records.append({"run_id": run_id, "seed": seed, "size": int(row[5]), "centralizer": int(row[6]), "images": images})
    if [record["size"] for record in records] != [192, 1536, 192]:
        raise ValueError("frozen forensic anchor mismatch")
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("D24C8_ORDINAL844_FORENSIC_ROWS:=[\n")
        for index, record in enumerate(records):
            images = ",".join("[" + ",".join(str(value) for value in image) + "]" for image in record["images"])
            suffix = "," if index + 1 < len(records) else ""
            handle.write(
                f"rec(runId:={gap_string(record['run_id'])},seed:={record['seed']},sourceOrdinalDiagnostic:=844,classSize:={record['size']},centralizerSize:={record['centralizer']},images:=[{images}]){suffix}\n"
            )
        handle.write("];\n")
    print(f"SHARD208_ORDINAL844_FORENSIC_ROWS_PASS\tRUNS\t{len(records)}")


if __name__ == "__main__":
    main()
