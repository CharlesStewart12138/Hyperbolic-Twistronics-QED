"""Exact regular-octagon/Bolza constants and neighbour isometries.

MANUSCRIPT SOURCE:
Equation: Eqs. (46)–(60).
Section: Genus-two regular-octagon/Bolza-surface lattice.
Model scope: exact {8,8} centre-orbit geometry.
"""

from __future__ import annotations

from cmath import exp
from dataclasses import dataclass
from math import acosh, pi, sqrt

from production_code.geometry.hyperbolic import distance


@dataclass(frozen=True)
class BolzaConstants:
    R: float
    area: float
    inradius: float
    lattice_spacing: float
    kappa_B: float
    circumradius: float
    vertex_disk_radius: float
    translation_eta: float


def constants(R: float) -> BolzaConstants:
    """Evaluate Eqs. (46)–(54) without fitted geometry constants."""

    radius = float(R)
    if radius <= 0.0:
        raise ValueError("R must be strictly positive")
    ac = acosh(1.0 + sqrt(2.0))
    spacing = 2.0 * radius * ac
    return BolzaConstants(
        R=radius,
        area=4.0 * pi * radius**2,
        inradius=radius * ac,
        lattice_spacing=spacing,
        kappa_B=spacing / radius,
        circumradius=radius * acosh((1.0 + sqrt(2.0)) ** 2),
        vertex_disk_radius=2.0 ** (-0.25),
        translation_eta=sqrt(2.0 * (sqrt(2.0) - 1.0)),
    )


def vertices() -> tuple[complex, ...]:
    """Return z_nu=2^-1/4 exp[i(2nu+1)pi/8], nu=0,...,7."""

    rho = 2.0 ** (-0.25)
    return tuple(rho * exp(1j * (2 * nu + 1) * pi / 8.0) for nu in range(8))


def centered_rotation(z: complex, phi: float) -> complex:
    return exp(1j * float(phi)) * complex(z)


def basic_translation(z: complex) -> complex:
    """Apply tau_eta(z)=(z+eta)/(eta*z+1), Eq. (55)."""

    eta = constants(1.0).translation_eta
    point = complex(z)
    return (point + eta) / (eta * point + 1.0)


def neighbour_map(nu: int, z: complex) -> complex:
    """Apply s_nu=r_{nu*pi/4} o tau_eta o r_{-nu*pi/4}, Eq. (57)."""

    index = int(nu)
    if index != nu or not 0 <= index < 8:
        raise ValueError("nu must be an integer from 0 through 7")
    phi = index * pi / 4.0
    return centered_rotation(basic_translation(centered_rotation(z, -phi)), phi)


def neighbour_centres(R: float) -> tuple[complex, ...]:
    """Return the eight nearest centre-orbit points s_nu(0)."""

    result = tuple(neighbour_map(nu, 0j) for nu in range(8))
    spacing = constants(R).lattice_spacing
    if not all(abs(distance(0j, point, R) - spacing) <= 2e-14 * max(1.0, spacing) for point in result):
        raise ArithmeticError("Bolza neighbour maps failed the exact spacing identity")
    return result

