"""Mathematically valid real-space bilayer restrictions for arbitrary twist."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt

import numpy as np
import scipy.sparse as sp

from geometry import OrbitPatch, pairwise_hyperbolic_distance_over_a, rotate
from multiorbital_hamiltonian import FrozenOrbitalModel


OMEGA_REF_OVER_T = 140.36861265335298


@dataclass(frozen=True)
class ScalarBilayerParameters:
    theta: float
    omega_over_omega_ref: float = 1.0
    lambda_perp_over_a: float = 0.20
    h_over_a: float = 0.50
    cutoff_over_a: float = 3.0
    intralayer_hopping_over_t: float = 1.0

    @property
    def w_over_t(self) -> float:
        return self.omega_over_omega_ref * OMEGA_REF_OVER_T

    def metadata(self) -> dict[str, float]:
        row = asdict(self)
        row["w_over_t"] = self.w_over_t
        return row

    def validate(self) -> None:
        values = tuple(float(v) for v in asdict(self).values())
        if not all(np.isfinite(values)):
            raise ValueError("all model parameters must be finite")
        if self.lambda_perp_over_a <= 0 or self.h_over_a < 0:
            raise ValueError("require lambda_perp/a>0 and h/a>=0")
        if self.cutoff_over_a < self.h_over_a:
            raise ValueError("physical cutoff must exceed vertical separation")
        if self.omega_over_omega_ref < 0:
            raise ValueError("hybridization must be nonnegative")


@dataclass(frozen=True)
class LocalBilayer:
    patch: OrbitPatch
    parameters: ScalarBilayerParameters
    interlayer: sp.csr_matrix
    hamiltonian: sp.csr_matrix
    boundary_semantics: str = "exact universal-cover Dirichlet restriction; no periodic identifications"

    @property
    def sites_per_layer(self) -> int:
        return self.patch.size

    @property
    def dimension(self) -> int:
        return 2 * self.patch.size


def interlayer_matrix(patch: OrbitPatch, parameters: ScalarBilayerParameters) -> sp.csr_matrix:
    parameters.validate()
    lower = patch.coordinates
    upper = rotate(patch.coordinates, parameters.theta)
    planar = pairwise_hyperbolic_distance_over_a(lower, upper)
    physical = np.sqrt(parameters.h_over_a**2 + planar**2)
    mask = physical <= parameters.cutoff_over_a + 64 * np.finfo(float).eps
    values = parameters.w_over_t * np.exp(-(physical - parameters.h_over_a) / parameters.lambda_perp_over_a)
    values[~mask] = 0.0
    result = sp.csr_matrix(values)
    result.eliminate_zeros()
    return result


def build_local_bilayer(patch: OrbitPatch, parameters: ScalarBilayerParameters) -> LocalBilayer:
    FrozenOrbitalModel().validate()
    coupling = interlayer_matrix(patch, parameters)
    intra = (-parameters.intralayer_hopping_over_t * patch.adjacency).tocsr()
    hamiltonian = sp.bmat([[intra, coupling], [coupling.T.conjugate(), intra]], format="csr")
    defect = hamiltonian - hamiltonian.T.conjugate()
    if defect.nnz and np.max(np.abs(defect.data)) > 1e-12:
        raise ArithmeticError("local bilayer Hamiltonian is not Hermitian")
    return LocalBilayer(patch, parameters, coupling, hamiltonian)


def assert_generic_not_periodic(theta_class: str, periodic_requested: bool) -> None:
    if theta_class == "Theta_G" and periodic_requested:
        raise ValueError("R5 forbids exact finite periodicization at generic twist")


def schur_row_sum_bound(patch: OrbitPatch, parameters: ScalarBilayerParameters) -> float:
    coupling = interlayer_matrix(patch, parameters)
    intra = abs(parameters.intralayer_hopping_over_t) * np.asarray(patch.adjacency.sum(axis=1)).ravel()
    cross = np.asarray(abs(coupling).sum(axis=1)).ravel()
    return float(np.max(intra + cross))

