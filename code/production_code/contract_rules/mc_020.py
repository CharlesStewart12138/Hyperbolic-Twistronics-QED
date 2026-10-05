"""MC-020 full complex-resolvent spectroscopy contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (2733)–(2939).
Model scope: calibrated input-output spectroscopy.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-020"
SEVERITY = "CRITICAL"
DIAGNOSTICS = {"passivity", "poles", "residues", "ldos", "rank"}


def check(config: Mapping[str, Any]) -> None:
    require_contract(contract_value(config, "spectroscopy.greens_formula", RULE_ID) == "[Omega*I-H+i*Gamma/2]^-1", RULE_ID, "full retarded Green function is required")
    require_contract(contract_value(config, "spectroscopy.scattering_formula", RULE_ID) == "I-i*K^dagger*G_R*K", RULE_ID, "full complex scattering matrix is required")
    for key in ["ports_calibrated", "loss_frozen", "frequency_grid_frozen"]:
        require_contract(contract_value(config, f"spectroscopy.{key}", RULE_ID) is True, RULE_ID, f"missing spectroscopy prerequisite: {key}")
    require_contract(contract_value(config, "spectroscopy.gamma_psd_verified", RULE_ID) is True, RULE_ID, "Gamma must be positive semidefinite")
    require_contract(DIAGNOSTICS.issubset(set(contract_value(config, "spectroscopy.diagnostics", RULE_ID))), RULE_ID, "incomplete spectroscopy diagnostics")
    for key in ["scalar_linewidth", "magnitude_only", "unspecified_ports"]:
        require_contract(contract_value(config, f"guards.{key}", RULE_ID) is False, RULE_ID, f"forbidden spectroscopy shortcut: {key}")

