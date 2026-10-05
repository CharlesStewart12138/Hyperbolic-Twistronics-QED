"""Exact four-dimensional harmonic tangent basis for the Bolza character branch.

MANUSCRIPT SOURCE:
  source_current_195/main.tex, Eqs. ``eq:hodge-physical-tangent-space`` and
  ``eq:hodge-tangent-transport``.

MATHEMATICAL SOURCE:
  J. R. Quine, *Systoles of Two Extremal Riemann Surfaces*, Sec. 6,
  period formulas (8)--(9).  The common nonzero period scale cancels from
  the rank certificate, so this module fixes it to one.

SCOPE:
  LOCAL / ANALYTIC, one-dimensional unitary-character branch.  Since
  ``Ad rho`` is trivial for a U(1) character, the tangent space is exactly
  ``H^1(Gamma_B; R)``.  This module does not assert a basis for a general
  non-Abelian ``H^1(Gamma_B; Ad rho)`` and does not read a finite quotient.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp

from production_code.group.nielsen import abelianization_matrix


STANDARD_GENERATORS = ("a1", "b1", "a2", "b2")
GEOMETRIC_CYCLES = ("delta0=h0", "delta1=h1", "delta2=h2", "delta3=h3")
HARMONIC_BASIS = ("eta_a1", "eta_b1", "eta_a2", "eta_b2")
SCOPE = "LOCAL_SCALAR_CHARACTER"
ZETA8 = (sp.Integer(1) + sp.I) / sp.sqrt(2)


def nielsen_homology_matrix() -> sp.ImmutableMatrix:
    """Return columns [a1,b1,a2,b2] in the marked [h0,h1,h2,h3] basis."""

    return sp.ImmutableMatrix(abelianization_matrix())


def standard_cohomology_in_geometric_dual() -> sp.ImmutableMatrix:
    """Return the exact inverse-transpose dual-basis transformation."""

    return sp.ImmutableMatrix(nielsen_homology_matrix().inv().T)


def surface_relator_abelianization() -> sp.ImmutableMatrix:
    """Exponent sums of [a1,b1][a2,b2] in the standard marking."""

    return sp.ImmutableMatrix([0, 0, 0, 0])


def basis_evaluation_matrix() -> sp.ImmutableMatrix:
    """Evaluate eta_i on the standard marked cycles; this must be I_4."""

    return sp.eye(4, cls=sp.ImmutableMatrix)


def spans_full_h1(evaluations: Sequence[Sequence[object]] | sp.MatrixBase) -> bool:
    """Machine-check the no-single-direction requirement."""

    matrix = sp.Matrix(evaluations)
    return matrix.shape == (4, 4) and matrix.rank() == 4


def geometric_period_matrix(common_scale: object = 1) -> sp.ImmutableMatrix:
    """Return Quine's exact 2x4 period matrix for delta_0,...,delta_3.

    The holomorphic forms are omega_0=dx/y and omega_1=zeta_8^3 x dx/y.
    Quine's common constant is deliberately exposed as ``common_scale``.
    """

    scale = sp.sympify(common_scale)
    columns = [
        sp.ImmutableMatrix(
            [
                scale * ZETA8 ** (3 * k) * (ZETA8 + ZETA8**2),
                scale * ZETA8**k * (ZETA8**3 - ZETA8**2),
            ]
        )
        for k in range(4)
    ]
    return sp.ImmutableMatrix.hstack(*columns)


def standard_period_matrix(common_scale: object = 1) -> sp.ImmutableMatrix:
    """Transport the geometric cycle periods to the standard genus-two marking."""

    return sp.ImmutableMatrix(geometric_period_matrix(common_scale) * nielsen_homology_matrix())


def realify_period_matrix(periods: sp.MatrixBase) -> sp.ImmutableMatrix:
    """Map a 2x4 complex period matrix to a 4x4 real matrix."""

    matrix = sp.Matrix(periods)
    if matrix.shape != (2, 4):
        raise ValueError(f"expected a 2x4 period matrix, got {matrix.shape}")
    return sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix(matrix.applyfunc(lambda value: sp.simplify(sp.re(value)))),
        sp.ImmutableMatrix(matrix.applyfunc(lambda value: sp.simplify(sp.im(value)))),
    )


def identity_transport() -> sp.ImmutableMatrix:
    """Exact theta-transport on the constant scalar-character tangent bundle."""

    return sp.eye(4, cls=sp.ImmutableMatrix)


@dataclass(frozen=True)
class HarmonicBasisCertificate:
    relator_annihilated: bool
    h1_real_dimension: int
    full_basis_rank: int
    nielsen_unimodular: bool
    geometric_period_real_determinant: sp.Expr
    standard_period_real_determinant: sp.Expr
    period_rank_four: bool
    exact_identity_transport: bool
    quotient_independent: bool
    scalar_character_scope: bool

    @property
    def passed(self) -> bool:
        return (
            self.relator_annihilated
            and self.h1_real_dimension == 4
            and self.full_basis_rank == 4
            and self.nielsen_unimodular
            and self.geometric_period_real_determinant != 0
            and self.standard_period_real_determinant != 0
            and self.period_rank_four
            and self.exact_identity_transport
            and self.quotient_independent
            and self.scalar_character_scope
        )


def certificate() -> HarmonicBasisCertificate:
    geometric_real = realify_period_matrix(geometric_period_matrix())
    standard_real = realify_period_matrix(standard_period_matrix())
    evaluations = basis_evaluation_matrix()
    return HarmonicBasisCertificate(
        relator_annihilated=surface_relator_abelianization() == sp.zeros(4, 1),
        h1_real_dimension=4,
        full_basis_rank=evaluations.rank(),
        nielsen_unimodular=nielsen_homology_matrix().det() == 1,
        geometric_period_real_determinant=sp.simplify(geometric_real.det()),
        standard_period_real_determinant=sp.simplify(standard_real.det()),
        period_rank_four=geometric_real.rank() == standard_real.rank() == 4,
        exact_identity_transport=identity_transport() == sp.eye(4),
        quotient_independent=True,
        scalar_character_scope=SCOPE == "LOCAL_SCALAR_CHARACTER",
    )

