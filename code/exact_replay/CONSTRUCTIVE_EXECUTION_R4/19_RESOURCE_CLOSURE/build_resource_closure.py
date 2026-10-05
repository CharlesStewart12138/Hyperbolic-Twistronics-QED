"""Build the post-construction resource audit and finite input request."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
OUT = R4 / "19_RESOURCE_CLOSURE"
H_MATH = json.loads((R4 / "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json").read_text(encoding="utf-8"))["H_MATH"]
Q = 46080
N = 2 * Q


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


rows = []


def add(field, required, source, value, units, provenance, status, blocking, notes, category):
    rows.append({
        "Field": field,
        "Required?": required,
        "Source": source,
        "Frozen value": value,
        "Units": units,
        "Exact / measured / chosen": provenance,
        "Status": status,
        "Blocking A1?": blocking,
        "Notes": notes,
        "Category": category,
    })


contract = "00_FROZEN_INPUTS/FROZEN_INPUT_CONTRACT.json"
workbook = "00_FROZEN_INPUTS/Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx"
add("B_mem_target", "YES", contract, "17179869184", "bytes", "CHOSEN/FROZEN", "PASS", "NO", "Numerical-A1 target memory.", "B_RESOURCE_ENVELOPE")
add("B_mem_hard", "YES", contract, "51539607552", "bytes", "CHOSEN/FROZEN", "PASS", "NO", "Hard RSS ceiling.", "B_RESOURCE_ENVELOPE")
add("B_mv", "YES", contract, "", "seconds/matvec or accepted throughput", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "No authoritative matvec budget.", "B_RESOURCE_ENVELOPE")
add("B_wall", "YES", contract, "", "seconds/job and total campaign", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "No authoritative wall-time budget.", "B_RESOURCE_ENVELOPE")
add("epsilon_res_eigenpair", "YES", f"{workbook}:PF-SCN-009", "1e-10", "relative residual", "CHOSEN/FROZEN", "PASS", "NO", "Eigenpair residual only.", "A_SCIENTIFIC_NUMERICAL")
add("epsilon_hermiticity", "YES", f"{workbook}:PF-SCN-009", "1e-12", "relative/norm contract", "CHOSEN/FROZEN", "PASS", "NO", "Hermiticity tolerance.", "A_SCIENTIFIC_NUMERICAL")
add("epsilon_root_linear_derivative", "YES", f"{workbook}:PF-SCN-009", "", "problem-specific", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Root, linear-solve, and derivative tolerances remain unspecified.", "A_SCIENTIFIC_NUMERICAL")
add("m_Krylov", "YES", contract, "", "vectors", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Determines basis memory and solver work.", "A_SCIENTIFIC_NUMERICAL")
add("restart_dimension", "YES", "no authoritative row found", "", "vectors", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Required for restarted Krylov solver cost.", "A_SCIENTIFIC_NUMERICAL")
add("solver_type", "YES", "no authoritative row found", "", "categorical", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "No eigensolver/backend selected.", "A_SCIENTIFIC_NUMERICAL")
add("requested_eigenpair_count", "YES", "no authoritative row found", "", "eigenpairs", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Target count is absent.", "A_SCIENTIFIC_NUMERICAL")
add("spectral_window", "YES", "no authoritative row found", "", "energy/frequency interval", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "No shift/target/window specification.", "A_SCIENTIFIC_NUMERICAL")
add("precision", "YES", contract, "", "complex64/complex128/mixed", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Pilot measured complex64 and complex128 only as alternatives.", "A_SCIENTIFIC_NUMERICAL")
add("KPM_polynomial_degree", "CONDITIONAL", f"{workbook}:PF-DOS-002", "8192; holdouts 4096,8192,16384", "moments", "CHOSEN/FROZEN", "PASS_CONDITIONAL", "NO", "Applies only if KPM is in selected production scope.", "A_SCIENTIFIC_NUMERICAL")
add("KPM_probe_count", "CONDITIONAL", f"{workbook}:PF-DOS-003", "64; holdouts 32,64,128", "probes", "CHOSEN/FROZEN", "PASS_CONDITIONAL", "NO", "Applies only if KPM is selected.", "A_SCIENTIFIC_NUMERICAL")
add("SLQ_depth", "CONDITIONAL", f"{workbook}:PF-DOS-004", "256 with full reorthogonalization", "steps", "CHOSEN/FROZEN", "PASS_CONDITIONAL", "NO", "Applies only if SLQ is selected.", "A_SCIENTIFIC_NUMERICAL")
add("SLQ_probe_count", "CONDITIONAL", f"{workbook}:PF-DOS-005", "64", "probes", "CHOSEN/FROZEN", "PASS_CONDITIONAL", "NO", "Independent RNG namespace required.", "A_SCIENTIFIC_NUMERICAL")
add("KPM_SLQ_rng_seeds", "CONDITIONAL", f"{workbook}:PF-DOS-007", "", "integer registry", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES_IF_DOS", "Seed 170217 is reserved for robustness and cannot be reused.", "A_SCIENTIFIC_NUMERICAL")
add("Theta_domain", "YES", f"{workbook}:PF-SCN-001", "[0,pi/8]", "radians", "CHOSEN/FROZEN", "PASS", "NO", "Irreducible hyperbolic twist interval.", "A_SCIENTIFIC_NUMERICAL")
add("Theta_grid_initial", "YES", f"{workbook}:PF-SCN-008", "91 endpoint-inclusive", "points", "CHOSEN/FROZEN", "PASS", "NO", "Adaptive refinement to delta_theta<=1e-4 rad with frozen triggers.", "A_SCIENTIFIC_NUMERICAL")
add("hopping_grid", "YES", f"{workbook}:PF-SCN-005", "[0,0.25,0.5,0.75,0.9,0.97,1,1.03,1.1,1.25,1.5,2]", "omega/omega_ref", "CHOSEN/FROZEN", "PASS", "NO", "One boundary-triggered expansion rule is frozen.", "A_SCIENTIFIC_NUMERICAL")
add("curvature_grid", "YES", f"{workbook}:PF-SCN-004", "[0,0.25,0.5,0.75,1]", "kappa_a/kappa_B", "CHOSEN/FROZEN", "PASS", "NO", "Intermediate values are synthetic deformations.", "A_SCIENTIFIC_NUMERICAL")
add("lambda_perp_grid", "YES", f"{workbook}:PF-SCN-006", "[0.125,0.20,0.25]", "lambda_perp/a_B", "CHOSEN/FROZEN", "PASS", "NO", "0.20 primary plus locked holdouts.", "A_SCIENTIFIC_NUMERICAL")
add("D_c_grid", "YES", f"{workbook}:PF-KER-002", "[2.5,3.0,3.5]; conditional monotone extension >=4", "a_B", "CHOSEN/FROZEN", "PASS", "NO", "Full all-pairs-within-support policy retained.", "A_SCIENTIFIC_NUMERICAL")
add("combined_parameter_schedule", "YES", "no authoritative row found", "", "blocks/cardinality", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Individual grids are frozen but their Cartesian/serial/adaptive composition is not.", "A_SCIENTIFIC_NUMERICAL")
add("mBZ_2D_grid", "CONDITIONAL", f"{workbook}:PF-EUC-003", "", "2D grid/refinement/tolerance", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES_IF_EUCLIDEAN_INCLUDED", "Path-only extrema are forbidden.", "A_SCIENTIFIC_NUMERICAL")
add("assembly_tolerance", "YES", "no authoritative row found", "", "distance/value tolerance", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Needed for supported-pair and numerical assembly acceptance.", "A_SCIENTIFIC_NUMERICAL")
add("observable_tail_tolerances", "YES", f"{workbook}:PF-KER-005;PF-HOD-004", "", "C0/C1/C2 budgets", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Observable-specific tail allocations and Hodge slope margin are absent.", "A_SCIENTIFIC_NUMERICAL")
add("production_mode", "YES", "frozen theory C47/C55; no workbook selection", "", "FULL-SPACE or REPRESENTATION-RESOLVED", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Theory defines both typed modes but does not select one.", "A_SCIENTIFIC_NUMERICAL")
add("production_hardware_definition", "YES", "local hardware snapshot is measurement only", "", "named host/node class", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Local pilot host cannot be silently declared the production target.", "B_RESOURCE_ENVELOPE")
add("CPU_cores_GPU_count_VRAM", "YES", "no authoritative production row found", "", "cores/count/bytes", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Local inventory is not a chosen production envelope.", "B_RESOURCE_ENVELOPE")
add("concurrency", "YES", "no authoritative row found", "", "simultaneous blocks/jobs", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Peak memory and total wall time depend on concurrency.", "B_RESOURCE_ENVELOPE")
add("storage_budget", "YES", contract, "107374182400 new output; preserve 250000000000 free", "bytes", "CHOSEN/FROZEN", "PASS", "NO", "Construction envelope; production output estimate still required.", "B_RESOURCE_ENVELOPE")
add("storage_format", "YES", "no authoritative row found", "", "CSR/BSR/matrix-free/cache", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Controls RAM, I/O, and reproducibility.", "C_IMPLEMENTATION_ESTIMATE")
add("checkpoint_interval", "YES", "no authoritative row found", "", "seconds or parameter blocks", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Required for production recovery cost.", "C_IMPLEMENTATION_ESTIMATE")
add("numerical_backend_versions", "YES", "software environment only freezes Python/GAP construction", "", "library/version/BLAS/GPU backend", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Production eigensolver/matvec backend is not selected.", "C_IMPLEMENTATION_ESTIMATE")
add("actual_interlayer_support_count", "YES", "CM-006/CM-008 not implemented for candidate 0005", "m_perp(theta,D_c) symbolic", "pairs", "IMPLEMENTATION_DEPENDENT", "UNVERIFIED_NOT_COMPUTED", "YES", "Cannot infer from dense all-pairs reference or nearest-neighbour surrogate.", "C_IMPLEMENTATION_ESTIMATE")
add("operator_storage_strategy", "YES", "no authoritative row found", "", "matrix-free or explicit sparse", "", "MISSING_USER_OR_PROJECT_SPECIFICATION", "YES", "Must retain full all-pairs-within-D_c physics.", "C_IMPLEMENTATION_ESTIMATE")

audit_path = OUT / "RESOURCE_CONTRACT_AUDIT.tsv"
with audit_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

missing = [row for row in rows if row["Status"] == "MISSING_USER_OR_PROJECT_SPECIFICATION" and row["Blocking A1?"] in ("YES", "YES_IF_DOS", "YES_IF_EUCLIDEAN_INCLUDED")]
implementation_open = [row for row in rows if row["Status"] == "UNVERIFIED_NOT_COMPUTED"]

formula_json = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "H_MATH": H_MATH,
    "quotient_vertices_per_layer": Q,
    "layers": 2,
    "orbitals_per_vertex": 1,
    "Hilbert_dimension": N,
    "physical_shell_degree": 8,
    "intralayer_directed_entries": 2 * Q * 8,
    "state_vector_bytes": {"complex64": N * 8, "complex128": N * 16},
    "krylov_basis_bytes": {"complex64": "737280*k", "complex128": "1474560*k"},
    "interlayer_supported_pairs": "m_perp(theta,D_c), currently uncomputed",
    "matrix_free_full_operator_nonzero_visits_per_matvec": "92160 diagonal + 737280 intralayer + 2*m_perp(theta,D_c) interlayer",
    "one_direction_interlayer_CSR_bytes_int32": "m_perp*(b+4)+4*(46080+1), b in {8,16}",
    "explicit_two_offdiagonal_blocks_CSR_payload_bytes": "2*m_perp*(b+4)+8*(46080+1), excluding framework/workspace overhead",
    "dense_cross_layer_reference_pairs_not_actual": Q * Q,
    "dense_one_direction_complex128_plus_int32_payload_not_actual": Q * Q * 20,
    "frozen_grid_component_counts": {"theta_initial": 91, "hopping": 12, "curvature": 5, "lambda_perp": 3, "D_c_primary_convergence": 3},
    "naive_full_cartesian_count_not_authorized": 91 * 12 * 5 * 3 * 3,
    "combined_schedule": "UNVERIFIED",
    "pilot": {
        "path": "19_RESOURCE_CLOSURE/INTRALAYER_MATRIX_FREE_PILOT.json",
        "sha256": sha256(OUT / "INTRALAYER_MATRIX_FREE_PILOT.json"),
        "scope": "intralayer-only empirical timing",
    },
    "classification": "EXACT_DIMENSIONS_AND_SYMBOLIC_RESOURCE_FORMULAS",
}
(OUT / "DETERMINISTIC_RESOURCE_FORMULAS.json").write_text(json.dumps(formula_json, indent=2) + "\n", encoding="utf-8")

formula_md = f"""
# Deterministic resource formulas for CAND-R4-0005

- Quotient vertices per layer: `|Q| = {Q}`.
- Layers/orbitals: `2 x 1`.
- Single-particle dimension: `N = 2|Q| = {N}`.
- Directed intralayer shell entries: `2 x {Q} x 8 = {2*Q*8}`.
- One state vector: `{N}b` bytes, namely `{N*8:,}` bytes for complex64 or `{N*16:,}` bytes for complex128.
- `k` simultaneous Krylov vectors: `k N b`, namely `{N*8}k` or `{N*16}k` bytes before orthogonalization and solver workspace.
- Let `m_perp(theta,D_c)` be the exact number of cross-layer pairs inside the frozen support. It is not yet computed. A full matrix-free matvec visits `N + 737280 + 2 m_perp` diagonal/off-diagonal entries, up to implementation constants.
- A one-direction CSR interlayer block with int32 columns requires `m_perp(b+4)+4(46080+1)` bytes before allocator/library overhead. Explicitly storing both off-diagonal blocks doubles the payload; matrix-free evaluation may avoid that duplication but still must enumerate the exact support.
- `46080^2 = {Q*Q:,}` is only a dense reference, not the certified supported-pair count.

The individual frozen component grids have counts 91 (initial twist), 12 (hopping), 5 (curvature), 3 (profile), and 3 (primary cutoff convergence). Their naive product `{91*12*5*3*3:,}` is not an authorized production schedule; serial/adaptive composition and concurrency remain unspecified.

The bounded pilot measures only the eight-direction intralayer term. It cannot close memory or time for the full `D_c` interlayer kernel.
"""
(OUT / "DETERMINISTIC_RESOURCE_FORMULAS.md").write_text(formula_md.lstrip(), encoding="utf-8")

request = """
# A1 Resource Input Request

Only the following unresolved project decisions are required. Existing frozen values—16 GiB target memory, 48 GiB hard RSS, the 91-point initial twist grid, the 12-point hopping grid, KPM 8192/64, and SLQ 256/64—do not need to be re-entered.

1. **Production mode**
   - Required field: `production_mode`
   - Current source: theory defines both modes; workbook selects neither
   - Why needed: decides whether the complete irreducible-representation inventory is mandatory
   - Allowed input: exactly `FULL-SPACE` or `REPRESENTATION-RESOLVED`

2. **Production execution target**
   - Required fields: named local/HPC target, CPU cores, GPU count/VRAM if used
   - Current source: no authoritative target; the captured laptop is measurement-only
   - Why needed: turns measured cost into an envelope decision
   - Allowed input: machine/node specification with numeric limits

3. **Precision and operator storage policy**
   - Required fields: scalar precision and `matrix-free` versus explicit sparse/cache policy
   - Current source: absent
   - Why needed: controls bytes per value, RAM, and I/O
   - Allowed input: `complex64`, `complex128`, or an explicit mixed-precision contract; plus a storage policy retaining every pair inside `D_c`

4. **Eigensolver contract**
   - Required fields: solver type/backend, requested eigenpair count, spectral target/window, Krylov dimension, restart dimension
   - Current source: absent
   - Why needed: determines basis/workspace memory and matvec count
   - Allowed input: named solver/backend, positive integers, and an explicit spectral interval/target

5. **Remaining numerical tolerances**
   - Required fields: root, linear-solve, derivative, assembly, and observable tolerances; C0/C1/C2 tail allocations and Hodge slope margin where those observables are requested
   - Current source: PF-SCN-009, PF-KER-005, and PF-HOD-004 remain incomplete
   - Why needed: defines scientific acceptance and stopping rules
   - Allowed input: positive numeric tolerances with their norm/unit and observable scope

6. **Production schedule and concurrency**
   - Required fields: which frozen grids are combined, which are separate scans, adaptive sequencing, batch size, and maximum concurrent blocks/jobs
   - Current source: individual grids are frozen but the combined schedule is absent
   - Why needed: determines total work, peak RAM, and output volume
   - Allowed input: explicit list of scan blocks and positive concurrency limits

7. **Runtime budgets and recovery**
   - Required fields: accepted matvec budget, per-job/total wall-time budget, storage format, checkpoint interval
   - Current source: absent
   - Why needed: Resource PASS/FAIL is undefined without limits
   - Allowed input: numeric budgets with units and a checkpoint cadence

8. **Stochastic estimator selection**
   - Required fields: whether KPM and/or SLQ are in A1 scope; independent production RNG seeds if used
   - Current source: orders/probe counts are frozen, but production seeds and inclusion choice are absent
   - Why needed: closes reproducibility and workload cardinality
   - Allowed input: estimator selection and explicit integer seed namespaces

9. **Euclidean control inclusion**
   - Required field: whether the Euclidean full-2D mBZ calculation is part of the A1 resource gate
   - Current source: PF-EUC-003 grid/refinement/tolerance is missing
   - Why needed: avoids silently adding or excluding a substantial branch
   - Allowed input: `IN_A1_SCOPE` with grid/refinement/tolerance, or `NOT_IN_A1_SCOPE`

After these decisions, the implementation must still compute the exact `m_perp(theta,D_c)` support count for candidate 0005; that is an implementation result, not a value for the user to guess.
"""
(OUT / "A1_RESOURCE_INPUT_REQUEST.md").write_text(request.lstrip(), encoding="utf-8")

status = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "H_MATH": H_MATH,
    "MATHEMATICAL_STATUS": "PASS",
    "RESOURCE_STATUS": "UNVERIFIED",
    "PRODUCTION_A1_STATUS": "NOT_FROZEN",
    "production_mode": "UNSPECIFIED",
    "resource_contract_rows": len(rows),
    "missing_project_decision_rows": len(missing),
    "implementation_dependent_open_rows": len(implementation_open),
    "resource_contract_audit_sha256": sha256(audit_path),
    "resource_formula_sha256": sha256(OUT / "DETERMINISTIC_RESOURCE_FORMULAS.json"),
    "pilot_sha256": sha256(OUT / "INTRALAYER_MATRIX_FREE_PILOT.json"),
    "HPC_status": "NOT_TRIGGERED_FOR_PRODUCTION_RESOURCE_GATE",
    "HPC_note": "the full production task is not defined while mandatory project fields are absent; the bounded local pilot did not exhaust resources",
    "classification": "STATE_B_RESOURCE_UNVERIFIED_MISSING_SPECIFICATION",
}
(OUT / "RESOURCE_STATUS.json").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

preview_rows = [
    ("Constructive finite quotient found", "YES", "CAND-R4-0005 mathematical freeze"),
    ("Candidate", "CAND-R4-0005", "H_MATH root certificate"),
    ("Order", "46080", "exact generated group"),
    ("Exact C8", "PASS", "mathematical freeze"),
    ("Parity", "PASS", "mathematical freeze"),
    ("Physical shell", "PASS", "mathematical freeze"),
    ("Local injectivity", "PASS", "local independent replay"),
    ("Global systole", "PASS; sys/a_B>6", "dual complete scan"),
    ("Independent global replay", "PASS", "785639753/785639753, no hit"),
    ("Mathematical construction", "COMPLETE", H_MATH),
    ("mu(Q)", "92", "GAP exact minimum faithful degree"),
    ("mu_tr(Q)", "5120", "complete core-free subgroup certificate"),
    ("q24 relation", "RESOLVED_BRANCH_A; Q not in degree-24 domain", "mu_tr(Q)>24"),
    ("Resource gate", "UNVERIFIED", "mandatory fields missing"),
    ("Production mode", "UNSPECIFIED", "user/project decision required"),
    ("A1", "NOT FROZEN", "Resource Gate not PASS"),
    ("HPC", "NOT NEEDED FOR COMPLETED MATH; NOT TRIGGERED FOR UNDEFINED PRODUCTION TASK", "bounded pilots safe"),
]
preview_path = OUT / "WORKBOOK_UPDATE_PREVIEW.tsv"
with preview_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["Field", "Proposed value", "Evidence"], lineterminator="\n")
    writer.writeheader()
    for field, value, evidence in preview_rows:
        writer.writerow({"Field": field, "Proposed value": value, "Evidence": evidence})

print(json.dumps({
    "classification": status["classification"],
    "audit_rows": len(rows),
    "missing_project_decision_rows": len(missing),
    "implementation_open_rows": len(implementation_open),
    "Hilbert_dimension": N,
}, indent=2))
