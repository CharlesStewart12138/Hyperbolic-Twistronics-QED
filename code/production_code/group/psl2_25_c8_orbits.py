"""Exact centralizer reduction for the PSL(2,25) semilinear C8 family."""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence

from production_code.group.psl2_25_c8_family import (
    ALPHA_MATRIX,
    Q,
    canonical,
    determinant,
    matinv,
    matmul,
    matrix_frobenius,
)


@lru_cache(maxsize=1)
def pgl_elements() -> tuple[tuple[int, int, int, int], ...]:
    elements = {
        canonical(matrix)
        for matrix in product(range(Q), repeat=4)
        if determinant(matrix) != 0
    }
    return tuple(sorted(elements))


def semilinear_action(
    pair: tuple[Sequence[int], int], matrix: Sequence[int]
) -> tuple[int, int, int, int]:
    conjugator, exponent = pair
    value = matrix_frobenius(matrix) if exponent & 1 else canonical(matrix)
    return matmul(conjugator, matmul(value, matinv(conjugator)))


@lru_cache(maxsize=1)
def alpha_centralizer() -> tuple[tuple[tuple[int, int, int, int], int], ...]:
    """Centralizer of alpha=(A,Frob) in PΓL(2,25), as exact pairs."""

    result = []
    for conjugator in pgl_elements():
        sigma_conjugator = matrix_frobenius(conjugator)
        for exponent in (0, 1):
            left = matmul(
                conjugator,
                matrix_frobenius(ALPHA_MATRIX) if exponent else ALPHA_MATRIX,
            )
            right = matmul(ALPHA_MATRIX, sigma_conjugator)
            if left == right:
                result.append((conjugator, exponent))
    return tuple(result)


def centralizer_orbits(
    seeds: Iterable[Sequence[int]],
) -> tuple[tuple[tuple[int, int, int, int], ...], ...]:
    all_seeds = {canonical(seed) for seed in seeds}
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

