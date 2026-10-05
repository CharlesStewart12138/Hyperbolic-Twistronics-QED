"""Verify final internal closure while preserving explicit external blockers."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reexecution_203/FINAL_INTERNAL_CLOSURE.json"

PASS_REPORTS = [
    "reproducibility/release_reproduction_report.json",
    "reproducibility/data/raw_data_policy_verification.json",
    "reproducibility/data/caption_status_verification.json",
    "reproducibility/data/reported_uncertainty_verification.json",
    "reproducibility/data/abstract_value_verification.json",
    "reproducibility/data/physics_content_edit_verification.json",
    "reproducibility/data/academic_english_verification.json",
    "reproducibility/data/ai_style_verification.json",
    "reproducibility/random/seed_verification.json",
]

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-active-final", action="store_true")
    args = parser.parse_args()

    state = json.loads((ROOT / "tmp/reexecution_203/state.json").read_text(encoding="utf-8"))
    statuses = Counter(item["reexecutionStatus"] for item in state)
    active = [item["id"] for item in state if item["reexecutionStatus"] == "IN_REEXECUTION"]
    terminal_ok = active == ["P3-20-21"] if args.allow_active_final else not active
    allowed = {"DONE", "BLOCKED", "DEFERRED"}
    if args.allow_active_final:
        allowed.add("IN_REEXECUTION")

    report_statuses = {}
    for relative in PASS_REPORTS:
        path = ROOT / relative
        payload = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        report_statuses[relative] = payload.get("status", "MISSING")

    archive_validation_path = ROOT / "products/release_archives/hyperbolic_moire_source_2026-09-03_validation.json"
    archive_validation = json.loads(archive_validation_path.read_text(encoding="utf-8"))
    archive_path = ROOT / "products/release_archives" / archive_validation["package"]
    archive_hash_ok = archive_path.is_file() and sha256(archive_path) == archive_validation["archive_sha256"]

    tex_path = ROOT / "source_current_195/main.tex"
    pdf_path = ROOT / "source_current_195/main.pdf"
    log_path = ROOT / "source_current_195/main.log"
    tex = tex_path.read_text(encoding="utf-8")
    log = log_path.read_text(encoding="utf-8", errors="replace")
    fatal_count = len(re.findall(r"(?m)^! ", log))
    undefined_count = len(re.findall(r"undefined (?:references|citations)|Reference .* undefined|Citation .* undefined", log, re.I))
    duplicate_destinations = len(re.findall(r"destination with the same identifier", log, re.I))
    overfull_hboxes = len(re.findall(r"Overfull \\hbox", log))
    overfull_vboxes = len(re.findall(r"Overfull \\vbox", log))

    registry = json.loads((ROOT / "reproducibility/data/figure_data_manifest.json").read_text(encoding="utf-8"))
    blockers = [item["id"] for item in state if item["reexecutionStatus"] == "BLOCKED"]
    deferred = [item["id"] for item in state if item["reexecutionStatus"] == "DEFERRED"]
    checks = {
        "exactly_203_tasks": len(state) == 203,
        "unique_ids_and_sequences": len({i["id"] for i in state}) == 203 and [i["sequence"] for i in state] == list(range(1, 204)),
        "all_statuses_allowed": all(i["reexecutionStatus"] in allowed for i in state),
        "active_state_is_valid": terminal_ok,
        "all_executable_reports_pass": all(value == "PASS" for value in report_statuses.values()),
        "archive_member_checks_pass": archive_validation.get("result") == "PASS" and archive_validation.get("expected_entries") == archive_validation.get("validated_entries") and archive_validation.get("checksum_failures") == 0,
        "archive_file_hash_matches": archive_hash_ok,
        "eight_figures_registered": registry.get("main_figure_count") == 8 and len(registry.get("figures", [])) == 8,
        "latex_fatal_errors_zero": fatal_count == 0,
        "undefined_references_zero": undefined_count == 0,
        "pdf_exists": pdf_path.is_file() and pdf_path.stat().st_size > 0,
        "task_provenance_comments_absent_from_tex": re.search(r"(?m)%\s*(?:BEGIN|END|source tasks?)\s+P", tex, re.I) is None,
        "external_reviews_remain_explicitly_blocked": all(x in blockers for x in ["P3-20-19", "P3-20-20"]),
        "submission_metadata_blockers_remain_explicit": all(x in blockers for x in ["P3-19-05", "P3-19-08", "P3-19-10"]),
    }
    critical_internal_defects = sum(1 for passed in checks.values() if not passed)
    result = {
        "task_id": "P3-20-21",
        "status": "PASS" if critical_internal_defects == 0 else "FAIL",
        "mode": "preclose" if args.allow_active_final else "terminal",
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "critical_internal_defects": critical_internal_defects,
        "task_status_counts": dict(sorted(statuses.items())),
        "blocked_count": len(blockers),
        "deferred_count": len(deferred),
        "submission_ready": False,
        "submission_blockers": ["author competing-interest confirmation", "public source-code DOI/URL", "public companion DOI/arXiv/URL", "two independent external blind reviews"],
        "manuscript": {
            "tex_sha256": sha256(tex_path),
            "pdf_sha256": sha256(pdf_path),
            "pdf_bytes": pdf_path.stat().st_size,
            "fatal_errors": fatal_count,
            "undefined_references_or_citations": undefined_count,
            "duplicate_pdf_destinations_nonfatal": duplicate_destinations,
            "overfull_hboxes_nonfatal": overfull_hboxes,
            "overfull_vboxes_nonfatal": overfull_vboxes,
        },
        "archive": archive_validation,
        "pass_reports": report_statuses,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
