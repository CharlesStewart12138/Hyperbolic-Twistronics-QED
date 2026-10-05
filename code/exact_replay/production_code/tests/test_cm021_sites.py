"""CM-021 layer-resolved Euclidean basis tests."""
from fractions import Fraction
import unittest

from production_code.euclidean.csl import csl
from production_code.euclidean.sites import bilayer_basis, layer_sites


class EuclideanLayerSiteTests(unittest.TestCase):
    def test_exact_sigma_sites_per_layer(self):
        for pair in [(3,1),(4,1),(9,1)]:
            cell=csl(*pair)
            self.assertEqual(len(layer_sites(cell,1)),cell.sigma)
            self.assertEqual(len(layer_sites(cell,2)),cell.sigma)
            self.assertEqual(len(bilayer_basis(cell)),2*cell.sigma)

    def test_rotated_coordinates_are_exact_rationals(self):
        cell=csl(4,1); second=layer_sites(cell,2)
        self.assertEqual(second[1].coordinate_over_a,(Fraction(15,17),Fraction(8,17)))

    def test_coincident_origin_keeps_two_layer_labels(self):
        basis=bilayer_basis(csl(3,1))
        origins=[site for site in basis if site.coordinate_over_a==(0,0)]
        self.assertEqual(len(origins),2)
        self.assertEqual({site.layer for site in origins},{1,2})
        self.assertNotEqual(origins[0],origins[1])

    def test_basis_order_is_layer_then_class(self):
        cell=csl(5,2); basis=bilayer_basis(cell)
        self.assertTrue(all(site.layer==1 for site in basis[:cell.sigma]))
        self.assertTrue(all(site.layer==2 for site in basis[cell.sigma:]))


if __name__ == "__main__": unittest.main()

