"""Enumerate and audit every representation sector of the R04 validation quotient."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.representations.z4_fourier import (  # noqa: E402
    audit_decomposition,
    character_sector_rows,
)
from reproducibility.src.spectrum.finite_registered import load_coo_csv  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(
    output_dir: Path,
    *,
    matrix_path: Path,
    dimension: int,
    q1: float,
    w_star_over_t: float,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = load_coo_csv(matrix_path, dimension=dimension)
    irrep_rows, sector_rows = character_sector_rows(q1=q1, w_star_over_t=w_star_over_t)
    comparison_rows, audit = audit_decomposition(
        matrix,
        q1=q1,
        w_star_over_t=w_star_over_t,
    )
    irrep_fields = list(irrep_rows[0])
    spectrum_fields = list(sector_rows[0])
    comparison_fields = list(comparison_rows[0])
    write_csv(output_dir / "irreducible_representations.csv", irrep_rows, irrep_fields)
    write_csv(output_dir / "sector_spectra.csv", sector_rows, spectrum_fields)
    write_csv(output_dir / "abelian_spectrum.csv", sector_rows, spectrum_fields)
    full_rows = [
        {
            "sorted_state_index": row["sorted_state_index"],
            "energy_over_t": row["full_energy_over_t"],
            "spectrum_scope": "FULL_REGISTERED_FINITE_QUOTIENT",
        }
        for row in comparison_rows
    ]
    write_csv(output_dir / "full_spectrum.csv", full_rows, list(full_rows[0]))
    write_csv(output_dir / "abelian_full_spectrum_comparison.csv", comparison_rows, comparison_fields)
    write_csv(
        output_dir / "higher_dimensional_sectors.csv",
        [],
        ["sector_id", "irrep_dimension", "regular_multiplicity", "state_count", "absence_reason"],
    )
    (output_dir / "peter_weyl_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if audit["status"] != "PASS":
        raise RuntimeError("representation-completion audit failed")
    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--matrix-path", type=Path, required=True)
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--q1", type=float, required=True)
    parser.add_argument("--w-star-over-t", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(run(
        args.output_dir,
        matrix_path=args.matrix_path,
        dimension=args.dimension,
        q1=args.q1,
        w_star_over_t=args.w_star_over_t,
    ), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
