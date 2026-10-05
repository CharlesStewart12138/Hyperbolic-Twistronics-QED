"""Repaired physical-shell Q09/Q11/Q12 tests."""

from dataclasses import replace
import unittest

from production_code.group.physical_quotient_contract import (
    diagnostic_q11_presentation_shell_covariance,
    q09_phi8_descends,
    q11_geometric_shell_covariance,
    q12_geometric_ball_injectivity,
)
from production_code.group.quotient_candidate import abelian_validation_candidate
from production_code.group.quotient_contract_no_go import certificate as historical_no_go


def exact_abelian_phi8(candidate):
    modulus = round(candidate.order ** 0.25)
    coordinates = [tuple(int(value) for value in label.split(",")) for label in candidate.element_labels]
    index = {value: position for position, value in enumerate(coordinates)}
    phi = []
    for x, y, z, w in coordinates:
        image = (
            y % modulus,
            (-x + y - z) % modulus,
            (-y - z + w) % modulus,
            (-z) % modulus,
        )
        phi.append(index[image])
    return replace(candidate, quotient_id=candidate.quotient_id + "_EXACT_PHI8", phi8_permutation=tuple(phi))


class PhysicalQuotientContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = exact_abelian_phi8(abelian_validation_candidate(4))

    def test_q09_revised_exact_descent(self):
        self.assertTrue(q09_phi8_descends(self.candidate))
        self.assertFalse(q09_phi8_descends(abelian_validation_candidate(4)))

    def test_q11_revised_geometric_covariance(self):
        self.assertTrue(q11_geometric_shell_covariance(self.candidate))
        self.assertFalse(diagnostic_q11_presentation_shell_covariance(self.candidate))

    def test_q12_revised_exact_geometric_b3(self):
        result = q12_geometric_ball_injectivity(self.candidate, 3)
        self.assertEqual(result.universal_ball_size, 457)
        self.assertFalse(result.injective)
        self.assertIsNotNone(result.collision_element_ids)

    def test_old_standard_shell_no_go_is_retained(self):
        self.assertTrue(historical_no_go().contradiction)


if __name__ == "__main__":
    unittest.main()
