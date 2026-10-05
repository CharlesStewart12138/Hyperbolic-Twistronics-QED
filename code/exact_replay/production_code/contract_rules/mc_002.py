"""MC-002 exact hyperbolic geometry and paired-cover lift contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (44)–(100), especially (45), (50), (56), (57), (84)–(86), (100).
Section: Genus-two regular-octagon/Bolza-surface lattice; Synthetic hyperbolic twist.
Model scope: exact finite-quotient hyperbolic bilayer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-002"
SEVERITY = "CRITICAL"


def check(config: Mapping[str, Any]) -> None:
    """Reject every non-manuscript production distance prescription.

    MANUSCRIPT SOURCE:
    Equation: Eqs. (45), (84)–(86), and (100).
    Section: Synthetic hyperbolic twist.
    Model scope: paired-cover distance on the declared surface-group quotient.
    """

    require_contract(contract_value(config, "geometry.metric", RULE_ID) == "poincare_disk_exact", RULE_ID, "geometry.metric must be poincare_disk_exact")
    require_contract(contract_value(config, "geometry.distance", RULE_ID) == "hyperbolic_geodesic", RULE_ID, "distance must be hyperbolic geodesic")
    require_contract(contract_value(config, "geometry.twist_action", RULE_ID) == "bolza_isometry_g_theta", RULE_ID, "twist must use the manuscript isometry")
    require_contract(contract_value(config, "geometry.paired_cover_rule", RULE_ID) == "subgroup_lift_minimization", RULE_ID, "paired-cover distance must minimize over subgroup lifts")
    require_contract(contract_value(config, "geometry.lift_invariance_verified", RULE_ID) is True, RULE_ID, "lift invariance must be verified")
    require_contract(contract_value(config, "geometry.local_uniqueness_certified", RULE_ID) is True, RULE_ID, "r_inj > D_c local uniqueness must be certified")
    forbidden = [
        "graph_shortest_path",
        "euclidean_chord",
        "euclidean_minimum_image",
        "same_label_pairing",
        "heuristic_lift_cutoff",
    ]
    active = [name for name in forbidden if contract_value(config, f"guards.{name}", RULE_ID) is not False]
    require_contract(not active, RULE_ID, f"forbidden geometry shortcut(s): {', '.join(active)}")

