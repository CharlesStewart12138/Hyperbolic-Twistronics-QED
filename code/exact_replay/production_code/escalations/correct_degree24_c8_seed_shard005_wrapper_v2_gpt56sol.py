#!/usr/bin/env python3
"""Correct the pre-execution shard005 GAP record-field syntax."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
SOURCE = B / "gap_run_degree24_c8_seed_shard005_segment001_unit1_14648_postverify_v7_gpt56sol.g"
WRAPPER = B / "gap_run_degree24_c8_seed_shard005_segment001_v2_unit1_14648_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard005_segment001_v2_postverify_v7.sh"
PARSE = B / "gap_parse_smoke_degree24_c8_seed_shard005_v2_v7_gpt56sol.g"
ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard005_v7_v2_gpt56sol.g"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    if temp.exists():
        raise RuntimeError(f"stale temp {temp}")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists() and path.read_bytes() == data


text = SOURCE.read_text(encoding="ascii")
assert text.count('method:"') == 283
assert text.count('representation:"') == 283
text = text.replace('method:"', 'method:="').replace('representation:"', 'representation:="')
assert 'method:"' not in text and 'representation:"' not in text
wrapper_data = text.encode("ascii")
runner_data = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n"
).encode("ascii")
parse_data = (
    f'f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}");\n'
    'if f=fail then Error("S005 V2 wrapper parse failed"); fi;\n'
    f'g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{ENGINE.name}");\n'
    'if g=fail then Error("S005 engine parse failed"); fi;\n'
    'Print("SHARD005_V2_V7_WRAPPER_ENGINE_PARSE_PASS\\n");\nQUIT_GAP(0);\n'
).encode("ascii")
for path in (WRAPPER, RUNNER, PARSE):
    assert not path.exists(), path
atomic_write(WRAPPER, wrapper_data)
atomic_write(RUNNER, runner_data)
atomic_write(PARSE, parse_data)
print(f"PASS RECORDS=283 WRAPPER_SHA256={digest(wrapper_data)}")
print(f"RUNNER_SHA256={digest(runner_data)} PARSE_SHA256={digest(parse_data)}")
