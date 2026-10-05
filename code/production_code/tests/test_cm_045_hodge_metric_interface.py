import json
from pathlib import Path
import unittest

import sympy as sp

from production_code.hodge.metric import (
    canonical_inverse_square_root,
    canonical_metric,
    certificate,
    generalized_characteristic_polynomial,
    generalized_principal_spectrum,
    hodge_inner,
    hodge_norm_squared,
    normalized_hessian,
    pullback_metric,
    transform_hessian,
)


ROOT = Path(__file__).resolve().parents[2]


class CM045HodgeMetricInterfaceTests(unittest.TestCase):
    def test_exact_metric_and_inverse_sqrt(self):
        root2 = sp.sqrt(2)
        expected = sp.Matrix([
            [root2, root2/2, -root2/2, 0],
            [root2/2, root2, 0, root2/2],
            [-root2/2, 0, root2, root2/2],
            [0, root2/2, root2/2, root2],
        ])
        self.assertEqual(canonical_metric(), expected)
        inverse = sp.Matrix(canonical_inverse_square_root())
        self.assertEqual(sp.simplify(inverse * expected * inverse), sp.eye(4))

    def test_inner_product_and_norm(self):
        u = sp.Matrix([1, 2, -1, 3])
        v = sp.Matrix([0, 1, 4, -2])
        metric = sp.Matrix(canonical_metric())
        self.assertEqual(hodge_inner(u, v), sp.simplify((u.T * metric * v)[0]))
        self.assertTrue(hodge_norm_squared(u).is_positive)

    def test_full_normalization_retains_four_directions(self):
        metric = canonical_metric()
        self.assertEqual(normalized_hessian(metric), sp.eye(4))
        spectrum = generalized_principal_spectrum(sp.eye(4))
        self.assertEqual(len(spectrum), 4)
        self.assertEqual(spectrum, (sp.sqrt(2)-1, sp.sqrt(2)-1, sp.sqrt(2)+1, sp.sqrt(2)+1))

    def test_basis_covariant_characteristic_polynomial(self):
        hessian = sp.diag(1, 2, 4, 7)
        change = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
        original = generalized_characteristic_polynomial(hessian)
        transformed = generalized_characteristic_polynomial(transform_hessian(hessian, change), pullback_metric(change))
        self.assertEqual(sp.simplify(original - transformed), 0)

    def test_invalid_shapes_asymmetry_and_singular_change_rejected(self):
        with self.assertRaises(ValueError):
            normalized_hessian(sp.eye(3))
        bad = sp.eye(4)
        bad[0, 1] = 1
        with self.assertRaises(ValueError):
            normalized_hessian(bad)
        with self.assertRaises(ValueError):
            pullback_metric(sp.zeros(4))

    def test_certificate_and_serialized_claim_boundary(self):
        result = certificate()
        self.assertTrue(result.passed)
        record = json.loads((ROOT / "production_code/hodge/CM_045_HODGE_METRIC_INTERFACE.json").read_text())
        self.assertTrue(record["acceptance"]["passed"])
        self.assertTrue(record["acceptance"]["basis_covariance_exact"])
        self.assertFalse(record["claim_boundary"]["Hodge_root"])
        self.assertFalse(record["claim_boundary"]["main_tex_modified"])


if __name__ == "__main__":
    unittest.main()
