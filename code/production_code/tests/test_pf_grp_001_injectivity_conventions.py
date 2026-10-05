"""Tests for the three noninterchangeable injectivity conventions."""

import unittest

from production_code.group.injectivity_conventions import side_by_side_report
from production_code.group.quotient_candidate import abelian_validation_candidate


class InjectivityConventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = side_by_side_report(
            abelian_validation_candidate(4),
            maximum_presentation_length=5,
            maximum_geometric_length=5,
        )

    def test_three_records_are_separate(self):
        self.assertIn("standard_presentation_word", self.record)
        self.assertIn("physical_geometric_word", self.record)
        self.assertIn("hyperbolic_geometric", self.record)
        self.assertFalse(self.record["word_metrics_interchangeable"])

    def test_word_witnesses_do_not_fill_geometric_minima(self):
        self.assertIsNotNone(self.record["standard_presentation_word"]["radius"])
        self.assertIsNotNone(self.record["physical_geometric_word"]["physical_geometric_word_radius"])
        self.assertIsNone(self.record["hyperbolic_geometric"]["based_hyperbolic_injectivity_over_a"])
        self.assertIsNone(self.record["hyperbolic_geometric"]["global_hyperbolic_injectivity_over_a"])
        self.assertFalse(self.record["word_radius_promoted_to_hyperbolic_radius"])

    def test_witness_supplies_only_upper_bounds(self):
        hyperbolic = self.record["hyperbolic_geometric"]
        self.assertIsNotNone(hyperbolic["based_witness_upper_bound_over_a"])
        self.assertIsNotNone(hyperbolic["global_witness_upper_bound_over_a"])
        self.assertIn("UPPER_BOUNDS_ONLY", hyperbolic["status"])

    def test_option_b_cutoffs_and_forbidden_surrogates(self):
        self.assertEqual(self.record["option_B_acceptance_cutoffs"], {
            "based_geometric_word_length": 127,
            "global_geometric_word_length": 156,
        })
        self.assertFalse(self.record["graph_diameter_used_as_radius"])
        self.assertFalse(self.record["group_order_used_as_radius"])


if __name__ == "__main__":
    unittest.main()
