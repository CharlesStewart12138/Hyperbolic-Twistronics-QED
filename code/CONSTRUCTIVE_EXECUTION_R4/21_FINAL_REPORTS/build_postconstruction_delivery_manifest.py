from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
OUT = R4 / "21_FINAL_REPORTS/POSTCONSTRUCTION_DELIVERY_MANIFEST.json"

FILES = [
    "17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json",
    "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json",
    "17_FINAL_FREEZE/H_MATH_PREIMAGE.txt",
    "17_FINAL_FREEZE/R4_DELIVERY_20_OF_20_VERIFICATION.json",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005_GROUP_ARTIFACT_MANIFEST.json",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005.elements_u8.bin",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005.right_generators_u32le.bin",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005.inverse_u32le.bin",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005.C8_automorphism_u32le.bin",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005.parity_u8.bin",
    "17_FINAL_FREEZE/artifacts/CAND-R4-0005_factor_regular_generators.g",
    "18_Q24_CLOSURE/FACTOR_IDENTIFICATION_GAP.txt",
    "18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_CERTIFICATE.json",
    "18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_SMALLER_INDEX_REJECTIONS.tsv",
    "18_Q24_CLOSURE/SL2_9_SUBGROUP_CLASS_AUDIT.tsv",
    "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json",
    "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_GAP_REPLAY.txt",
    "18_Q24_CLOSURE/Q24_RELATION_CERTIFICATE.md",
    "18_Q24_CLOSURE/FINITE_QUOTIENT_THEORY_STATUS.json",
    "19_RESOURCE_CLOSURE/RESOURCE_CONTRACT_AUDIT.tsv",
    "19_RESOURCE_CLOSURE/DETERMINISTIC_RESOURCE_FORMULAS.json",
    "19_RESOURCE_CLOSURE/DETERMINISTIC_RESOURCE_FORMULAS.md",
    "19_RESOURCE_CLOSURE/LOCAL_HARDWARE.json",
    "19_RESOURCE_CLOSURE/INTRALAYER_MATRIX_FREE_PILOT.json",
    "19_RESOURCE_CLOSURE/A1_RESOURCE_INPUT_REQUEST.md",
    "19_RESOURCE_CLOSURE/RESOURCE_STATUS.json",
    "19_RESOURCE_CLOSURE/WORKBOOK_UPDATE_PREVIEW.tsv",
    "20_POSTCONSTRUCTION/FINAL_CLAIM_REGISTRY.tsv",
    "20_POSTCONSTRUCTION/CERTIFICATION_PROVENANCE.md",
    "20_POSTCONSTRUCTION/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan_POST_CONSTRUCTION_FINAL.xlsx",
    "20_POSTCONSTRUCTION/AUTHORITATIVE_WORKBOOK_CONSOLIDATED_UPDATE_AUDIT.json",
    "20_POSTCONSTRUCTION/POSTCONSTRUCTION_PROCESS_AUDIT.json",
    "PAPER_INTEGRATION_R4/PAPER_INTEGRATION_MANIFEST.json",
    "21_FINAL_REPORTS/POSTCONSTRUCTION_FINAL_REPORT.md",
    "21_FINAL_REPORTS/POSTCONSTRUCTION_FINAL_REPORT.json",
    "21_FINAL_REPORTS/POSTCONSTRUCTION_STATE.json",
    "21_FINAL_REPORTS/POSTCONSTRUCTION_INDEPENDENT_AUDIT.json",
    "21_FINAL_REPORTS/POSTCONSTRUCTION_INDEPENDENT_AUDIT.junit.xml",
    "17_FINAL_FREEZE/build_exact_group_artifacts.py",
    "17_FINAL_FREEZE/create_mathematical_freeze.py",
    "18_Q24_CLOSURE/enumerate_sl2_9_subgroups.g",
    "18_Q24_CLOSURE/build_mu_tr_and_q24_certificates.py",
    "18_Q24_CLOSURE/replay_mu_q_compact_to_file.g",
    "19_RESOURCE_CLOSURE/build_resource_closure.py",
    "19_RESOURCE_CLOSURE/run_intralayer_matvec_pilot.py",
    "20_POSTCONSTRUCTION/build_claims_and_paper_package.py",
    "20_POSTCONSTRUCTION/create_consolidated_workbook_update.py",
    "20_POSTCONSTRUCTION/audit_background_processes.ps1",
    "21_FINAL_REPORTS/finalize_postconstruction_state_b_v2.py",
    "21_FINAL_REPORTS/run_postconstruction_independent_audit_v3.py",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    entries = []
    for relative in FILES:
        path = R4 / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})

    root = json.loads((R4 / FILES[1]).read_text(encoding="utf-8"))
    state = json.loads((R4 / "21_FINAL_REPORTS/POSTCONSTRUCTION_STATE.json").read_text(encoding="utf-8"))
    audit = json.loads((R4 / "21_FINAL_REPORTS/POSTCONSTRUCTION_INDEPENDENT_AUDIT.json").read_text(encoding="utf-8"))
    assert state["acceptance_state"] == "STATE_B"
    assert audit["classification"] == "PASS" and audit["failed"] == 0

    manifest = {
        "schema_version": "1.0",
        "classification": "POSTCONSTRUCTION_STATE_B_DELIVERY",
        "candidate_id": "CAND-R4-0005",
        "H_MATH": root["H_MATH"],
        "MATHEMATICAL_STATUS": "PASS",
        "q24_RELATION": "RESOLVED_BRANCH_A",
        "RESOURCE_STATUS": "UNVERIFIED",
        "PRODUCTION_A1_STATUS": "NOT_FROZEN",
        "acceptance_state": "STATE_B",
        "files": entries,
        "file_count": len(entries),
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "scope_note": "No full physical production run and no third 785,639,753-record scan were launched.",
    }
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "classification": manifest["classification"],
        "files": len(entries),
        "manifest_sha256": sha256(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
