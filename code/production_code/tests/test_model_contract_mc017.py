"""Regression tests for MC-017."""
import unittest
from production_code.contract_rules.mc_017 import CHECKS, METHODS, OUTPUTS, check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"dos":{"methods":sorted(METHODS),"kpm_slq_independent":True,"outputs":sorted(OUTPUTS),"controls":{"kpm_order":100,"probe_count":16,"lanczos_depth":64,"seed":7,"eta":0.02},"controls_frozen":True,"consistency_checks":sorted(CHECKS)},"guards":{"eta_shopping":False,"fixed_eta_unsmoothed_divergence":False}}


class ModelContractMC017Tests(unittest.TestCase):
    def test_complete_dos_pipeline_passes(self): check(valid_config())
    def test_missing_slq_is_fatal(self):
        c=valid_config(); c["dos"]["methods"].remove("slq")
        with self.assertRaisesRegex(ContractViolation,"SLQ"): check(c)
    def test_eta_shopping_is_fatal(self):
        c=valid_config(); c["guards"]["eta_shopping"]=True
        with self.assertRaisesRegex(ContractViolation,"eta shopping"): check(c)


if __name__ == "__main__": unittest.main()

