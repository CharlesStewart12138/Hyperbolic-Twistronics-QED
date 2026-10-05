"""VT-003 universal surface relation tests."""

from fractions import Fraction
import unittest

from validation_code.group.surface_relation import validate_surface_relation


class SurfaceRelationValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = validate_surface_relation()

    def test_universal_presentation_residual_is_empty(self):
        self.assertTrue(self.report["universal_certificate"])
        self.assertEqual(self.report["universal_relator_residual"], ())

    def test_nonabelian_s3_quotient_closes(self):
        self.assertEqual(self.report["s3_nonabelian_quotient_result"], (0, 1, 2))

    def test_exact_rational_matrix_representation_closes(self):
        identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
        self.assertEqual(self.report["rational_matrix_representation_result"], identity)

    def test_combined_gate_passes_exactly(self):
        self.assertTrue(self.report["passed"])
        self.assertEqual(self.report["criterion"], "Exact")


if __name__ == "__main__":
    unittest.main()
