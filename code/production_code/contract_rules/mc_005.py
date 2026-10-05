"""MC-005 curvature-scan scope contract.

MANUSCRIPT SOURCE:
Equation: Eq. (166) and parameter-space Eqs. (192), (197), (203).
Section: Parameter space and controlled comparison protocols.
Model scope: exact Bolza endpoint plus declared synthetic metric deformations.
"""

from collections.abc import Mapping
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-005"
SEVERITY = "HIGH"


def check(config: Mapping[str, Any]) -> None:
    """Enforce curvature-coordinate and intermediate-point provenance.

    MANUSCRIPT SOURCE:
    Equation: Eq. (166).
    Section: Parameter space and controlled comparison protocols.
    Model scope: curvature comparison on a fixed declared construction.
    """

    require_contract(contract_value(config, "scan.curvature.coordinate", RULE_ID) == "kappa=-K=1/R^2", RULE_ID, "use one canonical curvature coordinate")
    require_contract(contract_value(config, "scan.curvature.domain", RULE_ID) == [0, "kappa_B"], RULE_ID, "curvature domain must include flat and Bolza endpoints")
    require_contract(contract_value(config, "scan.curvature.bolza_endpoint_exact", RULE_ID) is True, RULE_ID, "Bolza endpoint must be exact")
    require_contract(contract_value(config, "scan.curvature.interior_scope", RULE_ID) == "synthetic_metric_deformation", RULE_ID, "interior curvature points require synthetic-deformation scope")
    require_contract(contract_value(config, "scan.curvature.grid_frozen_before_results", RULE_ID) is True, RULE_ID, "curvature grid must be frozen before results")
    require_contract(contract_value(config, "guards.every_curvature_exact_bolza", RULE_ID) is False, RULE_ID, "intermediate points cannot be called exact Bolza lattices")
    require_contract(contract_value(config, "guards.posthoc_curvature_grid", RULE_ID) is False, RULE_ID, "post-hoc curvature-grid changes are forbidden")

