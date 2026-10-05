"""VT-015 exact five-state no-root tests."""

from math import sqrt
import unittest

from validation_code.five_state.vt015_no_root import validate_no_root


class FiveStateNoRootValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = validate_no_root()

    def test_global_minimum_reproduced(self):
        self.assertTrue(self.report["minimum_matches"])
        self.assertAlmostEqual(self.report["minimum_closed_form"], 4.0 * sqrt(2.0) - 5.0, places=15)

    def test_minimum_is_strictly_positive(self):
        self.assertGreater(self.report["minimum"], 0.0)

    def test_formal_quadratic_zero_is_not_exact(self):
        self.assertAlmostEqual(self.report["formal_quadratic_alpha"], 1.0 / sqrt(8.0), places=15)
        self.assertTrue(self.report["formal_zero_remains_positive"])

    def test_combined_gate(self):
        self.assertTrue(self.report["passed"])
        self.assertEqual(self.report["test_id"], "VT-015")


if __name__ == "__main__":
    unittest.main()
