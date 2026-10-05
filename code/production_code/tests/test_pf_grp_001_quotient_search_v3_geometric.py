"""Focused tests for the expanded S5/S6 geometric-shell search."""

from production_code.group.quotient_search_v3_geometric import (
    _commutator,
    _generates_full_symmetric,
    audit_single,
    symmetric_group_data,
)


def test_exact_s5_and_s6_tables() -> None:
    assert len(symmetric_group_data(5).elements) == 120
    assert len(symmetric_group_data(6).elements) == 720


def test_reversal_pair_satisfies_surface_relation() -> None:
    data = symmetric_group_data(5)
    a = data.index[(1, 2, 3, 4, 0)]
    b = data.index[(1, 0, 2, 3, 4)]
    assert _generates_full_symmetric(data, (a, b))
    assert data.table[_commutator(data, a, b)][_commutator(data, b, a)] == data.identity


def test_single_v3_candidate_uses_physical_covariance() -> None:
    data = symmetric_group_data(5)
    a = data.index[(1, 2, 3, 4, 0)]
    b = data.index[(1, 0, 2, 3, 4)]
    record, _ = audit_single({"degree": 5, "family": "TEST", "images": (a, b, b, a)}, 1)
    assert record["gates"]["surface_relation"] is True
    assert record["gates"]["phi8_descent"] is True
    assert record["gates"]["physical_covariance"] is True
    assert record["option_B_127_156_certified"] is False
