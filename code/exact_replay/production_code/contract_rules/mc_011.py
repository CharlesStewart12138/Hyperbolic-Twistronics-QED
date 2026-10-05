"""MC-011 independent Hodge-pipeline contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (1591)–(1748), (1780)–(1888).
Section: canonical non-Abelian/Hodge diagnostics.
Model scope: diagnostic comparison after independent computation.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-011"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Keep Hodge and physical-flatness pipelines logically independent."""

    require_contract(contract_value(config, "hodge.metric", RULE_ID) == "canonical_G", RULE_ID, "Hodge analysis must use canonical metric G")
    require_contract(contract_value(config, "hodge.principal_components", RULE_ID) == "all", RULE_ID, "all Hodge principal components are required")
    require_contract(contract_value(config, "hodge.pipeline_id", RULE_ID) != contract_value(config, "flatness.pipeline_id", RULE_ID), RULE_ID, "Hodge and flatness pipeline identifiers must differ")
    require_contract(contract_value(config, "hodge.reads_physical_score", RULE_ID) is False, RULE_ID, "Hodge configuration may not read the physical score")
    require_contract(contract_value(config, "flatness.reads_hodge_root", RULE_ID) is False, RULE_ID, "physical flatness may not read the Hodge root")
    require_contract(contract_value(config, "comparison.stage", RULE_ID) == "post_computation", RULE_ID, "Hodge/flatness comparison is allowed only after independent computation")
    require_contract(contract_value(config, "guards.theta_flat_equals_theta_hodge", RULE_ID) is False, RULE_ID, "theta_flat must not be defined as theta_H")

