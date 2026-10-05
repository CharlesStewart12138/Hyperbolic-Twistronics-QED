"""Independent exact tests for the PSL(2,25) x C2 semilinear family."""

import json
from pathlib import Path

from production_code.group.psl2_25_c8_family import (
    IDENTITY,
    alpha_power,
    determinant,
    frobenius,
    inv,
    is_square,
    mul,
    psl_elements,
)
from production_code.group.psl2_25_c8_orbits import alpha_centralizer, pgl_elements


ROOT = Path(__file__).resolve().parents[2]


def test_f25_is_a_field_and_frobenius_is_exact() -> None:
    assert all(mul(value, inv(value)) == 1 for value in range(1, 25))
    assert all(frobenius(frobenius(value)) == value for value in range(25))
    assert sum(is_square(value) for value in range(25)) == 12


def test_projective_group_orders_and_semilinear_order() -> None:
    psl = psl_elements()
    assert len(psl) == 7800
    assert len(pgl_elements()) == 15600
    assert all(is_square(determinant(matrix)) for matrix in psl)
    assert all(alpha_power(matrix, 8) == matrix for matrix in psl)
    assert all(any(alpha_power(matrix, divisor) != matrix for matrix in psl) for divisor in (1, 2, 4))
    assert len(alpha_centralizer()) == 8


def test_certificate_exhausts_and_rejects_all_six_kernel_orbits() -> None:
    path = ROOT / "production_code" / "group" / "PSL2_25_C8_FAMILY_CERTIFICATE.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["classification"] == "PROOF_COMPLETE_SEMILINEAR_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR"
    proof = record["proof_complete_parameterization"]
    assert proof["relation_inverse_shell_eight_direction_and_exact_B3_seeds"] == 48
    assert proof["kernel_equivalence_orbits"] == 6
    assert proof["orbit_sizes"] == [8] * 6
    witnesses = record["global_rejection"]["witnesses"]
    assert len(witnesses) == 6
    assert all(item["quotient_image"] == list(IDENTITY) for item in witnesses)
    assert all(item["dangerous_strictly_below_6a_B"] for item in witnesses)
    assert max(item["translation_length_over_a_B"] for item in witnesses) < 6.0

