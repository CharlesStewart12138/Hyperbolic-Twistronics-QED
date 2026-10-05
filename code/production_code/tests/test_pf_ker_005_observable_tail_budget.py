import math

from production_code.kernel.observable_tail_budget import (
    HODGE_C1_FACTOR,
    HODGE_C2_FACTOR,
    OBSERVABLE_CONTRACTS,
    canonical_tail,
    deterministic_reassessment_record,
    observable_closure_audit,
)


def test_exact_hodge_conversion_factors() -> None:
    assert math.isclose(HODGE_C1_FACTOR**2, math.sqrt(2.0) + 1.0, rel_tol=0.0, abs_tol=2e-15)
    assert math.isclose(HODGE_C2_FACTOR, math.sqrt(2.0) + 1.0, rel_tol=0.0, abs_tol=2e-15)


def test_selected_canonical_tail_values() -> None:
    row = canonical_tail(12)
    assert math.isclose(row.c0_per_abs_w, 3.510102293203841e-08, rel_tol=2e-15)
    assert math.isclose(row.c1_hodge_per_abs_w, 2.4560975865109666e-05, rel_tol=2e-15)
    assert math.isclose(row.c2_hodge_per_abs_w, 0.01720267257303223, rel_tol=2e-15)


def test_c0_c1_c2_observables_are_separate() -> None:
    required = {
        "energy_edge",
        "bandwidth",
        "spectral_gap",
        "riesz_projector",
        "generalized_velocity",
        "first_spectral_derivative",
        "spectral_hessian",
        "principal_curvature",
        "hodge_hessian_comparison",
    }
    assert set(OBSERVABLE_CONTRACTS) == required
    assert {entry["topology"] for entry in OBSERVABLE_CONTRACTS.values()} == {"C0", "C1", "C2"}


def test_empty_margin_registry_refuses_false_closure() -> None:
    audit = observable_closure_audit({})
    assert audit["all_observables_input_complete"] is False
    assert audit["may_close_pf_ker_005"] is False
    assert all(not row["input_complete"] for row in audit["observables"].values())


def test_reassessment_is_blocked_for_exact_missing_objects() -> None:
    record = deterministic_reassessment_record()
    assert record["production_cutoff_closes"] is False
    assert record["status"] == "Blocked"
    assert "isolation/contour margins" in record["blocked_reason"]

