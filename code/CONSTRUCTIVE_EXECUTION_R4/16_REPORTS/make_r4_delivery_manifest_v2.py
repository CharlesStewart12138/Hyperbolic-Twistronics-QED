"""Build the corrected content-addressed R4 endpoint delivery manifest."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
OUTPUT = R4 / "16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_DELIVERY_MANIFEST.json"
FILES = [
    ("10_CANDIDATES/CAND-R4-0005.certificate.json", "immutable mathematical candidate certificate"),
    ("10_CANDIDATES/CANDIDATE_LEDGER.tsv", "live constructive candidate ledger"),
    ("11_CERTIFICATES/CANDIDATE_FROZEN_INPUT_BINDINGS.json", "content-addressed candidate/input-root bindings"),
    ("11_CERTIFICATES/CAND-R4-0005.global_pass_scan.json", "primary complete global scan"),
    ("11_CERTIFICATES/CAND-R4-0005.global_independent_replay.json", "independent complete global replay"),
    ("11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json", "composite endpoint certificate"),
    ("11_CERTIFICATES/R4_FINAL_ENDPOINT_INDEPENDENT_AUDIT_V2.json", "post-correction independent endpoint audit"),
    ("12_MINIMIZATION/CAND-R4-0005.factor_deletion.json", "factor-deletion minimization certificate"),
    ("08_PRODUCTS/CAND-R4-0005_DIRECT_PRODUCT_AND_ACTION_CERTIFICATE.json", "direct-product and faithful-action certificate"),
    ("13_RESOURCE_GATE/CAND-R4-0005_RESOURCE_GATE.json", "fail-closed numerical resource decision"),
    ("14_LEVEL_A1/A1_NOT_FOUND.json", "explicit A1 stopping record"),
    ("16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.md", "human-readable required A--V report"),
    ("16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.json", "machine-readable required A--V report"),
    ("16_REPORTS/CONSTRUCTIVE_OBSTRUCTION_REPORT_R4.md", "required no-A1 obstruction report"),
    ("16_REPORTS/WORKBOOK_CONSTRUCTIVE_TASK_ROWS.tsv", "R4 workbook task-row source"),
    ("16_REPORTS/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan_R4_Status.xlsx", "versioned workbook status copy"),
    ("16_REPORTS/WORKBOOK_R4_STATUS_UPDATE_AUDIT.json", "workbook preservation/update audit"),
    ("logs/WORK_LOG_R4_20260915.md", "concise execution log"),
    ("logs/FINAL_PROCESS_AUDIT.json", "no-active-scan process audit"),
    ("EXECUTION_STATE.json", "current constructive execution state"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


line = (R4 / "00_FROZEN_INPUTS/FROZEN_INPUT_ROOT_HASH.txt").read_text(encoding="utf-8").strip()
match = re.fullmatch(r"sha256\s+([0-9A-Fa-f]{64})\s+FROZEN_INPUT_MANIFEST\.tsv", line)
if not match:
    raise ValueError("invalid frozen-input checksum line")
root_hash = match.group(1).upper()

artifacts = []
for rel, role in FILES:
    path = R4 / rel
    if not path.is_file():
        raise FileNotFoundError(path)
    artifacts.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path), "role": role})

payload = {
    "schema_version": "2.0",
    "classification": "R4_ENDPOINT_DELIVERY_COMPLETE_A1_NOT_FOUND_RESOURCE_UNVERIFIED",
    "frozen_input_root_hash": root_hash,
    "best_candidate": "CAND-R4-0005",
    "candidate_order": 46080,
    "global_systole": "PASS_COMPLETE_CLOSED_DOMAIN",
    "resource_gate": "UNVERIFIED_UNSET_COMPONENTS",
    "A1": "NOT_FOUND",
    "HPC_handoff": "NOT_TRIGGERED",
    "artifacts": artifacts,
    "artifact_count": len(artifacts),
    "created_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
}
OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"classification": payload["classification"], "artifact_count": len(artifacts), "manifest_sha256": sha256(OUTPUT), "frozen_input_root_hash": root_hash}, indent=2))
