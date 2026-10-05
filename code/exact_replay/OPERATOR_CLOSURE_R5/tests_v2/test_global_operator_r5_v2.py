from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path


MODULE_DIR = Path(__file__).resolve().parents[1] / "16_IMPLEMENTATION"
sys.path.insert(0, str(MODULE_DIR))
import global_operator_r5 as r5


class R5OperatorTestsV2(unittest.TestCase):
    def test_zero_twist_is_normalizer(self) -> None:
        self.assertEqual(r5.classify_frozen_grid_index(0)["class"], "NORMALIZER")

    def test_all_nonzero_frozen_grid_points_are_generic(self) -> None:
        records = [r5.classify_frozen_grid_index(j) for j in range(1, 91)]
        self.assertTrue(all(x["class"] == "GENERIC_NONCOMMENSURATOR" for x in records))
        self.assertTrue(all(x["real_cyclotomic_degree"] > 2 for x in records))

    def test_known_c8_angle_trace_field_control(self) -> None:
        self.assertEqual(r5.euler_phi(8) // 2, 2)

    def test_generic_fails_closed(self) -> None:
        with self.assertRaises(r5.R5DomainError):
            r5.GLOBAL_INTERLAYER_SUPPORT_R5(
                twist_class=r5.TwistClass.GENERIC_NONCOMMENSURATOR,
                certified_branch_distances={},
                h=Decimal("0.5"), cutoff=Decimal("3"),
                amplitude=Decimal("1"), decay_length=Decimal("0.2"),
            )

    def test_commensurator_not_normalizer_changes_dimension(self) -> None:
        d = r5.common_cover_dimensions(3)
        self.assertEqual(d["bilayer_dimension"], 276_480)
        meta = r5.GLOBAL_OPERATOR_R5(
            twist_class=r5.TwistClass.COMMENSURATOR_NOT_NORMALIZER,
            support=(), correspondence_degree=3,
        )
        self.assertFalse(meta["same_q"])

    def test_ties_preserve_all_branch_ids(self) -> None:
        support = r5.GLOBAL_INTERLAYER_SUPPORT_R5(
            twist_class=r5.TwistClass.COMMENSURATOR_NOT_NORMALIZER,
            certified_branch_distances={(0, 1): (
                r5.BranchDistance("b", Decimal("1")),
                r5.BranchDistance("a", Decimal("1")),
                r5.BranchDistance("c", Decimal("2")),
            )},
            h=Decimal("0.5"), cutoff=Decimal("3"),
            amplitude=Decimal("1"), decay_length=Decimal("0.2"),
        )
        self.assertEqual(support[0].minimizing_branch_ids, ("a", "b"))

    def test_cutoff_boundary_is_included(self) -> None:
        support = r5.GLOBAL_INTERLAYER_SUPPORT_R5(
            twist_class=r5.TwistClass.NORMALIZER,
            certified_branch_distances={(2, 3): (
                r5.BranchDistance("id", Decimal("0")),
            )},
            h=Decimal("0.5"), cutoff=Decimal("0.5"),
            amplitude=Decimal("2"), decay_length=Decimal("0.2"),
        )
        self.assertEqual(len(support), 1)
        self.assertEqual(support[0].coefficient, Decimal("2"))

    def test_inverse_support_is_adjoint_location(self) -> None:
        entry = r5.SupportEntry(1, 7, Decimal("1"), Decimal("0.2"), ("x",))
        inverse = r5.hermitian_inverse_support((entry,))[0]
        self.assertEqual((inverse.row, inverse.column), (7, 1))
        self.assertEqual(inverse.coefficient, entry.coefficient)

    def test_c8_covariance_permutation(self) -> None:
        coefficients = {(0, 0): Decimal(1), (1, 1): Decimal(1)}
        self.assertTrue(r5.check_covariance(coefficients, (1, 0), (1, 0)))
        self.assertFalse(r5.check_covariance(coefficients, (1, 0), (0, 1)))

    def test_representative_relabeling_preserves_candidate_set(self) -> None:
        subgroup = (0, 4)
        distance = lambda x, y: min((x-y) % 8, (y-x) % 8)
        def values(a: int, b: int) -> set[int]:
            return {distance((k+a) % 8, (l+b+1) % 8)
                    for k in subgroup for l in subgroup}
        self.assertEqual(values(1, 2), values(5, 6))


if __name__ == "__main__":
    unittest.main()
