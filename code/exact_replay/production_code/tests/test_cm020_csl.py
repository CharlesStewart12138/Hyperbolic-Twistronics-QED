"""CM-020 exact square-CSL arithmetic regression tests."""
from fractions import Fraction
from math import isclose, pi
from pathlib import Path
import unittest
import yaml

from production_code.euclidean.csl import all_subhundred_cells, csl, complementary_pair, reduced_representative

ROOT = Path(__file__).resolve().parents[2]


class ExactSquareCSLTests(unittest.TestCase):
    def test_ten_site_certificate(self):
        cell = csl(2, 1)
        self.assertEqual((cell.cos_theta, cell.sin_theta), (Fraction(3,5), Fraction(4,5)))
        self.assertEqual((cell.sigma, cell.n_sc), (5, 10))
        self.assertEqual(cell.direct_basis_over_a, ((Fraction(2), Fraction(-1)), (Fraction(1), Fraction(2))))

    def test_thirty_four_site_certificate(self):
        cell = csl(4, 1)
        self.assertEqual((cell.cos_theta, cell.sin_theta), (Fraction(15,17), Fraction(8,17)))
        self.assertEqual((cell.sigma, cell.n_sc), (17, 34))
        self.assertEqual(cell.reciprocal_basis_over_2pi_over_a[0], (Fraction(4,17), Fraction(-1,17)))

    def test_complement_preserves_index(self):
        partner = complementary_pair(2, 1)
        self.assertEqual(partner, (3, 1))
        self.assertEqual(csl(2,1).sigma, csl(*partner).sigma)
        self.assertTrue(isclose(reduced_representative(2,1).theta, pi/2-csl(2,1).theta, abs_tol=2e-15))

    def test_all_seven_subhundred_cells_match_frozen_table(self):
        derived = all_subhundred_cells()
        self.assertEqual([cell.n_sc for cell in derived], [82, 50, 74, 26, 34, 10, 58])
        frozen = yaml.safe_load((ROOT / "production_code/config/euclidean.yaml").read_text(encoding="utf-8"))["production_supercells"]["cells"]
        self.assertEqual([(cell.sigma,cell.n_sc,cell.m,cell.n) for cell in derived], [(row["Sigma"],row["Nsc"],row["m"],row["n"]) for row in frozen])

    def test_cyclic_representatives_have_exact_count(self):
        cell = csl(5, 2)
        self.assertEqual(len(cell.representatives), cell.sigma)
        self.assertEqual(cell.representatives[0], (0,0))
        self.assertEqual(cell.representatives[-1], (cell.sigma-1,0))


if __name__ == "__main__": unittest.main()

