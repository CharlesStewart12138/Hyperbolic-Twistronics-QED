#!/usr/bin/env python3
"""Use recovery-aware minimal closure, then return to the shard controller."""

from pathlib import Path


B = Path(__file__).resolve().parent
base = B / "resume_degree24_c8_seed_shard_then_controller_gpt5.py"
source = base.read_text(encoding="ascii")
old = 'FINALIZER = B / "finalize_degree24_c8_seed_shard_minimal_generic_gpt56sol.py"'
new = 'FINALIZER = B / "finalize_degree24_c8_seed_shard_minimal_recovery_generic_gpt5.py"'
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(base), "__name__": "__main__"}
exec(compile(source, str(base) + "#V2", "exec"), namespace)
