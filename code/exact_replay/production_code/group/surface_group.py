"""Deterministic word engine for the genus-two surface group.

MANUSCRIPT SOURCE:
Equation: Eq. (57), Gamma_B=<a1,b1,a2,b2 | [a1,b1][a2,b2]=e>.
Section: Genus-two regular-octagon/Bolza-surface lattice.
Model scope: non-Abelian symbolic words before finite-quotient projection.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

TOKENS = ("a1", "a1_inv", "b1", "b1_inv", "a2", "a2_inv", "b2", "b2_inv")
INVERSE = {
    "a1": "a1_inv", "a1_inv": "a1",
    "b1": "b1_inv", "b1_inv": "b1",
    "a2": "a2_inv", "a2_inv": "a2",
    "b2": "b2_inv", "b2_inv": "b2",
}
RELATOR = ("a1", "b1", "a1_inv", "b1_inv", "a2", "b2", "a2_inv", "b2_inv")


def validate_word(word: Iterable[str]) -> tuple[str, ...]:
    result = tuple(word)
    invalid = [token for token in result if token not in INVERSE]
    if invalid:
        raise ValueError(f"unknown surface-group token(s): {invalid}")
    return result


def inverse_word(word: Sequence[str]) -> tuple[str, ...]:
    return tuple(INVERSE[token] for token in reversed(validate_word(word)))


def free_reduce(word: Sequence[str]) -> tuple[str, ...]:
    stack: list[str] = []
    for token in validate_word(word):
        if stack and INVERSE[token] == stack[-1]:
            stack.pop()
        else:
            stack.append(token)
    return tuple(stack)


def _cyclic_conjugates(word: tuple[str, ...]) -> set[tuple[str, ...]]:
    return {word[index:] + word[:index] for index in range(len(word))}


def _dehn_rules() -> tuple[tuple[tuple[str, ...], tuple[str, ...]], ...]:
    cyclic = _cyclic_conjugates(RELATOR) | _cyclic_conjugates(inverse_word(RELATOR))
    rules: dict[tuple[str, ...], tuple[str, ...]] = {}
    for relation in cyclic:
        for length in range(5, len(relation) + 1):
            pattern = relation[:length]
            replacement = inverse_word(relation[length:])
            previous = rules.get(pattern)
            if previous is None or replacement < previous:
                rules[pattern] = replacement
    return tuple(sorted(rules.items(), key=lambda item: (-len(item[0]), item[0], item[1])))


DEHN_RULES = _dehn_rules()


def dehn_reduce(word: Sequence[str]) -> tuple[str, ...]:
    """Return a deterministic freely and Dehn-reduced representative.

    Each rewrite replaces more than half of a cyclic relator by the inverse
    complementary word, so length strictly decreases.
    """

    current = free_reduce(word)
    while True:
        changed = False
        for pattern, replacement in DEHN_RULES:
            width = len(pattern)
            for start in range(len(current) - width + 1):
                if current[start:start + width] == pattern:
                    current = free_reduce(current[:start] + replacement + current[start + width:])
                    changed = True
                    break
            if changed:
                break
        if not changed:
            return current


def relation_residual(word: Sequence[str]) -> tuple[str, ...]:
    """Return the deterministic Dehn residual; empty means certified identity."""

    return dehn_reduce(word)


def equivalent(left: Sequence[str], right: Sequence[str]) -> bool:
    """Decide equality by reducing left*right^-1 in the surface group."""

    return not relation_residual(tuple(left) + inverse_word(right))

