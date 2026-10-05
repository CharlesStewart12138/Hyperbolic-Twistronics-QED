"""Run P2-14-15 wall-time, memory, and matrix-dimension measurement fixtures."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from resource_metrics import profile_callable


def dense_open_chain(size: int, *, diagonal: float, hopping: float) -> np.ndarray:
    matrix = np.zeros((size, size), dtype=float)
    np.fill_diagonal(matrix, diagonal)
    indices = np.arange(size - 1)
    matrix[indices, indices + 1] = hopping
    matrix[indices + 1, indices] = hopping
    return matrix


def flatten_record(record: dict[str, object]) -> dict[str, object]:
    return {
        key: json.dumps(value, separators=(",", ":")) if isinstance(value, (list, dict)) else value
        for key, value in record.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "environment" / "p2_14_15_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_15_resource_metrics",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    warmup = dense_open_chain(32, diagonal=0.1, hopping=0.8)
    np.linalg.eigvalsh(warmup)
    records = []
    for case in config["cases"]:
        size = int(case["dimension"])
        matrix = dense_open_chain(
            size, diagonal=float(case["diagonal"]), hopping=float(case["hopping"])
        )
        record, values = profile_callable(
            lambda: np.linalg.eigvalsh(matrix),
            label=str(case["case_id"]),
            matrix_dimension=size,
            matrix_storage_bytes=int(matrix.nbytes),
            repeats=int(case["repeats"]),
        )
        expected_storage = size * size * matrix.dtype.itemsize
        record["dtype"] = str(matrix.dtype)
        record["expected_matrix_storage_bytes"] = expected_storage
        record["matrix_storage_match"] = bool(matrix.nbytes == expected_storage)
        record["eigenvalue_count"] = len(values)
        record["eigenvalue_count_match"] = bool(len(values) == size)
        record["fixture_scope"] = "RESOURCE_INSTRUMENTATION_VALIDATION_ONLY"
        record["status"] = "PASS" if (
            not record["failed_checks"]
            and record["matrix_storage_match"]
            and record["eigenvalue_count_match"]
        ) else "FAIL"
        records.append(record)
    dimensions = [int(record["matrix_dimension"]) for record in records]
    global_checks = {
        "configured_cases_present": bool(len(records) == len(config["cases"])),
        "dimensions_strictly_increasing": bool(all(current > previous for previous, current in zip(dimensions, dimensions[1:]))),
        "all_case_checks_pass": bool(all(record["status"] == "PASS" for record in records)),
    }
    failed_global_checks = sorted(name for name, passed in global_checks.items() if not passed)
    with (args.output_dir / "runs.csv").open("w", encoding="utf-8", newline="") as handle:
        flattened = [flatten_record(record) for record in records]
        writer = csv.DictWriter(handle, fieldnames=list(flattened[0].keys()))
        writer.writeheader()
        writer.writerows(flattened)
    summary = {
        "task_id": "P2-14-15",
        "status": "PASS" if not failed_global_checks else "FAIL",
        "scientific_scope": "Instrumentation validation only; manuscript production runs are pending.",
        "metric_definitions": {
            "wall_time": "time.perf_counter_ns around the solver call only",
            "rss": "psutil process resident set before and after repeated calls",
            "process_peak": "OS-reported peak working set when available",
            "python_peak": "tracemalloc peak during repeated calls",
            "matrix_dimension": "dense square matrix row/column count",
            "matrix_storage": "NumPy ndarray nbytes",
        },
        "global_checks": global_checks,
        "failed_global_checks": failed_global_checks,
        "case_count": len(records),
        "cases": records,
        "data_file": "runs.csv",
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
