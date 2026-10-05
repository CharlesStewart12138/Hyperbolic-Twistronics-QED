#!/usr/bin/env python3
"""Correct V1's post-prefix parser and execute the shard003 recovery build."""

from __future__ import annotations

import os
from pathlib import Path


B = Path(__file__).resolve().parent


def atomic_copy(source: Path, destination: Path) -> None:
    data = source.read_bytes()
    temp = destination.with_name(destination.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, destination)
    assert not temp.exists() and destination.read_bytes() == data


# Preserve the executed V1 parser failure under explicit FAILED_V1 names.
for stem in ("STDOUT", "STDERR"):
    source = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_BUILD_{stem}_V7_GPT56SOL.txt"
    destination = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_BUILD_{stem}_FAILED_V1_GPT56SOL.txt"
    atomic_copy(source, destination)

base_path = B / "build_degree24_c8_seed_shard003_segment002_recovery_v7_gpt56sol.py"
source = base_path.read_text(encoding="ascii")
source = source.replace(
    'PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNCOMMITTED_OUTPUT_SUFFIX_UNIT8090_GPT56SOL.txt"',
    'PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_POSTPREFIX_SUFFIX_COMMIT8089_UNCOMMITTED8090_GPT56SOL.txt"',
)
old = '''suffix_lines = suffix.decode("ascii").splitlines()
assert len(suffix_lines) == 1
assert suffix_lines[0].startswith("ALPHA_DONE\\tUNIT\\t8090\\tKEY\\t24T6257\\tALPHA\\t16\\t")
assert "\\tCUM_UNITS\\t8090\\t" in suffix_lines[0]
assert "\\tNEXT_UNIT\\t8091\\t" in suffix_lines[0]
assert "\\tPREVIOUS_CHECKPOINT_SHA256\\t" + CP_SHA + "\\t" in suffix_lines[0]
'''
new = '''suffix_lines = suffix.decode("ascii").splitlines()
assert len(suffix_lines) == 2
assert suffix_lines[0] == (
    "CHECKPOINT_COMMITTED\\tUNIT\\t8089\\tCHECKPOINT_SHA256\\t" + CP_SHA
    + "\\tOUTPUT_PREFIX_BYTES\\t6148317\\tOUTPUT_PREFIX_SHA256\\t" + PREFIX_SHA
)
assert suffix_lines[1].startswith("ALPHA_DONE\\tUNIT\\t8090\\tKEY\\t24T6257\\tALPHA\\t16\\t")
assert "\\tCUM_UNITS\\t8090\\t" in suffix_lines[1]
assert "\\tNEXT_UNIT\\t8091\\t" in suffix_lines[1]
assert "\\tPREVIOUS_CHECKPOINT_SHA256\\t" + CP_SHA + "\\t" in suffix_lines[1]
'''
assert source.count(old) == 1
source = source.replace(old, new)
old = '''    f"UNCOMMITTED_SUFFIX\\t{PRESERVED_SUFFIX.name}\\tBYTES\\t{len(suffix)}\\tSHA256\\t{digest(suffix).upper()}\\tRECORD\\tALPHA_DONE_UNIT8090_24T6257_ALPHA16\\n"
'''
new = '''    f"POSTPREFIX_SUFFIX\\t{PRESERVED_SUFFIX.name}\\tBYTES\\t{len(suffix)}\\tSHA256\\t{digest(suffix).upper()}\\tRECORDS\\tCOMMITTED_UNIT8089_THEN_UNCOMMITTED_ALPHA_DONE_UNIT8090\\n"
'''
assert source.count(old) == 1
source = source.replace(old, new)

namespace = {"__file__": str(base_path), "__name__": "__main__"}
exec(compile(source, str(base_path), "exec"), namespace)
