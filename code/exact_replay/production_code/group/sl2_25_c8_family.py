"""Exact lifted semilinear C8 quotient family in SL(2,25) x C2."""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence

from production_code.group.psl2_25_c8_family import (
    ALPHA_MATRIX,
    PHYSICAL_RELATOR,
    Q,
    add,
    determinant,
    frobenius,
    inv,
    mul,
    neg,
)
from production_code.group.psl2_25_c8_orbits import alpha_centralizer


IDENTITY = (1, 0, 0, 1)


def scalar_mul(scalar: int, matrix: Sequence[int]) -> tuple[int, int, int, int]:
    return tuple(mul(scalar, value) for value in matrix)  # type: ignore[return-value]


def matmul(left: Sequence[int], right: Sequence[int]) -> tuple[int, int, int, int]:
    a, b, c, d = left
    e, f, g, h = right
    return (
        add(mul(a, e), mul(b, g)),
        add(mul(a, f), mul(b, h)),
        add(mul(c, e), mul(d, g)),
        add(mul(c, f), mul(d, h)),
    )


def matinv(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    a, b, c, d = matrix
    determinant_inverse = inv(determinant(matrix))
    return scalar_mul(determinant_inverse, (d, neg(b), neg(c), a))


def matrix_frobenius(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    return tuple(frobenius(value) for value in matrix)  # type: ignore[return-value]


def alpha(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    return matmul(ALPHA_MATRIX, matmul(matrix_frobenius(matrix), matinv(ALPHA_MATRIX)))


def alpha_power(matrix: Sequence[int], exponent: int) -> tuple[int, int, int, int]:
    result = tuple(map(int, matrix))
    for _ in range(exponent):
        result = alpha(result)
    return result  # type: ignore[return-value]


@lru_cache(maxsize=1)
def sl_elements() -> tuple[tuple[int, int, int, int], ...]:
    return tuple(matrix for matrix in product(range(Q), repeat=4) if determinant(matrix) == 1)


def physical_images(seed: Sequence[int]) -> tuple[tuple[int, int, int, int], ...]:
    result = []
    current = tuple(map(int, seed))
    for _ in range(8):
        result.append(current)
        current = alpha(current)
    return tuple(result)  # type: ignore[return-value]


def word_image(images: Sequence[Sequence[int]], word: Sequence[int]) -> tuple[int, int, int, int]:
    result = IDENTITY
    for digit in word:
        result = matmul(result, images[digit])
    return result


def relation_and_shell_seed(seed: Sequence[int]) -> bool:
    images = physical_images(seed)
    return (
        len(set(images)) == 8
        and all(images[j + 4] == matinv(images[j]) for j in range(4))
        and word_image(images, PHYSICAL_RELATOR) == IDENTITY
    )


def b3_injective(seed: Sequence[int], words: Iterable[Sequence[int]]) -> bool:
    images = physical_images(seed)
    values = [word_image(images, word) for word in words]
    return len(values) == len(set(values))


def generated_subgroup(seed: Sequence[int]) -> frozenset[tuple[int, int, int, int]]:
    generators = physical_images(seed)[:4]
    seen = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            value = matmul(current, generator)
            if value not in seen:
                seen.add(value)
                frontier.append(value)
    return frozenset(seen)


def candidate_seeds(words: Iterable[Sequence[int]]) -> tuple[tuple[int, int, int, int], ...]:
    word_tuple = tuple(tuple(word) for word in words)
    return tuple(seed for seed in sl_elements() if relation_and_shell_seed(seed) and b3_injective(seed, word_tuple))


def semilinear_action(
    pair: tuple[Sequence[int], int], matrix: Sequence[int]
) -> tuple[int, int, int, int]:
    conjugator, exponent = pair
    value = matrix_frobenius(matrix) if exponent & 1 else tuple(matrix)
    return matmul(conjugator, matmul(value, matinv(conjugator)))


def centralizer_orbits(
    seeds: Iterable[Sequence[int]],
) -> tuple[tuple[tuple[int, int, int, int], ...], ...]:
    all_seeds = {tuple(map(int, seed)) for seed in seeds}
    remaining = set(all_seeds)
    result = []
    centralizer = alpha_centralizer()
    while remaining:
        seed = min(remaining)
        orbit = {semilinear_action(pair, seed) for pair in centralizer} & all_seeds
        if not orbit:
            raise RuntimeError("centralizer orbit computation failed")
        result.append(tuple(sorted(orbit)))
        remaining -= orbit
    return tuple(result)

