"""Exact full-dimensional Euclidean moire Bloch Hamiltonian.

MANUSCRIPT SOURCE:
Equations: Eqs. (425)–(461), including the site/folded unitary equivalence.
Section: Euclidean tight-binding Hamiltonian.
Model scope: complete 2*Sigma microscopic basis; paths are not used for extrema.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, isfinite, pi, sqrt
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from production_code.euclidean.csl import SquareCSL
from production_code.euclidean.interlayer import translation_vector_over_a
from production_code.euclidean.sites import layer_sites


BlockMap = Mapping[tuple[int, int], ArrayLike]


@dataclass(frozen=True)
class BlochResult:
    h_layer_1: NDArray[np.complex128]
    h_layer_2: NDArray[np.complex128]
    interlayer: NDArray[np.complex128]
    hamiltonian: NDArray[np.complex128]
    hermiticity_relative_residual: float


@dataclass(frozen=True)
class FoldedResult:
    unitary: NDArray[np.complex128]
    hamiltonian: NDArray[np.complex128]
    unitarity_residual: float
    spectral_residual: float


def _k_vector(k_over_inverse_a: ArrayLike) -> NDArray[np.float64]:
    k = np.asarray(k_over_inverse_a, dtype=float)
    if k.shape != (2,) or np.any(~np.isfinite(k)):
        raise ValueError("k must be a finite Cartesian vector with shape (2,)")
    return k


def _coerce_block(block: ArrayLike, sigma: int) -> NDArray[np.complex128]:
    matrix = np.asarray(block, dtype=complex)
    if matrix.shape != (sigma, sigma) or np.any(~np.isfinite(matrix)):
        raise ValueError(f"every real-space block must have finite shape ({sigma},{sigma})")
    return matrix


def fourier_block(cell: SquareCSL, blocks: BlockMap, k_over_inverse_a: ArrayLike) -> NDArray[np.complex128]:
    """Evaluate sum_R block(R) exp(i k.R) in the site basis."""

    k = _k_vector(k_over_inverse_a)
    result = np.zeros((cell.sigma, cell.sigma), dtype=complex)
    for translation, raw_block in blocks.items():
        vector = translation_vector_over_a(cell, translation)
        phase = np.exp(1j*(k[0]*float(vector[0])+k[1]*float(vector[1])))
        result += _coerce_block(raw_block, cell.sigma)*phase
    return result


def nearest_neighbor_intralayer_blocks(cell: SquareCSL, layer: int, hopping_over_t: float = -1.0) -> dict[tuple[int, int], NDArray[np.float64]]:
    """Construct exact square-nearest-neighbor h_ss'(R)/t coefficient blocks."""

    hopping = float(hopping_over_t)
    if not isfinite(hopping):
        raise ValueError("hopping_over_t must be finite")
    sites = layer_sites(cell, layer)
    maximum_offset = max(
        sqrt(float((right.coordinate_over_a[0]-left.coordinate_over_a[0])**2+(right.coordinate_over_a[1]-left.coordinate_over_a[1])**2))
        for left in sites
        for right in sites
    )
    bound = ceil((maximum_offset+1.0)/sqrt(cell.sigma))+1
    blocks: dict[tuple[int, int], NDArray[np.float64]] = {}
    for u in range(-bound, bound+1):
        for v in range(-bound, bound+1):
            translation = translation_vector_over_a(cell, (u, v))
            block = np.zeros((cell.sigma, cell.sigma), dtype=float)
            for source, left in enumerate(sites):
                for target, right in enumerate(sites):
                    dx = right.coordinate_over_a[0]+translation[0]-left.coordinate_over_a[0]
                    dy = right.coordinate_over_a[1]+translation[1]-left.coordinate_over_a[1]
                    if dx*dx+dy*dy == 1:
                        block[source, target] = hopping
            if np.any(block):
                blocks[(u, v)] = block
    return dict(sorted(blocks.items()))


def bloch_hamiltonian(
    cell: SquareCSL,
    *,
    k_over_inverse_a: ArrayLike,
    layer_1_blocks: BlockMap,
    layer_2_blocks: BlockMap,
    interlayer_blocks_over_w: BlockMap,
    omega0_over_t: float = 0.0,
    w_over_t: float = 1.0,
) -> BlochResult:
    """Build the exact 2*Sigma Bloch matrix in the layer-resolved site basis."""

    omega0 = float(omega0_over_t)
    coupling = float(w_over_t)
    if not isfinite(omega0) or not isfinite(coupling):
        raise ValueError("omega0/t and w/t must be finite")
    h1 = fourier_block(cell, layer_1_blocks, k_over_inverse_a)
    h2 = fourier_block(cell, layer_2_blocks, k_over_inverse_a)
    interlayer = coupling*fourier_block(cell, interlayer_blocks_over_w, k_over_inverse_a)
    upper = np.concatenate((h1, interlayer), axis=1)
    lower = np.concatenate((interlayer.conjugate().T, h2), axis=1)
    matrix = np.concatenate((upper, lower), axis=0)+omega0*np.eye(2*cell.sigma, dtype=complex)
    scale = max(1.0, float(np.linalg.norm(matrix, ord=2)))
    residual = float(np.linalg.norm(matrix-matrix.conjugate().T, ord=2)/scale)
    return BlochResult(h1, h2, interlayer, matrix, residual)


def folding_vectors_over_inverse_a(cell: SquareCSL, layer: int) -> NDArray[np.float64]:
    """Return the Sigma cyclic reciprocal-quotient representatives Q_j."""

    if layer not in {1, 2}:
        raise ValueError("layer must be 1 or 2")
    generator = (2.0*pi/cell.sigma)*np.array([cell.p, cell.q], dtype=float)
    if layer == 2:
        rotation = np.array([[float(cell.cos_theta), -float(cell.sin_theta)], [float(cell.sin_theta), float(cell.cos_theta)]])
        generator = rotation@generator
    return np.arange(cell.sigma, dtype=float)[:, None]*generator[None, :]


def folding_unitary(cell: SquareCSL, layer: int, k_over_inverse_a: ArrayLike) -> NDArray[np.complex128]:
    """Evaluate U_l(k) from quotient-character representatives."""

    k = _k_vector(k_over_inverse_a)
    sites = layer_sites(cell, layer)
    coordinates = np.array([[float(site.coordinate_over_a[0]), float(site.coordinate_over_a[1])] for site in sites])
    momenta = k[None, :]+folding_vectors_over_inverse_a(cell, layer)
    return np.exp(1j*coordinates@momenta.T)/sqrt(cell.sigma)


def folded_hamiltonian(cell: SquareCSL, site_hamiltonian: ArrayLike, k_over_inverse_a: ArrayLike) -> FoldedResult:
    """Transform H_M(k) to the explicit layer-block quotient-character basis."""

    matrix = np.asarray(site_hamiltonian, dtype=complex)
    if matrix.shape != (2*cell.sigma, 2*cell.sigma) or np.any(~np.isfinite(matrix)):
        raise ValueError("site_hamiltonian must be a finite 2*Sigma square matrix")
    u1 = folding_unitary(cell, 1, k_over_inverse_a)
    u2 = folding_unitary(cell, 2, k_over_inverse_a)
    zero = np.zeros_like(u1)
    unitary = np.block([[u1, zero], [zero, u2]])
    identity = np.eye(2*cell.sigma)
    unitarity = float(np.linalg.norm(unitary.conjugate().T@unitary-identity, ord=2))
    transformed = unitary.conjugate().T@matrix@unitary
    site_spectrum = np.linalg.eigvalsh(matrix)
    folded_spectrum = np.linalg.eigvalsh(transformed)
    spectral = float(np.max(np.abs(site_spectrum-folded_spectrum)))
    return FoldedResult(unitary, transformed, unitarity, spectral)
