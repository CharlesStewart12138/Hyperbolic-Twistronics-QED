"""PF-ARC-003 degree-eight freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class IntralayerDegreeFreezeTests(unittest.TestCase):
    def test_declared_hyperbolic_degree_is_eight(self):
        model = yaml.safe_load((ROOT / "production_code/config/model.yaml").read_text(encoding="utf-8"))
        self.assertEqual(model["model_class"]["production_hyperbolic"]["intralayer_degree"], 8)


if __name__ == "__main__": unittest.main()

