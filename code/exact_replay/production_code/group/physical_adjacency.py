"""Physical nearest-neighbour adjacency from the exact geometric shell.

There is deliberately no generic ``S8`` selector. Physical Hamiltonians use
``S8_GEOMETRIC``; the standard presentation shell has a separately named
diagnostic function and cannot be selected by accident.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from production_code.group.quotient_candidate import FiniteQuotientCandidate
from production_code.group.shell_registry import S8_GEOMETRIC, S8_PRESENTATION
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.universal_cover import (
    GENERATOR_MATRICES,
    MatrixValue,
    matrix_multiply,
)


def universal_physical_neighbours(matrix: MatrixValue) -> tuple[MatrixValue, ...]:
    """Return the eight side-sharing universal-cover neighbours of a tile."""

    return tuple(matrix_multiply(matrix, generator) for generator in GENERATOR_MATRICES)


def quotient_physical_generator_images(candidate: FiniteQuotientCandidate) -> tuple[int, ...]:
    """Evaluate g0,...,g7 through their exact Nielsen words in a quotient."""

    return tuple(candidate.evaluate_word(GEOMETRIC_TO_STANDARD_WORD[index]) for index in range(8))


def quotient_physical_neighbours(candidate: FiniteQuotientCandidate, source: int) -> tuple[int, ...]:
    if not 0 <= source < candidate.order:
        raise ValueError("source is outside the quotient")
    return tuple(candidate.multiply(source, image)
                 for image in quotient_physical_generator_images(candidate))


def quotient_physical_adjacency_matrix(candidate: FiniteQuotientCandidate) -> tuple[tuple[int, ...], ...]:
    rows = []
    for source in range(candidate.order):
        counts = Counter(quotient_physical_neighbours(candidate, source))
        rows.append(tuple(counts.get(target, 0) for target in range(candidate.order)))
    return tuple(rows)


def presentation_adjacency_matrix_diagnostic(candidate: FiniteQuotientCandidate) -> tuple[tuple[int, ...], ...]:
    """Return the legacy algebraic-basis adjacency, never a physical default."""

    return candidate.adjacency_matrix


@dataclass(frozen=True)
class PhysicalAdjacencyCertificate:
    shell_name: str
    shell_order: tuple[str, ...]
    presentation_shell_distinct: bool
    inverse_closed: bool
    right_actions_are_permutations: bool
    weighted_degree_eight: bool
    simple_degree_eight: bool
    hermitian: bool
    phi8_shell_covariant: bool | None

    @property
    def passed(self) -> bool:
        mandatory: tuple[Any, ...] = (
            self.shell_name == "S8_GEOMETRIC",
            self.presentation_shell_distinct,
            self.inverse_closed,
            self.right_actions_are_permutations,
            self.weighted_degree_eight,
            self.simple_degree_eight,
            self.hermitian,
        )
        return all(mandatory) and self.phi8_shell_covariant is not False


def quotient_physical_adjacency_certificate(candidate: FiniteQuotientCandidate) -> PhysicalAdjacencyCertificate:
    images = quotient_physical_generator_images(candidate)
    matrix = quotient_physical_adjacency_matrix(candidate)
    inverse_closed = all(
        candidate.multiply(images[index], images[(index + 4) % 8]) == candidate.identity
        and candidate.multiply(images[(index + 4) % 8], images[index]) == candidate.identity
        for index in range(4)
    )
    right_permutations = all(
        set(candidate.multiply(source, image) for source in range(candidate.order))
        == set(range(candidate.order))
        for image in images
    )
    simple_degree = all(len(set(quotient_physical_neighbours(candidate, source))) == 8
                        for source in range(candidate.order))
    hermitian = all(matrix[left][right] == matrix[right][left]
                    for left in range(candidate.order) for right in range(candidate.order))
    covariance = None
    if candidate.phi8_permutation is not None:
        phi = candidate.phi8_permutation
        covariance = Counter(phi[image] for image in images) == Counter(images)
        if covariance:
            covariance = all(matrix[phi[left]][phi[right]] == matrix[left][right]
                             for left in range(candidate.order) for right in range(candidate.order))
    return PhysicalAdjacencyCertificate(
        shell_name="S8_GEOMETRIC",
        shell_order=S8_GEOMETRIC,
        presentation_shell_distinct=S8_GEOMETRIC != S8_PRESENTATION,
        inverse_closed=inverse_closed,
        right_actions_are_permutations=right_permutations,
        weighted_degree_eight=all(sum(row) == 8 for row in matrix),
        simple_degree_eight=simple_degree,
        hermitian=hermitian,
        phi8_shell_covariant=covariance,
    )
