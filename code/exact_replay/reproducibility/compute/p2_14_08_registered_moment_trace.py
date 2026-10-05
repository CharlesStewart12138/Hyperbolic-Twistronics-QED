"""Audit moments/traces of the registered validation Hamiltonian for P2-14-08."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.random.seed_registry import config_sha256, numpy_rng  # noqa: E402
from reproducibility.src.spectrum.finite_registered import load_coo_csv  # noqa: E402
from reproducibility.src.spectrum.moment_trace_audit import audit_moment_trace  # noqa: E402
from reproducibility.src.spectrum.stochastic_dos import scale_hermitian  # noqa: E402


def read_spectrum(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return np.asarray([float(row["energy_over_t"]) for row in csv.DictReader(handle)], dtype=float)


def run(output_dir: Path, *, matrix_path: Path, spectrum_path: Path, dimension: int) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = load_coo_csv(matrix_path, dimension=dimension)
    exact_values = np.sort(read_spectrum(spectrum_path))
    span = float(exact_values[-1] - exact_values[0])
    padding = 0.02 * span
    scaled, scaling = scale_hermitian(
        matrix,
        lower=float(exact_values[0] - padding),
        upper=float(exact_values[-1] + padding),
    )
    scaled_values = (exact_values - scaling.center) / scaling.radius
    result = audit_moment_trace(
        scaled,
        analytic_eigenvalues=scaled_values,
        max_order=4,
        probe_count=512,
        rng=numpy_rng("numpy.general", 100),
        exact_tolerance=1.0e-10,
        stochastic_sigma_multiplier=5.0,
        stochastic_absolute_floor=0.02,
    )
    result.update({
        "task_id": "P2-14-08",
        "scope": "REGISTERED_512_DIMENSIONAL_VALIDATION_HAMILTONIAN_SCALED_MOMENTS",
        "matrix_path": matrix_path.relative_to(PROJECT_ROOT).as_posix(),
        "spectrum_path": spectrum_path.relative_to(PROJECT_ROOT).as_posix(),
        "scaling": {
            "lower_over_t": scaling.lower,
            "upper_over_t": scaling.upper,
            "center_over_t": scaling.center,
            "radius_over_t": scaling.radius,
        },
        "namespace": "numpy.general",
        "stream_index": 100,
        "seed_config_sha256": config_sha256(),
    })
    with (output_dir / "moments.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result["records"][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(result["records"])
    (output_dir / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if result["status"] != "PASS":
        raise RuntimeError("registered moment/trace audit failed")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_08_registered_moment_trace",
    )
    parser.add_argument(
        "--matrix-path", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_hamiltonian_reconstruction" / "bilayer_h1_coo.csv",
    )
    parser.add_argument(
        "--spectrum-path", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_spectral_reconstruction" / "finite_spectrum.csv",
    )
    parser.add_argument("--dimension", type=int, default=512)
    args = parser.parse_args()
    print(json.dumps(run(
        args.output_dir,
        matrix_path=args.matrix_path,
        spectrum_path=args.spectrum_path,
        dimension=args.dimension,
    ), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
