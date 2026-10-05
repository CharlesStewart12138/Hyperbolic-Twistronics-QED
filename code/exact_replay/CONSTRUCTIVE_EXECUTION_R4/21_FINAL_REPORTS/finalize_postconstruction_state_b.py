from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "21_FINAL_REPORTS"


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    freeze = load_json("17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json")
    root = load_json("17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json")
    delivery = load_json("17_FINAL_FREEZE/R4_DELIVERY_20_OF_20_VERIFICATION.json")
    endpoint_audit = load_json("11_CERTIFICATES/R4_FINAL_ENDPOINT_INDEPENDENT_AUDIT_V2.json")
    mu_tr = load_json("18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_CERTIFICATE.json")
    mu = load_json("18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json")
    theory = load_json("18_Q24_CLOSURE/FINITE_QUOTIENT_THEORY_STATUS.json")
    resource = load_json("19_RESOURCE_CLOSURE/RESOURCE_STATUS.json")
    pilot = load_json("19_RESOURCE_CLOSURE/INTRALAYER_MATRIX_FREE_PILOT.json")
    workbook = load_json("20_POSTCONSTRUCTION/AUTHORITATIVE_WORKBOOK_CONSOLIDATED_UPDATE_AUDIT.json")
    processes = load_json("20_POSTCONSTRUCTION/POSTCONSTRUCTION_PROCESS_AUDIT.json")
    paper = load_json("PAPER_INTEGRATION_R4/PAPER_INTEGRATION_MANIFEST.json")
    factor = load_json("12_MINIMIZATION/CAND-R4-0005.factor_deletion.json")

    assert freeze["candidate_id"] == root["candidate_id"] == "CAND-R4-0005"
    assert freeze["exact_group_order"] == mu_tr["group"]["order"] == mu["group_order"] == 46080
    assert freeze["MATHEMATICAL_STATUS"] == "CERTIFIED"
    assert root["MATHEMATICAL_STATUS"] == "PASS"
    assert root["H_MATH"] == mu_tr["H_MATH"] == mu["H_MATH"]
    assert freeze["audit_results"]["final_independent_audit"] == "30/30 PASS"
    assert endpoint_audit["passed"] == 30 and endpoint_audit["failed"] == 0
    assert delivery["verified_artifacts"] == 20 and delivery["failed_artifacts"] == 0
    assert mu["mu"] == 92 and mu_tr["mu_tr"] == 5120
    assert theory["q24_RELATION"] == "RESOLVED_BRANCH_A" and theory["Q_NOT_IN_DEGREE24_DOMAIN"] is True
    assert resource["classification"] == "STATE_B_RESOURCE_UNVERIFIED_MISSING_SPECIFICATION"
    assert resource["RESOURCE_STATUS"] == "UNVERIFIED"
    assert resource["production_mode"] == "UNSPECIFIED"
    assert pilot["Hilbert_dimension"] == 92160
    assert workbook["classification"] == "PASS_SINGLE_CONSOLIDATED_VERSIONED_UPDATE"
    assert paper["classification"] == "PASS_STANDALONE_INTEGRATION_PACKAGE"
    assert processes["background_R4_process_count"] == 0
    assert processes["background_legacy_enumeration_process_count"] == 0
    assert processes["background_GAP_process_count"] == 0

    p64, p128 = pilot["results"]
    missing_groups = [
        "production mode",
        "production execution target/hardware",
        "precision and operator-storage policy",
        "eigensolver contract",
        "remaining numerical tolerances/tails",
        "production schedule and concurrency",
        "runtime budgets/storage/checkpoint policy",
        "stochastic-estimator selection and seeds",
        "Euclidean-control inclusion",
    ]

    items = [
        (1, "Candidate ID", "CAND-R4-0005"),
        (2, "Exact group order", "|Q| = 46,080"),
        (3, "Mathematical root hash", root["H_MATH"]),
        (4, "C8 status", "PASS — exact order-eight descended automorphism"),
        (5, "Parity status", "PASS — canonical parity character descends"),
        (6, "Physical-shell status", "PASS — eight-direction shell descends injectively"),
        (7, "Local-injectivity status", "PASS — declared B3/local gate"),
        (8, "Global-systole status", "PASS — sys(H^2/K_*)/a_B > 6; hence r_inj/a_B > 3"),
        (9, "Primary global scan count/result", "785,639,753 / 785,639,753; COMPLETE_NO_HIT; 0 kernel hits"),
        (10, "Independent global scan count/result", "785,639,753 / 785,639,753; COMPLETE_NO_HIT; 0 kernel hits"),
        (11, "Final audit result", "30 / 30 PASS"),
        (12, "Delivery-hash result", "20 / 20 PASS"),
        (13, "mu(Q), exact", "92 (faithful, possibly intransitive; certified orbit sizes 80, 2, 2, 4, 4)"),
        (14, "mu_tr(Q), exact", "5,120 (core-free stabilizer witness C3 x C3 of order 9; all indices 1..5,119 excluded)"),
        (15, "q24 relationship", "RESOLVED_BRANCH_A — Q_NOT_IN_DEGREE24_DOMAIN = TRUE"),
        (16, "Whether old q24 should have contained the successful marked quotient", "NO"),
        (17, "If yes, exact historical reason it was missed", "NOT APPLICABLE — no faithful transitive degree-24 action exists because mu_tr(Q)=5,120>24"),
        (18, "Resource-contract completeness", "INCOMPLETE / UNVERIFIED — 38 audited rows; 22 missing project-decision rows; 1 implementation-dependent open row"),
        (19, "Missing resource fields", "; ".join(missing_groups) + "; implementation must still compute exact m_perp(theta,D_c)"),
        (20, "Hilbert dimension", "N = 2|Q| = 92,160"),
        (21, "Matrix-free pilot result", (
            "PASS_SAFE_BOUNDED_INTRALAYER_ONLY_PILOT — N=92,160, 737,280 directed intralayer entries, 9 repetitions; "
            f"complex64 median={p64['median_seconds']:.7f} s, peak RSS={p64['peak_process_rss_bytes']:,} B; "
            f"complex128 median={p128['median_seconds']:.7f} s, peak RSS={p128['peak_process_rss_bytes']:,} B; "
            "not a full interlayer/Krylov/KPM/production bound"
        )),
        (22, "Resource Gate", "UNVERIFIED (missing authoritative specification; not FAIL)"),
        (23, "Production mode", "UNSPECIFIED — authoritative sources define FULL-SPACE and REPRESENTATION-RESOLVED but select neither"),
        (24, "Representation completeness status", "UNVERIFIED / NOT RUN, pending an authoritative production-mode selection"),
        (25, "A1 status", "NOT_FROZEN"),
        (26, "HPC status", "NOT_TRIGGERED_FOR_PRODUCTION_RESOURCE_GATE — production task is not fully specified; bounded local pilot did not exhaust resources"),
        (27, "Order optimality status", "UNPROVED; uniqueness and global classification also UNPROVED"),
        (28, "Factor-irredundancy status", "PASS within the declared two-factor factorization only: deleting p=2 leaves order 720 with parity FAIL/B3=337; deleting p=3 leaves order 64 with B3=55"),
        (29, "Paper integration package status", f"COMPLETE — standalone package, {len(paper['files'])} payload files plus manifest; locked main manuscript not modified"),
        (30, "Authoritative workbook update status", f"{workbook['classification']} — versioned output SHA256 {workbook['output_sha256']}; frozen source unchanged"),
        (31, "Background R4 process count", str(processes["background_R4_process_count"])),
        (32, "Background legacy enumeration process count", str(processes["background_legacy_enumeration_process_count"])),
    ]
    assert [number for number, _, _ in items] == list(range(1, 33))

    generated_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    state = {
        "schema_version": "1.0",
        "phase": "POST_CONSTRUCTION_CLOSURE",
        "acceptance_state": "STATE_B",
        "candidate_id": "CAND-R4-0005",
        "H_MATH": root["H_MATH"],
        "MATHEMATICAL_STATUS": "PASS",
        "FINITE_QUOTIENT_THEORY_STATUS": "CLOSED",
        "q24_RELATION": "RESOLVED_BRANCH_A",
        "RESOURCE_STATUS": "UNVERIFIED",
        "PRODUCTION_A1_STATUS": "NOT_FROZEN",
        "HPC_STATUS": resource["HPC_status"],
        "full_physics_production_started": False,
        "stop_reason": "authoritative resource parameters remain missing",
        "required_next_input": "19_RESOURCE_CLOSURE/A1_RESOURCE_INPUT_REQUEST.md",
        "generated_at": generated_at,
    }

    report_json = {
        "schema_version": "1.0",
        "title": "CAND-R4-0005 Post-Construction Final Report",
        "acceptance_state": "STATE_B",
        "generated_at": generated_at,
        "items": [
            {"number": number, "field": field, "value": value}
            for number, field, value in items
        ],
    }

    md_lines = [
        "# CAND-R4-0005 Post-Construction Final Report",
        "",
        "Acceptance state: **STATE B**.",
        "",
    ]
    for number, field, value in items:
        md_lines.append(f"{number}. **{field}:** {value}")
        md_lines.append("")

    report_md = OUT / "POSTCONSTRUCTION_FINAL_REPORT.md"
    report_js = OUT / "POSTCONSTRUCTION_FINAL_REPORT.json"
    state_js = OUT / "POSTCONSTRUCTION_STATE.json"
    report_md.write_text("\n".join(md_lines), encoding="utf-8", newline="\n")
    report_js.write_text(json.dumps(report_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    state_js.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({
        "classification": "STATE_B_POSTCONSTRUCTION_REPORT_COMPLETE",
        "items": len(items),
        "report_md_sha256": sha256(report_md),
        "report_json_sha256": sha256(report_js),
        "state_sha256": sha256(state_js),
    }, indent=2))


if __name__ == "__main__":
    main()
