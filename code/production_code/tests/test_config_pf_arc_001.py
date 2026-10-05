"""PF-ARC-001 layer-count freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class LayerCountFreezeTests(unittest.TestCase):
    def test_production_hyperbolic_layer_count_is_two(self):
        model = yaml.safe_load((ROOT / "production_code/config/model.yaml").read_text(encoding="utf-8"))
        self.assertEqual(model["model_class"]["production_hyperbolic"]["layers"], 2)


if __name__ == "__main__": unittest.main()

