"""Model-version and production/validation namespace gate.

MANUSCRIPT SOURCE:
Equation: all equations governed by MC-001--MC-022.
Section: complete current production model and numerical methods.
Model scope: every run before any Hamiltonian construction.
"""

from __future__ import annotations

from collections.abc import Mapping
from hashlib import sha256
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from production_code.model_contract import ContractViolation

RULE_ID = "CM-000"
FORBIDDEN_PRODUCTION_FLAGS = {
    "validation_fixture",
    "first_shell_only",
    "five_state_only",
    "q_val",
}
VALIDATION_ONLY_VALUES = {
    "h_over_a": 0.5,
    "lambda_perp_over_a": 0.125,
    "w_star_over_t": 140.37,
}


def _require(condition: bool, detail: str) -> None:
    if not condition:
        raise ContractViolation(RULE_ID, detail)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_deep_freeze(item) for item in value)
    return value


def _walk(mapping: Mapping[str, Any]):
    for key, value in mapping.items():
        yield str(key), value
        if isinstance(value, Mapping):
            yield from _walk(value)


def _explicit_production_choice(config: Mapping[str, Any], name: str, value: Any) -> bool:
    records = config.get("parameter_provenance", [])
    return any(
        isinstance(record, Mapping)
        and record.get("name") == name
        and record.get("value") == value
        and record.get("explicit_production_choice") is True
        and bool(record.get("freeze_id"))
        for record in records
    )


def validate_run_contract(config: Mapping[str, Any], workspace_root: Path) -> Mapping[str, Any]:
    """Validate source identity and namespace, then return an immutable view.

    MANUSCRIPT SOURCE:
    Equation: all production equations; source identity from PF-GOV-001.
    Section: model governance and validation/production separation.
    Model scope: exact production or explicitly labeled validation run.
    """

    _require(isinstance(config, Mapping), "run configuration must be a mapping")
    run_type = config.get("run_type")
    _require(run_type in {"production", "validation"}, "run_type must be production or validation")
    expected_namespace = f"data/{run_type}"
    _require(config.get("output_namespace") == expected_namespace, f"output_namespace must be {expected_namespace}")

    source = config.get("source_version")
    _require(isinstance(source, Mapping), "source_version is required")
    for kind in ("tex", "pdf"):
        relative = source.get(f"{kind}_path")
        expected = source.get(f"{kind}_sha256")
        _require(isinstance(relative, str) and isinstance(expected, str), f"missing {kind} source identity")
        path = workspace_root / relative
        _require(path.is_file(), f"missing frozen {kind} source: {relative}")
        _require(_digest(path) == expected.lower(), f"frozen {kind} hash mismatch")

    if run_type == "production":
        for key, value in _walk(config):
            normalized = key.lower()
            if normalized in FORBIDDEN_PRODUCTION_FLAGS:
                _require(value is False or value is None, f"validation-only production field: {key}")
            if normalized in VALIDATION_ONLY_VALUES and value == VALIDATION_ONLY_VALUES[normalized]:
                _require(_explicit_production_choice(config, normalized, value), f"validation-only value leaked into production: {key}={value}")
    return _deep_freeze(config)


def load_run_contract(path: Path, workspace_root: Path) -> Mapping[str, Any]:
    """Parse one YAML run configuration and return a validated immutable view."""

    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return validate_run_contract(payload, workspace_root)

