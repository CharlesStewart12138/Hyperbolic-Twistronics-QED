"""Run P2-14-14 independent real-space and analytic code-path validation."""

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

from independent_paths.analytic_cycle_path import analytic_cycle_spectrum, analytic_spectral_observables
from independent_paths.dense_cycle_path import dense_cycle_spectrum, dense_spectral_observables


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "independent_paths" / "p2_14_14_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_14_independent_code_path",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for case in config["cases"]:
        dense_values = dense_cycle_spectrum(
            int(case["dimension"]),
            diagonal=float(case["diagonal"]),
            hopping=float(case["hopping"]),
            total_flux=float(case["total_flux"]),
        )
        analytic_values = np.asarray(analytic_cycle_spectrum(
            int(case["dimension"]),
            diagonal=float(case["diagonal"]),
            hopping=float(case["hopping"]),
            total_flux=float(case["total_flux"]),
        ))
        dense_observables = dense_spectral_observables(dense_values, heat_time=float(case["heat_time"]))
        analytic_observables = analytic_spectral_observables(
            [float(value) for value in analytic_values], heat_time=float(case["heat_time"])
        )
        eigenvalue_max_error = float(np.max(np.abs(dense_values - analytic_values)))
        observable_errors = {
            name: abs(dense_observables[name] - analytic_observables[name])
            for name in dense_observables
        }
        tolerance = float(case["absolute_tolerance"])
        checks = {"eigenvalue_array": bool(eigenvalue_max_error <= tolerance)}
        checks.update({name: bool(error <= tolerance) for name, error in observable_errors.items()})
        failed = sorted(name for name, passed in checks.items() if not passed)
        case_dir = args.output_dir / str(case["case_id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        rows = [
            {
                "index": index,
                "dense_real_space": float(dense_value),
                "analytic_momentum": float(analytic_value),
                "absolute_error": abs(float(dense_value - analytic_value)),
            }
            for index, (dense_value, analytic_value) in enumerate(zip(dense_values, analytic_values))
        ]
        with (case_dir / "eigenvalues.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        results.append({
            "case_id": case["case_id"],
            "status": "PASS" if not failed else "FAIL",
            "fixture_scope": "INDEPENDENT_PATH_INFRASTRUCTURE_VALIDATION_ONLY",
            "dimension": int(case["dimension"]),
            "eigenvalue_max_absolute_error": eigenvalue_max_error,
            "dense_observables": dense_observables,
            "analytic_observables": analytic_observables,
            "observable_absolute_errors": observable_errors,
            "checks": checks,
            "failed_checks": failed,
            "data_file": f"{case['case_id']}/eigenvalues.csv",
        })
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-14",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Independent paths validated; manuscript flagship result selection and reconstruction are pending.",
        "path_a": "Real-space dense Hermitian matrix assembly plus numpy.linalg.eigvalsh.",
        "path_b": "Direct momentum quantization plus Python math evaluation; no matrix assembly or eigensolver.",
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
