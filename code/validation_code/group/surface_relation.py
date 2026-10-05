"""VT-003 universal surface-relation closure certificate.

MANUSCRIPT SOURCE:
Equation: (57), [a1,b1][a2,b2]=e.
Section: genus-two surface-group presentation.
Model scope: the universal presentation and every homomorphic quotient/representation.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TypeVar

from production_code.group.surface_group import RELATOR, inverse_word, relation_residual


T = TypeVar("T")
Permutation = tuple[int, ...]
Matrix2 = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


def _perm_multiply(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _perm_inverse(value: Permutation) -> Permutation:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def _mat_multiply(left: Matrix2, right: Matrix2) -> Matrix2:
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def _mat_inverse(value: Matrix2) -> Matrix2:
    (a, b), (c, d) = value
    determinant = a * d - b * c
    if determinant == 0:
        raise ValueError("matrix image must be invertible")
    return ((d / determinant, -b / determinant), (-c / determinant, a / determinant))


def _evaluate(images: dict[str, T], identity: T, multiply, inverse) -> T:
    token_images = dict(images)
    for generator in ("a1", "b1", "a2", "b2"):
        token_images[f"{generator}_inv"] = inverse(images[generator])
    result = identity
    for token in RELATOR:
        result = multiply(result, token_images[token])
    return result


def validate_surface_relation() -> dict[str, object]:
    """Return exact universal, finite-quotient and representation certificates.

    MANUSCRIPT SOURCE:
    Equation: (57).
    Model scope: because the defining relator has empty presentation residual,
    every quotient homomorphism and every representation maps it to identity.
    The S3 and exact rational-matrix evaluations are independent executable
    non-Abelian witnesses, not substitutes for that universal argument.
    """

    universal = relation_residual(RELATOR) == () and relation_residual(inverse_word(RELATOR)) == ()

    identity_perm: Permutation = (0, 1, 2)
    a: Permutation = (1, 0, 2)
    b: Permutation = (0, 2, 1)
    s3_images = {"a1": a, "b1": b, "a2": b, "b2": a}
    s3_result = _evaluate(s3_images, identity_perm, _perm_multiply, _perm_inverse)

    one, zero = Fraction(1), Fraction(0)
    identity_matrix: Matrix2 = ((one, zero), (zero, one))
    matrix_a: Matrix2 = ((one, one), (zero, one))
    matrix_b: Matrix2 = ((one, zero), (one, one))
    matrix_images = {"a1": matrix_a, "b1": matrix_b, "a2": matrix_b, "b2": matrix_a}
    matrix_result = _evaluate(matrix_images, identity_matrix, _mat_multiply, _mat_inverse)

    return {
        "test_id": "VT-003",
        "criterion": "Exact",
        "universal_relator_residual": relation_residual(RELATOR),
        "universal_certificate": universal,
        "s3_nonabelian_quotient_result": s3_result,
        "rational_matrix_representation_result": matrix_result,
        "passed": universal and s3_result == identity_perm and matrix_result == identity_matrix,
    }
