"""CORE-01 through CORE-05 practical-core acceptance tests."""

import unittest

from production_code.group.automorphism import phi8
from production_code.group.core import (
    conjugate,
    core_contract,
    core_index_upper_bound,
    core_signature,
    cumulative_core_membership,
    in_core,
    multiply_signatures,
)
from production_code.group.injectivity import freely_reduced_words
from production_code.group.parity import parity
from production_code.group.quotient_candidate import abelian_validation_candidate
from production_code.group.surface_group import free_reduce


class PracticalCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q4 = abelian_validation_candidate(4)
        cls.q2 = abelian_validation_candidate(2)
        cls.kernel_word = ("a1", "a1", "a1", "a1")

    def test_core_01_normality(self):
        self.assertTrue(in_core(self.q4, self.kernel_word))
        for token in ("a1", "b1", "a2", "b2"):
            self.assertTrue(in_core(self.q4, conjugate((token,), self.kernel_word)))

    def test_core_02_parity_inclusion(self):
        self.assertEqual(parity(self.kernel_word), 0)
        self.assertTrue(core_contract(self.q4)["parity_inclusion"])

    def test_core_03_c8_invariance(self):
        self.assertTrue(in_core(self.q4, phi8(self.kernel_word)))
        for length in range(1, 4):
            for word in freely_reduced_words(length):
                self.assertEqual(in_core(self.q4, word), in_core(self.q4, phi8(word)))

    def test_core_04_finite_index_quotient_consistency(self):
        left = ("a1", "b2_inv")
        right = ("a2", "b1")
        combined = free_reduce(left + right)
        self.assertEqual(
            core_signature(self.q4, combined),
            multiply_signatures(self.q4, core_signature(self.q4, left), core_signature(self.q4, right)),
        )
        self.assertEqual(core_index_upper_bound(self.q4), 2 * self.q4.order**8)
        self.assertFalse(core_contract(self.q4)["finite_index_upper_bound_is_exact_order"])

    def test_core_05_nested_cumulative_core(self):
        for length in range(1, 5):
            for word in freely_reduced_words(length):
                if cumulative_core_membership((self.q4,), word):
                    self.assertTrue(cumulative_core_membership((self.q2,), word))
                if cumulative_core_membership((self.q2, self.q4), word):
                    self.assertTrue(cumulative_core_membership((self.q2,), word))


if __name__ == "__main__":
    unittest.main()

