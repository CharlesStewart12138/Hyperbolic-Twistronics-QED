"""Option-B finite word-cutoff theorem regression tests."""

import unittest

from production_code.group.geometric_cutoff_bound import (
    geometric_acceptance_search_contract,
    production_cutoff_bound,
)


class GeometricCutoffBoundTests(unittest.TestCase):
    def test_bound_01_bolza_packing_constants(self):
        bound = production_cutoff_bound(3.0)
        self.assertAlmostEqual(bound.inradius_over_R * 2, bound.lattice_spacing_over_R, places=14)
        self.assertGreater(bound.tube_radius_over_R, bound.circumradius_over_R)

    def test_bound_02_based_displacement_option_b_cutoff(self):
        bound = production_cutoff_bound(3.0)
        self.assertGreater(bound.based_packing_ratio, 128.0)
        self.assertLess(bound.based_packing_ratio, 129.0)
        self.assertEqual(bound.based_word_cutoff, 127)

    def test_bound_03_global_normal_kernel_cutoff(self):
        bound = production_cutoff_bound(3.0)
        self.assertGreater(bound.global_packing_ratio, 157.0)
        self.assertLess(bound.global_packing_ratio, 158.0)
        self.assertEqual(bound.global_word_cutoff, 156)

    def test_bound_04_radius_six_is_not_promoted_to_acceptance(self):
        contract = geometric_acceptance_search_contract(3.0)
        self.assertEqual(contract["enumeration_required_for_based_acceptance"], 127)
        self.assertEqual(contract["enumeration_required_for_global_acceptance"], 156)
        self.assertFalse(contract["current_radius_sufficient_for_acceptance"])


if __name__ == "__main__":
    unittest.main()

