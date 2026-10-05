from __future__ import annotations

import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
OUT = R4 / "21_FINAL_REPORTS"
CHECKS: list[dict] = []


def load_json(relative: str) -> dict:
    return json.loads((R4 / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def check(name: str, condition: bool, evidence: str = "") -> None:
    CHECKS.append({"name": name, "pass": bool(condition), "evidence": evidence})


def main() -> None:
    freeze_path = R4 / "17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json"
    root_path = R4 / "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json"
    preimage_path = R4 / "17_FINAL_FREEZE/H_MATH_PREIMAGE.txt"
    freeze = load_json("17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json")
    root = load_json("17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json")
    group_manifest = load_json("17_FINAL_FREEZE/artifacts/CAND-R4-0005_GROUP_ARTIFACT_MANIFEST.json")
    delivery = load_json("17_FINAL_FREEZE/R4_DELIVERY_20_OF_20_VERIFICATION.json")
    mu_tr = load_json("18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_CERTIFICATE.json")
    mu = load_json("18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json")
    theory = load_json("18_Q24_CLOSURE/FINITE_QUOTIENT_THEORY_STATUS.json")
    resource = load_json("19_RESOURCE_CLOSURE/RESOURCE_STATUS.json")
    formulas = load_json("19_RESOURCE_CLOSURE/DETERMINISTIC_RESOURCE_FORMULAS.json")
    pilot = load_json("19_RESOURCE_CLOSURE/INTRALAYER_MATRIX_FREE_PILOT.json")
    paper = load_json("PAPER_INTEGRATION_R4/PAPER_INTEGRATION_MANIFEST.json")
    workbook = load_json("20_POSTCONSTRUCTION/AUTHORITATIVE_WORKBOOK_CONSOLIDATED_UPDATE_AUDIT.json")
    processes = load_json("20_POSTCONSTRUCTION/POSTCONSTRUCTION_PROCESS_AUDIT.json")
    report = load_json("21_FINAL_REPORTS/POSTCONSTRUCTION_FINAL_REPORT.json")
    state = load_json("21_FINAL_REPORTS/POSTCONSTRUCTION_STATE.json")

    preimage_bytes = preimage_path.read_bytes()
    h_math_recomputed = hashlib.sha256(preimage_bytes.rstrip(b"\r\n")).hexdigest().upper()
    check("candidate identity", freeze["candidate_id"] == "CAND-R4-0005")
    check("exact order 46080", freeze["exact_group_order"] == 46080)
    check("immutable freeze hash", sha256(freeze_path) == root["mathematical_freeze"]["sha256"])
    check("H_MATH preimage file hash", sha256(preimage_path) == root["H_MATH_preimage_file_sha256"])
    check("H_MATH recomputation", h_math_recomputed == root["H_MATH"], h_math_recomputed)
    check("mathematical status independent of resources", freeze["MATHEMATICAL_STATUS"] == "CERTIFIED" and root["MATHEMATICAL_STATUS"] == "PASS")
    check("resource status remains unverified", freeze["RESOURCE_STATUS"] == root["RESOURCE_STATUS"] == "UNVERIFIED")
    check("A1 remains not frozen", freeze["A1_STATUS"] == "NOT_FROZEN" and root["PRODUCTION_A1_STATUS"] == "NOT_FROZEN")

    artifact_dir = R4 / "17_FINAL_FREEZE/artifacts"
    artifact_results = []
    for name, spec in group_manifest["artifacts"].items():
        path = artifact_dir / name
        ok = path.is_file() and path.stat().st_size == spec["bytes"] and sha256(path) == spec["sha256"]
        artifact_results.append(ok)
    check("all exact group artifacts present, sized, and hashed", all(artifact_results), f"{sum(artifact_results)}/{len(artifact_results)}")
    check("group artifact direct-product equality", group_manifest["direct_product_set_equality"] is True)
    check("exact C8 artifact bound", group_manifest["artifacts"]["CAND-R4-0005.C8_automorphism_u32le.bin"]["sha256"] == freeze["exact_group_artifacts"]["C8_automorphism_sha256"])
    check("exact parity artifact bound", group_manifest["artifacts"]["CAND-R4-0005.parity_u8.bin"]["sha256"] == freeze["exact_group_artifacts"]["parity_character_sha256"])
    check("primary global complete scan", freeze["primary_scan_root"]["records_scanned"] == 785_639_753 and freeze["primary_scan_root"]["kernel_hits"] == 0)
    check("independent global complete scan", freeze["independent_scan_root"]["records_scanned"] == 785_639_753 and freeze["independent_scan_root"]["kernel_hits"] == 0)
    check("final independent endpoint audit", freeze["audit_results"]["final_independent_audit"] == "30/30 PASS")
    check("original delivery verification", delivery["verified_artifacts"] == 20 and delivery["failed_artifacts"] == 0)

    rejection_path = R4 / "18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_SMALLER_INDEX_REJECTIONS.tsv"
    with rejection_path.open("r", encoding="utf-8", newline="") as stream:
        rejection_rows = list(csv.DictReader(stream, delimiter="\t"))
    check("mu_tr exact value", mu_tr["mu_tr"] == 5120)
    check("mu_tr witness order/index/core", mu_tr["witness_subgroup"]["order"] == 9 and mu_tr["witness_subgroup"]["index_in_Q"] == 5120 and mu_tr["witness_subgroup"]["core_in_Q_order"] == 1)
    check("mu_tr complete smaller-index rejection", len(rejection_rows) == 5119 and sha256(rejection_path) == mu_tr["complete_exclusion"]["smaller_index_rejection_sha256"], str(len(rejection_rows)))
    check("mu exact value", mu["mu"] == 92)
    check("faithful witness degree and image order", sum(mu["faithful_upper_witness"]["orbit_sizes"]) == 92 and mu["faithful_upper_witness"]["image_order"] == 46080)
    replay_path = R4 / mu["verifier"]["replay_output"]
    check("mu GAP replay hash", sha256(replay_path) == mu["verifier"]["replay_output_sha256"] and "MU_Q=92" in replay_path.read_text(encoding="utf-8"))
    check("q24 branch A", theory["q24_RELATION"] == "RESOLVED_BRANCH_A" and theory["Q_NOT_IN_DEGREE24_DOMAIN"] is True and theory["old_q24_restart_required"] is False)
    check("finite quotient history closed", theory["FINITE_QUOTIENT_THEORY_STATUS"] == "CLOSED")

    audit_tsv = R4 / "19_RESOURCE_CLOSURE/RESOURCE_CONTRACT_AUDIT.tsv"
    with audit_tsv.open("r", encoding="utf-8", newline="") as stream:
        resource_rows = list(csv.DictReader(stream, delimiter="\t"))
    check("resource audit row count", len(resource_rows) == resource["resource_contract_rows"] == 38)
    check("resource missing-decision count", resource["missing_project_decision_rows"] == 22)
    check("resource implementation-open count", resource["implementation_dependent_open_rows"] == 1)
    check("resource audit hash", sha256(audit_tsv) == resource["resource_contract_audit_sha256"])
    check("resource state B classification", resource["classification"] == "STATE_B_RESOURCE_UNVERIFIED_MISSING_SPECIFICATION")
    check("production mode not silently chosen", resource["production_mode"] == "UNSPECIFIED")
    check("Hilbert dimension independently derived", freeze["exact_group_order"] * 2 == pilot["Hilbert_dimension"] == 92160)
    check("bounded pilot scope only", pilot["classification"] == "PASS_SAFE_BOUNDED_INTRALAYER_ONLY_PILOT" and "production resource upper bound" in pilot["not_in_scope"])
    check("deterministic formula candidate/order binding", formulas["candidate_id"] == "CAND-R4-0005" and formulas["dimensions"]["Hilbert_dimension"] == 92160)
    check("A1 input decision sheet exists", (R4 / "19_RESOURCE_CLOSURE/A1_RESOURCE_INPUT_REQUEST.md").is_file())
    check("no Level-A1 freeze directory", not (R4 / "LEVEL_A1_CONSTRUCTIVE_R4_FREEZE").exists())
    check("HPC not triggered for undefined production task", resource["HPC_status"] == "NOT_TRIGGERED_FOR_PRODUCTION_RESOURCE_GATE")

    paper_dir = R4 / "PAPER_INTEGRATION_R4"
    paper_results = []
    for spec in paper["files"]:
        path = paper_dir / spec["path"]
        paper_results.append(path.is_file() and path.stat().st_size == spec["bytes"] and sha256(path) == spec["sha256"])
    check("paper integration payload hashes", all(paper_results), f"{sum(paper_results)}/{len(paper_results)}")
    check("locked main manuscript untouched by package builder", paper["main_manuscript_modified"] is False)
    check("claim registry exists", (R4 / "20_POSTCONSTRUCTION/FINAL_CLAIM_REGISTRY.tsv").is_file())
    check("v1 false-positive provenance retained", "false-positive" in (R4 / "20_POSTCONSTRUCTION/CERTIFICATION_PROVENANCE.md").read_text(encoding="utf-8").lower())

    source_workbook = R4 / "00_FROZEN_INPUTS/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx"
    output_workbook = R4 / workbook["output"]
    check("authoritative source workbook immutable", sha256(source_workbook) == workbook["source_sha256_before"] == workbook["source_sha256_after"])
    check("consolidated workbook output hash", sha256(output_workbook) == workbook["output_sha256"])
    check("single consolidated workbook classification", workbook["classification"] == "PASS_SINGLE_CONSOLIDATED_VERSIONED_UPDATE")

    check("final report has exactly 32 ordered items", len(report["items"]) == 32 and [x["number"] for x in report["items"]] == list(range(1, 33)))
    check("terminal state B", report["acceptance_state"] == state["acceptance_state"] == "STATE_B")
    check("full physics production not started", state["full_physics_production_started"] is False)
    check("background R4 process count zero", processes["background_R4_process_count"] == 0)
    check("background legacy enumeration count zero", processes["background_legacy_enumeration_process_count"] == 0)
    check("background GAP process count zero", processes["background_GAP_process_count"] == 0)

    failed = [entry for entry in CHECKS if not entry["pass"]]
    result = {
        "schema_version": "1.0",
        "classification": "PASS" if not failed else "FAIL",
        "checks": CHECKS,
        "passed": len(CHECKS) - len(failed),
        "failed": len(failed),
        "failures": [entry["name"] for entry in failed],
        "H_MATH_recomputed": h_math_recomputed,
        "audited_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "audit_scope": "post-construction artifacts only; frozen 785,639,753-record scans were not rerun",
    }
    json_path = OUT / "POSTCONSTRUCTION_INDEPENDENT_AUDIT.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    suite = ET.Element("testsuite", {
        "name": "postconstruction-independent-audit",
        "tests": str(len(CHECKS)),
        "failures": str(len(failed)),
    })
    for entry in CHECKS:
        case = ET.SubElement(suite, "testcase", {"name": entry["name"]})
        if not entry["pass"]:
            failure = ET.SubElement(case, "failure", {"message": entry["evidence"] or "check failed"})
            failure.text = entry["evidence"] or entry["name"]
    xml_path = OUT / "POSTCONSTRUCTION_INDEPENDENT_AUDIT.junit.xml"
    ET.ElementTree(suite).write(xml_path, encoding="utf-8", xml_declaration=True)

    print(json.dumps({
        "classification": result["classification"],
        "passed": result["passed"],
        "failed": result["failed"],
        "audit_sha256": sha256(json_path),
        "junit_sha256": sha256(xml_path),
    }, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
