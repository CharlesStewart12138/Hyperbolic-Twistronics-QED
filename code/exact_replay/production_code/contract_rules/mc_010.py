"""MC-010 physical-flatness observable contract.

MANUSCRIPT SOURCE:
Equation: Eqs. (878)–(914), (1889)–(1907), (3572)–(3796).
Section: target tracking, flatness fold and projector-resolved DOS.
Model scope: full-domain physical flatness of one Riesz-tracked target.
"""

from collections.abc import Mapping
from numbers import Real
from typing import Any

from production_code.model_contract import contract_value, require_contract

RULE_ID = "MC-010"
SEVERITY = "CRITICAL"

REQUIRED_OBSERVABLES = {
    "bandwidth_W_C",
    "isolation_gap_Delta_C",
    "max_group_velocity",
    "principal_hessian_eigenvalues",
    "Lambda_max",
    "target_dos",
    "coherent_dos",
    "projector_coherence",
    "interlayer_hybridization",
    "orbital_layer_symmetry_ancestry",
    "uncertainty",
}


def _positive_mapping(value: Any, name: str) -> None:
    require_contract(isinstance(value, Mapping) and value, RULE_ID, f"{name} must be a nonempty mapping")
    require_contract(
        all(isinstance(v, Real) and not isinstance(v, bool) and v > 0 for v in value.values()),
        RULE_ID,
        f"{name} entries must be positive finite numbers",
    )


def check(config: Mapping[str, Any]) -> None:
    """Require the complete full-domain score and forbid one-number proxies."""

    require_contract(
        contract_value(config, "flatness.target_reference", RULE_ID) == "riesz_projector_ancestry",
        RULE_ID,
        "flatness must use the Riesz-tracked target",
    )
    require_contract(contract_value(config, "flatness.domain", RULE_ID) == "full_2d_bz", RULE_ID, "flatness must be evaluated on the full 2D Brillouin zone")
    observables = set(contract_value(config, "flatness.observables", RULE_ID))
    require_contract(REQUIRED_OBSERVABLES.issubset(observables), RULE_ID, "incomplete physical-flatness observable set")
    _positive_mapping(contract_value(config, "flatness.weights", RULE_ID), "flatness.weights")
    _positive_mapping(contract_value(config, "flatness.thresholds", RULE_ID), "flatness.thresholds")
    require_contract(contract_value(config, "flatness.weights_frozen", RULE_ID) is True, RULE_ID, "flatness weights are not frozen")
    require_contract(contract_value(config, "flatness.thresholds_frozen", RULE_ID) is True, RULE_ID, "flatness thresholds are not frozen")
    for proxy in ["bandwidth_only", "dos_only", "trace_only", "path_only"]:
        require_contract(contract_value(config, f"guards.{proxy}", RULE_ID) is False, RULE_ID, f"forbidden flatness proxy: {proxy}")

