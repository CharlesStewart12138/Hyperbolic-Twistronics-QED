import math

from production_code.hodge.hodge_root_budget import (
    REQUIRED_CURRENT_INPUTS,
    certify_hodge_root,
    deterministic_reassessment_record,
    input_audit,
)


def test_strict_contract_certifies_synthetic_root() -> None:
    cert = certify_hodge_root(
        w=2.0,
        c_s=3.0,
        g_tilde_left=-0.4,
        g_tilde_right=0.5,
        m_b_tilde=1.2,
        epsilon_b0=0.02,
        epsilon_b1=0.1,
        epsilon_c=0.01,
        root_residual=0.003,
    )
    assert cert.certified
    assert math.isclose(cert.certified_b_slope, 1.1)
    assert math.isclose(cert.certified_principal_value_slope, 6.6)
    assert math.isclose(cert.root_radius, 0.033 / 1.1)


def test_nonpositive_certified_slope_refuses_root_radius() -> None:
    cert = certify_hodge_root(
        w=1.0,
        c_s=1.0,
        g_tilde_left=-1.0,
        g_tilde_right=1.0,
        m_b_tilde=0.1,
        epsilon_b0=0.0,
        epsilon_b1=0.1,
        epsilon_c=0.0,
        root_residual=0.0,
    )
    assert not cert.certified
    assert math.isinf(cert.root_radius)


def test_endpoint_margin_is_strict() -> None:
    cert = certify_hodge_root(
        w=1.0,
        c_s=1.0,
        g_tilde_left=-0.1,
        g_tilde_right=0.2,
        m_b_tilde=1.0,
        epsilon_b0=0.1,
        epsilon_b1=0.0,
        epsilon_c=0.0,
        root_residual=0.0,
    )
    assert cert.endpoint_sign_change
    assert not cert.endpoint_margin_passed
    assert not cert.certified


def test_current_input_audit_is_exact_and_incomplete() -> None:
    audit = input_audit({})
    assert audit["missing_inputs"] == REQUIRED_CURRENT_INPUTS
    assert audit["may_evaluate_strict_contract"] is False


def test_reassessment_retains_real_blocker() -> None:
    record = deterministic_reassessment_record()
    assert record["status"] == "Blocked"
    assert record["blocked_dependencies"] == ("PF-KER-005",)
    assert "angle-path transport" in record["blocked_reason"]

