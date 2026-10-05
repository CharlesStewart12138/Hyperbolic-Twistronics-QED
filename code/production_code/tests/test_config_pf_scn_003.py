"""PF-SCN-003 curvature-coordinate freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class CurvatureCoordinateFreezeTests(unittest.TestCase):
    def test_coordinate_and_scope_are_unambiguous(self):
        curvature = yaml.safe_load((ROOT / "production_code/config/scan.yaml").read_text(encoding="utf-8"))["curvature"]
        self.assertEqual(curvature["primary_data_coordinate"], "kappa_a")
        self.assertEqual(curvature["signed_gaussian_curvature"], "K=-1/R^2")
        self.assertEqual(curvature["nonnegative_dimensional_magnitude"], "kappa=-K=1/R^2")
        self.assertEqual(curvature["scan_interval_exact"], ["0", "kappa_B"])
        self.assertEqual(curvature["endpoint_scope"]["open_interior"], "synthetic_constant_curvature_metric_interpolation")


if __name__ == "__main__": unittest.main()

