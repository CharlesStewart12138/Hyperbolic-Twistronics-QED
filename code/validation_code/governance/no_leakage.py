"""Exact production/validation leakage validation.

MANUSCRIPT SOURCE:
Contract: MC-014 and MC-022.
Section: validation-only reductions and parameter provenance.
Model scope: governance test; this module constructs no physical Hamiltonian.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from production_code.core.model_contract import validate_run_contract
from production_code.model_contract import ContractViolation


def _production_config(workspace_root: Path) -> dict[str, Any]:
    """Return the minimal exact production contract frozen by PF-GOV-001."""

    source = yaml.safe_load(
        (workspace_root / "production_code/config/model.yaml").read_text(encoding="utf-8")
    )["source_version"]
    return {
        "run_type": "production",
        "output_namespace": "data/production",
        "source_version": source,
        "parameters": {},
        "parameter_provenance": [],
    }


def run_validation(workspace_root: Path) -> dict[str, Any]:
    """Exercise every VT-001 forbidden fixture and return exact pass evidence.

    MANUSCRIPT SOURCE:
    Contract: MC-014 forbids reduced fixtures in production; MC-022 requires
    explicit parameter provenance for any re-frozen production coincidence.
    Model scope: exact pass/fail governance validation.
    """

    base = _production_config(workspace_root)
    forbidden = {
        "q_val": "Q_val",
        "validation_fixture": True,
        "first_shell_only": True,
        "five_state_only": True,
        "h_over_a": 0.5,
        "lambda_perp_over_a": 0.125,
        "w_star_over_t": 140.37,
    }
    rejected: list[str] = []
    for name, value in forbidden.items():
        candidate = deepcopy(base)
        candidate["parameters"][name] = value
        try:
            validate_run_contract(candidate, workspace_root)
        except ContractViolation:
            rejected.append(name)
    return {
        "test_id": "VT-001",
        "criterion": "Exact",
        "forbidden_cases": tuple(forbidden),
        "rejected_cases": tuple(rejected),
        "passed": tuple(rejected) == tuple(forbidden),
    }
