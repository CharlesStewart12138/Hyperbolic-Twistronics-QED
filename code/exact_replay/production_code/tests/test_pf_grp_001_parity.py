"""Exact parity-homomorphism acceptance tests."""

from pathlib import Path
import unittest

from production_code.group.automorphism import phi8
from production_code.group.parity import (
    certificate,
    homomorphism_identity,
    in_kernel,
    normal_kernel_identity,
    parity,
    phi8_parity_identity,
)
from production_code.group.surface_group import RELATOR, TOKENS


class BolzaParityTests(unittest.TestCase):
    def test_parity_01_relator_lies_in_kernel(self):
        self.assertEqual(parity(RELATOR), 0)
        self.assertTrue(in_kernel(RELATOR))
        self.assertTrue(certificate().relator_in_kernel)

    def test_parity_02_map_is_surjective_homomorphism(self):
        self.assertEqual(parity(("a1",)), 1)
        self.assertTrue(homomorphism_identity(("a1", "b2_inv"), ("a2", "b1")))
        self.assertTrue(certificate().surjective)
        self.assertTrue(certificate().homomorphism)

    def test_parity_03_kernel_is_normal(self):
        even_words = (RELATOR, ("a1", "b1"), ("a2", "b2_inv"))
        for conjugator in tuple((token,) for token in TOKENS):
            for word in even_words:
                self.assertTrue(normal_kernel_identity(conjugator, word))
        self.assertTrue(certificate().kernel_normal)

    def test_parity_04_phi8_preserves_kernel_and_cosets(self):
        self.assertTrue(certificate().phi8_invariant)
        for token in TOKENS:
            self.assertTrue(phi8_parity_identity((token,)))
            self.assertEqual(parity(phi8((token,))), parity((token,)))
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "group" / "BOLZA_PARITY_CERTIFICATE.yaml").is_file())
        self.assertTrue((root / "group" / "BOLZA_PARITY_CERTIFICATE.md").is_file())


if __name__ == "__main__":
    unittest.main()

