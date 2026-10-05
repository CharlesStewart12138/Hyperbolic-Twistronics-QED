"""Option-B word cutoffs for Bolza based/global geometric certification."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class BolzaPackingBound:
    lattice_spacing_over_R: float
    inradius_over_R: float
    circumradius_over_R: float
    tube_radius_over_R: float
    cutoff_Dc_over_a: float
    based_displacement_cutoff_over_R: float
    based_packing_ratio: float
    based_word_cutoff: int
    global_conjugate_displacement_cutoff_over_R: float
    global_packing_ratio: float
    global_word_cutoff: int


def hyperbolic_ball_area_over_R2(radius_over_R: float) -> float:
    return 2.0 * math.pi * (math.cosh(radius_over_R) - 1.0)


def hyperbolic_tube_area_over_R2(length_over_R: float, radius_over_R: float) -> float:
    """Area of the closed radius-r stadium around a geodesic segment."""

    return (
        2.0 * length_over_R * math.sinh(radius_over_R)
        + 2.0 * math.pi * (math.cosh(radius_over_R) - 1.0)
    )


def word_cutoff_for_based_displacement(displacement_over_R: float) -> tuple[float, int]:
    root2 = math.sqrt(2.0)
    spacing = 2.0 * math.acosh(1.0 + root2)
    inradius = spacing / 2.0
    circumradius = math.acosh((1.0 + root2) ** 2)
    tube_radius = circumradius + inradius
    ratio = (
        hyperbolic_tube_area_over_R2(displacement_over_R, tube_radius)
        / hyperbolic_ball_area_over_R2(inradius)
    )
    # At most floor(ratio) crossed tiles; a side-adjacent tile chain with N
    # vertices has at most N-1 generator steps.
    return ratio, math.floor(ratio) - 1


def production_cutoff_bound(cutoff_Dc_over_a: float = 3.0) -> BolzaPackingBound:
    cutoff = float(cutoff_Dc_over_a)
    if cutoff <= 0:
        raise ValueError("cutoff_Dc_over_a must be positive")
    root2 = math.sqrt(2.0)
    spacing = 2.0 * math.acosh(1.0 + root2)
    inradius = spacing / 2.0
    circumradius = math.acosh((1.0 + root2) ** 2)
    tube_radius = circumradius + inradius

    based_displacement = 2.0 * cutoff * spacing
    based_ratio, based_word_cutoff = word_cutoff_for_based_displacement(based_displacement)

    # If a normal kernel contains gamma with translation length <=2Dc,
    # conjugate its axis to meet the fundamental octagon.  The conjugate is
    # still in the kernel and moves the origin by at most ell+2*r_out.
    global_displacement = based_displacement + 2.0 * circumradius
    global_ratio, global_word_cutoff = word_cutoff_for_based_displacement(global_displacement)
    return BolzaPackingBound(
        lattice_spacing_over_R=spacing,
        inradius_over_R=inradius,
        circumradius_over_R=circumradius,
        tube_radius_over_R=tube_radius,
        cutoff_Dc_over_a=cutoff,
        based_displacement_cutoff_over_R=based_displacement,
        based_packing_ratio=based_ratio,
        based_word_cutoff=based_word_cutoff,
        global_conjugate_displacement_cutoff_over_R=global_displacement,
        global_packing_ratio=global_ratio,
        global_word_cutoff=global_word_cutoff,
    )


def geometric_acceptance_search_contract(cutoff_Dc_over_a: float = 3.0) -> dict[str, object]:
    bound = production_cutoff_bound(cutoff_Dc_over_a)
    return {
        "based": {
            "theorem": "d_H(0,gamma*0)<=2Dc implies |gamma|_Sgeo<=L_cert_based",
            "L_cert_based": bound.based_word_cutoff,
        },
        "global": {
            "theorem": "if normal K contains ell(gamma)<=2Dc, K contains a conjugate with |.|_Sgeo<=L_cert_global",
            "L_cert_global": bound.global_word_cutoff,
        },
        "enumeration_required_for_based_acceptance": bound.based_word_cutoff,
        "enumeration_required_for_global_acceptance": bound.global_word_cutoff,
        "current_universal_cover_radius": 6,
        "current_radius_sufficient_for_acceptance": False,
    }

