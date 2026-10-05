"""P-01--P-07 physical-shell parity acceptance tests."""

import unittest

from production_code.group.physical_parity import (
    certificate,
    geometric_shell_parities,
    physical_graph_bipartite,
    quotient_parity_labels,
)
from production_code.group.quotient_candidate import abelian_validation_candidate


class PhysicalParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good = abelian_validation_candidate(4)
        cls.cert = certificate(cls.good)

    def test_p01_relator_parity_zero(self):
        self.assertTrue(self.cert.p01_relator_parity_zero)

    def test_p02_homomorphism(self):
        self.assertTrue(self.cert.p02_homomorphism)

    def test_p03_kernel_normal(self):
        self.assertTrue(self.cert.p03_kernel_normal)

    def test_p04_phi8_invariant(self):
        self.assertTrue(self.cert.p04_phi8_invariant)

    def test_p05_every_physical_generator_is_odd(self):
        self.assertEqual(geometric_shell_parities(), (1,) * 8)
        self.assertTrue(self.cert.p05_all_geometric_generators_odd)

    def test_p06_parity_factors_through_good_quotient(self):
        labels = quotient_parity_labels(self.good)
        self.assertIsNotNone(labels)
        self.assertEqual(labels[self.good.identity], 0)
        self.assertTrue(self.cert.p06_parity_factors_through_quotient)

    def test_p07_physical_graph_bipartite_and_negative_fixture(self):
        self.assertTrue(physical_graph_bipartite(self.good))
        self.assertTrue(self.cert.p07_physical_graph_bipartite)
        bad = abelian_validation_candidate(3)
        self.assertIsNone(quotient_parity_labels(bad))
        self.assertFalse(physical_graph_bipartite(bad))


if __name__ == "__main__":
    unittest.main()
