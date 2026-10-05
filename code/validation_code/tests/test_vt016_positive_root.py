"""VT-016 first-shell positive-root tests."""

import unittest

from validation_code.first_shell.first_shell_surface import REGISTERED_Q1
from validation_code.first_shell.vt016_positive_root import validate_positive_root


class FirstShellPositiveRootValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = validate_positive_root()

    def test_root_formula(self):
        self.assertLessEqual(self.report["root_residual"], self.report["registered_tolerance"])
        self.assertAlmostEqual(self.report["w_star_over_t"], 1.0 / REGISTERED_Q1, places=14)

    def test_plus_block_is_flat(self):
        self.assertLessEqual(self.report["flat_plus_block_residual"], self.report["registered_tolerance"])

    def test_gap_formula_and_positivity(self):
        self.assertLessEqual(self.report["gap_residual"], self.report["registered_tolerance"])
        self.assertGreater(self.report["g_star_over_t"], 0.0)

    def test_combined_gate(self):
        self.assertTrue(self.report["passed"])
        self.assertEqual(self.report["test_id"], "VT-016")


if __name__ == "__main__":
    unittest.main()
