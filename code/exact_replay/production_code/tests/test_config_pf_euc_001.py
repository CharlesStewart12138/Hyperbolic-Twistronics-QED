"""PF-EUC-001 exact sub-100 CSL-set freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class EuclideanCSLSetFreezeTests(unittest.TestCase):
    def test_complete_exact_cell_inventory(self):
        config = yaml.safe_load((ROOT / "production_code/config/euclidean.yaml").read_text(encoding="utf-8"))["production_supercells"]
        cells = config["cells"]
        self.assertEqual(len(cells), 7)
        self.assertEqual({cell["Sigma"] for cell in cells}, {5, 13, 17, 25, 29, 37, 41})
        self.assertEqual({cell["Nsc"] for cell in cells}, {10, 26, 34, 50, 58, 74, 82})
        for cell in cells:
            self.assertEqual(cell["Nsc"], 2 * cell["Sigma"])
            self.assertEqual(cell["cos_num"] ** 2 + cell["sin_num"] ** 2, cell["denominator"] ** 2)
        self.assertFalse(config["forty_five_degree"]["finite_square_CSL"])


if __name__ == "__main__": unittest.main()

