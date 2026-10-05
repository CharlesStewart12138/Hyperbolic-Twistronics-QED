"""PF-HOD-002 exact canonical Hodge-metric tests."""

import unittest

import sympy as sp

from production_code.hodge.bolza_hodge_metric import (
    a_normalized_riemann_matrix,
    certificate,
    cycle_hermitian_form_block,
    cycle_metric_standard,
    hodge_metric_leading_principal_minors,
    hodge_metric_standard,
    inverse_sqrt_hodge_metric,
    metric_normalized_hessian,
    period_gram_cycle_metric_standard,
    period_stack,
    riemann_imaginary_part,
)


class BolzaHodgeMetricTests(unittest.TestCase):
    def test_exact_a_normalized_riemann_matrix(self):
        root2 = sp.sqrt(2)
        expected = sp.ImmutableMatrix(
            [
                [-sp.Rational(2, 3) + 2 * root2 * sp.I / 3, sp.Rational(1, 3) - root2 * sp.I / 3],
                [sp.Rational(1, 3) - root2 * sp.I / 3, -sp.Rational(2, 3) + 2 * root2 * sp.I / 3],
            ]
        )
        self.assertEqual(a_normalized_riemann_matrix(), expected)
        self.assertEqual(expected, expected.T)

    def test_riemann_imaginary_part_is_positive(self):
        root2 = sp.sqrt(2)
        y = riemann_imaginary_part()
        self.assertEqual(y.eigenvals(), {root2 / 3: 1, root2: 1})
        self.assertTrue(all(value.is_positive for value in y.eigenvals()))

    def test_period_stack_implements_declared_C_formula(self):
        omega = sp.Matrix(period_stack())
        y_inverse = sp.Matrix(riemann_imaginary_part()).inv()
        expected = (omega * y_inverse * omega.conjugate().T).applyfunc(sp.simplify)
        self.assertEqual(cycle_hermitian_form_block(), expected)
        self.assertEqual(expected, expected.conjugate().T)

    def test_two_independent_cycle_metric_constructions_agree(self):
        self.assertEqual(cycle_metric_standard(), period_gram_cycle_metric_standard())

    def test_exact_cohomology_hodge_metric(self):
        root2 = sp.sqrt(2)
        expected = sp.ImmutableMatrix(
            [
                [root2, root2 / 2, -root2 / 2, 0],
                [root2 / 2, root2, 0, root2 / 2],
                [-root2 / 2, 0, root2, root2 / 2],
                [0, root2 / 2, root2 / 2, root2],
            ]
        )
        self.assertEqual(hodge_metric_standard(), expected)
        self.assertEqual(expected.det(), 1)
        self.assertNotEqual(expected, sp.eye(4))

    def test_sylvester_and_spectral_positivity_certificates(self):
        root2 = sp.sqrt(2)
        self.assertEqual(hodge_metric_leading_principal_minors(), (root2, sp.Rational(3, 2), root2, 1))
        simplified_spectrum = {
            sp.simplify(eigenvalue): multiplicity
            for eigenvalue, multiplicity in hodge_metric_standard().eigenvals().items()
        }
        self.assertEqual(simplified_spectrum, {root2 - 1: 2, root2 + 1: 2})

    def test_exact_inverse_square_root(self):
        inverse_sqrt = sp.Matrix(inverse_sqrt_hodge_metric())
        metric = sp.Matrix(hodge_metric_standard())
        self.assertEqual(sp.simplify(inverse_sqrt * metric * inverse_sqrt), sp.eye(4))

    def test_metric_normalization_retains_all_principal_directions(self):
        metric = hodge_metric_standard()
        self.assertEqual(metric_normalized_hessian(metric), sp.eye(4))
        normalized_identity = metric_normalized_hessian(sp.eye(4))
        self.assertEqual(normalized_identity, metric.inv().applyfunc(sp.simplify))
        simplified_spectrum = {
            sp.simplify(eigenvalue): multiplicity
            for eigenvalue, multiplicity in normalized_identity.eigenvals().items()
        }
        self.assertEqual(simplified_spectrum, {sp.sqrt(2) - 1: 2, sp.sqrt(2) + 1: 2})

    def test_generalized_spectrum_is_coordinate_invariant(self):
        metric = sp.Matrix(hodge_metric_standard())
        hessian = sp.diag(1, 2, 4, 7)
        basis_change = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
        transformed_metric = basis_change.T * metric * basis_change
        transformed_hessian = basis_change.T * hessian * basis_change
        variable = sp.Symbol("lambda")
        original = sp.factor((hessian - variable * metric).det())
        transformed = sp.factor((transformed_hessian - variable * transformed_metric).det())
        self.assertEqual(original, transformed)

    def test_bad_hessian_shape_and_asymmetry_are_rejected(self):
        with self.assertRaises(ValueError):
            metric_normalized_hessian(sp.eye(3))
        bad = sp.eye(4)
        bad[0, 1] = 1
        with self.assertRaises(ValueError):
            metric_normalized_hessian(bad)

    def test_release_certificate_passes(self):
        result = certificate()
        self.assertTrue(result.passed)
        self.assertEqual(result.metric_determinant, 1)
        self.assertTrue(result.metric_not_identity)
        self.assertTrue(result.quotient_independent)


if __name__ == "__main__":
    unittest.main()

