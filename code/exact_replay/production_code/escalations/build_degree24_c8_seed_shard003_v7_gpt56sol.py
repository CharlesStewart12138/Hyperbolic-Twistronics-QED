#!/usr/bin/env python3
"""Build the exact checkpoint-safe V7 producer for degree-24 seed shard003."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path


B = Path(__file__).resolve().parent
PROFILE = B / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SOURCE_ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard002_v7_gpt56sol.g"
ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard003_v7_gpt56sol.g"
SLICE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_PLAN_SLICE_GPT56SOL.tsv"
WRAPPER = B / "gap_run_degree24_c8_seed_shard003_segment001_unit1_14648_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard003_segment001_postverify_v7.sh"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNIT1_14648_POSTVERIFY_V7_GPT56SOL.txt"

PROFILE_SHA = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
SOURCE_ENGINE_SHA = "49D42E9354E24511EED3682FD5020608A470ED4DF1F1CC8DED417DD119924248"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha(path: Path) -> str:
    return digest(path.read_bytes())


def fields(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        assert parts[index] not in result
        result[parts[index]] = parts[index + 1]
    return result


def atomic_write(path: Path, data: bytes) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    assert path.read_bytes() == data


for path in (PROFILE, PLAN, SOURCE_ENGINE):
    assert path.is_file(), path
for path in (
    ENGINE, SLICE, WRAPPER, RUNNER, B / OUTPUT_NAME,
    B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_GPT56SOL.txt",
    B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_TMP_GPT56SOL.txt",
):
    assert not path.exists(), f"no-clobber {path}"
assert sha(PROFILE) == PROFILE_SHA
assert sha(PLAN) == PLAN_SHA
assert sha(SOURCE_ENGINE) == SOURCE_ENGINE_SHA

# Mechanically specialize the already hardened V7 engine. The predicate block is unchanged.
engine = SOURCE_ENGINE.read_text(encoding="ascii")
engine = engine.replace("S002", "S003").replace("SHARD002", "SHARD003")
old_endpoint = '''if S003_RECORDS[1].k<>5715 or S003_RECORDS[1].first<>67 or
   S003_RECORDS[Length(S003_RECORDS)].k<>6031 or
   S003_RECORDS[Length(S003_RECORDS)].last<>8 then Error("S003 endpoint"); fi;'''
new_endpoint = '''if S003_RECORDS[1].k<>6032 or S003_RECORDS[1].first<>1 or
   S003_RECORDS[Length(S003_RECORDS)].k<>6440 or
   S003_RECORDS[Length(S003_RECORDS)].last<>2 then Error("S003 endpoint"); fi;'''
assert engine.count(old_endpoint) == 1
engine = engine.replace(old_endpoint, new_endpoint)
old_header = ' "PLAN_FIRST\\t24T5715\\t67\\nPLAN_LAST\\t24T6031\\t8\\nPLAN_KEYS\\t297\\n",'
new_header = ' "PLAN_FIRST\\t24T6032\\t1\\nPLAN_LAST\\t24T6440\\t2\\nPLAN_KEYS\\t335\\n",'
assert engine.count(old_header) == 1
engine = engine.replace(old_header, new_header)
changes = {
    "Length(S003_RECORDS)<>297": "Length(S003_RECORDS)<>335",
    "14514": "14649",
    "14513": "14648",
    "44583936": "44998656",
    "194398": "169845",
    '"SHARD\\t002\\tUNIT\\t"': '"SHARD\\t003\\tUNIT\\t"',
    '"SCOPE\\tExactly seed-plan shard002 only; shard003 and later are excluded.\\n");':
        '"SCOPE\\tExactly seed-plan shard003 only; shard004 and later are excluded.\\n");',
}
for old, new in changes.items():
    assert engine.count(old) >= 1, old
    engine = engine.replace(old, new)
for stale in (
    "S002", "SHARD002", "24T5715\\t67", "24T6031\\t8", "Length(S003_RECORDS)<>297",
    "14513", "14514", "44583936", "194398", "seed-plan shard002",
):
    assert stale not in engine, stale
atomic_write(ENGINE, engine.encode("ascii"))
engine_sha = sha(ENGINE)

profile: dict[int, dict[str, str]] = {}
for line in PROFILE.read_text(encoding="ascii").splitlines():
    if line.startswith("ENTRY\t"):
        parts = line.split("\t")
        match = re.fullmatch(r"24T([0-9]+)", parts[1])
        assert match
        key = int(match.group(1))
        assert key not in profile
        profile[key] = fields(parts, 2)
assert len(profile) == 10714

work: list[tuple[int, int, int, dict[str, str]]] = []
shard: dict[str, str] | None = None
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[0:2] == ["SHARD", "3"]:
        shard = fields(parts, 2)
    elif parts[0:2] == ["WORK", "3"]:
        row = fields(parts, 2)
        work.append((int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), row))
assert shard is not None
assert (len(work), work[0][:3], work[-1][:3]) == (335, (6032, 1, 48), (6440, 1, 2))
assert all(work[index][0] < work[index + 1][0] for index in range(len(work) - 1))
expected_shard = {
    "KEYS_TOUCHED": "335", "CLASS_UNITS": "14648", "RAW_PAIRS": "44998656",
    "PROFILE_REBUILD_MS": "169845", "PAIR_MODEL_MS": "599983",
    "POINT_MODEL_MS": "769828", "FRACTION_INTERNAL_GUARD": "0.583203",
}
for name, value in expected_shard.items():
    assert shard[name] == value

records: list[dict[str, int | str]] = []
slice_lines = [
    "CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003",
    f"PROFILE_SHA256\t{PROFILE_SHA}", f"PLAN_SHA256\t{PLAN_SHA}",
    "FIRST\t24T6032\t1", "LAST\t24T6440\t2",
]
unit = 1
for key, first, last, work_row in work:
    profile_row = profile[key]
    order = int(profile_row["ORDER"])
    classes = int(profile_row["ORDER8_CLASSES"])
    units = last - first + 1
    assert classes > 0 and 1 <= first <= last <= classes
    assert int(profile_row["RAW_PAIRS"]) == order * classes
    assert int(work_row["ORDER"]) == order
    assert int(work_row["CLASS_UNITS"]) == units
    assert int(work_row["RAW_PAIRS"]) == order * units
    assert profile_row["ROUTE"] in ("pc", "native")
    if profile_row["ROUTE"] == "pc":
        assert profile_row["REPRESENTATION"] == "legacy_sealed_pc"
        assert int(profile_row["PC_ORDER"]) == order
    else:
        assert profile_row["REPRESENTATION"] == "legacy_original_native"
        assert int(profile_row["PC_ORDER"]) == 0
    record: dict[str, int | str] = {
        "k": key, "first": first, "last": last, "unitFirst": unit,
        "unitLast": unit + units - 1, "order": order,
        "autOrder": int(profile_row["AUT_ORDER"]), "parity": int(profile_row["PARITY_MAPS"]),
        "classes": classes, "raw": int(profile_row["RAW_PAIRS"]),
        "method": profile_row["ROUTE"], "representation": profile_row["REPRESENTATION"],
        "pcOrder": int(profile_row["PC_ORDER"]), "profileMs": int(profile_row["PROFILE_COST_MS"]),
    }
    records.append(record)
    slice_lines.append(
        "WORK\tUNIT_FIRST\t{unitFirst}\tUNIT_LAST\t{unitLast}\tKEY\t24T{k}"
        "\tALPHA_FIRST\t{first}\tALPHA_LAST\t{last}\tORDER\t{order}\tAUT_ORDER\t{autOrder}"
        "\tPARITY_MAPS\t{parity}\tMETHOD\t{method}\tREPRESENTATION\t{representation}"
        "\tPC_ORDER\t{pcOrder}\tORDER8_CLASSES\t{classes}\tFULL_RAW_PAIRS\t{raw}"
        "\tPLANNED_RAW_PAIRS\t{planned}\tPROFILE_COST_MS\t{profileMs}".format(
            **record, planned=order * units,
        )
    )
    unit += units
assert unit == 14649
assert sum(int(row["order"]) * (int(row["last"]) - int(row["first"]) + 1) for row in records) == 44998656
assert sum(int(row["profileMs"]) for row in records) == 169845
slice_lines.extend([
    "CHECKSUM\tKEYS\t335\tCLASS_UNITS\t14648\tRAW_PAIRS\t44998656\tPROFILE_REBUILD_MS\t169845\tPAIR_MODEL_MS\t599983\tPOINT_MODEL_MS\t769828\tFRACTION_INTERNAL_GUARD\t0.583203",
    "SEED_PREDICATES\tNOT_RUN_BY_BUILDER", "DONE", "",
])
atomic_write(SLICE, "\n".join(slice_lines).encode("ascii"))

record_lines = [
    ('rec(k:={k},first:={first},last:={last},unitFirst:={unitFirst},unitLast:={unitLast},'
     'order:={order},autOrder:={autOrder},parity:={parity},classes:={classes},raw:={raw},'
     'method:="{method}",representation:="{representation}",pcOrder:={pcOrder},profileMs:={profileMs})').format(**row)
    for row in records
]
wrapper = "\n".join([
    "# Exact wrapper for sealed degree-24 seed workload shard003.",
    f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "STOP_AFTER_UNIT:=fail;", "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";',
    'CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_GPT56SOL.txt";',
    'CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_TMP_GPT56SOL.txt";',
    f'EXPECTED_PROFILE_SHA256:="{PROFILE_SHA}";', f'EXPECTED_PLAN_SHA256:="{PLAN_SHA}";',
    f'PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/{PROFILE.name}";',
    f'PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/{PLAN.name}";',
    f'ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/{ENGINE.name}";',
    f'EXPECTED_ENGINE_SHA256:="{engine_sha}";', "S003_RECORDS:=[",
    ",\n".join(record_lines), "];",
    f'Read("/mnt/d/work/revise/production_code/escalations/{ENGINE.name}");', "",
])
runner = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n"
)
atomic_write(WRAPPER, wrapper.encode("ascii"))
atomic_write(RUNNER, runner.encode("ascii"))

print(f"PASS keys=335 units=14648 raw=44998656 profileMs=169845 engine_sha256={engine_sha}")
print(f"SLICE\t{SLICE.name}\tSHA256\t{sha(SLICE)}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{sha(WRAPPER)}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{sha(RUNNER)}")
