"""INJ-01 through INJ-03 acceptance tests."""

import unittest

from production_code.group.injectivity import word_injectivity_certificate
from production_code.group.injectivity_bridge import (
    finite_radius_bounds,
    separated_injectivity_record,
    witness_geometry,
)
from production_code.group.quotient_candidate import abelian_validation_candidate


class InjectivityBridgeTests(unittest.TestCase):
    def test_inj_01_known_word_injectivity_fixture(self):
        certificate = word_injectivity_certificate(
            abelian_validation_candidate(4), maximum_word_length=6, active_cutoff_over_a=3.0
        )
        self.assertEqual(certificate["systole_word_length"], 4)
        self.assertEqual(certificate["word_injectivity_radius"], 2.0)
        self.assertEqual(certificate["shortest_quotient_only_relation_tokens"],
                         ["a1", "a1", "a1", "a1"])

    def test_inj_02_known_axis_geometry_fixture(self):
        geometry = witness_geometry(("a1", "a1", "a1", "a1"))
        self.assertAlmostEqual(geometry.based_displacement_over_a, 4.0, places=12)
        self.assertAlmostEqual(geometry.translation_length_over_a, 4.0, places=12)
        self.assertAlmostEqual(geometry.based_injectivity_upper_bound_over_a, 2.0, places=12)
        self.assertAlmostEqual(geometry.global_injectivity_upper_bound_over_a, 2.0, places=12)
        bounds = finite_radius_bounds(6)
        self.assertEqual(len(bounds), 6)
        self.assertTrue(all(row["minimum_translation_length_over_a"] <= 1.0 + 1e-12
                            for row in bounds))

    def test_inj_03_serialization_never_conflates_three_radii(self):
        record = separated_injectivity_record(
            quotient_id="QVAL_Z4_POWER4_N256",
            word_injectivity_radius=2.0,
            standard_kernel_witness=("a1", "a1", "a1", "a1"),
        )
        self.assertEqual(record["r_inj_word"], 2.0)
        self.assertIsNone(record["r_inj_based_geo_over_a"])
        self.assertIsNone(record["r_inj_global_geo_over_a"])
        self.assertFalse(record["physical_no_wraparound_pass"])
        self.assertEqual(record["physical_status"], "REJECTED_BY_EXPLICIT_TRANSLATION_WITNESS")
        self.assertFalse(record["word_lower_bound_promoted_to_geometric"])


if __name__ == "__main__":
    unittest.main()

