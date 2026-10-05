"""MC-019 full-Hamiltonian robustness contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (2466)–(2732).
Model scope: ensemble robustness of the exact production Hamiltonian.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-019"
SEVERITY = "CRITICAL"
PERTURBATIONS = {"disorder", "loss", "detuning", "cutoff", "multimode"}
ORDERS = {"C0", "C1", "C2"}


def check(config: Mapping[str, Any]) -> None:
    require_contract(contract_value(config, "robustness.rebuild_full_hamiltonian_each_sample", RULE_ID) is True, RULE_ID, "each sample must reconstruct the full Hamiltonian")
    require_contract(PERTURBATIONS.issubset(set(contract_value(config, "robustness.perturbations", RULE_ID))), RULE_ID, "incomplete robustness perturbation family")
    require_contract(contract_value(config, "robustness.uniform_loss_separate", RULE_ID) is True, RULE_ID, "uniform loss must be tracked separately")
    require_contract(contract_value(config, "robustness.nonuniform_loss_separate", RULE_ID) is True, RULE_ID, "nonuniform loss must be tracked separately")
    require_contract(ORDERS.issubset(set(contract_value(config, "robustness.derivative_checks", RULE_ID))), RULE_ID, "robustness requires C0/C1/C2 checks")
    for key in ["surrogate_hamiltonian", "scalar_noise_only", "linewidth_postprocessing"]:
        require_contract(contract_value(config, f"guards.{key}", RULE_ID) is False, RULE_ID, f"forbidden robustness shortcut: {key}")

