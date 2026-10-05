import json
import unittest
from pathlib import Path

from production_code.kernel.pf_ker_005_target_contract import ROOT, build_contract, main


class TargetContractTests(unittest.TestCase):
    def test_fails_closed_without_ex_ante_target(self):
        cert = build_contract()
        self.assertEqual(cert["classification"], "TARGET-CONTRACT-BLOCKED")
        self.assertEqual(cert["status"], "Blocked")
        self.assertIsNone(cert["R_target"]["target_ancestry"]["value"])
        self.assertFalse(cert["circularity_rule"]["target_selection_may_read_final_flatness_result"])

    def test_no_missing_quantity_is_invented(self):
        cert = build_contract()
        required_null = (
            "target_ancestry", "target_contour_C", "target_rank",
            "minimum_isolation_gap_Delta_C", "M1", "M2",
            "C0_acceptance_tolerance", "C1_acceptance_tolerance",
            "C2_acceptance_tolerance", "representation_scope", "cover_scope",
        )
        for key in required_null:
            self.assertIsNone(cert["R_target"][key]["value"], key)

    def test_independent_cutoff_is_retained(self):
        cert = build_contract()
        cutoff = cert["R_target"]["hopping_cutoff"]
        self.assertEqual(cutoff["status"], "FROZEN_INDEPENDENT_CONSTRAINT")
        self.assertEqual(cutoff["value"]["cutoff_over_a"]["primary"], 3)

    def test_derivative_orders_remain_separate_and_unresolved(self):
        cert = build_contract()
        self.assertEqual(cert["derivative_order_acceptance"], {
            "C0": "UNRESOLVED",
            "C1": "UNRESOLVED",
            "C2": "UNRESOLVED",
            "reason": "Per-|w| tail norms cannot be normalized against absent same-scope target margins and tolerances.",
        })
        self.assertFalse(cert["downstream_gates"]["PF_KER_005_derivative_order_closure_released"])

    def test_m6_values_are_immutable_inputs(self):
        cert = build_contract()
        m6 = cert["available_m6_tail_per_abs_w"]
        self.assertEqual(m6["C0"], 0.003856544343098889)
        self.assertEqual(m6["C1_Hodge"], 1.5561304907547204)
        self.assertEqual(m6["C2_Hodge"], 629.7779064951307)

    def test_generated_files_round_trip(self):
        main()
        path = ROOT / "production_code" / "kernel" / "PF_KER_005_TARGET_CONTRACT.json"
        loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(loaded, build_contract())
        self.assertTrue((ROOT / "production_code" / "kernel" / "PF_KER_005_TARGET_CONTRACT.md").exists())


if __name__ == "__main__":
    unittest.main()
