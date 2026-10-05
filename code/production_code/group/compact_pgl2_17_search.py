"""Complete direct-C8 seed search for PGL(2,17), order 4,896."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "compact_quotient_search"
P = 17
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)


def normalize(matrix: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    values = tuple(value % P for value in matrix)
    pivot = next((value for value in values if value), None)
    if pivot is None:
        raise ValueError("zero matrix has no projective class")
    scale = pow(pivot, -1, P)
    return tuple((value * scale) % P for value in values)  # type: ignore[return-value]


def determinant(matrix: tuple[int, int, int, int]) -> int:
    a, b, c, d = matrix
    return (a * d - b * c) % P


def multiply(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = left
    e, f, g, h = right
    return normalize((a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h))


def inverse(matrix: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = matrix
    return normalize((d, -b, -c, a))


IDENTITY = normalize((1, 0, 0, 1))


def power(value: tuple[int, int, int, int], exponent: int) -> tuple[int, int, int, int]:
    result = IDENTITY
    base = value
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def conjugate(conjugator: tuple[int, int, int, int], value: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return multiply(multiply(conjugator, value), inverse(conjugator))


def elements() -> tuple[tuple[int, int, int, int], ...]:
    values = set()
    for a in range(P):
        for b in range(P):
            for c in range(P):
                for d in range(P):
                    matrix = (a, b, c, d)
                    if determinant(matrix):
                        values.add(normalize(matrix))
    result = tuple(sorted(values))
    if len(result) != P * (P * P - 1):
        raise AssertionError(f"PGL(2,17) order drift: {len(result)}")
    return result


def nonsquare_determinant(value: tuple[int, int, int, int]) -> bool:
    return pow(determinant(value), (P - 1) // 2, P) == P - 1


def generated_order(generators: tuple[tuple[int, int, int, int], ...]) -> int:
    moves = generators[:4] + tuple(inverse(value) for value in generators[:4])
    seen = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        current = frontier.pop()
        for move in moves:
            candidate = multiply(current, move)
            if candidate not in seen:
                seen.add(candidate)
                frontier.append(candidate)
    return len(seen)


def relation_image(images: tuple[tuple[int, int, int, int], ...]) -> tuple[int, int, int, int]:
    value = IDENTITY
    for index in RELATOR:
        value = multiply(value, images[index])
    return value


def matrix_text(value: tuple[int, int, int, int]) -> str:
    return ":".join(map(str, value))


def main() -> None:
    started = time.perf_counter()
    group = elements()
    order_eight = {value for value in group if power(value, 8) == IDENTITY and power(value, 4) != IDENTITY}
    classes = []
    remaining = set(order_eight)
    while remaining:
        representative = min(remaining)
        orbit = {conjugate(value, representative) for value in group}
        classes.append((representative, orbit))
        remaining.difference_update(orbit)
    if sum(len(orbit) for _, orbit in classes) != len(order_eight):
        raise AssertionError("order-eight conjugacy partition drift")

    rows = []
    survivors = []
    counters = {"alpha_classes": len(classes), "seeds_examined": 0, "odd_seeds": 0, "inverse_closed": 0, "surface_relation": 0, "eight_distinct": 0, "surjective": 0, "cheap_survivors": 0}
    for class_index, (alpha_seed, alpha_class) in enumerate(classes):
        alpha_powers = tuple(power(alpha_seed, index) for index in range(8))
        for seed_index, seed in enumerate(group):
            counters["seeds_examined"] += 1
            odd = nonsquare_determinant(seed)
            counters["odd_seeds"] += int(odd)
            images = tuple(conjugate(alpha_powers[index], seed) for index in range(8))
            inverse_closed = all(images[index + 4] == inverse(images[index]) for index in range(4))
            counters["inverse_closed"] += int(inverse_closed)
            relation = inverse_closed and relation_image(images) == IDENTITY
            counters["surface_relation"] += int(relation)
            distinct = len(set(images)) == 8
            counters["eight_distinct"] += int(distinct)
            actual_order = generated_order(images) if relation and distinct and odd else 0
            surjective = actual_order == len(group)
            counters["surjective"] += int(surjective)
            cheap = all((odd, inverse_closed, relation, distinct, surjective))
            counters["cheap_survivors"] += int(cheap)
            candidate_id = f"DIRECT_PGL2_17_C{class_index:02d}_{seed_index:04d}"
            first_failed = next((name for name, passed in (
                ("PHYSICAL_INVERSE_CLOSURE", inverse_closed),
                ("CQ-01_SURFACE_RELATION", relation),
                ("CQ-02_SURJECTIVITY", surjective),
                ("CQ-03_DEGREE_8", distinct),
                ("CQ-04_PARITY", odd),
            ) if not passed), "NONE")
            rows.append({
                "candidate_id": candidate_id,
                "family": "PGL2_17_inner_C8",
                "declared_group_order": len(group),
                "actual_image_order": actual_order if actual_order else "",
                "seed_permutation": matrix_text(seed),
                "alpha_conjugator": matrix_text(alpha_seed),
                "physical_inverse_closure": "PASS" if inverse_closed else "FAIL",
                "CQ-01_surface_relation": "PASS" if relation else "FAIL",
                "CQ-02_surjectivity": "PASS" if surjective else "FAIL",
                "CQ-03_degree_8": "PASS" if distinct else "FAIL",
                "CQ-04_parity_factoring": "PASS" if odd else "FAIL",
                "CQ-05_bipartite": "PASS" if odd else "FAIL",
                "CQ-06_explicit_alpha": "PASS",
                "CQ-07_rho_phi8_alpha_rho": "PASS",
                "CQ-08_physical_C8_covariance": "PASS",
                "CQ-09_based_dangerous_separation": "NOT_EVALUATED_PENDING_IMMUTABLE_TREE" if cheap else "NOT_EVALUATED_NO_CHEAP_SURVIVOR",
                "CQ-10_based_geometric_admissibility": "NOT_EVALUATED_PENDING_CQ09" if cheap else "NOT_EVALUATED_NO_CHEAP_SURVIVOR",
                "first_failed_gate": first_failed,
                "accept_reject": "CHEAP_SURVIVOR" if cheap else "REJECT",
            })
            if cheap:
                survivors.append((candidate_id, class_index, seed_index, alpha_seed, seed, images))

    csv_path = DATA / "candidates.csv"
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writerows(rows)
    manifest_path = DATA / "pgl2_17_survivor_manifest.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["candidate_id", "alpha_class", "seed_index", "alpha", "seed", *[f"g{i}" for i in range(8)]])
        for candidate_id, class_index, seed_index, alpha_seed, seed, images in survivors:
            writer.writerow([candidate_id, class_index, seed_index, matrix_text(alpha_seed), matrix_text(seed), *[matrix_text(image) for image in images]])
    summary = {
        "family": "PGL(2,17) with inner automorphism alpha of exact order eight",
        "group_order": len(group),
        "parity": "determinant square class PGL(2,17)->C2",
        "automorphism_completeness": "For prime 17, every automorphism of PGL(2,17) is inner; every order-eight conjugacy class is enumerated.",
        "order_eight_elements": len(order_eight),
        "order_eight_conjugacy_classes": [{"representative": matrix_text(rep), "size": len(orbit)} for rep, orbit in classes],
        "counters": counters,
        "survivor_manifest": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "runtime_seconds": time.perf_counter() - started,
    }
    (DATA / "pgl2_17_search_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
