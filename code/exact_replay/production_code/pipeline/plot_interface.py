"""Read-only plot interface for verified structured compute outputs.

MANUSCRIPT SOURCE:
Equation: figure specifications consume numerical observables without recomputation.
Section: production figures and numerical methods.
Model scope: plot-only loading; no Hamiltonian, fitting or parameter mutation.
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

RULE_ID = "CM-113"
REQUIRED_METADATA = {"run_id","run_type","model_version","parameters","quotient","sector","errors","units","config_sha256","data"}
ALLOWED_STYLE_KEYS = {"title","xlabel","ylabel","color","linewidth","linestyle","marker","figsize","xscale","yscale","legend","panel_label"}
FORBIDDEN_STYLE_TOKENS = {"fit","filter","threshold","eta","broadening","normalize","hamiltonian","diagonalize","parameter"}


def _require(condition: bool, detail: str) -> None:
    if not condition:
        raise ContractViolation(RULE_ID, detail)


@dataclass(frozen=True)
class LoadedDataset:
    manifest: Mapping[str, Any]
    data: Any
    data_path: Path


def validate_plot_style(style: Mapping[str, Any]) -> Mapping[str, Any]:
    """Permit aesthetics only; reject physics-changing plot arguments."""

    _require(isinstance(style, Mapping), "plot style must be a mapping")
    unknown = set(style) - ALLOWED_STYLE_KEYS
    _require(not unknown, f"non-aesthetic plot option(s): {sorted(unknown)}")
    _require(not any(any(token in key.lower() for token in FORBIDDEN_STYLE_TOKENS) for key in style), "plot style contains a forbidden physics operation")
    return MappingProxyType(dict(style))


def load_plot_dataset(manifest_path: Path) -> LoadedDataset:
    """Verify the CM-111 sidecar and load its data without recomputation."""

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _require(REQUIRED_METADATA.issubset(manifest), "dataset manifest is incomplete")
    data_record = manifest["data"]
    _require(isinstance(data_record, Mapping), "manifest data record must be a mapping")
    filename = data_record.get("file")
    _require(isinstance(filename, str) and Path(filename).name == filename, "data filename must be local to the manifest")
    data_path = manifest_path.parent / filename
    _require(data_path.is_file(), "structured data file is missing")
    _require(sha256(data_path.read_bytes()).hexdigest() == data_record.get("sha256"), "structured data hash mismatch")
    kind = data_record.get("format")
    if kind == "json":
        data = json.loads(data_path.read_text(encoding="utf-8"))
    elif kind == "csv":
        with data_path.open("r", encoding="utf-8", newline="") as handle:
            data = tuple(MappingProxyType(dict(row)) for row in csv.DictReader(handle))
    elif kind == "npz":
        with np.load(data_path, allow_pickle=False) as archive:
            data = MappingProxyType({name: archive[name].copy() for name in archive.files})
    else:
        _require(False, f"unsupported structured data format: {kind}")
    return LoadedDataset(MappingProxyType(manifest), data, data_path)

