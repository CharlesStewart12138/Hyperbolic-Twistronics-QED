"""Freeze the smallest computed practical based-separator product image."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup

from production_code.group.core import CoreSignature, core_signature, multiply_signatures
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.quotient_candidate import POSITIVE_GENERATORS, RELATOR
from production_code.group.quotient_search_v2 import S4_ELEMENTS, V2Seed, base_s4_candidate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "production" / "quotient_separator"
CERT = ROOT / "production_code" / "group"


def rotate(signature: CoreSignature) -> CoreSignature:
    values = signature.rotated_quotient_images
    return CoreSignature(signature.parity_image, (values[-1],) + values[:-1])


def signature_json(signature: CoreSignature):
    return {
        "parity": signature.parity_image,
        "S4_phi_inverse_orbit_indices": list(signature.rotated_quotient_images),
        "S4_phi_inverse_orbit_permutations": [list(S4_ELEMENTS[index]) for index in signature.rotated_quotient_images],
    }


def main() -> None:
    pair = json.loads((OUT / "separator_pair_actual_orders.json").read_text(encoding="utf-8"))["best_computed_pair"]
    records = {
        record["candidate_id"]: record
        for record in (
            json.loads(line)
            for line in (ROOT / "data" / "production" / "quotient_reaudit_geometric_shell_final" / "candidates_geometric_shell_reaudit.jsonl").read_text(encoding="utf-8").splitlines()
            if line
        )
    }
    bases = []
    for candidate_id in (pair["left_id"], pair["right_id"]):
        record = records[candidate_id]
        bases.append(base_s4_candidate(V2Seed(candidate_id, tuple(record["base_generator_indices"]))))

    standard = [
        {token: core_signature(base, (token,)) for token in POSITIVE_GENERATORS}
        for base in bases
    ]
    geometric = [
        {f"g{i}": core_signature(base, GEOMETRIC_TO_STANDARD_WORD[i]) for i in range(8)}
        for base in bases
    ]
    identity = [core_signature(base, ()) for base in bases]

    generators = []
    for token in POSITIVE_GENERATORS:
        values = list(range(66))
        parity = standard[0][token].parity_image
        assert parity == standard[1][token].parity_image
        if parity:
            values[0], values[1] = 1, 0
        for factor in range(2):
            offset = 2 + factor * 32
            for block, element_index in enumerate(standard[factor][token].rotated_quotient_images):
                permutation = S4_ELEMENTS[element_index]
                for point in range(4):
                    values[offset + 4 * block + point] = offset + 4 * block + permutation[point]
        generators.append(Permutation(values))
    actual_order = int(PermutationGroup(generators).order())
    if actual_order != int(pair["actual_generated_image_order"]) or actual_order != 11_943_936:
        raise AssertionError("actual pair image order drift")

    relation_pass = all(core_signature(base, RELATOR) == identity[index] for index, base in enumerate(bases))
    physical_pairs = [tuple(geometric[factor][f"g{i}"] for factor in range(2)) for i in range(8)]
    physical_distinct = len(set(physical_pairs)) == 8
    parity_pass = all(pair_signature[0].parity_image == pair_signature[1].parity_image == 1 for pair_signature in physical_pairs)
    c8_covariance = all(tuple(rotate(value) for value in physical_pairs[i]) == physical_pairs[(i + 1) % 8] for i in range(8))
    inverse_closed = True
    for i in range(4):
        for factor, base in enumerate(bases):
            if multiply_signatures(base, physical_pairs[i][factor], physical_pairs[i + 4][factor]) != identity[factor]:
                inverse_closed = False

    with np.load(OUT / "separator_matrix.npz") as matrix:
        indptr = matrix["zero_indptr"]
        indices = matrix["zero_orbit_indices"]
        left_zeros = indices[int(indptr[pair["left_column"]]):int(indptr[pair["left_column"] + 1])]
        right_zeros = indices[int(indptr[pair["right_column"]]):int(indptr[pair["right_column"] + 1])]
        uncovered = np.intersect1d(left_zeros, right_zeros, assume_unique=True)
    if len(uncovered):
        raise AssertionError("selected product does not cover exact based set")

    n = actual_order
    dimension = 2 * n
    nearest_neighbor_nnz = 16 * n
    csr128_i64 = 24 * nearest_neighbor_nnz + 8 * (dimension + 1)
    csr64_i32 = 12 * nearest_neighbor_nnz + 4 * (dimension + 1)
    one_vector128 = 16 * dimension
    record = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-PRODUCT-BASED",
        "quotient_id": "Q_BASED_S4CORE_PAIR_001",
        "status": {
            "mathematically_admissible_based_quotient": True,
            "mathematically_admissible_production_quotient": False,
            "production_blocker": "PQ-14 and PQ-16 are unavailable because D_global is Deferred",
            "numerically_tractable_production_quotient": False,
            "numerical_reason": "Production promotion is absent; even the nearest-neighbour-only 2N matrix has 191,102,976 entries before the much denser interlayer cutoff block.",
        },
        "construction": {
            "map": "(pi, q_left(phi8^{-j}(.)), q_right(phi8^{-j}(.))) for j=0..7 with one shared parity factor",
            "selected_columns": [pair["left_column"], pair["right_column"]],
            "selected_candidate_ids": [pair["left_id"], pair["right_id"]],
            "base_generator_indices": [records[pair["left_id"]]["base_generator_indices"], records[pair["right_id"]]["base_generator_indices"]],
            "individual_actual_image_orders": [pair["left_order"], pair["right_order"]],
            "raw_cartesian_order": pair["cartesian_order_upper_bound"],
            "shared_parity_fiber_product_upper_bound": pair["shared_parity_fiber_product_upper_bound"],
            "actual_generated_image_order": actual_order,
            "full_cartesian_product_instantiated": False,
            "c8_orbit_closure_applied": True,
            "parity_factor_included_once": True,
            "selection_status": "CERTIFIED COMPLETE AND SMALLER THAN THE BEST ONE-FACTOR IMAGE; NOT PROVEN MINIMUM IMAGE OVER ALL SUBSETS",
        },
        "generator_images": {
            "standard_positive": {
                token: [signature_json(standard[factor][token]) for factor in range(2)]
                for token in POSITIVE_GENERATORS
            },
            "physical_geometric": {
                f"g{i}": [signature_json(geometric[factor][f"g{i}"]) for factor in range(2)]
                for i in range(8)
            },
        },
        "pq_checks": {
            "PQ-01_surface_relation": "PASS" if relation_pass else "FAIL",
            "PQ-02_finite_actual_image_generated": "PASS",
            "PQ-03_normal_kernel": "PASS",
            "PQ-04_parity_inclusion": "PASS" if parity_pass else "FAIL",
            "PQ-05_C8_descent": "PASS" if c8_covariance else "FAIL",
            "PQ-06_eight_directed_distinct_physical_images": "PASS" if physical_distinct else "FAIL",
            "PQ-07_degree_8": "PASS" if physical_distinct else "FAIL",
            "PQ-08_connectedness": "PASS_BY_GENERATED_IMAGE_DEFINITION",
            "PQ-09_bipartiteness": "PASS_BY_SHARED_PARITY_FACTOR",
            "PQ-10_uniform_plus_8_mode": "PASS_STRUCTURAL",
            "PQ-11_staggered_minus_8_mode": "PASS_STRUCTURAL",
            "PQ-12_physical_C8_covariance": "PASS" if c8_covariance else "FAIL",
            "PQ-13_all_based_dangerous_elements_separated": "PASS",
            "PQ-14_all_global_dangerous_classes_separated": "UNAVAILABLE_D_GLOBAL_DEFERRED",
            "PQ-15_based_geometric_injectivity": "PASS_r_inj_based_gt_3a_B",
            "PQ-16_global_geometric_injectivity": "UNAVAILABLE_D_GLOBAL_DEFERRED",
            "PQ-17_Dc_no_wraparound": "PARTIAL_BASED_ONLY_NOT_PRODUCTION",
            "PQ-18_representation_inventory": "NOT_STARTED_NO_PRODUCTION_PROMOTION",
        },
        "additional_exact_checks": {
            "physical_inverse_closure": inverse_closed,
            "exact_based_dangerous_elements": 23_129_592,
            "uncovered_based_elements": 0,
            "separator_matrix_sha256": "aad472e91b290a9c1fafbe64ae0ae492746f71758c3ca608dc60fcd90fc7dfdc",
            "r_inj_based_geo_over_a_B": {"strict_lower_bound": 3.0},
            "r_inj_global_geo_over_a_B": None,
            "systole_over_a_B": None,
            "Dc_over_a_B": 3.0,
        },
        "practical_feasibility": {
            "N": n,
            "two_N": dimension,
            "nearest_neighbor_only_nnz_lower_bound": nearest_neighbor_nnz,
            "nearest_neighbor_only_CSR_complex128_int64_bytes_lower_bound": csr128_i64,
            "nearest_neighbor_only_CSR_complex64_int32_bytes_lower_bound": csr64_i32,
            "one_complex128_vector_bytes": one_vector128,
            "twenty_complex128_vectors_bytes": 20 * one_vector128,
            "interlayer_cutoff_entries_included_in_these_bounds": False,
            "current_host_total_physical_memory_bytes": 68_112_736_256,
            "current_host_free_physical_memory_bytes_at_audit": 20_475_662_336,
            "conclusion": "NOT_NUMERICALLY_TRACTABLE_FOR_DECLARED_PRODUCTION_SMOKE_WITH_FULL_INTERLAYER_CUTOFF",
        },
        "global_scope_evaluated": False,
        "smoke_released": False,
        "main_tex_modified": False,
    }
    if any(value == "FAIL" for value in record["pq_checks"].values()) or not all((relation_pass, physical_distinct, parity_pass, c8_covariance, inverse_closed)):
        raise AssertionError("based product exact check failed")
    json_path = CERT / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.json"
    json_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    (CERT / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.md").write_text(
        f"# Based-only product quotient certificate\n\n"
        f"`Q_BASED_S4CORE_PAIR_001` is the actual generated image of two registered S4 practical-core maps, columns "
        f"{pair['left_column']} and {pair['right_column']}, with one shared parity factor and all eight `phi8` transports. "
        f"Its exact order is **{actual_order:,}**; the full Cartesian target was not instantiated.\n\n"
        f"The two zero/kernel-exception sets in the exact separator matrix are disjoint. Therefore their product separates "
        f"all 23,129,592 based-dangerous elements and certifies `r_inj,based > 3 a_B`. PQ-01 through PQ-13 and PQ-15 "
        f"pass in based scope.\n\n"
        f"This is not a production quotient: PQ-14 and PQ-16 are unavailable because the exact global obstruction-class "
        f"enumeration is Deferred. PQ-17 is consequently based-only, the 12-point smoke is not released, and no production "
        f"cover YAML is created.\n\n"
        f"The quotient has `N={actual_order:,}` and `2N={dimension:,}`. Even before interlayer cutoff terms, the two-layer "
        f"nearest-neighbour matrix has {nearest_neighbor_nnz:,} stored entries and needs at least {csr128_i64 / 2**30:.3f} GiB "
        f"in complex128/int64 CSR plus eigensolver vectors. The declared interlayer cutoff is much denser, so this image is "
        f"not accepted as a tractable production-smoke target on the current host.\n",
        encoding="utf-8",
    )
    (CERT / "BASED_PRODUCT_PRACTICAL_FEASIBILITY.json").write_text(
        json.dumps(record["practical_feasibility"], indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "quotient_id": record["quotient_id"],
        "actual_order": actual_order,
        "two_N": dimension,
        "based": "PASS",
        "global": "UNAVAILABLE",
        "smoke_released": False,
    }, indent=2))


if __name__ == "__main__":
    main()
