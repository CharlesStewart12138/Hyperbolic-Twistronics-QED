"""Post-correction independent audit of the R4 endpoint proof chain."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(rel: str) -> dict:
    return json.loads((R4 / rel).read_text(encoding="utf-8"))


checks: list[tuple[str, bool]] = []


def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))


line = (R4 / "00_FROZEN_INPUTS/FROZEN_INPUT_ROOT_HASH.txt").read_text(encoding="utf-8").strip()
match = re.fullmatch(r"sha256\s+([0-9A-Fa-f]{64})\s+FROZEN_INPUT_MANIFEST\.tsv", line)
root_hash = match.group(1).upper() if match else ""
check("checksum line parsed", bool(root_hash))

candidate = load("10_CANDIDATES/CAND-R4-0005.certificate.json")
global_cert = load("11_CERTIFICATES/CAND-R4-0005.global_pass_scan.json")
independent = load("11_CERTIFICATES/CAND-R4-0005.global_independent_replay.json")
representation = load("08_PRODUCTS/CAND-R4-0005_DIRECT_PRODUCT_AND_ACTION_CERTIFICATE.json")
resource = load("13_RESOURCE_GATE/CAND-R4-0005_RESOURCE_GATE.json")
endpoint = load("11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json")
minimum = load("12_MINIMIZATION/CAND-R4-0005.factor_deletion.json")
report = load("16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.json")
state = load("EXECUTION_STATE.json")
a1 = load("14_LEVEL_A1/A1_NOT_FOUND.json")
bindings = load("11_CERTIFICATES/CANDIDATE_FROZEN_INPUT_BINDINGS.json")
workbook_audit = load("16_REPORTS/WORKBOOK_R4_STATUS_UPDATE_AUDIT.json")
process_audit = load("logs/FINAL_PROCESS_AUDIT.json")

check("canonical root is 64 hex", bool(re.fullmatch(r"[0-9A-F]{64}", root_hash)))
check("root propagated", resource["frozen_input_root_hash"] == endpoint["frozen_input_root_hash"] == report["C_frozen_input_hash"] == state["frozen_input_root_hash"] == root_hash)
check("five candidates bound", bindings["candidate_count"] == 5 and all(r["frozen_input_root_hash"] == root_hash for r in bindings["candidate_bindings"]))
for row in bindings["candidate_bindings"]:
    check(f"binding hash {row['candidate_id']}", row["candidate_certificate_sha256"] == sha256(R4 / row["candidate_certificate"]))
for key in ("candidate_math_certificate", "global_scan", "independent_replay", "representation", "minimization", "resource"):
    row = endpoint["proof_chain"][key]
    check(f"endpoint proof hash {key}", row["sha256"] == sha256(R4 / row["path"]))
endpoint_hash = sha256(R4 / "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json")
check("endpoint hash propagated", report["endpoint_certificate_sha256"] == state["best_candidate_endpoint_sha256"] == a1["endpoint_certificate_sha256"] == endpoint_hash)
check("candidate order", candidate["actual_order"] == endpoint["actual_order"] == 46080)
check("complete primary global pass", global_cert["records_scanned"] == 785639753 and global_cert["kernel_hits"] == 0 and global_cert["classification"] == "PASS_COMPLETE_CLOSED_DOMAIN")
check("complete independent global pass", independent["global"]["closed_domain_records"] == 785639753 and independent["global"]["kernel_hits"] == 0 and independent["classification"] == "PASS_COMPLETE_CLOSED_DOMAIN")
check("faithful action constructions", representation["certified_permutation_actions"]["faithful_intransitive"]["degree"] == 784 and representation["certified_permutation_actions"]["faithful_transitive"]["degree"] == 46080)
check("physical dimension", representation["physical_regular_quotient_model"]["one_particle_hilbert_dimension"] == 92160)
check("selected-factor minimality", minimum["classification"] == "MINIMAL_WITHIN_SELECTED_TWO_FACTOR_PRESENTATION" and minimum["factors_deleted"] == [])
check("resource unverified", resource["decision"]["resource_gate"] == "UNVERIFIED" and not resource["decision"]["A1_release_allowed"])
check("A1 stopped", a1["status"] == "A1_NOT_FOUND" and not a1["full_Hamiltonian_started"])
check("workbook copy verified", workbook_audit["classification"] == "PASS_VERSIONED_COPY" and not workbook_audit["source_mutated"] and workbook_audit["rows_appended"] == 12)
check("no active scan process", process_audit["classification"] == "PASS_NO_ACTIVE_R4_OR_LEGACY_SCAN_PROCESS" and process_audit["active_match_count"] == 0)
check("legacy enumeration off", report["B_legacy_degree_enumeration_active"] == "NO" and report["V_old_exhaustive_degree_search_launched"] == "NO" and not state["legacy_degree_enumeration_active"])
check("HPC not triggered", report["HPC_handoff"] == "NOT_TRIGGERED" and not state["HPC_escalation_triggered"])

with (R4 / "10_CANDIDATES/CANDIDATE_LEDGER.tsv").open("r", encoding="utf-8", newline="") as handle:
    ledger = list(csv.DictReader(handle, delimiter="\t"))
check("candidate ledger sequence", [r["Candidate ID"] for r in ledger] == [f"CAND-R4-{i:04d}" for i in range(1, 6)])
check("candidate ledger endpoint", ledger[-1]["Certificate hash"] == endpoint_hash and ledger[-1]["Global status"] == "PASS_COMPLETE_CLOSED_DOMAIN" and ledger[-1]["Resource status"] == "UNVERIFIED_UNSET_COMPONENTS")

failed = [name for name, passed in checks if not passed]
payload = {
    "schema_version": "2.0",
    "classification": "PASS" if not failed else "FAIL",
    "checks": [{"name": name, "pass": passed} for name, passed in checks],
    "passed": sum(passed for _, passed in checks),
    "failed": len(failed),
    "failures": failed,
    "audited_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
}
(R4 / "11_CERTIFICATES/R4_FINAL_ENDPOINT_INDEPENDENT_AUDIT_V2.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
suite = ET.Element("testsuite", name="r4_final_endpoint_audit_v2", tests=str(len(checks)), failures=str(len(failed)), errors="0", skipped="0")
for name, passed in checks:
    case = ET.SubElement(suite, "testcase", name=name)
    if not passed:
        ET.SubElement(case, "failure", message="assertion failed").text = name
root = ET.Element("testsuites")
root.append(suite)
ET.ElementTree(root).write(R4 / "tests/final_endpoint_audit_v2.junit.xml", encoding="utf-8", xml_declaration=True)
print(json.dumps({"classification": payload["classification"], "passed": payload["passed"], "failed": payload["failed"], "failures": failed}, indent=2))
raise SystemExit(1 if failed else 0)
