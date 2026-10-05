"""Parity descent and bipartiteness for the geometric physical shell."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.parity import certificate as universal_parity_certificate
from production_code.group.parity import parity
from production_code.group.physical_adjacency import quotient_physical_adjacency_matrix
from production_code.group.quotient_candidate import FiniteQuotientCandidate
from production_code.group.surface_group import RELATOR


def geometric_shell_parities() -> tuple[int, ...]:
    return tuple(parity(GEOMETRIC_TO_STANDARD_WORD[index]) for index in range(8))


def quotient_parity_labels(candidate: FiniteQuotientCandidate) -> tuple[int, ...] | None:
    """Return the descended parity on Q, or None if ker(q) is not in ker(pi)."""

    labels: list[int | None] = [None] * candidate.order
    labels[candidate.identity] = 0
    queue = deque([candidate.identity])
    while queue:
        source = queue.popleft()
        assert labels[source] is not None
        for generator in candidate.s8_images:
            target = candidate.multiply(source, generator)
            proposed = 1 - int(labels[source])
            if labels[target] is None:
                labels[target] = proposed
                queue.append(target)
            elif labels[target] != proposed:
                return None
    if any(value is None for value in labels):
        return None
    result = tuple(int(value) for value in labels)
    if not all(
        result[candidate.multiply(left, right)] == (result[left] + result[right]) % 2
        for left in range(candidate.order) for right in range(candidate.order)
    ):
        return None
    return result


def physical_graph_bipartite(candidate: FiniteQuotientCandidate) -> bool:
    labels = quotient_parity_labels(candidate)
    if labels is None:
        return False
    matrix = quotient_physical_adjacency_matrix(candidate)
    return all(
        multiplicity == 0 or labels[left] != labels[right]
        for left, row in enumerate(matrix)
        for right, multiplicity in enumerate(row)
    )


@dataclass(frozen=True)
class PhysicalParityCertificate:
    p01_relator_parity_zero: bool
    p02_homomorphism: bool
    p03_kernel_normal: bool
    p04_phi8_invariant: bool
    p05_all_geometric_generators_odd: bool
    p06_parity_factors_through_quotient: bool
    p07_physical_graph_bipartite: bool

    @property
    def passed(self) -> bool:
        return all(self.__dict__.values())


def certificate(candidate: FiniteQuotientCandidate) -> PhysicalParityCertificate:
    universal = universal_parity_certificate()
    labels = quotient_parity_labels(candidate)
    return PhysicalParityCertificate(
        p01_relator_parity_zero=parity(RELATOR) == 0 and universal.relator_in_kernel,
        p02_homomorphism=universal.homomorphism and universal.surjective,
        p03_kernel_normal=universal.kernel_normal,
        p04_phi8_invariant=universal.phi8_invariant,
        p05_all_geometric_generators_odd=geometric_shell_parities() == (1,) * 8,
        p06_parity_factors_through_quotient=labels is not None,
        p07_physical_graph_bipartite=physical_graph_bipartite(candidate),
    )
