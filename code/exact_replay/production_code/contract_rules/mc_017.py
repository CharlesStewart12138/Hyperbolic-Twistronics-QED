"""MC-017 independent multi-method DOS contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (3572)–(3796).
Model scope: global and projector-resolved density of states.
"""

from collections.abc import Mapping
from numbers import Integral, Real
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-017"
SEVERITY = "CRITICAL"
METHODS = {"exact_finite", "kpm", "slq"}
OUTPUTS = {"global", "target", "layer", "site", "projector", "coherent"}
CHECKS = {"cdf", "sum_rule", "fixed_eta", "p_mass", "spectral_edges"}


def check(config: Mapping[str, Any]) -> None:
    require_contract(METHODS.issubset(set(contract_value(config, "dos.methods", RULE_ID))), RULE_ID, "exact finite, KPM and SLQ DOS are all required")
    require_contract(contract_value(config, "dos.kpm_slq_independent", RULE_ID) is True, RULE_ID, "KPM and SLQ implementations must be independent")
    require_contract(OUTPUTS.issubset(set(contract_value(config, "dos.outputs", RULE_ID))), RULE_ID, "incomplete resolved DOS output set")
    controls = contract_value(config, "dos.controls", RULE_ID)
    require_contract(isinstance(controls, Mapping), RULE_ID, "DOS controls must be a mapping")
    for key in ["kpm_order", "probe_count", "lanczos_depth", "seed", "eta"]:
        require_contract(key in controls and controls[key] is not None, RULE_ID, f"missing DOS control: {key}")
    require_contract(all(isinstance(controls[k], Integral) and not isinstance(controls[k], bool) and controls[k] > 0 for k in ["kpm_order", "probe_count", "lanczos_depth"]), RULE_ID, "DOS integer controls must be positive")
    require_contract(isinstance(controls["eta"], Real) and not isinstance(controls["eta"], bool) and controls["eta"] > 0, RULE_ID, "eta must be positive")
    require_contract(contract_value(config, "dos.controls_frozen", RULE_ID) is True, RULE_ID, "DOS controls must be frozen before production")
    require_contract(CHECKS.issubset(set(contract_value(config, "dos.consistency_checks", RULE_ID))), RULE_ID, "incomplete DOS consistency checks")
    require_contract(contract_value(config, "guards.eta_shopping", RULE_ID) is False, RULE_ID, "eta shopping is forbidden")
    require_contract(contract_value(config, "guards.fixed_eta_unsmoothed_divergence", RULE_ID) is False, RULE_ID, "fixed-eta data cannot establish unsmoothed pointwise divergence")

