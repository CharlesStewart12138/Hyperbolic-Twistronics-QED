"""Measure resource metrics for registered dense, sparse, KPM, and SLQ calls."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy.linalg
import scipy.sparse.linalg


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.random.seed_registry import config_sha256, numpy_rng  # noqa: E402
from reproducibility.src.resource_metrics import profile_callable  # noqa: E402
from reproducibility.src.spectrum.finite_registered import load_coo_csv  # noqa: E402
from reproducibility.src.spectrum.stochastic_dos import (  # noqa: E402
    kpm_density,
    scale_hermitian,
    slq_quadrature,
)


def deterministic_start(size: int) -> np.ndarray:
    indices = np.arange(1, size + 1, dtype=float)
    vector = np.cos(np.pi * indices / (size + 1)) + 0.37 * np.sin(2.0 * np.pi * indices / (size + 1))
    return vector / np.linalg.norm(vector)


def flatten(record: dict[str, object]) -> dict[str, object]:
    return {key: json.dumps(value, separators=(",", ":")) if isinstance(value, (list, dict)) else value for key, value in record.items()}


def run(output_dir: Path, *, matrix_path: Path, dimension: int) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sparse = load_coo_csv(matrix_path, dimension=dimension)
    dense = sparse.toarray()
    sparse_storage = int(sparse.data.nbytes + sparse.indices.nbytes + sparse.indptr.nbytes)
    scipy.linalg.eigvalsh(dense[:32, :32], check_finite=True, driver="evr")
    exact_values = scipy.linalg.eigvalsh(dense, check_finite=True, driver="evr")
    span = float(exact_values[-1] - exact_values[0])
    scaled, scaling = scale_hermitian(
        sparse,
        lower=float(exact_values[0] - 0.02 * span),
        upper=float(exact_values[-1] + 0.02 * span),
    )

    records = []
    dense_record, dense_values = profile_callable(
        lambda: scipy.linalg.eigvalsh(dense, check_finite=True, driver="evr"),
        label="registered_dense_full_spectrum",
        matrix_dimension=dimension,
        matrix_storage_bytes=int(dense.nbytes),
        repeats=3,
    )
    dense_record.update({
        "solver": "scipy.linalg.eigvalsh(driver='evr')",
        "matrix_format": "dense_float64",
        "output_count": int(len(dense_values)),
        "output_valid": bool(len(dense_values) == dimension and np.all(np.isfinite(dense_values))),
    })
    records.append(dense_record)

    start = deterministic_start(dimension)
    sparse_record, sparse_values = profile_callable(
        lambda: scipy.sparse.linalg.eigsh(
            sparse, k=1, which="SA", tol=1.0e-12, maxiter=max(20 * dimension, 1000), v0=start,
            return_eigenvectors=False,
        ),
        label="registered_sparse_lowest_extremum",
        matrix_dimension=dimension,
        matrix_storage_bytes=sparse_storage,
        repeats=3,
    )
    sparse_record.update({
        "solver": "scipy.sparse.linalg.eigsh(k=1,which='SA')",
        "matrix_format": "csr_float64",
        "output_count": int(len(sparse_values)),
        "output_valid": bool(len(sparse_values) == 1 and abs(float(sparse_values[0]) - float(exact_values[0])) <= 2.0e-9),
    })
    records.append(sparse_record)

    kpm_record, kpm = profile_callable(
        lambda: kpm_density(
            scaled,
            scaling,
            moment_count=160,
            probe_count=32,
            rng=numpy_rng("kpm.random_vectors", 100),
            grid_size=2001,
        ),
        label="registered_KPM_batch",
        matrix_dimension=dimension,
        matrix_storage_bytes=sparse_storage,
        repeats=2,
    )
    kpm_record.update({
        "solver": "Jackson-KPM(moment_count=160,probe_count=32)",
        "matrix_format": "csr_float64",
        "output_count": int(len(kpm["energy"])),
        "output_valid": bool(
            len(kpm["energy"]) == 2001
            and np.all(np.isfinite(kpm["density"]))
            and math.isfinite(float(kpm["mass_before_normalization"]))
        ),
    })
    records.append(kpm_record)

    slq_record, slq = profile_callable(
        lambda: slq_quadrature(
            scaled,
            scaling,
            depth=64,
            probe_count=32,
            rng=numpy_rng("slq.random_vectors", 100),
            breakdown_tolerance=1.0e-14,
        ),
        label="registered_SLQ_batch",
        matrix_dimension=dimension,
        matrix_storage_bytes=sparse_storage,
        repeats=2,
    )
    slq_record.update({
        "solver": "fully-reorthogonalized-SLQ(depth=64,probe_count=32)",
        "matrix_format": "csr_float64",
        "output_count": int(len(slq["atoms"])),
        "output_valid": bool(
            len(slq["atoms"]) > 0
            and np.all(np.isfinite(slq["atoms"]))
            and abs(float(np.sum(slq["weights"])) - 1.0) <= 1.0e-12
        ),
    })
    records.append(slq_record)

    for record in records:
        record["status"] = "PASS" if not record["failed_checks"] and record["output_valid"] else "FAIL"
        record["scope"] = "REGISTERED_512_DIMENSIONAL_VALIDATION_HAMILTONIAN"
    with (output_dir / "runs.csv").open("w", encoding="utf-8", newline="") as handle:
        flattened = [flatten(record) for record in records]
        writer = csv.DictWriter(handle, fieldnames=list(flattened[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(flattened)
    summary = {
        "task_id": "P2-14-15",
        "status": "PASS" if all(record["status"] == "PASS" for record in records) else "FAIL",
        "scope": "REGISTERED_RECONSTRUCTED_VALIDATION_RUNS_MACHINE_SPECIFIC_METRICS",
        "matrix_path": matrix_path.relative_to(PROJECT_ROOT).as_posix(),
        "matrix_dimension": dimension,
        "dense_matrix_storage_bytes": int(dense.nbytes),
        "sparse_matrix_nnz": int(sparse.nnz),
        "sparse_matrix_storage_bytes": sparse_storage,
        "seed_config_sha256": config_sha256(),
        "metric_definitions": {
            "wall_time": "time.perf_counter_ns around the solver call only; warm-up excluded",
            "rss": "psutil process resident set before and after repeated calls",
            "process_peak": "OS-reported peak working set when available",
            "python_peak": "tracemalloc peak during repeated calls; native allocations may appear only in process metrics",
            "matrix_dimension": "registered bilayer Hamiltonian row/column count",
            "matrix_storage": "dense ndarray nbytes or CSR data+indices+indptr nbytes",
        },
        "records": records,
        "data_file": "runs.csv",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    if summary["status"] != "PASS":
        raise RuntimeError("registered resource metrics failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_15_registered_resource_metrics",
    )
    parser.add_argument(
        "--matrix-path", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_hamiltonian_reconstruction" / "bilayer_h1_coo.csv",
    )
    parser.add_argument("--dimension", type=int, default=512)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, matrix_path=args.matrix_path, dimension=args.dimension), indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
