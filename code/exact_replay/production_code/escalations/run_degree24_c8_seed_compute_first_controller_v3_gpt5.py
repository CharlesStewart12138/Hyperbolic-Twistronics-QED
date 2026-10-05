#!/usr/bin/env python3
"""V2 compute-first controller with native/native shard-builder support."""

from pathlib import Path


B = Path(__file__).resolve().parent
BASE = B / "run_degree24_c8_seed_compute_first_controller_v2_gpt5.py"
source = BASE.read_text(encoding="ascii")

old = 'source = base.read_text(encoding="ascii")'
new = '''source = base.read_text(encoding="ascii")
old_builder = 'BUILDER = B / "build_degree24_c8_seed_shard_generic_v7_gpt56sol.py"'
new_builder = 'BUILDER = B / "build_degree24_c8_seed_shard_generic_v8_gpt5.py"'
if source.count(old_builder) != 1:
    raise RuntimeError("unexpected base controller builder declaration")
source = source.replace(old_builder, new_builder)'''
if source.count(old) != 1:
    raise RuntimeError("unexpected V2 controller template")
source = source.replace(old, new)

namespace = {"__file__": str(BASE), "__name__": "__main__"}
exec(compile(source, str(BASE) + "#V3", "exec"), namespace)
