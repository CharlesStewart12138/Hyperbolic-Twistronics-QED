"""Run P2-14-13 cross-tower comparison validation fixtures."""

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

from convergence.cross_tower import audit_cross_tower


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "convergence" / "p2_14_13_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_13_cross_tower_comparison",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for case in config["cases"]:
        result = audit_cross_tower(
            tower_a_sizes=[int(value) for value in case["tower_a_sizes"]],
            tower_b_sizes=[int(value) for value in case["tower_b_sizes"]],
            heat_times=[float(value) for value in case["heat_times"]],
            diagonal=float(case["diagonal"]),
            hopping=float(case["hopping"]),
            final_relative_tolerance=float(case["final_relative_tolerance"]),
            monotonic_slack=float(case["monotonic_slack"]),
            triangle_slack=float(case["triangle_slack"]),
        )
        result["case_id"] = case["case_id"]
        result["fixture_scope"] = "ANALYTIC_INFRASTRUCTURE_VALIDATION_ONLY"
        case_dir = args.output_dir / str(case["case_id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        with (case_dir / "comparisons.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(result["records"][0].keys()))
            writer.writeheader()
            writer.writerows(result["records"])
        result["data_file"] = f"{case['case_id']}/comparisons.csv"
        results.append(result)
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-13",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Infrastructure validation only; manuscript cover towers are pending.",
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
