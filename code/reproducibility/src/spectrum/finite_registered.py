"""Load and solve a registered sparse finite Hamiltonian without DOS."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import scipy.linalg
import scipy.sparse

from reproducibility.src.solvers.dense_sparse_crosscheck import CrosscheckTolerances, crosscheck_hermitian
from reproducibility.src.spectrum.projector_audit import audit_projector_pair


def load_coo_csv(path: Path, *, dimension: int) -> scipy.sparse.csr_matrix:
    rows: list[int] = []
    columns: list[int] = []
    values: list[float] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            rows.append(int(record["row"]))
            columns.append(int(record["column"]))
            values.append(float(record["value_over_t"]))
    return scipy.sparse.coo_matrix((values, (rows, columns)), shape=(dimension, dimension)).tocsr()


def solve_registered_root(matrix: scipy.sparse.csr_matrix, *, w_star_over_t: float) -> tuple[list[dict[str, object]], dict[str, object]]:
    dense = matrix.toarray()
    values, vectors = scipy.linalg.eigh(dense, driver="evr", check_finite=True)
    target_mask = np.abs(values - w_star_over_t) <= 2.0e-9
    target_indices = np.flatnonzero(target_mask)
    if target_indices.size == 0:
        raise RuntimeError("registered root target island was not found")
    target_vectors = vectors[:, target_indices]
    numerical_projector = target_vectors @ target_vectors.T
    single_dimension = dense.shape[0] // 2
    identity = np.eye(single_dimension)
    exact_projector = 0.5 * np.block([[identity, identity], [identity, identity]])
    projector_audit = audit_projector_pair(exact_projector, numerical_projector)
    complement = values[~target_mask]
    target_values = values[target_mask]
    target_lower = float(np.min(target_values))
    target_upper = float(np.max(target_values))
    complement_below = complement[complement < target_lower]
    lower_gap = target_lower - float(np.max(complement_below)) if complement_below.size else float("inf")

    limits = CrosscheckTolerances(
        hermiticity=1.0e-13,
        eigenvalue=2.0e-9,
        dense_residual=1.0e-12,
        sparse_residual=1.0e-9,
        orthogonality=1.0e-8,
    )
    # Cross-check the extremal eigenpair itself.  Requesting several vectors from
    # ARPACK is not a multiplicity audit when an edge eigenspace is more highly
    # degenerate than k; it may legitimately return vectors from adjacent clusters.
    low_crosscheck = crosscheck_hermitian(matrix, k=1, edge="lowest", tolerances=limits)
    high_crosscheck = crosscheck_hermitian(matrix, k=1, edge="highest", tolerances=limits)
    low_crosscheck["audit_scope"] = "EXTREMAL_EIGENPAIR_NOT_MULTIPLICITY"
    high_crosscheck["audit_scope"] = "EXTREMAL_EIGENPAIR_NOT_MULTIPLICITY"
    spectrum_rows = [
        {
            "eigenvalue_index": index,
            "energy_over_t": float(value),
            "target_island": bool(target_mask[index]),
            "solver": "scipy.linalg.eigh(driver=evr)",
        }
        for index, value in enumerate(values)
    ]
    checks = {
        "target_rank": target_indices.size == single_dimension,
        "projector": projector_audit["status"] == "PASS" and projector_audit["metrics"]["projector_operator_distance"] <= 1.0e-10,
        "target_bandwidth": target_upper - target_lower <= 2.0e-9,
        "positive_lower_gap": lower_gap > 0.0,
        "dense_sparse_low": low_crosscheck["status"] == "PASS",
        "dense_sparse_high": high_crosscheck["status"] == "PASS",
    }
    return spectrum_rows, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "dimension": dense.shape[0],
        "target_rank": int(target_indices.size),
        "target_lower_edge_over_t": target_lower,
        "target_upper_edge_over_t": target_upper,
        "target_bandwidth_over_t": target_upper - target_lower,
        "lower_isolation_gap_over_t": lower_gap,
        "projector_audit": projector_audit,
        "dense_sparse_low": low_crosscheck,
        "dense_sparse_high": high_crosscheck,
        "checks": checks,
        "dos_computed": False,
    }
