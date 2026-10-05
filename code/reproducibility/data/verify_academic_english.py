"""Mechanical and voice audit for academic English in the TeX source."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX_PATH = ROOT / "source_current_195/main.tex"
OUT = ROOT / "reproducibility/data/academic_english_verification.json"

def absent(tex: str, pattern: str, flags: int = 0) -> bool:
    return re.search(pattern, tex, flags) is None

def main() -> int:
    tex = TEX_PATH.read_text(encoding="utf-8")
    checks = {
        "no_known_sentence_joins": absent(tex, r"(?:reconstruction|state|identical|lattice|measure|twice|retuning|frequency|dimensional|models|threshold)\.(?:To|Write|The|For|Assume|In)"),
        "no_known_semicolon_join": "non-negligible;the measured" not in tex,
        "no_naked_qquad_after_comma": ",qquad" not in tex,
        "no_double_comma_tokens": ",," not in tex,
        "no_split_production_parameter": absent(tex, r"production-\s+parameter"),
        "data_subject_agreement": "The available data does not" not in tex and "The available data set does not" in tex,
        "no_this_manuscript_self_reference": absent(tex, r"this manuscript", re.I),
        "no_this_article_self_reference": absent(tex, r"this Article", re.I),
        "no_present_work_self_reference": absent(tex, r"the present work", re.I),
        "no_in_this_paper_self_reference": absent(tex, r"(?:in|declared in) this paper", re.I),
        "companion_interface_uses_first_person": "We use the companion file" in tex and "We treat a companion citation as traceable" in tex,
        "negative_claims_use_first_person": "hence we report no" in tex and "Hence we do not assign" in tex,
        "provenance_uses_active_first_person": "For the figures we actually load" in tex and "figures we load from their registered" in tex,
        "comparison_spacing_token_is_valid": "no root}\\quad\\hbox{and}\\quad" in tex,
    }
    report = {
        "task_id": "P3-20-17",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "scope": "full TeX source mechanical joins, LaTeX spacing tokens, subject agreement, and first-author self-reference",
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
