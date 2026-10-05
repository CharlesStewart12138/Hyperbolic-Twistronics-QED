"""Spectral-estimation utilities for clean-room computations."""

from .stochastic_dos import (
    cdf_from_atoms,
    cdf_from_density,
    kpm_density,
    scale_hermitian,
    slq_quadrature,
)

__all__ = [
    "cdf_from_atoms",
    "cdf_from_density",
    "kpm_density",
    "scale_hermitian",
    "slq_quadrature",
]
