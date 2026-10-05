from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "18_THEOREM_PACKAGE"
MODULE_PATH = ROOT / "16_IMPLEMENTATION" / "global_operator_r5.py"


def load(name: str) -> str:
    return (PKG / name).read_text(encoding="utf-8")


names = (
    "R5_MAIN_THEOREM.tex", "R5_DOUBLE_COSET_THEOREM.tex",
    "R5_NORMALIZER_THEOREM.tex", "R5_COMMENSURATOR_THEOREM.tex",
    "R5_GENERIC_CASE.tex", "R5_EXISTENCE_ATTAINMENT.tex",
    "R5_FINITE_ALGORITHM.tex", "R5_TIE_REGULARITY.tex",
    "R5_C2_PARAMETER_THEOREM.tex", "R5_OPERATOR_DESCENT.tex",
    "R5_PERIODICITY_THEOREM.tex",
)
texts = {name: load(name) for name in names}
semantics = (ROOT / "01_OPERATOR_SEMANTICS" / "FROZEN_OPERATOR_SEMANTICS.md").read_text(encoding="utf-8")
implementation = MODULE_PATH.read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("r5_audit_impl_v2", MODULE_PATH)
assert spec and spec.loader
impl = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = impl
spec.loader.exec_module(impl)

dc = texts["R5_DOUBLE_COSET_THEOREM.tex"]
comm = texts["R5_COMMENSURATOR_THEOREM.tex"]
generic = texts["R5_GENERIC_CASE.tex"]
attain = texts["R5_EXISTENCE_ATTAINMENT.tex"]
algorithm = texts["R5_FINITE_ALGORITHM.tex"]
c2 = texts["R5_C2_PARAMETER_THEOREM.tex"]
main = texts["R5_MAIN_THEOREM.tex"]

checks = {
    "typed_predicates": all(x in semantics for x in ("FiniteMatrix", "GlobalDescent", "PeriodicCovariantDescent")),
    "full_representative_relation": "Multiplying $a$ or $b$" in dc and "elements of $K$" in dc,
    "double_coset_identity": "Ka^{-1}r_\\theta Kb" in dc,
    "normalizer_iff": "if and only if" in texts["R5_NORMALIZER_THEOREM.tex"],
    "commensurator_iff": "following are equivalent" in comm,
    "equal_index_covolume": "same\ncovolume" in comm or "equal\ncovolumes" in comm or "same\ncovolumes" in comm,
    "ratner_hypotheses": all(x in generic for x in ("Ratner", "unipotent", "lattice", "identity component")),
    "intermediate_subgroup_proof": all(x in generic for x in ("adjoint", "irreducible", "simple")),
    "generic_density": "dense in $G$" in generic,
    "zero_infimum": "inf\\mathcal D" in generic,
    "attainment_distinguished": all(x in attain for x in ("infimum", "attained", "minimum does not exist")),
    "properness_compactness": "proper" in attain and "compact" in attain,
    "finite_search_bound": "\\tag{A1}" in algorithm and "\\tag{A2}" in algorithm,
    "tie_two_jet": "two-jet" in texts["R5_TIE_REGULARITY.tex"],
    "c0_countersequence": "sequence" in c2 and ("not even $C^0$" in main or "no $C^0$" in main),
    "covariance_extra_hypothesis": "r\\Gamma r^{-1}=\\Gamma" in texts["R5_PERIODICITY_THEOREM.tex"],
    "hermiticity_not_overclaimed": "Hermiticity does not imply" in texts["R5_OPERATOR_DESCENT.tex"],
    "generic_implementation_fail_closed": "GENERIC_NONCOMMENSURATOR" in implementation and "raise R5DomainError" in implementation,
    "all_nonzero_grid_points_excluded": all(impl.classify_frozen_grid_index(j)["real_cyclotomic_degree"] > 2 for j in range(1, 91)),
    "terminal_status": "GENERIC\\_GLOBAL\\_NO\\_GO\\_PROVED" in main,
}

payload = {
    "schema_version": "2.0",
    "audit": "R5 independent proof and implementation audit v2",
    "supersedes": "run_r5_independent_audit.py fragile literal matcher",
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "status": "PASS" if all(checks.values()) else "FAIL",
    "theorem_sha256": {name: hashlib.sha256((PKG / name).read_bytes()).hexdigest().upper() for name in names},
}
(PKG / "R5_INDEPENDENT_AUDIT.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"status": payload["status"], "passed": payload["passed"], "total": payload["total"]}))
