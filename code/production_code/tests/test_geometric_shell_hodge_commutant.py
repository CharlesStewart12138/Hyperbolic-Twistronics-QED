from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from production_code.hodge.geometric_shell_commutant import (
    exact_certificate,
    geometric_covectors,
    hodge_metric,
    phi8_homology_matrix,
    physical_first_shell_tensor,
    tangent_c8_action,
)


ROOT = Path(__file__).resolve().parents[2]


def test_physical_covectors_cycle_and_tensor_is_invariant():
    p = phi8_homology_matrix()
    vectors = geometric_covectors()
    assert all(p * vectors[i] == vectors[(i + 1) % 8] for i in range(8))
    u = tangent_c8_action()
    c = physical_first_shell_tensor()
    assert sp.simplify(u.T * c * u - c) == sp.zeros(4)
    assert sp.simplify(u.T * hodge_metric() * u - hodge_metric()) == sp.zeros(4)


def test_non_scalar_commutant_falsifies_scalar_locking_exactly():
    checks = exact_certificate()
    assert checks["G_selfadjoint_commutant_dimension"] == 2
    assert checks["G_inverse_C_is_G_selfadjoint"] is True
    assert checks["G_inverse_C_commutes_with_C8"] is True
    assert checks["G_inverse_C_is_scalar"] is False
    assert checks["generalized_eigenvalues_C_relative_to_G"] == {"-1 + sqrt(2)": 2, "1 + sqrt(2)": 2}
    assert checks["scalar_commutant_hypothesis_passed"] is False


def test_frozen_record_forbids_scalar_q_and_requires_tensor_root():
    record = json.loads((ROOT / "production_code" / "hodge" / "GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.json").read_text(encoding="utf-8"))
    assert record["status"] == "Done_SCIENTIFIC_FALSIFICATION"
    assert record["consequence"]["single_scalar_q_infinity_authorized"] is False
    assert record["consequence"]["scalar_root_equation_authorized"] is False
    assert "2t*C_S-w*B_infinity=0" in record["consequence"]["required_full_kernel_form"]
    assert record["consequence"]["trace_root_sufficient"] is False
    assert record["main_tex_modified"] is False
