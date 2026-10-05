"""CM-001 analytic metric and isometry regression tests."""
from cmath import exp
from math import isclose
import unittest

from production_code.geometry.hyperbolic import distance, gaussian_curvature, metric_tensor, radial_distance


class PoincareGeometryTests(unittest.TestCase):
    def test_curvature_and_metric_at_origin(self):
        self.assertEqual(gaussian_curvature(2.0), -0.25)
        self.assertEqual(metric_tensor(0j, 2.0), ((16.0, 0.0), (0.0, 16.0)))

    def test_origin_distance_identity(self):
        z = 0.3 + 0.2j
        self.assertTrue(isclose(distance(0j, z, 1.7), radial_distance(z, 1.7), rel_tol=2e-15))

    def test_centered_rotations_are_isometries(self):
        z, w = 0.2 + 0.1j, -0.15 + 0.4j
        phase = exp(0.73j)
        self.assertTrue(isclose(distance(phase*z, phase*w, 3.0), distance(z, w, 3.0), rel_tol=2e-15))

    def test_real_disk_translation_is_an_isometry(self):
        z, w, eta = 0.12 + 0.21j, -0.27 + 0.08j, 0.35
        tau = lambda q: (q + eta) / (eta*q + 1.0)
        self.assertTrue(isclose(distance(tau(z), tau(w), 0.9), distance(z, w, 0.9), rel_tol=3e-15, abs_tol=1e-15))


if __name__ == "__main__": unittest.main()

