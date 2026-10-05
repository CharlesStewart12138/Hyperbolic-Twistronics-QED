"""CM-003 exact surface-group relation regression tests."""
import unittest

from production_code.group.surface_group import RELATOR, equivalent, free_reduce, inverse_word, relation_residual


class SurfaceGroupWordTests(unittest.TestCase):
    def test_defining_relator_is_exact_identity(self):
        self.assertEqual(relation_residual(RELATOR), ())
        self.assertEqual(relation_residual(inverse_word(RELATOR)), ())

    def test_free_inverse_pairs_cancel(self):
        self.assertEqual(free_reduce(("a1", "a1_inv", "b2", "b2_inv")), ())

    def test_engine_does_not_abelianize(self):
        self.assertFalse(equivalent(("a1", "b1"), ("b1", "a1")))
        self.assertNotEqual(relation_residual(("a1", "b1", "a1_inv", "b1_inv")), ())

    def test_relator_allows_one_commutator_to_replace_the_other(self):
        first = ("a1", "b1", "a1_inv", "b1_inv")
        second = ("a2", "b2", "a2_inv", "b2_inv")
        self.assertTrue(equivalent(first, inverse_word(second)))


if __name__ == "__main__": unittest.main()

