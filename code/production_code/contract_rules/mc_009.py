"""MC-009 Riesz-projector target-tracking contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (905)–(914), (1566), (1577)–(1582), (1899)–(1901).
Section: Complete twist scan; Full non-Abelian spectrum; fold ancestry.
Model scope: continuous target identity across production scans.
"""

from collections.abc import Mapping
from typing import Any
from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-009"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Require frozen ancestry and strict projector-step continuation.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (905), (909), (914), (1899)–(1901).
    Section: target-projector continuation.
    Model scope: one tracked production target.
    """

    require_contract(contract_value(config, "target.tracking_method", RULE_ID) == "riesz_projector_ancestry", RULE_ID, "tracking must use Riesz projectors and ancestry")
    for key in ["anchor_frozen", "contour_frozen", "rank_frozen", "orbital_ancestry_frozen", "layer_ancestry_frozen", "symmetry_ancestry_frozen", "representation_support_frozen"]:
        require_contract(contract_value(config, f"target.{key}", RULE_ID) is True, RULE_ID, f"missing target freeze: {key}")
    distance = contract_value(config, "target.max_projector_step_norm", RULE_ID)
    error = contract_value(config, "target.projector_error_margin", RULE_ID)
    require_contract(isinstance(distance, (int, float)) and isinstance(error, (int, float)) and error >= 0, RULE_ID, "projector step and error margin must be numeric")
    require_contract(distance + error < 1, RULE_ID, "projector continuation requires ||P_next-P_prev|| plus error margin < 1")
    require_contract(contract_value(config, "target.on_step_failure", RULE_ID) in ["refine_step", "declare_identity_lost"], RULE_ID, "tracking failure must refine or declare identity lost")
    require_contract(contract_value(config, "guards.eigenvalue_sorting", RULE_ID) is False, RULE_ID, "eigenvalue sorting is forbidden")
    require_contract(contract_value(config, "guards.nearest_energy_tracking", RULE_ID) is False, RULE_ID, "nearest-energy tracking is forbidden")

