"""Audit the claim ladder in the reader-facing physics narrative."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX_PATH = ROOT / "source_current_195/main.tex"
OUT = ROOT / "reproducibility/data/physics_content_edit_verification.json"

def main() -> int:
    tex = TEX_PATH.read_text(encoding="utf-8")
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
    checks = {
        "abstract_root_is_finite_first_shell": "registered finite first-shell surface-group control" in abstract,
        "abstract_signature_is_prediction_not_observation": "predicted finite-model signature" in abstract,
        "introduction_excludes_device_and_full_bulk_inference": "does not identify a calibrated device setting or a" in tex,
        "comparison_equation_has_real_quad_spacing": "no root}\\quad\\hbox{and}\\quad" in tex and "no root}quad" not in tex,
        "discussion_names_first_generator_shell": "declared symmetric first generator shell" in tex,
        "validation_coordinate_not_called_device_point": "The number $140.37$ is not a device operating point" in tex,
        "experimental_network_is_capability_not_completed_device": "network can implement the required one-particle" in tex,
        "conditional_error_bounds_not_claimed_as_evaluated": "available data\ndo not verify every such condition" in tex,
        "conclusion_calls_it_test_protocol": "direct resonator test protocol" in tex,
        "four_level_claim_ladder_present": "physics-claim-ladder" in tex and "two-sided cover and projector convergence" in tex,
        "no_observed_qubit_interaction_claim": "report no positive numerical claim of enhanced exchange" in tex,
    }
    report = {
        "task_id": "P3-20-16",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "claim_levels": ["analytic theorem", "finite-device prediction", "device observation", "bulk statement"],
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
