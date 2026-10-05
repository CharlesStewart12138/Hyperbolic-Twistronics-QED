"""CM-027 exact first-shell validation-control tests."""
from math import isclose
import unittest
import numpy as np

from validation_code.first_shell.first_shell_surface import REGISTERED_Q1, gap_lower_bound, parity_blocks, registered_validation_certificate, root


class FirstShellSurfaceControlTests(unittest.TestCase):
    def test_registered_root_and_gap(self):
        cert = registered_validation_certificate(run_type="validation")
        self.assertTrue(isclose(cert["w_star_over_t"], 140.36861265335298, rel_tol=2e-16))
        self.assertTrue(isclose(cert["g_star_over_t"], 264.73722530670597, rel_tol=2e-16))

    def test_plus_block_is_flat_at_root(self):
        A = np.diag([-8.0, -2.0, 3.0, 8.0])
        w_star = root(1.0, REGISTERED_Q1, run_type="validation")
        plus, minus = parity_blocks(A, 1.0, w_star, REGISTERED_Q1, run_type="validation")
        self.assertTrue(np.allclose(plus, w_star*np.eye(4), rtol=0.0, atol=2e-14))
        self.assertTrue(np.allclose(minus, minus.conj().T, rtol=0.0, atol=0.0))

    def test_gap_requires_strict_isolation(self):
        with self.assertRaisesRegex(ValueError, "not isolated"):
            gap_lower_bound(1.0, 0.2, 8.0, run_type="validation")

    def test_production_namespace_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "validation-only"):
            root(1.0, REGISTERED_Q1, run_type="production")


if __name__ == "__main__": unittest.main()

