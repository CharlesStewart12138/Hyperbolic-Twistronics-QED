"""CM-023 exact full-dimensional Euclidean Bloch tests."""

from math import cos
import unittest

import numpy as np

from production_code.euclidean.bloch import (
    bloch_hamiltonian,
    folded_hamiltonian,
    folding_vectors_over_inverse_a,
    fourier_block,
    nearest_neighbor_intralayer_blocks,
)
from production_code.euclidean.csl import csl
from production_code.euclidean.interlayer import interlayer_translation_blocks


class EuclideanBlochTests(unittest.TestCase):
    def setUp(self):
        self.cell = csl(3, 1)
        self.k = np.array([0.073, -0.119])
        self.h1 = nearest_neighbor_intralayer_blocks(self.cell, 1)
        self.h2 = nearest_neighbor_intralayer_blocks(self.cell, 2)
        self.interlayer = interlayer_translation_blocks(
            self.cell, h_over_a=0.5, lambda_perp_over_a=0.2, cutoff_over_a=3.0
        )

    def test_intralayer_real_space_blocks_are_hermitian_pairs(self):
        for translation, block in self.h1.items():
            self.assertTrue(np.array_equal(block, self.h1[(-translation[0], -translation[1])].T))
        self.assertLess(np.linalg.norm(fourier_block(self.cell, self.h1, self.k)-fourier_block(self.cell, self.h1, self.k).conj().T), 1e-13)

    def test_uncoupled_site_spectrum_matches_all_folded_square_bands(self):
        h1k = fourier_block(self.cell, self.h1, self.k)
        momenta = self.k[None, :]+folding_vectors_over_inverse_a(self.cell, 1)
        expected = np.sort(np.array([-2.0*(cos(q[0])+cos(q[1])) for q in momenta]))
        self.assertTrue(np.allclose(np.linalg.eigvalsh(h1k), expected, rtol=0.0, atol=2e-13))

    def test_full_matrix_has_exact_dimension_and_hermiticity(self):
        result = bloch_hamiltonian(
            self.cell,
            k_over_inverse_a=self.k,
            layer_1_blocks=self.h1,
            layer_2_blocks=self.h2,
            interlayer_blocks_over_w=self.interlayer,
            omega0_over_t=7.0,
            w_over_t=0.3,
        )
        self.assertEqual(result.hamiltonian.shape, (2*self.cell.sigma, 2*self.cell.sigma))
        self.assertLessEqual(result.hermiticity_relative_residual, 1e-13)
        self.assertGreater(np.linalg.norm(result.interlayer), 0.0)

    def test_explicit_folded_transform_is_unitary_and_isospectral(self):
        result = bloch_hamiltonian(
            self.cell,
            k_over_inverse_a=self.k,
            layer_1_blocks=self.h1,
            layer_2_blocks=self.h2,
            interlayer_blocks_over_w=self.interlayer,
            w_over_t=0.3,
        )
        folded = folded_hamiltonian(self.cell, result.hamiltonian, self.k)
        self.assertLess(folded.unitarity_residual, 2e-14)
        self.assertLess(folded.spectral_residual, 2e-13)

    def test_invalid_block_dimension_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "real-space block"):
            bloch_hamiltonian(
                self.cell,
                k_over_inverse_a=self.k,
                layer_1_blocks={(0, 0): np.zeros((2, 2))},
                layer_2_blocks=self.h2,
                interlayer_blocks_over_w=self.interlayer,
            )


if __name__ == "__main__":
    unittest.main()
