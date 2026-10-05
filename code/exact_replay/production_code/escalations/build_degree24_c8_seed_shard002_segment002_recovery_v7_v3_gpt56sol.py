#!/usr/bin/env python3
"""Run the V2 recovery builder with the corrected prefix-versus-commit suffix audit."""

from pathlib import Path


source_path = Path(__file__).with_name(
    "build_degree24_c8_seed_shard002_segment002_recovery_v7_v2_gpt56sol.py"
)
source = source_path.read_text(encoding="ascii")

old = '''previous = SOURCE_OUTPUT.read_bytes()
assert len(previous) == PREFIX_BYTES and digest(previous) == PREFIX_SHA
assert previous.endswith(
    b"CHECKPOINT_COMMITTED\\tUNIT\\t12357\\tCHECKPOINT_SHA256\\t"
    + CP_SHA.encode("ascii")
    + b"\\tOUTPUT_PREFIX_BYTES\\t9401850\\tOUTPUT_PREFIX_SHA256\\t"
    + PREFIX_SHA.encode("ascii") + b"\\n"
)
'''
new = '''previous = SOURCE_OUTPUT.read_bytes()
assert len(previous) >= PREFIX_BYTES
assert digest(previous[:PREFIX_BYTES]) == PREFIX_SHA
expected_suffix = (
    b"CHECKPOINT_COMMITTED\\tUNIT\\t12357\\tCHECKPOINT_SHA256\\t"
    + CP_SHA.encode("ascii")
    + b"\\tOUTPUT_PREFIX_BYTES\\t9401850\\tOUTPUT_PREFIX_SHA256\\t"
    + PREFIX_SHA.encode("ascii") + b"\\n"
)
assert previous[PREFIX_BYTES:] == expected_suffix
'''
assert source.count(old) == 1
source = source.replace(old, new)

old_print = 'print(f"PREVIOUS_OUTPUT\\t{SOURCE_OUTPUT.name}\\tBYTES\\t{len(previous)}\\tSHA256\\t{digest(previous)}")'
new_print = 'print(f"PREVIOUS_OUTPUT\\t{SOURCE_OUTPUT.name}\\tPHYSICAL_BYTES\\t{len(previous)}\\tPHYSICAL_SHA256\\t{digest(previous)}\\tPREFIX_BYTES\\t{PREFIX_BYTES}\\tPREFIX_SHA256\\t{digest(previous[:PREFIX_BYTES])}")'
assert source.count(old_print) == 1
source = source.replace(old_print, new_print)

namespace = {"__file__": str(source_path), "__name__": "__main__"}
exec(compile(source, str(source_path), "exec"), namespace)
