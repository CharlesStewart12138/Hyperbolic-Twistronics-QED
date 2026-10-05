"""MC-012 exact Euclidean production-model contract.

MANUSCRIPT SOURCE:
Equation: Euclidean comparison and full radial-kernel definitions.
Model scope: production supercell Bloch Hamiltonian.
"""

from collections.abc import Mapping
from numbers import Integral
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-012"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    sigma = contract_value(config, "euclidean.Sigma", RULE_ID)
    dim = contract_value(config, "euclidean.hilbert_dimension", RULE_ID)
    require_contract(isinstance(sigma, Integral) and not isinstance(sigma, bool) and sigma > 0, RULE_ID, "Sigma must be a positive integer")
    require_contract(dim == 2 * sigma, RULE_ID, "production Euclidean Hamiltonian must have dimension 2*Sigma")
    require_contract(contract_value(config, "euclidean.interlayer_Tk", RULE_ID) == "full_radial_nonzero", RULE_ID, "T(k) must be the nonzero full radial interlayer matrix")
    require_contract(contract_value(config, "euclidean.extrema_domain", RULE_ID) == "full_2d_mbz", RULE_ID, "Euclidean extrema require the full 2D mini-Brillouin zone")
    require_contract(contract_value(config, "guards.five_state_in_production", RULE_ID) is False, RULE_ID, "five-state model is validation-only")
    require_contract(contract_value(config, "guards.zero_interlayer_in_production", RULE_ID) is False, RULE_ID, "w=0 is a control, not the production model")
    require_contract(contract_value(config, "validation.namespace_separate", RULE_ID) is True, RULE_ID, "validation outputs must be separately namespaced")

