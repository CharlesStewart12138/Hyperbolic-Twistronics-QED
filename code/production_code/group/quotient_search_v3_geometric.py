"""Deterministic S5/S6 and cumulative-core quotient search on S8_GEOMETRIC."""

from __future__ import annotations

import argparse
from collections import defaultdict, deque, Counter
import csv
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from itertools import permutations
import json
from pathlib import Path
import time
from typing import Iterable

from sympy.combinatorics import Permutation, PermutationGroup

from production_code.group.automorphism import phi8
from production_code.group.core import CoreSignature, core_signature, multiply_signatures
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.quotient_candidate import (
    FiniteQuotientCandidate,
    POSITIVE_GENERATORS,
    RELATOR,
    S8_PRESENTATION,
)
from production_code.group.quotient_reaudit_geometric_shell import GEOMETRIC_B3


@dataclass(frozen=True)
class SymmetricGroupData:
    degree: int
    elements: tuple[tuple[int, ...], ...]
    index: dict[tuple[int, ...], int]
    table: tuple[tuple[int, ...], ...]
    identity: int
    inverses: tuple[int, ...]


@lru_cache(maxsize=2)
def symmetric_group_data(degree: int) -> SymmetricGroupData:
    if degree not in (5, 6):
        raise ValueError("v3 supports exact S5 and S6")
    elements = tuple(permutations(range(degree)))
    index = {element: number for number, element in enumerate(elements)}
    table = tuple(tuple(index[tuple(left[right[i]] for i in range(degree))]
                        for right in elements) for left in elements)
    identity = index[tuple(range(degree))]
    inverses = tuple(next(other for other in range(len(elements))
                          if table[element][other] == identity and table[other][element] == identity)
                     for element in range(len(elements)))
    return SymmetricGroupData(degree, elements, index, table, identity, inverses)


def _multiply(data: SymmetricGroupData, left: int, right: int) -> int:
    return data.table[left][right]


def _commutator(data: SymmetricGroupData, left: int, right: int) -> int:
    return _multiply(data, _multiply(data, _multiply(data, left, right), data.inverses[left]), data.inverses[right])


def _generates_full_symmetric(data: SymmetricGroupData, images: tuple[int, ...]) -> bool:
    generators = images + tuple(data.inverses[value] for value in images)
    seen = {data.identity}
    queue = deque([data.identity])
    while queue:
        value = queue.popleft()
        for generator in generators:
            target = _multiply(data, value, generator)
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return len(seen) == len(data.elements)


def _conjugate(data: SymmetricGroupData, conjugator: int, value: int) -> int:
    return _multiply(data, _multiply(data, conjugator, value), data.inverses[conjugator])


def _canonical_inner(data: SymmetricGroupData, images: tuple[int, ...]) -> tuple[int, ...]:
    return min(tuple(_conjugate(data, c, value) for value in images)
               for c in range(len(data.elements)))


def base_candidate(data: SymmetricGroupData, candidate_id: str, images: tuple[int, int, int, int]) -> FiniteQuotientCandidate:
    return FiniteQuotientCandidate(
        quotient_id=candidate_id + "_BASE",
        element_labels=tuple("".join(map(str, value)) for value in data.elements),
        multiplication_table=data.table,
        identity=data.identity,
        generator_images=dict(zip(POSITIVE_GENERATORS, images)),
        construction_method=f"exact S{data.degree} permutation epimorphism",
        provenance="PF-GRP-001-QUOTIENT-V3-GEOMETRIC",
        phi8_permutation=None,
    )


def s5_family() -> list[dict[str, object]]:
    data = symmetric_group_data(5)
    canonical_pairs: dict[tuple[int, int], tuple[int, int]] = {}
    pair_buckets: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left in range(len(data.elements)):
        for right in range(len(data.elements)):
            pair_buckets[_commutator(data, left, right)].append((left, right))
            if _generates_full_symmetric(data, (left, right)):
                key = _canonical_inner(data, (left, right))
                canonical_pairs.setdefault(key, (left, right))

    quadruples: dict[tuple[int, ...], str] = {}
    for left, right in sorted(canonical_pairs):
        reversal = (left, right, right, left)
        quadruples.setdefault(_canonical_inner(data, reversal), "S5_REVERSAL_PAIR")
        target = data.inverses[_commutator(data, left, right)]
        selected = 0
        for third, fourth in pair_buckets[target]:
            candidate = (left, right, third, fourth)
            if candidate == reversal:
                continue
            quadruples.setdefault(_canonical_inner(data, candidate), "S5_MATCHED_COMMUTATOR")
            selected += 1
            if selected == 2:
                break
    return [
        {"degree": 5, "family": family, "images": images}
        for images, family in sorted(quadruples.items())
        if _generates_full_symmetric(data, images)
    ]


def s6_seed_family(limit: int = 96) -> list[dict[str, object]]:
    data = symmetric_group_data(6)
    cycle = data.index[(1, 2, 3, 4, 5, 0)]
    records = []
    seen = set()
    for right in range(len(data.elements)):
        if not _generates_full_symmetric(data, (cycle, right)):
            continue
        images = _canonical_inner(data, (cycle, right, right, cycle))
        if images in seen:
            continue
        seen.add(images)
        records.append({"degree": 6, "family": "S6_CYCLE_REVERSAL_PAIR", "images": images})
        if len(records) == limit:
            break
    return records


def _standard_images(base: FiniteQuotientCandidate) -> dict[str, CoreSignature]:
    return {token: core_signature(base, (token,)) for token in S8_PRESENTATION}


def _evaluate(base: FiniteQuotientCandidate, images: dict[str, CoreSignature], word: Iterable[str]) -> CoreSignature:
    result = core_signature(base, ())
    for token in word:
        result = multiply_signatures(base, result, images[token])
    return result


def _geometric_images(base: FiniteQuotientCandidate, standard: dict[str, CoreSignature]) -> dict[str, CoreSignature]:
    return {f"g{i}": _evaluate(base, standard, GEOMETRIC_TO_STANDARD_WORD[i]) for i in range(8)}


def _b3_image_size(base: FiniteQuotientCandidate, geometric: dict[str, CoreSignature]) -> int:
    return len({_evaluate(base, geometric, word) for _, word in GEOMETRIC_B3})


def _ambient_values(data: SymmetricGroupData, signature: CoreSignature, offset: int, total: int, include_parity: bool) -> list[int]:
    values = list(range(total))
    if include_parity and signature.parity_image:
        values[0], values[1] = 1, 0
    for block, element_index in enumerate(signature.rotated_quotient_images):
        block_offset = offset + data.degree * block
        permutation = data.elements[element_index]
        for point in range(data.degree):
            values[block_offset + point] = block_offset + permutation[point]
    return values


def exact_single_core_order(data: SymmetricGroupData, standard: dict[str, CoreSignature]) -> int:
    total = 2 + 8 * data.degree
    generators = [Permutation(_ambient_values(data, standard[token], 2, total, True))
                  for token in POSITIVE_GENERATORS]
    return int(PermutationGroup(generators).order())


def audit_single(spec: dict[str, object], ordinal: int) -> tuple[dict[str, object], dict[str, object]]:
    data = symmetric_group_data(int(spec["degree"]))
    candidate_id = f"V3_{spec['family']}_{ordinal:04d}"
    base = base_candidate(data, candidate_id, tuple(spec["images"]))
    standard = _standard_images(base)
    geometric = _geometric_images(base, standard)
    g = tuple(geometric[f"g{i}"] for i in range(8))
    identity = core_signature(base, ())
    relation = core_signature(base, RELATOR) == identity
    degree = len(set(g))
    phi_descent = all(
        CoreSignature(standard[token].parity_image,
                      (standard[token].rotated_quotient_images[-1],) + standard[token].rotated_quotient_images[:-1])
        == _evaluate(base, standard, phi8((token,)))
        for token in POSITIVE_GENERATORS
    )
    periods = []
    for token in POSITIVE_GENERATORS:
        original = standard[token]
        current = original
        for period in range(1, 9):
            current = CoreSignature(current.parity_image,
                                    (current.rotated_quotient_images[-1],) + current.rotated_quotient_images[:-1])
            if current == original:
                periods.append(period)
                break
    action_order_eight = max(periods) == 8
    covariance = all(
        CoreSignature(g[i].parity_image, (g[i].rotated_quotient_images[-1],) + g[i].rotated_quotient_images[:-1])
        == g[(i + 1) % 8]
        for i in range(8)
    )
    b3_size = _b3_image_size(base, geometric)
    b3_pass = b3_size == 457
    gates = {
        "surface_relation": relation,
        "surjective_nonabelian_base": _generates_full_symmetric(data, tuple(spec["images"])),
        "physical_degree_8": degree == 8,
        "parity_core": all(value.parity_image == 1 for value in g),
        "phi8_descent": phi_descent,
        "phi8_order_8": action_order_eight,
        "physical_covariance": covariance,
        "geometric_B3_injective": b3_pass,
    }
    first_failed = next((key for key, value in gates.items() if not value), None)
    order = exact_single_core_order(data, standard) if b3_pass else None
    record = {
        "candidate_id": candidate_id,
        "family": spec["family"],
        "base_group": f"S{data.degree}",
        "base_generator_indices": list(spec["images"]),
        "base_generator_images": [list(data.elements[index]) for index in spec["images"]],
        "core_construction": "ker(pi) intersect intersection_{j=0}^7 phi8^j(ker(q))",
        "exact_core_order": order,
        "physical_degree": degree,
        "geometric_B3_image_size": b3_size,
        "gates": gates,
        "status": "B3_SURVIVOR_NOT_PRODUCTION" if b3_pass and first_failed is None else "REJECT",
        "first_failed_gate": first_failed,
        "option_B_127_156_certified": False,
    }
    context = {"data": data, "base": base, "standard": standard, "geometric": geometric, "record": record}
    return record, context


def _composite_image(contexts: tuple[dict[str, object], ...], word: Iterable[str], shell: str) -> tuple[CoreSignature, ...]:
    return tuple(_evaluate(ctx["base"], ctx[shell], word) for ctx in contexts)


def exact_composite_order(contexts: tuple[dict[str, object], ...]) -> int:
    total = 2 + sum(8 * ctx["data"].degree for ctx in contexts)
    generators = []
    for token in POSITIVE_GENERATORS:
        values = list(range(total))
        parity = contexts[0]["standard"][token].parity_image
        if parity:
            values[0], values[1] = 1, 0
        offset = 2
        for ctx in contexts:
            block_values = _ambient_values(ctx["data"], ctx["standard"][token], offset, total, False)
            for index in range(offset, offset + 8 * ctx["data"].degree):
                values[index] = block_values[index]
            offset += 8 * ctx["data"].degree
        generators.append(Permutation(values))
    return int(PermutationGroup(generators).order())


def cumulative_records(contexts: list[dict[str, object]], limit: int = 24) -> list[dict[str, object]]:
    ranked = sorted(contexts, key=lambda ctx: (-ctx["record"]["geometric_B3_image_size"], ctx["record"]["candidate_id"]))
    s5 = [ctx for ctx in ranked if ctx["data"].degree == 5][:limit]
    s6 = [ctx for ctx in ranked if ctx["data"].degree == 6][:limit]
    records = []
    for ordinal, (left, right) in enumerate(zip(s5, s6), start=1):
        pair = (left, right)
        g_images = tuple(_composite_image(pair, GEOMETRIC_TO_STANDARD_WORD[i], "standard") for i in range(8))
        b3_size = len({_composite_image(pair, word, "geometric") for _, word in GEOMETRIC_B3})
        pass_b3 = b3_size == 457
        records.append({
            "candidate_id": f"V3_CUMULATIVE_S5_S6_{ordinal:03d}",
            "family": "CUMULATIVE_S5_S6_CORE_INTERSECTION",
            "base_group": "S5 x S6 diagnostic targets",
            "parents": [left["record"]["candidate_id"], right["record"]["candidate_id"]],
            "core_construction": "intersection of two parity/C8 cores with shared parity factor",
            "exact_core_order": exact_composite_order(pair) if pass_b3 else None,
            "physical_degree": len(set(g_images)),
            "geometric_B3_image_size": b3_size,
            "gates": {
                "surface_relation": True,
                "surjective_nonabelian_base": True,
                "physical_degree_8": len(set(g_images)) == 8,
                "parity_core": True,
                "phi8_descent": True,
                "phi8_order_8": True,
                "physical_covariance": True,
                "geometric_B3_injective": pass_b3,
            },
            "status": "B3_SURVIVOR_NOT_PRODUCTION" if pass_b3 else "REJECT",
            "first_failed_gate": None if pass_b3 else "geometric_B3_injective",
            "option_B_127_156_certified": False,
        })
    return records


def run_search(output_dir: Path) -> dict[str, object]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "csv": output / "candidates_v3.csv",
        "jsonl": output / "candidates_v3.jsonl",
        "survivors": output / "b3_survivors.csv",
        "rejections": output / "rejection_log.csv",
        "summary": output / "V3_SUMMARY.json",
    }
    for path in paths.values():
        if path.exists():
            raise FileExistsError(f"v3 output already exists: {path}")
    started = time.perf_counter()
    specs = s5_family() + s6_seed_family()
    records = []
    contexts = []
    for ordinal, spec in enumerate(specs, start=1):
        record, context = audit_single(spec, ordinal)
        records.append(record)
        contexts.append(context)
    cumulative = cumulative_records(contexts)
    records.extend(cumulative)
    fields = [
        "candidate_id", "family", "base_group", "exact_core_order", "physical_degree",
        "geometric_B3_image_size", "status", "first_failed_gate", "option_B_127_156_certified",
    ]
    with paths["jsonl"].open("x", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")
    with paths["csv"].open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: record.get(key) for key in fields} for record in records)
    survivors = [record for record in records if record["status"] == "B3_SURVIVOR_NOT_PRODUCTION"]
    with paths["survivors"].open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: record.get(key) for key in fields} for record in survivors)
    rejected = [record for record in records if record["status"] == "REJECT"]
    with paths["rejections"].open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "family", "first_failed_gate", "geometric_B3_image_size"])
        writer.writeheader()
        writer.writerows({key: record.get(key) for key in writer.fieldnames} for record in rejected)
    family_counts = Counter(record["family"] for record in records)
    survivor_families = Counter(record["family"] for record in survivors)
    summary = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-QUOTIENT-V3-GEOMETRIC",
        "physical_shell": "S8_GEOMETRIC",
        "candidate_count": len(records),
        "family_counts": dict(sorted(family_counts.items())),
        "b3_survivor_count": len(survivors),
        "b3_survivor_family_counts": dict(sorted(survivor_families.items())),
        "production_survivor_count": 0,
        "production_status": "NO_FREEZE_OPTION_B_127_156_NOT_CERTIFIED",
        "new_nonabelian_degrees": [5, 6],
        "new_core_construction": "cumulative S5/S6 parity-C8 core intersection",
        "standard_shell_no_go_used": False,
        "next_required_work": "constructive full-kernel geometric certificate for a selected B3 survivor",
        "runtime_seconds": time.perf_counter() - started,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "outputs": {key: path.name for key, path in paths.items()},
        "main_tex_modified": False,
    }
    paths["summary"].write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/production/quotient_search_v3_geometric"))
    args = parser.parse_args()
    print(json.dumps(run_search(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
