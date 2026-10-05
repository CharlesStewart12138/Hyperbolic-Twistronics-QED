"""Sparse local resolvent observables."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu


def resolvent_columns(hamiltonian: sp.spmatrix, energy: float, eta: float, sources: list[int]) -> np.ndarray:
    if eta <= 0:
        raise ValueError("eta must be positive")
    matrix = ((complex(energy, eta)) * sp.eye(hamiltonian.shape[0], format="csc") - hamiltonian.astype(complex).tocsc())
    factor = splu(matrix)
    rhs = np.zeros((hamiltonian.shape[0], len(sources)), dtype=complex)
    rhs[np.asarray(sources, dtype=int), np.arange(len(sources))] = 1.0
    return factor.solve(rhs)


def green_entries(hamiltonian: sp.spmatrix, energy: float, eta: float, pairs: list[tuple[int, int]]) -> np.ndarray:
    sources = sorted({source for _, source in pairs})
    columns = resolvent_columns(hamiltonian, energy, eta, sources)
    column_for = {source: index for index, source in enumerate(sources)}
    return np.asarray([columns[target, column_for[source]] for target, source in pairs])

