"""Run certified dense/sparse solvers and target-projector audit on the R05 matrix."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.spectrum.finite_registered import load_coo_csv, solve_registered_root  # noqa: E402


def run(output_dir: Path, *, matrix_path: Path, dimension: int, w_star_over_t: float) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = load_coo_csv(matrix_path, dimension=dimension)
    rows, checks = solve_registered_root(matrix, w_star_over_t=w_star_over_t)
    with (output_dir / "finite_spectrum.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["eigenvalue_index", "energy_over_t", "target_island", "solver"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "finite_solver_checks.json").write_text(
        json.dumps(checks, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if checks["status"] != "PASS":
        raise RuntimeError("finite registered spectral solver validation failed")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--matrix-path", type=Path, required=True)
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--w-star-over-t", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, matrix_path=args.matrix_path, dimension=args.dimension, w_star_over_t=args.w_star_over_t), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
