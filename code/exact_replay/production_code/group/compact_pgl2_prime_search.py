"""Direct C8-equivariant seed search for PGL(2,p), p=23 or 31."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "compact_quotient_search"
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)


class PGL2:
    def __init__(self, prime: int):
        self.p = prime
        self.identity = self.normalize((1, 0, 0, 1))

    def normalize(self, matrix: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        values = tuple(value % self.p for value in matrix)
        pivot = next((value for value in values if value), None)
        if pivot is None:
            raise ValueError("zero projective matrix")
        scale = pow(pivot, -1, self.p)
        return tuple((value * scale) % self.p for value in values)  # type: ignore[return-value]

    def determinant(self, matrix: tuple[int, int, int, int]) -> int:
        a, b, c, d = matrix
        return (a * d - b * c) % self.p

    def multiply(self, left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        a, b, c, d = left
        e, f, g, h = right
        return self.normalize((a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h))

    def inverse(self, matrix: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        a, b, c, d = matrix
        return self.normalize((d, -b, -c, a))

    def power(self, value: tuple[int, int, int, int], exponent: int) -> tuple[int, int, int, int]:
        result = self.identity
        base = value
        while exponent:
            if exponent & 1:
                result = self.multiply(result, base)
            base = self.multiply(base, base)
            exponent >>= 1
        return result

    def conjugate(self, by: tuple[int, int, int, int], value: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return self.multiply(self.multiply(by, value), self.inverse(by))

    def elements(self) -> tuple[tuple[int, int, int, int], ...]:
        values = set()
        for a in range(self.p):
            for b in range(self.p):
                for c in range(self.p):
                    for d in range(self.p):
                        matrix = (a, b, c, d)
                        if self.determinant(matrix):
                            values.add(self.normalize(matrix))
        result = tuple(sorted(values))
        if len(result) != self.p * (self.p * self.p - 1):
            raise AssertionError("PGL order drift")
        return result

    def odd(self, value: tuple[int, int, int, int]) -> bool:
        return pow(self.determinant(value), (self.p - 1) // 2, self.p) == self.p - 1

    def generated_order(self, generators: tuple[tuple[int, int, int, int], ...]) -> int:
        moves = generators[:4] + tuple(self.inverse(value) for value in generators[:4])
        seen = {self.identity}
        frontier = [self.identity]
        while frontier:
            current = frontier.pop()
            for move in moves:
                candidate = self.multiply(current, move)
                if candidate not in seen:
                    seen.add(candidate)
                    frontier.append(candidate)
        return len(seen)

    def relation(self, images: tuple[tuple[int, int, int, int], ...]) -> tuple[int, int, int, int]:
        value = self.identity
        for index in RELATOR:
            value = self.multiply(value, images[index])
        return value


def matrix_text(value: tuple[int, int, int, int]) -> str:
    return ":".join(map(str, value))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, choices=(23, 31), required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    pgl = PGL2(args.prime)
    group = pgl.elements()
    order_eight = {value for value in group if pgl.power(value, 8) == pgl.identity and pgl.power(value, 4) != pgl.identity}
    classes = []
    remaining = set(order_eight)
    while remaining:
        representative = min(remaining)
        orbit = {pgl.conjugate(value, representative) for value in group}
        classes.append((representative, orbit))
        remaining.difference_update(orbit)
    if sum(len(orbit) for _, orbit in classes) != len(order_eight):
        raise AssertionError("order-eight class partition drift")

    rows = []
    survivors = []
    counters = {"alpha_classes": len(classes), "seeds_examined": 0, "odd_seeds": 0, "inverse_closed": 0, "surface_relation": 0, "eight_distinct": 0, "surjective": 0, "cheap_survivors": 0}
    for class_index, (alpha, _orbit) in enumerate(classes):
        alpha_powers = tuple(pgl.power(alpha, index) for index in range(8))
        for seed_index, seed in enumerate(group):
            counters["seeds_examined"] += 1
            odd = pgl.odd(seed)
            counters["odd_seeds"] += int(odd)
            images = tuple(pgl.conjugate(alpha_powers[index], seed) for index in range(8))
            inverse_closed = all(images[index + 4] == pgl.inverse(images[index]) for index in range(4))
            counters["inverse_closed"] += int(inverse_closed)
            relation = inverse_closed and pgl.relation(images) == pgl.identity
            counters["surface_relation"] += int(relation)
            distinct = len(set(images)) == 8
            counters["eight_distinct"] += int(distinct)
            actual_order = pgl.generated_order(images) if relation and distinct and odd else 0
            surjective = actual_order == len(group)
            counters["surjective"] += int(surjective)
            cheap = all((odd, inverse_closed, relation, distinct, surjective))
            counters["cheap_survivors"] += int(cheap)
            candidate_id = f"DIRECT_PGL2_{args.prime}_C{class_index:02d}_{seed_index:05d}"
            first_failed = next((name for name, passed in (
                ("PHYSICAL_INVERSE_CLOSURE", inverse_closed),
                ("CQ-01_SURFACE_RELATION", relation),
                ("CQ-02_SURJECTIVITY", surjective),
                ("CQ-03_DEGREE_8", distinct),
                ("CQ-04_PARITY", odd),
            ) if not passed), "NONE")
            rows.append({
                "candidate_id": candidate_id,
                "family": f"PGL2_{args.prime}_inner_C8",
                "declared_group_order": len(group),
                "actual_image_order": actual_order if actual_order else "",
                "seed_permutation": matrix_text(seed),
                "alpha_conjugator": matrix_text(alpha),
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
                survivors.append((candidate_id, class_index, seed_index, alpha, seed, images))

    csv_path = DATA / "candidates.csv"
    existing_ids = set()
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        existing_ids = {row["candidate_id"] for row in csv.DictReader(handle)}
    if any(row["candidate_id"] in existing_ids for row in rows):
        raise AssertionError("candidate rows already appended")
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writerows(rows)

    manifest_path = DATA / f"pgl2_{args.prime}_survivor_manifest.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["candidate_id", "prime", "alpha_class", "seed_index", "alpha", "seed", *[f"g{i}" for i in range(8)]])
        for candidate_id, class_index, seed_index, alpha, seed, images in survivors:
            writer.writerow([candidate_id, args.prime, class_index, seed_index, matrix_text(alpha), matrix_text(seed), *[matrix_text(image) for image in images]])

    summary = {
        "family": f"PGL(2,{args.prime}) with all inner automorphisms of exact order eight",
        "group_order": len(group),
        "parity": f"determinant square class PGL(2,{args.prime})->C2",
        "automorphism_completeness": f"For prime {args.prime}, every automorphism of PGL(2,{args.prime}) is inner; every order-eight conjugacy class is enumerated.",
        "order_eight_elements": len(order_eight),
        "order_eight_conjugacy_classes": [{"representative": matrix_text(rep), "size": len(orbit)} for rep, orbit in classes],
        "counters": counters,
        "survivor_manifest": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "runtime_seconds": time.perf_counter() - started,
    }
    (DATA / f"pgl2_{args.prime}_search_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
