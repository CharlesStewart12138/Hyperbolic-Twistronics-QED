"""CM-022 full radial Euclidean interlayer-block tests."""

from math import exp, isclose
import unittest

import numpy as np

from production_code.euclidean.csl import csl
from production_code.euclidean.interlayer import interlayer_terms, interlayer_translation_blocks, translation_vector_over_a


class EuclideanInterlayerTests(unittest.TestCase):
    def setUp(self):
        self.cell = csl(3, 1)
        self.kwargs = dict(h_over_a=0.5, lambda_perp_over_a=0.2, cutoff_over_a=3.0)

    def test_exact_moire_translation_vectors(self):
        self.assertEqual(translation_vector_over_a(self.cell, (1, 0)), (2, -1))
        self.assertEqual(translation_vector_over_a(self.cell, (0, 1)), (1, 2))

    def test_vertical_pair_has_unit_normalized_amplitude(self):
        terms = interlayer_terms(self.cell, **self.kwargs)
        vertical = [term for term in terms if term.source_index == term.target_index == 0 and term.translation == (0, 0)]
        self.assertEqual(len(vertical), 1)
        self.assertEqual(vertical[0].distance_over_a, 0.5)
        self.assertEqual(vertical[0].amplitude_over_w, 1.0)

    def test_every_retained_pair_uses_full_distance_exponential(self):
        terms = interlayer_terms(self.cell, **self.kwargs)
        self.assertTrue(terms)
        self.assertTrue(all(term.distance_over_a <= 3.0+1e-14 for term in terms))
        for term in terms:
            expected = exp(-(term.distance_over_a-0.5)/0.2)
            self.assertTrue(isclose(term.amplitude_over_w, expected, rel_tol=2e-15, abs_tol=0.0))

    def test_all_pairs_not_same_label_reduction(self):
        terms = interlayer_terms(self.cell, **self.kwargs)
        self.assertTrue(any(term.source_index != term.target_index for term in terms))
        represented = {(term.source_index, term.target_index) for term in terms}
        self.assertEqual(represented, {(i, j) for i in range(self.cell.sigma) for j in range(self.cell.sigma)})

    def test_translation_blocks_are_exact_term_assembly(self):
        terms = interlayer_terms(self.cell, **self.kwargs)
        blocks = interlayer_translation_blocks(self.cell, **self.kwargs)
        reconstructed = sum(np.count_nonzero(block) for block in blocks.values())
        self.assertEqual(reconstructed, len(terms))
        for term in terms:
            self.assertEqual(blocks[term.translation].shape, (self.cell.sigma, self.cell.sigma))
            self.assertEqual(blocks[term.translation][term.source_index, term.target_index], term.amplitude_over_w)

    def test_invalid_cutoff_cannot_exclude_vertical_separation(self):
        with self.assertRaisesRegex(ValueError, "D_c/a>=h/a"):
            interlayer_terms(self.cell, h_over_a=0.5, lambda_perp_over_a=0.2, cutoff_over_a=0.4)


if __name__ == "__main__":
    unittest.main()
