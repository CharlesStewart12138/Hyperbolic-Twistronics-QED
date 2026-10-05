#!/usr/bin/env python3
"""Build exact checkpoint-safe V7 producer for degree-24 seed shard004."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

B = Path(__file__).resolve().parent
PROFILE = B / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SOURCE_ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard003_v7_gpt56sol.g"
ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard004_v7_gpt56sol.g"
SLICE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_PLAN_SLICE_GPT56SOL.tsv"
WRAPPER = B / "gap_run_degree24_c8_seed_shard004_segment001_unit1_14031_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard004_segment001_postverify_v7.sh"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_UNIT1_14031_POSTVERIFY_V7_GPT56SOL.txt"
PROFILE_SHA = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
SOURCE_ENGINE_SHA = "B5C1CFB76FF04F205846826700BCB6EAE36C96D7C89851B3434BEFDCE6A9BAA7"
EXPECTED_SLICE_SHA = "6E915D384DEF826C8A4F1CF533B6AD1D3202F2877CF6F2B00FDFD6A945215C8B"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists() and path.read_bytes() == data


def fields(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0
    result: dict[str, str] = {}
    for i in range(start, len(parts), 2):
        assert parts[i] not in result
        result[parts[i]] = parts[i + 1]
    return result


assert digest(PROFILE.read_bytes()) == PROFILE_SHA
assert digest(PLAN.read_bytes()) == PLAN_SHA
assert digest(SOURCE_ENGINE.read_bytes()) == SOURCE_ENGINE_SHA
for path in (ENGINE, SLICE, WRAPPER, RUNNER, B / OUTPUT_NAME,
             B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CHECKPOINT_GPT56SOL.txt",
             B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CHECKPOINT_TMP_GPT56SOL.txt"):
    assert not path.exists(), f"no-clobber {path}"

engine = SOURCE_ENGINE.read_text(encoding="ascii")
engine = engine.replace("S003", "S004").replace("SHARD003", "SHARD004").replace("shard003", "shard004")
changes = {
    "Length(S004_RECORDS)<>335": "Length(S004_RECORDS)<>302",
    "S004_RECORDS[1].k<>6032 or S004_RECORDS[1].first<>1":
        "S004_RECORDS[1].k<>6440 or S004_RECORDS[1].first<>3",
    "S004_RECORDS[Length(S004_RECORDS)].k<>6440":
        "S004_RECORDS[Length(S004_RECORDS)].k<>6769",
    "S004_RECORDS[Length(S004_RECORDS)].last<>2":
        "S004_RECORDS[Length(S004_RECORDS)].last<>90",
    "14648": "14031",
    "14649": "14032",
    "44998656": "43103232",
    "169845": "225287",
    "PLAN_FIRST\\t24T6032\\t1\\nPLAN_LAST\\t24T6440\\t2\\nPLAN_KEYS\\t335":
        "PLAN_FIRST\\t24T6440\\t3\\nPLAN_LAST\\t24T6769\\t90\\nPLAN_KEYS\\t302",
    "seed-plan shard004 only; shard004 and later are excluded":
        "seed-plan shard004 only; shard005 and later are excluded",
}
for old, new in changes.items():
    count = engine.count(old)
    if old in {"14648", "14649", "44998656", "169845"}:
        assert count > 0, (old, count)
    else:
        assert count == 1, (old, count)
    engine = engine.replace(old, new)
for stale in ("S003", "SHARD003", "shard003", "24T6032\\t1", "24T6440\\t2",
              "Length(S004_RECORDS)<>335", "14648", "14649", "44998656", "169845",
              "seed-plan shard004 only; shard004 and later"):
    assert stale not in engine, stale
atomic_write(ENGINE, engine.encode("ascii"))
engine_sha = digest(ENGINE.read_bytes())

profile: dict[int, dict[str, str]] = {}
for line in PROFILE.read_text(encoding="ascii").splitlines():
    if line.startswith("ENTRY\t"):
        parts = line.split("\t"); match = re.fullmatch(r"24T([0-9]+)", parts[1]); assert match
        key = int(match.group(1)); assert key not in profile; profile[key] = fields(parts, 2)
assert len(profile) == 10714

work: list[tuple[int, int, int, dict[str, str]]] = []
summary: dict[str, str] | None = None
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[:2] == ["SHARD", "4"]:
        summary = fields(parts, 2)
    elif parts[:2] == ["WORK", "4"]:
        row = fields(parts, 2)
        work.append((int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), row))
assert summary is not None
assert (len(work), work[0][:3], work[-1][:3]) == (302, (6440, 3, 94), (6769, 1, 90))
assert all(work[i][0] < work[i + 1][0] for i in range(len(work) - 1))
expected_summary = {"KEYS_TOUCHED":"302", "CLASS_UNITS":"14031", "RAW_PAIRS":"43103232",
                    "PROFILE_REBUILD_MS":"225287", "PAIR_MODEL_MS":"574710",
                    "POINT_MODEL_MS":"799997", "FRACTION_INTERNAL_GUARD":"0.606058"}
for name, value in expected_summary.items(): assert summary[name] == value

records: list[dict[str, int | str]] = []
slice_lines = ["CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD004",
               f"PROFILE_SHA256\t{PROFILE_SHA}", f"PLAN_SHA256\t{PLAN_SHA}",
               "FIRST\t24T6440\t3", "LAST\t24T6769\t90"]
unit = 1
for key, first, last, plan_row in work:
    p = profile[key]; order = int(p["ORDER"]); classes = int(p["ORDER8_CLASSES"]); units = last-first+1
    assert order == 3072 and p["SOLVABLE"] == "true" and classes > 0 and 1 <= first <= last <= classes
    assert int(p["RAW_PAIRS"]) == order * classes
    assert int(plan_row["ORDER"]) == order and int(plan_row["CLASS_UNITS"]) == units
    assert int(plan_row["RAW_PAIRS"]) == order * units
    route = p["ROUTE"]; representation = p["REPRESENTATION"]; pc_order = int(p["PC_ORDER"])
    assert (route, representation, pc_order) in {
        ("pc", "legacy_sealed_pc", order), ("native", "legacy_original_native", 0)}
    record: dict[str, int | str] = {
        "k":key,"first":first,"last":last,"unitFirst":unit,"unitLast":unit+units-1,
        "order":order,"autOrder":int(p["AUT_ORDER"]),"parity":int(p["PARITY_MAPS"]),
        "classes":classes,"raw":int(p["RAW_PAIRS"]),"method":route,
        "representation":representation,"pcOrder":pc_order,"profileMs":int(p["PROFILE_COST_MS"])}
    records.append(record)
    slice_lines.append(
        "WORK\tUNIT_FIRST\t{unitFirst}\tUNIT_LAST\t{unitLast}\tKEY\t24T{k}"
        "\tALPHA_FIRST\t{first}\tALPHA_LAST\t{last}\tORDER\t{order}\tAUT_ORDER\t{autOrder}"
        "\tPARITY_MAPS\t{parity}\tMETHOD\t{method}\tREPRESENTATION\t{representation}"
        "\tPC_ORDER\t{pcOrder}\tORDER8_CLASSES\t{classes}\tFULL_RAW_PAIRS\t{raw}"
        "\tPLANNED_RAW_PAIRS\t{planned}\tPROFILE_COST_MS\t{profileMs}".format(**record, planned=order*units))
    unit += units
assert unit == 14032
assert sum(int(r["order"])*(int(r["last"])-int(r["first"])+1) for r in records) == 43103232
assert sum(int(r["profileMs"]) for r in records) == 225287
slice_lines += ["CHECKSUM\tKEYS\t302\tCLASS_UNITS\t14031\tRAW_PAIRS\t43103232\tPROFILE_REBUILD_MS\t225287\tPAIR_MODEL_MS\t574710\tPOINT_MODEL_MS\t799997\tFRACTION_INTERNAL_GUARD\t0.606058",
                "SEED_PREDICATES\tNOT_RUN_BY_BUILDER", "DONE", ""]
slice_data = "\n".join(slice_lines).encode("ascii")
assert len(slice_data) == 78359 and digest(slice_data) == EXPECTED_SLICE_SHA
atomic_write(SLICE, slice_data)

record_lines = [('rec(k:={k},first:={first},last:={last},unitFirst:={unitFirst},unitLast:={unitLast},'
                 'order:={order},autOrder:={autOrder},parity:={parity},classes:={classes},raw:={raw},'
                 'method:="{method}",representation:="{representation}",pcOrder:={pcOrder},profileMs:={profileMs})').format(**r)
                for r in records]
wrapper_lines = ["# Exact wrapper for sealed degree-24 seed workload shard004.",
    f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "STOP_AFTER_UNIT:=fail;", "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";',
    'CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CHECKPOINT_GPT56SOL.txt";',
    'CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CHECKPOINT_TMP_GPT56SOL.txt";',
    f'EXPECTED_PROFILE_SHA256:="{PROFILE_SHA}";', f'EXPECTED_PLAN_SHA256:="{PLAN_SHA}";',
    f'PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/{PROFILE.name}";',
    f'PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/{PLAN.name}";',
    f'ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/{ENGINE.name}";',
    f'EXPECTED_ENGINE_SHA256:="{engine_sha}";', "S004_RECORDS:=[", ",\n".join(record_lines), "];",
    f'Read("/mnt/d/work/revise/production_code/escalations/{ENGINE.name}");', ""]
wrapper_data = "\n".join(wrapper_lines).encode("ascii")
runner_data = ("#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
               "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
               f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n").encode("ascii")
atomic_write(WRAPPER, wrapper_data); atomic_write(RUNNER, runner_data)
print(f"PASS keys=302 units=14031 raw=43103232 profileMs=225287 native=6 engine_sha256={engine_sha}")
print(f"SLICE\t{SLICE.name}\tSHA256\t{digest(slice_data)}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{digest(wrapper_data)}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{digest(runner_data)}")
