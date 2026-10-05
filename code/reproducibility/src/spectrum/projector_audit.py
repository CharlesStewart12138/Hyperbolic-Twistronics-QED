"""Automated rank, projector-quality, and subspace-overlap audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import scipy.linalg


@dataclass(frozen=True)
class ProjectorTolerances:
    hermiticity: float = 1.0e-12
    idempotency: float = 1.0e-12
    trace_rank: float = 1.0e-10
    eigenvalue_binary: float = 1.0e-10


def projector_from_basis(basis: np.ndarray) -> np.ndarray:
    """Build an orthogonal projector after validating basis orthonormality."""

    vectors = np.asarray(basis)
    if vectors.ndim != 2 or vectors.shape[0] < vectors.shape[1] or vectors.shape[1] < 1:
        raise ValueError("basis must have shape (ambient_dimension, positive_rank)")
    gram = vectors.conj().T @ vectors
    defect = float(np.linalg.norm(gram - np.eye(vectors.shape[1]), ord=2))
    if defect > 1.0e-10:
        raise ValueError(f"basis is not orthonormal: defect={defect:.3e}")
    return vectors @ vectors.conj().T


def audit_projector(projector: np.ndarray, tolerances: ProjectorTolerances | None = None) -> dict[str, object]:
    limits = tolerances or ProjectorTolerances()
    matrix = np.asarray(projector)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("projector must be square")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("projector contains non-finite entries")
    dimension = matrix.shape[0]
    scale = max(float(np.linalg.norm(matrix, ord="fro")), float(np.finfo(float).eps))
    hermiticity = float(np.linalg.norm(matrix - matrix.conj().T, ord="fro") / scale)
    idempotency = float(np.linalg.norm(matrix @ matrix - matrix, ord="fro") / scale)
    hermitian_part = 0.5 * (matrix + matrix.conj().T)
    eigenvalues = scipy.linalg.eigvalsh(hermitian_part)
    binary_distance = np.minimum(np.abs(eigenvalues), np.abs(eigenvalues - 1.0))
    eigenvalue_binary_error = float(np.max(binary_distance))
    rank = int(np.count_nonzero(eigenvalues > 0.5))
    trace_value = float(np.trace(hermitian_part).real)
    trace_rank_error = abs(trace_value - rank)
    checks = {
        "hermiticity": hermiticity <= limits.hermiticity,
        "idempotency": idempotency <= limits.idempotency,
        "trace_matches_rank": trace_rank_error <= limits.trace_rank,
        "binary_eigenvalues": eigenvalue_binary_error <= limits.eigenvalue_binary,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "dimension": dimension,
        "rank": rank,
        "trace": trace_value,
        "metrics": {
            "hermiticity_relative_frobenius": hermiticity,
            "idempotency_relative_frobenius": idempotency,
            "trace_rank_abs_error": trace_rank_error,
            "max_binary_eigenvalue_error": eigenvalue_binary_error,
            "minimum_eigenvalue": float(eigenvalues[0]),
            "maximum_eigenvalue": float(eigenvalues[-1]),
        },
        "checks": checks,
        "failed_checks": failed,
        "tolerances": asdict(limits),
    }


def _range_basis(projector: np.ndarray, rank: int) -> np.ndarray:
    values, vectors = scipy.linalg.eigh(0.5 * (projector + projector.conj().T), driver="evr")
    if rank == 0:
        return np.empty((projector.shape[0], 0), dtype=projector.dtype)
    return vectors[:, -rank:]


def audit_projector_pair(
    reference: np.ndarray,
    candidate: np.ndarray,
    tolerances: ProjectorTolerances | None = None,
) -> dict[str, object]:
    """Audit two projectors and report rank and principal-angle diagnostics."""

    limits = tolerances or ProjectorTolerances()
    p = np.asarray(reference)
    q = np.asarray(candidate)
    if p.shape != q.shape:
        raise ValueError("reference and candidate projector shapes differ")
    reference_audit = audit_projector(p, limits)
    candidate_audit = audit_projector(q, limits)
    rank_p = int(reference_audit["rank"])
    rank_q = int(candidate_audit["rank"])
    min_rank = min(rank_p, rank_q)
    basis_p = _range_basis(p, rank_p)
    basis_q = _range_basis(q, rank_q)
    singular_values = (
        np.clip(scipy.linalg.svdvals(basis_p.conj().T @ basis_q), 0.0, 1.0)
        if min_rank > 0
        else np.empty(0)
    )
    principal_angles = np.arccos(singular_values)
    trace_overlap = float(np.trace(p @ q).real)
    chordal_distance = float(np.sqrt(max(0.0, min_rank - np.sum(np.square(singular_values)))))
    projector_operator_distance = float(np.linalg.norm(p - q, ord=2))
    rank_match = rank_p == rank_q
    checks = {
        "reference_projector": reference_audit["status"] == "PASS",
        "candidate_projector": candidate_audit["status"] == "PASS",
        "rank_match": rank_match,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "reference": reference_audit,
        "candidate": candidate_audit,
        "rank_reference": rank_p,
        "rank_candidate": rank_q,
        "singular_values": [float(value) for value in singular_values],
        "principal_angles_rad": [float(value) for value in principal_angles],
        "metrics": {
            "trace_overlap": trace_overlap,
            "chordal_distance": chordal_distance,
            "projector_operator_distance": projector_operator_distance,
            "maximum_principal_angle_rad": float(np.max(principal_angles)) if principal_angles.size else 0.0,
            "minimum_singular_value": float(np.min(singular_values)) if singular_values.size else 1.0,
        },
        "checks": checks,
        "failed_checks": failed,
    }
