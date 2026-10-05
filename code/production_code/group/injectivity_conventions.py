"""Side-by-side injectivity conventions with fail-closed promotions."""

from __future__ import annotations

import math
from typing import Any

from production_code.group.injectivity import word_injectivity_certificate
from production_code.group.physical_adjacency import quotient_physical_generator_images
from production_code.group.quotient_candidate import FiniteQuotientCandidate
from production_code.group.universal_cover import (
    GEOMETRIC_TOKENS,
    enumerate_ball,
    exact_cosh_distance_over_R,
    field_to_complex,
)


def physical_geometric_word_injectivity(
    candidate: FiniteQuotientCandidate,
    maximum_geometric_length: int,
) -> dict[str, Any]:
    """Find the shortest nonidentity universal element killed by q in B_geo."""

    ball = enumerate_ball(maximum_geometric_length)
    images = quotient_physical_generator_images(candidate)
    witness = None
    for element in ball.elements[1:]:
        image = candidate.identity
        for token in element.representative:
            image = candidate.multiply(image, images[GEOMETRIC_TOKENS.index(token)])
        if image == candidate.identity:
            witness = element
            break

    if witness is None:
        return {
            "metric": "physical_geometric_generator_word_metric",
            "status": "LOWER_BOUND_ONLY",
            "shortest_kernel_word": None,
            "geometric_word_systole": None,
            "physical_geometric_word_radius": None,
            "lower_bound_strictly_greater_than": maximum_geometric_length / 2.0,
            "enumerated_through_length": maximum_geometric_length,
        }
    return {
        "metric": "physical_geometric_generator_word_metric",
        "status": "EXACT_SHORTEST_WORD_KERNEL_FOUND",
        "shortest_kernel_word": list(witness.representative),
        "geometric_word_systole": witness.word_length,
        "physical_geometric_word_radius": witness.word_length / 2.0,
        "lower_bound_strictly_greater_than": None,
        "enumerated_through_length": witness.word_length,
        "_matrix": witness.matrix,
    }


def hyperbolic_witness_upper_bounds(geometric_record: dict[str, Any]) -> dict[str, Any]:
    matrix = geometric_record.get("_matrix")
    if matrix is None:
        return {
            "based_hyperbolic_injectivity_over_a": None,
            "global_hyperbolic_injectivity_over_a": None,
            "based_witness_upper_bound_over_a": None,
            "global_witness_upper_bound_over_a": None,
            "status": "NOT_COMPUTED_NO_KERNEL_WITNESS",
        }
    spacing_over_R = 2.0 * math.acosh(1.0 + math.sqrt(2.0))
    cosh_based = max(1.0, field_to_complex(exact_cosh_distance_over_R(matrix)).real)
    based_displacement_over_a = math.acosh(cosh_based) / spacing_over_R
    half_trace = abs(field_to_complex(matrix[0]).real)
    translation_length_over_a = 2.0 * math.acosh(max(1.0, half_trace)) / spacing_over_R
    return {
        "based_hyperbolic_injectivity_over_a": None,
        "global_hyperbolic_injectivity_over_a": None,
        "based_witness_upper_bound_over_a": based_displacement_over_a / 2.0,
        "global_witness_upper_bound_over_a": translation_length_over_a / 2.0,
        "status": "WITNESS_UPPER_BOUNDS_ONLY_KERNEL_MINIMA_NOT_COMPUTED",
    }


def side_by_side_report(
    candidate: FiniteQuotientCandidate,
    *,
    maximum_presentation_length: int,
    maximum_geometric_length: int,
    active_cutoff_over_a: float = 3.0,
) -> dict[str, Any]:
    presentation = word_injectivity_certificate(
        candidate,
        maximum_word_length=maximum_presentation_length,
        active_cutoff_over_a=active_cutoff_over_a,
    )
    geometric = physical_geometric_word_injectivity(candidate, maximum_geometric_length)
    hyperbolic = hyperbolic_witness_upper_bounds(geometric)
    geometric.pop("_matrix", None)
    return {
        "schema_version": "1.0",
        "quotient_id": candidate.quotient_id,
        "standard_presentation_word": {
            "metric": "S8_PRESENTATION",
            "radius": presentation["word_injectivity_radius"],
            "lower_bound": presentation["word_injectivity_lower_bound"],
            "status": presentation["status"],
            "witness": presentation["shortest_quotient_only_relation_tokens"],
        },
        "physical_geometric_word": geometric,
        "hyperbolic_geometric": hyperbolic,
        "active_Dc_over_a": active_cutoff_over_a,
        "option_B_acceptance_cutoffs": {"based_geometric_word_length": 127, "global_geometric_word_length": 156},
        "word_metrics_interchangeable": False,
        "word_radius_promoted_to_hyperbolic_radius": False,
        "graph_diameter_used_as_radius": False,
        "group_order_used_as_radius": False,
    }
