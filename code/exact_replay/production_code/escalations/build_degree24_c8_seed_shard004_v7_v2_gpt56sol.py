#!/usr/bin/env python3
"""Execute the shard004 builder with the corrected pinned source hash."""

from pathlib import Path

source_path = Path(__file__).with_name("build_degree24_c8_seed_shard004_v7_gpt56sol.py")
source = source_path.read_text(encoding="ascii")
old = "285D7245AA84F7F5D09354DD6938F91B9A7F128934A2BD033F7EC0839B9FF106"
new = "FC5DFA877B2B00A44F974F1F9E5344D915A58717C80DE6CE7AB2892AAB2B3863"
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(source_path), "__name__": "__main__"}
exec(compile(source, str(source_path) + "#V2", "exec"), namespace)
