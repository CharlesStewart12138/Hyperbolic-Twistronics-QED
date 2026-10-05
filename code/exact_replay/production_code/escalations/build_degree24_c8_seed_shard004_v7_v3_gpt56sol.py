#!/usr/bin/env python3
"""Correct the two V1 header-literal lines, then execute the V2 builder."""

from pathlib import Path

source_path = Path(__file__).with_name("build_degree24_c8_seed_shard004_v7_v2_gpt56sol.py")
source = source_path.read_text(encoding="ascii")
old_name = 'source_path = Path(__file__).with_name("build_degree24_c8_seed_shard004_v7_gpt56sol.py")'
new_name = old_name
assert source.count(old_name) == 1

# V2 executes V1; intercept V1's text after it is loaded and remove the one
# unintended space inside each triple-quoted new_header match literal.
needle = 'source = source.replace(old, new)\nnamespace = {'
injection = '''source = source.replace(old, new)
source = source.replace("\\\\n\\\",' ''' + "'''" + '''", "\\\\n\\\",''' + "'''" + '''")
namespace = {'''
assert source.count(needle) == 1
source = source.replace(needle, injection)
namespace = {"__file__": str(source_path), "__name__": "__main__"}
exec(compile(source, str(source_path) + "#V3", "exec"), namespace)
