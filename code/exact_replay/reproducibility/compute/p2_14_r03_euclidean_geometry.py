"""Rebuild exact Euclidean square-CSL geometry datasets for P2-14-R03."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.euclidean.commensurate import (  # noqa: E402
    all_cell_records,
    lattice_representatives,
    wrap_rotated_representatives,
)


def _write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(output_dir: Path) -> dict[str, object]:
    cells = all_cell_records()
    cell_rows: list[dict[str, object]] = []
    basis_rows: list[dict[str, object]] = []
    site_rows: list[dict[str, object]] = []
    check_rows: list[dict[str, object]] = []

    for cell in cells:
        sigma = int(cell["sigma"])
        p = int(cell["p"])
        q = int(cell["q"])
        direct = cell["direct_basis_a"]
        reciprocal = cell["reciprocal_basis_a_over_2pi"]
        cell_rows.append({
            "site_count": cell["site_count"],
            "sigma": sigma,
            "m": cell["m"],
            "n": cell["n"],
            "parity_divisor": cell["parity_divisor"],
            "p": p,
            "q": q,
            "cos_theta": cell["cos_theta"],
            "sin_theta": cell["sin_theta"],
            "angle_radians": cell["angle_radians"],
            "angle_degrees": cell["angle_degrees"],
            "angle_degrees_source": cell["angle_degrees_source"],
            "supercell_length_over_a": cell["supercell_length_over_a"],
            "supercell_area_over_a2": cell["supercell_area_over_a2"],
            "mbz_area_over_primitive_bz": cell["mbz_area_over_primitive_bz"],
        })
        for vector_index in range(2):
            basis_rows.extend((
                {
                    "site_count": cell["site_count"],
                    "sigma": sigma,
                    "space": "direct",
                    "vector": f"T{vector_index + 1}",
                    "x_component": int(direct[0, vector_index]),
                    "y_component": int(direct[1, vector_index]),
                    "units": "a",
                },
                {
                    "site_count": cell["site_count"],
                    "sigma": sigma,
                    "space": "reciprocal",
                    "vector": f"G{vector_index + 1}",
                    "x_component": float(reciprocal[0, vector_index]),
                    "y_component": float(reciprocal[1, vector_index]),
                    "units": "2pi_over_a",
                },
            ))

        layer_one = lattice_representatives(p, q, sigma)
        layer_two = wrap_rotated_representatives(
            layer_one,
            direct_basis=direct,
            angle_radians=float(cell["angle_radians"]),
        )
        for layer, representatives in ((1, layer_one), (2, layer_two)):
            for site_index, representative in enumerate(representatives):
                if "fractional_u" in representative:
                    fractional_u = representative["fractional_u"]
                    fractional_v = representative["fractional_v"]
                else:
                    fractional_u = float(representative["fractional_u_numerator"]) / sigma
                    fractional_v = float(representative["fractional_v_numerator"]) / sigma
                site_rows.append({
                    "site_count": cell["site_count"],
                    "sigma": sigma,
                    "layer": layer,
                    "site_index": site_index,
                    "fractional_u": fractional_u,
                    "fractional_v": fractional_v,
                    "x_over_a": representative["x_over_a"],
                    "y_over_a": representative["y_over_a"],
                })
        checks = dict(cell["checks"])
        checks.update({
            "layer_one_site_count": len(layer_one) == sigma,
            "layer_two_site_count": len(layer_two) == sigma,
        })
        check_rows.append({
            "site_count": cell["site_count"],
            "sigma": sigma,
            "status": "PASS" if all(checks.values()) else "FAIL",
            "checks": checks,
            "failed_checks": sorted(name for name, passed in checks.items() if not passed),
        })

    _write_csv(
        output_dir / "commensurate_cells.csv", cell_rows,
        [
            "site_count", "sigma", "m", "n", "parity_divisor", "p", "q",
            "cos_theta", "sin_theta", "angle_radians", "angle_degrees",
            "angle_degrees_source", "supercell_length_over_a",
            "supercell_area_over_a2", "mbz_area_over_primitive_bz",
        ],
    )
    _write_csv(
        output_dir / "lattice_bases.csv", basis_rows,
        ["site_count", "sigma", "space", "vector", "x_component", "y_component", "units"],
    )
    _write_csv(
        output_dir / "real_space_sites.csv", site_rows,
        ["site_count", "sigma", "layer", "site_index", "fractional_u", "fractional_v", "x_over_a", "y_over_a"],
    )
    summary = {
        "status": "PASS" if all(row["status"] == "PASS" for row in check_rows) else "FAIL",
        "cell_count": len(cells),
        "declared_site_counts": [int(cell["site_count"]) for cell in cells],
        "real_space_row_count": len(site_rows),
        "cell_checks": check_rows,
    }
    _write_json(output_dir / "geometry_checks.json", summary)
    if summary["status"] != "PASS":
        raise RuntimeError("Euclidean CSL geometry validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
