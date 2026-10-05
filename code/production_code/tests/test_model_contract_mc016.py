"""Regression tests for MC-016."""
import unittest
from production_code.contract_rules.mc_016 import check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"derivatives":{"velocity_topology":"C1","hessian_topology":"C2","effective_mass_topology":"C2","hodge_topology":"C2"},"tails":{"derivative_errors":{"C0":0.01,"C1":0.02,"C2":0.03}},"guards":{"c0_only_derivative_claim":False}}


class ModelContractMC016Tests(unittest.TestCase):
    def test_order_matched_certification_passes(self): check(valid_config())
    def test_velocity_c0_is_fatal(self):
        c=valid_config(); c["derivatives"]["velocity_topology"]="C0"
        with self.assertRaisesRegex(ContractViolation,"C1"): check(c)
    def test_missing_c2_tail_is_fatal(self):
        c=valid_config(); del c["tails"]["derivative_errors"]["C2"]
        with self.assertRaisesRegex(ContractViolation,"C0/C1/C2"): check(c)


if __name__ == "__main__": unittest.main()

