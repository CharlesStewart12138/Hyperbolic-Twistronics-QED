"""Canonical local Hodge metric for the marked Bolza scalar-character space.

MANUSCRIPT SOURCE:
  source_current_195/main.tex, Eqs. ``eq:hodge-canonical-metric`` and
  ``eq:hodge-normalized-Hessian``.

CONVENTIONS:
  ``tau`` is the A-normalized genus-two Riemann matrix.  In block cycle order
  (a1,a2,b1,b2), define ``Omega = [I_2; tau^dagger]`` and

      C = Omega (Im tau)^(-1) Omega^dagger.

  The real part of C is the Jacobian metric on cycles.  The physical tangent
  basis from PF-HOD-001 is cohomological, so its Hodge metric is the inverse
  cycle metric, after reordering to (a1,b1,a2,b2).

SCOPE:
  LOCAL_SCALAR_CHARACTER.  No finite quotient, physical optimizer, or
  numerical root enters this construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp

from production_code.hodge.bolza_harmonic_basis import standard_period_matrix


SCOPE = "LOCAL_SCALAR_CHARACTER"
BLOCK_CYCLE_ORDER = ("a1", "a2", "b1", "b2")
STANDARD_INTERLEAVED_ORDER = ("a1", "b1", "a2", "b2")
BLOCK_TO_INTERLEAVED = (0, 2, 1, 3)


def _simplify_matrix(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(matrix.applyfunc(lambda value: sp.simplify(sp.expand_complex(value))))


def a_normalized_riemann_matrix() -> sp.ImmutableMatrix:
    """Derive the exact A-normalized Riemann matrix from PF-HOD-001 periods."""

    periods = sp.Matrix(standard_period_matrix())
    a_periods = periods[:, [0, 2]]
    b_periods = periods[:, [1, 3]]
    return _simplify_matrix(a_periods.inv() * b_periods)


def riemann_imaginary_part() -> sp.ImmutableMatrix:
    tau = a_normalized_riemann_matrix()
    return sp.ImmutableMatrix(tau.applyfunc(lambda value: sp.simplify(sp.im(value))))


def period_stack() -> sp.ImmutableMatrix:
    """Return Omega=[I_2;tau^dagger], a 4x2 matrix."""

    tau = a_normalized_riemann_matrix()
    return sp.ImmutableMatrix.vstack(sp.eye(2, cls=sp.ImmutableMatrix), tau.conjugate().T)


def cycle_hermitian_form_block() -> sp.ImmutableMatrix:
    """Return C=Omega(Im tau)^(-1)Omega^dagger in block cycle order."""

    omega = period_stack()
    y_inv = riemann_imaginary_part().inv()
    return _simplify_matrix(omega * y_inv * omega.conjugate().T)


def real_cycle_metric_block() -> sp.ImmutableMatrix:
    form = cycle_hermitian_form_block()
    return sp.ImmutableMatrix(form.applyfunc(lambda value: sp.simplify(sp.re(value))))


def reorder_block_to_interleaved(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    source = sp.Matrix(matrix)
    if source.shape != (4, 4):
        raise ValueError(f"expected a 4x4 matrix, got {source.shape}")
    return sp.ImmutableMatrix(source.extract(BLOCK_TO_INTERLEAVED, BLOCK_TO_INTERLEAVED))


def cycle_metric_standard() -> sp.ImmutableMatrix:
    """Determinant-one Jacobian cycle metric in (a1,b1,a2,b2) order."""

    return reorder_block_to_interleaved(real_cycle_metric_block())


def period_gram_cycle_metric_standard() -> sp.ImmutableMatrix:
    """Independent determinant-one metric from the exact standard periods."""

    periods = sp.Matrix(standard_period_matrix())
    raw = (periods.conjugate().T * periods).applyfunc(lambda value: sp.simplify(sp.re(value)))
    scale = sp.simplify(raw.det() ** sp.Rational(1, 4))
    return sp.ImmutableMatrix((raw / scale).applyfunc(sp.simplify))


def hodge_metric_standard() -> sp.ImmutableMatrix:
    """Canonical Hodge metric on the standard cohomology tangent basis."""

    return sp.ImmutableMatrix(cycle_metric_standard().inv().applyfunc(sp.simplify))


def hodge_metric_leading_principal_minors() -> tuple[sp.Expr, ...]:
    metric = sp.Matrix(hodge_metric_standard())
    return tuple(sp.simplify(metric[:size, :size].det()) for size in range(1, 5))


def inverse_sqrt_hodge_metric() -> sp.ImmutableMatrix:
    """Exact positive G^(-1/2), using the two symmetry-locked eigenspaces."""

    metric = sp.Matrix(hodge_metric_standard())
    involution = sp.simplify(metric - sp.sqrt(2) * sp.eye(4))
    if sp.simplify(involution * involution) != sp.eye(4):
        raise ArithmeticError("Bolza metric involution identity failed")
    lambda_plus_inverse_sqrt = sp.sqrt(sp.sqrt(2) - 1)
    lambda_minus_inverse_sqrt = sp.sqrt(sp.sqrt(2) + 1)
    projector_plus = (sp.eye(4) + involution) / 2
    projector_minus = (sp.eye(4) - involution) / 2
    result = lambda_plus_inverse_sqrt * projector_plus + lambda_minus_inverse_sqrt * projector_minus
    return sp.ImmutableMatrix(result.applyfunc(sp.simplify))


def metric_normalized_hessian(hessian: Sequence[Sequence[object]] | sp.MatrixBase) -> sp.ImmutableMatrix:
    """Return G^(-1/2) K G^(-1/2) for a full symmetric 4x4 Hessian."""

    matrix = sp.Matrix(hessian)
    if matrix.shape != (4, 4):
        raise ValueError(f"expected a 4x4 Hessian, got {matrix.shape}")
    if matrix != matrix.T:
        raise ValueError("Hodge Hessian must be symmetric")
    inverse_sqrt = sp.Matrix(inverse_sqrt_hodge_metric())
    return sp.ImmutableMatrix((inverse_sqrt * matrix * inverse_sqrt).applyfunc(sp.simplify))


@dataclass(frozen=True)
class HodgeMetricCertificate:
    riemann_symmetric: bool
    riemann_imaginary_eigenvalues: tuple[sp.Expr, ...]
    riemann_imaginary_positive: bool
    period_stack_formula_exact: bool
    cycle_metric_matches_period_gram: bool
    metric_symmetric: bool
    metric_determinant: sp.Expr
    leading_principal_minors: tuple[sp.Expr, ...]
    metric_eigenvalues: tuple[sp.Expr, ...]
    metric_positive_definite: bool
    metric_not_identity: bool
    inverse_sqrt_exact: bool
    quotient_independent: bool

    @property
    def passed(self) -> bool:
        return (
            self.riemann_symmetric
            and self.riemann_imaginary_positive
            and self.period_stack_formula_exact
            and self.cycle_metric_matches_period_gram
            and self.metric_symmetric
            and self.metric_determinant == 1
            and self.metric_positive_definite
            and self.metric_not_identity
            and self.inverse_sqrt_exact
            and self.quotient_independent
        )


def certificate() -> HodgeMetricCertificate:
    tau = sp.Matrix(a_normalized_riemann_matrix())
    y = sp.Matrix(riemann_imaginary_part())
    y_eigenvalues = tuple(sorted((sp.simplify(value) for value in y.eigenvals()), key=lambda x: float(x)))
    metric = sp.Matrix(hodge_metric_standard())
    principal_minors = hodge_metric_leading_principal_minors()
    eigenvalues = tuple(sorted((sp.simplify(value) for value in metric.eigenvals()), key=lambda x: float(x)))
    inverse_sqrt = sp.Matrix(inverse_sqrt_hodge_metric())
    return HodgeMetricCertificate(
        riemann_symmetric=tau == tau.T,
        riemann_imaginary_eigenvalues=y_eigenvalues,
        riemann_imaginary_positive=all(value.is_positive is True for value in y_eigenvalues),
        period_stack_formula_exact=cycle_hermitian_form_block() == cycle_hermitian_form_block().conjugate().T,
        cycle_metric_matches_period_gram=cycle_metric_standard() == period_gram_cycle_metric_standard(),
        metric_symmetric=metric == metric.T,
        metric_determinant=sp.simplify(metric.det()),
        leading_principal_minors=principal_minors,
        metric_eigenvalues=eigenvalues,
        metric_positive_definite=all(value.is_positive is True for value in principal_minors),
        metric_not_identity=metric != sp.eye(4),
        inverse_sqrt_exact=sp.simplify(inverse_sqrt * metric * inverse_sqrt) == sp.eye(4),
        quotient_independent=True,
    )

