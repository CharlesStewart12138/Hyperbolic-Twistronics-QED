"""MC-016 derivative-order bulk-certification contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (126)–(133), (2033)–(2462).
Model scope: velocity, Hessian/effective-mass and Hodge claims.
"""

from collections.abc import Mapping
from numbers import Real
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-016"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    require_contract(contract_value(config, "derivatives.velocity_topology", RULE_ID) in {"C1", "C2"}, RULE_ID, "velocity claims require at least C1 certification")
    for name in ["hessian_topology", "effective_mass_topology", "hodge_topology"]:
        require_contract(contract_value(config, f"derivatives.{name}", RULE_ID) == "C2", RULE_ID, f"{name} requires C2 certification")
    errors = contract_value(config, "tails.derivative_errors", RULE_ID)
    require_contract(isinstance(errors, Mapping) and set(errors) >= {"C0", "C1", "C2"}, RULE_ID, "independent C0/C1/C2 tail errors are required")
    require_contract(all(isinstance(errors[k], Real) and not isinstance(errors[k], bool) and errors[k] >= 0 for k in ["C0", "C1", "C2"]), RULE_ID, "tail errors must be nonnegative numbers")
    require_contract(len({id(errors[k]) for k in ["C0", "C1", "C2"]}) >= 1, RULE_ID, "derivative-tail errors must be explicitly represented")
    require_contract(contract_value(config, "guards.c0_only_derivative_claim", RULE_ID) is False, RULE_ID, "C0-only evidence cannot support derivative observables")

