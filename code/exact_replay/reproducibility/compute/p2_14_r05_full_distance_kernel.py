"""Generate physical exponential full-distance coefficients without a spectrum."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.hyperbolic.bolza import A_B_OVER_R  # noqa: E402
from reproducibility.src.hamiltonian.full_distance import full_distance_kernel_patch  # noqa: E402


def run(output_dir: Path, *, max_word_depth: int, h_over_a: float, lambda_over_a: float) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, checks = full_distance_kernel_patch(
        max_word_depth=max_word_depth,
        h_over_r=h_over_a * A_B_OVER_R,
        lambda_over_r=lambda_over_a * A_B_OVER_R,
    )
    with (output_dir / "universal_full_distance_kernel.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "orbit_index", "word", "inverse_word", "word_depth", "inplane_distance_over_r",
                "product_distance_over_r", "excess_distance_over_r", "q_gamma", "kernel_scope",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "full_distance_checks.json").write_text(
        json.dumps(checks, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if checks["status"] != "PASS":
        raise RuntimeError("full-distance exponential kernel validation failed")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-word-depth", type=int, default=3)
    parser.add_argument("--h-over-a", type=float, default=0.5)
    parser.add_argument("--lambda-over-a", type=float, default=0.125)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, max_word_depth=args.max_word_depth, h_over_a=args.h_over_a, lambda_over_a=args.lambda_over_a), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
