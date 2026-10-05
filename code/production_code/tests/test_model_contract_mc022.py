"""Regression tests for MC-022."""
import unittest
from production_code.contract_rules.mc_022 import check
from production_code.model_contract import ContractViolation


def valid_config():
    parameter={"name":"t","value":1.0,"units":"energy","allowed_interval":[0.5,1.5],"rationale":"reference hopping","source":"main.tex Eq. 137","freeze_id":"PF-HAM-001"}
    return {"provenance":{"production_parameters":[parameter],"config_immutable":True,"config_hash":"sha256:abc","fail_closed":True,"production_reference_schema_complete":True},"guards":{"code_magic_constants":False,"validation_fixture_values":False,"silent_defaults":False}}


class ModelContractMC022Tests(unittest.TestCase):
    def test_complete_provenance_passes(self): check(valid_config())
    def test_missing_units_is_fatal(self):
        c=valid_config(); c["provenance"]["production_parameters"][0]["units"]=""
        with self.assertRaisesRegex(ContractViolation,"null provenance"): check(c)
    def test_silent_default_is_fatal(self):
        c=valid_config(); c["guards"]["silent_defaults"]=True
        with self.assertRaisesRegex(ContractViolation,"silent_defaults"): check(c)


if __name__ == "__main__": unittest.main()

