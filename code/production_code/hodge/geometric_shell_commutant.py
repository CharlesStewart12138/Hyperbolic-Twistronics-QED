"""Exact physical-shell Hodge commutant audit for the Bolza C8 action."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from production_code.group.automorphism import PHI8_POSITIVE
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD


STANDARD = ("a1", "b1", "a2", "b2")
ABELIAN = {
    "a1": (1, 0, 0, 0), "a1_inv": (-1, 0, 0, 0),
    "b1": (0, 1, 0, 0), "b1_inv": (0, -1, 0, 0),
    "a2": (0, 0, 1, 0), "a2_inv": (0, 0, -1, 0),
    "b2": (0, 0, 0, 1), "b2_inv": (0, 0, 0, -1),
}


def abelianization(word) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix([sum(ABELIAN[token][i] for token in word) for i in range(4)])


def phi8_homology_matrix() -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix.hstack(*(abelianization(PHI8_POSITIVE[token]) for token in STANDARD))


def geometric_covectors() -> tuple[sp.ImmutableMatrix, ...]:
    return tuple(abelianization(GEOMETRIC_TO_STANDARD_WORD[i]) for i in range(8))


def physical_first_shell_tensor() -> sp.ImmutableMatrix:
    vectors = geometric_covectors()[:4]
    return sp.ImmutableMatrix(sum((vector * vector.T for vector in vectors), sp.zeros(4)))


def hodge_metric() -> sp.ImmutableMatrix:
    r = sp.sqrt(2)
    return sp.ImmutableMatrix([
        [r, r / 2, -r / 2, 0],
        [r / 2, r, 0, r / 2],
        [-r / 2, 0, r, r / 2],
        [0, r / 2, r / 2, r],
    ])


def tangent_c8_action() -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(phi8_homology_matrix().inv().T)


def selfadjoint_commutant_dimension() -> int:
    u = tangent_c8_action()
    g = hodge_metric()
    symbols = sp.symbols("a0:16")
    a = sp.Matrix(4, 4, symbols)
    equations = list(a * u - u * a) + list(a.T * g - g * a)
    coefficient, _ = sp.linear_eq_to_matrix(equations, symbols)
    return 16 - coefficient.rank()


def exact_certificate() -> dict[str, object]:
    p = phi8_homology_matrix()
    u = tangent_c8_action()
    g = hodge_metric()
    c = physical_first_shell_tensor()
    a = sp.ImmutableMatrix(g.inv() * c)
    mu_minus = sp.sqrt(2) - 1
    mu_plus = sp.sqrt(2) + 1
    projector_minus = sp.ImmutableMatrix((mu_plus * sp.eye(4) - a) / 2)
    projector_plus = sp.ImmutableMatrix((a - mu_minus * sp.eye(4)) / 2)
    vectors = geometric_covectors()
    c8_cycles_shell = all(p * vectors[i] == vectors[(i + 1) % 8] for i in range(8))
    generalized = a.eigenvals()
    commutant_dim = selfadjoint_commutant_dimension()
    return {
        "phi8_homology_order_8": p**8 == sp.eye(4),
        "phi8_cycles_geometric_covectors": c8_cycles_shell,
        "hodge_metric_invariant": sp.simplify(u.T * g * u - g) == sp.zeros(4),
        "physical_first_shell_invariant": sp.simplify(u.T * c * u - c) == sp.zeros(4),
        "C8_characteristic_polynomial": str(sp.factor(u.charpoly().as_expr())),
        "G_selfadjoint_commutant_dimension": commutant_dim,
        "G_inverse_C_is_G_selfadjoint": sp.simplify(a.T * g - g * a) == sp.zeros(4),
        "G_inverse_C_commutes_with_C8": sp.simplify(a * u - u * a) == sp.zeros(4),
        "G_inverse_C_is_scalar": bool(all(a[i, j] == 0 for i in range(4) for j in range(4) if i != j) and all(a[i, i] == a[0, 0] for i in range(1, 4))),
        "generalized_eigenvalues_C_relative_to_G": {
            str(mu_minus): int(generalized[mu_minus]),
            str(mu_plus): int(generalized[mu_plus]),
        },
        "sector_projectors": {
            "minus_rank": projector_minus.rank(),
            "plus_rank": projector_plus.rank(),
            "sum_identity": sp.simplify(projector_minus + projector_plus) == sp.eye(4),
            "orthogonal": sp.simplify(projector_minus * projector_plus) == sp.zeros(4),
            "minus_idempotent": sp.simplify(projector_minus**2 - projector_minus) == sp.zeros(4),
            "plus_idempotent": sp.simplify(projector_plus**2 - projector_plus) == sp.zeros(4),
        },
        "scalar_commutant_hypothesis_passed": commutant_dim == 1 and a.is_scalar(),
    }


def _matrix_strings(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(sp.simplify(value)) for value in matrix.row(i)] for i in range(matrix.rows)]


def write_certificate(output_dir: Path) -> dict[str, Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    p = phi8_homology_matrix()
    u = tangent_c8_action()
    g = hodge_metric()
    c = physical_first_shell_tensor()
    a = sp.ImmutableMatrix(g.inv() * c)
    mu_minus, mu_plus = sp.sqrt(2) - 1, sp.sqrt(2) + 1
    p_minus = sp.ImmutableMatrix((mu_plus * sp.eye(4) - a) / 2)
    p_plus = sp.ImmutableMatrix((a - mu_minus * sp.eye(4)) / 2)
    checks = exact_certificate()
    if not all((
        checks["phi8_homology_order_8"], checks["phi8_cycles_geometric_covectors"],
        checks["hodge_metric_invariant"], checks["physical_first_shell_invariant"],
        checks["G_selfadjoint_commutant_dimension"] == 2,
        checks["G_inverse_C_is_G_selfadjoint"], checks["G_inverse_C_commutes_with_C8"],
        not checks["G_inverse_C_is_scalar"], not checks["scalar_commutant_hypothesis_passed"],
    )):
        raise AssertionError("geometric-shell commutant certificate failed")
    record = {
        "schema_version": "1.0",
        "task_id": "PF-HOD-004-GEOMETRIC-COMMUTANT",
        "status": "Done_SCIENTIFIC_FALSIFICATION",
        "scope": "LOCAL S8_GEOMETRIC Hodge tangent space",
        "basis": list(STANDARD),
        "geometric_covectors_g0_to_g7": [_matrix_strings(vector) for vector in geometric_covectors()],
        "phi8_homology_matrix": _matrix_strings(p),
        "tangent_C8_action_U=P^{-T}": _matrix_strings(u),
        "hodge_metric_G": _matrix_strings(g),
        "physical_first_shell_tensor_C_S": _matrix_strings(c),
        "G_inverse_C_S": _matrix_strings(a),
        "exact_checks": checks,
        "C8_real_sectors": {
            "minus": {"generalized_weight": str(mu_minus), "multiplicity": 2, "projector": _matrix_strings(p_minus)},
            "plus": {"generalized_weight": str(mu_plus), "multiplicity": 2, "projector": _matrix_strings(p_plus)},
        },
        "theorem": (
            "For any microscopic point group preserving both G and the rebuilt physical C_S, "
            "A=G^{-1}C_S is a non-scalar G-self-adjoint commuting endomorphism. Therefore its "
            "G-self-adjoint commutant cannot be R I, even if extra reflection symmetry is added."
        ),
        "consequence": {
            "single_scalar_q_infinity_authorized": False,
            "scalar_root_equation_authorized": False,
            "required_full_kernel_form": "two-sector/full tensor B_infinity and 2t*C_S-w*B_infinity=0",
            "common_tensor_root_condition": "both rank-2 sector coefficients vanish at the same (theta,w)",
            "trace_root_sufficient": False,
        },
        "main_tex_modified": False,
    }
    json_path = directory / "GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.json"
    md_path = directory / "GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.md"
    json_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(
        "# Physical-shell Hodge commutant certificate\n\n"
        "The physical first-shell tensor was rebuilt from the four positive `S8_GEOMETRIC` covectors. In the frozen standard cohomology coordinates,\n\n"
        "```text\nC_S = [[ 3, 2,-1, 1],\n       [ 2, 3,-1, 1],\n       [-1,-1, 1, 0],\n       [ 1, 1, 0, 1]].\n```\n\n"
        "The exact C8 tangent action preserves both the nonidentity Hodge metric `G` and this `C_S`. The `G`-self-adjoint C8 commutant has dimension 2, not 1. More decisively, `A=G^{-1}C_S` is non-scalar, `G`-self-adjoint, and commutes with every symmetry that preserves both `G` and `C_S`. Its two generalized eigenvalues are\n\n"
        "```text\nsqrt(2)-1  (multiplicity 2),\nsqrt(2)+1  (multiplicity 2).\n```\n\n"
        "Therefore no additional reflection or point-group symmetry that also preserves the physical kinetic tensor can make the relevant self-adjoint commutant scalar. The scalar-locking premise `C_S=c_S G` and the resulting one-number `q_infinity` are false for `S8_GEOMETRIC`.\n\n"
        "The legal continuation is the full tensor equation `2t C_S-w B_infinity=0`, equivalently simultaneous cancellation in the two rank-2 C8 sectors. A trace root or either directional root is insufficient. The earlier scalar `q_infinity` interval is retained only as a historical `S8_PRESENTATION`/unrepaired-shell diagnostic and cannot be promoted.\n\n"
        "`main.tex` remains locked.\n",
        encoding="utf-8",
    )
    return {"json": json_path, "markdown": md_path}


if __name__ == "__main__":
    print({name: str(path) for name, path in write_certificate(Path("production_code/hodge")).items()})
