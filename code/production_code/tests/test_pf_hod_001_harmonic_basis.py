"""PF-HOD-001 exact local harmonic tangent-basis tests."""

import unittest

import sympy as sp

from production_code.hodge.bolza_harmonic_basis import (
    basis_evaluation_matrix,
    certificate,
    geometric_period_matrix,
    identity_transport,
    nielsen_homology_matrix,
    realify_period_matrix,
    spans_full_h1,
    standard_cohomology_in_geometric_dual,
    standard_period_matrix,
    surface_relator_abelianization,
)


class BolzaHarmonicBasisTests(unittest.TestCase):
    def test_surface_relator_has_zero_abelianization(self):
        self.assertEqual(surface_relator_abelianization(), sp.zeros(4, 1))

    def test_full_standard_dual_basis(self):
        evaluations = basis_evaluation_matrix()
        self.assertEqual(evaluations, sp.eye(4))
        self.assertTrue(spans_full_h1(evaluations))

    def test_single_direction_or_rank_three_surrogate_is_rejected(self):
        self.assertFalse(spans_full_h1([[1, 0, 0, 0]]))
        self.assertFalse(spans_full_h1(sp.diag(1, 1, 1, 0)))

    def test_nielsen_homology_transport_is_exact_and_unimodular(self):
        matrix = nielsen_homology_matrix()
        self.assertEqual(matrix.det(), 1)
        self.assertEqual(
            standard_cohomology_in_geometric_dual(),
            sp.ImmutableMatrix([[1, 0, 0, 0], [0, 1, 0, 0], [-1, -1, 1, 0], [1, 1, 0, 1]]),
        )

    def test_quine_geometric_periods_have_exact_real_rank_four(self):
        realified = realify_period_matrix(geometric_period_matrix())
        self.assertEqual(realified.det(), -8)
        self.assertEqual(realified.rank(), 4)

    def test_standard_marking_preserves_exact_period_rank(self):
        realified = realify_period_matrix(standard_period_matrix())
        self.assertEqual(realified.det(), -8)
        self.assertEqual(realified.rank(), 4)

    def test_nonzero_common_period_scale_preserves_rank(self):
        scaled = realify_period_matrix(geometric_period_matrix(sp.sqrt(3)))
        self.assertEqual(scaled.rank(), 4)
        self.assertNotEqual(scaled.det(), 0)

    def test_bad_period_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            realify_period_matrix(sp.eye(2))

    def test_scalar_character_transport_is_exact_identity(self):
        self.assertEqual(identity_transport(), sp.eye(4))

    def test_release_certificate_passes(self):
        result = certificate()
        self.assertTrue(result.passed)
        self.assertTrue(result.quotient_independent)
        self.assertTrue(result.scalar_character_scope)
        self.assertEqual(result.h1_real_dimension, 4)
        self.assertEqual(result.full_basis_rank, 4)
        self.assertEqual(result.geometric_period_real_determinant, -8)
        self.assertEqual(result.standard_period_real_determinant, -8)


if __name__ == "__main__":
    unittest.main()

