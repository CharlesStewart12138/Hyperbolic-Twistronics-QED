"""Audit released numerical precision and uncertainty classifications."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX_PATH = ROOT / "source_current_195/main.tex"
OUT = ROOT / "reproducibility/data/reported_uncertainty_verification.json"

def main() -> int:
    tex = TEX_PATH.read_text(encoding="utf-8")
    params = json.loads((ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/parameters.json").read_text(encoding="utf-8"))
    dos = json.loads((ROOT / "reproducibility/data/hyperbolic_dos_reconstruction/dos_audit.json").read_text(encoding="utf-8"))
    with (ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/target_observables.csv").open(encoding="utf-8", newline="") as handle:
        root_row = next(row for row in csv.DictReader(handle) if row["coupling_case"] == "root")

    q1 = params["clean_room_validation_fixture"]["q1"]
    w_star = params["clean_room_validation_fixture"]["w_star_over_t"]
    gap = float(root_row["signed_lower_isolation_gap_over_t"])
    eta = dos["broadening_schedule"][1]["eta_over_t"]
    residual = dos["metrics"]["resolved_sum_rule_linf"]
    checks = {
        "square_exact_decimal_rounds_to_0p6569": f"{4 * math.sqrt(2) - 5:.4f}" == "0.6569",
        "q1_rounds_to_eight_decimal_places": f"{q1:.8f}" == "0.00712410" and "q_1=0.00712410" in tex,
        "w_star_rounds_to_two_decimal_places": f"{w_star:.2f}" == "140.37" and "\\simeq140.37" in tex,
        "gap_rounds_to_two_decimal_places": f"{gap:.2f}" == "264.74" and "\\simeq264.74" in tex,
        "root_half_width_is_explicit": "2.5\\times10^{-10}" in tex and "1-2.5\\times10^{-10}" in tex,
        "eta_is_correctly_rounded_fixed_input": f"{eta:.12g}" == "1.48368612653" and "registered fixed broadening" in tex,
        "closure_residual_rounds_to_three_significant_digits": f"{residual:.3g}" == "5.55e-17" and "5.55\\times10^{-17}" in tex,
        "stale_residual_rounding_removed": "5.56\\times10^{-17}" not in tex,
        "floating_point_residual_not_called_experimental_uncertainty": "neither number is an experimental uncertainty" in tex,
        "missing_inputs_not_zero_uncertainty": "left missing rather than represented by a zero error bar" in tex,
    }
    report = {
        "task_id": "P3-20-13",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "source_values": {
            "q1": q1,
            "w_star_over_t": w_star,
            "gap_over_t": gap,
            "eta_over_t": eta,
            "resolved_sum_rule_linf": residual,
            "root_half_width_in_w_over_w_star": 2.5e-10,
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
