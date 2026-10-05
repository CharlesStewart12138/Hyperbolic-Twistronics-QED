"""MC-007 representation-complete spectrum contract.

MANUSCRIPT SOURCE:
Equation: Theorem 8 and Eqs. (1539), (1547), (1551)–(1597).
Section: Full non-Abelian spectrum.
Model scope: every inequivalent irrep of the frozen finite quotient.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-007"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Require exact irrep completeness, multiplicities, weights and spectrum closure.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (1539), (1547), (1551), (1557).
    Section: Full non-Abelian spectrum.
    Model scope: complete regular representation, not selected sectors.
    """

    order = contract_value(config, "quotient.order", RULE_ID)
    dims = contract_value(config, "representation.irrep_dimensions", RULE_ID)
    require_contract(isinstance(dims, list) and dims and all(isinstance(d, int) and d > 0 for d in dims), RULE_ID, "positive irrep dimensions are required")
    require_contract(sum(d * d for d in dims) == order, RULE_ID, "sum d_rho^2 must equal |Q_N|")
    require_contract(contract_value(config, "representation.every_inequivalent_irrep", RULE_ID) is True, RULE_ID, "every inequivalent irrep is required")
    require_contract(contract_value(config, "representation.explicit_matrices", RULE_ID) is True, RULE_ID, "explicit rho(g) matrices are required")
    require_contract(contract_value(config, "representation.regular_multiplicity_rule", RULE_ID) == "d_rho", RULE_ID, "regular multiplicity must equal d_rho")
    require_contract(contract_value(config, "representation.normalized_weight_rule", RULE_ID) == "d_rho^2/|Q_N|", RULE_ID, "normalized weights must be d_rho^2/|Q_N|")
    require_contract(contract_value(config, "representation.character_gram_verified", RULE_ID) is True, RULE_ID, "character Gram test must pass")
    require_contract(contract_value(config, "representation.direct_block_spectrum_verified", RULE_ID) is True, RULE_ID, "direct regular spectrum must equal the weighted block union")
    for key in ["abelian_only_as_full", "character_only_projectors", "selected_irreps_only", "equal_irrep_weighting"]:
        require_contract(contract_value(config, f"guards.{key}", RULE_ID) is False, RULE_ID, f"forbidden representation shortcut: {key}")

