"""PF-SCN-002 Euclidean-twist-domain freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class EuclideanTwistDomainFreezeTests(unittest.TestCase):
    def test_square_interval_and_csl_scope(self):
        scan = yaml.safe_load((ROOT / "production_code/config/scan.yaml").read_text(encoding="utf-8"))["euclidean_twist"]
        interval = scan["irreducible_interval"]
        self.assertEqual((interval["lower_exact"], interval["upper_exact"]), ("0", "pi/4"))
        self.assertEqual(scan["commensurate_policy"], "exact_CSL_points_only")
        self.assertEqual(scan["generic_angle_policy"], "fixed_Hilbert_space_no_CSL_index")


if __name__ == "__main__": unittest.main()

