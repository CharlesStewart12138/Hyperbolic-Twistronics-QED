"""VT-002 Bolza-constant regression tests."""

from math import acosh, sqrt
import unittest

from validation_code.geometry.bolza_constants import validate_bolza_constants


class BolzaConstantValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = validate_bolza_constants()

    def test_gate_passes_at_registered_tolerance(self):
        self.assertTrue(self.report["passed"])
        self.assertEqual(self.report["relative_tolerance"], 1e-12)

    def test_exact_formula_and_published_rounding_are_distinguished(self):
        exact = 2.0 * acosh(1.0 + sqrt(2.0))
        self.assertAlmostEqual(self.report["expected_kappa_exact"], exact, places=15)
        self.assertEqual(round(exact, self.report["display_decimal_places"]), self.report["expected_kappa_decimal"])
        self.assertGreater(self.report["literal_relative_difference"], 1e-12)

    def test_scale_independence(self):
        values = {round(item["a_B_over_R"], 14) for item in self.report["measurements"]}
        self.assertEqual(len(values), 1)


if __name__ == "__main__":
    unittest.main()
