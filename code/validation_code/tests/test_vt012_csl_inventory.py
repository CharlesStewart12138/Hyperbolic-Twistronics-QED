"""VT-012 exact Euclidean CSL inventory tests."""

from fractions import Fraction
import unittest

from validation_code.euclidean.csl_inventory import TABLE_III_EXACT, validate_inventory


class EuclideanInventoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = validate_inventory()

    def test_all_seven_exact_rows_match_table_iii(self):
        self.assertEqual(self.report["actual_rows"], TABLE_III_EXACT)
        self.assertEqual(len(self.report["actual_rows"]), 7)

    def test_ten_site_cell(self):
        self.assertEqual(self.report["ten_site_certificate"], (5, 10, Fraction(4, 5), Fraction(3, 5)))

    def test_thirty_four_site_cell(self):
        self.assertEqual(
            self.report["thirty_four_site_certificate"],
            (17, 34, Fraction(15, 17), Fraction(8, 17)),
        )

    def test_independent_angles_and_combined_gate(self):
        self.assertLessEqual(max(self.report["angle_residuals_radian"]), 1e-12)
        self.assertTrue(self.report["passed"])


if __name__ == "__main__":
    unittest.main()
