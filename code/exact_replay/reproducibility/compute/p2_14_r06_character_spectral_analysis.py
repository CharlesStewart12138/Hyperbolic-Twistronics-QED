"""Compute declared character-sector bands, projectors, derivatives, and Hodge data."""

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

from reproducibility.src.spectrum.first_shell_character import (  # noqa: E402
    derivative_audit, exact_observables, numerical_corner_observables,
    solve_character, validation_couplings,
)
from reproducibility.src.spectrum.projector_audit import audit_projector_pair  # noqa: E402


def _csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path, *, q1: float, w_star_over_t: float) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    grid_rows: list[dict[str, object]] = []
    observable_rows: list[dict[str, object]] = []
    hodge_rows: list[dict[str, object]] = []
    projector_rows: list[dict[str, object]] = []
    maximum_corner_residual = 0.0
    maximum_projector_distance = 0.0
    reference_projector = None
    couplings = validation_couplings(w_star_over_t)
    for coupling in couplings:
        w_value = float(coupling["w_over_t"])
        rows, numerical = numerical_corner_observables(w_over_t=w_value, q1=q1)
        exact = exact_observables(w_over_t=w_value, q1=q1)
        for row in rows:
            grid_rows.append({**coupling, **row, "sector_scope": "DECLARED_CHARACTER_ONLY"})
        residual = max(abs(float(numerical[key]) - float(exact[key])) for key in numerical)
        maximum_corner_residual = max(maximum_corner_residual, residual)
        observable_rows.append({
            **coupling,
            **exact,
            "corner_extrema_residual": residual,
            "observable_scope": "EXACT_FIRST_SHELL_CHARACTER_TORUS",
        })
        hessian_value = 2.0 * (1.0 - w_value * q1)
        hodge_rows.append({
            **coupling,
            "stationary_point": "trivial_character",
            "metric": "G=I4 validation normalization",
            "lambda_1_over_t": hessian_value,
            "lambda_2_over_t": hessian_value,
            "lambda_3_over_t": hessian_value,
            "lambda_4_over_t": hessian_value,
            "trace_over_t": 4.0 * hessian_value,
            "traceless_frobenius_over_t": 0.0,
        })
        solved = solve_character(np.zeros(4), w_over_t=w_value, q1=q1)
        projector = np.asarray(solved["even_projector"])
        if reference_projector is None:
            reference_projector = projector
        audit = audit_projector_pair(reference_projector, projector)
        distance = float(audit["metrics"]["projector_operator_distance"])
        maximum_projector_distance = max(maximum_projector_distance, distance)
        projector_rows.append({
            **coupling,
            "rank_reference": audit["rank_reference"],
            "rank_candidate": audit["rank_candidate"],
            "trace_overlap": audit["metrics"]["trace_overlap"],
            "projector_operator_distance": distance,
            "maximum_principal_angle_rad": audit["metrics"]["maximum_principal_angle_rad"],
            "status": audit["status"],
        })

    derivative_rows, derivative_checks = derivative_audit(
        w_over_t=w_star_over_t * 0.875,
        q1=q1,
        steps=(2.0 ** -5, 2.0 ** -6, 2.0 ** -7, 2.0 ** -8, 2.0 ** -9, 2.0 ** -10),
    )
    for row in derivative_rows:
        row["coupling_case"] = "seven_eighths"
        row["step_scope"] = "CLEAN_ROOM_DYADIC_VALIDATION_NOT_PRODUCTION_NUM_M07"

    _csv(
        output_dir / "character_spectral_grid.csv", grid_rows,
        [
            "coupling_case", "w_over_w_star", "w_over_t", "point_index", "k1_over_pi", "k2_over_pi",
            "k3_over_pi", "k4_over_pi", "C_k", "even_energy_over_t", "odd_energy_over_t",
            "maximum_solver_residual", "sector_scope",
        ],
    )
    _csv(
        output_dir / "target_observables.csv", observable_rows,
        [
            "coupling_case", "w_over_w_star", "w_over_t", "even_lower_edge_over_t", "even_upper_edge_over_t",
            "even_bandwidth_over_t", "odd_lower_edge_over_t", "odd_upper_edge_over_t",
            "signed_lower_isolation_gap_over_t", "maximum_generalized_velocity_t_over_hbar",
            "maximum_absolute_hessian_over_t", "hodge_trace_at_trivial_character_over_t",
            "corner_extrema_residual", "observable_scope",
        ],
    )
    _csv(
        output_dir / "hodge_eigenvalues.csv", hodge_rows,
        [
            "coupling_case", "w_over_w_star", "w_over_t", "stationary_point", "metric",
            "lambda_1_over_t", "lambda_2_over_t", "lambda_3_over_t", "lambda_4_over_t",
            "trace_over_t", "traceless_frobenius_over_t",
        ],
    )
    _csv(
        output_dir / "projector_tracking.csv", projector_rows,
        [
            "coupling_case", "w_over_w_star", "w_over_t", "rank_reference", "rank_candidate",
            "trace_overlap", "projector_operator_distance", "maximum_principal_angle_rad", "status",
        ],
    )
    _csv(
        output_dir / "derivative_audit.csv", derivative_rows,
        [
            "coupling_case", "step", "velocity_fd_t_over_hbar", "velocity_exact_t_over_hbar",
            "velocity_abs_error", "hessian_lambda_1_over_t", "hessian_lambda_2_over_t",
            "hessian_lambda_3_over_t", "hessian_lambda_4_over_t", "hessian_exact_over_t",
            "hessian_max_abs_error", "step_scope",
        ],
    )
    checks = {
        "corner_extrema": maximum_corner_residual <= 2.0e-10,
        "projector_tracking": maximum_projector_distance <= 2.0e-12 and all(row["status"] == "PASS" for row in projector_rows),
        "derivative_audit": derivative_checks["status"] == "PASS",
        "root_bandwidth_zero": abs(float(observable_rows[2]["even_bandwidth_over_t"])) <= 2.0e-12,
        "root_hodge_eigenvalues_zero": max(abs(float(hodge_rows[2][f"lambda_{index}_over_t"])) for index in range(1, 5)) <= 2.0e-12,
        "root_gap_positive": float(observable_rows[2]["signed_lower_isolation_gap_over_t"]) > 0.0,
    }
    summary = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "sector_scope": "DECLARED_FIRST_SHELL_CHARACTER_NOT_REPRESENTATION_COMPLETE",
        "coupling_case_count": len(couplings),
        "spectral_grid_row_count": len(grid_rows),
        "maximum_corner_extrema_residual": maximum_corner_residual,
        "maximum_projector_distance": maximum_projector_distance,
        "derivative_checks": derivative_checks,
        "checks": checks,
    }
    (output_dir / "character_analysis_checks.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if summary["status"] != "PASS":
        raise RuntimeError("character spectral analysis validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--q1", type=float, required=True)
    parser.add_argument("--w-star-over-t", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, q1=args.q1, w_star_over_t=args.w_star_over_t), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
