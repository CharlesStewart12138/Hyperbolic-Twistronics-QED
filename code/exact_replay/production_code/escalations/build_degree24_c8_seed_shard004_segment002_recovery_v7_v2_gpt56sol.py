#!/usr/bin/env python3
"""Correct V1's post-prefix parser and execute the shard004 recovery build."""

from __future__ import annotations

from pathlib import Path


B = Path(__file__).resolve().parent
base_path = B / "build_degree24_c8_seed_shard004_segment002_recovery_v7_gpt56sol.py"
source = base_path.read_text(encoding="ascii")
source = source.replace(
    'PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_UNCOMMITTED_OUTPUT_SUFFIX_UNIT11897_GPT56SOL.txt"',
    'PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_POSTPREFIX_SUFFIX_COMMIT11896_UNCOMMITTED11897_GPT56SOL.txt"',
)
old = '''suffix_lines = suffix.decode("ascii").splitlines()
assert len(suffix_lines) == 1
assert suffix_lines[0].startswith("ALPHA_DONE\\tUNIT\\t11897\\tKEY\\t24T6728\\tALPHA\\t44\\t")
assert "\\tCUM_UNITS\\t11897\\t" in suffix_lines[0]
assert "\\tNEXT_UNIT\\t11898\\t" in suffix_lines[0]
assert "\\tPREVIOUS_CHECKPOINT_SHA256\\t" + CP_SHA + "\\t" in suffix_lines[0]
'''
new = '''suffix_lines = suffix.decode("ascii").splitlines()
assert len(suffix_lines) == 2
assert suffix_lines[0] == (
    "CHECKPOINT_COMMITTED\\tUNIT\\t11896\\tCHECKPOINT_SHA256\\t" + CP_SHA
    + "\\tOUTPUT_PREFIX_BYTES\\t9065618\\tOUTPUT_PREFIX_SHA256\\t" + PREFIX_SHA
)
assert suffix_lines[1].startswith("ALPHA_DONE\\tUNIT\\t11897\\tKEY\\t24T6728\\tALPHA\\t44\\t")
assert "\\tCUM_UNITS\\t11897\\t" in suffix_lines[1]
assert "\\tNEXT_UNIT\\t11898\\t" in suffix_lines[1]
assert "\\tPREVIOUS_CHECKPOINT_SHA256\\t" + CP_SHA + "\\t" in suffix_lines[1]
'''
assert source.count(old) == 1
source = source.replace(old, new)
old = '''    f"UNCOMMITTED_SUFFIX\\t{PRESERVED_SUFFIX.name}\\tBYTES\\t{len(suffix)}\\tSHA256\\t{digest(suffix).upper()}\\tRECORD\\tALPHA_DONE_UNIT11897_24T6728_ALPHA44\\n"
'''
new = '''    f"POSTPREFIX_SUFFIX\\t{PRESERVED_SUFFIX.name}\\tBYTES\\t{len(suffix)}\\tSHA256\\t{digest(suffix).upper()}\\tRECORDS\\tCOMMITTED_UNIT11896_THEN_UNCOMMITTED_ALPHA_DONE_UNIT11897\\n"
'''
assert source.count(old) == 1
source = source.replace(old, new)

namespace = {"__file__": str(base_path), "__name__": "__main__"}
exec(compile(source, str(base_path), "exec"), namespace)
