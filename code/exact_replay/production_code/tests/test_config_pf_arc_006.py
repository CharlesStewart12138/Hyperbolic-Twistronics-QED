"""PF-ARC-006 exact Bolza-curvature freeze regression."""
from math import acosh, isclose, sqrt
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class BolzaCurvatureFreezeTests(unittest.TestCase):
    def test_exact_bolza_value(self):
        bolza = yaml.safe_load((ROOT / "production_code/config/geometry.yaml").read_text(encoding="utf-8"))["bolza"]["kappa_B"]
        self.assertTrue(isclose(bolza["value"], 2.0 * acosh(1.0 + sqrt(2.0)), rel_tol=0.0, abs_tol=5e-15))
        self.assertFalse(bolza["tunable"])
        self.assertEqual(bolza["units"], "dimensionless")


if __name__ == "__main__": unittest.main()

