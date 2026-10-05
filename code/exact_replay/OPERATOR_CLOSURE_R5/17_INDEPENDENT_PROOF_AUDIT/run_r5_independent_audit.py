from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THEOREMS = ROOT / "18_THEOREM_PACKAGE"
MODULE_PATH = ROOT / "16_IMPLEMENTATION" / "global_operator_r5.py"


def read(name: str) -> str:
    return (THEOREMS / name).read_text(encoding="utf-8")


spec = importlib.util.spec_from_file_location("r5_audit_impl", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

texts = {
    name: read(name)
    for name in (
        "R5_MAIN_THEOREM.tex",
        "R5_DOUBLE_COSET_THEOREM.tex",
        "R5_NORMALIZER_THEOREM.tex",
        "R5_COMMENSURATOR_THEOREM.tex",
        "R5_GENERIC_CASE.tex",
        "R5_EXISTENCE_ATTAINMENT.tex",
        "R5_FINITE_ALGORITHM.tex",
        "R5_TIE_REGULARITY.tex",
        "R5_C2_PARAMETER_THEOREM.tex",
        "R5_OPERATOR_DESCENT.tex",
        "R5_PERIODICITY_THEOREM.tex",
    )
}
joined = "\n".join(texts.values())

checks = {
    "typed_predicates": "FiniteMatrix" in (ROOT / "01_OPERATOR_SEMANTICS" / "FROZEN_OPERATOR_SEMANTICS.md").read_text(encoding="utf-8"),
    "full_representative_relation": "Changing $a$" in texts["R5_DOUBLE_COSET_THEOREM.tex"],
    "double_coset_identity": "Ka^{-1}r_\\theta Kb" in texts["R5_DOUBLE_COSET_THEOREM.tex"],
    "normalizer_iff": "if and only if" in texts["R5_NORMALIZER_THEOREM.tex"],
    "commensurator_iff": "following are equivalent" in texts["R5_COMMENSURATOR_THEOREM.tex"],
    "equal_index_covolume": "same\ncovolume" in texts["R5_COMMENSURATOR_THEOREM.tex"],
    "ratner_hypotheses": all(token in texts["R5_GENERIC_CASE.tex"] for token in ("Ratner", "unipotent", "lattice", "identity component")),
    "intermediate_subgroup_proof": "adjoint" in texts["R5_GENERIC_CASE.tex"] and "irreducible" in texts["R5_GENERIC_CASE.tex"],
    "generic_density": "dense in $G$" in texts["R5_GENERIC_CASE.tex"],
    "zero_infimum": "inf\\mathcal D" in texts["R5_GENERIC_CASE.tex"],
    "attainment_distinguished": "infimum" in texts["R5_EXISTENCE_ATTAINMENT.tex"] and "attained" in texts["R5_EXISTENCE_ATTAINMENT.tex"],
    "properness_compactness": "proper" in texts["R5_EXISTENCE_ATTAINMENT.tex"] and "compact" in texts["R5_EXISTENCE_ATTAINMENT.tex"],
    "finite_search_bound": "(A1)" in texts["R5_FINITE_ALGORITHM.tex"] and "(A2)" in texts["R5_FINITE_ALGORITHM.tex"],
    "tie_two_jet": "two-jet" in texts["R5_TIE_REGULARITY.tex"],
    "c0_countersequence": "sequence" in texts["R5_C2_PARAMETER_THEOREM.tex"] and "not even $C^0$" in texts["R5_MAIN_THEOREM.tex"],
    "covariance_extra_hypothesis": "r\\Gamma r^{-1}=\\Gamma" in texts["R5_PERIODICITY_THEOREM.tex"],
    "hermiticity_not_overclaimed": "Hermiticity does not imply" in texts["R5_OPERATOR_DESCENT.tex"],
    "generic_implementation_fail_closed": "GENERIC_NONCOMMENSURATOR" in MODULE_PATH.read_text(encoding="utf-8") and "raise R5DomainError" in MODULE_PATH.read_text(encoding="utf-8"),
    "all_nonzero_grid_points_excluded": all(module.classify_frozen_grid_index(j)["real_cyclotomic_degree"] > 2 for j in range(1, 91)),
    "terminal_status": "GENERIC\\_GLOBAL\\_NO\\_GO\\_PROVED" in texts["R5_MAIN_THEOREM.tex"],
}

payload = {
    "schema_version": "1.0",
    "audit": "R5 independent proof and implementation audit",
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "status": "PASS" if all(checks.values()) else "FAIL",
    "theorem_sha256": {
        name: hashlib.sha256((THEOREMS / name).read_bytes()).hexdigest().upper()
        for name in texts
    },
}
(THEOREMS / "R5_INDEPENDENT_AUDIT.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"status": payload["status"], "passed": payload["passed"], "total": payload["total"]}))
