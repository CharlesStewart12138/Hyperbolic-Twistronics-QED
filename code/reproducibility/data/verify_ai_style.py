"""Audit rendered prose and source comments for templated project language."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX_PATH = ROOT / "source_current_195/main.tex"
OUT = ROOT / "reproducibility/data/ai_style_verification.json"

def main() -> int:
    tex = TEX_PATH.read_text(encoding="utf-8")
    rendered = re.sub(r"(?m)%.*$", "", tex)
    checks = {
        "no_task_provenance_comments": re.search(r"(?m)%\s*(?:BEGIN|END|source tasks?)\s+P", tex, re.I) is None,
        "no_gate_or_firewall_metaphor": re.search(r"\b(?:gate|firewall)\b", rendered, re.I) is None,
        "no_blocker_noun": re.search(r"\bblocker\b", rendered, re.I) is None,
        "no_pipeline_metaphor": re.search(r"\bpipeline\b", rendered, re.I) is None,
        "no_terminal_task_status_prose": "terminal scientific scope" not in rendered and "task identifier" not in rendered,
        "no_authoritative_navigation_claim": "authoritative Topic" not in rendered and "authoritative closed-set" not in rendered,
        "no_product_management_labels": "PRL-candidate product" not in rendered and "course-facing PC5203 product" not in rendered,
        "no_release_check_or_audit_prose": "release check" not in rendered and "release audit" not in rendered,
        "no_task_specific_scripts_prose": "task-specific scripts" not in rendered,
        "no_presubmission_action_banner": "Pre-submission author action required" not in rendered,
        "competing_interest_block_remains_truthful": "pending the author's explicit" in rendered and "no declaration is inferred" in rendered,
        "first_author_voice_retained": "We provide the proof-bearing" in rendered and "we follow the eight-question" in rendered,
        "scientific_claims_retained": "c_\\square\\ge4\\sqrt2-5" in rendered and "w_*=t/q_1" in rendered,
        "reproducibility_equations_retained": "figure-raw-closure-error" in rendered and "release-reproduction-product" in rendered,
        "no_stock_ai_phrases": re.search(r"it is important to note|plays? a crucial role|delve|underscores?|testament to|seamlessly", rendered, re.I) is None,
    }
    report = {
        "task_id": "P3-20-18",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "scope": "reader-facing prose plus submission-source task provenance comments",
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
