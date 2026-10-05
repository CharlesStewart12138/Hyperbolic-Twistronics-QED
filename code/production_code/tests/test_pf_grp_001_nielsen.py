"""PF-GRP-001-NIELSEN acceptance tests."""

from pathlib import Path
import unittest

from production_code.group.nielsen import (
    GEOMETRIC_RELATOR,
    GEOMETRIC_TOKENS,
    STANDARD_RELATOR,
    STANDARD_TOKENS,
    abelianization_matrix,
    certificate,
    geometric_to_standard,
    independent_numeric_residual,
    standard_to_geometric,
)


class BolzaNielsenMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = certificate()

    def test_nielsen_01_forward_inverse_and_unimodular(self):
        self.assertTrue(self.certificate.standard_roundtrip)
        self.assertTrue(self.certificate.geometric_roundtrip)
        self.assertTrue(self.certificate.unimodular_abelianization)
        matrix = abelianization_matrix()
        self.assertTrue(all(sum(matrix[row][column] for row in range(4)) % 2 == 1
                            for column in range(4)))
        for token in STANDARD_TOKENS:
            self.assertEqual(geometric_to_standard(standard_to_geometric((token,))), (token,))
        for token in GEOMETRIC_TOKENS:
            self.assertEqual(standard_to_geometric(geometric_to_standard((token,))), (token,))

    def test_nielsen_02_exact_relator_transport(self):
        self.assertEqual(standard_to_geometric(STANDARD_RELATOR), GEOMETRIC_RELATOR)
        self.assertEqual(geometric_to_standard(GEOMETRIC_RELATOR), STANDARD_RELATOR)
        self.assertTrue(self.certificate.standard_relator_to_geometric)
        self.assertTrue(self.certificate.geometric_relator_to_standard)

    def test_nielsen_03_exact_matrix_transport_and_numeric_witness(self):
        self.assertTrue(self.certificate.exact_matrix_reconstruction)
        self.assertTrue(self.certificate.exact_standard_matrix_relation)
        self.assertLess(independent_numeric_residual(140), 10 ** -120)
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "group" / "BOLZA_NIELSEN_MAP.yaml").is_file())
        self.assertTrue((root / "group" / "BOLZA_NIELSEN_MAP.md").is_file())


if __name__ == "__main__":
    unittest.main()

