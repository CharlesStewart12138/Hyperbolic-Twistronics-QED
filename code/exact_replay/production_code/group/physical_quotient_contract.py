"""Repaired Q09/Q11/Q12 contract on the geometric physical shell."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from production_code.group.automorphism import phi8
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.physical_adjacency import (
    quotient_physical_adjacency_matrix,
    quotient_physical_generator_images,
)
from production_code.group.quotient_candidate import (
    FiniteQuotientCandidate,
    POSITIVE_GENERATORS,
)
from production_code.group.universal_cover import GEOMETRIC_TOKENS, enumerate_ball


@dataclass(frozen=True)
class GeometricBallInjectivity:
    radius: int
    universal_ball_size: int
    image_size: int
    injective: bool
    collision_element_ids: tuple[int, int] | None


def q09_phi8_descends(candidate: FiniteQuotientCandidate) -> bool:
    """Check that the proposed finite map is the descent of the exact phi8."""

    phi = candidate.phi8_permutation
    if phi is None or set(phi) != set(range(candidate.order)) or phi[candidate.identity] != candidate.identity:
        return False
    if not all(
        phi[candidate.multiply(left, right)] == candidate.multiply(phi[left], phi[right])
        for left in range(candidate.order)
        for right in range(candidate.order)
    ):
        return False
    return all(
        phi[candidate.evaluate_word((token,))] == candidate.evaluate_word(phi8((token,)))
        for token in POSITIVE_GENERATORS
    )


def q11_geometric_shell_covariance(candidate: FiniteQuotientCandidate) -> bool:
    """Check phi8 covariance of q(g0),...,q(g7), including adjacency."""

    if not q09_phi8_descends(candidate):
        return False
    assert candidate.phi8_permutation is not None
    phi = candidate.phi8_permutation
    images = quotient_physical_generator_images(candidate)
    cyclic = all(phi[images[index]] == images[(index + 1) % 8] for index in range(8))
    if not cyclic or Counter(phi[image] for image in images) != Counter(images):
        return False
    matrix = quotient_physical_adjacency_matrix(candidate)
    return all(matrix[phi[left]][phi[right]] == matrix[left][right]
               for left in range(candidate.order) for right in range(candidate.order))


def q12_geometric_ball_injectivity(
    candidate: FiniteQuotientCandidate,
    radius: int = 3,
) -> GeometricBallInjectivity:
    """Audit injectivity on the exact universal geometric ball B(e,radius)."""

    ball = enumerate_ball(radius)
    generator_images = quotient_physical_generator_images(candidate)
    seen: dict[int, int] = {}
    collision = None
    for element in ball.elements:
        image = candidate.identity
        for token in element.representative:
            image = candidate.multiply(image, generator_images[GEOMETRIC_TOKENS.index(token)])
        prior = seen.get(image)
        if prior is not None and collision is None:
            collision = (prior, element.element_id)
        seen.setdefault(image, element.element_id)
    return GeometricBallInjectivity(
        radius=radius,
        universal_ball_size=len(ball.elements),
        image_size=len(seen),
        injective=collision is None and len(seen) == len(ball.elements),
        collision_element_ids=collision,
    )


def diagnostic_q11_presentation_shell_covariance(candidate: FiniteQuotientCandidate) -> bool:
    """Historical standard-presentation Q11, explicitly nonphysical."""

    if not q09_phi8_descends(candidate):
        return False
    assert candidate.phi8_permutation is not None
    return Counter(candidate.phi8_permutation[image] for image in candidate.s8_images) == Counter(candidate.s8_images)


def geometric_shell_words() -> tuple[tuple[str, ...], ...]:
    return tuple(GEOMETRIC_TO_STANDARD_WORD[index] for index in range(8))
