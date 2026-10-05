"""Run P2-14-07 projector rank/overlap audit fixtures."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from spectrum.projector_audit import ProjectorTolerances, audit_projector_pair, projector_from_basis


def standard_basis(dimension: int, rank: int) -> np.ndarray:
    return np.eye(dimension, dtype=complex)[:, :rank]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "spectrum" / "p2_14_07_cases.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_07_projector_audit",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    limits = ProjectorTolerances(**config["projector_tolerances"])
    dimension = int(config["dimension"])
    rank = int(config["rank"])
    angle = float(config["controlled_rotation_angle_rad"])
    base = standard_basis(dimension, rank)
    reference = projector_from_basis(base)

    phase = np.exp(0.37j)
    internal = np.eye(rank, dtype=complex)
    internal[0, 0] = phase
    same_subspace = projector_from_basis(base @ internal)
    invariant = audit_projector_pair(reference, same_subspace, limits)

    rotated_basis = base.copy()
    rotated_basis[:, -1] = 0.0
    rotated_basis[rank - 1, -1] = np.cos(angle)
    rotated_basis[rank, -1] = np.sin(angle) * np.exp(0.23j)
    controlled = audit_projector_pair(reference, projector_from_basis(rotated_basis), limits)
    expected = {
        "maximum_principal_angle_rad": angle,
        "projector_operator_distance": float(np.sin(angle)),
        "chordal_distance": float(np.sin(angle)),
        "trace_overlap": float(rank - 1 + np.cos(angle) ** 2),
    }
    controlled_errors = {
        name: abs(float(controlled["metrics"][name]) - value) for name, value in expected.items()
    }

    rank_drop = audit_projector_pair(reference, projector_from_basis(base[:, :-1]), limits)
    perturbation = np.zeros_like(reference)
    perturbation[0, rank] = float(config["nonprojector_perturbation"])
    perturbation[rank, 0] = float(config["nonprojector_perturbation"])
    nonprojector = audit_projector_pair(reference, reference + perturbation, limits)

    metric_tolerance = float(config["metric_tolerance"])
    checks = {
        "basis_rotation_invariant": invariant["status"] == "PASS"
        and invariant["metrics"]["projector_operator_distance"] <= metric_tolerance,
        "controlled_rotation_pair_valid": controlled["status"] == "PASS",
        "controlled_rotation_metrics": max(controlled_errors.values()) <= metric_tolerance,
        "rank_drop_detected": rank_drop["status"] == "FAIL" and "rank_match" in rank_drop["failed_checks"],
        "nonprojector_detected": nonprojector["status"] == "FAIL"
        and "candidate_projector" in nonprojector["failed_checks"],
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    summary = {
        "task_id": "P2-14-07",
        "status": "PASS" if not failed else "FAIL",
        "scientific_scope": "Analytic projector-audit fixtures only; manuscript projectors are not yet reconstructed.",
        "dimension": dimension,
        "rank": rank,
        "controlled_rotation_angle_rad": angle,
        "checks": checks,
        "failed_checks": failed,
        "controlled_expected_metrics": expected,
        "controlled_metric_errors": controlled_errors,
        "cases": {
            "basis_rotation_invariance": invariant,
            "controlled_subspace_rotation": controlled,
            "rank_drop_negative_control": rank_drop,
            "nonprojector_negative_control": nonprojector,
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (args.output_dir / "cases.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "case_id", "pair_status", "rank_reference", "rank_candidate", "trace_overlap",
            "chordal_distance", "projector_operator_distance", "maximum_principal_angle_rad",
        ])
        for case_id, result in summary["cases"].items():
            writer.writerow([
                case_id, result["status"], result["rank_reference"], result["rank_candidate"],
                result["metrics"]["trace_overlap"], result["metrics"]["chordal_distance"],
                result["metrics"]["projector_operator_distance"], result["metrics"]["maximum_principal_angle_rad"],
            ])
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
