"""MC-004 certified finite-quotient production contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (57), (61)–(75), (84)–(86).
Section: Genus-two regular-octagon/Bolza-surface lattice; finite-cover methods.
Model scope: explicit normal production quotients only.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-004"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Require complete quotient provenance and group/injectivity certificates.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (57), (61)–(63), (68)–(75), (86).
    Section: finite quotient and symmetry construction.
    Model scope: production quotient, never the clean-room validation quotient.
    """

    identifier = contract_value(config, "quotient.identifier", RULE_ID)
    require_contract(isinstance(identifier, str) and bool(identifier.strip()), RULE_ID, "quotient identifier is required")
    require_contract(contract_value(config, "quotient.provenance", RULE_ID) == "production_parameter_freeze", RULE_ID, "quotient provenance is not production-frozen")
    for key in ["normal_subgroup_verified", "generator_images_archived", "multiplication_table_archived", "surface_relation_verified", "right_regular_action_verified", "injectivity_radius_certified"]:
        require_contract(contract_value(config, f"quotient.{key}", RULE_ID) is True, RULE_ID, f"missing quotient certificate: {key}")
    order = contract_value(config, "quotient.order", RULE_ID)
    require_contract(isinstance(order, int) and not isinstance(order, bool) and order > 0, RULE_ID, "quotient order must be a positive integer")
    radius = contract_value(config, "quotient.injectivity_radius", RULE_ID)
    cutoff = contract_value(config, "kernel.cutoff_distance", RULE_ID)
    require_contract(isinstance(radius, (int, float)) and radius > 0, RULE_ID, "certified injectivity radius must be positive")
    require_contract(isinstance(cutoff, (int, float)) and 0 < cutoff < radius, RULE_ID, "production support must satisfy D_c < r_inj")
    c8 = contract_value(config, "quotient.c8_compatible", RULE_ID)
    bipartite = contract_value(config, "quotient.bipartite", RULE_ID)
    require_contract(isinstance(c8, bool) and isinstance(bipartite, bool), RULE_ID, "C8 and bipartite statuses must be explicit booleans")
    if contract_value(config, "claims.c8_exact", RULE_ID):
        require_contract(c8, RULE_ID, "exact C8 claim requires quotient compatibility")
    if contract_value(config, "claims.bipartite_benchmark", RULE_ID):
        require_contract(bipartite, RULE_ID, "bipartite benchmark requires the parity-kernel condition")
    require_contract(contract_value(config, "guards.validation_quotient_reused", RULE_ID) is False, RULE_ID, "validation quotient cannot be reused as production")
    require_contract(contract_value(config, "guards.graph_only_quotient", RULE_ID) is False, RULE_ID, "an adjacency graph without quotient provenance is insufficient")

