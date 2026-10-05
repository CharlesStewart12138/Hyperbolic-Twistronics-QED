"""T-CR01 through T-CR07 theorem-contract tests."""

from pathlib import Path
import unittest

from production_code.group.characteristic_tower import (
    homomorphism_count_upper_bound,
    residual_separation_level,
    theorem_level,
)


class CharacteristicResidualTowerTests(unittest.TestCase):
    def test_t_cr01_normal(self):
        self.assertTrue(theorem_level(1).normal)

    def test_t_cr02_finite_index(self):
        self.assertTrue(theorem_level(7).finite_index)
        self.assertEqual(homomorphism_count_upper_bound((1, 2), 4), 17)

    def test_t_cr03_nested(self):
        self.assertTrue(theorem_level(2).nested_in_previous)
        self.assertFalse(theorem_level(1).nested_in_previous)

    def test_t_cr04_characteristic(self):
        self.assertTrue(theorem_level(5).characteristic)

    def test_t_cr05_phi8_invariant(self):
        self.assertTrue(theorem_level(5).automorphism_invariant)

    def test_t_cr06_parity_inclusion_for_M_at_least_two(self):
        self.assertFalse(theorem_level(1).parity_compatible)
        self.assertTrue(theorem_level(2).parity_compatible)

    def test_t_cr07_residual_and_not_falsely_enumerated(self):
        self.assertEqual(residual_separation_level(24), 24)
        self.assertFalse(theorem_level(24).explicit_enumerated_level)
        root = Path(__file__).resolve().parents[1] / "group"
        self.assertTrue((root / "CHARACTERISTIC_RESIDUAL_TOWER_NOTE.md").is_file())
        self.assertTrue((root / "CHARACTERISTIC_RESIDUAL_TOWER_CONTRACT.yaml").is_file())


if __name__ == "__main__":
    unittest.main()

