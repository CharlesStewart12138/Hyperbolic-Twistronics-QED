"""MC-021 full photonic-resolvent qubit contract.

MANUSCRIPT SOURCE:
Equation: Sigma_q^R = V_q G_gamma^R V_q^dagger.
Model scope: resolvent-mediated qubit interactions and decay.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-021"
SEVERITY = "CRITICAL"
FROZEN_INPUTS = {"sites", "frequencies", "anharmonicities", "couplings", "loss"}


def check(config: Mapping[str, Any]) -> None:
    require_contract(contract_value(config, "qubit.self_energy_formula", RULE_ID) == "V_q*G_gamma_R*V_q^dagger", RULE_ID, "qubit self-energy must use the full photonic resolvent")
    require_contract(contract_value(config, "qubit.target_projection_after_remainder_bound", RULE_ID) is True, RULE_ID, "target projection is allowed only after a remainder bound")
    require_contract(FROZEN_INPUTS.issubset(set(contract_value(config, "qubit.frozen_inputs", RULE_ID))), RULE_ID, "incomplete frozen qubit inputs")
    require_contract(contract_value(config, "qubit.dispersive_margins_verified", RULE_ID) is True, RULE_ID, "dispersive margins must be verified")
    require_contract(contract_value(config, "qubit.gamma_mediated_psd_verified", RULE_ID) is True, RULE_ID, "mediated decay matrix must be positive semidefinite")
    for key in ["target_only_self_energy", "scalar_g", "unresolved_poles"]:
        require_contract(contract_value(config, f"guards.{key}", RULE_ID) is False, RULE_ID, f"forbidden qubit shortcut: {key}")

