"""CM-025 ideal and finite-window diffraction tests."""

from math import pi
import unittest

import numpy as np

from production_code.euclidean.diffraction import (
    ReciprocalPeak,
    first_shell_splitting,
    normalized_structure_factor,
    reciprocal_peaks,
    rectangular_window_transform,
    windowed_amplitude,
    windowed_intensity,
)


class EuclideanDiffractionTests(unittest.TestCase):
    def test_ideal_support_is_two_layer_resolved_reciprocal_combs(self):
        peaks = reciprocal_peaks(pi/6, maximum_index=1)
        self.assertEqual(len(peaks), 18)
        self.assertEqual({peak.layer for peak in peaks}, {1, 2})
        layer1 = {peak.indices: peak.q for peak in peaks if peak.layer == 1}
        self.assertEqual(layer1[(1, 0)], (2*pi, 0.0))

    def test_exact_first_shell_splitting_matches_rotated_vector(self):
        theta = 0.173
        peaks = reciprocal_peaks(theta, maximum_index=1)
        q1 = np.array(next(peak.q for peak in peaks if peak.layer == 1 and peak.indices == (1, 0)))
        q2 = np.array(next(peak.q for peak in peaks if peak.layer == 2 and peak.indices == (1, 0)))
        self.assertAlmostEqual(np.linalg.norm(q2-q1), first_shell_splitting(theta), places=14)

    def test_rectangular_window_has_exact_area_and_fourier_zero(self):
        values = rectangular_window_transform(np.array([[0.0, 0.0], [2*pi/8.0, 0.0]]), lengths_over_a=(8.0, 5.0))
        self.assertEqual(values[0], 40.0)
        self.assertLess(abs(values[1]), 2e-15)

    def test_rigid_layer_translation_changes_phase_not_isolated_intensity(self):
        peak = ReciprocalPeak(2, (1, 0), (2*pi, 0.0))
        window = lambda dq: rectangular_window_transform(dq, lengths_over_a=(6.0, 7.0))
        q = np.array([2*pi, 0.0])
        unshifted = windowed_amplitude(q, [peak], window)
        shifted = windowed_amplitude(q, [peak], window, layer_2_displacement_over_a=(0.125, 0.0))
        self.assertAlmostEqual(abs(unshifted), abs(shifted), places=13)
        self.assertAlmostEqual(windowed_intensity(q, [peak], window), abs(unshifted)**2, places=13)

    def test_normalized_structure_factor_mass_at_origin(self):
        positions = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
        self.assertEqual(normalized_structure_factor(np.zeros(2), positions), 4.0)
        q = np.array([[0.0, 0.0], [pi, pi]])
        values = normalized_structure_factor(q, positions)
        self.assertEqual(values.shape, (2,))
        self.assertLess(values[1], 1e-30)

    def test_equal_weight_45_degree_peak_union_has_c8_symmetry(self):
        peaks = reciprocal_peaks(pi/4, maximum_index=1)
        support = np.array([peak.q for peak in peaks])
        rotate = np.array([[np.cos(pi/4), -np.sin(pi/4)], [np.sin(pi/4), np.cos(pi/4)]])
        for point in support:
            rotated = rotate@point
            self.assertLess(np.min(np.linalg.norm(support-rotated[None, :], axis=1)), 2e-12)


if __name__ == "__main__":
    unittest.main()
