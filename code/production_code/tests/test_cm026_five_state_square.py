"""CM-026 exact five-state validation-control tests."""
from math import isclose, sqrt
import unittest
import numpy as np

from validation_code.five_state.five_state_square import ALPHA_MIN_SQUARED, LOWER_BOUND, curvature_coefficient, hamiltonian, point_spectrum


class FiveStateSquareControlTests(unittest.TestCase):
    def test_exact_matrix_and_point_spectrum(self):
        alpha = 0.3
        matrix = hamiltonian(0.0, 0.0, alpha, run_type="validation")
        self.assertEqual(matrix.shape, (5,5))
        self.assertTrue(np.allclose(matrix, matrix.T, rtol=0.0, atol=0.0))
        self.assertTrue(np.allclose(np.linalg.eigvalsh(matrix), point_spectrum(alpha, run_type="validation"), rtol=2e-15, atol=2e-15))

    def test_global_minimum_is_four_sqrt_two_minus_five(self):
        alpha_min = sqrt(ALPHA_MIN_SQUARED)
        self.assertTrue(isclose(curvature_coefficient(alpha_min, run_type="validation"), LOWER_BOUND, rel_tol=2e-15))
        for alpha in np.linspace(0.0, 20.0, 1001):
            self.assertGreaterEqual(curvature_coefficient(float(alpha), run_type="validation") + 1e-15, LOWER_BOUND)

    def test_formal_perturbative_root_is_not_exact(self):
        exact = curvature_coefficient(1.0/sqrt(8.0), run_type="validation")
        self.assertTrue(isclose(exact, 3.0-4.0*sqrt(3.0)/3.0, rel_tol=2e-15))
        self.assertGreater(exact, 0.0)

    def test_production_namespace_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "validation-only"):
            hamiltonian(0.0, 0.0, 0.1, run_type="production")


if __name__ == "__main__": unittest.main()

