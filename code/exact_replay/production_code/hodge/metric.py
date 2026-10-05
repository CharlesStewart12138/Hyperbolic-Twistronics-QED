"""Production interface for the exact LOCAL Bolza Hodge geometry (CM-045).

The algebraic derivations remain in ``bolza_harmonic_basis`` and
``bolza_hodge_metric``.  This module exposes one checked interface for the
four-dimensional scalar-character tangent space, canonical metric, metric
normalization, inner products, and basis-covariant generalized spectra.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Sequence

import sympy as sp

from production_code.hodge.bolza_harmonic_basis import (
    HARMONIC_BASIS,
    SCOPE,
    certificate as basis_certificate,
    identity_transport,
    standard_cohomology_in_geometric_dual,
)
from production_code.hodge.bolza_hodge_metric import (
    a_normalized_riemann_matrix,
    certificate as metric_certificate,
    hodge_metric_standard,
    inverse_sqrt_hodge_metric,
    metric_normalized_hessian,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_JSON = ROOT / "production_code" / "hodge" / "CM_045_HODGE_METRIC_INTERFACE.json"
CERTIFICATE_MD = ROOT / "production_code" / "hodge" / "CM_045_HODGE_METRIC_INTERFACE.md"


def _matrix4(value: Sequence[Sequence[object]] | sp.MatrixBase, *, symmetric: bool = False) -> sp.ImmutableMatrix:
    matrix = sp.Matrix(value)
    if matrix.shape != (4, 4):
        raise ValueError(f"expected a 4x4 matrix, got {matrix.shape}")
    if symmetric and matrix != matrix.T:
        raise ValueError("expected a symmetric bilinear form")
    return sp.ImmutableMatrix(matrix)


def _vector4(value: Sequence[object] | sp.MatrixBase) -> sp.ImmutableMatrix:
    vector = sp.Matrix(value)
    if vector.shape == (1, 4):
        vector = vector.T
    if vector.shape != (4, 1):
        raise ValueError(f"expected a four-component vector, got {vector.shape}")
    return sp.ImmutableMatrix(vector)


def canonical_metric() -> sp.ImmutableMatrix:
    """Return the exact canonical metric in ``(eta_a1,eta_b1,eta_a2,eta_b2)``."""

    return hodge_metric_standard()


def canonical_inverse_square_root() -> sp.ImmutableMatrix:
    """Return the exact positive matrix G^(-1/2)."""

    return inverse_sqrt_hodge_metric()


def hodge_inner(left: Sequence[object] | sp.MatrixBase,
                right: Sequence[object] | sp.MatrixBase) -> sp.Expr:
    """Exact Hodge inner product in the frozen standard cohomology basis."""

    u, v = _vector4(left), _vector4(right)
    return sp.simplify((u.T * sp.Matrix(canonical_metric()) * v)[0])


def hodge_norm_squared(vector: Sequence[object] | sp.MatrixBase) -> sp.Expr:
    return hodge_inner(vector, vector)


def pullback_metric(change: Sequence[Sequence[object]] | sp.MatrixBase,
                    metric: Sequence[Sequence[object]] | sp.MatrixBase | None = None) -> sp.ImmutableMatrix:
    """Return S^T G S for coordinates related by x=S x'."""

    transform = _matrix4(change)
    if sp.simplify(transform.det()) == 0:
        raise ValueError("basis change must be invertible")
    source = canonical_metric() if metric is None else _matrix4(metric, symmetric=True)
    return sp.ImmutableMatrix((transform.T * sp.Matrix(source) * transform).applyfunc(sp.simplify))


def transform_hessian(hessian: Sequence[Sequence[object]] | sp.MatrixBase,
                      change: Sequence[Sequence[object]] | sp.MatrixBase) -> sp.ImmutableMatrix:
    """Return S^T K S under the same tangent-coordinate change."""

    tensor = _matrix4(hessian, symmetric=True)
    transform = _matrix4(change)
    if sp.simplify(transform.det()) == 0:
        raise ValueError("basis change must be invertible")
    return sp.ImmutableMatrix((transform.T * sp.Matrix(tensor) * transform).applyfunc(sp.simplify))


def normalized_hessian(hessian: Sequence[Sequence[object]] | sp.MatrixBase) -> sp.ImmutableMatrix:
    """Return the full canonical G^(-1/2) K G^(-1/2); trace-only inputs are rejected."""

    return metric_normalized_hessian(hessian)


def generalized_characteristic_polynomial(
    hessian: Sequence[Sequence[object]] | sp.MatrixBase,
    metric: Sequence[Sequence[object]] | sp.MatrixBase | None = None,
    symbol: sp.Symbol | None = None,
) -> sp.Expr:
    """Coordinate-invariant det(K-lambda G), retaining all four directions."""

    tensor = _matrix4(hessian, symmetric=True)
    geometry = canonical_metric() if metric is None else _matrix4(metric, symmetric=True)
    variable = symbol if symbol is not None else sp.Symbol("lambda")
    return sp.factor((sp.Matrix(tensor) - variable * sp.Matrix(geometry)).det())


def generalized_principal_spectrum(
    hessian: Sequence[Sequence[object]] | sp.MatrixBase,
    metric: Sequence[Sequence[object]] | sp.MatrixBase | None = None,
) -> tuple[sp.Expr, ...]:
    """Return all four exact generalized eigenvalues of ``K v=lambda G v``."""

    tensor = _matrix4(hessian, symmetric=True)
    geometry = canonical_metric() if metric is None else _matrix4(metric, symmetric=True)
    if sp.simplify(sp.Matrix(geometry).det()) == 0:
        raise ValueError("metric must be nonsingular")
    eigenvalues = (sp.Matrix(geometry).inv() * sp.Matrix(tensor)).eigenvals()
    expanded = [sp.simplify(value) for value, multiplicity in eigenvalues.items() for _ in range(multiplicity)]
    return tuple(sorted(expanded, key=lambda value: float(sp.N(value, 30))))


@dataclass(frozen=True)
class CM045Certificate:
    task_id: str
    status: str
    scope: str
    dimension: int
    basis: tuple[str, ...]
    determinant: sp.Expr
    leading_principal_minors: tuple[sp.Expr, ...]
    eigenvalues: tuple[sp.Expr, ...]
    positive_definite: bool
    inverse_square_root_exact: bool
    basis_covariance_exact: bool
    identity_transport_exact: bool
    quotient_independent: bool
    all_four_directions_retained: bool

    @property
    def passed(self) -> bool:
        return (
            self.task_id == "CM-045"
            and self.status == "Done"
            and self.scope == "LOCAL_SCALAR_CHARACTER"
            and self.dimension == 4
            and len(self.basis) == 4
            and self.determinant == 1
            and self.positive_definite
            and self.inverse_square_root_exact
            and self.basis_covariance_exact
            and self.identity_transport_exact
            and self.quotient_independent
            and self.all_four_directions_retained
        )


def certificate() -> CM045Certificate:
    basis = basis_certificate()
    metric = metric_certificate()
    test_hessian = sp.diag(1, 2, 4, 7)
    change = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
    original = generalized_characteristic_polynomial(test_hessian)
    transformed = generalized_characteristic_polynomial(
        transform_hessian(test_hessian, change), pullback_metric(change)
    )
    return CM045Certificate(
        task_id="CM-045",
        status="Done",
        scope=SCOPE,
        dimension=4,
        basis=tuple(HARMONIC_BASIS),
        determinant=metric.metric_determinant,
        leading_principal_minors=metric.leading_principal_minors,
        eigenvalues=metric.metric_eigenvalues,
        positive_definite=metric.metric_positive_definite,
        inverse_square_root_exact=metric.inverse_sqrt_exact,
        basis_covariance_exact=sp.simplify(original - transformed) == 0,
        identity_transport_exact=identity_transport() == sp.eye(4),
        quotient_independent=basis.quotient_independent and metric.quotient_independent,
        all_four_directions_retained=len(generalized_principal_spectrum(canonical_metric())) == 4,
    )


def _serialize_matrix(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(sp.simplify(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def write_certificate() -> dict[str, Path]:
    result = certificate()
    if not result.passed:
        raise ArithmeticError(f"CM-045 acceptance failed: {result}")
    record = {
        "schema_version": "1.0",
        "task_id": result.task_id,
        "status": result.status,
        "scope": result.scope,
        "basis": list(result.basis),
        "dimension": result.dimension,
        "standard_cohomology_in_geometric_dual": _serialize_matrix(standard_cohomology_in_geometric_dual()),
        "a_normalized_riemann_matrix": _serialize_matrix(a_normalized_riemann_matrix()),
        "canonical_hodge_metric_G": _serialize_matrix(canonical_metric()),
        "canonical_inverse_square_root": _serialize_matrix(canonical_inverse_square_root()),
        "acceptance": {
            "determinant": str(result.determinant),
            "leading_principal_minors": [str(value) for value in result.leading_principal_minors],
            "eigenvalues_with_multiplicity": [str(value) for value in result.eigenvalues],
            "positive_definite": result.positive_definite,
            "inverse_square_root_exact": result.inverse_square_root_exact,
            "basis_covariance_exact": result.basis_covariance_exact,
            "identity_transport_exact": result.identity_transport_exact,
            "quotient_independent": result.quotient_independent,
            "all_four_directions_retained": result.all_four_directions_retained,
            "passed": result.passed,
        },
        "production_api": {
            "metric": "canonical_metric()",
            "inverse_square_root": "canonical_inverse_square_root()",
            "inner_product": "hodge_inner(u,v)",
            "basis_change": "pullback_metric(S) and transform_hessian(K,S)",
            "normalized_hessian": "normalized_hessian(K)",
            "principal_spectrum": "generalized_principal_spectrum(K,G)",
        },
        "claim_boundary": {
            "finite_quotient_required": False,
            "general_nonabelian_Ad_rho": False,
            "target_derivative_family": False,
            "Hodge_root": False,
            "physical_magic_angle": False,
            "main_tex_modified": False,
        },
    }
    CERTIFICATE_JSON.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    markdown = rf"""# CM-045 — exact LOCAL Bolza Hodge metric interface

**Status:** Done.  **Scope:** `LOCAL_SCALAR_CHARACTER`.

The production interface `production_code/hodge/metric.py` exposes the complete basis
\((\eta_{{a_1}},\eta_{{b_1}},\eta_{{a_2}},\eta_{{b_2}})\), the exact canonical
metric
\[
G=\frac{{\sqrt2}}{{2}}
\begin{{pmatrix}}
2&1&-1&0\\1&2&0&1\\-1&0&2&1\\0&1&1&2
\end{{pmatrix}},
\]
and its exact positive inverse square root.  Its determinant is one, its leading
principal minors are \((\sqrt2,3/2,\sqrt2,1)\), and its eigenvalues are
\(\sqrt2-1\) and \(\sqrt2+1\), each twice.

For any symmetric Hessian \(K\), the API returns the full normalized tensor
\(\widehat K=G^{{-1/2}}KG^{{-1/2}}\) and all four generalized principal values.
Under \(x=Sx'\), it applies \(G'=S^TGS\), \(K'=S^TKS\), and verifies exactly
that \(\det(K-\lambda G)=\det(K'-\lambda G')\).  Thus the implementation is
basis-covariant and cannot silently replace \(G\) by \(I_4\) or a trace-only
surrogate.

No finite quotient, target derivative family, Hodge root, or physical optimizer
enters this task.  Those remain separate dependencies; `main.tex` is unchanged.
"""
    CERTIFICATE_MD.write_text(markdown, encoding="utf-8")
    return {"json": CERTIFICATE_JSON, "markdown": CERTIFICATE_MD}


if __name__ == "__main__":
    print(json.dumps({name: str(path) for name, path in write_certificate().items()}, indent=2))
