"""Fail-closed implementation of the proved R5 trichotomy.

This module does not pretend to construct the impossible generic same-Q
operator.  It implements the theorem-level domain gate, the exact frozen-grid
classification, deterministic reduction of a certified finite branch table,
and common-cover dimension bookkeeping.  Exact geometric branch enumeration
is delegated to the certified Dirichlet-flood input required by Theorem
R5-COMM; no heuristic word cutoff is accepted.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from math import gcd
from typing import Iterable, Mapping, Sequence


FROZEN_Q_ORDER = 46_080
FROZEN_A1_DIMENSION = 92_160


class TwistClass(str, Enum):
    NORMALIZER = "NORMALIZER"
    COMMENSURATOR_NOT_NORMALIZER = "COMMENSURATOR_NOT_NORMALIZER"
    GENERIC_NONCOMMENSURATOR = "GENERIC_NONCOMMENSURATOR"


class R5DomainError(RuntimeError):
    """Raised when a requested operator lies outside its proved domain."""


@dataclass(frozen=True)
class BranchDistance:
    branch_id: str
    distance: Decimal

    def __post_init__(self) -> None:
        if self.distance < 0:
            raise ValueError("distance must be nonnegative")
        if not self.branch_id:
            raise ValueError("branch_id must be nonempty")


@dataclass(frozen=True)
class SupportEntry:
    row: int
    column: int
    in_plane_distance: Decimal
    coefficient: Decimal
    minimizing_branch_ids: tuple[str, ...]


def euler_phi(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    result = n
    p = 2
    value = n
    while p * p <= value:
        if value % p == 0:
            while value % p == 0:
                value //= p
            result -= result // p
        p += 1
    if value > 1:
        result -= result // value
    return result


def classify_frozen_grid_index(j: int) -> dict[str, int | str]:
    """Classify theta_j=j*pi/720 using the proved trace-field obstruction."""
    if not 0 <= j <= 90:
        raise ValueError("frozen grid index must lie in 0..90")
    if j == 0:
        return {
            "index": 0,
            "class": TwistClass.NORMALIZER.value,
            "root_of_unity_order": 1,
            "real_cyclotomic_degree": 1,
        }
    order = 1440 // gcd(j, 1440)
    degree = euler_phi(order) // 2
    if degree <= 2:
        raise AssertionError("R5 trace-field exclusion unexpectedly failed")
    return {
        "index": j,
        "class": TwistClass.GENERIC_NONCOMMENSURATOR.value,
        "root_of_unity_order": order,
        "real_cyclotomic_degree": degree,
    }


def common_cover_dimensions(
    correspondence_degree: int,
    *,
    normal_core_index_over_intersection: int = 1,
) -> dict[str, int]:
    if correspondence_degree < 1 or normal_core_index_over_intersection < 1:
        raise ValueError("indices must be positive")
    layer_sites = (
        FROZEN_Q_ORDER
        * correspondence_degree
        * normal_core_index_over_intersection
    )
    return {
        "intersection_index_m": correspondence_degree,
        "normal_core_index_over_intersection": normal_core_index_over_intersection,
        "layer_sites": layer_sites,
        "bilayer_dimension": 2 * layer_sites,
    }


def generic_infimum() -> Decimal:
    """The proved infimum; it is not an attained frozen minimum in general."""
    return Decimal(0)


def _decimal_exp(value: Decimal) -> Decimal:
    return value.exp()


def GLOBAL_INTERLAYER_SUPPORT_R5(
    *,
    twist_class: TwistClass,
    certified_branch_distances: Mapping[tuple[int, int], Sequence[BranchDistance]],
    h: Decimal,
    cutoff: Decimal,
    amplitude: Decimal,
    decay_length: Decimal,
) -> tuple[SupportEntry, ...]:
    """Reduce a complete certified finite branch table to frozen coefficients.

    Completeness of the branch table must be certified by the geometric flood
    from R5_FINITE_ALGORITHM.tex.  Generic inputs are rejected because no such
    finite table can represent the frozen minimum.
    """
    if twist_class is TwistClass.GENERIC_NONCOMMENSURATOR:
        raise R5DomainError(
            "generic double coset is dense: frozen minimum is generally absent"
        )
    if h <= 0 or cutoff < h or decay_length <= 0:
        raise ValueError("require h>0, cutoff>=h, decay_length>0")

    output: list[SupportEntry] = []
    for (row, column), branches in sorted(certified_branch_distances.items()):
        if row < 0 or column < 0 or not branches:
            raise ValueError("pair indices must be nonnegative and branches nonempty")
        minimum = min(branch.distance for branch in branches)
        minimizers = tuple(
            sorted(branch.branch_id for branch in branches if branch.distance == minimum)
        )
        product_distance = (h * h + minimum * minimum).sqrt()
        if product_distance <= cutoff:  # exact closed-boundary convention
            coefficient = amplitude * _decimal_exp(
                -(product_distance - h) / decay_length
            )
            output.append(
                SupportEntry(
                    row=row,
                    column=column,
                    in_plane_distance=minimum,
                    coefficient=coefficient,
                    minimizing_branch_ids=minimizers,
                )
            )
    return tuple(output)


def hermitian_inverse_support(entries: Iterable[SupportEntry]) -> tuple[SupportEntry, ...]:
    """Return the adjoint block entries, preserving real radial coefficients."""
    return tuple(
        SupportEntry(
            row=e.column,
            column=e.row,
            in_plane_distance=e.in_plane_distance,
            coefficient=e.coefficient,
            minimizing_branch_ids=e.minimizing_branch_ids,
        )
        for e in entries
    )


def GLOBAL_OPERATOR_R5(
    *,
    twist_class: TwistClass,
    support: Sequence[SupportEntry],
    correspondence_degree: int = 1,
) -> dict[str, object]:
    """Return exact operator metadata without allocating a 92160 square matrix."""
    if twist_class is TwistClass.GENERIC_NONCOMMENSURATOR:
        raise R5DomainError("GLOBAL_OPERATOR_R5 is impossible on generic twists")
    if twist_class is TwistClass.NORMALIZER:
        if correspondence_degree != 1:
            raise ValueError("normalizer same-Q level must have degree one")
        dimension = FROZEN_A1_DIMENSION
        same_q = True
        status = "SAME_Q_THEOREM_DOMAIN"
    else:
        if correspondence_degree <= 1:
            raise ValueError("non-normalizer correspondence degree must exceed one")
        dimension = FROZEN_A1_DIMENSION * correspondence_degree
        same_q = False
        status = "COMMON_COVER_ONLY"
    return {
        "status": status,
        "same_q": same_q,
        "bilayer_dimension": dimension,
        "interlayer_nnz_one_direction": len(support),
        "hermitian_completion": "offdiagonal block plus exact adjoint",
    }


def check_covariance(
    coefficients: Mapping[tuple[int, int], Decimal],
    layer1_permutation: Sequence[int],
    layer2_permutation: Sequence[int],
) -> bool:
    if len(layer1_permutation) != len(layer2_permutation):
        return False
    for (i, j), value in coefficients.items():
        if coefficients.get((layer1_permutation[i], layer2_permutation[j])) != value:
            return False
    return True
