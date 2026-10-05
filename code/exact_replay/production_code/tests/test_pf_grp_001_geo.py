"""PF-GRP-001-GEO exact Bolza generator acceptance tests."""

from pathlib import Path
import unittest

import sympy as sp

from production_code.group.bolza_interface import (
    ALPHA,
    BETA,
    exact_certificate,
    generator_matrix,
    independent_numeric_residual,
    oriented_polygon_word,
    vertices,
)


class ExactBolzaInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = exact_certificate()

    def test_geo_01_exact_regular_octagon(self):
        self.assertEqual(len(vertices()), 8)
        self.assertTrue(self.certificate.octagon_geometry)
        self.assertEqual(oriented_polygon_word(), (
            (0, 1), (1, -1), (2, 1), (3, -1),
            (0, -1), (1, 1), (2, -1), (3, 1),
        ))

    def test_geo_02_exact_su11_generators_and_inverse_pairs(self):
        self.assertEqual(sp.simplify(ALPHA**2 - BETA**2), 1)
        self.assertTrue(self.certificate.su11)
        self.assertTrue(self.certificate.inverse_pairing)
        self.assertEqual(len({str(generator_matrix(nu)) for nu in range(8)}), 8)

    def test_geo_03_exact_oriented_polygon_relation_and_numeric_witness(self):
        self.assertTrue(self.certificate.oriented_polygon_relation)
        self.assertLess(independent_numeric_residual(140), 10 ** -120)

    def test_geo_04_ordered_endpoints_and_midpoints(self):
        self.assertTrue(self.certificate.endpoint_pairing)
        self.assertTrue(self.certificate.midpoint_pairing)

    def test_machine_registry_and_report_exist(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "group" / "BOLZA_GEOMETRIC_GENERATORS.yaml").is_file())
        self.assertTrue((root / "group" / "BOLZA_GEOMETRIC_GENERATORS.md").is_file())


if __name__ == "__main__":
    unittest.main()

