#!/usr/bin/env python3
"""Mechanically specialize the audited shard003 V7 builder for shard004."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name("build_degree24_c8_seed_shard003_v7_gpt56sol.py")
SOURCE_SHA256 = "285D7245AA84F7F5D09354DD6938F91B9A7F128934A2BD033F7EC0839B9FF106"

source_bytes = SOURCE.read_bytes()
actual = hashlib.sha256(source_bytes).hexdigest().upper()
assert actual == SOURCE_SHA256, (actual, SOURCE_SHA256)
source = source_bytes.decode("ascii")
source = source.replace("shard003", "shard004")
source = source.replace("SHARD003", "SHARD004")
source = source.replace("S003", "S004")


def replace_once(old: str, new: str) -> None:
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)


replace_once(
    '''new_endpoint = ''' + "'''" + '''if S004_RECORDS[1].k<>6032 or S004_RECORDS[1].first<>1 or
   S004_RECORDS[Length(S004_RECORDS)].k<>6440 or
   S004_RECORDS[Length(S004_RECORDS)].last<>2 then Error("S004 endpoint"); fi;''' + "'''",
    '''new_endpoint = ''' + "'''" + '''if S004_RECORDS[1].k<>6440 or S004_RECORDS[1].first<>3 or
   S004_RECORDS[Length(S004_RECORDS)].k<>6769 or
   S004_RECORDS[Length(S004_RECORDS)].last<>90 then Error("S004 endpoint"); fi;''' + "'''",
)
replace_once(
    '''new_header = ' "PLAN_FIRST\\t24T6032\\t1\\nPLAN_LAST\\t24T6440\\t2\\nPLAN_KEYS\\t335\\n",' ''',
    '''new_header = ' "PLAN_FIRST\\t24T6440\\t3\\nPLAN_LAST\\t24T6769\\t90\\nPLAN_KEYS\\t302\\n",' ''',
)
for old, new in (
    ('"Length(S004_RECORDS)<>335"', '"Length(S004_RECORDS)<>302"'),
    ('"14514": "14649"', '"14514": "14032"'),
    ('"14513": "14648"', '"14513": "14031"'),
    ('"44583936": "44998656"', '"44583936": "43103232"'),
    ('"194398": "169845"', '"194398": "225287"'),
    ('seed-plan shard004 only; shard004 and later are excluded',
     'seed-plan shard004 only; shard005 and later are excluded'),
    ('["SHARD", "3"]', '["SHARD", "4"]'),
    ('["WORK", "3"]', '["WORK", "4"]'),
    ('(335, (6032, 1, 48), (6440, 1, 2))',
     '(302, (6440, 3, 94), (6769, 1, 90))'),
    ('"KEYS_TOUCHED": "335", "CLASS_UNITS": "14648", "RAW_PAIRS": "44998656",',
     '"KEYS_TOUCHED": "302", "CLASS_UNITS": "14031", "RAW_PAIRS": "43103232",'),
    ('"PROFILE_REBUILD_MS": "169845", "PAIR_MODEL_MS": "599983",',
     '"PROFILE_REBUILD_MS": "225287", "PAIR_MODEL_MS": "574710",'),
    ('"POINT_MODEL_MS": "769828", "FRACTION_INTERNAL_GUARD": "0.583203",',
     '"POINT_MODEL_MS": "799997", "FRACTION_INTERNAL_GUARD": "0.606058",'),
    ('"FIRST\\t24T6032\\t1", "LAST\\t24T6440\\t2",',
     '"FIRST\\t24T6440\\t3", "LAST\\t24T6769\\t90",'),
    ('assert unit == 14649', 'assert unit == 14032'),
    ('== 44998656', '== 43103232'),
    ('== 169845', '== 225287'),
    ('"CHECKSUM\\tKEYS\\t335\\tCLASS_UNITS\\t14648\\tRAW_PAIRS\\t44998656\\tPROFILE_REBUILD_MS\\t169845\\tPAIR_MODEL_MS\\t599983\\tPOINT_MODEL_MS\\t769828\\tFRACTION_INTERNAL_GUARD\\t0.583203",',
     '"CHECKSUM\\tKEYS\\t302\\tCLASS_UNITS\\t14031\\tRAW_PAIRS\\t43103232\\tPROFILE_REBUILD_MS\\t225287\\tPAIR_MODEL_MS\\t574710\\tPOINT_MODEL_MS\\t799997\\tFRACTION_INTERNAL_GUARD\\t0.606058",'),
    ('print(f"PASS keys=335 units=14648 raw=44998656 profileMs=169845 engine_sha256={engine_sha}")',
     'print(f"PASS keys=302 units=14031 raw=43103232 profileMs=225287 engine_sha256={engine_sha}")'),
):
    replace_once(old, new)

# The source's stale-token assertions describe the generated engine.  Replace
# the shard003 values with the new generated shard004 values.
source = source.replace('"24T6032\\t1", "24T6440\\t2"', '"24T6440\\t3", "24T6769\\t90"')
source = source.replace('"14648", "14649", "44998656", "169845"',
                        '"14031", "14032", "43103232", "225287"')

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(source, str(SOURCE) + "#SHARD004", "exec"), namespace)
