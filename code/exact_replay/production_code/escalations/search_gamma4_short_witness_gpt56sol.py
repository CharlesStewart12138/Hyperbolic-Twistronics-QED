"""Search simple weight-four commutators for an exact Bolza short witness."""
from itertools import product

from production_code.group.injectivity_bridge import _geometry_from_matrix
from production_code.group.universal_cover import matrix_from_word


def inverse(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x + 4) % 8 for x in reversed(word))


def reduce_word(word: tuple[int, ...]) -> tuple[int, ...]:
    stack: list[int] = []
    for x in word:
        if stack and stack[-1] == (x + 4) % 8:
            stack.pop()
        else:
            stack.append(x)
    return tuple(stack)


def commutator(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return reduce_word(x + y + inverse(x) + inverse(y))


def main() -> None:
    hits = []
    for i, j, k, ell in product(range(8), repeat=4):
        w2 = commutator((i,), (j,))
        w3 = commutator(w2, (k,))
        w4 = commutator(w3, (ell,))
        if not w4:
            continue
        matrix = matrix_from_word(tuple(f"g{x}" for x in w4))
        based, translation, _, half_trace = _geometry_from_matrix(matrix)
        if translation < 6.0:
            hits.append((translation, based, w4, half_trace))
    hits.sort(key=lambda row: (row[0], len(row[2]), row[2]))
    print(f"hits={len(hits)}")
    for translation, based, word, trace in hits[:40]:
        print(
            f"ell={translation:.15f} based={based:.15f} depth={len(word)} "
            f"word={' '.join(f'g{x}' for x in word)} half_trace={tuple(trace)}"
        )


if __name__ == "__main__":
    main()
