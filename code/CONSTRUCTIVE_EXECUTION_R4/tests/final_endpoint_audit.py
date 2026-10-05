"""Independent consistency audit for the finalized R4 endpoint artifacts."""
from __future__ import annotations

import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: str) -> dict:
    return json.loads((R4 / path).read_text(encoding="utf-8"))


checks: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    checks.append((name, bool(condition), detail))


root_hash = (R4 / "00_FROZEN_INPUTS/FROZEN_INPUT_ROOT_HASH.txt").read_text(encoding="utf-8").strip()
candidate_path = R4 / "10_CANDIDATES/CAND-R4-0005.certificate.json"
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

check("root hash propagated", endpoint["frozen_input_root_hash"] == root_hash == resource["frozen_input_root_hash"])
check("candidate order", candidate["actual_order"] == endpoint["actual_order"] == 46080)
check("candidate marked hash", candidate["marked_quotient_hash"] == endpoint["marked_quotient_hash"])
check("candidate math certificate hash", endpoint["proof_chain"]["candidate_math_certificate"]["sha256"] == sha256(candidate_path))
for key in ("global_scan", "independent_replay", "representation", "minimization", "resource"):
    row = endpoint["proof_chain"][key]
    check(f"proof hash {key}", row["sha256"] == sha256(R4 / row["path"]))
check("primary global complete", global_cert["classification"] == "PASS_COMPLETE_CLOSED_DOMAIN" and global_cert["records_scanned"] == 785639753 and global_cert["kernel_hits"] == 0)
check("independent global complete", independent["classification"] == "PASS_COMPLETE_CLOSED_DOMAIN" and independent["global"]["closed_domain_records"] == 785639753 and independent["global"]["kernel_hits"] == 0)
check("direct product proof", representation["subdirect_product_proof"]["actual_generated_diagonal_image_order"] == 720 * 64 == 46080 and representation["subdirect_product_proof"]["equal_finite_orders"])
check("faithful action bounds", representation["certified_permutation_actions"]["faithful_intransitive"]["degree"] == 784 and representation["certified_permutation_actions"]["faithful_transitive"]["degree"] == 46080)
check("physical Hilbert dimension", representation["physical_regular_quotient_model"]["one_particle_hilbert_dimension"] == 92160)
check("resource fails closed", resource["decision"]["resource_gate"] == "UNVERIFIED" and not resource["decision"]["A1_release_allowed"])
check("mandatory resource fields null", all(resource["frozen_numerical_A1_budget"][key] is None for key in ("matvec_budget", "wall_time_budget_seconds", "residual_tolerance", "krylov_dimension", "polynomial_degree", "parameter_grid_cardinality", "probe_count", "precision_policy")))
check("minimal selected presentation", minimum["classification"] == "MINIMAL_WITHIN_SELECTED_TWO_FACTOR_PRESENTATION" and minimum["factors_deleted"] == [])
check("A1 not found", a1["status"] == report["T_A1"] == "A1_NOT_FOUND" or (a1["status"] == "A1_NOT_FOUND" and report["T_A1"] == "NOT FOUND"))
check("no Hamiltonian", not a1["full_Hamiltonian_started"] and not state["full_hamiltonian_started"])
check("legacy enumeration off", report["B_legacy_degree_enumeration_active"] == "NO" and report["V_old_exhaustive_degree_search_launched"] == "NO" and not state["legacy_degree_enumeration_active"])
check("HPC not triggered", report["HPC_handoff"] == "NOT_TRIGGERED" and not state["HPC_escalation_triggered"])
check("final report endpoint hash", report["endpoint_certificate_sha256"] == sha256(R4 / "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json"))

with (R4 / "10_CANDIDATES/CANDIDATE_LEDGER.tsv").open("r", encoding="utf-8", newline="") as handle:
    ledger = list(csv.DictReader(handle, delimiter="\t"))
check("five sequential candidate rows", [r["Candidate ID"] for r in ledger] == [f"CAND-R4-{i:04d}" for i in range(1, 6)])
row5 = ledger[-1]
check("ledger endpoint hash", row5["Certificate hash"] == sha256(R4 / "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json"))
check("ledger resource status", row5["Resource status"] == "UNVERIFIED_UNSET_COMPONENTS")
check("ledger global status", row5["Global status"] == "PASS_COMPLETE_CLOSED_DOMAIN")

failures = [name for name, passed, _ in checks if not passed]
audit = {
    "schema_version": "1.0",
    "classification": "PASS" if not failures else "FAIL",
    "checks": [{"name": n, "pass": p, "detail": d} for n, p, d in checks],
    "passed": sum(1 for _, p, _ in checks if p),
    "failed": len(failures),
    "failures": failures,
    "audited_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
}
(R4 / "11_CERTIFICATES/R4_FINAL_ENDPOINT_INDEPENDENT_AUDIT.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

suite = ET.Element("testsuite", name="r4_final_endpoint_audit", tests=str(len(checks)), failures=str(len(failures)), errors="0", skipped="0")
for name, passed, detail in checks:
    case = ET.SubElement(suite, "testcase", name=name)
    if not passed:
        failure = ET.SubElement(case, "failure", message=detail or "assertion failed")
        failure.text = name
tree = ET.ElementTree(ET.Element("testsuites"))
tree.getroot().append(suite)
tree.write(R4 / "tests/final_endpoint_audit.junit.xml", encoding="utf-8", xml_declaration=True)

print(json.dumps({"classification": audit["classification"], "passed": audit["passed"], "failed": audit["failed"], "failures": failures}, indent=2))
raise SystemExit(1 if failures else 0)
