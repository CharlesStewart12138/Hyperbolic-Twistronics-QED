"""Explicit Nielsen transport for the constructive Bolza group interface.

The oriented polygon basis ``(h0,h1,h2,h3)`` is transported to the standard
genus-two basis ``(a1,b1,a2,b2)`` without treating a relabelling as a proof.
Both free-group substitutions and their exact SU(1,1) matrices are certified.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import mpmath as mp

from production_code.group.bolza_interface import (
    _field_data,
    _field_generator,
    _inverse,
    _matmul,
)
from production_code.group.surface_group import INVERSE as STANDARD_INVERSE
from production_code.group.surface_group import RELATOR as STANDARD_RELATOR
from production_code.group.surface_group import TOKENS as STANDARD_TOKENS


GEOMETRIC_TOKENS = (
    "h0", "h0_inv", "h1", "h1_inv",
    "h2", "h2_inv", "h3", "h3_inv",
)
GEOMETRIC_INVERSE = {
    "h0": "h0_inv", "h0_inv": "h0",
    "h1": "h1_inv", "h1_inv": "h1",
    "h2": "h2_inv", "h2_inv": "h2",
    "h3": "h3_inv", "h3_inv": "h3",
}
GEOMETRIC_RELATOR = (
    "h0", "h1", "h2", "h3",
    "h0_inv", "h1_inv", "h2_inv", "h3_inv",
)

# Standard generators written in the oriented geometric polygon basis.
STANDARD_TO_GEOMETRIC_POSITIVE: dict[str, tuple[str, ...]] = {
    "a1": ("h0",),
    "b1": ("h1",),
    "a2": ("h1", "h0", "h2"),
    "b2": ("h3", "h0_inv", "h1_inv"),
}

# The exact inverse Nielsen substitution.
GEOMETRIC_TO_STANDARD_POSITIVE: dict[str, tuple[str, ...]] = {
    "h0": ("a1",),
    "h1": ("b1",),
    "h2": ("a1_inv", "b1_inv", "a2"),
    "h3": ("b2", "b1", "a1"),
}


@dataclass(frozen=True)
class NielsenCertificate:
    standard_roundtrip: bool
    geometric_roundtrip: bool
    standard_relator_to_geometric: bool
    geometric_relator_to_standard: bool
    unimodular_abelianization: bool
    exact_matrix_reconstruction: bool
    exact_standard_matrix_relation: bool

    @property
    def passed(self) -> bool:
        return all(self.__dict__.values())


def _inverse_word(word: Sequence[str], inverse: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(inverse[token] for token in reversed(tuple(word)))


def _free_reduce(word: Sequence[str], inverse: Mapping[str, str]) -> tuple[str, ...]:
    stack: list[str] = []
    for token in word:
        if token not in inverse:
            raise ValueError(f"unknown token: {token}")
        if stack and inverse[token] == stack[-1]:
            stack.pop()
        else:
            stack.append(token)
    return tuple(stack)


def _complete_substitution(
    positive: Mapping[str, tuple[str, ...]],
    source_inverse: Mapping[str, str],
    target_inverse: Mapping[str, str],
) -> dict[str, tuple[str, ...]]:
    result = dict(positive)
    for token, image in positive.items():
        result[source_inverse[token]] = _inverse_word(image, target_inverse)
    return result


STANDARD_TO_GEOMETRIC = _complete_substitution(
    STANDARD_TO_GEOMETRIC_POSITIVE, STANDARD_INVERSE, GEOMETRIC_INVERSE
)
GEOMETRIC_TO_STANDARD = _complete_substitution(
    GEOMETRIC_TO_STANDARD_POSITIVE, GEOMETRIC_INVERSE, STANDARD_INVERSE
)


def _substitute(
    word: Sequence[str],
    substitution: Mapping[str, tuple[str, ...]],
    target_inverse: Mapping[str, str],
) -> tuple[str, ...]:
    expanded: list[str] = []
    for token in word:
        try:
            expanded.extend(substitution[token])
        except KeyError as exc:
            raise ValueError(f"unknown source token: {token}") from exc
    return _free_reduce(expanded, target_inverse)


def standard_to_geometric(word: Sequence[str]) -> tuple[str, ...]:
    return _substitute(word, STANDARD_TO_GEOMETRIC, GEOMETRIC_INVERSE)


def geometric_to_standard(word: Sequence[str]) -> tuple[str, ...]:
    return _substitute(word, GEOMETRIC_TO_STANDARD, STANDARD_INVERSE)


def abelianization_matrix() -> tuple[tuple[int, ...], ...]:
    """Columns are ``a1,b1,a2,b2`` in the ``h0,h1,h2,h3`` basis."""

    return (
        (1, 0, 1, -1),
        (0, 1, 1, -1),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )


def _det4(matrix: tuple[tuple[int, ...], ...]) -> int:
    total = 0
    for column in range(4):
        minor = tuple(
            tuple(matrix[row][other] for other in range(4) if other != column)
            for row in range(1, 4)
        )
        determinant3 = (
            minor[0][0] * (minor[1][1] * minor[2][2] - minor[1][2] * minor[2][1])
            - minor[0][1] * (minor[1][0] * minor[2][2] - minor[1][2] * minor[2][0])
            + minor[0][2] * (minor[1][0] * minor[2][1] - minor[1][1] * minor[2][0])
        )
        total += (-1)**column * matrix[0][column] * determinant3
    return total


def _identity_matrix() -> tuple[Any, ...]:
    data = _field_data()
    return (data["one"], data["zero"], data["zero"], data["one"])


def _oriented_h_matrices() -> tuple[tuple[Any, ...], ...]:
    return (
        _field_generator(0),
        _inverse(_field_generator(1)),
        _field_generator(2),
        _inverse(_field_generator(3)),
    )


def _matrix_from_geometric_word(word: Sequence[str]) -> tuple[Any, ...]:
    h_matrices = _oriented_h_matrices()
    product = _identity_matrix()
    for token in word:
        if token not in GEOMETRIC_INVERSE:
            raise ValueError(f"unknown geometric token: {token}")
        index = int(token[1])
        matrix = h_matrices[index]
        if token.endswith("_inv"):
            matrix = _inverse(matrix)
        product = _matmul(product, matrix)
    return product


def _standard_matrices() -> dict[str, tuple[Any, ...]]:
    result = {
        token: _matrix_from_geometric_word(image)
        for token, image in STANDARD_TO_GEOMETRIC_POSITIVE.items()
    }
    result.update({STANDARD_INVERSE[token]: _inverse(matrix) for token, matrix in tuple(result.items())})
    return result


def _matrix_from_standard_word(word: Sequence[str]) -> tuple[Any, ...]:
    matrices = _standard_matrices()
    product = _identity_matrix()
    for token in word:
        try:
            product = _matmul(product, matrices[token])
        except KeyError as exc:
            raise ValueError(f"unknown standard token: {token}") from exc
    return product


def certificate() -> NielsenCertificate:
    standard_samples = tuple((token,) for token in STANDARD_TOKENS) + (STANDARD_RELATOR,)
    geometric_samples = tuple((token,) for token in GEOMETRIC_TOKENS) + (GEOMETRIC_RELATOR,)
    standard_roundtrip = all(
        geometric_to_standard(standard_to_geometric(word))
        == _free_reduce(word, STANDARD_INVERSE)
        for word in standard_samples
    )
    geometric_roundtrip = all(
        standard_to_geometric(geometric_to_standard(word))
        == _free_reduce(word, GEOMETRIC_INVERSE)
        for word in geometric_samples
    )
    standard_relator_to_geometric = standard_to_geometric(STANDARD_RELATOR) == GEOMETRIC_RELATOR
    geometric_relator_to_standard = geometric_to_standard(GEOMETRIC_RELATOR) == STANDARD_RELATOR
    unimodular_abelianization = _det4(abelianization_matrix()) == 1

    h_matrices = _oriented_h_matrices()
    exact_matrix_reconstruction = all(
        _matrix_from_standard_word(GEOMETRIC_TO_STANDARD_POSITIVE[f"h{index}"])
        == h_matrices[index]
        for index in range(4)
    )
    exact_standard_matrix_relation = _matrix_from_standard_word(STANDARD_RELATOR) == _identity_matrix()
    return NielsenCertificate(
        standard_roundtrip=standard_roundtrip,
        geometric_roundtrip=geometric_roundtrip,
        standard_relator_to_geometric=standard_relator_to_geometric,
        geometric_relator_to_standard=geometric_relator_to_standard,
        unimodular_abelianization=unimodular_abelianization,
        exact_matrix_reconstruction=exact_matrix_reconstruction,
        exact_standard_matrix_relation=exact_standard_matrix_relation,
    )


def independent_numeric_residual(dps: int = 140) -> mp.mpf:
    """Independently evaluate ``[a1,b1][a2,b2]`` after Nielsen transport."""

    precision = int(dps)
    if precision < 110:
        raise ValueError("at least 110 decimal digits are required")
    with mp.workdps(precision):
        root2 = mp.sqrt(2)
        alpha = 1 + root2
        beta = mp.sqrt(2 + 2 * root2)
        zeta8 = mp.exp(mp.j * mp.pi / 4)

        def g(index: int) -> mp.matrix:
            return mp.matrix([
                [alpha, beta * zeta8**index],
                [beta * zeta8**(-index), alpha],
            ])

        h0, h1, h2, h3 = g(0), g(1)**-1, g(2), g(3)**-1
        a1 = h0
        b1 = h1
        a2 = h1 * h0 * h2
        b2 = h3 * h0**-1 * h1**-1

        def commutator(left: mp.matrix, right: mp.matrix) -> mp.matrix:
            return left * right * left**-1 * right**-1

        product = commutator(a1, b1) * commutator(a2, b2)
        return max(
            abs(product[row, column] - (1 if row == column else 0))
            for row in range(2) for column in range(2)
        )

