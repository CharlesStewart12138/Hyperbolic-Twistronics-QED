"""Run P2-14-09 representation-domain mesh-refinement validation fixtures."""

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

from convergence.mesh_refinement import audit_mesh_refinement


def csv_safe(record: dict[str, object]) -> dict[str, object]:
    return {key: "" if value is None else value for key, value in record.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "convergence" / "p2_14_09_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_09_mesh_refinement",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for case in config["cases"]:
        result = audit_mesh_refinement(
            levels=[int(value) for value in case["levels"]],
            origin_fractions=[float(value) for value in case["origin_fractions"]],
            beta=float(case["beta"]),
            gamma=float(case["gamma"]),
            coupling=float(case["coupling"]),
            phase_x=float(case["phase_x"]),
            phase_y=float(case["phase_y"]),
            final_relative_tolerance=float(case["final_relative_tolerance"]),
            final_origin_agreement_tolerance=float(case["final_origin_agreement_tolerance"]),
            minimum_contractions=int(case["minimum_contractions"]),
            required_reduction_factor=float(case["required_reduction_factor"]),
        )
        result["case_id"] = case["case_id"]
        result["fixture_scope"] = "ANALYTIC_INFRASTRUCTURE_VALIDATION_ONLY"
        case_dir = args.output_dir / str(case["case_id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        with (case_dir / "levels.csv").open("w", encoding="utf-8", newline="") as handle:
            fieldnames = list(result["records"][0].keys())
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_safe(record) for record in result["records"])
        result["data_file"] = f"{case['case_id']}/levels.csv"
        results.append(result)
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-09",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Infrastructure validation only; manuscript mBZ and representation domains are pending.",
        "case_count": len(results),
        "failed_cases": failed_cases,
        "cases": results,
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

