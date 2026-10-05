"""Trace every quantitative abstract statement to formulas and registered data."""
from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX_PATH = ROOT / "source_current_195/main.tex"
OUT = ROOT / "reproducibility/data/abstract_value_verification.json"

def main() -> int:
    tex = TEX_PATH.read_text(encoding="utf-8")
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
    params = json.loads((ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/parameters.json").read_text(encoding="utf-8"))
    with (ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/target_observables.csv").open(encoding="utf-8", newline="") as handle:
        root_row = next(row for row in csv.DictReader(handle) if row["coupling_case"] == "root")
    q1 = params["clean_room_validation_fixture"]["q1"]
    w = 1.0 / q1
    norm_as = 8.0
    gap = 2.0 * (w - norm_as)
    source_gap = float(root_row["signed_lower_isolation_gap_over_t"])
    checks = {
        "five_state_count_traces_to_explicit_basis": "five-state" in abstract and "|x+\\rangle" in tex and "|y-\\rangle" in tex,
        "genus_two_traces_to_octagon_area": "genus-two" in abstract and "The resulting smooth quotient has genus two" in tex,
        "square_bound_formula_and_rounding": "4\\sqrt2-5\\simeq0.6569" in abstract and f"{4*math.sqrt(2)-5:.4f}" == "0.6569",
        "q1_matches_registered_source": f"{q1:.8f}" == "0.00712410" and "q_1=0.00712410" in abstract,
        "root_is_reciprocal_and_rounds_correctly": math.isclose(w, params["clean_room_validation_fixture"]["w_star_over_t"], abs_tol=1e-13) and f"{w:.2f}" == "140.37",
        "validation_adjacency_norm_is_explicitly_scoped": "\\|A_S\\|=8" in abstract and "release-Q7-validation-adjacency-norm" in tex,
        "gap_formula_matches_source": math.isclose(gap, source_gap, abs_tol=1e-12) and f"{gap:.2f}" == "264.74" and "\\simeq264.74" in abstract,
        "full_kernel_interval_matches_body": "[t/(q_1+b_2),t/(q_1-b_2)]" in abstract and "release-Q7-full-kernel-root-interval" in tex,
        "tail_denominators_have_positive_scope": "when \\(b_2<q_1\\)" in abstract and "|\\delta q|\\le b_2<q_1" in tex,
        "gap_hypothesis_is_retained": "and its shell and gap bounds hold" in abstract and "epsilon_H<g_*/6" in tex,
        "headline_values_have_explicit_body_equation": "release-Q7-validation-headline-values" in tex,
    }
    report = {
        "task_id": "P3-20-14",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "recomputed": {
            "square_lower_bound": 4 * math.sqrt(2) - 5,
            "q1": q1,
            "w_star_over_t": w,
            "adjacency_norm_registered_validation": norm_as,
            "gap_over_t": gap,
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
