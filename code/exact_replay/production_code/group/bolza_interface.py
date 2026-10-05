"""Constructive exact interface for the regular-octagon Bolza group.

This module deliberately stops at the geometric side-pairing basis.  The
Nielsen transformation to the standard genus-two commutator presentation is
a separate atomic deliverable and is not silently assumed here.

CONVENTIONS
-----------
``mobius(M, z)`` is ``(M00*z + M01)/(M10*z + M11)``.  Matrix products act by
composition, so ``mobius(M*N, z) == mobius(M, mobius(N, z))``.  The regular
octagon is centred at zero and has vertices

    v_j = 2**(-1/4) exp(i (2j+1) pi/8),  j=0,...,7.

The geometric side-pairing generator ``g_nu`` maps the side centred at
``-q*zeta8**nu`` to the side centred at ``+q*zeta8**nu`` with reversed
boundary orientation.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import mpmath as mp
import sympy as sp
from sympy import QQ


SQRT2 = sp.sqrt(2)
RHO = sp.Pow(2, -sp.Rational(1, 4))
ZETA8 = (1 + sp.I) / SQRT2
ZETA16 = sp.sqrt(2 + SQRT2) / 2 + sp.I * sp.sqrt(2 - SQRT2) / 2
Q_SIDE = sp.sqrt(SQRT2 - 1)
ETA = sp.sqrt(2 * (SQRT2 - 1))
ALPHA = 1 + SQRT2
BETA = sp.sqrt(2 + 2 * SQRT2)


@dataclass(frozen=True)
class ExactCertificate:
    """Machine-readable outcome of the four geometric identities."""

    octagon_geometry: bool
    su11: bool
    inverse_pairing: bool
    endpoint_pairing: bool
    midpoint_pairing: bool
    oriented_polygon_relation: bool

    @property
    def passed(self) -> bool:
        return all(self.__dict__.values())


def vertex(j: int) -> sp.Expr:
    """Return the exact disk-coordinate vertex ``v_j`` (indices modulo 8)."""

    return sp.expand(RHO * ZETA16 ** (2 * (int(j) % 8) + 1))


def vertices() -> tuple[sp.Expr, ...]:
    return tuple(vertex(j) for j in range(8))


def generator_matrix(nu: int) -> sp.ImmutableMatrix:
    """Return the exact SU(1,1) matrix of geometric generator ``g_nu``."""

    index = int(nu)
    if index != nu or not 0 <= index < 8:
        raise ValueError("nu must be an integer from 0 through 7")
    phase = sp.expand(ZETA8**index)
    inverse_phase = sp.expand(ZETA8 ** (-index))
    return sp.ImmutableMatrix(((ALPHA, BETA * phase), (BETA * inverse_phase, ALPHA)))


def mobius(matrix: sp.MatrixBase, z: sp.Expr) -> sp.Expr:
    """Apply an exact two-by-two matrix as a fractional linear map."""

    if matrix.shape != (2, 2):
        raise ValueError("matrix must be 2 by 2")
    return sp.cancel((matrix[0, 0] * z + matrix[0, 1]) /
                     (matrix[1, 0] * z + matrix[1, 1]))


def side_midpoint(nu: int, *, opposite: bool = False) -> sp.Expr:
    """Return the exact hyperbolic midpoint of a paired octagon side."""

    index = int(nu)
    if index != nu or not 0 <= index < 8:
        raise ValueError("nu must be an integer from 0 through 7")
    sign = -1 if opposite else 1
    return sp.expand(sign * Q_SIDE * ZETA8**index)


def oriented_polygon_word() -> tuple[tuple[int, int], ...]:
    """Return the exact boundary word in ``(g_index, exponent)`` notation."""

    basis = ((0, 1), (1, -1), (2, 1), (3, -1))
    return basis + tuple((index, -exponent) for index, exponent in basis)


@lru_cache(maxsize=1)
def _field_data() -> dict[str, Any]:
    """Build the degree-16 algebraic field used for exact certificates.

    A common algebraic field avoids branch-sensitive radical simplification.
    Equality of its elements is literal exact equality, not a tolerance test.
    """

    cos_pi_8 = sp.sqrt(2 + SQRT2) / 2
    field = QQ.algebraic_field(SQRT2, BETA, sp.I, RHO, cos_pi_8)
    one = field.one
    root2 = field.convert(SQRT2)
    beta = field.convert(BETA)
    rho = field.convert(RHO)
    imaginary = field.convert(sp.I)
    cos_value = field.convert(cos_pi_8)
    # sin(pi/8)=sqrt(2)/(4*cos(pi/8)); q=sqrt(2)/beta.
    zeta16 = cos_value + imaginary * root2 / (field.convert(4) * cos_value)
    zeta8 = zeta16 * zeta16
    q_side = root2 / beta
    alpha = one + root2
    return {
        "field": field,
        "zero": field.zero,
        "one": one,
        "rho": rho,
        "zeta16": zeta16,
        "zeta8": zeta8,
        "q_side": q_side,
        "alpha": alpha,
        "beta": beta,
    }


def _matmul(left: tuple[Any, ...], right: tuple[Any, ...]) -> tuple[Any, ...]:
    return (
        left[0] * right[0] + left[1] * right[2],
        left[0] * right[1] + left[1] * right[3],
        left[2] * right[0] + left[3] * right[2],
        left[2] * right[1] + left[3] * right[3],
    )


def _det(matrix: tuple[Any, ...]) -> Any:
    return matrix[0] * matrix[3] - matrix[1] * matrix[2]


def _inverse(matrix: tuple[Any, ...]) -> tuple[Any, ...]:
    determinant = _det(matrix)
    return (
        matrix[3] / determinant,
        -matrix[1] / determinant,
        -matrix[2] / determinant,
        matrix[0] / determinant,
    )


def _field_generator(nu: int) -> tuple[Any, ...]:
    data = _field_data()
    index = int(nu) % 8
    phase = data["zeta8"]**index
    inverse_phase = data["zeta8"] ** (-index)
    return (data["alpha"], data["beta"] * phase,
            data["beta"] * inverse_phase, data["alpha"])


def _field_vertex(j: int) -> Any:
    data = _field_data()
    return data["rho"] * data["zeta16"] ** (2 * (int(j) % 8) + 1)


def _field_mobius(matrix: tuple[Any, ...], z: Any) -> Any:
    return (matrix[0] * z + matrix[1]) / (matrix[2] * z + matrix[3])


def exact_certificate() -> ExactCertificate:
    """Prove the geometry and side-pairing identities in an algebraic field."""

    data = _field_data()
    identity = (data["one"], data["zero"], data["zero"], data["one"])

    octagon_geometry = all(
        _field_vertex(j + 1) == data["zeta8"] * _field_vertex(j)
        for j in range(8)
    ) and all(
        _field_vertex(j) * data["rho"] * data["zeta16"] ** (-(2 * j + 1))
        == data["rho"] * data["rho"]
        for j in range(8)
    )

    generators = tuple(_field_generator(nu) for nu in range(8))
    su11 = all(_det(matrix) == data["one"] for matrix in generators)
    inverse_pairing = all(
        generators[nu + 4] == _inverse(generators[nu]) for nu in range(4)
    )

    endpoint_pairing = all(
        _field_mobius(generators[nu], _field_vertex(nu + 3)) == _field_vertex(nu)
        and _field_mobius(generators[nu], _field_vertex(nu + 4)) == _field_vertex(nu - 1)
        for nu in range(8)
    )
    midpoint_pairing = all(
        _field_mobius(
            generators[nu], -data["q_side"] * data["zeta8"]**nu
        ) == data["q_side"] * data["zeta8"]**nu
        for nu in range(8)
    )

    product = identity
    for index, exponent in oriented_polygon_word():
        matrix = generators[index]
        product = _matmul(product, matrix if exponent == 1 else _inverse(matrix))
    oriented_polygon_relation = product == identity

    return ExactCertificate(
        octagon_geometry=octagon_geometry,
        su11=su11,
        inverse_pairing=inverse_pairing,
        endpoint_pairing=endpoint_pairing,
        midpoint_pairing=midpoint_pairing,
        oriented_polygon_relation=oriented_polygon_relation,
    )


def independent_numeric_residual(dps: int = 140) -> mp.mpf:
    """Independently evaluate the boundary relation with ``mpmath``.

    The computation intentionally reconstructs all constants from ``mpmath``
    rather than converting the exact algebraic-field result.
    """

    precision = int(dps)
    if precision < 110:
        raise ValueError("at least 110 decimal digits are required")
    with mp.workdps(precision):
        root2 = mp.sqrt(2)
        alpha = 1 + root2
        beta = mp.sqrt(2 + 2 * root2)
        zeta8 = mp.exp(mp.j * mp.pi / 4)

        def numeric_generator(index: int) -> mp.matrix:
            return mp.matrix([
                [alpha, beta * zeta8**index],
                [beta * zeta8**(-index), alpha],
            ])

        basis = [numeric_generator(0), numeric_generator(1)**-1,
                 numeric_generator(2), numeric_generator(3)**-1]
        product = mp.eye(2)
        for matrix in basis + [matrix**-1 for matrix in basis]:
            product = product * matrix
        return max(
            abs(product[row, column] - (1 if row == column else 0))
            for row in range(2) for column in range(2)
        )

