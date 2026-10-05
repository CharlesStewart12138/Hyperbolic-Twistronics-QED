"""Construct the least C8-stable class-2 p=2 marginal separator.

The universal lower-exponent-2 class-2 surface quotient has normal form

    (v,z) in F2^4 x F2^9,

where four central coordinates are generator squares and five are basic
commutators (the surface relator identifies [b2,a2] with [b1,a1]).
The script enumerates quotient row spaces of dimension one, then two, in a
frozen lexicographic order.  It accepts the first C8-stable quotient that
separates the current global witness.  All operations are exact bit algebra.
"""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
import time
from collections import deque
from pathlib import Path
from typing import Iterable


d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
OUT_DIR = R4 / "05_P_QUOTIENT"
CERT = OUT_DIR / "P2C2_C8_MARGINAL_SEPARATOR.certificate.json"
LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"
MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
WITNESSES = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"

# Central basis: q_i=x_i^2, followed by c_ji=[x_j,x_i].
CENTRAL_BASIS = (
    "a1^2", "b1^2", "a2^2", "b2^2",
    "[b1,a1]", "[a2,a1]", "[a2,b1]", "[b2,a1]", "[b2,b1]",
)
COMMUTATOR_BIT = {
    (1, 0): 4,
    (2, 0): 5,
    (2, 1): 6,
    (3, 0): 7,
    (3, 1): 8,
    # [b2,a2]=[b1,a1] in characteristic two by the surface relator.
    (3, 2): 4,
}

STANDARD_INDEX = {"a1": 0, "b1": 1, "a2": 2, "b2": 3}
STANDARD_INVERSE = {"a1_inv": 0, "b1_inv": 1, "a2_inv": 2, "b2_inv": 3}

PHI_STANDARD_WORDS = (
    ("b1_inv",),
    ("a2_inv", "b1", "a1"),
    ("a2_inv", "b1", "a1", "b1_inv", "a1_inv", "b1_inv", "b2_inv"),
    ("a1", "b1", "a1_inv", "b1_inv", "a2"),
)

FullElement = tuple[int, int]
QuotientElement = tuple[int, int]


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def cocycle(left_v: int, right_v: int) -> int:
    result = 0
    for i in range(4):
        if ((left_v >> i) & 1) and ((right_v >> i) & 1):
            result ^= 1 << i
    for j in range(1, 4):
        if not ((left_v >> j) & 1):
            continue
        for i in range(j):
            if (right_v >> i) & 1:
                result ^= 1 << COMMUTATOR_BIT[(j, i)]
    return result


def full_multiply(left: FullElement, right: FullElement) -> FullElement:
    return left[0] ^ right[0], left[1] ^ right[1] ^ cocycle(left[0], right[0])


def full_inverse(value: FullElement) -> FullElement:
    return value[0], value[1] ^ cocycle(value[0], value[0])


def full_generator(index: int) -> FullElement:
    return 1 << index, 0


def evaluate_standard(word: Iterable[str], generators: tuple[FullElement, ...] | None = None) -> FullElement:
    gens = generators or tuple(full_generator(i) for i in range(4))
    result = (0, 0)
    for token in word:
        if token in STANDARD_INDEX:
            image = gens[STANDARD_INDEX[token]]
        elif token in STANDARD_INVERSE:
            image = full_inverse(gens[STANDARD_INVERSE[token]])
        else:
            raise ValueError(f"unknown standard token: {token}")
        result = full_multiply(result, image)
    return result


def physical_full(index: int) -> FullElement:
    return evaluate_standard(d0.G_TO_STANDARD[f"g{index}"])


def central_basis_elements() -> tuple[FullElement, ...]:
    elements: list[FullElement] = []
    gens = tuple(full_generator(i) for i in range(4))
    for i in range(4):
        elements.append(full_multiply(gens[i], gens[i]))
    for j, i in ((1, 0), (2, 0), (2, 1), (3, 0), (3, 1)):
        word = full_multiply(full_multiply(full_multiply(gens[j], gens[i]), full_inverse(gens[j])), full_inverse(gens[i]))
        elements.append(word)
    expected = tuple((0, 1 << i) for i in range(9))
    if tuple(elements) != expected:
        raise RuntimeError(f"central basis realization mismatch: {elements}")
    return expected


def phi_generator_images() -> tuple[FullElement, ...]:
    return tuple(evaluate_standard(word) for word in PHI_STANDARD_WORDS)


def substitute_full(word: Iterable[str], generator_images: tuple[FullElement, ...]) -> FullElement:
    return evaluate_standard(word, generator_images)


def phi_full(value: FullElement) -> FullElement:
    """Apply phi to a normal-form element by a fixed normal-form section."""
    images = phi_generator_images()
    result = (0, 0)
    # Reconstruct the F2 generator part in standard order.
    for i in range(4):
        if (value[0] >> i) & 1:
            result = full_multiply(result, images[i])
    basis_words: list[tuple[str, ...]] = []
    names = ("a1", "b1", "a2", "b2")
    inv = ("a1_inv", "b1_inv", "a2_inv", "b2_inv")
    for i in range(4):
        basis_words.append((names[i], names[i]))
    for j, i in ((1, 0), (2, 0), (2, 1), (3, 0), (3, 1)):
        basis_words.append((names[j], names[i], inv[j], inv[i]))
    for bit, word in enumerate(basis_words):
        if (value[1] >> bit) & 1:
            result = full_multiply(result, substitute_full(word, images))
    return result


def phi_central_columns() -> tuple[int, ...]:
    columns = []
    for element in central_basis_elements():
        image = phi_full(element)
        if image[0] != 0:
            raise RuntimeError("phi does not preserve the central layer")
        columns.append(image[1])
    return tuple(columns)


def dual_phi(row: int, columns: tuple[int, ...]) -> int:
    result = 0
    for source_bit, image in enumerate(columns):
        if dot(row, image):
            result |= 1 << source_bit
    return result


def quotient_central(z: int, rows: tuple[int, ...]) -> int:
    result = 0
    for index, row in enumerate(rows):
        result |= dot(row, z) << index
    return result


def q_multiply(left: QuotientElement, right: QuotientElement, rows: tuple[int, ...]) -> QuotientElement:
    return left[0] ^ right[0], left[1] ^ right[1] ^ quotient_central(cocycle(left[0], right[0]), rows)


def q_inverse(value: QuotientElement, rows: tuple[int, ...]) -> QuotientElement:
    return value[0], value[1] ^ quotient_central(cocycle(value[0], value[0]), rows)


def q_physical_generators(rows: tuple[int, ...]) -> tuple[QuotientElement, ...]:
    return tuple((element[0], quotient_central(element[1], rows)) for element in (physical_full(i) for i in range(8)))


def q_word(word: Iterable[str], rows: tuple[int, ...]) -> QuotientElement:
    generators = q_physical_generators(rows)
    result = (0, 0)
    for token in word:
        result = q_multiply(result, generators[int(token[1])], rows)
    return result


def enumerate_q(rows: tuple[int, ...]) -> tuple[list[QuotientElement], dict[QuotientElement, QuotientElement] | None]:
    one = (0, 0)
    generators = q_physical_generators(rows)
    seen = {one}
    elements = [one]
    queue = deque([one])
    rotation: dict[QuotientElement, QuotientElement] = {one: one}
    while queue:
        source = queue.popleft()
        source_rotated = rotation[source]
        for index, image in enumerate(generators):
            target = q_multiply(source, image, rows)
            rotated_target = q_multiply(source_rotated, generators[(index + 1) % 8], rows)
            previous = rotation.get(target)
            if previous is not None and previous != rotated_target:
                return elements, None
            if target not in seen:
                seen.add(target)
                elements.append(target)
                queue.append(target)
                rotation[target] = rotated_target
    if len(set(rotation.values())) != len(rotation):
        return elements, None
    return elements, rotation


def canonical_row_spaces(dimension: int) -> Iterable[tuple[int, ...]]:
    if dimension == 1:
        for row in range(1, 1 << 9):
            yield (row,)
        return
    if dimension != 2:
        raise ValueError("only marginal dimensions one and two are permitted")
    spaces = set()
    for left in range(1, 1 << 9):
        for right in range(left + 1, 1 << 9):
            spaces.add(tuple(sorted((left, right, left ^ right))))
    for space in sorted(spaces):
        yield space[:2]


def stable(rows: tuple[int, ...], columns: tuple[int, ...]) -> bool:
    span = {0}
    for row in rows:
        span |= {value ^ row for value in tuple(span)}
    return all(dual_phi(row, columns) in span for row in rows)


def word_full_geometric(word: Iterable[str]) -> FullElement:
    result = (0, 0)
    physical = tuple(physical_full(i) for i in range(8))
    for token in word:
        result = full_multiply(result, physical[int(token[1])])
    return result


def factor_hash(rows: tuple[int, ...], elements: list[QuotientElement]) -> str:
    payload = {
        "family": "lower-exponent-2 class-2 central quotient",
        "central_basis": CENTRAL_BASIS,
        "dual_row_space": rows,
        "physical_generators": q_physical_generators(rows),
        "actual_order": len(elements),
        "elements_sha256": hashlib.sha256(json.dumps(sorted(elements), separators=(",", ":")).encode("ascii")).hexdigest().upper(),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def rewrite_separator_outputs(factor: dict, coverage: dict[str, int]) -> None:
    with LIBRARY.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        factors = list(reader)
    factor_row = {
        "factor_id": factor["factor_id"],
        "family": factor["family"],
        "parameters": f"p=2; class=2; marginal_dimension={factor['marginal_dimension']}",
        "actual_order": str(factor["actual_order"]),
        "marked_quotient_hash": factor["marked_quotient_hash"],
        "coverage_count": str(sum(coverage.values())),
        "C8_cost": "0",
        "parity_cost": "0",
        "subdirect_marginal_order_increase": str(2 ** factor["marginal_dimension"]),
        "resource_marginal_increase": str(factor["actual_order"]),
        "certificate_path": "05_P_QUOTIENT/P2C2_C8_MARGINAL_SEPARATOR.certificate.json",
        "certificate_sha256": "PENDING_SELF_HASH",
        "status": "AVAILABLE",
    }
    factors = [row for row in factors if row["factor_id"] != factor["factor_id"]]
    factors.append(factor_row)
    write_tsv(LIBRARY, fields, factors)

    with MATRIX.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        matrix_rows = list(reader)
        old_fields = list(reader.fieldnames or [])
    new_fields = old_fields + ([factor["factor_id"]] if factor["factor_id"] not in old_fields else [])
    for row in matrix_rows:
        row[factor["factor_id"]] = str(coverage[row["witness_id"]])
    write_tsv(MATRIX, new_fields, matrix_rows)


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    started = time.perf_counter()
    columns = phi_central_columns()
    full_elements = [(v, z) for v in range(16) for z in range(512)]
    phi_images = [phi_full(element) for element in full_elements]
    relator = ("a1", "b1", "a1_inv", "b1_inv", "a2", "b2", "a2_inv", "b2_inv")
    phi_gens = phi_generator_images()
    foundation = {
        "normal_form_cardinality_8192": len(full_elements) == 8192,
        "surface_relator_identity": evaluate_standard(relator) == (0, 0),
        "phi_surface_relator_identity": evaluate_standard(relator, phi_gens) == (0, 0),
        "phi_bijection_on_universal_quotient": len(set(phi_images)) == 8192,
        "phi_eighth_power_identity": all((lambda x: x)(element) == element for element in full_elements),
        "physical_rotation_in_universal_quotient": all(phi_full(physical_full(i)) == physical_full((i + 1) % 8) for i in range(8)),
    }
    # Evaluate the eighth-power condition explicitly without retaining eight maps.
    foundation["phi_eighth_power_identity"] = all(
        (lambda value: value)(
            (lambda start: (lambda y: y)(start))(element)
        ) == element
        for element in ()
    )
    eighth_ok = True
    for element in full_elements:
        image = element
        for _ in range(8):
            image = phi_full(image)
        if image != element:
            eighth_ok = False
            break
    foundation["phi_eighth_power_identity"] = eighth_ok
    if not all(foundation.values()):
        raise RuntimeError(f"universal class-2 foundation failed: {foundation}")

    target_word = tuple("g0 g1 g3 g6 g3 g1 g6 g3 g1 g7 g1 g4".split())
    target_full = word_full_geometric(target_word)
    if target_full[0] != 0 or target_full == (0, 0):
        raise RuntimeError(f"target must be a nonzero central class-2 witness: {target_full}")

    selected: tuple[int, ...] | None = None
    selected_elements: list[QuotientElement] = []
    selected_rotation: dict[QuotientElement, QuotientElement] | None = None
    tested = {"dimension_1": 0, "dimension_2": 0, "stable_dimension_1": 0, "stable_dimension_2": 0}
    for dimension in (1, 2):
        for rows in canonical_row_spaces(dimension):
            tested[f"dimension_{dimension}"] += 1
            if not stable(rows, columns):
                continue
            tested[f"stable_dimension_{dimension}"] += 1
            if quotient_central(target_full[1], rows) == 0:
                continue
            elements, rotation = enumerate_q(rows)
            if rotation is None or len(elements) != 16 * (1 << dimension):
                continue
            selected, selected_elements, selected_rotation = rows, elements, rotation
            break
        if selected is not None:
            break
    if selected is None or selected_rotation is None:
        raise RuntimeError("no C8-stable marginal class-2 separator exists in dimensions one or two")

    dimension = len(selected)
    physical = q_physical_generators(selected)
    rotation_order = 1
    probe = physical[0]
    image = selected_rotation[probe]
    while image != probe:
        rotation_order += 1
        image = selected_rotation[image]
        if rotation_order > 8:
            raise RuntimeError("induced rotation order exceeded eight")
    with WITNESSES.open(encoding="utf-8", newline="") as handle:
        witness_rows = list(csv.DictReader(handle, delimiter="\t"))
    coverage = {
        row["Witness ID"]: int(q_word(tuple(row["Canonical word"].split()), selected) != (0, 0))
        for row in witness_rows
    }
    marked_hash = factor_hash(selected, selected_elements)
    factor_id = f"P2C2-C8-D{dimension}-{marked_hash[:16]}"
    factor = {
        "factor_id": factor_id,
        "family": "C8-stable lower-exponent-2 class-2 central quotient",
        "marginal_dimension": dimension,
        "actual_order": len(selected_elements),
        "marked_quotient_hash": marked_hash,
    }
    certificate = {
        "schema_version": "1.0",
        **factor,
        "construction": {
            "universal_normal_form": "F2^4 x F2^9 with exact class-2 cocycle",
            "central_basis": list(CENTRAL_BASIS),
            "surface_relation": "[a1,b1][a2,b2]=1; [b2,a2]=[b1,a1] in the exponent-2 central layer",
            "selected_dual_row_space_integers": list(selected),
            "selected_dual_row_space_bits_lsb_first": [format(row, "09b")[::-1] for row in selected],
            "phi_central_columns": list(columns),
            "deterministic_search_order": "dimension 1 then 2; lexicographic canonical row spaces",
        },
        "foundation_checks": foundation,
        "search_counts": tested,
        "proof_rows": {
            "target_universal_image": list(target_full),
            "target_quotient_image": list(q_word(target_word, selected)),
            "target_separated": q_word(target_word, selected) != (0, 0),
            "C8_stable_dual_row_space": stable(selected, columns),
            "generated_actual_order": len(selected_elements),
            "expected_normal_form_order": 16 * (1 << dimension),
            "physical_shell_distinct_nonidentity": len(set(physical)) == 8 and (0, 0) not in physical,
            "induced_rotation_bijective": len(set(selected_rotation.values())) == len(selected_elements),
            "induced_rotation_exact_order": rotation_order,
            "parity_descends_as_sum_H1_coordinates": all((element[0].bit_count() & 1) == 1 for element in physical),
        },
        "witness_coverage": coverage,
        "runtime_seconds": time.perf_counter() - started,
        "classification": "PASS",
    }
    proof = certificate["proof_rows"]
    if not all((
        proof["target_separated"], proof["C8_stable_dual_row_space"],
        proof["physical_shell_distinct_nonidentity"], proof["induced_rotation_bijective"],
        proof["induced_rotation_exact_order"] == 8,
        proof["parity_descends_as_sum_H1_coordinates"],
    )):
        raise RuntimeError(f"selected quotient failed proof rows: {proof}")
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    rewrite_separator_outputs(factor, coverage)
    # Replace the temporary self-hash after the certificate exists.
    with LIBRARY.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    for row in rows:
        if row["factor_id"] == factor_id:
            row["certificate_sha256"] = hashlib.sha256(CERT.read_bytes()).hexdigest().upper()
    write_tsv(LIBRARY, fields, rows)


if __name__ == "__main__":
    main()
