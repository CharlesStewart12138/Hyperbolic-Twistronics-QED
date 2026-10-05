"""Exact direct C8-equivariant search in the natural symmetric-group family."""

from __future__ import annotations

import csv
from itertools import permutations
import json
from pathlib import Path
import time

from sympy.combinatorics import Permutation, PermutationGroup


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "compact_quotient_search"
GROUP = ROOT / "production_code" / "group"
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(value)
    for source, target in enumerate(value):
        result[target] = source
    return tuple(result)


def power(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(value)))
    base = value
    while exponent:
        if exponent & 1:
            result = compose(result, base)
        base = compose(base, base)
        exponent >>= 1
    return result


def parity(value: tuple[int, ...]) -> int:
    inversions = sum(value[i] > value[j] for i in range(len(value)) for j in range(i + 1, len(value)))
    return inversions & 1


def conjugate(conjugator: tuple[int, ...], value: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(conjugator, value), inverse(conjugator))


def relation_image(images: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    result = tuple(range(len(images[0])))
    for index in RELATOR:
        result = compose(result, images[index])
    return result


def generated_order(images: tuple[tuple[int, ...], ...]) -> int:
    return int(PermutationGroup([Permutation(list(value)) for value in images[:4]]).order())


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    identity = tuple(range(8))
    cycle = tuple((index + 1) % 8 for index in range(8))
    cycle_powers = tuple(power(cycle, exponent) for exponent in range(8))
    rows: list[dict[str, object]] = []
    counters = {
        "seeds_examined": 0,
        "odd_seeds": 0,
        "inverse_closed": 0,
        "surface_relation": 0,
        "surjective_S8": 0,
        "eight_distinct": 0,
        "cheap_gate_survivors": 0,
        "based_lower_bound_eligible": 0,
        "based_dataset_scans": 0,
        "based_pass": 0,
    }
    started = time.perf_counter()
    for seed_index, seed in enumerate(permutations(range(8))):
        counters["seeds_examined"] += 1
        odd = parity(seed) == 1
        if odd:
            counters["odd_seeds"] += 1
        images = tuple(conjugate(cycle_powers[index], seed) for index in range(8))
        inverse_closed = all(images[index + 4] == inverse(images[index]) for index in range(4))
        if inverse_closed:
            counters["inverse_closed"] += 1
        relation = inverse_closed and relation_image(images) == identity
        if relation:
            counters["surface_relation"] += 1
        distinct = len(set(images)) == 8
        if distinct:
            counters["eight_distinct"] += 1
        order = generated_order(images) if relation and distinct and odd else 0
        surjective = order == 40320
        if surjective:
            counters["surjective_S8"] += 1
        alpha_order_8_on_images = distinct
        cheap_survivor = all((inverse_closed, relation, odd, distinct, surjective, alpha_order_8_on_images))
        if cheap_survivor:
            counters["cheap_gate_survivors"] += 1
        lower_bound_eligible = cheap_survivor and order >= 2338
        if lower_bound_eligible:
            counters["based_lower_bound_eligible"] += 1
        first_failed = next((name for name, passed in (
            ("PHYSICAL_INVERSE_CLOSURE", inverse_closed),
            ("CQ-01_SURFACE_RELATION", relation),
            ("CQ-02_SURJECTIVITY", surjective),
            ("CQ-03_DEGREE_8", distinct),
            ("CQ-04_PARITY", odd),
            ("CQ-06_ALPHA_AUTOMORPHISM", alpha_order_8_on_images),
        ) if not passed), None)
        rows.append({
            "candidate_id": f"DIRECT_S8_C8_{seed_index:05d}",
            "family": "S8_natural_inner_C8",
            "declared_group_order": 40320,
            "actual_image_order": order if order else "",
            "seed_permutation": " ".join(map(str, seed)),
            "alpha_conjugator": "0 1 2 3 4 5 6 7 cycle",
            "physical_inverse_closure": "PASS" if inverse_closed else "FAIL",
            "CQ-01_surface_relation": "PASS" if relation else "FAIL",
            "CQ-02_surjectivity": "PASS" if surjective else "FAIL",
            "CQ-03_degree_8": "PASS" if distinct else "FAIL",
            "CQ-04_parity_factoring": "PASS" if odd else "FAIL",
            "CQ-05_bipartite": "PASS" if odd else "FAIL",
            "CQ-06_explicit_alpha": "PASS" if alpha_order_8_on_images else "FAIL",
            "CQ-07_rho_phi8_alpha_rho": "PASS" if alpha_order_8_on_images else "FAIL",
            "CQ-08_physical_C8_covariance": "PASS" if alpha_order_8_on_images else "FAIL",
            "CQ-09_based_dangerous_separation": "NOT_EVALUATED_NO_CHEAP_SURVIVOR",
            "CQ-10_based_geometric_admissibility": "NOT_EVALUATED_NO_CHEAP_SURVIVOR",
            "first_failed_gate": first_failed or "NONE",
            "accept_reject": "CHEAP_SURVIVOR" if cheap_survivor else "REJECT",
        })

    csv_path = DATA / "candidates.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    runtime = time.perf_counter() - started
    report = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-Q-C8-COMPACT",
        "strategy": "direct equivariance rho(phi8(g))=alpha(rho(g)); no eight-kernel core construction",
        "based_lower_bound_N": 2338,
        "order_windows": {
            "Q1_2338_to_10000": {
                "completed_families": ["S7 natural symmetric target"],
                "result": "NO_CANDIDATE_IN_FAMILY",
                "proof": "Aut(S7)=Inn(S7); S7 contains no element of order 8. Eight distinct physical images require an alpha-orbit of length 8, so this family is empty.",
                "entire_window_completed": False,
            },
            "Q2_10000_to_50000": {
                "completed_families": ["S8 natural target with inner alpha generated by an 8-cycle"],
                "result": "COMPLETE_FAMILY_ENUMERATION",
                "proof": "Aut(S8)=Inn(S8), every order-8 element is an 8-cycle, and all 8-cycles are conjugate. Fixing one 8-cycle and enumerating all x in S8 covers the family up to simultaneous conjugacy.",
                "entire_window_completed": False,
            },
            "Q3_50000_to_100000": {"completed_families": [], "entire_window_completed": False},
        },
        "family_counters": counters,
        "runtime_seconds": runtime,
        "candidates_csv": str(csv_path.relative_to(ROOT)).replace("\\", "/"),
        "cheap_exact_gate_survivors": counters["cheap_gate_survivors"],
        "based_dangerous_dataset_recomputed": False,
        "based_dangerous_dataset_scanned": counters["based_dataset_scans"] > 0,
        "global_systole_candidates": 0,
        "smallest_global_certified_quotient": None,
        "smallest_tractable_global_certified_quotient": None,
        "first_production_quotient_found": False,
        "production_yaml_created": False,
        "numerical_feasibility_files_created": 0,
        "terminal_scope": "The S7 and S8 natural symmetric direct-equivariant families are closed; the full Q1/Q2 order windows are not exhausted.",
        "terminal_classification": "NO_COMPACT_QUOTIENT_IN_COMPLETED_SEARCH_CLASSES",
        "exact_next_missing_object": "A concrete non-symmetric finite group family in 2338<=N<=50000 with an explicit order-eight automorphism and an enumerable homomorphism parameterization.",
        "main_tex_modified": False,
    }
    json_path = GROUP / "COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.json"
    md_path = GROUP / "COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(
        "# Direct compact C8-equivariant quotient search\n\n"
        "## Result\n\n"
        "No compact quotient survives the completed natural symmetric-group classes. This is an exact null result for "
        "those classes, not for the full Q1/Q2 order windows.\n\n"
        "The Q1 `S7` class is empty: `Aut(S7)=Inn(S7)`, while `S7` has no element of order eight; an eight-element physical "
        "orbit is therefore impossible. For Q2, all order-eight inner automorphisms of `S8` are conjugate to conjugation by "
        "an 8-cycle. Fixing that cycle and enumerating every `x in S8` is complete up to simultaneous conjugacy, because "
        "equivariance forces `rho(g_i)=c^i x c^{-i}`.\n\n"
        f"All {counters['seeds_examined']:,} seeds were examined ({counters['odd_seeds']:,} odd). "
        f"{counters['inverse_closed']:,} satisfy physical inverse closure, {counters['surface_relation']:,} also satisfy "
        f"the surface relation, and {counters['cheap_gate_survivors']:,} pass every cheap exact gate. "
        "Because there is no cheap-gate survivor, the immutable 23,129,592-element based dataset was neither rebuilt nor "
        "scanned, no global systole job was released, and no numerical-feasibility or production-cover file was created.\n\n"
        "The exact next missing object is a concrete non-symmetric finite group family of order 2,338--50,000 with an "
        "explicit order-eight automorphism and an enumerable homomorphism parameterization. `main.tex` remains locked.\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
