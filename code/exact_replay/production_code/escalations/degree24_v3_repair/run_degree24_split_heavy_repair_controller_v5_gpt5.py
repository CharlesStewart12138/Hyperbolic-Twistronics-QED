#!/usr/bin/env python3
"""Launch V4 binary-safe repair only after the checkpoint/resume smoke gate passes."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
SMOKE_CERT = BASE / "DEG24_SPLIT_HEAVY_ENGINE_CHECKPOINT_RESUME_SMOKE_V3.json"
V4 = BASE / "run_degree24_split_heavy_repair_controller_v4_gpt5.py"


def load_v4():
    spec = importlib.util.spec_from_file_location("degree24_split_heavy_repair_controller_v4", V4)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V4 repair controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_smoke_gate() -> None:
    certificate = json.loads(SMOKE_CERT.read_text(encoding="utf-8"))
    if (
        certificate.get("schema") != "DEG24_SPLIT_HEAVY_ENGINE_CHECKPOINT_RESUME_SMOKE_V3"
        or certificate.get("status") != "PASS"
        or certificate.get("coverage_missing_count") != 0
        or certificate.get("coverage_duplicate_count") != 0
        or certificate.get("expected_class_ids") != certificate.get("observed_class_ids")
    ):
        raise ValueError("CLASS_ID checkpoint/resume smoke gate not PASS")


if __name__ == "__main__":
    validate_smoke_gate()
    load_v4().main()
