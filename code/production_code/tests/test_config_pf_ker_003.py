"""PF-KER-003 paired-cover rule freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class PairedCoverRuleFreezeTests(unittest.TestCase):
    def test_exact_lift_minimization_and_ties(self):
        rule = yaml.safe_load((ROOT / "production_code/config/kernel.yaml").read_text(encoding="utf-8"))["paired_cover_distance"]
        self.assertEqual(rule["method"], "exact_paired_cover_subgroup_lift_minimization")
        self.assertEqual(rule["lift_domain"], "certified_normal_subgroup")
        self.assertEqual(rule["tie_action"], "retain_all_minimizers")
        self.assertIn("euclidean_minimum_image", rule["forbidden_approximations"])
        self.assertIn("graph_shortest_path", rule["forbidden_approximations"])


if __name__ == "__main__": unittest.main()

