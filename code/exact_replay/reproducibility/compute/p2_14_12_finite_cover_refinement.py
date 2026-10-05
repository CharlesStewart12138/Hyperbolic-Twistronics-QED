"""Run P2-14-12 finite-cover refinement validation fixtures."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from convergence.finite_cover import audit_finite_cover


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "convergence" / "p2_14_12_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_12_finite_cover_refinement",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for case in config["cases"]:
        result = audit_finite_cover(
            cover_sizes=[int(value) for value in case["cover_sizes"]],
            heat_times=[float(value) for value in case["heat_times"]],
            diagonal=float(case["diagonal"]),
            hopping=float(case["hopping"]),
            max_centered_moment_order=int(case["max_centered_moment_order"]),
            exact_moment_tolerance=float(case["exact_moment_tolerance"]),
            final_heat_relative_tolerance=float(case["final_heat_relative_tolerance"]),
            monotonic_slack=float(case["monotonic_slack"]),
        )
        result["case_id"] = case["case_id"]
        result["fixture_scope"] = "ANALYTIC_INFRASTRUCTURE_VALIDATION_ONLY"
        case_dir = args.output_dir / str(case["case_id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        with (case_dir / "heat_trace.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(result["heat_records"][0].keys()))
            writer.writeheader()
            writer.writerows(result["heat_records"])
        with (case_dir / "moments.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(result["moment_records"][0].keys()))
            writer.writeheader()
            writer.writerows(result["moment_records"])
        result["heat_data_file"] = f"{case['case_id']}/heat_trace.csv"
        result["moment_data_file"] = f"{case['case_id']}/moments.csv"
        results.append(result)
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-12",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Infrastructure validation only; manuscript finite covers are pending.",
        "case_count": len(results),
        "failed_cases": failed_cases,
        "cases": results,
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
