"""P8-01 through P8-07 exact automorphism acceptance tests."""

from pathlib import Path
import unittest

from production_code.group.automorphism import (
    PHI8_POSITIVE,
    PRIMITIVE_GENERATORS,
    certificate,
    independent_numeric_conjugation_residual,
    parity,
    phi8,
    phi8_inverse,
    phi8_power,
    standard_s8_images,
)
from production_code.group.surface_group import RELATOR, TOKENS, relation_residual


class BolzaPhi8Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = certificate()

    def test_p8_01_surface_relator_maps_to_identity(self):
        self.assertFalse(relation_residual(phi8(RELATOR)))
        self.assertTrue(self.certificate.p8_01_relator_identity)

    def test_p8_02_explicit_inverse(self):
        self.assertTrue(self.certificate.p8_02_invertible)
        for token in TOKENS:
            self.assertEqual(phi8_inverse(phi8((token,))), (token,))
            self.assertEqual(phi8(phi8_inverse((token,))), (token,))

    def test_p8_03_eighth_power_is_identity(self):
        self.assertTrue(self.certificate.p8_03_eighth_power_identity)
        for token in TOKENS:
            self.assertEqual(phi8_power((token,), 8), (token,))

    def test_p8_04_no_smaller_positive_power_is_identity(self):
        self.assertTrue(self.certificate.p8_04_no_smaller_positive_power)
        self.assertTrue(all(phi8_power(("a1",), power) != ("a1",) for power in range(1, 8)))

    def test_p8_05_declared_standard_s8_claim_fails_closed(self):
        self.assertFalse(self.certificate.p8_05_declared_standard_s8_invariant)
        self.assertTrue(any(image is None for image in standard_s8_images().values()))
        report = Path(__file__).resolve().parents[1] / "group" / "INTERNAL_MANUSCRIPT_INCONSISTENCY_P8_05.md"
        self.assertTrue(report.is_file())

    def test_p8_06_exact_geometric_conjugation(self):
        self.assertTrue(self.certificate.p8_06_geometric_conjugation)
        self.assertLess(independent_numeric_conjugation_residual(140), 10 ** -120)

    def test_p8_07_parity_invariance(self):
        self.assertTrue(self.certificate.p8_07_parity_invariant)
        for token in PRIMITIVE_GENERATORS:
            self.assertEqual(parity(phi8((token,))), parity((token,)))
        self.assertEqual(PHI8_POSITIVE["a1"], ("b1_inv",))
        registry = Path(__file__).resolve().parents[1] / "group" / "BOLZA_PHI8_AUTOMORPHISM.yaml"
        self.assertTrue(registry.is_file())


if __name__ == "__main__":
    unittest.main()

