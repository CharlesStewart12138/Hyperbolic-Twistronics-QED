"""Exact and stochastic spectral moment/trace audits."""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.sparse


def direct_normalized_moments(matrix: np.ndarray, max_order: int) -> np.ndarray:
    dense = np.asarray(matrix)
    if dense.ndim != 2 or dense.shape[0] != dense.shape[1]:
        raise ValueError("matrix must be square")
    if max_order < 1:
        raise ValueError("max_order must be positive")
    size = dense.shape[0]
    power = np.eye(size, dtype=dense.dtype)
    moments = [1.0]
    for _ in range(max_order):
        power = power @ dense
        moments.append(float(np.trace(power).real / size))
    return np.asarray(moments)


def eigenvalue_normalized_moments(matrix: np.ndarray, max_order: int) -> np.ndarray:
    values = scipy.linalg.eigvalsh(np.asarray(matrix), check_finite=True)
    return np.asarray([float(np.mean(np.power(values, order))) for order in range(max_order + 1)])


def stochastic_normalized_moments(
    matrix: np.ndarray | scipy.sparse.spmatrix,
    *,
    max_order: int,
    probe_count: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    sparse_matrix = scipy.sparse.csr_matrix(matrix)
    size = sparse_matrix.shape[0]
    if sparse_matrix.shape[1] != size:
        raise ValueError("matrix must be square")
    if max_order < 1 or probe_count < 2:
        raise ValueError("max_order must be positive and probe_count at least 2")
    complex_probe = np.iscomplexobj(sparse_matrix.data)
    samples = np.zeros((probe_count, max_order + 1), dtype=float)
    for probe_index in range(probe_count):
        if complex_probe:
            phases = rng.integers(0, 4, size=size)
            probe = np.choose(phases, [1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j, 0.0 - 1.0j])
        else:
            probe = 2.0 * rng.integers(0, 2, size=size).astype(float) - 1.0
        probe /= np.sqrt(size)
        current = probe.copy()
        samples[probe_index, 0] = float(np.vdot(probe, current).real)
        for order in range(1, max_order + 1):
            current = sparse_matrix @ current
            samples[probe_index, order] = float(np.vdot(probe, current).real)
    means = np.mean(samples, axis=0)
    standard_errors = np.std(samples, axis=0, ddof=1) / np.sqrt(probe_count)
    return means, standard_errors


def audit_moment_trace(
    matrix: np.ndarray | scipy.sparse.spmatrix,
    *,
    analytic_eigenvalues: np.ndarray,
    max_order: int,
    probe_count: int,
    rng: np.random.Generator,
    exact_tolerance: float,
    stochastic_sigma_multiplier: float,
    stochastic_absolute_floor: float,
) -> dict[str, object]:
    dense = matrix.toarray() if scipy.sparse.issparse(matrix) else np.asarray(matrix)
    analytic_values = np.asarray(analytic_eigenvalues)
    direct = direct_normalized_moments(dense, max_order)
    eigensolver = eigenvalue_normalized_moments(dense, max_order)
    analytic = np.asarray([
        float(np.mean(np.power(analytic_values, order))) for order in range(max_order + 1)
    ])
    stochastic, standard_errors = stochastic_normalized_moments(
        dense, max_order=max_order, probe_count=probe_count, rng=rng
    )
    second_moment_frobenius = float(np.linalg.norm(dense, ord="fro") ** 2 / dense.shape[0])
    records = []
    checks: dict[str, bool] = {}
    for order in range(max_order + 1):
        direct_error = abs(float(direct[order] - analytic[order]))
        eigensolver_error = abs(float(eigensolver[order] - analytic[order]))
        stochastic_error = abs(float(stochastic[order] - analytic[order]))
        stochastic_limit = max(
            stochastic_absolute_floor,
            stochastic_sigma_multiplier * float(standard_errors[order]),
        )
        checks[f"direct_order_{order}"] = bool(direct_error <= exact_tolerance)
        checks[f"eigensolver_order_{order}"] = bool(eigensolver_error <= exact_tolerance)
        checks[f"stochastic_order_{order}"] = bool(stochastic_error <= stochastic_limit)
        records.append({
            "order": order,
            "analytic": float(analytic[order]),
            "direct_trace": float(direct[order]),
            "eigensolver": float(eigensolver[order]),
            "stochastic": float(stochastic[order]),
            "stochastic_standard_error": float(standard_errors[order]),
            "direct_abs_error": direct_error,
            "eigensolver_abs_error": eigensolver_error,
            "stochastic_abs_error": stochastic_error,
            "stochastic_limit": stochastic_limit,
        })
    checks["second_moment_frobenius_identity"] = bool(abs(second_moment_frobenius - direct[2]) <= exact_tolerance)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "dimension": dense.shape[0],
        "max_order": max_order,
        "probe_count": probe_count,
        "second_moment_frobenius": second_moment_frobenius,
        "records": records,
        "checks": checks,
        "failed_checks": failed,
    }

