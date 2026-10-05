"""Validated eigensolver utilities for clean-room computations."""

from .dense_sparse_crosscheck import CrosscheckTolerances, crosscheck_hermitian

__all__ = ["CrosscheckTolerances", "crosscheck_hermitian"]
