"""Finalize the constructive-R4 endpoint without mutating frozen inputs.

The first mathematically global-valid quotient has been found.  This script
adds the representation, resource, endpoint, workbook-update, and reporting
layers.  It deliberately does not create LEVEL_A1 because the frozen numerical
resource contract is incomplete.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
ROOT = R4.parent
NOW = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


root_hash = (R4 / "00_FROZEN_INPUTS/FROZEN_INPUT_ROOT_HASH.txt").read_text(encoding="utf-8").strip()
candidate_path = R4 / "10_CANDIDATES/CAND-R4-0005.certificate.json"
candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
candidate_hash = sha256(candidate_path)
workbook_path = R4 / "00_FROZEN_INPUTS/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx"

arith_path = R4 / "04_ARITHMETIC/ARITH-P3-6F6FBFF4038772DA.certificate.json"
p2_path = R4 / "05_P_QUOTIENT/P2C2_C8_D2_BRANCH_0005.certificate.json"
global_path = R4 / "11_CERTIFICATES/CAND-R4-0005.global_pass_scan.json"
independent_path = R4 / "11_CERTIFICATES/CAND-R4-0005.global_independent_replay.json"
minimization_path = R4 / "12_MINIMIZATION/CAND-R4-0005.factor_deletion.json"

order_arith = 720
order_p2 = 64
order_q = 46080
hilbert_dimension = 2 * order_q
assert order_arith * order_p2 == order_q == candidate["actual_order"]

representation_path = R4 / "08_PRODUCTS/CAND-R4-0005_DIRECT_PRODUCT_AND_ACTION_CERTIFICATE.json"
representation = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "candidate_math_certificate": {
        "path": "10_CANDIDATES/CAND-R4-0005.certificate.json",
        "sha256": candidate_hash,
    },
    "factor_evidence": [
        {
            "factor_id": "ARITH-P3-6F6FBFF4038772DA",
            "order": order_arith,
            "certificate": "04_ARITHMETIC/ARITH-P3-6F6FBFF4038772DA.certificate.json",
            "certificate_sha256": sha256(arith_path),
            "marked_projection_surjective": True,
        },
        {
            "factor_id": "P2C2-C8-D2-1D16194A8DBB81E2",
            "order": order_p2,
            "certificate": "05_P_QUOTIENT/P2C2_C8_D2_BRANCH_0005.certificate.json",
            "certificate_sha256": sha256(p2_path),
            "marked_projection_surjective": True,
        },
    ],
    "subdirect_product_proof": {
        "actual_generated_diagonal_image_order": order_q,
        "ambient_direct_product_order": order_arith * order_p2,
        "image_is_subgroup_of_direct_product": True,
        "both_coordinate_projections_surjective": True,
        "equal_finite_orders": True,
        "conclusion": "the actual generated subdirect image equals the full direct product of the two certified factors",
    },
    "certified_permutation_actions": {
        "faithful_intransitive": {
            "degree": order_arith + order_p2,
            "construction": "disjoint union of the right-regular actions of the order-720 and order-64 factors",
            "kernel_argument": "the first orbit kills exactly the second factor and the second orbit kills exactly the first; the two kernels intersect trivially",
            "C8_compatible": True,
            "C8_argument": "the descended factor automorphisms act on their regular point sets and conjugate each right-regular action to the image under beta",
        },
        "faithful_transitive": {
            "degree": order_q,
            "construction": "right-regular action of Q",
            "kernel": "trivial",
            "C8_compatible": True,
        },
        "minimum_faithful_degree": "UNVERIFIED",
        "minimum_transitive_degree": "UNVERIFIED",
        "scope_warning": "the constructed degrees are rigorous upper bounds, not proofs of minimum degree",
    },
    "physical_regular_quotient_model": {
        "sites_per_layer": order_q,
        "layers": 2,
        "one_particle_hilbert_dimension": hilbert_dimension,
        "scope_warning": "the degree-784 faithful action is not a replacement for the regular quotient site's |Q|-site-per-layer physical model",
    },
    "representation_completeness": "UNVERIFIED",
    "missing_for_completeness": "a complete irreducible-representation registry with dimensions, multiplicities, C8 action, and parity sectors",
    "classification": "PASS_CONSTRUCTED_FAITHFUL_ACTIONS_MINIMUM_AND_IRREP_COMPLETENESS_UNVERIFIED",
    "created_at": NOW,
}
write_json(representation_path, representation)

state_vector_bytes = hilbert_dimension * 16
intralayer_directed_entries = 2 * order_q * 8
dense_interlayer_pairs = order_q * order_q
dense_csr_one_direction_payload = dense_interlayer_pairs * (16 + 4)
dense_csr_two_directions_payload = 2 * dense_csr_one_direction_payload

resource_path = R4 / "13_RESOURCE_GATE/CAND-R4-0005_RESOURCE_GATE.json"
resource = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "frozen_input_root_hash": root_hash,
    "candidate_math_certificate_sha256": candidate_hash,
    "authoritative_workbook": {
        "path": "00_FROZEN_INPUTS/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx",
        "sha256": sha256(workbook_path),
        "audit": "13_RESOURCE_GATE/FROZEN_WORKBOOK_RESOURCE_AUDIT.json",
        "mutation_performed": False,
    },
    "mathematical_gate_status": "PASS",
    "construction_resource_gate": {
        "status": "PASS_LOCAL",
        "maximum_new_peak_working_set_bytes": 8589934592,
        "maximum_new_output_bytes": 107374182400,
        "mandatory_preserved_free_bytes": 250000000000,
        "hard_rss_ceiling_bytes": 51539607552,
        "observed_method": "constant-memory sequential scans with durable checkpoints",
        "global_records_scanned_primary": 785639753,
        "global_records_scanned_independent": 785639753,
        "hpc_escalation_triggered": False,
    },
    "physical_problem_size": {
        "quotient_sites_per_layer": order_q,
        "layers": 2,
        "one_particle_hilbert_dimension": hilbert_dimension,
        "one_complex128_state_vector_bytes": state_vector_bytes,
        "intralayer_directed_nearest_neighbour_entries": intralayer_directed_entries,
        "full_interlayer_policy": "all pairs within the frozen D_c support; no nearest-neighbour or same-label surrogate",
        "actual_interlayer_supported_pair_count": "UNVERIFIED",
    },
    "dense_interlayer_reference_not_a_claim_of_actual_storage": {
        "all_possible_cross_layer_pairs": dense_interlayer_pairs,
        "one_direction_CSR_data_plus_int32_column_bytes_excluding_row_pointer": dense_csr_one_direction_payload,
        "two_explicit_directions_same_payload_model_bytes_excluding_row_pointers": dense_csr_two_directions_payload,
        "interpretation": "a conservative dense reference only; the actual D_c-supported sparsity and matrix-free policy are not certified",
    },
    "frozen_numerical_A1_budget": {
        "target_memory_bytes": 17179869184,
        "hard_rss_ceiling_bytes": 51539607552,
        "matvec_budget": None,
        "wall_time_budget_seconds": None,
        "residual_tolerance": None,
        "krylov_dimension": None,
        "polynomial_degree": None,
        "parameter_grid_cardinality": None,
        "probe_count": None,
        "precision_policy": None,
    },
    "additional_authoritative_unset_rows": [
        {
            "task_id": "PF-SCN-009",
            "status": "BLOCKED",
            "missing": "root, linear-solve, and derivative tolerances; hermiticity 1e-12 and eigenpair residual 1e-10 are already fixed",
        },
        {
            "task_id": "PF-KER-005",
            "status": "BLOCKED",
            "missing": "observable-specific C0/C1/C2 tail allocations and acceptance margins",
        },
        {
            "task_id": "PF-EUC-003",
            "status": "BLOCKED",
            "missing": "full-2D mBZ grid, refinement rule, and convergence tolerance",
        },
        {
            "task_id": "PF-HOD-004",
            "status": "BLOCKED",
            "missing": "Hodge C0/C1 error allocation and positive certified slope margin",
        },
    ],
    "frozen_items_retained": {
        "h_over_a_B": 0.5,
        "lambda_perp_over_a_B_primary": 0.2,
        "D_c_over_a_B_primary": 3.0,
        "interlayer_pair_policy": "all pairs within support",
        "KPM_primary_moments": 8192,
        "KPM_primary_probes": 64,
        "SLQ_depth": 256,
        "SLQ_primary_probes": 64,
    },
    "decision": {
        "resource_gate": "UNVERIFIED",
        "classification": "MATH_PASS_RESOURCE_UNVERIFIED_UNSET_COMPONENTS",
        "production_eligible": False,
        "A1_release_allowed": False,
        "strongest_exact_obstruction": "the authoritative numerical-A1 contract has mandatory null budget/solver fields and does not certify the actual D_c-supported interlayer pair count or peak-memory/matvec implementation",
        "not_a_math_failure": True,
    },
    "HPC_routing": {
        "triggered": False,
        "reason": "the blocker is missing frozen scientific/runtime input, not measured local CPU, RAM, GPU, storage, I/O, wall-time, or parallelism exhaustion",
        "handoff_created": False,
    },
    "created_at": NOW,
}
write_json(resource_path, resource)

endpoint_path = R4 / "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json"
endpoint = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "frozen_input_root_hash": root_hash,
    "marked_quotient_hash": candidate["marked_quotient_hash"],
    "actual_order": order_q,
    "mathematical_gates": {
        "algebra": "PASS",
        "exact_C8": "PASS",
        "parity": "PASS",
        "physical_shell": "PASS",
        "local_injectivity": "PASS",
        "based_geometry": "NOT_REQUESTED",
        "global_systole": "PASS_COMPLETE_CLOSED_DOMAIN",
        "certified_bound": "sys(H^2/K)/a_B > 6",
    },
    "resource_gate": "UNVERIFIED_UNSET_COMPONENTS",
    "representation_completeness": "UNVERIFIED",
    "independent_replay": "PASS_COMPLETE_CLOSED_DOMAIN",
    "minimization": "MINIMAL_WITHIN_SELECTED_TWO_FACTOR_PRESENTATION",
    "A1": "NOT_FOUND",
    "classification": "GLOBAL_VALID_RESOURCE_UNVERIFIED_A1_NOT_RELEASED",
    "proof_chain": {
        "candidate_math_certificate": {"path": "10_CANDIDATES/CAND-R4-0005.certificate.json", "sha256": candidate_hash},
        "global_scan": {"path": "11_CERTIFICATES/CAND-R4-0005.global_pass_scan.json", "sha256": sha256(global_path)},
        "independent_replay": {"path": "11_CERTIFICATES/CAND-R4-0005.global_independent_replay.json", "sha256": sha256(independent_path)},
        "representation": {"path": "08_PRODUCTS/CAND-R4-0005_DIRECT_PRODUCT_AND_ACTION_CERTIFICATE.json", "sha256": sha256(representation_path)},
        "minimization": {"path": "12_MINIMIZATION/CAND-R4-0005.factor_deletion.json", "sha256": sha256(minimization_path)},
        "resource": {"path": "13_RESOURCE_GATE/CAND-R4-0005_RESOURCE_GATE.json", "sha256": sha256(resource_path)},
    },
    "created_at": NOW,
}
write_json(endpoint_path, endpoint)
endpoint_hash = sha256(endpoint_path)

# Candidate ledger is a live registry, not a frozen input.  Preserve the five
# candidates and update only the endpoint-layer fields of CAND-R4-0005.
ledger_path = R4 / "10_CANDIDATES/CANDIDATE_LEDGER.tsv"
with ledger_path.open("r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    fieldnames = list(reader.fieldnames or [])
    rows = list(reader)
assert len(rows) == 5
for row in rows:
    if row["Candidate ID"] != "CAND-R4-0005":
        continue
    estimate = json.loads(row["Resource estimate"])
    estimate.update(
        {
            "physical_hilbert_dimension": hilbert_dimension,
            "resource_gate_certificate": "13_RESOURCE_GATE/CAND-R4-0005_RESOURCE_GATE.json",
            "numerical_A1_contract_complete": False,
        }
    )
    row["Minimum known faithful degree"] = "<=784 faithful (intransitive); <=46080 faithful transitive; minima UNVERIFIED"
    row["Resource estimate"] = json.dumps(estimate, separators=(",", ":"))
    row["Resource status"] = "UNVERIFIED_UNSET_COMPONENTS"
    row["Representation status"] = "FAITHFUL_ACTIONS_CONSTRUCTED_MINIMA_AND_IRREP_COMPLETENESS_UNVERIFIED"
    row["Final disposition"] = "GLOBAL_VALID_RESOURCE_UNVERIFIED_A1_NOT_RELEASED"
    row["Certificate hash"] = endpoint_hash
with ledger_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

a1_not_found_path = R4 / "14_LEVEL_A1/A1_NOT_FOUND.json"
write_json(
    a1_not_found_path,
    {
        "schema_version": "1.0",
        "status": "A1_NOT_FOUND",
        "best_mathematical_candidate": "CAND-R4-0005",
        "candidate_order": order_q,
        "global_systole": "PASS_COMPLETE_CLOSED_DOMAIN",
        "resource_gate": "UNVERIFIED_UNSET_COMPONENTS",
        "reason": "mandatory numerical resource/solver inputs remain unset in the authoritative frozen contract",
        "endpoint_certificate": "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json",
        "endpoint_certificate_sha256": endpoint_hash,
        "full_Hamiltonian_started": False,
        "HPC_handoff_triggered": False,
        "created_at": NOW,
    },
)

task_rows_path = R4 / "16_REPORTS/WORKBOOK_CONSTRUCTIVE_TASK_ROWS.tsv"
task_fields = [
    "Task ID", "Phase", "Category", "Priority", "Task Type", "Task",
    "Exact Manuscript Contract", "Required Inputs", "Deliverable",
    "Acceptance Criteria", "Forbidden Simplification / Failure Mode",
    "Dependencies", "Owner", "Status", "Freeze Gate?", "Numerical?",
    "Source Location", "Notes",
]
common = {
    "Phase": "1 Parameter Freeze",
    "Category": "Finite quotient",
    "Priority": "P0",
    "Task Type": "Constructive R4",
    "Exact Manuscript Contract": "Revision-4 kernel-first constructive finite-quotient directive",
    "Owner": "Math/Code",
    "Freeze Gate?": "Yes",
    "Numerical?": "No",
    "Source Location": "CONSTRUCTIVE_EXECUTION_R4",
}
task_specs = [
    ("PF-GRP-CONSTRUCTIVE-R4", "Construct and certify production A1 quotient", "R4 child certificates", "A1 freeze or exact obstruction", "All math, resource, and replay gates PASS", "Do not revive degree enumeration", "PF-GRP-CONSTRUCTIVE-R4-RESOURCE", "Blocked", "A mathematically valid quotient exists; parent is blocked only by the unset resource contract."),
    ("PF-GRP-CONSTRUCTIVE-R4-FROZEN", "Freeze exact constructive inputs", "Theory, workbook, exact registries", "Frozen input root hash", "Manifest/hash replay PASS", "Do not mutate frozen inputs", "", "Done", root_hash),
    ("PF-GRP-CONSTRUCTIVE-R4-ARITH", "Build arithmetic separators", "Frozen Bolza arithmetic model", "Certified p=3 and p=5 factors", "Exact relations/images PASS", "No catalogue ordinal IDs", "PF-GRP-CONSTRUCTIVE-R4-FROZEN", "Done", "Two arithmetic factors constructed."),
    ("PF-GRP-CONSTRUCTIVE-R4-SEPLIB", "Build separator library", "Certified witness orbits", "Separator ledger and matrix", "Content-addressed coverage", "No unverified legacy claims", "PF-GRP-CONSTRUCTIVE-R4-ARITH", "Done", "Five standalone separator columns plus one homology support factor."),
    ("PF-GRP-CONSTRUCTIVE-R4-CEGAR", "Run kernel-first CEGAR chain", "Witness/separator registries", "Candidate sequence 0001--0005", "First complete global PASS frozen", "No witness regression", "PF-GRP-CONSTRUCTIVE-R4-SEPLIB", "Done", "CAND-R4-0005 is the first complete global PASS."),
    ("PF-GRP-CONSTRUCTIVE-R4-PQUOT", "Construct C8-stable p-quotient separators", "Class-2 F2 central layer", "D1/D2 factor certificates", "All stable D1/D2 branches audited", "Do not sample branch spaces", "PF-GRP-CONSTRUCTIVE-R4-CEGAR", "Done", "7 D1 and 19 D2 stable spaces exhaustively audited."),
    ("PF-GRP-CONSTRUCTIVE-R4-EXT", "Construct cohomological extensions if required", "Failed globally valid branch", "Extension certificate", "Needed only if current global-valid branch fails a later mandatory gate", "Do not add factors without a certified witness need", "PF-GRP-CONSTRUCTIVE-R4-PQUOT", "Deferred", "Not required before the resource decision."),
    ("PF-GRP-CONSTRUCTIVE-R4-PRODUCT", "Form actual subdirect products and minimize", "Selected factors", "Actual-order and deletion certificates", "No Cartesian order substituted for actual image", "No unproved product-order claim", "PF-GRP-CONSTRUCTIVE-R4-PQUOT", "Done", "Order 46080; full direct product proved by equal-order argument; neither selected factor deletable."),
    ("PF-GRP-CONSTRUCTIVE-R4-GLOBAL", "Certify strict global systole", "Complete closed dangerous registry", "Primary and independent complete scans", "All 785639753 records covered; zero kernel hits", "No based-to-global promotion", "PF-GRP-CONSTRUCTIVE-R4-PRODUCT", "Done", "sys/a_B > 6 certified."),
    ("PF-GRP-CONSTRUCTIVE-R4-RESOURCE", "Certify numerical A1 resources", "Frozen solver/runtime budgets and actual D_c-supported operator cost", "Resource PASS/FAIL certificate", "Peak RAM, matvec, wall time, precision and parameter concurrency certified", "Do not invent missing budgets or use dense/NN surrogates", "PF-GRP-CONSTRUCTIVE-R4-GLOBAL;PF-SCN-009;PF-KER-005;PF-EUC-003;PF-HOD-004", "Blocked", "Mandatory numerical-A1 fields remain unset; current certificate is UNVERIFIED."),
    ("PF-GRP-CONSTRUCTIVE-R4-A1", "Freeze LEVEL_A1_CONSTRUCTIVE_R4", "All mandatory gate certificates", "Immutable A1 root", "Resource gate and representation claims at requested scope PASS", "Do not freeze a math-only candidate as A1", "PF-GRP-CONSTRUCTIVE-R4-RESOURCE", "Blocked", "A1 NOT FOUND at this endpoint."),
    ("PF-GRP-CONSTRUCTIVE-R4-TOWER", "Construct two inequivalent towers", "Frozen A1", "Tower A/B certificates", "Begin only after A1 freeze", "Do not start from an unreleased quotient", "PF-GRP-CONSTRUCTIVE-R4-A1", "Deferred", "Correctly not started."),
]
with task_rows_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=task_fields, lineterminator="\n")
    writer.writeheader()
    for task_id, task, inputs, deliverable, accept, forbidden, deps, status, notes in task_specs:
        row = dict(common)
        row.update({
            "Task ID": task_id,
            "Task": task,
            "Required Inputs": inputs,
            "Deliverable": deliverable,
            "Acceptance Criteria": accept,
            "Forbidden Simplification / Failure Mode": forbidden,
            "Dependencies": deps,
            "Status": status,
            "Notes": notes,
        })
        writer.writerow(row)

obstruction_report = f"""
# Constructive Obstruction Report R4

## Endpoint

The constructive search did **not** fail mathematically. `CAND-R4-0005` is an explicit marked quotient of order {order_q} that passes algebra, exact C8, parity, physical shell, local injectivity, and a complete closed-domain global systole scan. A1 is not released because the mandatory numerical resource contract is incomplete.

## Construction families attempted

- Arithmetic reductions: canonical factors at p=3 (order 720) and p=5 (order 15600). The attempted prime set was `{{3,5}}`; this is not an exclusion of other primes.
- Homology support: `H1(Gamma_B;F2)` in candidate 0002.
- C8-stable lower-exponent-2 class-2 quotients: every stable one-dimensional space (7 total) and every stable two-dimensional space (19 total) in the certified nine-dimensional central layer were audited. No D1 space covers all three accumulated global witnesses; exactly three D2 spaces do.
- Actual subdirect products: candidates 0001--0005. Candidate 0005 is proved to equal the full product of its order-720 and order-64 factors because its actual image has their product order.
- Cohomological extensions and classical/semilinear families were not required after the global-valid candidate was found; they remain open directions rather than excluded families.

## Complete finite domains actually certified

- The authoritative closed global dangerous registry contains 785,639,753 records, including the boundary at `6 a_B`. Both the primary and independent scanners covered all records and found zero candidate-0005 kernel hits.
- The p=2 class-2 stable-space domain is complete at dimensions 1 and 2: 7 D1 and 19 D2 spaces.
- The candidate ledger contains five constructive candidates. This is not a proof of global optimality across all finite quotients.

## Best achieved candidates

- Best globally valid quotient: `CAND-R4-0005`, order {order_q}, `sys/a_B > 6`, globally replayed independently.
- Best resource-valid but geometry-failing quotient: none has a numerical-A1 Resource PASS. Candidate 0001 (order 31200) stayed within the construction resource envelope but fails local `B_geom(3)` injectivity.

## Witness and separator statistics

- 14 distinct C8 witness orbits, represented by 81 typed registry rows: 36 shell, 36 local-radius-1, 1 local-radius-3, 5 based, and 3 global rows.
- Standalone separator library: 2 arithmetic factors and 3 p-quotient factors. One additional F2-homology support factor was used in candidate 0002.
- CEGAR outcomes: candidate 0001 failed locally; candidates 0002--0004 produced exact global witnesses; candidate 0005 passed the complete global domain.

## Exact order and minimization obstructions

- Any genuine separator refinement of candidate 0001 has order at least 62400, above the frozen ceiling 50000.
- The tested p=5 refinement of candidate 0002 constructed 50001 distinct elements and is therefore outside the order window without needing full enumeration.
- Any strict nested refinement of candidate 0004 has order at least 92160.
- In candidate 0005, deleting the p=2 factor leaves order 720 and only 337 local images; deleting the p=3 factor leaves order 64 and only 55 local images. Thus it is minimal within the selected two-factor presentation, not proved globally order-minimal.

## Resource lower bounds and unresolved upper bound

- The physical regular quotient model has {order_q} sites per layer, two layers, and one-particle dimension {hilbert_dimension}.
- One complex128 state vector needs {state_vector_bytes:,} bytes; the two intralayer degree-eight directed shells contain {intralayer_directed_entries:,} entries.
- A dense all-cross-layer reference has {dense_interlayer_pairs:,} pairs and would require {dense_csr_one_direction_payload:,} bytes for one CSR data+int32-column payload, excluding row pointers. This is a reference, not the actual `D_c`-supported count.
- The actual supported interlayer nonzero count, production matvec implementation, Krylov dimension, precision, concurrency, wall-time budget, and several tolerances are not frozen. Consequently neither a safe peak-memory upper bound nor Resource PASS can be certified.

## Strongest exact obstruction to A1

The frozen numerical-A1 contract explicitly contains null values for `matvec_budget`, `wall_time_budget_seconds`, `residual_tolerance`, `krylov_dimension`, `polynomial_degree`, `parameter_grid_cardinality`, `probe_count`, and `precision_policy`. Workbook tasks PF-SCN-009, PF-KER-005, PF-EUC-003, and PF-HOD-004 also retain genuine missing numerical data. Inventing these values is forbidden. Therefore:

`A1 = NOT FOUND` and `Resource Gate = UNVERIFIED`, even though the quotient is mathematically global-valid.

This does not trigger the supplemental HPC handoff rule: HPC cannot supply missing scientific acceptance parameters, and no local resource limit was reached during the exact construction scans.

## Next theory-guided step

Freeze the missing numerical-A1 contract and certify the actual all-pairs-within-`D_c` operator support/matvec memory model for candidate 0005. Then rerun only the resource gate. If it passes, freeze A1; if it fails, resume construction from the certified candidate/witness/separator state without returning to degree enumeration.
"""
write_text(R4 / "16_REPORTS/CONSTRUCTIVE_OBSTRUCTION_REPORT_R4.md", obstruction_report)

final_report = f"""
# Constructive Execution R4 — Final Endpoint Report

**A. Strategy:**  
CONSTRUCTIVE R4

**B. Legacy degree enumeration active:**  
NO

**C. Frozen input hash:**  
`{root_hash}`

**D. Constructive iterations:**  
5 candidates (`CAND-R4-0001` through `CAND-R4-0005`)

**E. Unique witness orbits:**  
14

**F. Separator factors constructed:**  
arithmetic = 2  
p-quotient = 3  
cohomological = 0  
classical = 0  
other = 1 (`H1(Gamma_B;F2)` support factor; not a standalone separator-library column)

**G. Best candidate:**  
ID = `CAND-R4-0005`

**H. Group order:**  
`|Q| = {order_q}`

**I. Minimum known faithful/transitive degree:**  
Minima UNVERIFIED. Certified constructions: faithful intransitive degree <= {order_arith + order_p2}; faithful transitive regular degree <= {order_q}.

**J. Exact C8:**  
PASS

**K. Parity:**  
PASS

**L. Physical shell:**  
PASS

**M. Local injectivity:**  
PASS

**N. Based geometry:**  
NOT-REQUESTED

**O. Global systole:**  
PASS

**P. Certified lower bound:**  
`sys(H^2/K)/a_B > 6`

**Q. Resource gate:**  
UNVERIFIED (`UNVERIFIED_UNSET_COMPONENTS`)

**R. Representation completeness:**  
UNVERIFIED (faithful actions are constructed; a complete irrep/multiplicity/C8/parity registry is not)

**S. Independent replay:**  
PASS

**T. A1:**  
NOT FOUND

**U. If not found — strongest exact obstruction:**  
The authoritative numerical-A1 resource contract has mandatory unset solver/budget/precision/grid/probe fields and lacks a certified actual `D_c`-supported operator cost. Those values may not be invented, so the Resource Gate cannot be promoted to PASS.

**V. Old exhaustive degree search launched:**  
NO

## Endpoint interpretation

Candidate 0005 is the first constructively generated quotient with a complete independent global proof: both scanners covered 785,639,753 closed-domain records and found no kernel hit. It is minimal within its selected two-factor presentation. It is frozen as a mathematically global-valid candidate, not as A1. No full Hamiltonian or tower run was launched.

The supplemental HPC rule was not triggered: all exact scans finished locally within the safe construction envelope, and the remaining blocker is missing frozen scientific input rather than compute capacity.
"""
final_report_path = R4 / "16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.md"
write_text(final_report_path, final_report)

final_report_json = {
    "schema_version": "1.0",
    "A_strategy": "CONSTRUCTIVE R4",
    "B_legacy_degree_enumeration_active": "NO",
    "C_frozen_input_hash": root_hash,
    "D_constructive_iterations": 5,
    "E_unique_witness_orbits": 14,
    "F_separator_factors_constructed": {"arithmetic": 2, "p_quotient": 3, "cohomological": 0, "classical": 0, "other": 1},
    "G_best_candidate": "CAND-R4-0005",
    "H_group_order": order_q,
    "I_minimum_known_faithful_transitive_degree": {
        "minimum_faithful": "UNVERIFIED",
        "constructed_faithful_intransitive_upper_bound": order_arith + order_p2,
        "minimum_transitive": "UNVERIFIED",
        "constructed_faithful_transitive_upper_bound": order_q,
    },
    "J_exact_C8": "PASS",
    "K_parity": "PASS",
    "L_physical_shell": "PASS",
    "M_local_injectivity": "PASS",
    "N_based_geometry": "NOT-REQUESTED",
    "O_global_systole": "PASS",
    "P_certified_lower_bound": "sys(H^2/K)/a_B > 6",
    "Q_resource_gate": "UNVERIFIED",
    "R_representation_completeness": "UNVERIFIED",
    "S_independent_replay": "PASS",
    "T_A1": "NOT FOUND",
    "U_strongest_exact_obstruction": resource["decision"]["strongest_exact_obstruction"],
    "V_old_exhaustive_degree_search_launched": "NO",
    "HPC_handoff": "NOT_TRIGGERED",
    "endpoint_certificate": "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json",
    "endpoint_certificate_sha256": endpoint_hash,
    "resource_certificate_sha256": sha256(resource_path),
    "representation_certificate_sha256": sha256(representation_path),
    "created_at": NOW,
}
write_json(R4 / "16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_FINAL_REPORT.json", final_report_json)

write_text(
    R4 / "logs/SUPERSEDED_ARTIFACTS.md",
    """
# Superseded and quarantined artifacts

These files are preserved for provenance and are excluded from the final proof chain:

- `10_CANDIDATES/verify_global_candidate_generic.py` — incomplete first generic verifier; superseded by the candidate-specific verifiers and v2 finalizer path.
- `10_CANDIDATES/finalize_global_candidate_generic.py` — first generic finalizer used an over-restrictive projective-sign assumption; superseded by `finalize_global_candidate_generic_v2.py`.
- `10_CANDIDATES/scan_candidate_0003_axis6.cpp` — first class-2 scanner omitted a relation cocycle cross-term and stopped in self-test before reading the authoritative registry; superseded by `scan_candidate_0003_axis6_v2.cpp`.
- `11_CERTIFICATES/scan_candidate_0005_independent.cpp` — first independent implementation tested a registry superset without the exact trace filter and produced a non-dangerous candidate identity. It is quarantined by `CAND-R4-0005.independent_v1_false_hit_quarantine.json` and superseded by `scan_candidate_0005_independent_v2.cpp`.

No listed artifact contributes a PASS assertion to the endpoint certificate.
""",
)

write_text(
    R4 / "logs/WORK_LOG_R4_20260915.md",
    f"""
# Work Log — Constructive R4 — 2026-09-15

- Disabled legacy degree-enumeration autostart and preserved legacy evidence.
- Froze exact inputs under root hash `{root_hash}`; foundational regression 56/56 and frozen-contract regression 8/8 passed.
- Constructed five candidates sequentially. Candidate 0001 failed local injectivity; candidates 0002--0004 failed with exact global witnesses; candidate 0005 passed.
- Primary and independent candidate-0005 scans each covered all 785,639,753 closed-domain records with zero kernel hits.
- Certified candidate order {order_q}, strict `sys/a_B > 6`, exact C8, parity, shell, local injectivity, and two-factor deletion minimality.
- Constructed faithful permutation actions of degrees {order_arith + order_p2} (intransitive) and {order_q} (regular transitive); minimum degree and irrep completeness remain unverified.
- Audited the frozen workbook read-only. Resource Gate remains `UNVERIFIED_UNSET_COMPONENTS`; A1 is not released and no Hamiltonian/tower run was started.
- Supplemental HPC escalation was not triggered because local scans completed safely; the remaining blocker is missing frozen scientific input, not workstation exhaustion.
""",
)

execution_state = {
    "strategy": "CONSTRUCTIVE_R4",
    "legacy_enumeration_autostart": "OFF",
    "legacy_degree_enumeration_active": False,
    "theory_authority": "THEORY_EXPANDED_V2_C59_R6 / internal revision 4",
    "theory_authority_status": "PASS",
    "theory_map_status": "PASS",
    "frozen_input_contract_status": "PASS_FROZEN_EXACT_MATH_AND_ORDER_SCOPE",
    "foundational_regression_status": "PASS_56_OF_56",
    "frozen_contract_regression_status": "PASS_8_OF_8",
    "separator_library_size": 5,
    "homology_support_factors": 1,
    "unique_witness_orbits": 14,
    "arithmetic_factors": 2,
    "p_quotient_factors": 3,
    "extension_factors": 0,
    "constructive_iterations": 5,
    "current_candidate_order": order_q,
    "current_gate_reached": "RESOURCE_GATE",
    "global_status": "PASS_COMPLETE_CLOSED_DOMAIN",
    "resource_status": "UNVERIFIED_UNSET_COMPONENTS",
    "representation_status": "FAITHFUL_ACTIONS_CONSTRUCTED_MINIMA_AND_IRREP_COMPLETENESS_UNVERIFIED",
    "best_candidate": "CAND-R4-0005",
    "best_candidate_endpoint_certificate": "11_CERTIFICATES/CAND-R4-0005.endpoint_certificate.json",
    "best_candidate_endpoint_sha256": endpoint_hash,
    "a1_status": "NOT_FOUND",
    "full_hamiltonian_started": False,
    "tower_a_level": 0,
    "tower_b_level": 0,
    "HPC_escalation_triggered": False,
    "updated_at": NOW,
}
write_json(R4 / "EXECUTION_STATE.json", execution_state)

print(json.dumps({
    "status": "R4_ENDPOINT_FINALIZED",
    "candidate": "CAND-R4-0005",
    "order": order_q,
    "global": "PASS",
    "resource": "UNVERIFIED_UNSET_COMPONENTS",
    "A1": "NOT_FOUND",
    "endpoint_sha256": endpoint_hash,
}, indent=2))
