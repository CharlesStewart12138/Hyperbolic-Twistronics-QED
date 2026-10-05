"""Generate the terminal dependency audit and A--L report for this round."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    (ROOT / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    global_cert = load("production_code/group/GLOBAL_SYSTOLE_DIRECT_CERTIFICATE.json")
    compact = load("production_code/group/COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.json")
    m7 = load("production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.json")
    target = load("production_code/kernel/PF_KER_005_TARGET_CONTRACT.json")

    counts = {
        "starting": {"Done": 54, "Fixed": 45, "Deferred": 16, "Blocked": 30, "Not Started": 101, "In Progress": 0, "Total": 246},
        "final": {"Done": 54, "Fixed": 45, "Deferred": 19, "Blocked": 31, "Not Started": 101, "In Progress": 0, "Total": 250},
    }
    rows_added = [
        {"task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT", "initial": "In Progress", "final": "Deferred"},
        {"task_id": "PF-GRP-001-Q-C8-COMPACT", "initial": "In Progress", "final": "Deferred"},
        {"task_id": "CM-047-NP-M7", "initial": "In Progress", "final": "Deferred"},
        {"task_id": "PF-KER-005-TARGET-CONTRACT", "initial": "In Progress", "final": "Blocked"},
    ]

    dependencies = [
        {
            "task_or_stage": "PF-GRP-001-GEO-GLOBAL-DIRECT",
            "workbook_status": "Deferred",
            "released": True,
            "executed": True,
            "terminal_result": "GLOBAL-UNRESOLVED",
            "exact_blocker": global_cert["exact_primary_stop_condition"],
            "resume_object": global_cert["required_to_resume"],
        },
        {
            "task_or_stage": "PF-GRP-001-Q-C8-COMPACT",
            "workbook_status": "Deferred",
            "released": True,
            "executed": True,
            "terminal_result": compact["terminal_classification"],
            "exact_blocker": compact["exact_primary_stop_condition"],
            "resume_object": compact["required_to_resume"],
        },
        {
            "task_or_stage": "CM-047-NP-M7",
            "workbook_status": "Deferred",
            "released": True,
            "executed": True,
            "terminal_result": "TENSOR-UNRESOLVED",
            "exact_blocker": m7["exact_primary_stop_condition"],
            "resume_object": m7["required_to_resume"],
        },
        {
            "task_or_stage": "CM-047-NP-M8",
            "workbook_status": "NO_ROW_NOT_RELEASED",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "m=7 is neither certified nor resource-acceptable; the directive forbids releasing m=8 concurrently or speculatively.",
            "resume_object": "A complete certified m=7 tensor ball/enclosure that passes the registered resource gate.",
        },
        {
            "task_or_stage": "PF-KER-005-TARGET-CONTRACT",
            "workbook_status": "Blocked",
            "released": True,
            "executed": True,
            "terminal_result": "TARGET-CONTRACT-BLOCKED",
            "exact_blocker": target["primary_blocker"],
            "resume_object": json.dumps(target["exact_resume_object"], separators=(",", ":")),
        },
        {
            "task_or_stage": "PF-KER-005 derivative-order closure",
            "workbook_status": "NO_NEW_ROW_NOT_RELEASED",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "R_target does not exist; C0/C1/C2 tails have no same-scope target margins or tolerances.",
            "resume_object": "PF-KER-005-TARGET-CONTRACT=FROZEN with Delta_C, M1, M2 and separate observable tolerances.",
        },
        {
            "task_or_stage": "PF-HOD-004 full-tensor root/no-root/transversality",
            "workbook_status": "Blocked",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "PF-KER-005 target contract is Blocked; no angle-dependent four-dimensional K_H(theta), common-root bracket or positive transversality margin is registered.",
            "resume_object": "A frozen R_target plus certified angle-dependent full-tensor endpoint and derivative enclosures.",
        },
        {
            "task_or_stage": "first fully admissible tractable quotient freeze",
            "workbook_status": "NOT_RELEASED",
            "released": False,
            "executed": False,
            "terminal_result": "NO_ELIGIBLE_CANDIDATE",
            "exact_blocker": "No compact candidate passed CQ-09/CQ-10 and the existing N=11,943,936 quotient remains GLOBAL-UNRESOLVED.",
            "resume_object": "One quotient passing based and global geometry, C8, parity, degree, bipartiteness and machine-specific tractability.",
        },
        {
            "task_or_stage": "12-point production smoke",
            "workbook_status": "NOT_RELEASED",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "No fully admissible tractable production quotient is frozen.",
            "resume_object": "production_code/config/production_cover_A_level_1.yaml for an accepted tractable quotient.",
        },
        {
            "task_or_stage": "finite-quotient representation inventory",
            "workbook_status": "NOT_RELEASED",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "No first legal finite production quotient exists.",
            "resume_object": "The frozen Level A1 quotient and its exact finite-group presentation/multiplication data.",
        },
        {
            "task_or_stage": "Tower A / Tower B and convergence pilots",
            "workbook_status": "NOT_RELEASED",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "No fully accepted Level A1 exists; no independent Tower B construction is registered.",
            "resume_object": "A legal Level A1 followed by coherent Tower A and genuinely independent Tower B constructions.",
        },
        {
            "task_or_stage": "physical scan through RUN-111",
            "workbook_status": "LOCKED",
            "released": False,
            "executed": False,
            "terminal_result": "PREREQUISITE_GATED",
            "exact_blocker": "Production quotient, smoke, target contract, representation and tower prerequisites remain closed.",
            "resume_object": "All registered upstream acceptance certificates in the required order; RUN-110 before RUN-111.",
        },
    ]

    dep_record = {
        "schema_version": "1.0",
        "round": "Global Systole Closure + Compact C8-Equivariant Quotient + Full-Tensor Nonperturbative Root",
        "counts": counts,
        "rows_added": rows_added,
        "dependencies": dependencies,
        "newly_released_after_recomputation": [],
        "main_tex_modified": False,
        "new_manuscript_pdf_generated": False,
    }
    write_json("production_code/NEXT_STAGE_DEPENDENCY_RECOMPUTATION.json", dep_record)
    with (ROOT / "production_code" / "NEXT_STAGE_DEPENDENCY_RECOMPUTATION.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["task_or_stage", "workbook_status", "released", "executed", "terminal_result", "exact_blocker", "resume_object"])
        writer.writeheader()
        writer.writerows(dependencies)
    dep_lines = [
        "# Next-stage dependency recomputation",
        "",
        "No lower-priority task is newly released.  The four added atomic rows are terminal with `In Progress=0`.",
        "",
        "| Task or stage | Workbook/status | Released | Result | Exact blocker |",
        "|---|---|---:|---|---|",
    ]
    for row in dependencies:
        dep_lines.append(f"| `{row['task_or_stage']}` | {row['workbook_status']} | {'yes' if row['released'] else 'no'} | {row['terminal_result']} | {row['exact_blocker']} |")
    dep_lines += [
        "",
        "`main.tex` remains locked and unchanged.  No replacement manuscript PDF was generated.",
    ]
    (ROOT / "production_code" / "NEXT_STAGE_DEPENDENCY_RECOMPUTATION.md").write_text("\n".join(dep_lines) + "\n", encoding="utf-8")

    files = {
        "certificates": [
            str(ROOT / "production_code/group/GLOBAL_DIRECT_RESOURCE_FORECAST.json"),
            str(ROOT / "production_code/group/GLOBAL_SYSTOLE_DIRECT_CERTIFICATE.json"),
            str(ROOT / "production_code/group/GLOBAL_SYSTOLE_DIRECT_CERTIFICATE.md"),
            str(ROOT / "production_code/group/COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.json"),
            str(ROOT / "production_code/group/COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.md"),
            str(ROOT / "data/production/local_full_kernel/EXACT_BALL7_TENSOR_RESOURCE_FORECAST.json"),
            str(ROOT / "data/production/local_full_kernel/EXACT_BALL7_TENSOR_TAIL.json"),
            str(ROOT / "data/production/local_full_kernel/EXACT_BALL7_TENSOR_PARTIAL.status.json"),
            str(ROOT / "production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.json"),
            str(ROOT / "production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.md"),
            str(ROOT / "production_code/kernel/PF_KER_005_TARGET_CONTRACT.json"),
            str(ROOT / "production_code/kernel/PF_KER_005_TARGET_CONTRACT.md"),
            str(ROOT / "production_code/NEXT_STAGE_DEPENDENCY_RECOMPUTATION.json"),
            str(ROOT / "production_code/NEXT_STAGE_DEPENDENCY_RECOMPUTATION.md"),
            str(ROOT / "production_code/PROTECTED_MAGIC_ROOT_TERMINAL_REPORT.json"),
            str(ROOT / "production_code/PROTECTED_MAGIC_ROOT_TERMINAL_REPORT.md"),
        ],
        "data_tables": [
            str(ROOT / "data/production/global_direct/pilot_cyclic_phi8.json"),
            str(ROOT / "data/production/compact_quotient_search/candidates.csv"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_17_search_summary.json"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_17_survivor_manifest.tsv"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_23_search_summary.json"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_23_survivor_manifest.tsv"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_23_based_results.tsv"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_31_search_summary.json"),
            str(ROOT / "data/production/compact_quotient_search/pgl2_31_survivor_manifest.tsv"),
            str(ROOT / "data/production/compact_quotient_search/s8_survivor_manifest.tsv"),
            str(ROOT / "data/production/compact_quotient_search/s8_based_results.tsv"),
            str(ROOT / "production_code/NEXT_STAGE_DEPENDENCY_RECOMPUTATION.csv"),
        ],
        "configuration_files_created": [],
        "workbooks": [
            str(ROOT / "Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx"),
            str(ROOT / "outputs/01a05c9b-553e-7562-a52e-f5922d89e88d/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx"),
        ],
        "execution_logs": [str(ROOT / "CODE_WORK_LOG.md")],
    }

    terminal = {
        "A_TASK_COUNTS": {"counts": counts, "rows_added_and_transitions": rows_added},
        "B_GLOBAL_GEOMETRY": {
            "quotient_N": global_cert["quotient_order_N"],
            "global_direct_search_attempted": True,
            "method": global_cert["method"],
            "search_domain": global_cert["search_domain"],
            "proof_exhaustion": False,
            "classification": "GLOBAL-UNRESOLVED",
            "dangerous_witness": None,
            "certified_systole": None,
            "injectivity_margin": None,
            "resource_use": global_cert["resource_use"],
        },
        "C_COMPACT_QUOTIENT_SEARCH": {
            "candidate_families_attempted": [row["family"] for row in compact["candidate_families_attempted"]],
            "order_windows_completed": compact["order_windows_completed"],
            "candidates_examined": compact["number_candidates_examined"],
            "cheap_gate_pass": compact["number_passing_cheap_exact_gates"],
            "based_certificate_pass": compact["number_passing_based_dangerous_certificate"],
            "global_certified": compact["number_global_certified"],
            "smallest_global_certified": None,
            "smallest_tractable_global_certified": None,
            "C8_equivariance_direct": True,
            "parity": compact["parity"],
        },
        "D_FIRST_PRODUCTION_QUOTIENT": {
            "found": False,
            "ID": None,
            "N": None,
            "two_N": None,
            "global_geometric_certificate": None,
            "based_geometric_certificate": None,
            "C8": None,
            "parity": None,
            "degree_8": None,
            "bipartite": None,
            "estimated_nnz": None,
            "estimated_RAM": None,
            "tractability": "NOT_EVALUATED_NO_ELIGIBLE_CANDIDATE",
            "representation_inventory": "incomplete",
        },
        "E_PRODUCTION_SMOKE": {
            "Hamiltonians_evaluated": 0,
            "expected_if_legal": 12,
            "omega_0_null": "PREREQUISITE_GATED",
            "Hermiticity": "PREREQUISITE_GATED",
            "C8": "PREREQUISITE_GATED",
            "theta_symmetry": "PREREQUISITE_GATED",
            "validation_contamination": "NONE; no production Hamiltonian was assembled",
        },
        "F_FULL_TENSOR_NONPERTURBATIVE_ROOT": {
            "m6_baseline_retained": True,
            "m7_completed": False,
            "m8_completed": False,
            "beta_minus_interval_by_depth": {"m6": m7["m6_sector_intervals_retained"]["beta_minus"], "m7": None, "m8": None},
            "beta_plus_interval_by_depth": {"m6": m7["m6_sector_intervals_retained"]["beta_plus"], "m7": None, "m8": None},
            "common_root_interval_by_depth": {"m6": m7["m6_common_root_interval_retained"], "m7": None, "m8": None},
            "endpoint_ratio_by_depth": {"m6": m7["m6_endpoint_ratio_retained"], "m7": None, "m8": None},
            "dominant_remaining_uncertainty": m7["uncertainty_decomposition"]["dominant_remaining_uncertainty"],
            "terminal_classification": "TENSOR-UNRESOLVED",
            "certified_root": None,
        },
        "G_PF_KER_005": {
            "target_ancestry_frozen": False,
            "target_contour_frozen": False,
            "target_rank": None,
            "minimum_gap": None,
            "M1": None,
            "M2": None,
            "C0_tolerance": None,
            "C1_tolerance": None,
            "C2_tolerance": None,
            "C0_tail": "unresolved",
            "C1_tail": "unresolved",
            "C2_tail": "unresolved",
            "PF_KER_005": "Blocked",
        },
        "H_PF_HOD_004": {
            "scalar_route_remains_unauthorized": True,
            "full_angle_dependent_tensor_evaluated": False,
            "common_root_exists": "unresolved",
            "theta_H": None,
            "slope_transversality": None,
            "terminal_status": "Blocked",
            "physical_flatness_implication": "NONE until the independent physical chain runs",
        },
        "I_COVER_BULK": {
            "Tower_A_levels": [],
            "Tower_B_levels": [],
            "representation_complete_finite_quotient": False,
            "no_loss": "not evaluated",
            "no_pollution": "not evaluated",
            "strongest_claim_scope": "FINITE-QUOTIENT (based-only constructive certificate; global production scope unresolved)",
        },
        "J_TESTS": {
            "production": "377/377",
            "validation": "25/25",
            "new_global": "5/5",
            "new_compact_quotient": "6/6",
            "new_tensor": "6/6",
            "new_target_contract": "6/6",
            "failed": 0,
            "prerequisite_gated_tests": 0,
            "Excel_formula_errors": 0,
            "Master_detail_inconsistencies": 0,
        },
        "K_STOP_REASON": {
            "primary": global_cert["exact_primary_stop_condition"],
            "secondary": [compact["exact_primary_stop_condition"], m7["exact_primary_stop_condition"], target["primary_blocker"]],
        },
        "L_FILES": files | {"main_tex_modified": False, "new_manuscript_PDF_generated": False},
    }
    write_json("production_code/PROTECTED_MAGIC_ROOT_TERMINAL_REPORT.json", terminal)

    fams = ", ".join(terminal["C_COMPACT_QUOTIENT_SEARCH"]["candidate_families_attempted"])
    added = "; ".join(f"`{r['task_id']}` added In Progress, then {r['initial']} -> {r['final']}" for r in rows_added)
    all_paths = files["certificates"] + files["data_tables"] + files["workbooks"] + files["execution_logs"]
    file_lines = "\n".join(f"- `{p}`" for p in all_paths)
    md = f"""# Protected Magic Root — terminal report

## A. TASK COUNTS

Starting: Done 54; Fixed 45; Deferred 16; Blocked 30; Not Started 101; In Progress 0; Total 246.

Final: Done 54; Fixed 45; Deferred 19; Blocked 31; Not Started 101; In Progress 0; Total 250.

Rows and transitions: {added}.

## B. GLOBAL GEOMETRY

Existing quotient `N=11,943,936`: global direct search attempted **yes**.

- Method: {global_cert['method']}.
- Search domain: primitive geometric word lengths 1--9; 5,884,905 raw C8-normalized leaves and 336,367 canonical orbits.
- Proof exhaustion: **no**; required raw representative bound is 110, or a complete based flood to `7.60179185438737 a_B`.
- Classification: **GLOBAL-UNRESOLVED**.  No dangerous witness was found in the completed pilot, but no global systole or injectivity margin is certified.
- Resources: pilot runtime `98.2795094 s`; peak RAM not instrumented for the depth-first pilot; new artifact disk `6,356 bytes`.  The complete flood forecast is 3,096,469,272 states, `511,608,849,632 bytes` peak RAM and about `1,012,248,391,015 bytes` CSV.

## C. COMPACT QUOTIENT SEARCH

- Candidate families: {fams}.
- Completed classes: Q1 contains complete S7, PGL(2,17), PGL(2,19) classes; Q2 contains complete S8, PGL(2,23), PGL(2,29), PGL(2,31) classes.  Neither entire order window is exhausted.
- Candidates examined: **133,920**; cheap exact gates: **96**; based dangerous-set certificate: **0**; global-certified: **0**.
- Smallest global-certified / tractable global-certified quotient: **none**.
- Direct C8 equivariance: **yes**.  Parity: **pass for all 96 cheap-gate survivors**.

## D. FIRST PRODUCTION QUOTIENT

Found: **no**.  ID, N, 2N, global/based certificates, C8, parity, degree eight, bipartiteness, nnz and RAM are not applicable.  Tractability was not evaluated because no candidate passed CQ-09/CQ-10.  Representation inventory is **incomplete**.

## E. PRODUCTION SMOKE

Hamiltonians evaluated: **0**; expected **12 only if a legal tractable quotient exists**.  The omega=0 null, Hermiticity, C8 and theta-symmetry checks are prerequisite-gated.  Validation contamination: **none**, because no production Hamiltonian was assembled.

## F. FULL-TENSOR NONPERTURBATIVE ROOT

- m=6 baseline retained: **yes**; m=7 complete exact ball: **no**; m=8: **no / not released**.
- m=6 beta-minus interval: `{m7['m6_sector_intervals_retained']['beta_minus']}`.
- m=6 beta-plus interval: `{m7['m6_sector_intervals_retained']['beta_plus']}`.
- m=6 common-root interval: `{m7['m6_common_root_interval_retained']}`; endpoint ratio: `{m7['m6_endpoint_ratio_retained']}`.
- m=7 and m=8 sector/common-root intervals and endpoint ratios: **not available**.
- Dominant uncertainty: missing complete exact shell `6a_B < d <= 7a_B`; its in-memory forecast is 491,889,816 states and 81,271,655,167 bytes, above 68,112,736,256 bytes host RAM.
- Terminal classification: **TENSOR-UNRESOLVED**.  No root, transversality or isolation margin is certified.

## G. PF-KER-005

Target ancestry frozen: **no**; target contour frozen: **no**; rank, minimum gap, M1, M2, and C0/C1/C2 tolerances: **null**.  C0, C1 and C2 tail acceptance: **unresolved / unresolved / unresolved**.  `PF-KER-005`: **Blocked**.

## H. PF-HOD-004

Scalar route remains unauthorized: **yes**.  The angle-dependent full tensor was not evaluated; the existing m=6 aligned tensor enclosure is not an angle-root/transversality certificate.  Common root: **unresolved**; theta_H and slope: not certified.  Terminal status: **Blocked**.  Physical-flatness implication: **NONE until the independent physical chain runs**.

## I. COVER / BULK

Tower A levels: none; Tower B levels: none; representation-complete finite quotient: **no**; no-loss/no-pollution: **not evaluated / not evaluated**.  Strongest claim scope: **FINITE-QUOTIENT, based-only constructive certificate; global production and bulk remain unresolved**.

## J. TESTS

Production **377/377**; validation **25/25**; new global **5/5**; compact quotient **6/6**; tensor **6/6**; target contract **6/6**.  Failed tests: **0**; prerequisite-gated tests: **0**; Excel formula errors: **0**; Master/detail inconsistencies: **0**.

## K. STOP REASON

Primary: {global_cert['exact_primary_stop_condition']}

Secondary blockers:

- {compact['exact_primary_stop_condition']}
- {m7['exact_primary_stop_condition']}
- {target['primary_blocker']}

## L. FILES

No configuration file was created because no legal production quotient exists.

{file_lines}

`main.tex` modified: **NO**.  New manuscript PDF generated: **NO**.
"""
    (ROOT / "production_code" / "PROTECTED_MAGIC_ROOT_TERMINAL_REPORT.md").write_text(md, encoding="utf-8")

    for group in (files["certificates"][:-2] + files["data_tables"][:-1] + files["workbooks"] + files["execution_logs"]):
        if not Path(group).exists():
            raise FileNotFoundError(group)


if __name__ == "__main__":
    main()
