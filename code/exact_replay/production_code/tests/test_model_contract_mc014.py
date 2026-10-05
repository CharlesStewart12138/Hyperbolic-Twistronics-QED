"""Regression tests for MC-014."""
import unittest
from production_code.contract_rules.mc_014 import check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"run":{"type":"validation","namespace":"validation/first_shell"},"analytic":{"q1":4.0,"w_star_over_t":0.25,"isolation_gap":0.1},"guards":{"production_use":False,"parameter_transfer":False}}


class ModelContractMC014Tests(unittest.TestCase):
    def test_positive_root_control_passes(self): check(valid_config())
    def test_wrong_root_is_fatal(self):
        c=valid_config(); c["analytic"]["w_star_over_t"]=0.3
        with self.assertRaisesRegex(ContractViolation,"1/q1"): check(c)
    def test_closed_gap_is_fatal(self):
        c=valid_config(); c["analytic"]["isolation_gap"]=0.0
        with self.assertRaisesRegex(ContractViolation,"positive isolation"): check(c)


if __name__ == "__main__": unittest.main()

