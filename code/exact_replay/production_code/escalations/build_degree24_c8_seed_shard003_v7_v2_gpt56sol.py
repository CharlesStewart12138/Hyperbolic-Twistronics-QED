#!/usr/bin/env python3
"""Corrected launcher for the shard003 V7 builder (sealed first row has 42 classes)."""

from pathlib import Path


source_path = Path(__file__).with_name("build_degree24_c8_seed_shard003_v7_gpt56sol.py")
source = source_path.read_text(encoding="ascii")
old = "(335, (6032, 1, 48), (6440, 1, 2))"
new = "(335, (6032, 1, 42), (6440, 1, 2))"
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(source_path), "__name__": "__main__"}
exec(compile(source, str(source_path), "exec"), namespace)
