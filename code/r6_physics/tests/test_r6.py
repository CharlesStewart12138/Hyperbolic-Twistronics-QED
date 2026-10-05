from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import aslinearoperator

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "02_OPERATOR_BUILDERS"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(BUILDERS))

from common_cover_loader import certified_theta_c_record, require_physical_common_cover_operator
from demo_reduced import reduced_patch
from green_function import green_entries
from group_inputs import QSTAR_TABLE
from kpm import chebyshev_moments
from local_operator import ScalarBilayerParameters, assert_generic_not_periodic, build_local_bilayer
from matvec import explicit_action_residual
from multiorbital_hamiltonian import FrozenOrbitalModel
from qa import check_qstar_manifest_hash, sparse_hermiticity_defect
from time_evolution import evolve


class R6NumericalContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patch = reduced_patch()
        cls.model = build_local_bilayer(
            cls.patch,
            ScalarBilayerParameters(theta=0.137, omega_over_omega_ref=0.01),
        )

    def test_01_hermiticity(self):
        self.assertLess(sparse_hermiticity_defect(self.model.hamiltonian), 1e-13)

    def test_02_matrix_free_matches_explicit(self):
        self.assertLess(explicit_action_residual(self.model.hamiltonian, aslinearoperator(self.model.hamiltonian)), 1e-14)

    def test_03_theta_zero_agreement(self):
        model = build_local_bilayer(self.patch, ScalarBilayerParameters(theta=0.0, omega_over_omega_ref=0.01))
        defect = model.interlayer - model.interlayer.T
        value = 0.0 if defect.nnz == 0 else float(np.max(np.abs(defect.data)))
        self.assertLess(value, 1e-13)

    def test_04_common_cover_exact_example(self):
        record = certified_theta_c_record()
        self.assertEqual(record.index, 234)
        self.assertEqual(record.bilayer_dimension, 21_565_440)
        self.assertFalse(record.physical_interlayer_matrix_available)
        with self.assertRaises(RuntimeError):
            require_physical_common_cover_operator()

    def test_05_local_operator_norm_sanity(self):
        dense = self.model.hamiltonian.toarray()
        self.assertLessEqual(np.linalg.norm(dense, 2), np.linalg.norm(dense, np.inf) + 1e-10)

    def test_06_kpm_moment_normalization(self):
        dense = self.model.hamiltonian.toarray()
        spectrum = np.linalg.eigvalsh(dense)
        vector = np.eye(dense.shape[0])[0]
        moments = chebyshev_moments(
            self.model.hamiltonian,
            vector,
            12,
            (float(spectrum[0] - 1), float(spectrum[-1] + 1)),
        )
        self.assertLess(abs(moments[0, 0] - 1.0), 1e-14)
        self.assertLessEqual(float(np.max(np.abs(moments))), 1.0 + 1e-10)

    def test_07_time_evolution_norm_conservation(self):
        initial = np.eye(self.model.dimension)[0]
        trace = evolve(self.model.hamiltonian, initial, np.linspace(0, 2, 9))
        self.assertLess(trace.norm_residual, 2e-10)

    def test_08_green_function_symmetry(self):
        values = green_entries(self.model.hamiltonian, 0.1, 0.05, [(0, 2), (2, 0)])
        self.assertLess(abs(values[0] - values[1]), 1e-10)

    def test_09_orbital_and_layer_indexing(self):
        FrozenOrbitalModel().validate()
        n = self.model.sites_per_layer
        self.assertEqual(self.model.hamiltonian[:n, n:].shape, (n, n))
        self.assertEqual(self.model.hamiltonian[n:, :n].shape, (n, n))

    def test_10_r4_hash_when_external_artifact_is_present(self):
        if not QSTAR_TABLE.is_file():
            self.skipTest("large R4 Q* table is intentionally absent from the source-only repository")
        self.assertTrue(check_qstar_manifest_hash()["listed_in_manifest"])

    def test_11_no_generic_periodicization(self):
        with self.assertRaises(ValueError):
            assert_generic_not_periodic("Theta_G", True)
        assert_generic_not_periodic("Theta_G", False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
