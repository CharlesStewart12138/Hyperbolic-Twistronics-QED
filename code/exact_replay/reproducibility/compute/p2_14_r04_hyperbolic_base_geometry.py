"""Generate exact normalized Bolza geometry and a short group-orbit sample."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.hyperbolic.bolza import (  # noqa: E402
    A_B_OVER_R, ETA, R_CIRC_OVER_R, R_IN_OVER_R, VERTEX_DISK_RADIUS,
    base_geometry_checks, bolza_vertices, enumerate_orbit, mobius_apply,
    neighbor_matrix, poincare_distance,
)


def _csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path, *, diagnostic_orbit_depth: int) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    base_rows = [
        {"quantity": "curvature", "symbol": "K", "value": -1.0, "units": "R^-2", "source_state": "EXACT"},
        {"quantity": "primitive_genus", "symbol": "g", "value": 2, "units": "dimensionless", "source_state": "EXACT"},
        {"quantity": "octagon_side_count", "symbol": "n_oct", "value": 8, "units": "dimensionless", "source_state": "EXACT"},
        {"quantity": "interior_angle", "symbol": "alpha_8", "value": math.pi / 4.0, "units": "radian", "source_state": "EXACT"},
        {"quantity": "primitive_area", "symbol": "A_0", "value": 4.0 * math.pi, "units": "R^2", "source_state": "EXACT"},
        {"quantity": "inradius", "symbol": "r_in", "value": R_IN_OVER_R, "units": "R", "source_state": "EXACT"},
        {"quantity": "microscopic_spacing", "symbol": "a_B", "value": A_B_OVER_R, "units": "R", "source_state": "EXACT"},
        {"quantity": "circumradius", "symbol": "r_circ", "value": R_CIRC_OVER_R, "units": "R", "source_state": "EXACT"},
        {"quantity": "vertex_disk_radius", "symbol": "rho_v", "value": VERTEX_DISK_RADIUS, "units": "disk_radius", "source_state": "EXACT"},
        {"quantity": "translation_parameter", "symbol": "eta", "value": ETA, "units": "dimensionless", "source_state": "EXACT"},
        {"quantity": "nearest_neighbor_coordination", "symbol": "z", "value": 8, "units": "dimensionless", "source_state": "EXACT"},
    ]
    _csv(output_dir / "bolza_base_geometry.csv", base_rows, ["quantity", "symbol", "value", "units", "source_state"])

    vertices = [
        {
            "vertex_index": index,
            "disk_x": vertex.real,
            "disk_y": vertex.imag,
            "disk_radius": abs(vertex),
            "polar_angle_radians": (2 * index + 1) * math.pi / 8.0,
        }
        for index, vertex in enumerate(bolza_vertices())
    ]
    _csv(output_dir / "bolza_vertices.csv", vertices, ["vertex_index", "disk_x", "disk_y", "disk_radius", "polar_angle_radians"])

    generator_rows: list[dict[str, object]] = []
    for direction in range(8):
        matrix = neighbor_matrix(direction)
        point = mobius_apply(matrix, 0.0j)
        generator_rows.append({
            "generator": f"s{direction}",
            "inverse_generator": f"s{(direction + 4) % 8}",
            "direction_radians": direction * math.pi / 4.0,
            "alpha_real": matrix[0, 0].real,
            "alpha_imag": matrix[0, 0].imag,
            "beta_real": matrix[0, 1].real,
            "beta_imag": matrix[0, 1].imag,
            "origin_image_x": point.real,
            "origin_image_y": point.imag,
            "origin_image_distance_over_r": poincare_distance(0.0j, point),
        })
    _csv(
        output_dir / "group_generators.csv", generator_rows,
        [
            "generator", "inverse_generator", "direction_radians", "alpha_real", "alpha_imag",
            "beta_real", "beta_imag", "origin_image_x", "origin_image_y", "origin_image_distance_over_r",
        ],
    )

    orbit_rows, orbit_checks = enumerate_orbit(diagnostic_orbit_depth)
    _csv(
        output_dir / "group_orbit_sample.csv", orbit_rows,
        [
            "orbit_index", "word", "word_depth", "parent_index", "last_generator",
            "disk_x", "disk_y", "geodesic_radius_over_r",
        ],
    )
    base_checks = base_geometry_checks()
    summary = {
        "status": "PASS" if base_checks["status"] == orbit_checks["status"] == "PASS" else "FAIL",
        "base_geometry": base_checks,
        "orbit_sample": orbit_checks,
        "orbit_scope": "SHORT_WORD_DIAGNOSTIC_SAMPLE_NOT_A_FINITE_QUOTIENT",
    }
    (output_dir / "base_geometry_checks.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if summary["status"] != "PASS":
        raise RuntimeError("Bolza base-geometry validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--diagnostic-orbit-depth", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, diagnostic_orbit_depth=args.diagnostic_orbit_depth), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
