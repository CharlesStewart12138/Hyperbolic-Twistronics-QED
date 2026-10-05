"""MC-003 full radial interlayer coupling contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (100)–(103), (126)–(133); baseline law Eq. (101).
Section: Interlayer coupling.
Model scope: full production interlayer matrix on the frozen support.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-003"
SEVERITY = "CRITICAL"
EXACT_KERNEL_FORM = "w*exp(-(D-h)/lambda_perp)"


def check(config: Mapping[str, Any]) -> None:
    """Require the complete all-pair exponential kernel and derivative/tail gates.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (101), (126)–(133).
    Section: Interlayer coupling.
    Model scope: production radial hopping, not a validation shell.
    """

    require_contract(contract_value(config, "kernel.family", RULE_ID) == "exponential_full_distance", RULE_ID, "wrong production kernel family")
    require_contract(contract_value(config, "kernel.formula", RULE_ID) == EXACT_KERNEL_FORM, RULE_ID, "kernel formula does not match Eq. (101)")
    require_contract(contract_value(config, "kernel.pair_policy", RULE_ID) == "all_frozen_support_pairs", RULE_ID, "all allowed site pairs must be enumerated")
    require_contract(contract_value(config, "kernel.support_policy_frozen", RULE_ID) is True, RULE_ID, "support/cutoff policy must be frozen")
    require_contract(contract_value(config, "kernel.theta_derivative_orders", RULE_ID) == [0, 1, 2], RULE_ID, "T, dT/dtheta and d2T/dtheta2 are required")
    require_contract(contract_value(config, "kernel.tail_certificate_orders", RULE_ID) == [0, 1, 2], RULE_ID, "separate C0/C1/C2 tail certificates are required")
    require_contract(contract_value(config, "kernel.parameters_from_frozen_config", RULE_ID) is True, RULE_ID, "kernel parameters must come from frozen config")
    forbidden = ["first_shell_only", "nearest_interlayer_only", "same_label_pairing", "constant_interlayer_coupling"]
    active = [name for name in forbidden if contract_value(config, f"guards.{name}", RULE_ID) is not False]
    require_contract(not active, RULE_ID, f"forbidden interlayer shortcut(s): {', '.join(active)}")

