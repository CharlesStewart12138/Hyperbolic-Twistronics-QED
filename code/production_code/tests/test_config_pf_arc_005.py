"""PF-ARC-005 surface-presentation freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class SurfacePresentationFreezeTests(unittest.TestCase):
    def test_genus_two_relator_is_exact(self):
        surface = yaml.safe_load((ROOT / "production_code/config/geometry.yaml").read_text(encoding="utf-8"))["surface_group"]
        presentation = surface["presentation"]
        self.assertEqual(presentation["positive_generators"], ["a1", "b1", "a2", "b2"])
        self.assertEqual(presentation["relator_tokens"], ["a1", "b1", "a1_inv", "b1_inv", "a2", "b2", "a2_inv", "b2_inv"])
        inverse = surface["inverse_map"]
        tokens = presentation["relator_tokens"]
        self.assertEqual(tokens[2], inverse[tokens[0]])
        self.assertEqual(tokens[3], inverse[tokens[1]])
        self.assertEqual(tokens[6], inverse[tokens[4]])
        self.assertEqual(tokens[7], inverse[tokens[5]])


if __name__ == "__main__": unittest.main()

