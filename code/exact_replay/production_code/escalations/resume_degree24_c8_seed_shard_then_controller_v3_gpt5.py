#!/usr/bin/env python3
"""Recovery-aware shard resume that relaunches the V3 controller."""

from pathlib import Path


B = Path(__file__).resolve().parent
BASE = B / "resume_degree24_c8_seed_shard_then_controller_v2_gpt5.py"
source = BASE.read_text(encoding="ascii")

old = 'source = base.read_text(encoding="ascii")'
new = '''source = base.read_text(encoding="ascii")
old_controller = 'CONTROLLER = B / "run_degree24_c8_seed_compute_first_controller_v2_gpt5.py"'
new_controller = 'CONTROLLER = B / "run_degree24_c8_seed_compute_first_controller_v3_gpt5.py"'
if source.count(old_controller) != 1:
    raise RuntimeError("unexpected base recovery controller declaration")
source = source.replace(old_controller, new_controller)'''
if source.count(old) != 1:
    raise RuntimeError("unexpected V2 recovery template")
source = source.replace(old, new)

namespace = {"__file__": str(BASE), "__name__": "__main__"}
exec(compile(source, str(BASE) + "#V3", "exec"), namespace)
