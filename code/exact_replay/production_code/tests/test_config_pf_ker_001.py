"""PF-KER-001 radial-law freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class RadialKernelFreezeTests(unittest.TestCase):
    def test_exact_exponential_family_is_frozen(self):
        radial = yaml.safe_load((ROOT / "production_code/config/kernel.yaml").read_text(encoding="utf-8"))["radial_hopping"]
        self.assertEqual(radial["family"], "exponential_full_distance")
        self.assertEqual(radial["exact_formula"], "T(D)=w*exp(-(D-h)/lambda_perp)")
        self.assertEqual(radial["alternate_profile_policy"], "separate_model_freeze_required")
        self.assertEqual(radial["derivatives_required"][:2], ["theta_first", "theta_second"])


if __name__ == "__main__": unittest.main()

