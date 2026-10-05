"""Independent exact verification of the eight ambient degree-15 candidates.

Permutations are zero-based images and multiply as functions: (a*b)[i]=a[b[i]].
The factoradic ranks are emitted by enumerate_inner_c8_permutation_degree15_gpt56sol.cpp.
"""

from __future__ import annotations

from collections import deque


D = 15
RANKS = (
    757701091722,
    710759741466,
    911941300008,
    777302836524,
    773670498474,
    862924518342,
    761057489982,
    765089238222,
)
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)
ONE = tuple(range(D))


def mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(D))


def inv(a: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * D
    for i, image in enumerate(a):
        result[image] = i
    return tuple(result)


def power(a: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = ONE
    while exponent:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent >>= 1
    return result


def conj(t: tuple[int, ...], a: tuple[int, ...]) -> tuple[int, ...]:
    return mul(mul(t, a), inv(t))


def odd(a: tuple[int, ...]) -> bool:
    return sum(a[i] > a[j] for i in range(D) for j in range(i + 1, D)) % 2 == 1


def rank_perm(a: tuple[int, ...]) -> int:
    result = 0
    for i in range(D):
        result = result * (D - i) + sum(a[j] < a[i] for j in range(i + 1, D))
    return result


def unrank_perm(rank: int) -> tuple[int, ...]:
    digits = [0] * D
    residual = rank
    for i in range(D - 1, -1, -1):
        digits[i] = residual % (D - i)
        residual //= D - i
    if residual:
        raise ValueError("rank outside S15")
    available = list(range(D))
    result = tuple(available.pop(digit) for digit in digits)
    if rank_perm(result) != rank:
        raise RuntimeError("factoradic round trip failed")
    return result


def b3(images: tuple[tuple[int, ...], ...], augmented: bool) -> int:
    seen: set[object] = {(ONE, 0) if augmented else ONE}
    for a in range(8):
        seen.add((images[a], 1) if augmented else images[a])
        for b in range(8):
            if b == (a + 4) % 8:
                continue
            ab = mul(images[a], images[b])
            seen.add((ab, 0) if augmented else ab)
            for c in range(8):
                if c == (b + 4) % 8:
                    continue
                abc = mul(ab, images[c])
                seen.add((abc, 1) if augmented else abc)
    return len(seen)


def generated(images: tuple[tuple[int, ...], ...]) -> tuple[int, int, int]:
    seen = {ONE}
    todo = deque((ONE,))
    while todo:
        left = todo.popleft()
        for right in images:
            value = mul(left, right)
            if value not in seen:
                seen.add(value)
                todo.append(value)
    odd_count = sum(odd(value) for value in seen)
    return len(seen), len(seen) - odd_count, odd_count


def main() -> None:
    tau = list(ONE)
    for i in range(8):
        tau[i] = (i + 1) % 8
    for i in range(8, 12):
        tau[i] = 8 + ((i - 8 + 1) % 4)
    tau = tuple(tau)
    assert power(tau, 8) == ONE
    for ordinal, rank in enumerate(RANKS):
        seed = unrank_perm(rank)
        images = [seed]
        for _ in range(7):
            images.append(conj(tau, images[-1]))
        image_tuple = tuple(images)
        assert conj(tau, images[-1]) == seed
        assert images[4] == inv(seed)
        assert len(set(images)) == 8
        relation = ONE
        for index in RELATOR:
            relation = mul(relation, images[index])
        assert relation == ONE
        assert odd(seed) and all(odd(value) for value in images)
        assert b3(image_tuple, False) == 457
        assert b3(image_tuple, True) == 457
        order, even_count, odd_count = generated(image_tuple)
        assert (order, even_count, odd_count) == (38880, 19440, 19440)
        print(f"candidate={ordinal} rank={rank} seed={','.join(map(str, seed))}")
        for j, value in enumerate(images):
            print(f"  g{j}={','.join(map(str, value))}")
        print(f"  order={order} even={even_count} odd={odd_count} B3=457")


if __name__ == "__main__":
    main()
