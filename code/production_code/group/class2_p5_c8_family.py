"""Proof-complete class-two exponent-five C8 quotient family.

The physical generators have homology vectors e0,e1,e2,e3,-e0,...,-e3.
The central quotient is a C8-stable two-dimensional quotient of exterior
square homology that kills the exact surface relator.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Iterator, Sequence

import numpy as np
from numpy.typing import NDArray


P = 5
HALF = 3
EXTERIOR_PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PHYSICAL_RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)


def rotation_matrix(p: int = P) -> NDArray[np.int64]:
    result = np.zeros((4, 4), dtype=np.int64)
    for index in range(3):
        result[index + 1, index] = 1
    result[0, 3] = -1
    return result % p


def exterior_vector(left: Sequence[int], right: Sequence[int], p: int = P) -> NDArray[np.int64]:
    return np.array([(left[i] * right[j] - left[j] * right[i]) % p for i, j in EXTERIOR_PAIRS], dtype=np.int64)


def exterior_rotation(p: int = P) -> NDArray[np.int64]:
    rotation = rotation_matrix(p)
    result = np.zeros((6, 6), dtype=np.int64)
    for column, (first, second) in enumerate(EXTERIOR_PAIRS):
        result[:, column] = exterior_vector(rotation[:, first], rotation[:, second], p)
    return result


def physical_vectors(p: int = P) -> tuple[NDArray[np.int64], ...]:
    rotation = rotation_matrix(p)
    vector = np.array((1, 0, 0, 0), dtype=np.int64)
    result = []
    for _ in range(8):
        result.append(vector)
        vector = rotation @ vector % p
    return tuple(result)


def relator_exterior_vector(p: int = P) -> NDArray[np.int64]:
    vectors = physical_vectors(p)
    result = np.zeros(6, dtype=np.int64)
    for left in range(len(PHYSICAL_RELATOR)):
        for right in range(left + 1, len(PHYSICAL_RELATOR)):
            result += exterior_vector(vectors[PHYSICAL_RELATOR[left]], vectors[PHYSICAL_RELATOR[right]], p)
    return result % p


def rref_two_subspaces(dimension: int = 6, p: int = P) -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Yield every two-dimensional subspace exactly once in RREF."""

    for first_pivot, second_pivot in combinations(range(dimension), 2):
        positions = []
        for column in range(dimension):
            if column in (first_pivot, second_pivot):
                continue
            if column > first_pivot:
                positions.append((0, column))
            if column > second_pivot:
                positions.append((1, column))
        for values in product(range(p), repeat=len(positions)):
            rows = np.zeros((2, dimension), dtype=np.int64)
            rows[0, first_pivot] = rows[1, second_pivot] = 1
            for (row, column), value in zip(positions, values, strict=True):
                rows[row, column] = value
            yield tuple(map(int, rows[0])), tuple(map(int, rows[1]))


def _pivots(rows: NDArray[np.int64]) -> tuple[int, int]:
    return tuple(int(np.flatnonzero(row)[0]) for row in rows)  # type: ignore[return-value]


def _is_in_row_space(vector: NDArray[np.int64], rows: NDArray[np.int64], p: int) -> bool:
    first, second = _pivots(rows)
    reconstructed = (vector[first] * rows[0] + vector[second] * rows[1]) % p
    return bool(np.array_equal(vector % p, reconstructed))


@dataclass(frozen=True)
class Class2Candidate:
    ordinal: int
    rows: tuple[tuple[int, ...], tuple[int, ...]]

    @property
    def order(self) -> int:
        return 2 * P**6

    def image(self, word: Sequence[int]) -> tuple[int, ...]:
        vectors = physical_vectors(P)
        homology = np.zeros(4, dtype=np.int64)
        central = np.zeros(6, dtype=np.int64)
        parity = 0
        for generator in word:
            vector = vectors[generator]
            central = (central + HALF * exterior_vector(homology, vector, P)) % P
            homology = (homology + vector) % P
            parity ^= 1
        projected = np.asarray(self.rows, dtype=np.int64) @ central % P
        return (parity, *map(int, homology), *map(int, projected))


def invariant_relator_quotients(p: int = P) -> tuple[Class2Candidate, ...]:
    if p != P:
        raise ValueError("the frozen compact family is defined over F5")
    action = exterior_rotation(p)
    relator = relator_exterior_vector(p)
    result = []
    for rows_tuple in rref_two_subspaces(6, p):
        rows = np.asarray(rows_tuple, dtype=np.int64)
        if np.any(rows @ relator % p):
            continue
        if all(_is_in_row_space(row @ action % p, rows, p) for row in rows):
            result.append(Class2Candidate(len(result), rows_tuple))
    return tuple(result)


def b3_survivors(words: Iterable[Sequence[int]]) -> tuple[Class2Candidate, ...]:
    result = []
    for candidate in invariant_relator_quotients():
        images = [candidate.image(word) for word in words]
        if len(images) == len(set(images)):
            result.append(candidate)
    return tuple(result)


def decode_word(high: int, low: int, depth: int) -> tuple[int, ...]:
    result = []
    for index in range(depth):
        shift = 3 * (depth - 1 - index)
        result.append((low >> shift) & 7 if shift < 64 else (high >> (shift - 64)) & 7)
    return tuple(result)
