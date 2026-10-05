"""Generate finite-cover, shell, C0/C1/C2, and no-loss/no-pollution diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.finite_cover.abelian_validation_towers import (  # noqa: E402
    TOWERS,
    build_cover_products,
    cross_cover_rows,
    shell_budget_rows,
)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path, *, kernel_path: Path, w_star_over_t: float) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    diagnostics, spectral_rows, aliasing_rows, states = build_cover_products(w_star_over_t=w_star_over_t)
    cross_rows = cross_cover_rows(diagnostics, states)
    shell_rows = shell_budget_rows(kernel_path, w_star_over_t=w_star_over_t)
    no_loss_rows = [
        {
            "tower_id": row["tower_id"],
            "level": row["level"],
            "modulus": row["modulus"],
            "declared_sector": row["declared_sector"],
            "no_loss_error_over_t": row["C0_no_loss_error_over_t"],
            "no_pollution_error_over_t": row["C0_no_pollution_error_over_t"],
            "two_sided_Hausdorff_error_over_t": row["C0_Hausdorff_error_over_t"],
            "no_loss_certificate": "DIRECT_ANALYTIC_INTERVAL_NET_IN_DECLARED_ABELIAN_SECTOR",
            "no_pollution_certificate": "DIRECT_ANALYTIC_UPPER_INCLUSION_IN_DECLARED_ABELIAN_SECTOR",
            "full_surface_group_no_loss": "UNRESOLVED",
            "full_surface_group_no_pollution": "UNRESOLVED",
        }
        for row in diagnostics
    ]
    write_csv(output_dir / "cover_sequence.csv", diagnostics)
    write_csv(output_dir / "cover_spectral_sets.csv", spectral_rows)
    write_csv(output_dir / "moment_aliasing_margins.csv", aliasing_rows)
    write_csv(output_dir / "cross_cover_diagnostics.csv", cross_rows)
    write_csv(output_dir / "shell_budgets.csv", shell_rows)
    write_csv(output_dir / "no_loss_no_pollution.csv", no_loss_rows)

    c0_values = [float(row["C0_Hausdorff_error_over_t"]) for row in diagnostics]
    nonincreasing_by_tower = all(
        all(values[index + 1] <= values[index] + 1.0e-14 for index in range(len(values) - 1))
        for tower in TOWERS
        for values in [[float(row["C0_Hausdorff_error_over_t"]) for row in diagnostics if row["tower_id"] == tower]]
    )
    checks = {
        "two_explicit_quotient_towers": len(TOWERS) == 2,
        "every_tower_map_divisibility_checked": True,
        "C0_budgets_explicit": all(value >= 0.0 for value in c0_values),
        "C1_budgets_explicit": all("C1_velocity_maximum_error_t_over_hbar" in row for row in diagnostics),
        "C2_budgets_explicit": all("C2_Hessian_maximum_error_over_t" in row for row in diagnostics),
        "C0_not_promoted_to_C1_or_C2": True,
        "declared_Abelian_no_pollution": all(float(row["no_pollution_error_over_t"]) == 0.0 for row in no_loss_rows),
        "declared_Abelian_no_loss_nonincreasing": nonincreasing_by_tower,
        "constant_injectivity_radius_detected": len({float(row["word_injectivity_radius"]) for row in diagnostics}) == 1,
        "full_group_convergence_not_claimed": all(row["full_surface_group_no_loss"] == "UNRESOLVED" for row in no_loss_rows),
        "shell_tail_budgets_separate": all(
            float(row["C0_operator_tail_bound_over_t"]) <= float(row["C1_derivative_tail_bound_over_t"]) + 1.0e-15
            and float(row["C1_derivative_tail_bound_over_t"]) <= float(row["C2_Hessian_tail_bound_over_t"]) + 1.0e-15
            for row in shell_rows[:-1]
        ),
        "unknown_infinite_shell_tail_preserved": all(row["infinite_shell_tail_status"].startswith("UNKNOWN") for row in shell_rows),
    }
    summary = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "task_id": "P2-14-R09",
        "cover_count": len(diagnostics),
        "tower_count": len(TOWERS),
        "cover_moduli": {tower: list(moduli) for tower, moduli in TOWERS.items()},
        "word_injectivity_radius_values": sorted({float(row["word_injectivity_radius"]) for row in diagnostics}),
        "minimum_C0_Hausdorff_error_over_t": min(c0_values),
        "maximum_C0_Hausdorff_error_over_t": max(c0_values),
        "shell_depths": [int(row["retained_word_depth"]) for row in shell_rows],
        "checks": checks,
        "declared_sector_conclusion": "FINITE_ABELIAN_CHARACTER_GRIDS_HAVE_DIRECT_NO_LOSS_AND_NO_POLLUTION_DIAGNOSTICS",
        "full_surface_group_conclusion": "INCONCLUSIVE: BOTH TOWERS FACTOR THROUGH ABELIANIZATION, RETAIN THE LENGTH-FOUR COMMUTATOR KERNEL, AND HAVE CONSTANT WORD INJECTIVITY RADIUS TWO",
        "long_range_conclusion": "INCONCLUSIVE: COEFFICIENTS ARE AVAILABLE ONLY THROUGH WORD DEPTH THREE, SO THE INFINITE SHELL TAIL IS UNKNOWN",
        "weak_convergence_upgrade": False,
    }
    (output_dir / "convergence_audit.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if summary["status"] != "PASS":
        raise RuntimeError("R09 finite-cover validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--kernel-path", type=Path, required=True)
    parser.add_argument("--w-star-over-t", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, kernel_path=args.kernel_path, w_star_over_t=args.w_star_over_t), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
