"""Assemble finite first-shell scalar surface-group Hamiltonian matrices."""

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
from reproducibility.src.hamiltonian.scalar_surface import (  # noqa: E402
    assemble_validation_hamiltonians, sparse_rows,
)


MATRIX_FILES = {
    "monolayer_h0": "monolayer_h0_coo.csv",
    "interlayer_wq1": "interlayer_q1_coo.csv",
    "bilayer_h1": "bilayer_h1_coo.csv",
}


def run(output_dir: Path, *, modulus: int, h_over_a: float, lambda_over_a: float) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrices, audits = assemble_validation_hamiltonians(
        modulus=modulus,
        a_over_r=A_B_OVER_R,
        h_over_a=h_over_a,
        lambda_over_a=lambda_over_a,
    )
    for matrix_name, filename in MATRIX_FILES.items():
        rows = sparse_rows(matrices[matrix_name], matrix_name=matrix_name)
        with (output_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["matrix", "row", "column", "value_over_t"], lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    (output_dir / "hamiltonian_audits.json").write_text(
        json.dumps(audits, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if audits["status"] != "PASS":
        raise RuntimeError("finite scalar Hamiltonian audits failed")
    return audits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--modulus", type=int, default=4)
    parser.add_argument("--h-over-a", type=float, default=0.5)
    parser.add_argument("--lambda-over-a", type=float, default=0.125)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, modulus=args.modulus, h_over_a=args.h_over_a, lambda_over_a=args.lambda_over_a), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
