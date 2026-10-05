"""Machine contract for the theorem-level characteristic residual tower."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CharacteristicTowerLevel:
    maximum_target_order: int
    normal: bool
    finite_index: bool
    nested_in_previous: bool
    characteristic: bool
    automorphism_invariant: bool
    parity_compatible: bool
    explicit_enumerated_level: bool


def theorem_level(maximum_target_order: int) -> CharacteristicTowerLevel:
    """Return the logical theorem contract for K_M, not an enumerated group."""

    bound = int(maximum_target_order)
    if bound != maximum_target_order or bound < 1:
        raise ValueError("maximum_target_order must be a positive integer")
    return CharacteristicTowerLevel(
        maximum_target_order=bound,
        normal=True,
        finite_index=True,
        nested_in_previous=bound > 1,
        characteristic=True,
        automorphism_invariant=True,
        parity_compatible=bound >= 2,
        explicit_enumerated_level=False,
    )


def homomorphism_count_upper_bound(target_orders: tuple[int, ...], generator_rank: int = 4) -> int:
    """Finite upper bound before relation filtering, sum_F |F|^rank."""

    if generator_rank < 1 or any(order < 1 for order in target_orders):
        raise ValueError("rank and target orders must be positive")
    return sum(order**generator_rank for order in target_orders)


def residual_separation_level(finite_witness_group_order: int) -> int:
    """The first guaranteed M containing a supplied residual-finiteness witness."""

    order = int(finite_witness_group_order)
    if order != finite_witness_group_order or order < 1:
        raise ValueError("finite witness order must be a positive integer")
    return order

