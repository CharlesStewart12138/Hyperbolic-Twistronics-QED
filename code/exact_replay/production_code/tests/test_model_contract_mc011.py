"""Regression tests for MC-011."""
import unittest

from production_code.contract_rules.mc_011 import check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"hodge":{"metric":"canonical_G","principal_components":"all","pipeline_id":"hodge_v1","reads_physical_score":False},"flatness":{"pipeline_id":"flatness_v1","reads_hodge_root":False},"comparison":{"stage":"post_computation"},"guards":{"theta_flat_equals_theta_hodge":False}}


class ModelContractMC011Tests(unittest.TestCase):
    def test_independent_pipelines_pass(self): check(valid_config())
    def test_hodge_reading_score_is_fatal(self):
        c=valid_config(); c["hodge"]["reads_physical_score"]=True
        with self.assertRaisesRegex(ContractViolation,"physical score"): check(c)
    def test_equating_roots_is_fatal(self):
        c=valid_config(); c["guards"]["theta_flat_equals_theta_hodge"]=True
        with self.assertRaisesRegex(ContractViolation,"theta_flat"): check(c)


if __name__ == "__main__": unittest.main()

