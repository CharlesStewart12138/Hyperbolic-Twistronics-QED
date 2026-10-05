"""PF-ARC-004 S8 generator-set freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class GeneratorSetFreezeTests(unittest.TestCase):
    def test_order_and_inverse_closure(self):
        group = yaml.safe_load((ROOT / "production_code/config/geometry.yaml").read_text(encoding="utf-8"))["surface_group"]
        expected = ["a1", "a1_inv", "b1", "b1_inv", "a2", "a2_inv", "b2", "b2_inv"]
        self.assertEqual(group["generator_order"], expected)
        self.assertEqual(len(set(expected)), 8)
        for generator in expected:
            inverse = group["inverse_map"][generator]
            self.assertIn(inverse, expected)
            self.assertEqual(group["inverse_map"][inverse], generator)


if __name__ == "__main__": unittest.main()

