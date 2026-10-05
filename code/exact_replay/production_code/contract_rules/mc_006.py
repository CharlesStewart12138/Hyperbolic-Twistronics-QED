"""MC-006 continuous-twist fixed-Hilbert-space contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (878)–(914), especially (884), (905)–(909), (914).
Section: Complete twist scan.
Model scope: continuous theta derivatives and target transport.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-006"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Require one fixed fiber for theta derivatives and projector continuation.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (884), (905)–(909), (914).
    Section: Complete twist scan.
    Model scope: continuous hyperbolic twist on a fixed quotient Hilbert space.
    """

    require_contract(contract_value(config, "twist.hilbert_space_policy", RULE_ID) == "fixed_fiber", RULE_ID, "continuous twist requires a fixed Hilbert space")
    require_contract(contract_value(config, "twist.dimension_constant", RULE_ID) is True, RULE_ID, "Hilbert-space dimension must remain constant")
    require_contract(contract_value(config, "twist.geometry_derivative_orders", RULE_ID) == [1, 2], RULE_ID, "first and second geometry derivatives are required")
    require_contract(contract_value(config, "twist.hamiltonian_derivative_orders", RULE_ID) == [1, 2], RULE_ID, "first and second Hamiltonian derivatives are required")
    require_contract(contract_value(config, "twist.projector_transport", RULE_ID) == "riesz_fixed_contour_with_refinement", RULE_ID, "Riesz projector transport is required")
    require_contract(contract_value(config, "twist.signed_internal_coordinate", RULE_ID) is True, RULE_ID, "signed theta must be retained internally")
    require_contract(contract_value(config, "guards.changing_commensurate_dimension", RULE_ID) is False, RULE_ID, "cannot differentiate changing commensurate-cell dimensions")
    require_contract(contract_value(config, "guards.eigenvalue_index_transport", RULE_ID) is False, RULE_ID, "eigenvalue-index transport is forbidden")

