"""Scalar first-shell surface-group Hamiltonians without spectral analysis."""

from __future__ import annotations

import math
from collections import defaultdict

from reproducibility.src.hyperbolic.validation_quotient import build_quotient


SparseMap = dict[tuple[int, int], float]


def first_shell_weight(*, a_over_r: float, h_over_a: float, lambda_over_a: float) -> dict[str, float]:
    h_over_r = h_over_a * a_over_r
    lambda_over_r = lambda_over_a * a_over_r
    excess_over_r = math.sqrt(h_over_r * h_over_r + a_over_r * a_over_r) - h_over_r
    q1 = math.exp(-excess_over_r / lambda_over_r)
    return {
        "a_over_r": a_over_r,
        "h_over_a": h_over_a,
        "lambda_over_a": lambda_over_a,
        "h_over_r": h_over_r,
        "lambda_over_r": lambda_over_r,
        "first_shell_excess_over_r": excess_over_r,
        "q1": q1,
        "b0": 1.0 - 8.0 * q1,
        "w_star_over_t": 1.0 / q1,
    }


def adjacency_from_edges(edge_rows: list[dict[str, object]], *, t_over_t: float = 1.0) -> SparseMap:
    matrix: defaultdict[tuple[int, int], float] = defaultdict(float)
    for edge in edge_rows:
        matrix[(int(edge["source_index"]), int(edge["target_index"]))] += -t_over_t
    return dict(matrix)


def first_shell_interlayer(
    edge_rows: list[dict[str, object]],
    *,
    dimension: int,
    q1: float,
    w_over_t: float,
) -> SparseMap:
    matrix: defaultdict[tuple[int, int], float] = defaultdict(float)
    for index in range(dimension):
        matrix[(index, index)] += w_over_t
    for edge in edge_rows:
        matrix[(int(edge["source_index"]), int(edge["target_index"]))] += w_over_t * q1
    return dict(matrix)


def bilayer_block(monolayer: SparseMap, interlayer: SparseMap, *, dimension: int) -> SparseMap:
    matrix: defaultdict[tuple[int, int], float] = defaultdict(float)
    for (row, column), value in monolayer.items():
        matrix[(row, column)] += value
        matrix[(row + dimension, column + dimension)] += value
    for (row, column), value in interlayer.items():
        matrix[(row, column + dimension)] += value
        matrix[(column + dimension, row)] += value
    return dict(matrix)


def maximum_hermiticity_residual(matrix: SparseMap) -> float:
    keys = set(matrix) | {(column, row) for row, column in matrix}
    return max((abs(matrix.get((row, column), 0.0) - matrix.get((column, row), 0.0)) for row, column in keys), default=0.0)


def permutation_residual(matrix: SparseMap, permutation: list[int]) -> float:
    transformed = {(permutation[row], permutation[column]): value for (row, column), value in matrix.items()}
    keys = set(matrix) | set(transformed)
    return max((abs(matrix.get(key, 0.0) - transformed.get(key, 0.0)) for key in keys), default=0.0)


def layer_exchange_residual(matrix: SparseMap, dimension: int) -> float:
    permutation = [index + dimension if index < dimension else index - dimension for index in range(2 * dimension)]
    return permutation_residual(matrix, permutation)


def add_matrices(left: SparseMap, right: SparseMap) -> SparseMap:
    result: defaultdict[tuple[int, int], float] = defaultdict(float)
    for matrix in (left, right):
        for key, value in matrix.items():
            result[key] += value
    return {key: value for key, value in result.items() if value != 0.0}


def scalar_multiple_identity_residual(matrix: SparseMap, *, dimension: int, scalar: float) -> float:
    keys = set(matrix) | {(index, index) for index in range(dimension)}
    return max(
        (
            abs(matrix.get((row, column), 0.0) - (scalar if row == column else 0.0))
            for row, column in keys
        ),
        default=0.0,
    )


def assemble_validation_hamiltonians(*, modulus: int, a_over_r: float, h_over_a: float, lambda_over_a: float) -> tuple[dict[str, SparseMap], dict[str, object]]:
    elements, edges, quotient_certificate = build_quotient(modulus)
    dimension = len(elements)
    shell = first_shell_weight(a_over_r=a_over_r, h_over_a=h_over_a, lambda_over_a=lambda_over_a)
    monolayer = adjacency_from_edges(edges)
    interlayer = first_shell_interlayer(
        edges,
        dimension=dimension,
        q1=shell["q1"],
        w_over_t=shell["w_star_over_t"],
    )
    bilayer = bilayer_block(monolayer, interlayer, dimension=dimension)
    c8_single = [int(row["c8_image_index"]) for row in elements]
    c8_bilayer = c8_single + [index + dimension for index in c8_single]
    even_block = add_matrices(monolayer, interlayer)
    row_nnz = [sum(1 for row, _ in bilayer if row == index) for index in range(2 * dimension)]
    residuals = {
        "monolayer_hermiticity": maximum_hermiticity_residual(monolayer),
        "interlayer_self_adjoint_at_alignment": maximum_hermiticity_residual(interlayer),
        "bilayer_hermiticity": maximum_hermiticity_residual(bilayer),
        "monolayer_c8": permutation_residual(monolayer, c8_single),
        "interlayer_c8": permutation_residual(interlayer, c8_single),
        "bilayer_c8": permutation_residual(bilayer, c8_bilayer),
        "layer_exchange": layer_exchange_residual(bilayer, dimension),
        "first_shell_root_even_block_identity": scalar_multiple_identity_residual(
            even_block, dimension=dimension, scalar=shell["w_star_over_t"]
        ),
    }
    checks = {
        "quotient_certificate": quotient_certificate["status"] == "PASS",
        "first_shell_positivity": shell["b0"] > 0.0,
        "hermiticity": max(residuals[key] for key in ("monolayer_hermiticity", "interlayer_self_adjoint_at_alignment", "bilayer_hermiticity")) <= 1.0e-12,
        "c8_symmetry": max(residuals[key] for key in ("monolayer_c8", "interlayer_c8", "bilayer_c8")) <= 1.0e-12,
        "layer_exchange_symmetry": residuals["layer_exchange"] <= 1.0e-12,
        "root_operator_identity": residuals["first_shell_root_even_block_identity"] <= 1.0e-10,
        "expected_bilayer_row_sparsity": min(row_nnz) == max(row_nnz) == 17,
        "real_time_reversal": all(isinstance(value, float) and math.isfinite(value) for value in bilayer.values()),
    }
    return {
        "monolayer_h0": monolayer,
        "interlayer_wq1": interlayer,
        "bilayer_h1": bilayer,
    }, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "CLEAN_ROOM_VALIDATION_QUOTIENT_FIRST_SHELL_AT_DECLARED_ROOT_RELATION",
        "single_layer_dimension": dimension,
        "bilayer_dimension": 2 * dimension,
        "matrix_nnz": {"monolayer_h0": len(monolayer), "interlayer_wq1": len(interlayer), "bilayer_h1": len(bilayer)},
        "bilayer_row_nnz": {"minimum": min(row_nnz), "maximum": max(row_nnz)},
        "parameters": shell,
        "residuals": residuals,
        "checks": checks,
        "spectrum_computed": False,
        "dos_computed": False,
    }


def sparse_rows(matrix: SparseMap, *, matrix_name: str) -> list[dict[str, object]]:
    return [
        {"matrix": matrix_name, "row": row, "column": column, "value_over_t": value}
        for (row, column), value in sorted(matrix.items())
    ]
