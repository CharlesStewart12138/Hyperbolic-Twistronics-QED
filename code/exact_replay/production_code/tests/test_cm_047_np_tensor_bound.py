import json
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class TensorBoundCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.partial = json.loads((ROOT / "data/production/local_full_kernel/EXACT_BALL6_TENSOR_PARTIAL.json").read_text())
        cls.tail = json.loads((ROOT / "data/production/local_full_kernel/EXACT_BALL6_TENSOR_TAIL.json").read_text())
        cls.cert = json.loads((ROOT / "production_code/hodge/CM_047_NP_TENSOR_BOUND.json").read_text())

    def test_complete_exact_ball_and_orbits(self):
        self.assertEqual(self.partial["dangerous_nonidentity_elements"], 23_129_592)
        self.assertEqual(self.partial["inversion_C8_orbits"], 1_446_488)
        self.assertEqual(self.partial["exact_C8_invariant_orbit_moments"], 1_446_488)

    def test_entrywise_intervals_are_symmetric_and_tight(self):
        lo = [[float(v) for v in row] for row in self.partial["partial_tensor_entrywise_lower"]]
        hi = [[float(v) for v in row] for row in self.partial["partial_tensor_entrywise_upper"]]
        for i in range(4):
            for j in range(4):
                self.assertLessEqual(lo[i][j], hi[i][j])
                self.assertEqual(lo[i][j], lo[j][i])
                self.assertEqual(hi[i][j], hi[j][i])
                self.assertLess(hi[i][j] - lo[i][j], 2e-15)

    def test_midpoint_satisfies_c8_parameterization(self):
        lo = [[float(v) for v in row] for row in self.partial["partial_tensor_entrywise_lower"]]
        hi = [[float(v) for v in row] for row in self.partial["partial_tensor_entrywise_upper"]]
        b = [[0.5 * (lo[i][j] + hi[i][j]) for j in range(4)] for i in range(4)]
        x, y = b[2][3], b[3][3]
        expected = [
            [-4*x+3*y, -3*x+2*y, x-y, -2*x+y],
            [-3*x+2*y, -4*x+3*y, 2*x-y, -x+y],
            [x-y, 2*x-y, y, x],
            [-2*x+y, -x+y, x, y],
        ]
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(b[i][j], expected[i][j], places=14)

    def test_directed_tail_and_integer_envelope(self):
        directed = float(self.tail["coordinate_trace_C2_upper_directed"])
        self.assertLess(directed, 261.0)
        self.assertEqual(self.tail["certified_rational_coordinate_trace_upper"], 261)
        self.assertEqual(self.tail["first_omitted_shell"], 6)

    def test_two_sector_not_scalar(self):
        sectors = self.cert["partial_generalized_coefficients_B_relative_to_C_S"]
        minus = [float(x) for x in sectors["minus_interval"]]
        plus = [float(x) for x in sectors["plus_interval"]]
        self.assertGreater(minus[0], plus[1])
        self.assertFalse(self.cert["scientific_decision"]["single_scalar_q_infinity_authorized"])

    def test_joint_bound_materially_improves_legacy(self):
        result = self.cert["improvement_over_legacy_scalar_envelope"]
        self.assertGreater(float(result["raw_tail_reduction_factor"]), 1700)
        self.assertGreater(float(result["legacy_upper_over_new_common_root_upper"]), 10_000)
        common = [float(x) for x in self.cert["aligned_tensor_zero_condition"]["common_root_necessary_interval"]]
        self.assertTrue(math.isfinite(common[0]) and math.isfinite(common[1]))
        self.assertGreater(common[1], common[0])
        self.assertFalse(self.cert["aligned_tensor_zero_condition"]["common_root_resolved"])


if __name__ == "__main__":
    unittest.main()
