"""MC-014 first-shell surface validation contract.

MANUSCRIPT SOURCE:
Equation: w_star/t = 1/q_1.
Model scope: validation/control only.
"""

from collections.abc import Mapping
from math import isclose
from numbers import Real
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-014"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    require_contract(contract_value(config, "run.type", RULE_ID) == "validation", RULE_ID, "first-shell model must be a validation run")
    require_contract(contract_value(config, "run.namespace", RULE_ID) == "validation/first_shell", RULE_ID, "first-shell outputs require a validation namespace")
    q1 = contract_value(config, "analytic.q1", RULE_ID)
    ratio = contract_value(config, "analytic.w_star_over_t", RULE_ID)
    gap = contract_value(config, "analytic.isolation_gap", RULE_ID)
    for value, name in [(q1, "q1"), (ratio, "w_star_over_t"), (gap, "isolation_gap")]:
        require_contract(isinstance(value, Real) and not isinstance(value, bool), RULE_ID, f"{name} must be numeric")
    require_contract(q1 > 0 and ratio > 0, RULE_ID, "the first-shell root must be positive")
    require_contract(isclose(ratio, 1.0 / q1, rel_tol=1e-12, abs_tol=1e-14), RULE_ID, "w_star/t must equal 1/q1")
    require_contract(gap > 0, RULE_ID, "the first-shell control requires a positive isolation gap")
    require_contract(contract_value(config, "guards.production_use", RULE_ID) is False, RULE_ID, "first-shell model cannot enter production")
    require_contract(contract_value(config, "guards.parameter_transfer", RULE_ID) is False, RULE_ID, "first-shell parameters cannot seed production")

