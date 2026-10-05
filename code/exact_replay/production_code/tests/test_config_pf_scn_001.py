"""PF-SCN-001 hyperbolic-twist-domain freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class HyperbolicTwistDomainFreezeTests(unittest.TestCase):
    def test_irreducible_interval_is_full_zero_to_pi_over_eight(self):
        scan = yaml.safe_load((ROOT / "production_code/config/scan.yaml").read_text(encoding="utf-8"))["hyperbolic_twist"]
        interval = scan["irreducible_interval"]
        self.assertEqual((interval["lower_exact"], interval["upper_exact"]), ("0", "pi/8"))
        self.assertTrue(interval["lower_inclusive"] and interval["upper_inclusive"])
        self.assertEqual(scan["coverage_policy"], "full_interval")
        self.assertEqual(scan["internal_coordinate"], "signed_radians")


if __name__ == "__main__": unittest.main()

