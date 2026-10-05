"""MC-008 explicit projector-observable contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (1566), (1577)–(1582).
Section: Full non-Abelian spectrum.
Model scope: representation/projector resolved observables.
"""

from collections.abc import Mapping
from typing import Any
from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-008"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Require explicit matrices and certified Riesz projectors for observables.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (1566), (1577)–(1582).
    Section: Full non-Abelian spectrum.
    Model scope: coherence/Hodge/LDOS/ancestry on the frozen target.
    """

    require_contract(contract_value(config, "projectors.construction", RULE_ID) == "explicit_matrix_riesz", RULE_ID, "projectors must be explicit matrix Riesz projectors")
    for key in ["idempotence_verified", "hermiticity_verified", "rank_verified", "contour_isolated", "representation_resolution_verified"]:
        require_contract(contract_value(config, f"projectors.{key}", RULE_ID) is True, RULE_ID, f"missing projector check: {key}")
    observables = set(contract_value(config, "projectors.observables", RULE_ID))
    require_contract({"coherence", "hodge", "ldos", "ancestry"}.issubset(observables), RULE_ID, "projectors must support coherence, Hodge, LDOS and ancestry")
    require_contract(contract_value(config, "guards.character_only_observables", RULE_ID) is False, RULE_ID, "characters cannot determine projector observables")
    require_contract(contract_value(config, "guards.power_sum_eigenvectors", RULE_ID) is False, RULE_ID, "power sums cannot determine eigenvectors")

