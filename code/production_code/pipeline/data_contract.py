"""Structured numerical dataset and provenance contract.

MANUSCRIPT SOURCE:
Equation: all equations producing numerical observables.
Section: production numerical methods.
Model scope: CSV, JSON and NPZ compute outputs with mandatory metadata.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import numpy as np

from production_code.model_contract import ContractViolation

RULE_ID = "CM-111"


def _require(condition: bool, detail: str) -> None:
    if not condition:
        raise ContractViolation(RULE_ID, detail)


def _freeze_mapping(value: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping) and bool(value), f"{name} metadata must be nonempty")
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class DatasetMetadata:
    run_id: str
    run_type: str
    model_version: Mapping[str, Any]
    parameters: Mapping[str, Any]
    quotient: Mapping[str, Any]
    sector: Mapping[str, Any]
    errors: Mapping[str, Any]
    units: Mapping[str, Any]
    config_sha256: str

    def __post_init__(self) -> None:
        _require(bool(self.run_id) and all(char.isalnum() or char in "-_" for char in self.run_id), "run_id must be filesystem-safe")
        _require(self.run_type in {"production", "validation"}, "run_type must be production or validation")
        _require(len(self.config_sha256) == 64, "config_sha256 must contain 64 hexadecimal characters")
        try:
            int(self.config_sha256, 16)
        except ValueError:
            _require(False, "config_sha256 is not hexadecimal")
        for name in ("model_version", "parameters", "quotient", "sector", "errors", "units"):
            object.__setattr__(self, name, _freeze_mapping(getattr(self, name), name))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "run_id": self.run_id,
            "run_type": self.run_type,
            "model_version": dict(self.model_version),
            "parameters": dict(self.parameters),
            "quotient": dict(self.quotient),
            "sector": dict(self.sector),
            "errors": dict(self.errors),
            "units": dict(self.units),
            "config_sha256": self.config_sha256,
        }


def _output_directory(metadata: DatasetMetadata, output_dir: Path, workspace_root: Path) -> Path:
    allowed = (workspace_root / "data" / metadata.run_type).resolve()
    resolved = output_dir.resolve()
    _require(resolved == allowed or resolved.is_relative_to(allowed), f"dataset must remain under data/{metadata.run_type}")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _write_manifest(metadata: DatasetMetadata, data_path: Path, data_format: str) -> Path:
    payload = metadata.as_dict()
    payload["data"] = {"format": data_format, "file": data_path.name, "sha256": sha256(data_path.read_bytes()).hexdigest()}
    path = data_path.with_suffix(data_path.suffix + ".metadata.json")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def write_json_dataset(data: Any, metadata: DatasetMetadata, output_dir: Path, workspace_root: Path) -> tuple[Path, Path]:
    directory = _output_directory(metadata, output_dir, workspace_root)
    path = directory / f"{metadata.run_id}.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path, _write_manifest(metadata, path, "json")


def write_csv_dataset(rows: list[Mapping[str, Any]], metadata: DatasetMetadata, output_dir: Path, workspace_root: Path) -> tuple[Path, Path]:
    _require(bool(rows), "CSV dataset cannot be empty")
    columns = tuple(rows[0])
    _require(bool(columns) and all(tuple(row) == columns for row in rows), "CSV rows must share one ordered schema")
    directory = _output_directory(metadata, output_dir, workspace_root)
    path = directory / f"{metadata.run_id}.csv"
    temporary = path.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader(); writer.writerows(rows)
    temporary.replace(path)
    return path, _write_manifest(metadata, path, "csv")


def write_npz_dataset(arrays: Mapping[str, Any], metadata: DatasetMetadata, output_dir: Path, workspace_root: Path) -> tuple[Path, Path]:
    _require(isinstance(arrays, Mapping) and bool(arrays), "NPZ arrays must be nonempty")
    directory = _output_directory(metadata, output_dir, workspace_root)
    path = directory / f"{metadata.run_id}.npz"
    temporary = directory / f"{metadata.run_id}.tmp.npz"
    np.savez(temporary, **arrays)
    temporary.replace(path)
    return path, _write_manifest(metadata, path, "npz")

