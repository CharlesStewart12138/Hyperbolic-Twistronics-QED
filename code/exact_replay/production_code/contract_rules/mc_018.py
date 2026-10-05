"""MC-018 certified fold-point contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (1889)–(1907).
Model scope: interval-certified interior folds of a tracked branch.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-018"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    outcome = contract_value(config, "fold.outcome", RULE_ID)
    require_contract(outcome in {"certified_fold", "no_certified_fold"}, RULE_ID, "fold outcome must be explicit")
    require_contract(contract_value(config, "guards.grid_minimum_as_fold", RULE_ID) is False, RULE_ID, "a grid minimum is not a certified fold")
    require_contract(contract_value(config, "guards.endpoint_as_fold", RULE_ID) is False, RULE_ID, "an endpoint extremum is not a certified interior fold")
    if outcome == "no_certified_fold":
        require_contract(bool(contract_value(config, "fold.failure_certificate", RULE_ID)), RULE_ID, "no-fold outcome requires a recorded certificate")
        return
    for key in ["same_point_F_zero", "same_point_dtheta_F_zero", "nonzero_dkappa_F", "nonzero_dtheta2_F", "interval_newton_unique", "branch_ancestry_verified", "interior_margins_verified", "square_root_law_verified"]:
        require_contract(contract_value(config, f"fold.{key}", RULE_ID) is True, RULE_ID, f"missing fold certificate: {key}")

