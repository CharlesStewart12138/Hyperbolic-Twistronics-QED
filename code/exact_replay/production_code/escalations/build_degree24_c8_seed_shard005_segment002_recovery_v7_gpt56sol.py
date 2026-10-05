#!/usr/bin/env python3
"""Derive and execute the exact shard005 recovery builder from validated S004 logic."""

from pathlib import Path


B = Path(__file__).resolve().parent
base = B / "build_degree24_c8_seed_shard004_segment002_recovery_v7_gpt56sol.py"
source = base.read_text(encoding="ascii")
source = source.replace("shard004", "shard005").replace("SHARD004", "SHARD005").replace("S004", "S005")

replacements = {
    'gap_run_degree24_c8_seed_shard005_segment001_unit1_14031_postverify_v7_gpt56sol.g':
        'gap_run_degree24_c8_seed_shard005_segment001_v2_unit1_14648_postverify_v7_gpt56sol.g',
    'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_UNIT1_14031_POSTVERIFY_V7_GPT56SOL.txt':
        'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_UNIT1_14648_POSTVERIFY_V7_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt':
        'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_RUN_STDOUT_V2_V7_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt':
        'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_RUN_STDERR_V2_V7_GPT56SOL.txt',
    'gap_run_degree24_c8_seed_shard005_segment002_unit11897_14031_postverify_v7_gpt56sol.g':
        'gap_run_degree24_c8_seed_shard005_segment002_unit12944_14648_postverify_v7_gpt56sol.g',
    'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT002_UNIT11897_14031_POSTVERIFY_V7_GPT56SOL.txt':
        'GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT002_UNIT12944_14648_POSTVERIFY_V7_GPT56SOL.txt',
    'UNCOMMITTED_OUTPUT_SUFFIX_UNIT11897': 'UNCOMMITTED_OUTPUT_SUFFIX_UNIT12944',
    '"bbe5270942524e5fe250e4a9a9656040c7d9a889b5d838074235ddb991fc0423"':
        '"e6eaacfb669ca4c3fa9edeb8b4a144d8e0829fdf6465ef8a9939188a986d8e71"',
    'PREFIX_BYTES = 9_065_618': 'PREFIX_BYTES = 9_861_389',
    '"d8addbd6fe7afcc9507da0794e5761bfc44e40ab0aad46a71816bfb65e784898"':
        '"9e1dee3c1c93f0a66da6a5ebda15eb6aae2bd12198f283f9fe8a9d82019dff04"',
    'PHYSICAL_BYTES = 9_066_383': 'PHYSICAL_BYTES = 9_862_152',
    '"4580fdd32dece25f022dbfb369b31cb0b84ff16d3fc6ae1d35dc939681604550"':
        '"58e1d2b950f0586de9b13a402b2f328ff67a1d5852b190ae7c918c9ec3a5809b"',
    'COUNTERS = [11_896, 36_544_512, 11_896, 606, 3_091_144, 2_304_656,\n            678_848, 108_608, 0, 0, 0, 0]':
        'COUNTERS = [12_943, 39_760_896, 12_943, 566, 3_106_632, 2_475_328,\n            707_264, 77_632, 0, 0, 0, 0]',
    'assert fields[0:2] == ["SHARD", "003"]': 'assert fields[0:2] == ["SHARD", "005"]',
    'assert values["UNIT"] == "11896" and values["NEXT_UNIT"] == "11897"':
        'assert values["UNIT"] == "12943" and values["NEXT_UNIT"] == "12944"',
    'assert values["KEY"] == "24T6728" and values["ALPHA"] == "43"':
        'assert values["KEY"] == "24T7029" and values["ALPHA"] == "3"',
    'assert b"CHECKPOINT_COMMITTED\\tUNIT\\t11897\\t" not in physical':
        'assert b"CHECKPOINT_COMMITTED\\tUNIT\\t12944\\t" not in physical',
    'assert b"ALPHA_DONE\\tUNIT\\t11898\\t" not in physical':
        'assert b"ALPHA_DONE\\tUNIT\\t12945\\t" not in physical',
    '"LAST_DURABLE_UNIT\\t11896\\nNEXT_UNIT\\t11897\\nLAST_DURABLE_KEY_ALPHA\\t24T6728\\t43\\n"':
        '"LAST_DURABLE_UNIT\\t12943\\nNEXT_UNIT\\t12944\\nLAST_DURABLE_KEY_ALPHA\\t24T7029\\t3\\n"',
    '"EXCLUSION\\tUncommitted ALPHA_DONE unit11897 is evidence only and excluded from scientific totals\\n"':
        '"EXCLUSION\\tUncommitted ALPHA_DONE unit12944 is evidence only and excluded from scientific totals\\n"',
    '"RECOVERY\\tSTART_UNIT11897 recomputes 24T6728 alpha44; committed units1..11896 are not replayed\\n"':
        '"RECOVERY\\tSTART_UNIT12944 recomputes 24T7029 alpha4; committed units1..12943 are not replayed\\n"',
    '"INTERNAL_GUARD_MS:=1320000; START_UNIT:=11897;':
        '"INTERNAL_GUARD_MS:=1320000; START_UNIT:=12944;',
    '"PASS START_UNIT=11897 PREVIOUS_UNIT=11896 NO_REPLAY=1 RECOMPUTE_UNCOMMITTED=1"':
        '"PASS START_UNIT=12944 PREVIOUS_UNIT=12943 NO_REPLAY=1 RECOMPUTE_UNCOMMITTED=1"',
}
for old, new in replacements.items():
    assert source.count(old) >= 1, old
    source = source.replace(old, new)

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
    "CHECKPOINT_COMMITTED\\tUNIT\\t12943\\tCHECKPOINT_SHA256\\t" + CP_SHA
    + "\\tOUTPUT_PREFIX_BYTES\\t9861389\\tOUTPUT_PREFIX_SHA256\\t" + PREFIX_SHA
)
assert suffix_lines[1].startswith("ALPHA_DONE\\tUNIT\\t12944\\tKEY\\t24T7029\\tALPHA\\t4\\t")
assert "\\tCUM_UNITS\\t12944\\t" in suffix_lines[1]
assert "\\tNEXT_UNIT\\t12945\\t" in suffix_lines[1]
assert "\\tPREVIOUS_CHECKPOINT_SHA256\\t" + CP_SHA + "\\t" in suffix_lines[1]
'''
assert source.count(old) == 1
source = source.replace(old, new)
old = '''    f"UNCOMMITTED_SUFFIX\\t{PRESERVED_SUFFIX.name}\\tBYTES\\t{len(suffix)}\\tSHA256\\t{digest(suffix).upper()}\\tRECORD\\tALPHA_DONE_UNIT11897_24T6728_ALPHA44\\n"
'''
new = '''    f"POSTPREFIX_SUFFIX\\t{PRESERVED_SUFFIX.name}\\tBYTES\\t{len(suffix)}\\tSHA256\\t{digest(suffix).upper()}\\tRECORDS\\tCOMMITTED_UNIT12943_THEN_UNCOMMITTED_ALPHA_DONE_UNIT12944\\n"
'''
assert source.count(old) == 1
source = source.replace(old, new)
source = source.replace(
    'PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_UNCOMMITTED_OUTPUT_SUFFIX_UNIT12944_GPT56SOL.txt"',
    'PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_POSTPREFIX_SUFFIX_COMMIT12943_UNCOMMITTED12944_GPT56SOL.txt"',
)
source = source.replace(
    '"LABEL_NOTE\\tCheckpoint SHARD=003 is an inherited non-scientific label defect; certificate header and all S005 identities are correct\\n"',
    '"LABEL_NOTE\\tCheckpoint SHARD=005 matches shard identity\\n"',
)
namespace = {"__file__": str(base), "__name__": "__main__"}
exec(compile(source, str(base) + "#S005", "exec"), namespace)
