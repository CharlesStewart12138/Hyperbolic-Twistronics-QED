"""Regression tests for MC-010."""

import unittest

from production_code.contract_rules.mc_010 import REQUIRED_OBSERVABLES, check
from production_code.model_contract import ContractViolation


def valid_config():
    return {
        "flatness": {
            "target_reference": "riesz_projector_ancestry",
            "domain": "full_2d_bz",
            "observables": sorted(REQUIRED_OBSERVABLES),
            "weights": {name: 1.0 for name in REQUIRED_OBSERVABLES},
            "thresholds": {name: 0.1 for name in REQUIRED_OBSERVABLES},
            "weights_frozen": True,
            "thresholds_frozen": True,
        },
        "guards": {"bandwidth_only": False, "dos_only": False, "trace_only": False, "path_only": False},
    }


class ModelContractMC010Tests(unittest.TestCase):
    def test_complete_physical_score_passes(self):
        check(valid_config())

    def test_missing_hessian_is_fatal(self):
        config = valid_config()
        config["flatness"]["observables"].remove("principal_hessian_eigenvalues")
        with self.assertRaisesRegex(ContractViolation, "incomplete"):
            check(config)

    def test_bandwidth_only_is_fatal(self):
        config = valid_config()
        config["guards"]["bandwidth_only"] = True
        with self.assertRaisesRegex(ContractViolation, "bandwidth_only"):
            check(config)


if __name__ == "__main__":
    unittest.main()

