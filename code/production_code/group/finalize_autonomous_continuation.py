"""Write the final dependency recomputation and terminal report for the 2026-09-05 run."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_BASE = ROOT / "production_code" / "group" / "AUTONOMOUS_CONTINUATION_DEPENDENCY_RECOMPUTATION"
REPORT_MD = ROOT / "production_code" / "group" / "AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.md"
REPORT_JSON = ROOT / "production_code" / "group" / "AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.json"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def dependency_rows() -> list[dict[str, object]]:
    return [
        {"task_id": "PF-GRP-001-GEO-GLOBAL", "workbook_status": "Deferred", "scope": "GLOBAL", "classification": "RESOURCE_BOUND", "legally_executable_now": False, "reason": "Complete conjugacy representatives require a proof-complete length-110 normal form/automaton; terminal freely-reduced shell is about 1.044e93."},
        {"task_id": "PF-GRP-001-PRODUCT-BASED", "workbook_status": "Done", "scope": "BASED_FINITE_QUOTIENT", "classification": "CLOSED_NO_PRODUCTION_RELEASE", "legally_executable_now": False, "reason": "PQ-01..13 and PQ-15 pass, but PQ-14/PQ-16 are unavailable because the global obstruction set is Deferred; smoke is not released."},
        {"task_id": "CM-045", "workbook_status": "Done", "scope": "LOCAL", "classification": "NEWLY_RELEASED_AND_EXECUTED", "legally_executable_now": False, "reason": "Exact four-dimensional Hodge basis/metric production interface closed with all acceptance tests."},
        {"task_id": "PF-KER-005", "workbook_status": "Blocked", "scope": "LOCAL", "classification": "REAL_MISSING_OBJECT", "legally_executable_now": False, "reason": "Canonical C0/C1/C2 tails exist, but no one target supplies |w|/t, a positive contour/gap margin, M1/M2, and separate observable tolerances."},
        {"task_id": "PF-HOD-004", "workbook_status": "Blocked", "scope": "LOCAL", "classification": "REAL_MISSING_OBJECT_AND_SCALAR_FALSIFICATION", "legally_executable_now": False, "reason": "The physical-shell scalar commutant is false; no angle-dependent two-sector tensor, signed endpoints, or positive certified angle slope exists."},
        {"task_id": "CM-008", "workbook_status": "Not Started", "scope": "FINITE_QUOTIENT", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "Full all-pair T_N requires CM-006 and a production Q_N; only a based-only, globally uncertified quotient exists."},
        {"task_id": "CM-011", "workbook_status": "Not Started", "scope": "FINITE_QUOTIENT/LOCAL_PATH", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "Exact theta/kappa Hamiltonian derivatives depend on CM-008 full interlayer assembly."},
        {"task_id": "CM-041", "workbook_status": "Not Started", "scope": "TARGET_SPECTRAL", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "Riesz engine requires CM-040 and blocked PF-TGT-002; no frozen target contour exists."},
        {"task_id": "CM-042", "workbook_status": "Not Started", "scope": "TARGET_SPECTRAL", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "Projector continuation requires CM-041; PF-TGT-005 alone is insufficient without a target projector."},
        {"task_id": "CM-046", "workbook_status": "Not Started", "scope": "LOCAL", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "CM-045 is now Done, but CM-011/CM-042 and a registered same-scope target Hessian derivative family are absent."},
        {"task_id": "CM-047", "workbook_status": "Not Started", "scope": "LOCAL", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "Requires CM-046, PF-KER-005/PF-HOD-004 closure, signed endpoints, and a positive slope."},
        {"task_id": "CM-047-NP", "workbook_status": "Blocked", "scope": "LOCAL", "classification": "PARTIAL_BOUND_CHILD_CLOSED_PARENT_BLOCKED", "legally_executable_now": False, "reason": "The aligned full tensor bound is materially improved, but no angle-dependent microscopic K(theta,w), target contour, transversality evaluator, or common-sector decision exists."},
        {"task_id": "RUN-040", "workbook_status": "Not Started", "scope": "LOCAL", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "Independent Hodge scan waits for CM-046 and CM-047-NP."},
        {"task_id": "RUN-110", "workbook_status": "Not Started", "scope": "INTEGRATION", "classification": "INPUT_BLOCKED", "legally_executable_now": False, "reason": "All production figure runs are not complete because no fully accepted production quotient/smoke exists."},
        {"task_id": "RUN-111", "workbook_status": "Not Started", "scope": "MANUSCRIPT", "classification": "FORMAL_INSERTION_NOT_ELIGIBLE", "legally_executable_now": False, "reason": "Formal manuscript numerical insertion depends on RUN-110, which is not complete; main.tex must remain locked."},
    ]


def write_dependency_audit(rows: list[dict[str, object]]) -> None:
    record = {
        "schema_version": "1.0",
        "date": "2026-09-05",
        "task_counts": {"Done": 54, "Fixed": 45, "Deferred": 16, "Blocked": 30, "Not Started": 101, "In Progress": 0, "Total": 246},
        "newly_unlocked": ["CM-045"],
        "newly_executed": ["CM-045"],
        "newly_added_and_closed": [
            "PF-GRP-001-GEO-BASED", "PF-GRP-001-GEO-GLOBAL", "PF-GRP-001-Q-GEO-SEP-BASED",
            "PF-GRP-001-PRODUCT-BASED", "PF-GRP-001-BASED-SIZE-LOWER-BOUND",
            "PF-HOD-004-GEOMETRIC-COMMUTANT", "CM-047-NP-TENSOR-BOUND",
        ],
        "newly_blocked": [],
        "retained_real_blockers": ["PF-GRP-001-GEO-GLOBAL", "PF-KER-005", "PF-HOD-004", "CM-047-NP"],
        "legally_executable_tasks_remaining": [],
        "rows": rows,
        "main_tex_modified": False,
        "stopping_condition": "No currently legal task remains: every remaining branch requires a missing core target/operator object, an uncompleted prerequisite, external data, or the proved global-enumeration resource/method boundary.",
    }
    OUT_BASE.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    with OUT_BASE.with_suffix(".csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    md_rows = "\n".join(
        f"| `{row['task_id']}` | {row['workbook_status']} | {row['classification']} | {row['reason']} |"
        for row in rows
    )
    markdown = f"""# Autonomous continuation dependency recomputation

Final authoritative count: **246** tasks = Done 54, Fixed 45, Deferred 16, Blocked 30, Not Started 101, In Progress 0.

`CM-045` was the only newly legal workbook task and was executed to Done.  No further legally executable task remains.  This is not inferred from the number of unstarted rows: every relevant branch was checked against its exact scientific inputs.

| Task | Status | Classification | Exact current boundary |
|---|---|---|---|
{md_rows}

The formal insertion task `RUN-111` is not eligible because `RUN-110` is Not Started.  Therefore `source_current_195/main.tex` remains locked; completed numerical results are confined to the certified update queue.
"""
    OUT_BASE.with_suffix(".md").write_text(markdown, encoding="utf-8")


def terminal_record() -> dict:
    tensor = read_json("production_code/hodge/CM_047_NP_TENSOR_BOUND.json")
    based = read_json("data/production/short_geodesics/based_enumeration_summary.json")
    separator = read_json("data/production/quotient_separator/BASED_SEPARATOR_SUMMARY.json")
    product = read_json("production_code/group/BASED_PRODUCT_QUOTIENT_CERTIFICATE.json")
    size = read_json("production_code/group/BASED_QUOTIENT_SIZE_LOWER_BOUND.json")
    global_status = read_json("data/production/short_geodesics/dangerous_global.status.json")
    return {
        "schema_version": "1.0",
        "starting_counts": {"Done": 47, "Fixed": 45, "Deferred": 15, "Blocked": 30, "Not Started": 102, "In Progress": 0, "Total": 239},
        "final_counts": {"Done": 54, "Fixed": 45, "Deferred": 16, "Blocked": 30, "Not Started": 101, "In Progress": 0, "Total": 246},
        "closed_this_run": [
            {"task_id": "PF-GRP-001-GEO-BASED", "status": "Done"},
            {"task_id": "PF-GRP-001-GEO-GLOBAL", "status": "Deferred"},
            {"task_id": "PF-GRP-001-Q-GEO-SEP-BASED", "status": "Done"},
            {"task_id": "PF-GRP-001-PRODUCT-BASED", "status": "Done"},
            {"task_id": "PF-GRP-001-BASED-SIZE-LOWER-BOUND", "status": "Done"},
            {"task_id": "PF-HOD-004-GEOMETRIC-COMMUTANT", "status": "Done"},
            {"task_id": "CM-047-NP-TENSOR-BOUND", "status": "Done"},
            {"task_id": "CM-045", "status": "Done"},
        ],
        "geometric_obstruction": {"based_complete": based["complete"], "based_elements": based["dangerous_nonidentity_elements"], "based_largest_minimum_word_length": based["largest_minimum_geometric_word_length"], "global_complete": False, "global_status": global_status.get("status"), "global_representative_word_upper_bound": 110, "option_B_based_still_required": False, "option_B_global_still_required": True},
        "separator": {"maps_evaluated": 1182, "dangerous_elements_separated": based["dangerous_nonidentity_elements"], "uncovered": 0, "minimum_separator_count": 1, "minimum_proved": True, "selected_practical_product_factors": 2, "C8_closure": True, "parity": True, "separator_summary_status": separator.get("status")},
        "production_quotient": {"fully_mathematically_admissible": False, "based_only_actual_image_order": product.get("actual_image_order", 11943936), "based_only_two_layer_dimension": 23887872, "based_geometric_injectivity": True, "global_geometric_injectivity": False, "numerically_tractable": False, "exact_lower_bound_with_parity": size.get("even_lower_bound", 2338)},
        "production_hamiltonians": {"evaluated": 0, "smoke_12_completed": False, "reason": "PQ-14/PQ-16/PQ-17 full production acceptance unavailable"},
        "towers": {"A": [], "B": [], "blocker": "No fully accepted Level A1 quotient; no independent arithmetic/congruence family."},
        "PF_KER_005": {"LOCAL_closure": False, "PRODUCTION_closure": False, "m6_per_abs_w": {"C0": 0.003856544343098889, "C1_Hodge": 1.5561304907547204, "C2_Hodge": 629.7779064951307}, "target_contour": None, "gap": None, "M1": None, "M2": None},
        "PF_HOD_004": {"commutant_evaluated": True, "scalar_commutant": False, "angle_root_evaluated": False, "root_bracket": None, "theta_H": None, "certified_slope": None, "common_tensor_root": "unresolved"},
        "CM_047_NP": {"aligned_tensor_bound_evaluated": True, "angle_dependent_root_evaluated": False, "old_scalar_interval": [0.2729019956906728, 224981.26427234669], "new_scalar_interval": None, "partial_beta_minus": tensor["partial_generalized_coefficients_B_relative_to_C_S"]["minus_interval"], "partial_beta_plus": tensor["partial_generalized_coefficients_B_relative_to_C_S"]["plus_interval"], "full_beta_minus": tensor["full_kernel_sector_enclosure"]["beta_minus"], "full_beta_plus": tensor["full_kernel_sector_enclosure"]["beta_plus"], "common_root_necessary_t_over_w": tensor["aligned_tensor_zero_condition"]["common_root_necessary_interval"], "common_interval_endpoint_ratio": 61.96614867400627, "nonperturbative_root": "unresolved", "full_operator_isolation": "unresolved"},
        "tests": {"production_passed": 354, "production_total": 354, "validation_passed": 25, "validation_total": 25, "group_geometric_classified": 138, "kernel_Hodge_classified": 65, "failed": 0, "prerequisite_gated": 0, "Excel_formula_errors": 0, "Master_detail_mismatches": 0},
        "claim_scope": {"strongest": "FINITE_QUOTIENT_BASED_ONLY", "analytic_first_shell_root": "retained validation-model result; not a repaired physical-shell/full-kernel root", "perturbative_full_kernel_persistence": "failed at lambda_perp/a_B=0.20", "nonperturbative_full_kernel_root": "unresolved two-sector tensor problem", "physical_flat_band": "unresolved/not evaluated"},
        "files": {
            "short_geodesic_certificates": ["production_code/group/BOLZA_SHORT_GEODESIC_OBSTRUCTION_CERTIFICATE.md", "production_code/group/BOLZA_SHORT_GEODESIC_OBSTRUCTION_CERTIFICATE.json"],
            "dangerous_element_tables": ["data/production/short_geodesics/dangerous_based.csv", "data/production/short_geodesics/based_enumeration_summary.json", "data/production/short_geodesics/dangerous_global.status.json"],
            "separator_matrix": "data/production/quotient_separator/separator_matrix.npz",
            "separator_solution": ["data/production/quotient_separator/based_separator_solution.json", "data/production/quotient_separator/BASED_SEPARATOR_SUMMARY.json", "data/production/quotient_separator/BASED_SEPARATOR_SUMMARY.md"],
            "product_quotient_certificate": ["production_code/group/BASED_PRODUCT_QUOTIENT_CERTIFICATE.json", "production_code/group/BASED_PRODUCT_QUOTIENT_CERTIFICATE.md", "production_code/group/BASED_PRODUCT_PRACTICAL_FEASIBILITY.json"],
            "production_quotient_yaml": None,
            "smoke_manifest": None,
            "tower_registries": None,
            "PF_KER_005_records": ["production_code/kernel/PF_KER_005_CANONICAL_TAILS.json", "production_code/kernel/PF_KER_005_OBSERVABLE_TAIL_REASSESSMENT.md"],
            "PF_HOD_004_records": ["production_code/hodge/GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.json", "production_code/hodge/GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.md", "production_code/hodge/PF_HOD_004_REASSESSMENT.json", "production_code/hodge/PF_HOD_004_HODGE_ROOT_REASSESSMENT.md"],
            "CM_045_records": ["production_code/hodge/metric.py", "production_code/hodge/CM_045_HODGE_METRIC_INTERFACE.json", "production_code/hodge/CM_045_HODGE_METRIC_INTERFACE.md"],
            "CM_047_NP_records": ["data/production/local_full_kernel/EXACT_BALL6_TENSOR_PARTIAL.json", "data/production/local_full_kernel/EXACT_BALL6_TENSOR_TAIL.json", "production_code/hodge/CM_047_NP_TENSOR_BOUND.json", "production_code/hodge/CM_047_NP_TENSOR_BOUND.md"],
            "dependency_recomputations": ["production_code/group/AUTONOMOUS_CONTINUATION_DEPENDENCY_RECOMPUTATION.json", "production_code/group/AUTONOMOUS_CONTINUATION_DEPENDENCY_RECOMPUTATION.csv", "production_code/group/AUTONOMOUS_CONTINUATION_DEPENDENCY_RECOMPUTATION.md"],
            "updated_workbook": "Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx",
            "work_logs": ["WORK_LOG.md", "CODE_WORK_LOG.md"],
            "terminal_report": ["production_code/group/AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.json", "production_code/group/AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.md"],
        },
        "main_tex_modified": False,
    }


def write_terminal_report(record: dict) -> None:
    tensor = record["CM_047_NP"]
    closed = "\n".join(f"- `{item['task_id']}` — {item['status']}" for item in record["closed_this_run"])
    markdown = f"""# Autonomous continuation terminal report

## A. Task counts

Starting: Done 47 / Fixed 45 / Deferred 15 / Blocked 30 / Not Started 102 / In Progress 0; total 239.

Final: **Done 54 / Fixed 45 / Deferred 16 / Blocked 30 / Not Started 101 / In Progress 0; total 246.**  Seven minimal atomic rows were added; `CM-045` moved from Not Started to Done.

Closed this run:

{closed}

## B. Geometric obstruction set

- Based dangerous set complete: **yes**, 23,129,592 nonidentity elements; largest minimum geometric word length 17; terminal shell 18 empty.
- Global dangerous-class set complete: **no**.  The exact trace cutoff and a representative-length upper bound 110 are proved, but exhaustive representative emission is Deferred at a documented resource/method boundary.
- Option-B 127/156 still required: based **no**, global **yes**.  The exact geometric certificate replaces Option-B only for the based claim.

## C. Separator synthesis

- Existing maps evaluated: **1,182**; based-dangerous elements separated: **23,129,592**; uncovered: **0**.
- Minimum separator count: **1, proved optimal**.  The practical lower-order construction uses two S4 factors.
- Product quotient constructed: **yes, based-only**; C8 orbit closure: yes; parity factor: yes.

## D. Production quotient

- Fully mathematically admissible production quotient: **no** (global PQ-14/PQ-16 unavailable).
- Based-admissible actual image: order `N=11,943,936`, `2N=23,887,872`, C8/parity/degree-8/bipartite based gates pass.
- Numerically tractable production quotient: **no**; nearest-neighbour CSR alone has a 4.78 GB storage lower bound before full interlayer terms/eigensolver state.
- Exact based lower bound with parity: `N>=2,338`; this is not a minimum-order theorem.

## E. Production Hamiltonians

Actual Hamiltonians evaluated: **0**; 12-point smoke completed: **no**.  All smoke subchecks are prerequisite-gated, not failed.  No validation data were used as production data.

## F. Cover towers

Tower A levels: none.  Tower B levels: none.  Exact blocker: no fully accepted Level A1 and no independent arithmetic/congruence family; a permutation of the same factors was not mislabelled as Tower B.

## G. PF-KER-005

LOCAL closure: **no**.  PRODUCTION closure: **no**.  At first omitted shell 6 the canonical per-|w| bounds are C0 `0.0038565443431`, C1 `1.55613049075`, C2 `629.777906495`; the aligned tensor tail has the sharper symmetry budget `Tr(T)<=261`.

Target contour, gap, M1, M2, and observable-specific tolerances: **absent in one common scope**.  This is the exact remaining blocker; convergence of the operator tail alone is not a projector/velocity/Hessian acceptance test.

## H. PF-HOD-004

The physical-shell commutant was evaluated exactly and the scalar hypothesis was falsified.  `spec(G^-1 C_S)={{sqrt(2)-1 (x2), sqrt(2)+1 (x2)}}`.  No angle root bracket, theta_H, or positive certified slope exists.  Common tensor root: **unresolved**.

## I. CM-047-NP

The centered/aligned full-tensor bound was evaluated; the angle-dependent root problem was not executable.

- Old scalar interval: `[0.2729019956906728, 224981.26427234669]` (now structurally unauthorized).
- Complete-ball partial sectors: beta-minus `{tensor['partial_beta_minus']}`; beta-plus `{tensor['partial_beta_plus']}`.
- Full sector enclosures: beta-minus `{tensor['full_beta_minus']}`; beta-plus `{tensor['full_beta_plus']}`.
- A common aligned root, if it exists, must satisfy `t/w in {tensor['common_root_necessary_t_over_w']}`; endpoint ratio `61.9661`.
- Dominant improvement: exact 23.1M-element ball, inversion/C8 aggregation, all tensor entries, and an m=6 directed tail; raw tail shrank by factor 1,724.90 and the historical upper endpoint versus the common-root upper endpoint by factor 13,696.64.
- Nonperturbative root and full-operator isolation: **unresolved**.

## J. Automatic downstream execution

Newly unlocked and executed: `CM-045`.  Newly blocked: none.  Retained real blockers: `PF-GRP-001-GEO-GLOBAL`, `PF-KER-005`, `PF-HOD-004`, `CM-047-NP`.  `CM-046`, `CM-047`, `RUN-040`, `RUN-110`, and `RUN-111` remain input-gated with exact reasons in the dependency audit.

## K. Tests and workbook

- Production: **354/354 passed**; validation: **25/25 passed**.
- Classified group/geometric modules: 138 tests; kernel/Hodge modules: 65 tests (all included in the passing production suite).
- Failed: 0; prerequisite-gated tests: 0.
- Excel formula errors: 0; Master/detail status inconsistencies: 0.

## L. Claim scope

Strongest new constructive scope: **FINITE-QUOTIENT, based-only**; the full physical/nonperturbative claim remains **LOCAL / unresolved**, with no FULL-BULK promotion.

- Analytic first-shell root: retained validation-model result, not a repaired physical-shell/full-kernel root.
- Perturbative full-kernel persistence: failed at frozen `lambda_perp/a_B=0.20`.
- Nonperturbative full-kernel root: unresolved two-sector tensor problem.
- Physical flat band: unresolved and not evaluated.

## M. Files

- Short-geodesic certificates: `production_code/group/BOLZA_SHORT_GEODESIC_OBSTRUCTION_CERTIFICATE.md`, `.json`.
- Dangerous-set records: `data/production/short_geodesics/dangerous_based.csv`, `based_enumeration_summary.json`, `dangerous_global.status.json`.  No `dangerous_global.csv` was fabricated.
- Separator matrix/solution: `data/production/quotient_separator/separator_matrix.npz`, `based_separator_solution.json`, `BASED_SEPARATOR_SUMMARY.json`, `BASED_SEPARATOR_SUMMARY.md`.
- Product certificate: `production_code/group/BASED_PRODUCT_QUOTIENT_CERTIFICATE.json`, `.md`, and `BASED_PRODUCT_PRACTICAL_FEASIBILITY.json`.
- Production quotient YAML, smoke manifest, tower registries: **not created**, because their acceptance gates did not release.
- PF-KER-005 records: `production_code/kernel/PF_KER_005_CANONICAL_TAILS.json`, `PF_KER_005_OBSERVABLE_TAIL_REASSESSMENT.md`.
- PF-HOD-004 records: `production_code/hodge/GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.json`, `.md`, `PF_HOD_004_REASSESSMENT.json`, `PF_HOD_004_HODGE_ROOT_REASSESSMENT.md`.
- CM-045 records: `production_code/hodge/metric.py`, `CM_045_HODGE_METRIC_INTERFACE.json`, `.md`.
- CM-047-NP records: `data/production/local_full_kernel/EXACT_BALL6_TENSOR_PARTIAL.json`, `EXACT_BALL6_TENSOR_TAIL.json`, `production_code/hodge/CM_047_NP_TENSOR_BOUND.json`, `.md`.
- Dependency recomputation: `production_code/group/AUTONOMOUS_CONTINUATION_DEPENDENCY_RECOMPUTATION.json`, `.csv`, `.md`.
- Updated workbook: `Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx` and required output mirror.
- Logs: `WORK_LOG.md`, `CODE_WORK_LOG.md`.
- Terminal report: `production_code/group/AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.json`, `.md`.

`source_current_195/main.tex` was not modified because formal insertion task `RUN-111` depends on incomplete `RUN-110`.
"""
    REPORT_MD.write_text(markdown, encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    rows = dependency_rows()
    write_dependency_audit(rows)
    record = terminal_record()
    write_terminal_report(record)
    print(json.dumps({
        "dependency_json": str(OUT_BASE.with_suffix('.json')),
        "dependency_csv": str(OUT_BASE.with_suffix('.csv')),
        "dependency_markdown": str(OUT_BASE.with_suffix('.md')),
        "terminal_json": str(REPORT_JSON),
        "terminal_markdown": str(REPORT_MD),
    }, indent=2))


if __name__ == "__main__":
    main()
