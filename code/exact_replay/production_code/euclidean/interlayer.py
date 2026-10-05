"""Full radial Euclidean supercell interlayer translation blocks.

MANUSCRIPT SOURCE:
Equations: Eqs. (421)–(429), especially T_ss'(R) and the exponential profile.
Section: Euclidean tight-binding Hamiltonian.
Model scope: all microscopic layer pairs and all moire translations inside D_c.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import ceil, hypot, isfinite, sqrt

import numpy as np
from numpy.typing import NDArray

from production_code.euclidean.csl import SquareCSL
from production_code.euclidean.sites import layer_sites
from production_code.kernel.radial import evaluate


@dataclass(frozen=True)
class InterlayerTerm:
    """One matrix element T_ss'(R), normalized by the vertical hopping w."""

    source_index: int
    target_index: int
    translation: tuple[int, int]
    translation_over_a: tuple[Fraction, Fraction]
    planar_displacement_over_a: tuple[Fraction, Fraction]
    distance_over_a: float
    amplitude_over_w: float


def translation_vector_over_a(cell: SquareCSL, translation: tuple[int, int]) -> tuple[Fraction, Fraction]:
    """Map integer moire coordinates (u,v) to u*T1+v*T2 in units of a."""

    u, v = translation
    if isinstance(u, bool) or isinstance(v, bool) or not isinstance(u, int) or not isinstance(v, int):
        raise TypeError("moire translation coordinates must be integers")
    rows = cell.direct_basis_over_a
    return rows[0][0]*u + rows[0][1]*v, rows[1][0]*u + rows[1][1]*v


def _parameters(h_over_a: float, lambda_perp_over_a: float, cutoff_over_a: float) -> tuple[float, float, float]:
    h = float(h_over_a)
    decay = float(lambda_perp_over_a)
    cutoff = float(cutoff_over_a)
    if not all(isfinite(value) for value in (h, decay, cutoff)):
        raise ValueError("h/a, lambda_perp/a and D_c/a must be finite")
    if h < 0.0 or decay <= 0.0 or cutoff < h:
        raise ValueError("require h/a>=0, lambda_perp/a>0 and D_c/a>=h/a")
    return h, decay, cutoff


def _translation_index_bound(cell: SquareCSL, planar_cutoff: float) -> int:
    first = layer_sites(cell, 1)
    second = layer_sites(cell, 2)
    maximum_offset = max(
        hypot(float(site2.coordinate_over_a[0]-site1.coordinate_over_a[0]), float(site2.coordinate_over_a[1]-site1.coordinate_over_a[1]))
        for site1 in first
        for site2 in second
    )
    # The orthogonal CSL vectors have length sqrt(Sigma)*a.  If a term can
    # survive, ||R|| <= ||r2-r1|| + planar_cutoff by the triangle inequality.
    return ceil((maximum_offset+planar_cutoff)/sqrt(cell.sigma))+1


def interlayer_terms(
    cell: SquareCSL,
    *,
    h_over_a: float,
    lambda_perp_over_a: float,
    cutoff_over_a: float,
) -> tuple[InterlayerTerm, ...]:
    """Enumerate every T_ss'(R)/w whose full three-dimensional distance is <=D_c.

    The cutoff is only an enumeration cutoff.  A full-kernel claim additionally
    requires the separately certified omitted-tail bound mandated by the model.
    """

    h, decay, cutoff = _parameters(h_over_a, lambda_perp_over_a, cutoff_over_a)
    planar_cutoff = sqrt(max(0.0, cutoff*cutoff-h*h))
    bound = _translation_index_bound(cell, planar_cutoff)
    first = layer_sites(cell, 1)
    second = layer_sites(cell, 2)
    result: list[InterlayerTerm] = []
    cutoff_squared = cutoff*cutoff
    for u in range(-bound, bound+1):
        for v in range(-bound, bound+1):
            translation = translation_vector_over_a(cell, (u, v))
            for source, site1 in enumerate(first):
                for target, site2 in enumerate(second):
                    displacement = (
                        site2.coordinate_over_a[0]+translation[0]-site1.coordinate_over_a[0],
                        site2.coordinate_over_a[1]+translation[1]-site1.coordinate_over_a[1],
                    )
                    planar_squared = float(displacement[0]*displacement[0]+displacement[1]*displacement[1])
                    distance_squared = h*h+planar_squared
                    if distance_squared > cutoff_squared+32.0*np.finfo(float).eps*max(1.0, cutoff_squared):
                        continue
                    distance = sqrt(distance_squared)
                    result.append(
                        InterlayerTerm(
                            source_index=source,
                            target_index=target,
                            translation=(u, v),
                            translation_over_a=translation,
                            planar_displacement_over_a=displacement,
                            distance_over_a=distance,
                            amplitude_over_w=float(evaluate(distance, 1.0, h, decay).value),
                        )
                    )
    result.sort(key=lambda term: (term.translation, term.source_index, term.target_index))
    return tuple(result)


def interlayer_translation_blocks(
    cell: SquareCSL,
    *,
    h_over_a: float,
    lambda_perp_over_a: float,
    cutoff_over_a: float,
) -> dict[tuple[int, int], NDArray[np.float64]]:
    """Return dense Sigma-by-Sigma coefficient blocks T(R)/w by translation."""

    blocks: dict[tuple[int, int], NDArray[np.float64]] = {}
    for term in interlayer_terms(
        cell,
        h_over_a=h_over_a,
        lambda_perp_over_a=lambda_perp_over_a,
        cutoff_over_a=cutoff_over_a,
    ):
        block = blocks.setdefault(term.translation, np.zeros((cell.sigma, cell.sigma), dtype=float))
        block[term.source_index, term.target_index] = term.amplitude_over_w
    return dict(sorted(blocks.items()))
