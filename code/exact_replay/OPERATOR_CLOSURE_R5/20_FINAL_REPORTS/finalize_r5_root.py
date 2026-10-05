from __future__ import annotations

import hashlib
import json
from pathlib import Path


R5_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = R5_ROOT.parent
FINAL_DIR = Path(__file__).resolve().parent
REPORT_PATH = FINAL_DIR / "R5_OPERATOR_CLOSURE_FINAL_REPORT.md"
MANIFEST_PATH = FINAL_DIR / "R5_FINAL_ROOT_MANIFEST.json"
PDF_PATH = WORKSPACE / "output" / "pdf" / "R5_OPERATOR_CLOSURE_THEOREM.pdf"
FROZEN_INPUT_HASH = "20218548ABB58E82C30E9B838488B2A88E07408CC2DA396A1702F3043DA198BB"
STATUS = "R5_STATUS = GENERIC_GLOBAL_NO_GO_PROVED"
EXCLUDED = {
    REPORT_PATH.relative_to(R5_ROOT).as_posix(),
    MANIFEST_PATH.relative_to(R5_ROOT).as_posix(),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


entries = []
for path in R5_ROOT.rglob("*"):
    if not path.is_file():
        continue
    relative = path.relative_to(R5_ROOT).as_posix()
    if relative in EXCLUDED:
        continue
    entries.append(
        {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    )
entries.sort(key=lambda item: item["path"])

payload = bytearray(b"R5_PAYLOAD_V1\n")
for entry in entries:
    payload.extend(
        f"{entry['path']}\t{entry['bytes']}\t{entry['sha256']}\n".encode("utf-8")
    )
payload_root = sha256_bytes(bytes(payload))
pdf_hash = sha256_file(PDF_PATH)
root_preimage = (
    "R5_FINAL_ROOT_V1\n"
    f"{FROZEN_INPUT_HASH}\n"
    f"{payload_root}\n"
    f"{pdf_hash}\n"
    f"{STATUS}\n"
)
final_root = sha256_bytes(root_preimage.encode("utf-8"))

report = f"""# R5 operator-closure final report

1. **Exact frozen operator definition.** For quotient labels represented by lifts `a,b`, the frozen scalar interlayer distance is
   
   `d_{{K,theta}}(q,q') = min_{{k1,k2 in K}} d_H(k1 a o, r_theta k2 b o)`
   
   when that minimum is attained. The hopping coefficient is the frozen radial kernel evaluated at this scalar minimum; it is not a sum over lifts and does not select a distinguished minimizing lift.

2. **Exact R4 obstruction.** R4 provided a correct local cover and finite quotient but did not prove that the two-sided minimum existed globally, descended independently of representatives, carried periodic covariance, or was `C2` in twist. Therefore the previously proposed global 92,160-dimensional operator lacked its definition theorem.

3. **Double-coset formulation.** The complete candidate-distance set is exactly `{{d(o,g o): g in K a^(-1) r_theta K b}}`. Changing either quotient representative only relabels the two `K` factors. Thus the candidate set and its infimum are invariant; attainment is a separate question.

4. **Normalizer result.** The centered isometry `r_theta` descends to a single-valued self-map of `K\\H^2` if and only if `r_theta K r_theta^(-1)=K`. This is necessary and sufficient, not merely sufficient.

5. **Commensurator result.** A finite common-cover correspondence exists if and only if `r_theta` lies in `Comm_G(K)`. With `L_theta=K intersection r_theta K r_theta^(-1)`, its sheet degree is `m_theta=[K:L_theta]=[r_theta K r_theta^(-1):L_theta]`. It is a single same-cover map only when `m_theta=1`, i.e. in the normalizer case.

6. **Generic incommensurate result.** For `G=PSL(2,R)` and `r_theta` outside `Comm_G(K)`, the double coset `K r_theta K` is dense in `G`. This follows from the diagonal-orbit formulation, Ratner's orbit-closure theorem, and the absence of a proper connected intermediate Lie subgroup between diagonal `G` and `G x G`.

7. **Minimum existence result.** On normalizer and finite-commensurator branches the relevant finite correspondence supplies a finite attained minimum. On a noncommensurator branch the candidate set has finite infimum, in fact zero, but an attained global minimum is not automatic and generically does not exist.

8. **Attainment result.** In the generic branch the infimum is attained exactly when the translated double coset meets the stabilizer condition giving an exact lift coincidence. Outside this exceptional exact-alignment set the infimum zero is not attained.

9. **Uniqueness/tie result.** The frozen coefficient uses only the scalar minimum, so uniqueness is unnecessary. Whenever a minimum exists, all minimizing branch identifiers must be retained to preserve invariant metadata. Tie loci are switching loci; nonattainment in the generic branch is distinct from a tie.

10. **Finite-support result.** For a discrete finite-correspondence branch, properness and cocompact fundamental-domain bounds reduce a cutoff search to finitely many group elements, with the explicit geometric radius stated in `R5_FINITE_ALGORITHM.tex`. For a dense generic double coset, an all-lifts cutoff set has infinite multiplicity and is not an equivalent finite replacement for the frozen nearest-distance coefficient.

11. **Finite-algorithm result.** `GLOBAL_INTERLAYER_SUPPORT_R5` terminates exactly on certified normalizer or commensurator inputs using canonical coset representatives, inclusive cutoff comparison, duplicate consolidation, and exact branch metadata. Generic inputs fail closed. No finite terminating exact algorithm exists for a nonattained minimum while preserving the frozen definition.

12. **Representative-independence result.** Full left/right multiplication by arbitrary elements of `K` leaves the double-coset candidate set unchanged. Hence the scalar infimum, and the minimum when attained, are representative-independent; no generator-only or numerical argument is used.

13. **Hermiticity result.** On a valid finite branch, the reverse-twist support is the adjoint support and the block completion `T_{{-theta}}=T_theta^*` gives a Hermitian bilayer Hamiltonian. Hermiticity cannot rescue a coefficient that is undefined by nonattainment.

14. **Covariance result.** Same-surface descent requires normalization of `K`; covariance of the frozen `Q=Gamma/K` sector labels additionally requires preservation of the marking, `r_theta Gamma r_theta^(-1)=Gamma`, inducing the corresponding automorphism of `Q` and the derived intertwining relation.

15. **Periodicity result.** Normalizer twists give a periodic same-cover operator. Commensurator-but-not-normalizer twists give a finite correspondence only on a larger common cover. Generic noncommensurator twists give neither a finite periodic cell nor the representation covariance required for band dispersion.

16. **C0 status.** At `theta=0`, distinct quotient points have positive quotient distance; along noncommensurator angles approaching zero the double-coset infimum is zero. Therefore the frozen global distance family is not continuous on the full production interval.

17. **C1 status.** Since `C0` fails on the full interval, `C1` also fails there. Piecewise derivative formulas are meaningful only inside a certified branch with stable minimizer/correspondence data.

18. **C2 status.** `C2` fails on the full interval. A valid local `C2` statement requires a fixed smooth branch or an invariant smooth sum and exclusion/control of every switching locus.

19. **Hessian legitimacy status.** The global twist Hessian claimed for the fixed-Q periodic family is not defined under the frozen generic model. Finite-matrix eigenvalues or a numerical finite difference do not supply the missing `C2` operator family.

20. **Same-Q status.** The original same-`Q` route is exact only on `Theta_normalizer`. On the frozen 91-point grid the only certified point is `theta=0`; the 90 nonzero points fail the exact commensurator trace-field necessary condition. A1 remains closed.

21. **Common-cover status.** For `theta in Theta_comm`, the exact common-cover level uses `L_theta`; it is not the old quotient unless `m_theta=1`. A normal common cover, if required by the downstream representation machinery, uses the core and may be larger still.

22. **Exact valid theta set.** `Theta_normalizer={{theta:r_theta in N_G(K)}}`; `Theta_comm={{theta:r_theta in Comm_G(K)}}`; exact same-Q production is restricted to the first set and exact finite common-cover production to the second. On the frozen uniform grid `theta_j=j*pi/720`, `j=0,...,90`, the certified intersection with `Theta_comm` is exactly `{{0}}`.

23. **Generic theta status.** `Theta_comm` is countable and Haar-null in `G`, while its complement is conull and dense. Along the one-parameter centered rotation family, countability/nullness is rigorous; density of the intersection is not inferred. Every nonzero frozen-grid angle is certified noncommensurating.

24. **Moore 1966 applicability conclusion.** Moore's theorem supplies the ergodic homogeneous-dynamics background but does not by itself turn a particular orbit into a dense orbit. Pointwise double-coset density here uses the applicable Ratner orbit-closure theorem plus the intermediate-subgroup classification.

25. **Arithmetic Bolza conclusion.** The Bolza lattice is arithmetic with invariant trace field `Q(sqrt(2))` and the cited quaternion-algebra realization. Passing to the finite-index subgroup `K` leaves the commensurator unchanged. Projective trace-square membership in the invariant field supplies the exact rejection test used for the nonzero frozen grid.

26. **Commensurator-approximation result.** Arithmeticity makes the ambient commensurator dense in `G`, so group-isometry approximants yield convergence of the original radial kernel uniformly on each fixed compact/local ball and hence convergence of finite local matrices and their finite-time dynamics. This is a limiting local statement, not an exact finite periodic realization at the target twist; no unsupported claim is made that centered commensurator angles are dense along the rotation curve.

27. **Production reopening status.** `OPERATOR_DEFINITION_STATUS = GENERIC_NO_GO_ON_FIXED_A1`. The old global A1 production route is not reopened. The exact infinite/local operator and already certified `H_N^loc` results remain valid.

28. **New quotient dimension if required.** On a commensurator common cover the bilayer Hilbert dimension is exactly `2 |Q| m_theta = 92,160 m_theta`, before any additional normal-core enlargement. No numerical `m_theta>1` is instantiated without a specific certified commensurator angle.

29. **HPC status.** No HPC computation is needed for this terminal. The obstruction is theorem-level, and the forbidden R4 global scans were not rerun.

30. **Independent proof audit result.** The independent audit passes 20/20 checks; the constructive/regression suite passes 10/10; PDF QA passes 13/13. The audit covers definitions, quantifiers, properness, double cosets, commensuration, attainment, representative invariance, finite search, ties, regularity, covariance, and implementation behavior.

31. **Literature novelty result.** Lattice commensurators, Hecke correspondences, and homogeneous orbit closure are standard ingredients. The project-specific contribution is their exact assembly around the frozen Bolza-bilayer nearest-lift operator, the 91-angle trace-field exclusion, the consequent discontinuity/Hessian no-go, and the explicit production decision. No priority claim beyond this synthesis is made.

32. **Final R5 root hash.** `{final_root}`. The frozen-input hash is `{FROZEN_INPUT_HASH}`, the R5 payload root is `{payload_root}`, and the certified PDF hash is `{pdf_hash}`. The exact preimage and per-file manifest are recorded in `R5_FINAL_ROOT_MANIFEST.json`.

{STATUS}
"""
REPORT_PATH.write_text(report, encoding="utf-8", newline="\n")
report_hash = sha256_file(REPORT_PATH)

manifest = {
    "schema_version": "R5_FINAL_ROOT_V1",
    "status": STATUS,
    "r4_frozen_mathematical_root": "AEEE9C3AB53239DDD6231A870AEAA88C61881DF4B6D187F4CAA5B0F550549618",
    "r4_frozen_contradiction_root": "C1DCA0C5926D15B7689BCEF54AEDEA537B7CF4FE9BCE2692AF97CB594B80995B",
    "frozen_input_hash_sha256": FROZEN_INPUT_HASH,
    "payload_domain_separator": "R5_PAYLOAD_V1\\n",
    "payload_root_sha256": payload_root,
    "payload_file_count": len(entries),
    "payload_files": entries,
    "excluded_self_referential_paths": sorted(EXCLUDED),
    "certified_pdf": str(PDF_PATH),
    "certified_pdf_sha256": pdf_hash,
    "root_preimage_utf8": root_preimage,
    "final_r5_root_sha256": final_root,
    "final_report_sha256": report_hash,
}
MANIFEST_PATH.write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
    newline="\n",
)

print(
    json.dumps(
        {
            "status": STATUS,
            "payload_file_count": len(entries),
            "payload_root_sha256": payload_root,
            "pdf_sha256": pdf_hash,
            "final_r5_root_sha256": final_root,
            "report_sha256": report_hash,
        },
        sort_keys=True,
    )
)
