"""Proof-complete direct inner-C8 family in PSL(3,3) x C2."""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence


P = 3
IDENTITY = (1,0,0, 0,1,0, 0,0,1)
PHYSICAL_RELATOR = (0,5,2,7,4,1,6,3)


def determinant(m: Sequence[int]) -> int:
    a,b,c,d,e,f,g,h,i = m
    return (a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)) % P


def matmul(x: Sequence[int], y: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        sum(x[3*r+k]*y[3*k+c] for k in range(3)) % P
        for r in range(3) for c in range(3)
    )


def matinv(m: Sequence[int]) -> tuple[int, ...]:
    a,b,c,d,e,f,g,h,i = m
    cof = (
        e*i-f*h, -(d*i-f*g), d*h-e*g,
        -(b*i-c*h), a*i-c*g, -(a*h-b*g),
        b*f-c*e, -(a*f-c*d), a*e-b*d,
    )
    det_inv = pow(determinant(m), -1, P)
    # adjugate is transpose of the cofactor matrix.
    return tuple((cof[3*c+r]*det_inv) % P for r in range(3) for c in range(3))


def power(x: Sequence[int], exponent: int) -> tuple[int, ...]:
    result = IDENTITY
    base = tuple(x)
    while exponent:
        if exponent & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        exponent >>= 1
    return result


def conjugate(by: Sequence[int], value: Sequence[int]) -> tuple[int, ...]:
    return matmul(by, matmul(value, matinv(by)))


@lru_cache(maxsize=1)
def elements() -> tuple[tuple[int, ...], ...]:
    result = tuple(matrix for matrix in product(range(P), repeat=9) if determinant(matrix) == 1)
    if len(result) != 5616:
        raise RuntimeError("PSL(3,3) order drift")
    return result


@lru_cache(maxsize=1)
def order_eight_classes() -> tuple[tuple[tuple[int, ...], tuple[tuple[int, ...], ...]], ...]:
    group = elements()
    remaining = {x for x in group if power(x,8)==IDENTITY and power(x,4)!=IDENTITY}
    classes = []
    while remaining:
        representative = min(remaining)
        orbit = {conjugate(g, representative) for g in group}
        exact_orbit = tuple(sorted(orbit & remaining))
        classes.append((representative, exact_orbit))
        remaining -= orbit
    return tuple(classes)


def physical_images(alpha: Sequence[int], seed: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    result = []
    alpha_powers = [power(alpha,j) for j in range(8)]
    for value in alpha_powers:
        result.append(conjugate(value, seed))
    return tuple(result)


def word_image(images: Sequence[Sequence[int]], word: Sequence[int]) -> tuple[int, ...]:
    result = IDENTITY
    for digit in word:
        result = matmul(result, images[digit])
    return result


def relation_and_shell(alpha: Sequence[int], seed: Sequence[int]) -> bool:
    images = physical_images(alpha, seed)
    return (
        len(set(images)) == 8
        and all(images[j+4] == matinv(images[j]) for j in range(4))
        and word_image(images, PHYSICAL_RELATOR) == IDENTITY
    )


def b3_image_size(alpha: Sequence[int], seed: Sequence[int], words: Iterable[Sequence[int]]) -> int:
    images = physical_images(alpha, seed)
    return len({word_image(images, word) for word in words})


def generated_subgroup(alpha: Sequence[int], seed: Sequence[int]) -> frozenset[tuple[int, ...]]:
    generators = physical_images(alpha, seed)[:4]
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


def candidate_seeds(words: Iterable[Sequence[int]]) -> tuple[dict[str, object], ...]:
    words = tuple(tuple(word) for word in words)
    result = []
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes()):
        for seed in elements():
            if not relation_and_shell(alpha, seed):
                continue
            image_size = b3_image_size(alpha, seed, words)
            generated = len(generated_subgroup(alpha, seed))
            result.append({
                "class_index": class_index,
                "alpha": alpha,
                "seed": seed,
                "B3_image_size": image_size,
                "generated_order": generated,
                "B3_survivor": image_size == len(words) and generated == 5616,
            })
    return tuple(result)

