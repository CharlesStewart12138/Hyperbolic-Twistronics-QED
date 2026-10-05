"""MC-022 production parameter-provenance contract.

MANUSCRIPT SOURCE:
Source: authoritative Parameter Freeze and Source Map workbook sheets.
Model scope: every production configuration and executable module.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-022"
SEVERITY = "CRITICAL"
REQUIRED_FIELDS = {"name", "value", "units", "allowed_interval", "rationale", "source", "freeze_id"}


def check(config: Mapping[str, Any]) -> None:
    parameters = contract_value(config, "provenance.production_parameters", RULE_ID)
    require_contract(isinstance(parameters, Sequence) and not isinstance(parameters, (str, bytes)) and parameters, RULE_ID, "production parameter records are required")
    names: list[str] = []
    for index, parameter in enumerate(parameters):
        require_contract(isinstance(parameter, Mapping), RULE_ID, f"parameter record {index} must be a mapping")
        require_contract(REQUIRED_FIELDS.issubset(parameter), RULE_ID, f"parameter record {index} has an incomplete provenance schema")
        require_contract(all(parameter[field] is not None and parameter[field] != "" for field in REQUIRED_FIELDS), RULE_ID, f"parameter record {index} contains a null provenance field")
        interval = parameter["allowed_interval"]
        require_contract(isinstance(interval, Sequence) and not isinstance(interval, (str, bytes)) and len(interval) == 2, RULE_ID, f"parameter {parameter['name']} requires a two-sided allowed interval")
        names.append(str(parameter["name"]))
    require_contract(len(set(names)) == len(names), RULE_ID, "production parameter names must be unique")
    require_contract(contract_value(config, "provenance.config_immutable", RULE_ID) is True, RULE_ID, "production configuration must be immutable")
    require_contract(bool(contract_value(config, "provenance.config_hash", RULE_ID)), RULE_ID, "production configuration hash is required")
    require_contract(contract_value(config, "provenance.fail_closed", RULE_ID) is True, RULE_ID, "configuration loading must fail closed")
    require_contract(contract_value(config, "provenance.production_reference_schema_complete", RULE_ID) is True, RULE_ID, "production_reference schema is incomplete")
    for key in ["code_magic_constants", "validation_fixture_values", "silent_defaults"]:
        require_contract(contract_value(config, f"guards.{key}", RULE_ID) is False, RULE_ID, f"forbidden parameter source: {key}")

