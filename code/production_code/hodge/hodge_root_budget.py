"""Executable form of the independent Hodge-root enclosure theorem.

This module implements the strict inequalities in the frozen manuscript.  It
does not invent the missing angle interval, scalar Hodge sum, tail errors, or
slope margin for PF-HOD-004.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Mapping


REQUIRED_CURRENT_INPUTS = (
    "theta_minus",
    "theta_plus",
    "K",
    "t",
    "w",
    "c_S",
    "g_tilde_left",
    "g_tilde_right",
    "m_b_tilde",
    "epsilon_b0",
    "epsilon_b1",
    "epsilon_c",
    "root_residual",
)


@dataclass(frozen=True)
class HodgeRootCertificate:
    epsilon_g: float
    certified_b_slope: float
    certified_principal_value_slope: float
    endpoint_sign_change: bool
    endpoint_margin: float
    endpoint_margin_passed: bool
    root_radius: float
    certified: bool


def certify_hodge_root(
    *,
    w: float,
    c_s: float,
    g_tilde_left: float,
    g_tilde_right: float,
    m_b_tilde: float,
    epsilon_b0: float,
    epsilon_b1: float,
    epsilon_c: float,
    root_residual: float,
) -> HodgeRootCertificate:
    """Evaluate the exact scalar-commutant Hodge-root acceptance contract."""

    values = (
        w,
        c_s,
        g_tilde_left,
        g_tilde_right,
        m_b_tilde,
        epsilon_b0,
        epsilon_b1,
        epsilon_c,
        root_residual,
    )
    if not all(math.isfinite(float(value)) for value in values):
        raise ValueError("all Hodge-root inputs must be finite")
    if w <= 0.0 or c_s <= 0.0 or m_b_tilde < 0.0:
        raise ValueError("require w>0, c_S>0 and m_b_tilde>=0")
    if min(epsilon_b0, epsilon_b1, epsilon_c, root_residual) < 0.0:
        raise ValueError("error budgets and residual must be nonnegative")

    epsilon_g = epsilon_b0 + epsilon_c
    certified_b_slope = m_b_tilde - epsilon_b1
    endpoint_sign_change = g_tilde_left * g_tilde_right < 0.0
    endpoint_margin = min(abs(g_tilde_left), abs(g_tilde_right)) - epsilon_g
    endpoint_margin_passed = endpoint_margin > 0.0
    certified = certified_b_slope > 0.0 and endpoint_sign_change and endpoint_margin_passed
    root_radius = (
        (root_residual + epsilon_g) / certified_b_slope if certified else math.inf
    )
    principal_slope = w * c_s * certified_b_slope
    return HodgeRootCertificate(
        epsilon_g=epsilon_g,
        certified_b_slope=certified_b_slope,
        certified_principal_value_slope=principal_slope,
        endpoint_sign_change=endpoint_sign_change,
        endpoint_margin=endpoint_margin,
        endpoint_margin_passed=endpoint_margin_passed,
        root_radius=root_radius,
        certified=certified,
    )


def input_audit(values: Mapping[str, float | int | None]) -> dict[str, object]:
    missing = tuple(key for key in REQUIRED_CURRENT_INPUTS if values.get(key) is None)
    return {
        "required_inputs": REQUIRED_CURRENT_INPUTS,
        "missing_inputs": missing,
        "input_complete": not missing,
        "may_evaluate_strict_contract": not missing,
    }


def deterministic_reassessment_record() -> dict[str, object]:
    audit = input_audit({})
    return {
        "task_id": "PF-HOD-004",
        "scope": "LOCAL_SCALAR_CHARACTER",
        "available": {
            "harmonic_basis": "PF-HOD-001-LOCAL-2026-09-05",
            "canonical_metric": "PF-HOD-002-LOCAL-2026-09-05",
            "canonical_kernel_tail_conversion": True,
            "root_contract_implemented": True,
        },
        "input_audit": audit,
        "status": "Blocked",
        "blocked_dependencies": ("PF-KER-005",),
        "blocked_reason": (
            "No registered same-scope angle interval and scalar b_tilde(theta,K) data supply "
            "signed endpoint values, epsilon_b0, an angle-derivative epsilon_b1, or a positive "
            "certified slope m_b_tilde-epsilon_b1.  The existing character-coordinate C1 tail "
            "cannot be promoted to an angle derivative without a frozen angle-path transport."
        ),
    }

