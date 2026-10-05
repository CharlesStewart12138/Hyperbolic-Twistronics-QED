"""Exact order-eight Bolza automorphism induced by centred disk rotation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import mpmath as mp
import sympy as sp

from production_code.group.bolza_interface import (
    ZETA16,
    _field_data,
    _field_generator,
    _inverse,
    _matmul,
)
from production_code.group.nielsen import (
    GEOMETRIC_INVERSE,
    GEOMETRIC_TOKENS,
    _free_reduce as _generic_free_reduce,
    _matrix_from_standard_word,
    geometric_to_standard,
    standard_to_geometric,
)
from production_code.group.surface_group import (
    INVERSE as STANDARD_INVERSE,
    RELATOR,
    TOKENS,
    free_reduce,
    relation_residual,
)


PRIMITIVE_GENERATORS = ("a1", "b1", "a2", "b2")

# Derived by h0->h1^-1, h1->h2^-1, h2->h3^-1, h3->h0 and the
# parity-compatible Nielsen map.  These are data, not guessed permutations.
PHI8_POSITIVE: dict[str, tuple[str, ...]] = {
    "a1": ("b1_inv",),
    "b1": ("a2_inv", "b1", "a1"),
    "a2": ("a2_inv", "b1", "a1", "b1_inv", "a1_inv", "b1_inv", "b2_inv"),
    "b2": ("a1", "b1", "a1_inv", "b1_inv", "a2"),
}

PHI8_INVERSE_POSITIVE: dict[str, tuple[str, ...]] = {
    "a1": ("b2", "b1", "a1"),
    "b1": ("a1_inv",),
    "a2": ("a1_inv", "b2", "b1", "a1", "b1_inv"),
    "b2": ("a2_inv", "b2_inv", "a1"),
}

GEOMETRIC_ROTATION_POSITIVE: dict[str, tuple[str, ...]] = {
    "h0": ("h1_inv",),
    "h1": ("h2_inv",),
    "h2": ("h3_inv",),
    "h3": ("h0",),
}


@dataclass(frozen=True)
class Phi8Certificate:
    p8_01_relator_identity: bool
    p8_02_invertible: bool
    p8_03_eighth_power_identity: bool
    p8_04_no_smaller_positive_power: bool
    p8_05_declared_standard_s8_invariant: bool
    p8_06_geometric_conjugation: bool
    p8_07_parity_invariant: bool

    @property
    def mathematical_automorphism_passed(self) -> bool:
        return all((
            self.p8_01_relator_identity,
            self.p8_02_invertible,
            self.p8_03_eighth_power_identity,
            self.p8_04_no_smaller_positive_power,
            self.p8_06_geometric_conjugation,
            self.p8_07_parity_invariant,
        ))


def rotation_matrix() -> sp.ImmutableMatrix:
    """Return the exact SU(1,1) lift of ``z -> exp(i*pi/4) z``."""

    return sp.ImmutableMatrix(((ZETA16, 0), (0, ZETA16**-1)))


def _complete_standard_images(
    positive: Mapping[str, tuple[str, ...]],
) -> dict[str, tuple[str, ...]]:
    result = dict(positive)
    for token, image in positive.items():
        result[STANDARD_INVERSE[token]] = tuple(
            STANDARD_INVERSE[item] for item in reversed(image)
        )
    return result


def _complete_geometric_images(
    positive: Mapping[str, tuple[str, ...]],
) -> dict[str, tuple[str, ...]]:
    result = dict(positive)
    for token, image in positive.items():
        result[GEOMETRIC_INVERSE[token]] = tuple(
            GEOMETRIC_INVERSE[item] for item in reversed(image)
        )
    return result


PHI8 = _complete_standard_images(PHI8_POSITIVE)
PHI8_INVERSE = _complete_standard_images(PHI8_INVERSE_POSITIVE)
GEOMETRIC_ROTATION = _complete_geometric_images(GEOMETRIC_ROTATION_POSITIVE)


def _substitute_standard(
    word: Sequence[str], images: Mapping[str, tuple[str, ...]]
) -> tuple[str, ...]:
    expanded: list[str] = []
    for token in word:
        try:
            expanded.extend(images[token])
        except KeyError as exc:
            raise ValueError(f"unknown standard token: {token}") from exc
    return free_reduce(expanded)


def phi8(word: Sequence[str]) -> tuple[str, ...]:
    return _substitute_standard(word, PHI8)


def phi8_inverse(word: Sequence[str]) -> tuple[str, ...]:
    return _substitute_standard(word, PHI8_INVERSE)


def phi8_power(word: Sequence[str], power: int) -> tuple[str, ...]:
    exponent = int(power)
    if exponent != power:
        raise ValueError("power must be an integer")
    current = free_reduce(word)
    images = PHI8 if exponent >= 0 else PHI8_INVERSE
    for _ in range(abs(exponent)):
        current = _substitute_standard(current, images)
    return current


def geometric_rotation(word: Sequence[str], power: int = 1) -> tuple[str, ...]:
    exponent = int(power)
    if exponent != power or exponent < 0:
        raise ValueError("geometric rotation power must be a nonnegative integer")
    current = _generic_free_reduce(word, GEOMETRIC_INVERSE)
    for _ in range(exponent):
        expanded = tuple(item for token in current for item in GEOMETRIC_ROTATION[token])
        current = _generic_free_reduce(expanded, GEOMETRIC_INVERSE)
    return current


def parity(word: Sequence[str]) -> int:
    """Evaluate the declared all-primitive-generators-to-one map modulo two."""

    return len(free_reduce(word)) % 2


def standard_s8_images() -> dict[str, str | None]:
    """Identify phi-images with standard S8 elements using exact matrices."""

    matrices = {token: _matrix_from_standard_word((token,)) for token in TOKENS}
    result: dict[str, str | None] = {}
    for token in TOKENS:
        image_matrix = _matrix_from_standard_word(phi8((token,)))
        matches = [candidate for candidate, matrix in matrices.items() if matrix == image_matrix]
        result[token] = matches[0] if len(matches) == 1 else None
    return result


def _field_rotation_matrix() -> tuple[Any, ...]:
    data = _field_data()
    zeta16 = data["zeta16"]
    return (zeta16, data["zero"], data["zero"], zeta16**-1)


def certificate() -> Phi8Certificate:
    p8_01 = not relation_residual(phi8(RELATOR))
    p8_02 = all(
        phi8_inverse(phi8((token,))) == (token,)
        and phi8(phi8_inverse((token,))) == (token,)
        for token in TOKENS
    )
    p8_03 = all(phi8_power((token,), 8) == (token,) for token in TOKENS)

    # a1=g0, and its k-th rotated exact matrix is g_k.  Exact distinction
    # from g0 for k=1,...,7 proves no smaller positive power is the identity.
    g0 = _field_generator(0)
    p8_04 = all(_field_generator(power) != g0 for power in range(1, 8))

    s8_images = standard_s8_images()
    p8_05 = all(image is not None for image in s8_images.values())

    rotation = _field_rotation_matrix()
    inverse_rotation = _inverse(rotation)
    geometric_conjugation = all(
        _matmul(_matmul(rotation, _field_generator(index)), inverse_rotation)
        == _field_generator((index + 1) % 8)
        for index in range(8)
    )
    induced_standard_action = all(
        _matmul(
            _matmul(rotation, _matrix_from_standard_word((token,))),
            inverse_rotation,
        ) == _matrix_from_standard_word(phi8((token,)))
        for token in PRIMITIVE_GENERATORS
    )
    transported_words = all(
        geometric_to_standard(geometric_rotation(standard_to_geometric((token,))))
        == phi8((token,))
        for token in PRIMITIVE_GENERATORS
    )
    p8_06 = geometric_conjugation and induced_standard_action and transported_words
    p8_07 = all(parity(phi8((token,))) == parity((token,)) for token in PRIMITIVE_GENERATORS)
    return Phi8Certificate(p8_01, p8_02, p8_03, p8_04, p8_05, p8_06, p8_07)


def independent_numeric_conjugation_residual(dps: int = 140) -> mp.mpf:
    """Independent high-precision witness for all eight conjugation identities."""

    precision = int(dps)
    if precision < 110:
        raise ValueError("at least 110 decimal digits are required")
    with mp.workdps(precision):
        root2 = mp.sqrt(2)
        alpha = 1 + root2
        beta = mp.sqrt(2 + 2 * root2)
        zeta8 = mp.exp(mp.j * mp.pi / 4)
        zeta16 = mp.exp(mp.j * mp.pi / 8)
        rotation = mp.matrix([[zeta16, 0], [0, zeta16**-1]])

        def g(index: int) -> mp.matrix:
            return mp.matrix([
                [alpha, beta * zeta8**index],
                [beta * zeta8**(-index), alpha],
            ])

        residuals = []
        for index in range(8):
            difference = rotation * g(index) * rotation**-1 - g((index + 1) % 8)
            residuals.extend(abs(difference[row, column]) for row in range(2) for column in range(2))
        return max(residuals)

