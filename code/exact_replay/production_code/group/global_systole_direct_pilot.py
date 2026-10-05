"""Bounded quotient-specific pilot for a dangerous global kernel witness.

The pilot is deliberately not a global completeness proof.  It enumerates
freely and cyclically reduced geometric words through a declared length,
quotients by cyclic rotation, inversion, and the exact C8 label shift, then
tests whether the order of the word's finite image produces a kernel power
whose hyperbolic translation length is at most 6 a_B.  Any reported witness
is re-evaluated with the project's exact algebraic SU(1,1) arithmetic.
"""

from __future__ import annotations

import argparse
from itertools import permutations
import json
import math
from pathlib import Path
import time

import mpmath as mp

from production_code.group.universal_cover import (
    IDENTITY_MATRIX,
    field_to_complex,
    matrix_from_word,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "production_code" / "group" / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.json"
OUTPUT = ROOT / "data" / "production" / "global_direct" / "pilot_cyclic_phi8.json"
INVERSE = tuple((index + 4) % 8 for index in range(8))


def permutation_table() -> tuple[tuple[int, ...], ...]:
    elements = tuple(permutations(range(4)))
    index = {element: number for number, element in enumerate(elements)}
    return tuple(
        tuple(index[tuple(left[right[i]] for i in range(4))] for right in elements)
        for left in elements
    )


S4_TABLE = permutation_table()
IDENTITY_STATE = (0,) + (0,) * 16


def multiply_state(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return ((left[0] + right[0]) & 1,) + tuple(
        S4_TABLE[left[index]][right[index]] for index in range(1, 17)
    )


def finite_images() -> tuple[tuple[int, ...], ...]:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    images = []
    for generator in range(8):
        factors = record["generator_images"]["physical_geometric"][f"g{generator}"]
        parity = int(factors[0]["parity"])
        if parity != int(factors[1]["parity"]):
            raise AssertionError("shared parity drift")
        images.append((parity,) + tuple(
            int(value)
            for factor in factors
            for value in factor["S4_phi_inverse_orbit_indices"]
        ))
    for generator in range(4):
        if multiply_state(images[generator], images[generator + 4]) != IDENTITY_STATE:
            raise AssertionError("finite-image inverse drift")
    return tuple(images)


def finite_order(state: tuple[int, ...]) -> int:
    value = IDENTITY_STATE
    for order in range(1, 13):
        value = multiply_state(value, state)
        if value == IDENTITY_STATE:
            return order
    raise AssertionError("state order exceeds exponent 12 of the S4 product")


def canonical_phi8_dihedral(word: tuple[int, ...]) -> bool:
    """Canonical under cyclic conjugacy, inversion, and uniform C8 shift."""
    candidates = []
    inverse = tuple(INVERSE[index] for index in reversed(word))
    for source in (word, inverse):
        for shift in range(len(source)):
            rotated = source[shift:] + source[:shift]
            offset = rotated[0]
            candidates.append(tuple((value - offset) % 8 for value in rotated))
    return word == min(candidates)


def q2_sign(a: int, b: int) -> int:
    """Exact sign of a+b*sqrt(2)."""
    if a == 0:
        return (b > 0) - (b < 0)
    if b == 0:
        return (a > 0) - (a < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    delta = a * a - 2 * b * b
    if delta == 0:
        raise AssertionError("unexpected rational equality to sqrt(2)")
    return (1 if delta > 0 else -1) if a > 0 else (-1 if delta > 0 else 1)


def exact_witness(word: tuple[int, ...], image_order: int) -> dict[str, object]:
    powered = word * image_order
    tokens = tuple(f"g{index}" for index in powered)
    matrix = matrix_from_word(tokens)
    if matrix == IDENTITY_MATRIX:
        raise AssertionError("candidate power is the group identity")
    a = matrix[0]
    if any(a[index] for index in (3, 4, 5, 6, 7, 8)):
        raise AssertionError("half trace left Q(sqrt(2))")
    denominator = 1 << a[0]
    c0, c1 = int(a[1]), int(a[2])
    if q2_sign(c0, c1) < 0:
        c0, c1 = -c0, -c1
    cutoff_a = 2405 * denominator
    cutoff_b = 1700 * denominator
    exact_margin_sign = q2_sign(cutoff_a - c0, cutoff_b - c1)
    if exact_margin_sign < 0:
        raise AssertionError("numeric candidate fails the exact trace cutoff")
    mp.mp.dps = 90
    half_trace = (mp.mpf(c0) + mp.mpf(c1) * mp.sqrt(2)) / denominator
    a_b = 2 * mp.acosh(1 + mp.sqrt(2))
    translation = 2 * mp.acosh(half_trace) / a_b
    return {
        "canonical_primitive_word": [f"g{index}" for index in word],
        "finite_image_order": image_order,
        "kernel_witness_word": list(tokens),
        "kernel_witness_geometric_word_length": len(tokens),
        "quotient_identity_exact": True,
        "group_nonidentity_exact": True,
        "matrix_top_row_exact": [list(matrix[0]), list(matrix[1])],
        "absolute_half_trace_exact": {
            "denominator_power_of_two": a[0],
            "q_sqrt2_numerators": [c0, c1],
            "display": f"({c0}+{c1}*sqrt(2))/2^{a[0]}",
        },
        "trace_cutoff_half_exact": "2405+1700*sqrt(2)",
        "trace_cutoff_comparison_exact": "PASS_LEQ" if exact_margin_sign >= 0 else "FAIL",
        "translation_length_over_a_B": mp.nstr(translation, 70),
        "r_inj_global_geo_over_a_B_upper_bound": mp.nstr(translation / 2, 70),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-length", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.maximum_length <= 10:
        raise ValueError("pilot maximum length must lie in 1..10")

    images = finite_images()
    alpha = 1 + math.sqrt(2.0)
    beta = math.sqrt(2 + 2 * math.sqrt(2.0))
    generators = tuple(
        (complex(alpha, 0.0), beta * complex(math.cos(math.pi * index / 4), math.sin(math.pi * index / 4)))
        for index in range(8)
    )
    a_b = 2 * math.acosh(alpha)
    raw_leaves_by_length: dict[str, int] = {}
    canonical_by_length: dict[str, int] = {}
    power_candidates_by_length: dict[str, int] = {}
    best: tuple[float, tuple[int, ...], int] | None = None
    started = time.perf_counter()

    for target_length in range(1, args.maximum_length + 1):
        raw_leaves = 0
        canonical_count = 0
        power_candidates = 0

        def visit(word: tuple[int, ...], a: complex, b: complex, state: tuple[int, ...]) -> None:
            nonlocal raw_leaves, canonical_count, power_candidates, best
            if len(word) == target_length:
                if INVERSE[word[-1]] == word[0]:
                    return
                raw_leaves += 1
                if not canonical_phi8_dihedral(word):
                    return
                canonical_count += 1
                if abs(a - 1) < 1e-11 and abs(b) < 1e-11:
                    return
                order = finite_order(state)
                half_trace = abs(a.real)
                primitive_translation = 2 * math.acosh(max(1.0, half_trace)) / a_b
                powered_translation = order * primitive_translation
                if powered_translation <= 6.0 + 1e-10:
                    power_candidates += 1
                    key = (powered_translation, word, order)
                    if best is None or key < best:
                        best = key
                return
            for generator in range(8):
                if word and generator == INVERSE[word[-1]]:
                    continue
                c, d = generators[generator]
                visit(
                    word + (generator,),
                    a * c + b * d.conjugate(),
                    a * d + b * c.conjugate(),
                    multiply_state(state, images[generator]),
                )

        # C8 normalization permits a representative beginning with g0.
        first_a, first_b = generators[0]
        visit((0,), first_a, first_b, images[0])
        raw_leaves_by_length[str(target_length)] = raw_leaves
        canonical_by_length[str(target_length)] = canonical_count
        power_candidates_by_length[str(target_length)] = power_candidates

    elapsed = time.perf_counter() - started
    witness = None if best is None else exact_witness(best[1], best[2])
    output = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT",
        "quotient_id": "Q_BASED_S4CORE_PAIR_001",
        "scope": "bounded pilot; not a proof-complete global conjugacy enumeration",
        "method": "freely and cyclically reduced words; cyclic rotation, inversion, and exact C8 label-shift canonicalization; finite-image order power test; exact algebraic witness recheck",
        "maximum_primitive_geometric_word_length": args.maximum_length,
        "raw_c8_normalized_leaves_by_length": raw_leaves_by_length,
        "canonical_orbits_by_length": canonical_by_length,
        "dangerous_kernel_power_candidates_by_length": power_candidates_by_length,
        "runtime_seconds": elapsed,
        "canonical_orbits_per_second": sum(canonical_by_length.values()) / elapsed,
        "explicit_witness": witness,
        "global_classification_if_witness": "GLOBAL-FAIL" if witness else None,
        "global_classification_without_witness": "GLOBAL-UNRESOLVED",
        "why_nonexhaustive": "The proved representative side-crossing bound is 110; this pilot covers only primitive representatives through the declared maximum length.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
