"""Exhaust the direct inner-C8 orbit-seed maps into PSL(3,3) x C2.

This is an isolated escalation helper.  It reads (but never modifies) the
frozen universal-cover radius-six archive and the immutable based tree.
PSL(3,3)=SL(3,3), since its scalar centre is trivial, and matrices are
encoded as nine row-major base-three digits.
"""

from __future__ import annotations

from collections import deque
from itertools import product
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
FROZEN_BALL = ROOT / "data" / "production" / "universal_cover" / "ball_radius_6_exact.jsonl.gz"
BASED_TREE = ROOT / "data" / "production" / "quotient_separator" / "based_tree_meta.bin"
OUTPUT = Path(__file__).with_suffix(".json")
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)
IDENTITY = (1, 0, 0, 0, 1, 0, 0, 0, 1)


def determinant(a: tuple[int, ...]) -> int:
    return (
        a[0] * (a[4] * a[8] - a[5] * a[7])
        - a[1] * (a[3] * a[8] - a[5] * a[6])
        + a[2] * (a[3] * a[7] - a[4] * a[6])
    ) % 3


def multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(a[3 * row + k] * b[3 * k + column] for k in range(3)) % 3
        for row in range(3)
        for column in range(3)
    )


def inverse(a: tuple[int, ...]) -> tuple[int, ...]:
    # det(a)=1, so the inverse is the adjugate without a scalar denominator.
    return (
        (a[4] * a[8] - a[5] * a[7]) % 3,
        (a[2] * a[7] - a[1] * a[8]) % 3,
        (a[1] * a[5] - a[2] * a[4]) % 3,
        (a[5] * a[6] - a[3] * a[8]) % 3,
        (a[0] * a[8] - a[2] * a[6]) % 3,
        (a[2] * a[3] - a[0] * a[5]) % 3,
        (a[3] * a[7] - a[4] * a[6]) % 3,
        (a[1] * a[6] - a[0] * a[7]) % 3,
        (a[0] * a[4] - a[1] * a[3]) % 3,
    )


def matrix_code(a: tuple[int, ...]) -> int:
    return sum(value * 3**index for index, value in enumerate(a))


def matrix_json(a: tuple[int, ...]) -> dict[str, object]:
    return {
        "row_major_entries_F3": list(a),
        "rows": [list(a[0:3]), list(a[3:6]), list(a[6:9])],
        "base3_code_little_endian": matrix_code(a),
    }


def power(a: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = IDENTITY
    while exponent:
        if exponent & 1:
            result = multiply(result, a)
        a = multiply(a, a)
        exponent >>= 1
    return result


def frozen_b3() -> tuple[tuple[int, tuple[int, ...]], ...]:
    rows: list[tuple[int, tuple[int, ...]]] = []
    with gzip.open(FROZEN_BALL, "rt", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if int(record["minimum_geometric_word_length"]) <= 3:
                word = tuple(int(token[1:]) for token in record["representative"])
                rows.append((int(record["element_id"]), word))
    if len(rows) != 457 or [element_id for element_id, _ in rows] != list(range(457)):
        raise AssertionError("frozen geometric B3 is not the registered 457-element prefix")
    return tuple(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def subgroup(elements: tuple[tuple[int, ...], ...], index: dict[tuple[int, ...], int],
             identity: int, generators: tuple[int, ...]) -> frozenset[int]:
    seen = {identity}
    frontier = [identity]
    generator_matrices = tuple(elements[g] for g in generators)
    while frontier:
        current = frontier.pop()
        left = elements[current]
        for generator in generator_matrices:
            value = index[multiply(left, generator)]
            if value not in seen:
                seen.add(value)
                frontier.append(value)
    return frozenset(seen)


def direct_subgroup_order(elements: tuple[tuple[int, ...], ...], index: dict[tuple[int, ...], int],
                          identity: int, generators: tuple[int, ...]) -> int:
    seen = {2 * identity}
    frontier = [2 * identity]
    generator_matrices = tuple(elements[g] for g in generators)
    while frontier:
        current = frontier.pop()
        base, parity = divmod(current, 2)
        left = elements[base]
        for generator in generator_matrices:
            value = 2 * index[multiply(left, generator)] + (parity ^ 1)
            if value not in seen:
                seen.add(value)
                frontier.append(value)
    return len(seen)


def b3_result(elements: tuple[tuple[int, ...], ...], index: dict[tuple[int, ...], int],
              identity: int, images: tuple[int, ...], words: tuple[tuple[int, tuple[int, ...]], ...]) -> dict[str, object]:
    seen: dict[int, tuple[int, tuple[int, ...]]] = {}
    image_matrices = tuple(elements[value] for value in images)
    first_collision = None
    for element_id, word in words:
        value = elements[identity]
        for generator in word:
            value = multiply(value, image_matrices[generator])
        key = 2 * index[value] + (len(word) & 1)
        if key in seen and first_collision is None:
            prior_id, prior_word = seen[key]
            first_collision = {
                "element_ids": [prior_id, element_id],
                "words": [[f"g{i}" for i in prior_word], [f"g{i}" for i in word]],
                "direct_product_image": {"base_element_index": index[value], "C2": len(word) & 1},
            }
        seen.setdefault(key, (element_id, word))
    return {"image_size": len(seen), "injective": len(seen) == len(words), "first_collision": first_collision}


def centralizer_orbits(seed_ids: set[int], centralizer: tuple[int, ...],
                       elements: tuple[tuple[int, ...], ...], index: dict[tuple[int, ...], int],
                       inverses: tuple[int, ...]) -> list[list[int]]:
    remaining = set(seed_ids)
    result: list[list[int]] = []
    while remaining:
        seed = min(remaining)
        orbit = {
            index[multiply(multiply(elements[g], elements[seed]), elements[inverses[g]])]
            for g in centralizer
        }
        members = sorted(orbit & seed_ids)
        if not members:
            raise AssertionError("empty centralizer orbit")
        result.append(members)
        remaining.difference_update(members)
    return result


def based_tree_scan(elements: tuple[tuple[int, ...], ...], index: dict[tuple[int, ...], int],
                    identity: int, images: tuple[int, ...]) -> dict[str, object]:
    """Scan the immutable 23,129,593-node based tree in PSL(3,3) x C2."""
    with BASED_TREE.open("rb") as handle:
        magic = handle.read(8)
        count, record_size = struct.unpack("<QI", handle.read(12))
        if magic != b"BOLZAT01" or count != 23_129_593 or record_size != 8:
            raise AssertionError("based-tree header drift")
        payload = handle.read()
    if len(payload) != count * record_size:
        raise AssertionError("short based-tree payload")
    right_tables = []
    for generator in images:
        right = elements[generator]
        right_tables.append(tuple(index[multiply(left, right)] for left in elements))
    # uint16 suffices because |PSL(3,3)|=5616.  Depth stores the C2 image.
    from array import array
    states = array("H", [identity])
    witness = None
    evaluated = 0
    for element_id in range(1, count):
        parent, generator, depth, reserved = struct.unpack_from("<IBBH", payload, element_id * 8)
        if parent >= element_id or generator >= 8 or reserved != 0:
            raise AssertionError(f"bad based-tree record {element_id}")
        value = right_tables[generator][states[parent]]
        states.append(value)
        evaluated = element_id
        if value == identity and not (depth & 1):
            witness = element_id
            break
    result: dict[str, object] = {
        "passed": witness is None,
        "elements_evaluated": evaluated,
        "tree_elements": count,
        "first_kernel_element_id": witness,
    }
    if witness is not None:
        reverse: list[int] = []
        current = witness
        while current:
            parent, generator, depth, reserved = struct.unpack_from("<IBBH", payload, current * 8)
            reverse.append(generator)
            current = parent
        result["first_kernel_word"] = [f"g{i}" for i in reversed(reverse)]
        result["first_kernel_depth"] = len(reverse)
    return result


def main() -> None:
    started = time.perf_counter()
    elements = tuple(a for a in product(range(3), repeat=9) if determinant(a) == 1)
    if len(elements) != 5616 or len(set(elements)) != 5616:
        raise AssertionError("SL(3,3) order drift")
    index = {value: i for i, value in enumerate(elements)}
    identity = index[IDENTITY]
    inverses = tuple(index[inverse(value)] for value in elements)
    if any(multiply(elements[i], elements[inverses[i]]) != IDENTITY for i in range(len(elements))):
        raise AssertionError("inverse table failure")

    order8 = tuple(i for i, value in enumerate(elements)
                   if power(value, 8) == IDENTITY and power(value, 4) != IDENTITY)
    remaining = set(order8)
    classes: list[list[int]] = []
    while remaining:
        representative = min(remaining)
        h = elements[representative]
        conjugates = {
            index[multiply(multiply(g, h), elements[inverses[g_id]])]
            for g_id, g in enumerate(elements)
        }
        if not conjugates <= set(order8):
            raise AssertionError("order-eight conjugacy class escaped inventory")
        classes.append(sorted(conjugates))
        remaining.difference_update(conjugates)

    words = frozen_b3()
    class_records = []
    all_b3_orbit_records = []
    for class_number, conjugacy_class in enumerate(classes):
        representative = conjugacy_class[0]
        h = elements[representative]
        h_inverse = elements[inverses[representative]]
        alpha = tuple(index[multiply(multiply(h, value), h_inverse)] for value in elements)
        if any(alpha[alpha[alpha[alpha[alpha[alpha[alpha[alpha[i]]]]]]]] != i for i in range(len(elements))):
            raise AssertionError("alpha^8 failure")
        centralizer = tuple(i for i, value in enumerate(elements) if multiply(value, h) == multiply(h, value))
        if len(conjugacy_class) * len(centralizer) != len(elements):
            raise AssertionError("class-centralizer count failure")

        counters = {
            "seeds_examined": len(elements),
            "alpha4_inverse": 0,
            "eight_distinct": 0,
            "alpha4_inverse_and_eight_distinct": 0,
            "surface_relation": 0,
            "inverse_orbit_and_surface_relation": 0,
            "base_generation_PSL3_3": 0,
            "direct_generation_PSL3_3_x_C2": 0,
            "B3_injective": 0,
            "all_gates": 0,
        }
        gate_sets: dict[str, set[int]] = {name: set() for name in (
            "inverse_orbit_relation", "generation", "B3", "all_gates")
        }
        seed_details: dict[int, dict[str, object]] = {}
        for seed in range(len(elements)):
            image_ids = [seed]
            for _ in range(7):
                image_ids.append(alpha[image_ids[-1]])
            images = tuple(image_ids)
            inverse_pass = images[4] == inverses[seed]
            distinct_pass = len(set(images)) == 8
            if inverse_pass:
                counters["alpha4_inverse"] += 1
            if distinct_pass:
                counters["eight_distinct"] += 1
            if inverse_pass and distinct_pass:
                counters["alpha4_inverse_and_eight_distinct"] += 1
            relation_value = identity
            for digit in RELATOR:
                relation_value = index[multiply(elements[relation_value], elements[images[digit]])]
            relation_pass = relation_value == identity
            if relation_pass:
                counters["surface_relation"] += 1
            if not (inverse_pass and distinct_pass and relation_pass):
                continue
            counters["inverse_orbit_and_surface_relation"] += 1
            gate_sets["inverse_orbit_relation"].add(seed)
            base_order = len(subgroup(elements, index, identity, images))
            base_generation = base_order == 5616
            if base_generation:
                counters["base_generation_PSL3_3"] += 1
                gate_sets["generation"].add(seed)
            direct_order = direct_subgroup_order(elements, index, identity, images) if base_generation else 0
            direct_generation = direct_order == 11232
            if direct_generation:
                counters["direct_generation_PSL3_3_x_C2"] += 1
            b3 = b3_result(elements, index, identity, images, words)
            if b3["injective"]:
                counters["B3_injective"] += 1
                gate_sets["B3"].add(seed)
            all_pass = base_generation and direct_generation and bool(b3["injective"])
            if all_pass:
                counters["all_gates"] += 1
                gate_sets["all_gates"].add(seed)
            seed_details[seed] = {
                "seed": matrix_json(elements[seed]),
                "physical_images": [matrix_json(elements[i]) for i in images],
                "base_generated_order": base_order,
                "direct_product_generated_order": direct_order,
                "B3": b3,
            }

        orbit_summaries: dict[str, object] = {}
        for gate_name, seed_set in gate_sets.items():
            orbits = centralizer_orbits(seed_set, centralizer, elements, index, inverses)
            orbit_summaries[gate_name] = {
                "orbit_count": len(orbits),
                "orbit_sizes": [len(orbit) for orbit in orbits],
                "representative_seed_indices": [orbit[0] for orbit in orbits],
                "representative_seeds": [matrix_json(elements[orbit[0]]) for orbit in orbits],
            }
            if gate_name == "all_gates":
                for orbit_index, orbit in enumerate(orbits):
                    rep = orbit[0]
                    based = based_tree_scan(elements, index, identity, tuple(
                        index[multiply(multiply(power(h, exponent), elements[rep]), power(h_inverse, exponent))]
                        for exponent in range(8)
                    ))
                    all_b3_orbit_records.append({
                        "class_number": class_number,
                        "orbit_index": orbit_index,
                        "representative_seed_index": rep,
                        "member_seed_indices": orbit,
                        "detail": seed_details[rep],
                        "based_tree": based,
                    })

        class_records.append({
            "class_number": class_number,
            "representative_index": representative,
            "representative": matrix_json(h),
            "inverse_representative_index": inverses[representative],
            "class_size": len(conjugacy_class),
            "centralizer_size": len(centralizer),
            "member_indices": conjugacy_class,
            "counters": counters,
            "centralizer_seed_orbits": orbit_summaries,
        })

    output = {
        "schema_version": "1.0",
        "scope": "exhaustive direct inner-C8 orbit-seed maps into PSL(3,3) x C2",
        "encoding": {
            "base_group": "PSL(3,3)=SL(3,3), exact 3x3 determinant-one matrices over F3",
            "matrix": "row-major nine-tuple; entry tuple is also little-endian base-3 digits for the reported integer code",
            "direct_product": "(base_matrix,C2_bit), identity=(I,0), each physical generator=(alpha^i(x),1)",
            "automorphism": "alpha(y)=h*y*h^-1; centre PSL(3,3) is trivial, so exact order(alpha)=exact order(h)=8",
        },
        "group_orders": {"PSL3_3": 5616, "C2": 2, "direct_product": 11232},
        "physical_contract": {
            "images": "g_i -> (alpha^i(x),1)",
            "inverse": "alpha^4(x)=x^-1",
            "surface_relator_indices": list(RELATOR),
            "eight_distinct_required": True,
            "generation_required": "PSL(3,3) x C2",
        },
        "frozen_B3": {
            "source": str(FROZEN_BALL.relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": sha256(FROZEN_BALL),
            "selection": "all archived exact universal-cover records with minimum_geometric_word_length <= 3",
            "element_count": len(words),
            "element_id_range": [words[0][0], words[-1][0]],
        },
        "based_tree": {
            "source": str(BASED_TREE.relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": sha256(BASED_TREE),
            "scanned_only_for_all-gate centralizer-orbit representatives": True,
        },
        "order8_elements": len(order8),
        "order8_conjugacy_classes": len(classes),
        "classes": class_records,
        "all_gate_seed_orbits": all_b3_orbit_records,
        "total_all_gate_raw_seeds": sum(record["counters"]["all_gates"] for record in class_records),
        "total_all_gate_seed_orbits": len(all_b3_orbit_records),
        "runtime_seconds": time.perf_counter() - started,
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT),
        "order8_elements": len(order8),
        "classes": len(classes),
        "class_counters": [record["counters"] for record in class_records],
        "all_gate_seed_orbits": len(all_b3_orbit_records),
        "based_results": [record["based_tree"] for record in all_b3_orbit_records],
        "runtime_seconds": output["runtime_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
