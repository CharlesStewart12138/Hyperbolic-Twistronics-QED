"""Exact parity homomorphism from the genus-two surface group to Z/2Z."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from production_code.group.automorphism import PRIMITIVE_GENERATORS, phi8
from production_code.group.surface_group import (
    INVERSE,
    RELATOR,
    TOKENS,
    free_reduce,
    inverse_word,
    validate_word,
)


@dataclass(frozen=True)
class ParityCertificate:
    relator_in_kernel: bool
    surjective: bool
    homomorphism: bool
    kernel_normal: bool
    phi8_invariant: bool

    @property
    def passed(self) -> bool:
        return all(self.__dict__.values())


def parity(word: Sequence[str]) -> int:
    """Evaluate ``pi`` with every signed primitive generator mapped to one.

    Free cancellation removes two letters and hence does not change this
    value.  The surface relator has length eight, so the map descends from the
    free group to the declared genus-two quotient.
    """

    return len(validate_word(word)) % 2


def in_kernel(word: Sequence[str]) -> bool:
    return parity(word) == 0


def multiply(left: Sequence[str], right: Sequence[str]) -> tuple[str, ...]:
    return free_reduce(tuple(left) + tuple(right))


def homomorphism_identity(left: Sequence[str], right: Sequence[str]) -> bool:
    return parity(multiply(left, right)) == (parity(left) + parity(right)) % 2


def conjugate(conjugator: Sequence[str], word: Sequence[str]) -> tuple[str, ...]:
    return free_reduce(tuple(conjugator) + tuple(word) + inverse_word(conjugator))


def normal_kernel_identity(conjugator: Sequence[str], kernel_word: Sequence[str]) -> bool:
    """Check the normal-kernel implication for explicit words."""

    if not in_kernel(kernel_word):
        raise ValueError("kernel_word must lie in ker(pi)")
    return in_kernel(conjugate(conjugator, kernel_word))


def phi8_parity_identity(word: Sequence[str]) -> bool:
    return parity(phi8(word)) == parity(word)


def certificate() -> ParityCertificate:
    relator_in_kernel = in_kernel(RELATOR)
    surjective = parity(("a1",)) == 1

    # Generator images determine a homomorphism from the free group.  Since
    # the single defining relator maps to zero, it descends to Gamma_B.
    samples = tuple((token,) for token in TOKENS) + (
        ("a1", "b1", "a2_inv"),
        RELATOR,
    )
    homomorphism = all(homomorphism_identity(left, right) for left in samples for right in samples)

    even_samples = (
        (),
        RELATOR,
        ("a1", "b1"),
        ("a2_inv", "b2"),
        ("a1", "b1", "a2", "b2_inv"),
    )
    kernel_normal = all(
        normal_kernel_identity(conjugator, kernel_word)
        for conjugator in samples for kernel_word in even_samples
    )
    phi8_invariant = all(
        phi8_parity_identity((token,)) for token in PRIMITIVE_GENERATORS
    ) and all(phi8_parity_identity(word) for word in samples)

    return ParityCertificate(
        relator_in_kernel=relator_in_kernel,
        surjective=surjective,
        homomorphism=homomorphism,
        kernel_normal=kernel_normal,
        phi8_invariant=phi8_invariant,
    )

