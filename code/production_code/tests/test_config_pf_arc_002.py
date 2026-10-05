"""PF-ARC-002 orbital-count freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class OrbitalCountFreezeTests(unittest.TestCase):
    def test_production_hyperbolic_orbitals_per_site_is_one(self):
        model = yaml.safe_load((ROOT / "production_code/config/model.yaml").read_text(encoding="utf-8"))
        self.assertEqual(model["model_class"]["production_hyperbolic"]["orbitals_per_site"], 1)


if __name__ == "__main__": unittest.main()

