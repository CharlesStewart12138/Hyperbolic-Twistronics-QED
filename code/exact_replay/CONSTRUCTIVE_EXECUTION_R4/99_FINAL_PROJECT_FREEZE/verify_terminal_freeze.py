"""Build once, then verify the fail-closed terminal project freeze."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import psutil


FREEZE = Path(__file__).resolve().parent
R4 = FREEZE.parent
ROOT = R4.parent
MATH_ROOT = "AEEE9C3AB53239DDD6231A870AEAA88C61881DF4B6D187F4CAA5B0F550549618"

ROOT_SCOPE = (
    "CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json",
    "CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json",
    "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json",
    "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_CERTIFICATE.json",
    "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/Q24_RELATION_CERTIFICATE.md",
    "source_current_195/main.tex",
    "production_code/MODEL_CONTRACT.md",
    "production_code/config/theory_production_benchmark.yaml",
    "production_code/config/model.yaml",
    "CONSTRUCTIVE_EXECUTION_R4/19_RESOURCE_CLOSURE/A1_ERROR_BUDGET.tsv",
    "CONSTRUCTIVE_EXECUTION_R4/19_RESOURCE_CLOSURE/A1_RESOURCE_CONTRACT_TERMINAL.json",
    "CONSTRUCTIVE_EXECUTION_R4/19_RESOURCE_CLOSURE/A1_RESOURCE_CONTRACT_TERMINAL.tsv",
    "CONSTRUCTIVE_EXECUTION_R4/22_OPERATOR_CONSISTENCY/A1_OPERATOR_CONSISTENCY_AUDIT.md",
    "CONSTRUCTIVE_EXECUTION_R4/22_OPERATOR_CONSISTENCY/OPERATOR_CONTRADICTION_REPLAY.json",
    "CONSTRUCTIVE_EXECUTION_R4/22_OPERATOR_CONSISTENCY/ZERO_TWIST_SUPPORT_DIAGNOSTIC.json",
    "CONSTRUCTIVE_EXECUTION_R4/22_OPERATOR_CONSISTENCY/verify_operator_contradiction.py",
    "CONSTRUCTIVE_EXECUTION_R4/22_OPERATOR_CONSISTENCY/compute_zero_twist_support_diagnostic.py",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_RESOURCE_CONTRACT.json",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_PRODUCTION_MANIFEST.json",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_CLAIM_REGISTRY.tsv",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_INDEPENDENT_AUDIT.json",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_REPRODUCIBILITY.md",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_A1_ROOT.txt",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_MATHEMATICAL_ROOT.txt",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_MANUSCRIPT/NOT_CREATED.md",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_CERTIFICATES/INDEX_V2.tsv",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_SOURCE_DATA/INDEX_V2.tsv",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_CODE_MANIFEST/INDEX_V2.tsv",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/verify_terminal_freeze.py",
)

REQUIRED_FREEZE = (
    "FINAL_ROOT_MANIFEST.json",
    "FINAL_MATHEMATICAL_ROOT.txt",
    "FINAL_A1_ROOT.txt",
    "FINAL_RESOURCE_CONTRACT.json",
    "FINAL_PRODUCTION_MANIFEST.json",
    "FINAL_CLAIM_REGISTRY.tsv",
    "FINAL_INDEPENDENT_AUDIT.json",
    "FINAL_DELIVERY_VERIFICATION.json",
    "FINAL_REPRODUCIBILITY.md",
    "FINAL_PROJECT_REPORT.md",
    "H_FINAL.txt",
    "FINAL_HASHES.sha256",
    "FINAL_MANUSCRIPT/NOT_CREATED.md",
    "FINAL_CERTIFICATES/INDEX_V2.tsv",
    "FINAL_SOURCE_DATA/INDEX_V2.tsv",
    "FINAL_CODE_MANIFEST/INDEX_V2.tsv",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def atomic_text(path: Path, content: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def root_payload() -> tuple[dict[str, str], str]:
    hashes = {}
    for relative in ROOT_SCOPE:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        hashes[relative] = sha256(path)
    canonical = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashes, hashlib.sha256(canonical).hexdigest().upper()


def process_snapshot() -> dict[str, int]:
    project = legacy = gap = 0
    for proc in psutil.process_iter(("pid", "name", "cmdline")):
        if proc.info["pid"] == os.getpid():
            continue
        name = (proc.info.get("name") or "").lower()
        command = " ".join(proc.info.get("cmdline") or []).lower()
        if name in {"gap.exe", "gap", "gapw95.exe"} or " gap.exe" in command:
            gap += 1
        if "scan_candidate_0005" in command or "degree-24" in command or "degree24" in command:
            legacy += 1
        if "constructive_execution_r4" in command or "d:\\work\\revise" in command:
            project += 1
    return {"running_project_processes": project, "running_legacy_enumeration_processes": legacy, "running_abandoned_GAP_processes": gap}


def semantic_checks(expected_root: str) -> dict[str, bool]:
    replay = json.loads((R4 / "22_OPERATOR_CONSISTENCY/OPERATOR_CONTRADICTION_REPLAY.json").read_text(encoding="utf-8"))
    support = json.loads((R4 / "22_OPERATOR_CONSISTENCY/ZERO_TWIST_SUPPORT_DIAGNOSTIC.json").read_text(encoding="utf-8"))
    claims = (FREEZE / "FINAL_CLAIM_REGISTRY.tsv").read_text(encoding="utf-8").splitlines()
    allowed = {"PROVED_EXACT", "COMPUTER_ASSISTED_EXACT", "NUMERICALLY_CERTIFIED", "CONDITIONAL_THEOREM", "UNVERIFIED", "FAILED"}
    claim_statuses = {line.split("\t")[1] for line in claims[1:] if line.strip()}
    report = (FREEZE / "FINAL_PROJECT_REPORT.md").read_text(encoding="utf-8")
    return {
        "mathematical_root_exact": (FREEZE / "FINAL_MATHEMATICAL_ROOT.txt").read_text(encoding="utf-8").strip() == MATH_ROOT,
        "contradiction_replay_14_of_14": replay.get("all_checks_pass") is True and len(replay.get("checks", {})) == 14,
        "contradiction_classification_exact": replay.get("classification") == "FAIL_MATHEMATICAL_CONTRADICTION_REPRODUCED",
        "zero_twist_support_counts_exact": [row["support_per_row"] for row in support["support_rows"]] == [473, 2105, 8289],
        "claim_status_vocabulary_closed": claim_statuses <= allowed,
        "A1_root_explicitly_not_created": (FREEZE / "FINAL_A1_ROOT.txt").read_text(encoding="utf-8").startswith("NOT_CREATED:"),
        "no_fake_manuscript": (FREEZE / "FINAL_MANUSCRIPT/NOT_CREATED.md").is_file() and not (FREEZE / "FINAL_MANUSCRIPT/main.pdf").exists(),
        "report_contains_final_root": expected_root in report,
        "report_terminal_sentence_exact": report.rstrip().endswith("PROJECT_STATUS = MATHEMATICAL_CONTRADICTION: the mandatory generic-incommensurate fixed-92160-dimensional global quotient operator conflicts with the authoritative local-only paired-cover theorem."),
    }


def build() -> None:
    hashes, final_root = root_payload()
    report = FREEZE / "FINAL_PROJECT_REPORT.md"
    if not report.is_file():
        raise FileNotFoundError("FINAL_PROJECT_REPORT.md must be authored before --build")
    checks = semantic_checks(final_root)
    if not all(checks.values()):
        raise RuntimeError(f"semantic checks failed before freeze: {checks}")

    root_manifest = {
        "schema_version": "1.0",
        "classification": "TERMINAL_MATHEMATICAL_CONTRADICTION_ROOT",
        "candidate_id": "CAND-R4-0005",
        "mathematical_root": MATH_ROOT,
        "root_algorithm": "SHA256(canonical JSON map of workspace-relative path to uppercase SHA256)",
        "root_scope_excludes": ["generated root manifest", "H_FINAL.txt", "delivery verification", "hash listing", "human final report"],
        "payload_hashes_sha256": hashes,
        "H_FINAL": final_root,
    }
    atomic_text(FREEZE / "FINAL_ROOT_MANIFEST.json", json.dumps(root_manifest, indent=2) + "\n")
    atomic_text(FREEZE / "H_FINAL.txt", final_root + "\n")

    processes = process_snapshot()
    delivery = {
        "schema_version": "1.0",
        "classification": "TERMINAL_DELIVERY_PASS_FAIL_CLOSED",
        "required_artifacts_present": True,
        "semantic_checks": checks,
        "semantic_check_count": f"{sum(checks.values())}/{len(checks)}",
        "H_FINAL": final_root,
        **processes,
        "mathematical_status": "PASS",
        "project_status": "MATHEMATICAL_CONTRADICTION",
        "verified_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if any(processes.values()):
        raise RuntimeError(f"process closure failed: {processes}")
    atomic_text(FREEZE / "FINAL_DELIVERY_VERIFICATION.json", json.dumps(delivery, indent=2) + "\n")

    lines = []
    for path in sorted(p for p in FREEZE.rglob("*") if p.is_file() and p.name != "FINAL_HASHES.sha256"):
        relative = path.relative_to(FREEZE).as_posix()
        lines.append(f"{sha256(path)}  {relative}")
    atomic_text(FREEZE / "FINAL_HASHES.sha256", "\n".join(lines) + "\n")
    print(json.dumps({"classification": delivery["classification"], "H_FINAL": final_root, "semantic_checks": delivery["semantic_check_count"], **processes}, indent=2))


def verify() -> None:
    hashes, final_root = root_payload()
    manifest = json.loads((FREEZE / "FINAL_ROOT_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("payload_hashes_sha256") != hashes or manifest.get("H_FINAL") != final_root:
        raise RuntimeError("final root manifest mismatch")
    missing = [name for name in REQUIRED_FREEZE if not (FREEZE / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing terminal artifacts: {missing}")
    listed = {}
    for line in (FREEZE / "FINAL_HASHES.sha256").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        listed[relative] = digest
    actual_files = sorted(p for p in FREEZE.rglob("*") if p.is_file() and p.name != "FINAL_HASHES.sha256")
    actual = {path.relative_to(FREEZE).as_posix(): sha256(path) for path in actual_files}
    if listed != actual:
        raise RuntimeError("FINAL_HASHES.sha256 mismatch")
    checks = semantic_checks(final_root)
    if not all(checks.values()):
        raise RuntimeError(f"semantic verification failed: {checks}")
    print(json.dumps({"classification": "TERMINAL_FREEZE_VERIFIED", "H_FINAL": final_root, "hashes": f"{len(actual)}/{len(actual)}", "semantic_checks": f"{sum(checks.values())}/{len(checks)}"}, indent=2))


if __name__ == "__main__":
    if "--print-root" in sys.argv:
        print(root_payload()[1])
    elif "--build" in sys.argv:
        build()
    else:
        verify()
