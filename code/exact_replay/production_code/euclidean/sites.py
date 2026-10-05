"""Exact layer-resolved basis for one square CSL supercell.

MANUSCRIPT SOURCE:
Equation: Eqs. (421)–(424).
Section: Euclidean tight-binding Hamiltonian.
Model scope: Sigma microscopic site classes per layer; layer labels never merged.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite

from production_code.euclidean.csl import SquareCSL


@dataclass(frozen=True, order=True)
class LayerSite:
    layer: int
    site_index: int
    quotient_class: int
    coordinate_over_a: tuple[Fraction, Fraction]

    def coordinate(self, a: float) -> tuple[float, float]:
        spacing = float(a)
        if not isfinite(spacing) or spacing <= 0.0:
            raise ValueError("a must be finite and strictly positive")
        return spacing*float(self.coordinate_over_a[0]), spacing*float(self.coordinate_over_a[1])


def layer_sites(cell: SquareCSL, layer: int) -> tuple[LayerSite, ...]:
    """Return the Sigma algebraic representatives for one layer."""

    if layer not in {1, 2}:
        raise ValueError("layer must be 1 or 2")
    result: list[LayerSite] = []
    for class_index, _ in enumerate(cell.representatives):
        if layer == 1:
            coordinate = (Fraction(class_index), Fraction(0))
        else:
            coordinate = (class_index*cell.cos_theta, class_index*cell.sin_theta)
        result.append(LayerSite(layer, class_index+1, class_index, coordinate))
    if len(result) != cell.sigma:
        raise ArithmeticError("layer basis cardinality differs from Sigma")
    return tuple(result)


def bilayer_basis(cell: SquareCSL) -> tuple[LayerSite, ...]:
    """Return the ordered 2*Sigma basis (layer 1 first, layer 2 second)."""

    basis = layer_sites(cell, 1) + layer_sites(cell, 2)
    if len(basis) != cell.n_sc or len(set((site.layer, site.quotient_class) for site in basis)) != cell.n_sc:
        raise ArithmeticError("layer-resolved bilayer basis failed the exact count")
    return basis

