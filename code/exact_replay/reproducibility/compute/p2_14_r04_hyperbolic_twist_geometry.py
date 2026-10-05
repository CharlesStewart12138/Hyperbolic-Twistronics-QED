"""Generate exact local twist-displacement and effective-moire geometry controls."""

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

from reproducibility.src.hyperbolic.bolza import A_B_OVER_R, R_CIRC_OVER_R, R_IN_OVER_R  # noqa: E402
from reproducibility.src.hyperbolic.local_twist import (  # noqa: E402
    displacement_disk_crosscheck, moire_geometry, twist_displacement_over_r,
)


def _csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    angle_cases = [
        ("aligned", 0.0, "SOURCE_ENDPOINT"),
        ("pi_over_256", math.pi / 256.0, "CLEAN_ROOM_DYADIC_DIAGNOSTIC"),
        ("pi_over_128", math.pi / 128.0, "CLEAN_ROOM_DYADIC_DIAGNOSTIC"),
        ("pi_over_64", math.pi / 64.0, "CLEAN_ROOM_DYADIC_DIAGNOSTIC"),
        ("pi_over_32", math.pi / 32.0, "CLEAN_ROOM_DYADIC_DIAGNOSTIC"),
        ("pi_over_16", math.pi / 16.0, "CLEAN_ROOM_DYADIC_DIAGNOSTIC"),
        ("pi_over_8", math.pi / 8.0, "SOURCE_ENDPOINT"),
    ]
    radius_cases = [
        ("origin", 0.0),
        ("octagon_inradius", R_IN_OVER_R),
        ("microscopic_spacing", A_B_OVER_R),
        ("octagon_circumradius", R_CIRC_OVER_R),
    ]
    displacement_rows: list[dict[str, object]] = []
    maximum_crosscheck_residual = 0.0
    for angle_label, theta, angle_role in angle_cases:
        for radius_label, radius in radius_cases:
            residual = displacement_disk_crosscheck(radius, theta)
            maximum_crosscheck_residual = max(maximum_crosscheck_residual, residual)
            displacement_rows.append({
                "angle_case": angle_label,
                "angle_role": angle_role,
                "theta_radians": theta,
                "theta_over_pi": theta / math.pi,
                "radius_case": radius_label,
                "geodesic_radius_over_r": radius,
                "twist_displacement_over_r": twist_displacement_over_r(radius, theta),
                "disk_formula_residual_over_r": residual,
            })
    _csv(
        output_dir / "twist_displacement.csv", displacement_rows,
        [
            "angle_case", "angle_role", "theta_radians", "theta_over_pi", "radius_case",
            "geodesic_radius_over_r", "twist_displacement_over_r", "disk_formula_residual_over_r",
        ],
    )

    moire_rows = []
    maximum_threshold_residual = 0.0
    finite_radii = []
    for angle_label, theta, angle_role in angle_cases:
        geometry = moire_geometry(a_over_r=A_B_OVER_R, theta=theta, orbitals_per_layer=1)
        residual = float(geometry["registry_threshold_residual_over_r"])
        maximum_threshold_residual = max(maximum_threshold_residual, residual)
        if math.isfinite(float(geometry["moire_radius_over_r"])):
            finite_radii.append(float(geometry["moire_radius_over_r"]))
        moire_rows.append({
            "angle_case": angle_label,
            "angle_role": angle_role,
            "theta_over_pi": theta / math.pi,
            **geometry,
        })
    _csv(
        output_dir / "local_moire_geometry.csv", moire_rows,
        [
            "angle_case", "angle_role", "theta_radians", "theta_over_pi", "half_angle_sine",
            "chi", "moire_radius_over_r", "effective_area_over_r2", "effective_bilayer_count",
            "registry_threshold_residual_over_r", "status",
        ],
    )
    checks = {
        "disk_distance_crosscheck": maximum_crosscheck_residual <= 2.0e-12,
        "registry_threshold_equation": maximum_threshold_residual <= 2.0e-12,
        "moire_radius_decreases_with_twist": all(first > second for first, second in zip(finite_radii, finite_radii[1:])),
        "source_scan_bounds_respected": all(0.0 <= theta <= math.pi / 8.0 for _, theta, _ in angle_cases),
    }
    summary = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "angle_case_count": len(angle_cases),
        "displacement_row_count": len(displacement_rows),
        "moire_row_count": len(moire_rows),
        "maximum_disk_formula_residual_over_r": maximum_crosscheck_residual,
        "maximum_registry_threshold_residual_over_r": maximum_threshold_residual,
        "checks": checks,
        "mesh_scope": "SOURCE_ENDPOINTS_PLUS_CLEAN_ROOM_DYADIC_DIAGNOSTICS_NOT_A_PRODUCTION_SCAN",
    }
    (output_dir / "twist_geometry_checks.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if summary["status"] != "PASS":
        raise RuntimeError("Hyperbolic local-twist validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
