"""Run P2-14-05 dense/sparse solver cross-checks on analytic fixtures."""

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

from solvers import CrosscheckTolerances, crosscheck_hermitian


def open_chain_matrix(size: int, diagonal: float, hopping: float, phase: float) -> np.ndarray:
    """Return an open Hermitian nearest-neighbour chain with a Peierls phase."""

    dtype = complex if phase != 0.0 else float
    matrix = np.zeros((size, size), dtype=dtype)
    np.fill_diagonal(matrix, diagonal)
    forward = hopping * np.exp(1j * phase) if phase != 0.0 else hopping
    for index in range(size - 1):
        matrix[index, index + 1] = forward
        matrix[index + 1, index] = np.conjugate(forward)
    return matrix


def analytic_open_chain_eigenvalues(size: int, diagonal: float, hopping: float) -> np.ndarray:
    modes = np.arange(1, size + 1, dtype=float)
    values = diagonal + 2.0 * hopping * np.cos(modes * np.pi / (size + 1))
    return np.sort(values)


def run_case(case: dict[str, object], tolerances: CrosscheckTolerances) -> dict[str, object]:
    size = int(case["dimension"])
    k = int(case["k"])
    edge = str(case["edge"])
    diagonal = float(case["diagonal"])
    hopping = float(case["hopping"])
    phase = float(case["phase"])
    matrix = open_chain_matrix(size, diagonal, hopping, phase)
    result = crosscheck_hermitian(matrix, k=k, edge=edge, tolerances=tolerances)
    analytic_all = analytic_open_chain_eigenvalues(size, diagonal, hopping)
    analytic_selected = analytic_all[:k] if edge == "lowest" else analytic_all[-k:]
    dense_values = np.asarray(result["dense_eigenvalues"])
    sparse_values = np.asarray(result["sparse_eigenvalues"])
    dense_analytic_error = float(np.max(np.abs(dense_values - analytic_selected)))
    sparse_analytic_error = float(np.max(np.abs(sparse_values - analytic_selected)))
    analytic_tolerance = float(case["analytic_tolerance"])
    analytic_checks = {
        "dense_matches_analytic": dense_analytic_error <= analytic_tolerance,
        "sparse_matches_analytic": sparse_analytic_error <= analytic_tolerance,
    }
    result["case_id"] = case["case_id"]
    result["fixture_scope"] = "ANALYTIC_INFRASTRUCTURE_VALIDATION_ONLY"
    result["analytic_reference"] = "d + 2 t cos(m pi/(n+1)); phase removable by open-chain gauge transform"
    result["analytic_eigenvalues"] = [float(value) for value in analytic_selected]
    result["metrics"]["dense_max_abs_analytic_difference"] = dense_analytic_error
    result["metrics"]["sparse_max_abs_analytic_difference"] = sparse_analytic_error
    result["checks"].update(analytic_checks)
    result["failed_checks"] = sorted(name for name, passed in result["checks"].items() if not passed)
    result["status"] = "PASS" if not result["failed_checks"] else "FAIL"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "solvers" / "p2_14_05_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_05_solver_crosscheck",
    )
    args = parser.parse_args()
    config = json.loads(args.cases.read_text(encoding="utf-8"))
    tolerances = CrosscheckTolerances(**config["tolerances"])
    results = [run_case(case, tolerances) for case in config["cases"]]
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-05",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Infrastructure validation only; manuscript Hamiltonians are not yet reconstructed.",
        "dense_solver": "scipy.linalg.eigh",
        "sparse_solver": "scipy.sparse.linalg.eigsh",
        "case_count": len(results),
        "failed_cases": failed_cases,
        "cases": results,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (args.output_dir / "cases.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_id", "status", "dimension", "k", "edge", "matrix_dtype",
                "max_abs_eigenvalue_difference", "dense_relative_frobenius_residual",
                "sparse_relative_frobenius_residual", "dense_max_abs_analytic_difference",
                "sparse_max_abs_analytic_difference",
            ],
        )
        writer.writeheader()
        for result in results:
            metrics = result["metrics"]
            writer.writerow({
                "case_id": result["case_id"],
                "status": result["status"],
                "dimension": result["dimension"],
                "k": result["k"],
                "edge": result["edge"],
                "matrix_dtype": result["matrix_dtype"],
                "max_abs_eigenvalue_difference": metrics["max_abs_eigenvalue_difference"],
                "dense_relative_frobenius_residual": metrics["dense_relative_frobenius_residual"],
                "sparse_relative_frobenius_residual": metrics["sparse_relative_frobenius_residual"],
                "dense_max_abs_analytic_difference": metrics["dense_max_abs_analytic_difference"],
                "sparse_max_abs_analytic_difference": metrics["sparse_max_abs_analytic_difference"],
            })
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
