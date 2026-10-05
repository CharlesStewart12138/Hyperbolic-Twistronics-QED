"""Run P2-14-08 automated moment and trace audits on analytic fixtures."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
RANDOM_ROOT = PROJECT_ROOT / "reproducibility" / "random"
for entry in (SRC_ROOT, RANDOM_ROOT):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from seed_registry import config_sha256, numpy_rng
from spectrum.moment_trace_audit import audit_moment_trace


def open_chain_matrix(size: int, diagonal: float, hopping: float, phase: float) -> np.ndarray:
    matrix = np.zeros((size, size), dtype=complex if phase != 0.0 else float)
    np.fill_diagonal(matrix, diagonal)
    forward = hopping * np.exp(1j * phase) if phase != 0.0 else hopping
    indices = np.arange(size - 1)
    matrix[indices, indices + 1] = forward
    matrix[indices + 1, indices] = np.conjugate(forward)
    return matrix


def analytic_open_chain_eigenvalues(size: int, diagonal: float, hopping: float) -> np.ndarray:
    modes = np.arange(1, size + 1, dtype=float)
    return np.sort(diagonal + 2.0 * hopping * np.cos(modes * np.pi / (size + 1)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "spectrum" / "p2_14_08_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_08_moment_trace_audit",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for case in config["cases"]:
        size = int(case["dimension"])
        diagonal = float(case["diagonal"])
        hopping = float(case["hopping"])
        matrix = open_chain_matrix(size, diagonal, hopping, float(case["phase"]))
        analytic_values = analytic_open_chain_eigenvalues(size, diagonal, hopping)
        result = audit_moment_trace(
            matrix,
            analytic_eigenvalues=analytic_values,
            max_order=int(case["max_order"]),
            probe_count=int(case["probe_count"]),
            rng=numpy_rng("numpy.general", int(case["stream_index"])),
            exact_tolerance=float(case["exact_tolerance"]),
            stochastic_sigma_multiplier=float(case["stochastic_sigma_multiplier"]),
            stochastic_absolute_floor=float(case["stochastic_absolute_floor"]),
        )
        result["case_id"] = case["case_id"]
        result["fixture_scope"] = "ANALYTIC_INFRASTRUCTURE_VALIDATION_ONLY"
        result["namespace"] = "numpy.general"
        result["stream_index"] = case["stream_index"]
        case_dir = args.output_dir / str(case["case_id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        with (case_dir / "moments.csv").open("w", encoding="utf-8", newline="") as handle:
            fieldnames = list(result["records"][0].keys())
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result["records"])
        result["data_file"] = f"{case['case_id']}/moments.csv"
        results.append(result)
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-08",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Infrastructure validation only; manuscript Hamiltonian moment audits are pending.",
        "seed_config_sha256": config_sha256(),
        "case_count": len(results),
        "failed_cases": failed_cases,
        "cases": results,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
