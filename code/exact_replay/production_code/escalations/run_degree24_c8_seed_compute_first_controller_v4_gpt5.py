#!/usr/bin/env python3
"""V3 controller wrapper selecting the corrected native/native builder."""

from pathlib import Path


B = Path(__file__).resolve().parent
BASE = B / "run_degree24_c8_seed_compute_first_controller_v3_gpt5.py"
source = BASE.read_text(encoding="ascii")
old = 'new_builder = \'BUILDER = B / "build_degree24_c8_seed_shard_generic_v8_gpt5.py"\''
new = 'new_builder = \'BUILDER = B / "build_degree24_c8_seed_shard_generic_v9_gpt5.py"\''
if source.count(old) != 1:
    raise RuntimeError("unexpected V3 builder selection")
source = source.replace(old, new)
namespace = {"__file__": str(BASE), "__name__": "__main__"}
exec(compile(source, str(BASE) + "#V4", "exec"), namespace)
