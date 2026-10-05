"""MC-013 square five-state validation-only contract.

MANUSCRIPT SOURCE:
Equation: analytic no-root bound c_square >= 4 sqrt(2) - 5.
Model scope: validation fixture only.
"""

from collections.abc import Mapping
from math import sqrt
from numbers import Real
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-013"
SEVERITY = "CRITICAL"
LOWER_BOUND = 4.0 * sqrt(2.0) - 5.0


def check(config: Mapping[str, Any]) -> None:
    require_contract(contract_value(config, "run.type", RULE_ID) == "validation", RULE_ID, "five-state square control must be a validation run")
    require_contract(contract_value(config, "run.namespace", RULE_ID) == "validation/five_state", RULE_ID, "five-state outputs require the validation/five_state namespace")
    c_square = contract_value(config, "analytic.c_square", RULE_ID)
    require_contract(isinstance(c_square, Real) and not isinstance(c_square, bool), RULE_ID, "c_square must be numeric")
    require_contract(c_square >= LOWER_BOUND, RULE_ID, "square-control no-root bound is violated")
    require_contract(contract_value(config, "analytic.root_exists", RULE_ID) is False, RULE_ID, "the certified square-control result is no root")
    require_contract(contract_value(config, "guards.production_use", RULE_ID) is False, RULE_ID, "five-state square control cannot enter production")
    require_contract(contract_value(config, "guards.parameter_transfer", RULE_ID) is False, RULE_ID, "five-state parameters cannot seed production")

