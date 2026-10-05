#!/usr/bin/env python3
"""Final production entry: require the independent V3 plan audit, then run V5."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
AUDIT = BASE / "DEG24_SPLIT_HEAVY_COVERAGE_INDEPENDENT_AUDIT_V3.json"
V5 = BASE / "run_degree24_split_heavy_repair_controller_v5_gpt5.py"


def load_v5():
    spec = importlib.util.spec_from_file_location("degree24_split_heavy_repair_controller_v5", V5)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V5 repair controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_independent_plan_audit() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    if (
        audit.get("schema") != "DEG24_SPLIT_HEAVY_COVERAGE_INDEPENDENT_AUDIT_V3"
        or audit.get("status") != "PASS"
        or audit.get("affected_keys") != 806
        or audit.get("coverage_missing_count") != 0
        or audit.get("coverage_extra_count") != 0
        or audit.get("coverage_duplicate_count") != 0
        or audit.get("every_class_id_occurs_exactly_once") is not True
        or audit.get("segment_data_matches_class_id_lists") is not True
    ):
        raise ValueError("independent V3 plan audit not PASS")


if __name__ == "__main__":
    validate_independent_plan_audit()
    module = load_v5()
    module.validate_smoke_gate()
    module.load_v4().main()
