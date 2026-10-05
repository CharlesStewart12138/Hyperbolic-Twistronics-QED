#!/usr/bin/env python3
"""Correct V4's nonexistent merged-profile SOLVABLE field and use a new engine file."""

from pathlib import Path

source_path = Path(__file__).with_name("build_degree24_c8_seed_shard004_v7_v4_gpt56sol.py")
source = source_path.read_text(encoding="ascii")
old = 'ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard004_v7_gpt56sol.g"'
new = 'ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard004_v7_v2_gpt56sol.g"'
assert source.count(old) == 1
source = source.replace(old, new)
old = 'assert order == 3072 and p["SOLVABLE"] == "true" and classes > 0 and 1 <= first <= last <= classes'
new = 'assert order == 3072 and classes > 0 and 1 <= first <= last <= classes'
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(source_path), "__name__": "__main__"}
exec(compile(source, str(source_path) + "#V5", "exec"), namespace)
