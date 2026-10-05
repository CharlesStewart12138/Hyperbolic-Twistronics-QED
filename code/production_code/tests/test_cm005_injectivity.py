"""CM-005 / T-Q12 and T-Q13 word-injectivity regression tests."""

import unittest

from production_code.group.injectivity import freely_reduced_words, word_injectivity_certificate
from production_code.group.quotient_candidate import abelian_validation_candidate


class WordInjectivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qval = abelian_validation_candidate(4)
        cls.certificate = word_injectivity_certificate(
            cls.qval,
            maximum_word_length=6,
            active_cutoff_over_a=3.0,
        )

    def test_freely_reduced_word_counts(self):
        self.assertEqual(len(list(freely_reduced_words(1))), 8)
        self.assertEqual(len(list(freely_reduced_words(2))), 8 * 7)
        self.assertEqual(len(list(freely_reduced_words(3))), 8 * 7 * 7)

    def test_t_q12_known_word_injectivity_fixture(self):
        certificate = self.certificate
        self.assertEqual(certificate["status"], "EXACT_SHORTEST_RELATION_FOUND")
        self.assertEqual(certificate["systole_word_length"], 4)
        self.assertEqual(certificate["word_injectivity_radius"], 2.0)
        self.assertEqual(certificate["exhaustive_no_relation_through_length"], 3)
        self.assertTrue(certificate["surface_group_residual_tokens"])

    def test_t_q13_qval_remains_rejected_at_production_cutoff(self):
        certificate = self.certificate
        self.assertEqual(certificate["active_Dc_over_a"], 3.0)
        self.assertFalse(certificate["no_wraparound_pass"])
        self.assertEqual(certificate["production_cutoff_status"], "NOT_CERTIFIED_WORD_ONLY")
        self.assertIsNone(certificate["physical_no_wraparound_pass"])
        self.assertFalse(certificate["word_lower_bound_promoted_to_geometric"])
        self.assertFalse(certificate["graph_diameter_used"])
        self.assertFalse(certificate["group_order_used_as_radius"])

    def test_modulus_two_negative_fixture_has_shorter_kernel(self):
        candidate = abelian_validation_candidate(2)
        certificate = word_injectivity_certificate(
            candidate,
            maximum_word_length=2,
            active_cutoff_over_a=3.0,
        )
        self.assertEqual(certificate["systole_word_length"], 2)
        self.assertEqual(certificate["word_injectivity_radius"], 1.0)
        self.assertFalse(certificate["no_wraparound_pass"])

    def test_invalid_search_bounds_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            word_injectivity_certificate(self.qval, maximum_word_length=0, active_cutoff_over_a=3.0)
        with self.assertRaisesRegex(ValueError, "cutoff"):
            word_injectivity_certificate(self.qval, maximum_word_length=4, active_cutoff_over_a=0.0)


if __name__ == "__main__":
    unittest.main()
