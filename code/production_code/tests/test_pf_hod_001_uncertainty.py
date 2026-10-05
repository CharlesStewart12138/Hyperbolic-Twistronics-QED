"""Deterministic uncertainty-accounting regression for PF-HOD-001."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class HarmonicBasisUncertaintyTests(unittest.TestCase):
    def test_exact_channels_are_zero_and_scope_is_explicit(self):
        payload = json.loads(
            (ROOT / "production_code/hodge/PF_HOD_001_DETERMINISTIC_UNCERTAINTY.json").read_text(encoding="utf-8")
        )
        channels = payload["uncertainty_channels"]
        self.assertEqual(channels["algebraic_roundoff"]["bound"], 0)
        self.assertEqual(channels["period_common_scale"]["effect_on_basis_rank"], 0)
        self.assertEqual(channels["homology_marking"]["bound"], 0)
        self.assertEqual(channels["theta_transport"]["bound"], 0)
        self.assertIn("non-Abelian", channels["scope_systematic"]["excluded"])
        self.assertFalse(payload["finite_quotient_input"])
        self.assertFalse(payload["physical_chain_input"])
        self.assertFalse(payload["main_tex_modified"])


if __name__ == "__main__":
    unittest.main()

