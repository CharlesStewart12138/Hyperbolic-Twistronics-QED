"""Normalize the frozen-input root hash and rebind downstream endpoint files."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(rel: str) -> dict:
    return json.loads((R4 / rel).read_text(encoding="utf-8"))


def save(rel: str, value: dict) -> None:
    (R4 / rel).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


root_line = (R4 / "00_FROZEN_INPUTS/FROZEN_INPUT_ROOT_HASH.txt").read_text(encoding="utf-8").strip()
match = re.fullmatch(r"sha256\s+([0-9A-Fa-f]{64})\s+FROZEN_INPUT_MANIFEST\.tsv", root_line)
if not match:
    raise ValueError(f"unexpected frozen root checksum line: {root_line!r}")
root_hash = match.group(1).upper()

resource_rel = "13_RESOURCE_GATE/CAND-R4-0005_RESOURCE_GATE.json"
resource = load(resource_rel)
resource["frozen_input_root_hash"] = root_hash
resource["schema_version"] = "1.1"
resource["hash_field_correction"] = "v2: canonical 64-hex digest extracted from checksum-file line"
save(resource_rel, resource)

endpoint_rel = "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json"
endpoint = load(endpoint_rel)
endpoint["frozen_input_root_hash"] = root_hash
endpoint["proof_chain"]["resource"]["sha256"] = sha256(R4 / resource_rel)
endpoint["schema_version"] = "1.1"
endpoint["hash_field_correction"] = "v2: canonical 64-hex frozen-input digest"
save(endpoint_rel, endpoint)
endpoint_hash = sha256(R4 / endpoint_rel)

# Bind all immutable mathematical candidate certificates to the same canonical
# input root without rewriting the already-referenced math certificates.
bindings = []
for index in range(1, 6):
    rel = f"10_CANDIDATES/CAND-R4-{index:04d}.certificate.json"
    cert = load(rel)
    bindings.append({
        "candidate_id": cert["candidate_id"],
        "candidate_certificate": rel,
        "candidate_certificate_sha256": sha256(R4 / rel),
        "marked_quotient_hash": cert["marked_quotient_hash"],
        "frozen_input_root_hash": root_hash,
    })
save(
    "11_CERTIFICATES/CANDIDATE_FROZEN_INPUT_BINDINGS.json",
    {
        "schema_version": "1.0",
        "classification": "PASS_CONTENT_ADDRESSED_FROZEN_INPUT_BINDING",
        "frozen_input_root_hash": root_hash,
        "binding_method": "immutable candidate certificate hash plus marked quotient hash",
        "candidate_bindings": bindings,
        "candidate_count": len(bindings),
    },
)

ledger_path = R4 / "10_CANDIDATES/CANDIDATE_LEDGER.tsv"
with ledger_path.open("r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    fields = list(reader.fieldnames or [])
    rows = list(reader)
for row in rows:
    if row["Candidate ID"] == "CAND-R4-0005":
        row["Certificate hash"] = endpoint_hash
with ledger_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

a1_rel = "14_LEVEL_A1/A1_NOT_FOUND.json"
a1 = load(a1_rel)
a1["endpoint_certificate_sha256"] = endpoint_hash
a1["schema_version"] = "1.1"
save(a1_rel, a1)

report_json_rel = "16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.json"
report_json = load(report_json_rel)
report_json["C_frozen_input_hash"] = root_hash
report_json["endpoint_certificate_sha256"] = endpoint_hash
report_json["resource_certificate_sha256"] = sha256(R4 / resource_rel)
report_json["candidate_input_bindings_sha256"] = sha256(R4 / "11_CERTIFICATES/CANDIDATE_FROZEN_INPUT_BINDINGS.json")
report_json["schema_version"] = "1.1"
save(report_json_rel, report_json)

report_md_path = R4 / "16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.md"
report_md = report_md_path.read_text(encoding="utf-8")
report_md = report_md.replace(f"`{root_line}`", f"`{root_hash}`")
report_md_path.write_text(report_md, encoding="utf-8")

state = load("EXECUTION_STATE.json")
state["best_candidate_endpoint_sha256"] = endpoint_hash
state["frozen_input_root_hash"] = root_hash
state["schema_version"] = "1.1"
save("EXECUTION_STATE.json", state)

worklog_path = R4 / "logs/WORK_LOG_R4_20260915.md"
worklog = worklog_path.read_text(encoding="utf-8").replace(f"`{root_line}`", f"`{root_hash}`")
worklog_path.write_text(worklog, encoding="utf-8")

tasks_path = R4 / "16_REPORTS/WORKBOOK_CONSTRUCTIVE_TASK_ROWS.tsv"
with tasks_path.open("r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    task_fields = list(reader.fieldnames or [])
    task_rows = list(reader)
for row in task_rows:
    if row["Task ID"] == "PF-GRP-CONSTRUCTIVE-R4-FROZEN":
        row["Notes"] = root_hash
with tasks_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=task_fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(task_rows)

print(json.dumps({
    "classification": "PASS_CANONICAL_ROOT_HASH_CORRECTION_V2",
    "canonical_frozen_input_root_hash": root_hash,
    "endpoint_certificate_sha256": endpoint_hash,
    "candidate_binding_count": len(bindings),
}, indent=2))
