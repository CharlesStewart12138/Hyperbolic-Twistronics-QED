"""CM-000 model-version and namespace-gate regression tests."""
from pathlib import Path
from types import MappingProxyType
import unittest
import yaml

from production_code.core.model_contract import validate_run_contract
from production_code.model_contract import ContractViolation

ROOT = Path(__file__).resolve().parents[2]


def base_config():
    source = yaml.safe_load((ROOT / "production_code/config/model.yaml").read_text(encoding="utf-8"))["source_version"]
    return {"run_type":"production","output_namespace":"data/production","source_version":source,"parameters":{"w_over_t":"unfrozen_symbolic"},"parameter_provenance":[]}


class CoreModelContractTests(unittest.TestCase):
    def test_valid_contract_is_deeply_immutable(self):
        frozen = validate_run_contract(base_config(), ROOT)
        self.assertIsInstance(frozen, MappingProxyType)
        with self.assertRaises(TypeError):
            frozen["run_type"] = "validation"

    def test_validation_fixture_is_rejected_in_production(self):
        config = base_config(); config["parameters"]["validation_fixture"] = "Q_val"
        with self.assertRaisesRegex(ContractViolation, "validation-only production field"):
            validate_run_contract(config, ROOT)

    def test_validation_numeric_value_requires_explicit_refreeze(self):
        config = base_config(); config["parameters"]["h_over_a"] = 0.5
        with self.assertRaisesRegex(ContractViolation, "leaked into production"):
            validate_run_contract(config, ROOT)
        config["parameter_provenance"].append({"name":"h_over_a","value":0.5,"freeze_id":"PF-PHY-005","explicit_production_choice":True})
        validate_run_contract(config, ROOT)


if __name__ == "__main__": unittest.main()

