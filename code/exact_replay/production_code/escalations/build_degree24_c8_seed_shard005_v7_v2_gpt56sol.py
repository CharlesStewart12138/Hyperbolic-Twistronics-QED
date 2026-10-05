#!/usr/bin/env python3
"""Correct shard005's frozen first-key alpha endpoint and rebuild uniquely."""

from pathlib import Path


B = Path(__file__).resolve().parent
base = B / "build_degree24_c8_seed_shard005_v7_gpt56sol.py"
source = base.read_text(encoding="ascii")
old = 'ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard005_v7_gpt56sol.g"'
new = 'ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard005_v7_v2_gpt56sol.g"'
assert source.count(old) == 1
source = source.replace(old, new)
old = 'assert (len(work), work[0][:3], work[-1][:3]) == (283, (6769, 91, 108), (7070, 1, 2))'
new = 'assert (len(work), work[0][:3], work[-1][:3]) == (283, (6769, 91, 100), (7070, 1, 2))'
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(base), "__name__": "__main__"}
exec(compile(source, str(base) + "#V2", "exec"), namespace)
