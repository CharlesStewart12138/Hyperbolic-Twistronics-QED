"""PF-KER-004 all-pairs enumeration freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class PairEnumerationFreezeTests(unittest.TestCase):
    def test_all_pairs_and_sparse_storage(self):
        policy = yaml.safe_load((ROOT / "production_code/config/kernel.yaml").read_text(encoding="utf-8"))["pair_enumeration"]
        self.assertEqual(policy["domain"], "all_ordered_layer1_layer2_site_pairs")
        self.assertFalse(policy["diagonal_label_special_case"])
        self.assertFalse(policy["first_neighbor_special_case"])
        self.assertEqual(policy["storage"]["format"], "CSR")
        self.assertTrue(policy["storage"]["preserve_all_supported_entries"])


if __name__ == "__main__": unittest.main()

