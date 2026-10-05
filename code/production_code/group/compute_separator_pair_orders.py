"""Compute actual generated-image orders for exact two-column S4 covers."""

from __future__ import annotations

import json
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

from production_code.group.core import core_signature
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.quotient_candidate import POSITIVE_GENERATORS
from production_code.group.quotient_search_v2 import S4_ELEMENTS, V2Seed, base_s4_candidate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "production" / "quotient_separator"


def main() -> None:
    shortlist = json.loads((OUT / "separator_pair_shortlist.json").read_text(encoding="utf-8"))["smallest_cartesian_upper_bound_pairs"]
    records = {
        record["candidate_id"]: record
        for record in (
            json.loads(line)
            for line in (ROOT / "data" / "production" / "quotient_reaudit_geometric_shell_final" / "candidates_geometric_shell_reaudit.jsonl").read_text(encoding="utf-8").splitlines()
            if line
        )
    }
    bases = {}
    signatures = {}

    def context(candidate_id):
        if candidate_id not in bases:
            record = records[candidate_id]
            base = base_s4_candidate(V2Seed(candidate_id, tuple(record["base_generator_indices"])))
            bases[candidate_id] = base
            signatures[candidate_id] = {
                token: core_signature(base, (token,)) for token in POSITIVE_GENERATORS
            }
        return bases[candidate_id], signatures[candidate_id]

    results = []
    for pair in shortlist:
        left_base, left = context(pair["left_id"])
        right_base, right = context(pair["right_id"])
        generators = []
        for token in POSITIVE_GENERATORS:
            if left[token].parity_image != right[token].parity_image:
                raise AssertionError("shared parity drift")
            values = list(range(66))
            if left[token].parity_image:
                values[0], values[1] = 1, 0
            for factor, signature in enumerate((left[token], right[token])):
                offset = 2 + factor * 32
                for block, element_index in enumerate(signature.rotated_quotient_images):
                    permutation = S4_ELEMENTS[element_index]
                    block_offset = offset + block * 4
                    for point in range(4):
                        values[block_offset + point] = block_offset + permutation[point]
            generators.append(Permutation(values))
        actual_order = int(PermutationGroup(generators).order())
        geometric_pairs = []
        for index in range(8):
            word = GEOMETRIC_TO_STANDARD_WORD[index]
            geometric_pairs.append((core_signature(left_base, word), core_signature(right_base, word)))
        result = dict(pair)
        result.update({
            "actual_generated_image_order": actual_order,
            "shared_parity_fiber_product_upper_bound": pair["cartesian_order_upper_bound"] // 2,
            "physical_shell_distinct": len(set(geometric_pairs)) == 8,
        })
        results.append(result)
    results.sort(key=lambda item: (item["actual_generated_image_order"], item["left_column"], item["right_column"]))
    output = {
        "schema_version": "1.0",
        "scope": "exact based separator pair feasibility",
        "pairs_computed": len(results),
        "selection_not_claimed_globally_minimal_over_all_pairs": True,
        "best_computed_pair": results[0],
        "computed_pairs": results,
    }
    (OUT / "separator_pair_actual_orders.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pairs_computed": len(results), "best": results[0]}, indent=2))


if __name__ == "__main__":
    main()
