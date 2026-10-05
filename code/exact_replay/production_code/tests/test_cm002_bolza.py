"""CM-002 exact Bolza-geometry regression tests."""
from math import acosh, isclose, pi, sqrt
import unittest

from production_code.geometry.bolza import basic_translation, constants, neighbour_centres, neighbour_map, vertices
from production_code.geometry.hyperbolic import distance


class BolzaGeometryTests(unittest.TestCase):
    def test_manuscript_constants(self):
        c = constants(2.3)
        self.assertTrue(isclose(c.area, 4*pi*2.3**2, rel_tol=2e-15))
        self.assertTrue(isclose(c.inradius, 2.3*acosh(1+sqrt(2)), rel_tol=2e-15))
        self.assertTrue(isclose(c.kappa_B, 2*acosh(1+sqrt(2)), rel_tol=2e-15))
        self.assertTrue(isclose(c.vertex_disk_radius, 2**(-0.25), rel_tol=0.0, abs_tol=0.0))

    def test_eight_exact_vertices(self):
        points = vertices()
        self.assertEqual(len(points), 8)
        self.assertTrue(all(isclose(abs(z), 2**(-0.25), rel_tol=2e-15) for z in points))

    def test_neighbour_spacing(self):
        R = 1.7
        spacing = constants(R).lattice_spacing
        self.assertTrue(all(isclose(distance(0j, z, R), spacing, rel_tol=3e-15) for z in neighbour_centres(R)))

    def test_inverse_pairing_s_nu_plus_four(self):
        z = 0.12 + 0.08j
        for nu in range(4):
            self.assertAlmostEqual(neighbour_map(nu+4, neighbour_map(nu, z)).real, z.real, places=14)
            self.assertAlmostEqual(neighbour_map(nu+4, neighbour_map(nu, z)).imag, z.imag, places=14)

    def test_basic_translation_is_not_linearized(self):
        z = 0.2j
        eta = constants(1.0).translation_eta
        self.assertEqual(basic_translation(z), (z+eta)/(eta*z+1))


if __name__ == "__main__": unittest.main()

