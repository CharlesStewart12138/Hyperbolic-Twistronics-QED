"""Exact word-metric kernel certificates for finite-cover candidates.

This module computes only the standard-primitive-S8_PRESENTATION word half-systole.  It is
not a based or global geometric injectivity radius.  Physical no-wraparound is
therefore left uncertified here and must be supplied by injectivity_bridge.py.
Graph diameter and group order are never substitutes for any radius.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from production_code.group.quotient_candidate import FiniteQuotientCandidate, INVERSE_TOKEN, S8_PRESENTATION
from production_code.group.surface_group import relation_residual


def freely_reduced_words(length: int) -> Iterator[tuple[str, ...]]:
    """Yield all freely reduced S8_PRESENTATION words of one length in fixed token order."""

    if length < 0:
        raise ValueError("word length must be nonnegative")
    if length == 0:
        yield ()
        return

    def extend(prefix: tuple[str, ...]) -> Iterator[tuple[str, ...]]:
        if len(prefix) == length:
            yield prefix
            return
        for token in S8_PRESENTATION:
            if prefix and token == INVERSE_TOKEN[prefix[-1]]:
                continue
            yield from extend(prefix + (token,))

    yield from extend(())


def word_injectivity_certificate(
    candidate: FiniteQuotientCandidate,
    *,
    maximum_word_length: int,
    active_cutoff_over_a: float,
) -> dict[str, Any]:
    """Search deterministically for the shortest quotient-only relation.

    A found witness at length ``ell`` certifies minimality because every
    freely reduced word of lengths 1 through ``ell-1`` was exhausted first.
    If no witness is found, the result is only a lower bound and is never
    reported as an exact systole.
    """

    if maximum_word_length < 1:
        raise ValueError("maximum_word_length must be positive")
    if active_cutoff_over_a <= 0:
        raise ValueError("active cutoff must be positive")

    examined_by_length: dict[str, int] = {}
    quotient_identity_by_length: dict[str, int] = {}
    surface_identity_excluded_by_length: dict[str, int] = {}
    witness: tuple[str, ...] | None = None
    witness_surface_residual: tuple[str, ...] | None = None

    for length in range(1, maximum_word_length + 1):
        examined = 0
        quotient_identity = 0
        surface_identity_excluded = 0
        for word in freely_reduced_words(length):
            examined += 1
            if candidate.evaluate_word(word) != candidate.identity:
                continue
            quotient_identity += 1
            residual = relation_residual(word)
            if not residual:
                surface_identity_excluded += 1
                continue
            witness = word
            witness_surface_residual = residual
            break
        examined_by_length[str(length)] = examined
        quotient_identity_by_length[str(length)] = quotient_identity
        surface_identity_excluded_by_length[str(length)] = surface_identity_excluded
        if witness is not None:
            break

    if witness is None:
        systole = None
        word_r_inj = None
        exhaustive_no_relation_through = maximum_word_length
        lower_bound = maximum_word_length / 2.0
        no_wraparound = lower_bound >= active_cutoff_over_a
        status = "LOWER_BOUND_ONLY"
        proof = (
            f"Every freely reduced S8_PRESENTATION word of lengths 1..{maximum_word_length} was enumerated; "
            "words equal to e in Gamma_B were excluded by deterministic Dehn reduction."
        )
    else:
        systole = len(witness)
        word_r_inj = systole / 2.0
        exhaustive_no_relation_through = systole - 1
        lower_bound = word_r_inj
        no_wraparound = word_r_inj > active_cutoff_over_a
        status = "EXACT_SHORTEST_RELATION_FOUND"
        proof = (
            f"Every freely reduced S8_PRESENTATION word of lengths 1..{systole - 1} was exhausted before "
            f"the displayed length-{systole} quotient-only relation; Dehn residual is nonempty."
        )

    return {
        "schema_version": 1,
        "quotient_id": candidate.quotient_id,
        "algorithm": "length-ordered exhaustive freely-reduced S8_PRESENTATION enumeration + exact quotient multiplication + Gamma_B Dehn reduction",
        "deterministic_token_order": list(S8_PRESENTATION),
        "maximum_word_length": maximum_word_length,
        "status": status,
        "shortest_quotient_only_relation_tokens": list(witness) if witness is not None else None,
        "shortest_quotient_only_relation": " ".join(witness) if witness is not None else None,
        "surface_group_residual_tokens": list(witness_surface_residual) if witness_surface_residual is not None else None,
        "systole_word_length": systole,
        "systole_convention": "shortest nontrivial kernel word in the active S8_PRESENTATION generator metric",
        "word_injectivity_radius": word_r_inj,
        "word_injectivity_convention": "r_inj = systole_word_length / 2",
        "word_injectivity_lower_bound": lower_bound,
        "exhaustive_no_relation_through_length": exhaustive_no_relation_through,
        "examined_by_length": examined_by_length,
        "quotient_identity_words_by_length": quotient_identity_by_length,
        "surface_identity_words_excluded_by_length": surface_identity_excluded_by_length,
        "minimality_proof": proof,
        "active_Dc_over_a": active_cutoff_over_a,
        "word_threshold_comparison_only": "r_inj_word > D_c/a",
        "word_threshold_pass": no_wraparound,
        "no_wraparound_requirement": "physical acceptance requires r_inj_global_geo/a > D_c/a",
        "no_wraparound_pass": False,
        "physical_no_wraparound_pass": None,
        "production_cutoff_status": "NOT_CERTIFIED_WORD_ONLY",
        "word_lower_bound_promoted_to_geometric": False,
        "graph_diameter_used": False,
        "group_order_used_as_radius": False,
    }
