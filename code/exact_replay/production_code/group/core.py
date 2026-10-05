"""Practical parity/C8 core of a finite quotient kernel."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from production_code.group.automorphism import phi8, phi8_power
from production_code.group.parity import parity
from production_code.group.quotient_candidate import FiniteQuotientCandidate
from production_code.group.surface_group import free_reduce, inverse_word


@dataclass(frozen=True)
class CoreSignature:
    parity_image: int
    rotated_quotient_images: tuple[int, ...]


def core_signature(candidate: FiniteQuotientCandidate, word: Sequence[str]) -> CoreSignature:
    """Evaluate the diagonal map with kernel N_core.

    If N=ker(q), then x lies in phi8^j(N) exactly when
    q(phi8^(-j)(x)) is the finite-group identity.
    """

    reduced = free_reduce(word)
    return CoreSignature(
        parity_image=parity(reduced),
        rotated_quotient_images=tuple(
            candidate.evaluate_word(phi8_power(reduced, -power)) for power in range(8)
        ),
    )


def in_core(candidate: FiniteQuotientCandidate, word: Sequence[str]) -> bool:
    signature = core_signature(candidate, word)
    return signature.parity_image == 0 and all(
        image == candidate.identity for image in signature.rotated_quotient_images
    )


def multiply_signatures(
    candidate: FiniteQuotientCandidate,
    left: CoreSignature,
    right: CoreSignature,
) -> CoreSignature:
    return CoreSignature(
        parity_image=(left.parity_image + right.parity_image) % 2,
        rotated_quotient_images=tuple(
            candidate.multiply(a, b)
            for a, b in zip(left.rotated_quotient_images, right.rotated_quotient_images)
        ),
    )


def conjugate(conjugator: Sequence[str], word: Sequence[str]) -> tuple[str, ...]:
    return free_reduce(tuple(conjugator) + tuple(word) + inverse_word(conjugator))


def core_index_upper_bound(candidate: FiniteQuotientCandidate) -> int:
    """Return the diagonal-target bound 2*|Q|^8, never an exact order claim."""

    return 2 * candidate.order**8


def cumulative_core_membership(
    candidates: Sequence[FiniteQuotientCandidate], word: Sequence[str]
) -> bool:
    """Membership in the cumulative intersection of practical cores."""

    return all(in_core(candidate, word) for candidate in candidates)


def core_contract(candidate: FiniteQuotientCandidate) -> dict[str, object]:
    return {
        "base_quotient_id": candidate.quotient_id,
        "definition": "ker(pi) intersect intersection_{j=0}^7 phi8^j(ker(q))",
        "normal": True,
        "parity_inclusion": True,
        "c8_invariant": True,
        "finite_index": True,
        "finite_index_upper_bound": core_index_upper_bound(candidate),
        "finite_index_upper_bound_is_exact_order": False,
        "nested_core_construction": "cumulative intersections preserve nesting and residuality",
    }

