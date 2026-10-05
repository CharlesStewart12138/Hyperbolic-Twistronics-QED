#!/usr/bin/env python3
"""V2 launcher for the shard003 audit's excluded non-LF preexec stdout."""

from pathlib import Path


source_path = Path(__file__).with_name(
    "independent_audit_degree24_c8_seed_shard003_gpt56sol.py"
)
source = source_path.read_text(encoding="ascii")
old = '''    ascii_lines(blob, label, empty_ok=(label == "stdout1"))
    data[label] = blob
'''
new = '''    if label == "failed_preexec_stdout":
        # GAP's excluded pre-execution break-loop prompt ends in ANSI colour
        # state bytes, not LF. Pin its complete physical byte stream rather
        # than weakening the canonical-LF rule for any scientific artifact.
        assert len(blob) == 90
        assert blob == (
            b"you can 'quit;' to quit to outer loop, or\\n"
            b"you can 'return;' to continue\\n"
            b"\\x1b[1m\\x1b[34m\\x1b[0m\\x1b[31m"
        )
        blob.decode("ascii")
    else:
        ascii_lines(blob, label, empty_ok=(label == "stdout1"))
    data[label] = blob
'''
assert source.count(old) == 1
source = source.replace(old, new)
namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(source, str(source_path), "exec"), namespace)
