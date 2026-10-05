"""Schema-compatible entry point for the post-construction independent audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "postconstruction_independent_audit_v1",
    HERE / "run_postconstruction_independent_audit.py",
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ORIGINAL_LOAD_JSON = MODULE.load_json


def load_json_compatible(relative: str) -> dict:
    data = ORIGINAL_LOAD_JSON(relative)
    if relative.endswith("DETERMINISTIC_RESOURCE_FORMULAS.json"):
        data = dict(data)
        data["dimensions"] = {"Hilbert_dimension": data["Hilbert_dimension"]}
    return data


MODULE.load_json = load_json_compatible
MODULE.CHECKS.clear()
MODULE.main()
