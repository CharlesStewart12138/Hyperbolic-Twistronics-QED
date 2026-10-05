"""Exact tests for the lifted SL(2,25) x C2 semilinear family."""

import json
from pathlib import Path

from production_code.group.sl2_25_c8_family import IDENTITY, alpha_power, sl_elements


ROOT = Path(__file__).resolve().parents[2]


def test_sl_order_and_lifted_alpha_order() -> None:
    elements = sl_elements()
    assert len(elements) == 15600
    assert all(alpha_power(element, 8) == element for element in elements)
    assert all(any(alpha_power(element, divisor) != element for element in elements) for divisor in (1, 2, 4))


def test_lifted_family_certificate_rejects_all_orbits_exactly() -> None:
    path = ROOT / "production_code" / "group" / "SL2_25_C8_FAMILY_CERTIFICATE.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["classification"] == "PROOF_COMPLETE_LIFTED_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR"
    proof = record["proof_complete_parameterization"]
    assert proof["relation_inverse_shell_eight_direction_and_exact_B3_seeds"] == 128
    assert proof["kernel_equivalence_orbits"] == 16
    assert proof["orbit_sizes"] == [8] * 16
    witnesses = record["global_rejection"]["witnesses"]
    assert len(witnesses) == 16
    assert all(item["quotient_image"] == list(IDENTITY) for item in witnesses)
    assert all(item["dangerous_strictly_below_6a_B"] for item in witnesses)
    assert max(item["translation_length_over_a_B"] for item in witnesses) < 6.0

