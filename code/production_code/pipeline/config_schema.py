"""Typed validation of the frozen production-reference manifest.

MANUSCRIPT SOURCE:
Equation: all production equations through their Parameter Freeze records.
Section: production numerical methods and model governance.
Model scope: complete configuration schema; execution requires every PF row Fixed.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from production_code.model_contract import ContractViolation

RULE_ID = "CM-110"


@dataclass(frozen=True)
class FreezeRecord:
    freeze_id: str
    status: str
    domain: str
    parameter: str
    key: str
    value_ref: str | None
    units: str | None
    allowed_region: str
    rationale: str
    source: str
    owner: str
    downstream_gate: str


@dataclass(frozen=True)
class ProductionReference:
    path: Path
    freeze_status: str
    ready_for_production: bool
    config_files: tuple[Path, ...]
    records: Mapping[str, FreezeRecord]


def _fail(detail: str) -> None:
    raise ContractViolation(RULE_ID, detail)


def _contains_validation_fixture(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(_contains_validation_fixture(key) or _contains_validation_fixture(item) for key, item in value.items())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return any(_contains_validation_fixture(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in ("validation_fixture", "q_val", "first_shell_only", "five_state_only"))
    return False


def load_production_reference(path: Path, *, require_ready: bool = True) -> ProductionReference:
    """Load and validate the complete PF manifest; optionally require every value."""

    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping) or payload.get("run_type") != "production":
        _fail("production_reference must be a production mapping")
    required_ids = payload.get("required_freeze_ids")
    records_raw = payload.get("parameter_freeze")
    if not isinstance(required_ids, list) or not required_ids or not isinstance(records_raw, Mapping):
        _fail("required_freeze_ids and parameter_freeze mapping are mandatory")
    if len(required_ids) != len(set(required_ids)) or set(required_ids) != set(records_raw):
        _fail("parameter_freeze records must match every unique required freeze ID")
    files_raw = payload.get("config_files")
    if not isinstance(files_raw, list) or not files_raw:
        _fail("config_files list is mandatory")
    config_files = tuple(path.parent / str(name) for name in files_raw)
    missing_files = [file.name for file in config_files if not file.is_file()]
    if missing_files:
        _fail(f"missing configuration fragment(s): {missing_files}")

    records: dict[str, FreezeRecord] = {}
    fields = set(FreezeRecord.__dataclass_fields__)
    for freeze_id in required_ids:
        raw = records_raw[freeze_id]
        if not isinstance(raw, Mapping) or not fields.issubset(raw):
            _fail(f"incomplete parameter record: {freeze_id}")
        if raw["freeze_id"] != freeze_id:
            _fail(f"freeze ID mismatch: {freeze_id}")
        records[freeze_id] = FreezeRecord(**{field: raw[field] for field in fields})

    if _contains_validation_fixture(payload):
        _fail("validation fixture token found in production reference")
    ready = payload.get("ready_for_production") is True and payload.get("freeze_status") == "frozen"
    unresolved = [record.freeze_id for record in records.values() if record.status != "Fixed" or not record.value_ref or not record.units]
    if require_ready and (not ready or unresolved):
        _fail(f"production reference is not frozen; unresolved={unresolved}")
    return ProductionReference(path, str(payload.get("freeze_status")), bool(payload.get("ready_for_production")), config_files, MappingProxyType(records))

