"""Freeze explicit finite-group action artifacts for CAND-R4-0005.

The files use the already-certified deterministic BFS enumeration.  Binary
integer arrays are little-endian uint32 unless stated otherwise.  Together,
the element encoding, eight right-generator transitions, inverse map, C8 map,
and parity vector give a compact exact reconstruction contract.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import struct
from pathlib import Path


cand = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0005")
arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
p2 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")

R4 = Path(__file__).resolve().parents[1]
OUT = R4 / "17_FINAL_FREEZE/artifacts"
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write_u32(path: Path, values) -> None:
    with path.open("wb") as handle:
        buffer: list[int] = []
        for value in values:
            buffer.append(int(value))
            if len(buffer) >= 65536:
                handle.write(struct.pack(f"<{len(buffer)}I", *buffer))
                buffer.clear()
        if buffer:
            handle.write(struct.pack(f"<{len(buffer)}I", *buffer))


def inverse_table(elements, multiply, identity):
    lookup = {value: index for index, value in enumerate(elements)}
    result = []
    for value in elements:
        found = None
        for candidate in elements:
            if multiply(value, candidate) == identity:
                found = lookup[candidate]
                break
        if found is None:
            raise RuntimeError("inverse not found")
        result.append(found)
    return result


a_elements, _, _ = arith.enumerate_image(3)
b_elements, b_rotation = p2.enumerate_q((6, 9))
q_elements = cand.enumerate_image()
assert len(a_elements) == 720 and len(b_elements) == 64 and len(q_elements) == 46080
assert b_rotation is not None
assert set(q_elements) == {a + b for a in a_elements for b in b_elements}

a_lookup = {value: index for index, value in enumerate(a_elements)}
b_lookup = {value: index for index, value in enumerate(b_elements)}
q_lookup = {value: index for index, value in enumerate(q_elements)}
a_gens = [arith.generator(i, 3) for i in range(8)]
b_gens = list(p2.q_physical_generators((6, 9)))
q_gens = [cand.generator(i) for i in range(8)]

a_transitions = [[a_lookup[arith.amul(value, gen, 3)] for value in a_elements] for gen in a_gens]
b_transitions = [[b_lookup[p2.q_multiply(value, gen, (6, 9))] for value in b_elements] for gen in b_gens]

element_path = OUT / "CAND-R4-0005.elements_u8.bin"
with element_path.open("wb") as handle:
    for element in q_elements:
        if any(not 0 <= x <= 255 for x in element):
            raise RuntimeError("element encoding overflow")
        handle.write(bytes(element))

transition_path = OUT / "CAND-R4-0005.right_generators_u32le.bin"
write_u32(
    transition_path,
    (q_lookup[cand.multiply(value, generator)] for generator in q_gens for value in q_elements),
)

a_inverse = inverse_table(a_elements, lambda x, y: arith.amul(x, y, 3), arith.aidentity(3))
b_inverse = [b_lookup[p2.q_inverse(value, (6, 9))] for value in b_elements]
q_inverse_path = OUT / "CAND-R4-0005.inverse_u32le.bin"
write_u32(
    q_inverse_path,
    (
        q_lookup[a_elements[a_inverse[a_lookup[value[:8]]]] + b_elements[b_inverse[b_lookup[value[8:]]]]]
        for value in q_elements
    ),
)

phi_path = OUT / "CAND-R4-0005.C8_automorphism_u32le.bin"
write_u32(phi_path, (q_lookup[cand.phi(value)] for value in q_elements))

parity_path = OUT / "CAND-R4-0005.parity_u8.bin"
parity_path.write_bytes(bytes(value[8].bit_count() & 1 for value in q_elements))


def word_id(indices: tuple[int, ...]) -> int:
    value = cand.identity()
    for index in indices:
        value = cand.multiply(value, q_gens[index])
    return q_lookup[value]


presentation_images = {
    "a1": word_id((0,)),
    "b1": word_id((5,)),
    "a2": word_id((5, 0, 2)),
    "b2": word_id((7, 4, 1)),
}
physical_images = {f"g{i}": q_lookup[q_gens[i]] for i in range(8)}

gap_path = OUT / "CAND-R4-0005_factor_regular_generators.g"
with gap_path.open("w", encoding="ascii", newline="\n") as handle:
    handle.write("# Generated exact regular factor actions for CAND-R4-0005.\n")
    handle.write("Areg := Group(\n")
    for index, row in enumerate(a_transitions):
        comma = "," if index < len(a_transitions) - 1 else ""
        handle.write("PermList([" + ",".join(str(x + 1) for x in row) + "])" + comma + "\n")
    handle.write(");;\n")
    handle.write("Breg := Group(\n")
    for index, row in enumerate(b_transitions):
        comma = "," if index < len(b_transitions) - 1 else ""
        handle.write("PermList([" + ",".join(str(x + 1) for x in row) + "])" + comma + "\n")
    handle.write(");;\n")

manifest = {
    "schema_version": "1.0",
    "candidate_id": "CAND-R4-0005",
    "candidate_order": len(q_elements),
    "factor_orders": [len(a_elements), len(b_elements)],
    "direct_product_set_equality": True,
    "enumeration": "deterministic BFS order from certified physical generators",
    "presentation_generator_image_ids_zero_based": presentation_images,
    "physical_shell_image_ids_zero_based": physical_images,
    "artifacts": {
        path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in (element_path, transition_path, q_inverse_path, phi_path, parity_path, gap_path)
    },
    "formats": {
        element_path.name: "46080 records x 10 unsigned bytes: eight F3 arithmetic coordinates, then v in [0,15], z in [0,3]",
        transition_path.name: "generator-major 8 x 46080 zero-based uint32 little-endian right-multiplication targets",
        q_inverse_path.name: "46080 zero-based uint32 little-endian inverse IDs",
        phi_path.name: "46080 zero-based uint32 little-endian exact C8 automorphism targets",
        parity_path.name: "46080 bytes in {0,1}",
        gap_path.name: "GAP source defining Areg and Breg as exact regular permutation groups",
    },
    "reconstruction_rule": "Q is the full direct product Areg x Breg; the candidate marked images are the diagonal pairs of like-indexed physical generators",
    "classification": "PASS_EXPLICIT_EXACT_ACTION_ARTIFACTS",
}
(OUT / "CAND-R4-0005_GROUP_ARTIFACT_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "classification": manifest["classification"],
    "candidate_order": len(q_elements),
    "factor_orders": [len(a_elements), len(b_elements)],
    "manifest_sha256": sha256(OUT / "CAND-R4-0005_GROUP_ARTIFACT_MANIFEST.json"),
}, indent=2))
