"""Deterministic, resumable compute-only run orchestration.

MANUSCRIPT SOURCE:
Equation: all production numerical modules governed by the frozen contract.
Section: production numerical methods.
Model scope: one immutable production reference per run ID; plotting excluded.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from production_code.model_contract import ContractViolation
from production_code.pipeline.config_schema import load_production_reference

RULE_ID = "CM-112"
PLOT_TOKENS = ("plot", "figure", "matplotlib", "seaborn", "render")


def _require(condition: bool, detail: str) -> None:
    if not condition:
        raise ContractViolation(RULE_ID, detail)


@dataclass(frozen=True)
class ComputeStage:
    name: str
    entrypoint: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require(bool(self.name) and all(char.isalnum() or char in "-_" for char in self.name), "stage name must be filesystem-safe")
        lowered = self.entrypoint.lower()
        _require(":" in self.entrypoint and not any(token in lowered for token in PLOT_TOKENS), "compute stage may not contain a plot/figure/render entrypoint")
        _require(self.name not in self.dependencies, "stage cannot depend on itself")


@dataclass(frozen=True)
class RunState:
    run_id: str
    config_sha256: str
    state_path: Path
    output_directory: Path
    stage_order: tuple[str, ...]
    statuses: Mapping[str, str]


def _safe_run_id(run_id: str) -> str:
    _require(bool(run_id) and all(char.isalnum() or char in "-_" for char in run_id), "run_id must be filesystem-safe")
    return run_id


def _validate_stages(stages: tuple[ComputeStage, ...]) -> None:
    names = [stage.name for stage in stages]
    _require(names and len(names) == len(set(names)), "compute stages must be nonempty and uniquely named")
    prior: set[str] = set()
    for stage in stages:
        _require(set(stage.dependencies).issubset(prior), f"stage dependencies must refer to prior stages: {stage.name}")
        prior.add(stage.name)


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _state(payload: dict, state_path: Path, output_directory: Path) -> RunState:
    return RunState(payload["run_id"], payload["config_sha256"], state_path, output_directory, tuple(payload["stage_order"]), {name: payload["stages"][name]["status"] for name in payload["stage_order"]})


def initialize_run(reference_path: Path, workspace_root: Path, run_id: str, stages: tuple[ComputeStage, ...]) -> RunState:
    """Create or resume one run after a fully frozen config passes CM-110."""

    identifier = _safe_run_id(run_id)
    _validate_stages(stages)
    load_production_reference(reference_path, require_ready=True)
    config_hash = sha256(reference_path.read_bytes()).hexdigest()
    state_path = workspace_root / "logs" / f"{identifier}.run_state.json"
    output_directory = workspace_root / "data" / "production" / identifier
    stage_payload = {stage.name: {"entrypoint":stage.entrypoint,"dependencies":list(stage.dependencies),"status":"pending","output_hashes":{}} for stage in stages}
    expected = {"schema_version":1,"run_id":identifier,"config_sha256":config_hash,"stage_order":[stage.name for stage in stages],"stages":stage_payload}
    if state_path.exists():
        existing = json.loads(state_path.read_text(encoding="utf-8"))
        _require(existing["config_sha256"] == config_hash, "run ID is already bound to a different configuration")
        _require(existing["stage_order"] == expected["stage_order"], "resume cannot change the stage graph")
        for name in existing["stage_order"]:
            _require(existing["stages"][name]["entrypoint"] == expected["stages"][name]["entrypoint"], "resume cannot change stage entrypoints")
        return _state(existing, state_path, output_directory)
    output_directory.mkdir(parents=True, exist_ok=False)
    _atomic_json(state_path, expected)
    return _state(expected, state_path, output_directory)


def mark_stage_complete(state_path: Path, stage_name: str, output_hashes: Mapping[str, str]) -> RunState:
    """Atomically complete one stage after dependency and SHA-256 checks."""

    payload = json.loads(state_path.read_text(encoding="utf-8"))
    _require(stage_name in payload["stages"], f"unknown stage: {stage_name}")
    stage = payload["stages"][stage_name]
    _require(stage["status"] == "pending", f"stage is not pending: {stage_name}")
    _require(all(payload["stages"][name]["status"] == "done" for name in stage["dependencies"]), "stage dependencies are incomplete")
    _require(bool(output_hashes), "completed stage requires output hashes")
    _require(all(len(value) == 64 and all(char in "0123456789abcdef" for char in value.lower()) for value in output_hashes.values()), "output hashes must be SHA-256 hex")
    stage["status"] = "done"; stage["output_hashes"] = dict(output_hashes)
    _atomic_json(state_path, payload)
    root = state_path.parent.parent
    return _state(payload, state_path, root/"data"/"production"/payload["run_id"])

