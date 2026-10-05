"""Emit exact commensurability controls and explicit finite-quotient requirements."""

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

from reproducibility.src.hyperbolic.finite_quotient import quotient_identity  # noqa: E402


def _csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cases = [
        {
            "case": "aligned_identity",
            "theta_radians": 0.0,
            "theta_over_pi": 0.0,
            "commensurator_membership": "KNOWN_TRUE",
            "normalizer_membership": "KNOWN_TRUE",
            "coincidence_index": 1,
            "common_genus": 2,
            "exact_cell_area_over_r2": 4.0 * math.pi,
            "bilayer_orbitals_per_exact_cell": 2,
            "source_basis": "identity normalizes Gamma_B",
        },
        {
            "case": "centered_c8_control",
            "theta_radians": math.pi / 4.0,
            "theta_over_pi": 0.25,
            "commensurator_membership": "KNOWN_TRUE",
            "normalizer_membership": "KNOWN_TRUE",
            "coincidence_index": 1,
            "common_genus": 2,
            "exact_cell_area_over_r2": 4.0 * math.pi,
            "bilayer_orbitals_per_exact_cell": 2,
            "source_basis": "centered C8 automorphism preserves the Bolza generator set",
        },
        {
            "case": "source_scan_endpoint_pi_over_8",
            "theta_radians": math.pi / 8.0,
            "theta_over_pi": 0.125,
            "commensurator_membership": "UNDETERMINED",
            "normalizer_membership": "UNDETERMINED",
            "coincidence_index": "MISSING",
            "common_genus": "MISSING",
            "exact_cell_area_over_r2": "MISSING",
            "bilayer_orbitals_per_exact_cell": "MISSING",
            "source_basis": "the scan endpoint is declared but no commensurator certificate or index is supplied",
        },
    ]
    _csv(
        output_dir / "commensurability_cases.csv", cases,
        [
            "case", "theta_radians", "theta_over_pi", "commensurator_membership",
            "normalizer_membership", "coincidence_index", "common_genus",
            "exact_cell_area_over_r2", "bilayer_orbitals_per_exact_cell", "source_basis",
        ],
    )

    requirements = [
        {"parameter_id": "COV-M01", "field": "quotient_tower", "state": "MISSING", "needed_for": "finite quotient presentation, multiplication, cosets, cover maps"},
        {"parameter_id": "COV-M02", "field": "cover_degree", "state": "MISSING", "needed_for": "finite quotient size and device dimension"},
        {"parameter_id": "COV-M03", "field": "injectivity_radius", "state": "MISSING", "needed_for": "geometric, based, and word injectivity certificates"},
        {"parameter_id": "COV-M04", "field": "distance_cutoff", "state": "MISSING", "needed_for": "unique-image/no-wraparound condition"},
        {"parameter_id": "R04-M01", "field": "commensurator_certificate_and_q_M", "state": "MISSING", "needed_for": "nontrivial exact centred-twist quotient"},
        {"parameter_id": "R04-M02", "field": "subgroup_word_or_matrix_generators", "state": "MISSING", "needed_for": "systole and injectivity-radius calculation"},
        {"parameter_id": "R04-M03", "field": "embedded_quotient_site_coordinates", "state": "MISSING", "needed_for": "finite-quotient distance table"},
    ]
    _csv(output_dir / "finite_quotient_requirements.csv", requirements, ["parameter_id", "field", "state", "needed_for"])

    identity = quotient_identity(coincidence_index=1, cover_degree=1)
    checks = {
        "aligned_index_identity": identity["common_genus"] == 2 and identity["exact_cell_orbitals"] == 2,
        "c8_index_identity": cases[1]["coincidence_index"] == 1 and cases[1]["common_genus"] == 2,
        "missing_quotient_inputs_are_explicit": all(row["state"] == "MISSING" for row in requirements),
        "no_nontrivial_index_inferred": all(case["coincidence_index"] in {1, "MISSING"} for case in cases),
    }
    summary = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "finite_quotient_status": "MISSING_INPUTS",
        "injectivity_radius_status": "MISSING_INPUTS",
        "exact_definitions": {
            "common_group": "Gamma_M(theta) = Gamma intersect g_theta Gamma g_theta^{-1}",
            "coincidence_index": "q_M = [Gamma:Gamma_M]",
            "common_genus_bolza": "g_M = 1 + q_M",
            "finite_cover": "Q_N = Gamma_M/Gamma_N",
            "geometric_injectivity_radius": "r_inj_geo = 0.5 inf_{gamma in Gamma_N\\{e}} ell(gamma)",
            "based_injectivity_radius": "r_inj(o) = 0.5 min_{gamma in Gamma_N\\{e}} d_H(o,gamma o)",
            "word_injectivity_radius": "r_inj_word = 0.5 min_{gamma in Gamma_N\\{e}} |gamma|_S",
        },
    }
    (output_dir / "quotient_geometry_checks.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if summary["status"] != "PASS":
        raise RuntimeError("Hyperbolic quotient-input validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
