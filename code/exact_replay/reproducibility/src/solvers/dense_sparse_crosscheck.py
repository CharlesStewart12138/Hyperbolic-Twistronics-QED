"""Dense-versus-sparse Hermitian eigensolver cross-checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg


Edge = Literal["lowest", "highest"]


@dataclass(frozen=True)
class CrosscheckTolerances:
    hermiticity: float = 1.0e-13
    eigenvalue: float = 1.0e-10
    dense_residual: float = 1.0e-12
    sparse_residual: float = 1.0e-10
    orthogonality: float = 1.0e-10


def _normalized_frobenius_residual(matrix: np.ndarray, eigenvalues: np.ndarray, eigenvectors: np.ndarray) -> float:
    residual = matrix @ eigenvectors - eigenvectors * eigenvalues[np.newaxis, :]
    denominator = max(float(np.linalg.norm(matrix, ord="fro")), float(np.finfo(float).eps))
    return float(np.linalg.norm(residual, ord="fro") / denominator)


def _orthogonality_error(eigenvectors: np.ndarray) -> float:
    identity = np.eye(eigenvectors.shape[1], dtype=eigenvectors.dtype)
    return float(np.linalg.norm(eigenvectors.conj().T @ eigenvectors - identity, ord=2))


def _deterministic_start_vector(size: int, complex_matrix: bool) -> np.ndarray:
    indices = np.arange(1, size + 1, dtype=float)
    vector = np.cos(np.pi * indices / (size + 1)) + 0.37 * np.sin(2.0 * np.pi * indices / (size + 1))
    if complex_matrix:
        vector = vector.astype(complex) + 0.19j * np.sin(3.0 * np.pi * indices / (size + 1))
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        raise ValueError("deterministic sparse-solver start vector has zero norm")
    return vector / norm


def crosscheck_hermitian(
    matrix: np.ndarray | scipy.sparse.spmatrix,
    *,
    k: int,
    edge: Edge,
    tolerances: CrosscheckTolerances | None = None,
) -> dict[str, object]:
    """Cross-check selected Hermitian eigenpairs with dense and sparse solvers.

    The dense path uses ``scipy.linalg.eigh``.  The sparse path uses
    ``scipy.sparse.linalg.eigsh`` with an explicit deterministic start vector.
    """

    limits = tolerances or CrosscheckTolerances()
    dense_matrix = matrix.toarray() if scipy.sparse.issparse(matrix) else np.asarray(matrix)
    if dense_matrix.ndim != 2 or dense_matrix.shape[0] != dense_matrix.shape[1]:
        raise ValueError("matrix must be square")
    size = dense_matrix.shape[0]
    if size < 3:
        raise ValueError("matrix dimension must be at least 3")
    if not isinstance(k, int) or not 1 <= k < size:
        raise ValueError("k must satisfy 1 <= k < matrix dimension")
    if edge not in {"lowest", "highest"}:
        raise ValueError("edge must be 'lowest' or 'highest'")
    if not np.all(np.isfinite(dense_matrix)):
        raise ValueError("matrix contains non-finite entries")

    matrix_norm = max(float(np.linalg.norm(dense_matrix, ord="fro")), float(np.finfo(float).eps))
    hermiticity_error = float(np.linalg.norm(dense_matrix - dense_matrix.conj().T, ord="fro") / matrix_norm)
    if hermiticity_error > limits.hermiticity:
        raise ValueError(
            f"matrix is not Hermitian within tolerance: {hermiticity_error:.3e} > {limits.hermiticity:.3e}"
        )

    dense_values_all, dense_vectors_all = scipy.linalg.eigh(dense_matrix, check_finite=True, driver="evr")
    if edge == "lowest":
        dense_values = dense_values_all[:k]
        dense_vectors = dense_vectors_all[:, :k]
        which = "SA"
    else:
        dense_values = dense_values_all[-k:]
        dense_vectors = dense_vectors_all[:, -k:]
        which = "LA"

    sparse_matrix = scipy.sparse.csr_matrix(dense_matrix)
    sparse_values, sparse_vectors = scipy.sparse.linalg.eigsh(
        sparse_matrix,
        k=k,
        which=which,
        tol=min(limits.sparse_residual * 0.1, 1.0e-12),
        maxiter=max(20 * size, 1000),
        v0=_deterministic_start_vector(size, np.iscomplexobj(dense_matrix)),
        return_eigenvectors=True,
    )
    order = np.argsort(sparse_values)
    sparse_values = np.asarray(sparse_values[order])
    sparse_vectors = np.asarray(sparse_vectors[:, order])

    eigenvalue_error = float(np.max(np.abs(dense_values - sparse_values)))
    dense_residual = _normalized_frobenius_residual(dense_matrix, dense_values, dense_vectors)
    sparse_residual = _normalized_frobenius_residual(dense_matrix, sparse_values, sparse_vectors)
    dense_orthogonality = _orthogonality_error(dense_vectors)
    sparse_orthogonality = _orthogonality_error(sparse_vectors)
    checks = {
        "hermiticity": hermiticity_error <= limits.hermiticity,
        "eigenvalue_agreement": eigenvalue_error <= limits.eigenvalue,
        "dense_residual": dense_residual <= limits.dense_residual,
        "sparse_residual": sparse_residual <= limits.sparse_residual,
        "dense_orthogonality": dense_orthogonality <= limits.orthogonality,
        "sparse_orthogonality": sparse_orthogonality <= limits.orthogonality,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "dimension": size,
        "k": k,
        "edge": edge,
        "matrix_dtype": str(dense_matrix.dtype),
        "dense_solver": "scipy.linalg.eigh(driver='evr')",
        "sparse_solver": f"scipy.sparse.linalg.eigsh(which='{which}')",
        "tolerances": asdict(limits),
        "metrics": {
            "hermiticity_relative_frobenius": hermiticity_error,
            "max_abs_eigenvalue_difference": eigenvalue_error,
            "dense_relative_frobenius_residual": dense_residual,
            "sparse_relative_frobenius_residual": sparse_residual,
            "dense_orthogonality_2norm": dense_orthogonality,
            "sparse_orthogonality_2norm": sparse_orthogonality,
        },
        "dense_eigenvalues": [float(value) for value in dense_values],
        "sparse_eigenvalues": [float(value) for value in sparse_values],
        "checks": checks,
        "failed_checks": failed,
    }
