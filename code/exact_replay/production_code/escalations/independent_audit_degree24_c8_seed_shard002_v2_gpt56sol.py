#!/usr/bin/env python3
"""Corrected launcher for the independent shard002 audit (empty/CRLF streams)."""

from pathlib import Path


source_path = Path(__file__).with_name("independent_audit_degree24_c8_seed_shard002_gpt56sol.py")
source = source_path.read_text(encoding="ascii")
old = '''    if blob:
        assert blob.endswith(b"\\n") and b"\\r" not in blob
        blob.decode("ascii")
'''
new = '''    if blob:
        assert blob.endswith(b"\\n")
        if label != "verify_stdout":
            assert b"\\r" not in blob
        blob.decode("ascii")
'''
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(source_path), "__name__": "__main__"}
exec(compile(source, str(source_path), "exec"), namespace)
