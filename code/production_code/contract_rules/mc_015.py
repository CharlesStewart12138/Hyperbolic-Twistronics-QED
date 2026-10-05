"""MC-015 finite-cover bulk-certification contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (2033)–(2462).
Model scope: strong bulk claims from two inequivalent residual towers.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-015"
SEVERITY = "CRITICAL"
REQUIRED_CHECKS = {"no_loss", "no_pollution", "spectral_edges", "gaps", "projectors"}


def check(config: Mapping[str, Any]) -> None:
    towers = contract_value(config, "bulk.towers", RULE_ID)
    require_contract(isinstance(towers, Sequence) and not isinstance(towers, (str, bytes)) and len(towers) >= 2, RULE_ID, "at least two towers are required")
    ids = [tower.get("id") for tower in towers if isinstance(tower, Mapping)]
    require_contract(len(ids) == len(towers) and len(set(ids)) == len(ids), RULE_ID, "bulk towers must be inequivalent and explicitly identified")
    for key in ["model_hash", "target_id", "cutoff_policy"]:
        values = {tower.get(key) for tower in towers}
        require_contract(None not in values and len(values) == 1, RULE_ID, f"all towers must share {key}")
    checks = set(contract_value(config, "bulk.certifications", RULE_ID))
    require_contract(REQUIRED_CHECKS.issubset(checks), RULE_ID, "incomplete no-loss/no-pollution cross-tower certification")
    require_contract(contract_value(config, "bulk.cross_tower_comparison", RULE_ID) is True, RULE_ID, "cross-tower comparison is required")
    require_contract(contract_value(config, "guards.dos_only_evidence", RULE_ID) is False, RULE_ID, "DOS-only evidence is insufficient for a bulk claim")

