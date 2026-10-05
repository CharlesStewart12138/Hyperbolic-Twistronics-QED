"""Certify mu(Q), build the claim registry, and prepare paper integration."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
OUT = R4 / "20_POSTCONSTRUCTION"
PAPER = R4 / "PAPER_INTEGRATION_R4"
FIG = PAPER / "FIGURE_DATA"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


root = json.loads((R4 / "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json").read_text(encoding="utf-8"))
H_MATH = root["H_MATH"]
replay_path = R4 / "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_GAP_REPLAY.txt"
replay = replay_path.read_text(encoding="utf-8")
required_lines = {
    "GAP_VERSION": "4.16.0",
    "Q_ORDER": "46080",
    "INPUT_FAITHFUL_DEGREE": "92",
    "MU_Q": "92",
    "CLASSIFICATION": "PASS_EXACT",
}
observed = dict(line.split("=", 1) for line in replay.splitlines() if "=" in line)
if any(observed.get(key) != value for key, value in required_lines.items()):
    raise RuntimeError(f"mu(Q) replay mismatch: {observed}")

mu_cert_path = R4 / "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json"
mu_cert = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "H_MATH": H_MATH,
    "group_structure": "SL(2,9) x C4 x C4 x C2 x C2",
    "group_order": 46080,
    "mu": 92,
    "definition": "minimum degree of a faithful permutation representation, allowing multiple orbits",
    "exact_lower_bound_method": "GAP 4.16.0 MinimalFaithfulPermutationDegree on a faithful degree-92 compact direct-product action",
    "faithful_upper_witness": {
        "degree": 92,
        "orbit_sizes": [80, 2, 2, 4, 4],
        "construction": "direct product of an exact minimum faithful transitive degree-80 action of SL(2,9) and exact minimum degree-12 action of C4 x C4 x C2 x C2",
        "factor_minimum_degrees": {"SL(2,9)": 80, "C4 x C4 x C2 x C2": 12},
        "image_order": 46080,
    },
    "lower_degrees_excluded": "exact GAP minimum-faithful-degree algorithm returned 92",
    "verifier": {
        "GAP_version": "4.16.0",
        "replay_output": "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_GAP_REPLAY.txt",
        "replay_output_sha256": sha256(replay_path),
        "replay_script": "18_Q24_CLOSURE/replay_mu_q_compact_to_file.g",
        "replay_script_sha256": sha256(R4 / "18_Q24_CLOSURE/replay_mu_q_compact_to_file.g"),
        "compact_factor_images": "18_Q24_CLOSURE/minimal_factor_images.g",
        "compact_factor_images_sha256": sha256(R4 / "18_Q24_CLOSURE/minimal_factor_images.g"),
    },
    "separate_degrees": {
        "minimum_faithful_intransitive_mu": 92,
        "minimum_faithful_transitive_mu_tr": 5120,
        "regular_degree": 46080,
        "physical_single_particle_Hilbert_dimension": 92160,
    },
    "classification": "PASS_EXACT_MINIMUM_FAITHFUL_PERMUTATION_DEGREE",
}
mu_cert_path.write_text(json.dumps(mu_cert, indent=2) + "\n", encoding="utf-8")

claims = [
    ("A finite marked quotient Q exists", "PASS", "exact finite algebra plus computer-assisted exact certification", "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json", "There exists a certified marked quotient Q_* satisfying the stated gates."),
    ("|Q|=46080", "PASS", "exact generated finite group", "17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json", "The quotient has exact order 46,080."),
    ("Q is SL(2,9) x C4 x C4 x C2 x C2", "PASS", "exact GAP isomorphism and IdGroup", "18_Q24_CLOSURE/FACTOR_IDENTIFICATION_GAP.txt", "The certified quotient is isomorphic to the stated direct product."),
    ("C8 descends with exact order eight", "PASS", "exact automorphism table", "17_FINAL_FREEZE/artifacts/CAND-R4-0005.C8_automorphism_u32le.bin", "The Bolza order-eight automorphism descends with exact order eight."),
    ("Canonical parity descends", "PASS", "exact character table/vector", "17_FINAL_FREEZE/artifacts/CAND-R4-0005.parity_u8.bin", "The canonical parity character factors through Q_*."),
    ("Physical eight-direction shell is injective", "PASS", "exact finite algebra", "10_CANDIDATES/CAND-R4-0005.certificate.json", "The eight physical directions descend to distinct nonidentity elements."),
    ("Declared local B3 injectivity", "PASS", "complete exact local ball replay", "11_CERTIFICATES/CAND-R4-0005.local_independent_replay.json", "The declared local B_3 condition holds."),
    ("sys/a_B > 6", "PASS", "two complete exact closed-domain scans", "11_CERTIFICATES/CAND-R4-0005.global_independent_replay.json", "The global systole satisfies sys/a_B>6."),
    ("r_inj/a_B > 3", "PASS", "exact consequence r_inj=sys/2", "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json", "Hence r_inj/a_B>3."),
    ("mu(Q)=92", "PASS", "exact minimum faithful permutation computation", "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json", "The minimum faithful permutation degree allowing multiple orbits is 92."),
    ("mu_tr(Q)=5120", "PASS", "complete core-free subgroup classification", "18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_CERTIFICATE.json", "The minimum faithful transitive permutation degree is 5,120."),
    ("Q belongs to old degree-24 domain", "FAIL_EXACT_EXCLUSION", "mu_tr(Q)>24", "18_Q24_CLOSURE/Q24_RELATION_CERTIFICATE.md", "Q_* lies outside the historical faithful transitive degree-24 domain."),
    ("Both selected factors are necessary", "PASS_WITHIN_CURRENT_FACTORIZATION", "exact factor deletion", "12_MINIMIZATION/CAND-R4-0005.factor_deletion.json", "The construction is factor-irredundant within the declared two-factor factorization."),
    ("Order 46080 is globally minimal", "UNPROVED", "none", "", "Do not claim global minimum order."),
    ("Q is unique", "UNPROVED", "none", "", "Do not claim uniqueness."),
    ("Global classification is complete", "UNPROVED", "none", "", "Do not claim classification of all admissible quotients."),
    ("Resource feasibility", "UNVERIFIED", "incomplete authoritative contract", "19_RESOURCE_CLOSURE/RESOURCE_CONTRACT_AUDIT.tsv", "Resource feasibility remains unverified pending the listed project decisions and full interlayer support estimate."),
    ("Production mode", "UNSPECIFIED", "authoritative source audit", "19_RESOURCE_CLOSURE/A1_RESOURCE_INPUT_REQUEST.md", "Do not choose FULL-SPACE or REPRESENTATION-RESOLVED silently."),
    ("Representation completeness", "UNVERIFIED", "complete irrep inventory not constructed", "", "No representation-resolved spectral claim is made."),
    ("A1 production", "NOT_FROZEN", "Resource Gate not PASS", "19_RESOURCE_CLOSURE/RESOURCE_STATUS.json", "CAND-R4-0005 is mathematically frozen but not released as A1."),
    ("FULL-BULK convergence", "NOT_PROMOTED", "separate hypotheses remain open", "", "The finite-quotient theorem does not establish FULL-BULK spectral/projector/derivative convergence."),
]
claim_path = OUT / "FINAL_CLAIM_REGISTRY.tsv"
with claim_path.open("w", encoding="utf-8", newline="") as handle:
    fields = ["Claim", "Status", "Proof type", "Certificate", "Paper-allowed wording"]
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for claim, status, proof, cert, wording in claims:
        writer.writerow({"Claim": claim, "Status": status, "Proof type": proof, "Certificate": cert, "Paper-allowed wording": wording})

provenance = f"""
# Certification provenance

## Frozen result

The immutable mathematical root is `{H_MATH}`. Candidate `CAND-R4-0005` has exact order 46,080 and is certified independently against the complete closed global domain.

## Independent-v1 false positive

The first independent scanner used an independent 46,080-state group machine but tested the complete registry as if every record were dangerous. The registry deliberately contains a superset; the scanner omitted the exact trace-threshold filter and therefore reported a candidate-kernel element whose `|tr/2| = 11303+7992 sqrt(2)` lies above the frozen dangerous cutoff `2405+1700 sqrt(2)`.

The incident is preserved in `11_CERTIFICATES/CAND-R4-0005.independent_v1_false_hit_quarantine.json`. The corrected v2 scanner kept the independent group state machine, restored exact algebraic threshold filtering, scanned all 785,639,753 records, and returned zero dangerous kernel hits.

This is classified as a certification-only implementation bug caught before freeze. It did not alter the candidate or frozen mathematical conclusion. The v1 scanner is a regression fixture and is excluded from the PASS proof chain.
"""
(OUT / "CERTIFICATION_PROVENANCE.md").write_text(provenance.lstrip(), encoding="utf-8")
(PAPER / "CERTIFICATION_PROVENANCE.md").write_text(provenance.lstrip(), encoding="utf-8")

result_md = f"""
# Finite-quotient result for manuscript integration

We construct an explicit normal subgroup `K_*` of the Bolza surface group whose marked quotient `Q_*` has order 46,080 and abstract structure `SL(2,9) x C4 x C4 x C2 x C2`. The physical eight-direction shell remains injective, the Bolza automorphism descends with exact order eight, canonical parity descends, and the declared local `B_3` condition holds.

The global statement is computer-assisted exact certification rather than floating-point evidence. The closed domain contains 785,639,753 records, including the equality boundary at `6 a_B`. Two implementation-independent complete scans returned zero dangerous kernel hits. Thus `sys(H^2/K_*)/a_B>6` and `r_inj(H^2/K_*)/a_B>3`.

The result is an existence theorem, not an optimality or uniqueness theorem. Factor deletion proves only that both factors are necessary within the declared two-factor construction. Exact permutation degrees are `mu(Q_*)=92` and `mu_tr(Q_*)=5120`; consequently the quotient lies outside the old faithful transitive degree-24 search domain.

The mathematical result is frozen under `H_MATH={H_MATH}`. Resource feasibility and A1 production release remain separate and currently unverified because mandatory production settings are absent.
"""
(PAPER / "FINITE_QUOTIENT_RESULT.md").write_text(result_md.lstrip(), encoding="utf-8")

theorem_tex = r"""\begin{theorem}[Certified Bolza quotient]\label{thm:certified-bolza-quotient}
Let $\Gamma_B$ be the Bolza genus-two surface group with the frozen physical geometric shell, order-eight automorphism $\phi_8$, and canonical parity character $\chi$.  There exists a finite-index normal subgroup $K_*\triangleleft\Gamma_B$ such that
\[
Q_*:=\Gamma_B/K_*,\qquad |Q_*|=46080,
\]
with the following properties: (i) the eight physical directions have distinct nonidentity images; (ii) $\phi_8$ descends to an automorphism of $Q_*$ of exact order eight; (iii) $\chi$ factors through $Q_*$; (iv) the declared local $B_3$ injectivity condition holds; and (v)
\[
\operatorname{sys}(\mathbb H^2/K_*)>6a_B,
\qquad
r_{\mathrm{inj}}(\mathbb H^2/K_*)>3a_B.
\]
\end{theorem}

\noindent The theorem asserts existence at order $46080$; it does not assert minimum order, uniqueness, or a classification of all admissible quotients.
"""
(PAPER / "FINITE_QUOTIENT_THEOREM.tex").write_text(theorem_tex, encoding="utf-8")

proof_tex = r"""\paragraph{Proof architecture.}
The analytical construction theory supplies exact arithmetic and lower-exponent-$2$ class-$2$ quotient maps, the $C_8$-equivariant kernel-intersection rule, parity closure, and the finite exact dangerous-domain reduction.  Exact finite-algebra computation then constructs the marked image
\[
Q_*\cong \mathrm{SL}(2,9)\times C_4\times C_4\times C_2\times C_2
\]
of order $46080$, verifies the surface relation and marked generation, and checks the shell, $C_8$, parity, and complete local $B_3$ gates.

For the global gate, the frozen closed dangerous domain contains $785{,}639{,}753$ records and includes the equality boundary at $6a_B$.  A primary exact scanner and an independently implemented group-state scanner each traversed the complete domain, replayed the exact algebraic trace filter, and found no kernel hit.  Hence no nontrivial conjugacy class of translation length at most $6a_B$ lies in $K_*$, proving the strict systole inequality.  The injectivity-radius statement follows from $r_{\mathrm{inj}}=\operatorname{sys}/2$.  This separates the analytical reduction, finite exact algebra, and computer-assisted exact exhaustion.
"""
(PAPER / "FINITE_QUOTIENT_PROOF_SUMMARY.tex").write_text(proof_tex, encoding="utf-8")

construction_tex = r"""\paragraph{Constructive method.}
The quotient was obtained by a kernel-first counterexample-guided sequence.  An arithmetic factor at $p=3$ gives an exact image isomorphic to $\mathrm{SL}(2,9)$ of order $720$.  Exact global witnesses from intermediate candidates were then separated by a $C_8$-stable lower-exponent-$2$ class-$2$ quotient.  Exhaustion of all seven stable one-dimensional and nineteen stable two-dimensional central row spaces selected the nonnested row space $\langle6,9\rangle$, whose image is $C_4^2\times C_2^2$ of order $64$.  The generated diagonal image has order $720\cdot64=46080$ and therefore equals the full direct product.  Deleting either factor destroys the declared gates, so the factorization is irredundant within this construction; no global order-minimality claim is made.
"""
(PAPER / "CONSTRUCTION_METHOD_SUMMARY.tex").write_text(construction_tex, encoding="utf-8")

methods_tex = r"""\paragraph{Computer-assisted exact certification.}
All finite-group evaluations use canonical exact encodings.  The global domain is a frozen closed registry of $785{,}639{,}753$ records.  Two implementation-independent complete scans, including exact threshold filtering and the boundary case, returned zero dangerous kernel hits.  The post-scan independent endpoint audit passed $30/30$ checks and the frozen delivery manifest passed $20/20$ content hashes.  These computations constitute computer-assisted exact certification.  A first independent scanner that omitted the exact trace filter produced a false positive on a nondangerous superset element; it is quarantined as a regression fixture and contributes no PASS assertion.
"""
(PAPER / "CERTIFICATE_METHODS.tex").write_text(methods_tex, encoding="utf-8")

q24_tex = r"""\paragraph{Relation to the historical degree-24 search.}
The historical search covered faithful transitive permutation actions of degree $24$.  For
$Q_*\cong\mathrm{SL}(2,9)\times C_4^2\times C_2^2$, every core-free subgroup injects into a subgroup of $\mathrm{SL}(2,9)$ avoiding its central involution.  A complete audit of the $27$ subgroup conjugacy classes shows that the largest such subgroup is $C_3^2$ of order $9$.  Consequently
\[
\mu_{\mathrm{tr}}(Q_*)=46080/9=5120>24.
\]
Thus the successful quotient was outside the old search domain; it was not a missed degree-24 target.  Separately, the minimum faithful degree allowing multiple orbits is $\mu(Q_*)=92$.
"""
(PAPER / "Q24_HISTORICAL_RELATION.tex").write_text(q24_tex, encoding="utf-8")

resource_tex = r"""\paragraph{Resource and production status.}
For the two-layer one-orbital model the physical single-particle dimension is $2|Q_*|=92160$.  The mathematical quotient is certified, but the Resource Gate is currently \texttt{UNVERIFIED}: the authoritative project record does not select the typed production mode and does not freeze several mandatory solver, precision, runtime, concurrency, tolerance, and storage coordinates.  Accordingly the quotient is not yet frozen as production Level A1.  This resource status does not weaken the mathematical theorem.
"""
(PAPER / "RESOURCE_STATUS.tex").write_text(resource_tex, encoding="utf-8")

table_tex = r"""\begin{table}[t]
\centering
\caption{Certified status of the constructive quotient.}
\label{tab:cand-r4-0005}
\begin{tabular}{ll}
\hline
Candidate & CAND-R4-0005\\
Abstract group & $\mathrm{SL}(2,9)\times C_4^2\times C_2^2$\\
Order & $46080$\\
Physical Hilbert dimension & $92160$\\
Exact $C_8$ / parity / shell & PASS / PASS / PASS\\
Local $B_3$ & PASS\\
Global systole & $\operatorname{sys}/a_B>6$\\
Primary / independent scan & $785{,}639{,}753$ / $785{,}639{,}753$, no hit\\
$\mu(Q)$ / $\mu_{\mathrm{tr}}(Q)$ & $92$ / $5120$\\
Order optimality / uniqueness & UNPROVED / UNPROVED\\
Resource / A1 & UNVERIFIED / NOT FROZEN\\
\hline
\end{tabular}
\end{table}
"""
(PAPER / "TABLE_CAND_R4_0005.tex").write_text(table_tex, encoding="utf-8")

with (FIG / "CEGAR_ITERATIONS.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["candidate", "order", "terminal_gate", "result"])
    writer.writerows([
        ["CAND-R4-0001", 31200, "local_B3", "FAIL"],
        ["CAND-R4-0002", 11520, "global_systole", "FAIL_EXACT_WITNESS"],
        ["CAND-R4-0003", 23040, "global_systole", "FAIL_EXACT_WITNESS"],
        ["CAND-R4-0004", 46080, "global_systole", "FAIL_EXACT_WITNESS"],
        ["CAND-R4-0005", 46080, "global_systole", "PASS_COMPLETE_CLOSED_DOMAIN"],
    ])
with (FIG / "GLOBAL_SCAN_SUMMARY.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["implementation", "records", "kernel_hits", "result"])
    writer.writerow(["primary", 785639753, 0, "PASS"])
    writer.writerow(["independent_v2", 785639753, 0, "PASS"])

bib = """
# Bibliography notes

- Cite the project construction-theory source for the arithmetic residual-finiteness, C8 orbit-core, class-2 p-quotient, and exact dangerous-domain reduction theorems.
- Cite a standard finite-group reference for `SL(2,9)` and core-free subgroup/permutation-degree terminology if the journal requires external background.
- The candidate-specific existence, scan counts, hashes, and q24 relation are original computer-assisted results and should cite the archived certificate repository/data availability statement, not an unrelated catalogue search.
- Do not cite the old degree-24 numerical zero as proof of the new theorem. Its role is historical scope comparison only.
"""
(PAPER / "BIBLIOGRAPHY_NOTES.md").write_text(bib.lstrip(), encoding="utf-8")

manifest_rows = []
for path in sorted(PAPER.rglob("*")):
    if path.is_file():
        manifest_rows.append({"path": path.relative_to(PAPER).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
(PAPER / "PAPER_INTEGRATION_MANIFEST.json").write_text(json.dumps({
    "schema_version": "1.0",
    "classification": "PASS_STANDALONE_INTEGRATION_PACKAGE",
    "candidate_id": "CAND-R4-0005",
    "H_MATH": H_MATH,
    "main_manuscript_modified": False,
    "files": manifest_rows,
}, indent=2) + "\n", encoding="utf-8")

print(json.dumps({
    "mu_Q": 92,
    "claim_registry_rows": len(claims),
    "paper_package_files": len(manifest_rows) + 1,
    "H_MATH": H_MATH,
    "classification": "PASS_POSTCONSTRUCTION_CLAIMS_AND_PAPER_PACKAGE",
}, indent=2))
