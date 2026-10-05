"""Build the exact minimum-transitive-degree and q24-closure certificates."""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
Q_ORDER = 46080


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def canonical_subgroup_id(element_ids: str) -> tuple[str, str]:
    payload = ",".join(str(x) for x in sorted(int(v) for v in element_ids.split(",") if v != ""))
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest().upper()
    return f"A-SUB-{digest[:20]}", digest


raw_path = HERE / "SL2_9_SUBGROUP_CLASSES_RAW.tsv"
raw_text = raw_path.read_text(encoding="utf-8").replace("\\\n", "").replace("\\\r\n", "")
reader = csv.DictReader(io.StringIO(raw_text), delimiter="\t")
raw_rows = list(reader)
if len(raw_rows) != 27:
    raise RuntimeError(f"expected 27 subgroup classes, got {len(raw_rows)}")

rows = []
for raw in raw_rows:
    subgroup_id, set_hash = canonical_subgroup_id(raw["element_ids"])
    order = int(raw["order"])
    contains_center = raw["contains_center"] == "true"
    core_order = int(raw["core_order"])
    rows.append({
        "canonical_subgroup_id": subgroup_id,
        "subgroup_element_set_sha256": set_hash,
        "order": order,
        "index_in_SL2_9": int(raw["index_in_A"]),
        "contains_center": str(contains_center).upper(),
        "core_order_in_SL2_9": core_order,
        "structure": raw["structure"],
        "generator_element_ids_zero_based": raw["generator_element_ids"],
        "eligible_as_core_free_projection": str((not contains_center) and core_order == 1).upper(),
        "source_class_index_nonpersistent": int(raw["class_index"]),
    })

clean_path = HERE / "SL2_9_SUBGROUP_CLASS_AUDIT.tsv"
with clean_path.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

eligible = [row for row in rows if row["eligible_as_core_free_projection"] == "TRUE"]
max_order = max(row["order"] for row in eligible)
witness = next(row for row in eligible if row["order"] == max_order)
mu_tr = Q_ORDER // max_order
if max_order != 9 or mu_tr != 5120 or witness["core_order_in_SL2_9"] != 1:
    raise RuntimeError("unexpected core-free maximum")

reject_path = HERE / "MIN_TRANSITIVE_DEGREE_SMALLER_INDEX_REJECTIONS.tsv"
with reject_path.open("w", encoding="utf-8", newline="") as handle:
    fields = ["candidate_index", "divides_group_order", "required_stabilizer_order", "status", "exact_reason"]
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for index in range(1, mu_tr):
        divides = Q_ORDER % index == 0
        required = Q_ORDER // index if divides else ""
        if not divides:
            status = "REJECTED_NOT_AN_INDEX"
            reason = "index does not divide |Q| (Lagrange)"
        else:
            status = "REJECTED_CORE_FREE_ORDER_BOUND"
            reason = f"would require a core-free stabilizer of order {required}>9, but every core-free stabilizer injects into a center-avoiding subgroup of SL(2,9), whose complete maximum is 9"
        writer.writerow({
            "candidate_index": index,
            "divides_group_order": str(divides).upper(),
            "required_stabilizer_order": required,
            "status": status,
            "exact_reason": reason,
        })

h_math = json.loads((R4 / "17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json").read_text(encoding="utf-8"))["H_MATH"]
factor_id_text = (HERE / "FACTOR_IDENTIFICATION_GAP.txt").read_text(encoding="utf-8")
if "A_STRUCTURE=SL(2,9)" not in factor_id_text or "B_STRUCTURE=C4 x C4 x C2 x C2" not in factor_id_text:
    raise RuntimeError("factor identification replay mismatch")

cert = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "H_MATH": h_math,
    "group": {
        "order": Q_ORDER,
        "structure": "SL(2,9) x C4 x C4 x C2 x C2",
        "factor_identification_replay": "18_Q24_CLOSURE/FACTOR_IDENTIFICATION_GAP.txt",
        "factor_identification_replay_sha256": sha256(HERE / "FACTOR_IDENTIFICATION_GAP.txt"),
    },
    "definition": "mu_tr(Q)=min{[Q:L] : L<=Q and core_Q(L)=1}",
    "mu_tr": mu_tr,
    "witness_subgroup": {
        "canonical_subgroup_id": witness["canonical_subgroup_id"],
        "structure": witness["structure"],
        "order": witness["order"],
        "index_in_Q": mu_tr,
        "generator_set_in_frozen_A_element_ids_then_B_identity": [[int(x), 0] for x in witness["generator_element_ids_zero_based"].split(",") if x],
        "subgroup_element_set_sha256": witness["subgroup_element_set_sha256"],
        "core_in_SL2_9_order": witness["core_order_in_SL2_9"],
        "core_in_Q_order": 1,
    },
    "exact_reduction_proof": [
        "Write Q=A x B with A=SL(2,9) and B=C4 x C4 x C2 x C2 central.",
        "If L is core-free in Q then L intersect B=1, because every element of L intersect B is central in Q and hence belongs to core_Q(L).",
        "Therefore projection L->A is injective and |L|=|H| for H=pi_A(L).",
        "If H contains the central involution z of A, its unique lift (z,b) in L is central in Q, contradicting core-freeness. Thus H avoids Z(A).",
        "The complete 27-class subgroup audit of A proves that every subgroup avoiding Z(A) has order at most 9.",
        "The certified subgroup H=C3 x C3 of order 9 avoids Z(A) and has trivial core in A; H x 1 has trivial core in Q.",
        "Hence the maximum core-free stabilizer order is exactly 9 and mu_tr(Q)=46080/9=5120.",
    ],
    "complete_exclusion": {
        "SL2_9_subgroup_conjugacy_classes": 27,
        "maximum_center_avoiding_order": 9,
        "subgroup_audit": "18_Q24_CLOSURE/SL2_9_SUBGROUP_CLASS_AUDIT.tsv",
        "subgroup_audit_sha256": sha256(clean_path),
        "every_smaller_integer_index_1_through_5119": "18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_SMALLER_INDEX_REJECTIONS.tsv",
        "smaller_index_rejection_sha256": sha256(reject_path),
        "smaller_index_rows": mu_tr - 1,
    },
    "canonical_identifier_policy": "SHA256 of the sorted zero-based element IDs in the frozen A-factor regular enumeration; GAP class ordinals are retained only as nonpersistent provenance",
    "verifier": {
        "GAP_version": "4.16.0",
        "GAP_subgroup_enumerator": "18_Q24_CLOSURE/enumerate_sl2_9_subgroups.g",
        "GAP_subgroup_enumerator_sha256": sha256(HERE / "enumerate_sl2_9_subgroups.g"),
        "raw_output_sha256": sha256(raw_path),
        "certificate_builder_sha256": sha256(Path(__file__)),
    },
    "classification": "PASS_EXACT_MINIMUM_TRANSITIVE_DEGREE",
}
(HERE / "MIN_TRANSITIVE_DEGREE_CERTIFICATE.json").write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")

q24 = f"""
# q24 relation certificate

## Certified objects

- Successful marked quotient: `CAND-R4-0005`.
- Abstract group: `Q = SL(2,9) x C4 x C4 x C2 x C2`.
- Exact order: `|Q| = 46080`.
- Exact minimum faithful transitive permutation degree: `mu_tr(Q) = 5120`.
- Mathematical root: `{h_math}`.

## Old search domain

The historical q24 workflow enumerated transitive permutation groups/actions of degree 24 together with marked generators, C8 automorphisms, parity, and geometric gates. A quotient belongs to that faithful marked-quotient discovery domain only if it admits a faithful transitive action of degree 24.

## Exact exclusion

Every core-free subgroup of `Q` has order at most 9. The maximum is attained by an embedded `C3 x C3`, so the smallest faithful transitive action has degree

`[Q:L] = 46080/9 = 5120`.

Therefore `mu_tr(Q)=5120>24` and

`Q_NOT_IN_DEGREE24_DOMAIN = TRUE`.

The old Degree-24 search could not have discovered `CAND-R4-0005` as a faithful transitive degree-24 quotient. This is a domain exclusion, not a missed-target implementation failure. The 905 old shards need not be reopened.

## Logical status

`FINITE_QUOTIENT_THEORY_STATUS = CLOSED`  
`q24_RELATION = RESOLVED_BRANCH_A`  
`OLD_Q24_SHOULD_HAVE_CONTAINED_SUCCESSFUL_MARKED_QUOTIENT = NO`
"""
(HERE / "Q24_RELATION_CERTIFICATE.md").write_text(q24.lstrip(), encoding="utf-8")

(HERE / "FINITE_QUOTIENT_THEORY_STATUS.json").write_text(json.dumps({
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "H_MATH": h_math,
    "MATHEMATICAL_STATUS": "PASS",
    "mu_tr": 5120,
    "q24_RELATION": "RESOLVED_BRANCH_A",
    "Q_NOT_IN_DEGREE24_DOMAIN": True,
    "FINITE_QUOTIENT_THEORY_STATUS": "CLOSED",
    "old_q24_restart_required": False,
    "certificate_sha256": sha256(HERE / "MIN_TRANSITIVE_DEGREE_CERTIFICATE.json"),
}, indent=2) + "\n", encoding="utf-8")

print(json.dumps({
    "classification": cert["classification"],
    "mu_tr": mu_tr,
    "witness_subgroup": witness["canonical_subgroup_id"],
    "smaller_indices_rejected": mu_tr - 1,
    "q24_relation": "RESOLVED_BRANCH_A",
}, indent=2))
