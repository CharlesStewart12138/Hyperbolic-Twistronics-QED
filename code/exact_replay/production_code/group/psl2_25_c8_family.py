"""Exact semilinear C8 quotient family in PSL(2,25) x C2.

Field elements are encoded as ``a + b*u -> a + 5*b`` with
``u**2 = 3`` over F5.  PSL(2,25) is represented by projective 2x2
matrices with square determinant, normalized so the first nonzero entry is
one.  The extra C2 coordinate is the physical bipartite parity.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence


P = 5
Q = 25
IDENTITY = (1, 0, 0, 1)
PHYSICAL_RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)
ALPHA_MATRIX = (0, 1, 5, 5)


def add(x: int, y: int) -> int:
    return ((x % 5 + y % 5) % 5) + 5 * (((x // 5) + (y // 5)) % 5)


def neg(x: int) -> int:
    return ((-x) % 5) + 5 * ((-(x // 5)) % 5)


def sub(x: int, y: int) -> int:
    return add(x, neg(y))


def mul(x: int, y: int) -> int:
    a, b = x % 5, x // 5
    c, d = y % 5, y // 5
    return ((a * c + 3 * b * d) % 5) + 5 * ((a * d + b * c) % 5)


def power(x: int, exponent: int) -> int:
    result = 1
    while exponent:
        if exponent & 1:
            result = mul(result, x)
        x = mul(x, x)
        exponent >>= 1
    return result


def inv(x: int) -> int:
    if x == 0:
        raise ZeroDivisionError("zero has no inverse")
    return power(x, Q - 2)


def frobenius(x: int) -> int:
    # (a+b*u)^5 = a-b*u because u^2=3 and u^4=-1 in F5.
    return (x % 5) + 5 * ((-(x // 5)) % 5)


def is_square(x: int) -> bool:
    return x != 0 and power(x, (Q - 1) // 2) == 1


def determinant(matrix: Sequence[int]) -> int:
    a, b, c, d = matrix
    return sub(mul(a, d), mul(b, c))


def canonical(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    values = tuple(map(int, matrix))
    pivot = next((x for x in values if x), None)
    if pivot is None:
        raise ValueError("zero matrix is not projective")
    scale = inv(pivot)
    return tuple(mul(scale, x) for x in values)  # type: ignore[return-value]


def matmul(left: Sequence[int], right: Sequence[int]) -> tuple[int, int, int, int]:
    a, b, c, d = left
    e, f, g, h = right
    return canonical((add(mul(a, e), mul(b, g)),
                      add(mul(a, f), mul(b, h)),
                      add(mul(c, e), mul(d, g)),
                      add(mul(c, f), mul(d, h))))


def matinv(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    a, b, c, d = matrix
    if determinant(matrix) == 0:
        raise ValueError("singular matrix")
    return canonical((d, neg(b), neg(c), a))


def matrix_frobenius(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    return canonical(tuple(frobenius(x) for x in matrix))


def alpha(matrix: Sequence[int]) -> tuple[int, int, int, int]:
    return matmul(ALPHA_MATRIX, matmul(matrix_frobenius(matrix), matinv(ALPHA_MATRIX)))


def alpha_power(matrix: Sequence[int], exponent: int) -> tuple[int, int, int, int]:
    result = canonical(matrix)
    for _ in range(exponent):
        result = alpha(result)
    return result


@lru_cache(maxsize=1)
def psl_elements() -> tuple[tuple[int, int, int, int], ...]:
    elements = {
        canonical(matrix)
        for matrix in product(range(Q), repeat=4)
        if is_square(determinant(matrix))
    }
    return tuple(sorted(elements))


def physical_images(seed: Sequence[int]) -> tuple[tuple[int, int, int, int], ...]:
    result = []
    current = canonical(seed)
    for _ in range(8):
        result.append(current)
        current = alpha(current)
    return tuple(result)


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
    images = physical_images(seed)
    generators = images[:4]
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
    return tuple(seed for seed in psl_elements() if relation_and_shell_seed(seed) and b3_injective(seed, word_tuple))


def encode_matrix(matrix: Sequence[int]) -> int:
    a, b, c, d = canonical(matrix)
    return a + Q * (b + Q * (c + Q * d))

