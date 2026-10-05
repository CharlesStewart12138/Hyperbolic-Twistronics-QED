"""Regression tests for MC-013."""
import unittest
from production_code.contract_rules.mc_013 import LOWER_BOUND, check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"run":{"type":"validation","namespace":"validation/five_state"},"analytic":{"c_square":LOWER_BOUND,"root_exists":False},"guards":{"production_use":False,"parameter_transfer":False}}


class ModelContractMC013Tests(unittest.TestCase):
    def test_no_root_validation_passes(self): check(valid_config())
    def test_below_bound_is_fatal(self):
        c=valid_config(); c["analytic"]["c_square"]=LOWER_BOUND-1e-9
        with self.assertRaisesRegex(ContractViolation,"bound"): check(c)
    def test_production_use_is_fatal(self):
        c=valid_config(); c["guards"]["production_use"]=True
        with self.assertRaisesRegex(ContractViolation,"production"): check(c)


if __name__ == "__main__": unittest.main()

