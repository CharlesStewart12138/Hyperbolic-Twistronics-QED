"""Fail-closed exact-model contract for every production run.

MANUSCRIPT SOURCE:
Equation: Eq. (137), label ``eq:platform-complete-one-particle-hamiltonian``.
Section: Complete Hamiltonian.
Model scope: exact finite-quotient hyperbolic bilayer; validation fixtures are excluded.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Any


EXACT_HYPERBOLIC_BLOCK_FORM = (
    "omega0*I_2N + [[-t*A_N,T_N(theta)],"
    "[T_N(theta)^dagger,-t*A_N]]"
)


@dataclass(frozen=True)
class ContractViolation(ValueError):
    """A fatal production-contract violation."""

    rule_id: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule_id}: {self.detail}"


def _at(config: Mapping[str, Any], dotted_key: str) -> Any:
    value: Any = config
    for key in dotted_key.split("."):
        if not isinstance(value, Mapping) or key not in value:
            raise ContractViolation("MC-001", f"missing required key: {dotted_key}")
        value = value[key]
    return value


def _require(condition: bool, detail: str) -> None:
    if not condition:
        raise ContractViolation("MC-001", detail)


def contract_value(config: Mapping[str, Any], dotted_key: str, rule_id: str) -> Any:
    """Return a required nested contract value or raise for the named rule."""

    value: Any = config
    for key in dotted_key.split("."):
        if not isinstance(value, Mapping) or key not in value:
            raise ContractViolation(rule_id, f"missing required key: {dotted_key}")
        value = value[key]
    return value


def require_contract(condition: bool, rule_id: str, detail: str) -> None:
    """Raise a rule-specific fatal contract violation when condition is false."""

    if not condition:
        raise ContractViolation(rule_id, detail)


def check_mc_001(config: Mapping[str, Any]) -> None:
    """Validate the complete production Hamiltonian block contract.

    MANUSCRIPT SOURCE:
    Equation: Eq. (137), ``eq:platform-complete-one-particle-hamiltonian``.
    Section: Complete Hamiltonian.
    Model scope: production finite quotient with two N-site layers.
    """

    _require(_at(config, "run_type") == "production", "run_type must be production")
    _require(_at(config, "model.kind") == "exact_finite_quotient_hyperbolic_bilayer", "wrong model kind")
    _require(_at(config, "model.layers") == 2, "the exact bilayer has two layers")
    _require(_at(config, "model.orbitals_per_site") == 1, "the declared model has one orbital per site")

    order = _at(config, "quotient.order")
    _require(isinstance(order, int) and not isinstance(order, bool) and order > 0, "quotient.order must be a positive integer")
    _require(_at(config, "hamiltonian.dimension") == 2 * order, "Hamiltonian dimension must equal 2*quotient.order")
    _require(_at(config, "hamiltonian.intralayer_block_shape") == [order, order], "A_N block must have shape N x N")
    _require(_at(config, "hamiltonian.interlayer_block_shape") == [order, order], "T_N(theta) block must have shape N x N")
    _require(_at(config, "hamiltonian.block_form") == EXACT_HYPERBOLIC_BLOCK_FORM, "block form does not match Eq. (137)")
    _require(_at(config, "hamiltonian.hermiticity_verified") is True, "Hermiticity must be verified before production")

    forbidden = {
        "validation_fixture": _at(config, "guards.validation_fixture"),
        "first_shell_only": _at(config, "guards.first_shell_only"),
        "toy_2x2": _at(config, "guards.toy_2x2"),
        "scalar_self_energy": _at(config, "guards.scalar_self_energy"),
    }
    enabled = [name for name, value in forbidden.items() if value is not False]
    _require(not enabled, f"forbidden production shortcut(s): {', '.join(enabled)}")


def assert_production_contract(config: Mapping[str, Any]) -> None:
    """Run every registered CRITICAL production gate and fail on first violation.

    MANUSCRIPT SOURCE:
    Equation: all equations registered in ``MODEL_CONTRACT.md``.
    Section: complete current manuscript production model.
    Model scope: production only; never a validation fixture.
    """

    if not isinstance(config, Mapping):
        raise ContractViolation("MC-001", "configuration must be a mapping")
    check_mc_001(config)
    rules_path = Path(__file__).with_name("contract_rules")
    for module_info in sorted(iter_modules([str(rules_path)]), key=lambda item: item.name):
        if not module_info.name.startswith("mc_"):
            continue
        module = import_module(f"production_code.contract_rules.{module_info.name}")
        if getattr(module, "SEVERITY", None) == "CRITICAL":
            module.check(config)

