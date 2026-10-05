"""Regression tests for MC-015."""
import unittest
from production_code.contract_rules.mc_015 import REQUIRED_CHECKS, check
from production_code.model_contract import ContractViolation


def valid_config():
    base={"model_hash":"abc","target_id":"C","cutoff_policy":"C2"}
    return {"bulk":{"towers":[dict(base,id="A"),dict(base,id="B")],"certifications":sorted(REQUIRED_CHECKS),"cross_tower_comparison":True},"guards":{"dos_only_evidence":False}}


class ModelContractMC015Tests(unittest.TestCase):
    def test_two_towers_pass(self): check(valid_config())
    def test_one_tower_is_fatal(self):
        c=valid_config(); c["bulk"]["towers"]=c["bulk"]["towers"][:1]
        with self.assertRaisesRegex(ContractViolation,"two towers"): check(c)
    def test_mismatched_model_is_fatal(self):
        c=valid_config(); c["bulk"]["towers"][1]["model_hash"]="other"
        with self.assertRaisesRegex(ContractViolation,"model_hash"): check(c)


if __name__ == "__main__": unittest.main()

