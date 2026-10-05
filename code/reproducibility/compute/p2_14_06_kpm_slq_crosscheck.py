"""Run P2-14-06 KPM/SLQ cross-checks on analytic spectral fixtures."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import scipy.linalg


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
RANDOM_ROOT = PROJECT_ROOT / "reproducibility" / "random"
for entry in (SRC_ROOT, RANDOM_ROOT):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from seed_registry import config_sha256, numpy_rng
from spectrum import cdf_from_atoms, cdf_from_density, kpm_density, scale_hermitian, slq_quadrature


def open_chain_matrix(size: int, diagonal: float, hopping: float, phase: float) -> np.ndarray:
    matrix = np.zeros((size, size), dtype=complex if phase != 0.0 else float)
    np.fill_diagonal(matrix, diagonal)
    forward = hopping * np.exp(1j * phase) if phase != 0.0 else hopping
    indices = np.arange(size - 1)
    matrix[indices, indices + 1] = forward
    matrix[indices + 1, indices] = np.conjugate(forward)
    return matrix


def weighted_moments(atoms: np.ndarray, weights: np.ndarray) -> tuple[float, float]:
    mean = float(np.sum(weights * atoms))
    variance = float(np.sum(weights * np.square(atoms - mean)))
    return mean, variance


def run_case(case: dict[str, object], output_dir: Path) -> dict[str, object]:
    matrix = open_chain_matrix(
        int(case["dimension"]), float(case["diagonal"]), float(case["hopping"]), float(case["phase"])
    )
    exact_values = scipy.linalg.eigvalsh(matrix)
    span = float(exact_values[-1] - exact_values[0])
    padding = float(case["bound_padding_fraction"]) * span
    lower = float(exact_values[0] - padding)
    upper = float(exact_values[-1] + padding)
    scaled, scaling = scale_hermitian(matrix, lower=lower, upper=upper)
    kpm = kpm_density(
        scaled,
        scaling,
        moment_count=int(case["kpm_moment_count"]),
        probe_count=int(case["kpm_probe_count"]),
        rng=numpy_rng("kpm.random_vectors", int(case["kpm_stream_index"])),
        grid_size=int(case["grid_size"]),
    )
    slq = slq_quadrature(
        scaled,
        scaling,
        depth=int(case["slq_depth"]),
        probe_count=int(case["slq_probe_count"]),
        rng=numpy_rng("slq.random_vectors", int(case["slq_stream_index"])),
    )
    energy = np.asarray(kpm["energy"])
    kpm_density_values = np.asarray(kpm["density"])
    kpm_cdf = cdf_from_density(energy, kpm_density_values)
    slq_cdf = cdf_from_atoms(energy, np.asarray(slq["atoms"]), np.asarray(slq["weights"]))
    exact_weights = np.full(exact_values.size, 1.0 / exact_values.size)
    exact_cdf = cdf_from_atoms(energy, exact_values, exact_weights)

    kpm_mean = float(np.trapz(energy * kpm_density_values, energy))
    kpm_variance = float(np.trapz(np.square(energy - kpm_mean) * kpm_density_values, energy))
    slq_mean, slq_variance = weighted_moments(np.asarray(slq["atoms"]), np.asarray(slq["weights"]))
    exact_mean = float(np.mean(exact_values))
    exact_variance = float(np.mean(np.square(exact_values - exact_mean)))
    metrics = {
        "kpm_mass_error_before_normalization": abs(float(kpm["mass_before_normalization"]) - 1.0),
        "slq_mass_error_before_normalization": abs(float(slq["mass_before_normalization"]) - 1.0),
        "kpm_exact_cdf_linf": float(np.max(np.abs(kpm_cdf - exact_cdf))),
        "slq_exact_cdf_linf": float(np.max(np.abs(slq_cdf - exact_cdf))),
        "kpm_slq_cdf_linf": float(np.max(np.abs(kpm_cdf - slq_cdf))),
        "kpm_mean_abs_error": abs(kpm_mean - exact_mean),
        "slq_mean_abs_error": abs(slq_mean - exact_mean),
        "kpm_variance_abs_error": abs(kpm_variance - exact_variance),
        "slq_variance_abs_error": abs(slq_variance - exact_variance),
    }
    tolerances = case["tolerances"]
    checks = {name: metrics[name] <= float(limit) for name, limit in tolerances.items()}
    failed = sorted(name for name, passed in checks.items() if not passed)

    case_dir = output_dir / str(case["case_id"])
    case_dir.mkdir(parents=True, exist_ok=True)
    with (case_dir / "cdf.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["energy", "exact_cdf", "kpm_cdf", "slq_cdf", "kpm_density"])
        writer.writerows(zip(energy, exact_cdf, kpm_cdf, slq_cdf, kpm_density_values, strict=True))
    return {
        "case_id": case["case_id"],
        "status": "PASS" if not failed else "FAIL",
        "fixture_scope": "ANALYTIC_INFRASTRUCTURE_VALIDATION_ONLY",
        "dimension": matrix.shape[0],
        "spectral_bounds": {"lower": lower, "upper": upper},
        "kpm": {
            "namespace": "kpm.random_vectors",
            "stream_index": case["kpm_stream_index"],
            "moment_count": case["kpm_moment_count"],
            "probe_count": case["kpm_probe_count"],
        },
        "slq": {
            "namespace": "slq.random_vectors",
            "stream_index": case["slq_stream_index"],
            "depth": case["slq_depth"],
            "probe_count": case["slq_probe_count"],
            "minimum_realized_depth": slq["minimum_realized_depth"],
            "maximum_realized_depth": slq["maximum_realized_depth"],
        },
        "exact_moments": {"mean": exact_mean, "variance": exact_variance},
        "estimated_moments": {
            "kpm_mean": kpm_mean,
            "kpm_variance": kpm_variance,
            "slq_mean": slq_mean,
            "slq_variance": slq_variance,
        },
        "metrics": metrics,
        "tolerances": tolerances,
        "checks": checks,
        "failed_checks": failed,
        "data_file": f"{case['case_id']}/cdf.csv",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "spectrum" / "p2_14_06_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_06_kpm_slq_crosscheck",
    )
    args = parser.parse_args()
    config = json.loads(args.cases.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = [run_case(case, args.output_dir) for case in config["cases"]]
    failed_cases = [result["case_id"] for result in results if result["status"] != "PASS"]
    summary = {
        "task_id": "P2-14-06",
        "status": "PASS" if not failed_cases else "FAIL",
        "scientific_scope": "Infrastructure validation only; manuscript DOS Hamiltonians are not yet reconstructed.",
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
