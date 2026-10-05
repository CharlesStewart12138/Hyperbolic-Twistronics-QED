"""CM-007 exact exponential-kernel regression tests."""
from math import isclose
import unittest
import numpy as np

from production_code.kernel.radial import chain_derivatives, evaluate


class ExponentialRadialKernelTests(unittest.TestCase):
    def test_vertical_pair_has_exact_amplitude(self):
        result=evaluate(D=0.4,w=2.5,h=0.4,lambda_perp=0.2)
        self.assertEqual(result.value,2.5)
        self.assertEqual(result.first_distance_derivative,-12.5)
        self.assertTrue(isclose(result.second_distance_derivative,62.5,rel_tol=5e-16))

    def test_vector_values_are_full_radial_exponential(self):
        D=np.array([0.5,0.7,1.1]); result=evaluate(D,w=3.0,h=0.5,lambda_perp=0.2)
        self.assertTrue(np.allclose(result.value,3.0*np.exp(-(D-0.5)/0.2),rtol=1e-15,atol=0.0))

    def test_theta_chain_rule_matches_finite_difference(self):
        h,w,decay=0.3,1.7,0.4; D0=0.8; D1=0.2; D2=-0.1
        analytic=chain_derivatives(D0,D1,D2,w,h,decay)
        step=2e-4
        distance=lambda x: D0+D1*x+0.5*D2*x*x
        plus=evaluate(distance(step),w,h,decay).value; zero=evaluate(distance(0.0),w,h,decay).value; minus=evaluate(distance(-step),w,h,decay).value
        self.assertTrue(isclose((plus-minus)/(2*step),analytic.first_derivative,rel_tol=1e-8))
        self.assertTrue(isclose((plus-2*zero+minus)/step**2,analytic.second_derivative,rel_tol=2e-8))

    def test_subvertical_distance_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"D>=h"):
            evaluate(0.2,1.0,0.3,0.1)


if __name__ == "__main__": unittest.main()

