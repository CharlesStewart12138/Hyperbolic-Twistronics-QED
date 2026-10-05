#!/usr/bin/env python3
"""Build the exact checkpoint-safe V7 producer for degree-24 seed shard005."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path


B = Path(__file__).resolve().parent
PROFILE = B / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SOURCE_ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard004_v7_v2_gpt56sol.g"
ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard005_v7_gpt56sol.g"
SLICE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_PLAN_SLICE_GPT56SOL.tsv"
WRAPPER = B / "gap_run_degree24_c8_seed_shard005_segment001_unit1_14648_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard005_segment001_postverify_v7.sh"
PARSE = B / "gap_parse_smoke_degree24_c8_seed_shard005_v7_gpt56sol.g"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_SEGMENT001_UNIT1_14648_POSTVERIFY_V7_GPT56SOL.txt"
PROFILE_SHA = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
SOURCE_ENGINE_SHA = "55C88A7D4AB5DD68EE8B1DDA6C2836651AA140278CAE08A986C33D7A127B071F"


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
for path in (ENGINE, SLICE, WRAPPER, RUNNER, PARSE, B / OUTPUT_NAME,
             B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_CHECKPOINT_GPT56SOL.txt",
             B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_CHECKPOINT_TMP_GPT56SOL.txt"):
    assert not path.exists(), f"no-clobber {path}"

engine = SOURCE_ENGINE.read_text(encoding="ascii")
engine = engine.replace("S004", "S005").replace("SHARD004", "SHARD005").replace("shard004", "shard005")
changes = {
    "Length(S005_RECORDS)<>302": "Length(S005_RECORDS)<>283",
    "S005_RECORDS[1].k<>6440 or S005_RECORDS[1].first<>3":
        "S005_RECORDS[1].k<>6769 or S005_RECORDS[1].first<>91",
    "S005_RECORDS[Length(S005_RECORDS)].k<>6769":
        "S005_RECORDS[Length(S005_RECORDS)].k<>7070",
    "S005_RECORDS[Length(S005_RECORDS)].last<>90":
        "S005_RECORDS[Length(S005_RECORDS)].last<>2",
    "14032": "14649",
    "14031": "14648",
    "43103232": "44998656",
    "225287": "151674",
    "PLAN_FIRST\\t24T6440\\t3\\nPLAN_LAST\\t24T6769\\t90\\nPLAN_KEYS\\t302":
        "PLAN_FIRST\\t24T6769\\t91\\nPLAN_LAST\\t24T7070\\t2\\nPLAN_KEYS\\t283",
    "seed-plan shard005 only; shard005 and later are excluded":
        "seed-plan shard005 only; shard006 and later are excluded",
    '"SHARD\\t003\\tUNIT\\t"': '"SHARD\\t005\\tUNIT\\t"',
}
for old, new in changes.items():
    count = engine.count(old)
    if old in {"14032", "14031", "43103232", "225287"}:
        assert count > 0, (old, count)
    else:
        assert count == 1, (old, count)
    engine = engine.replace(old, new)
for stale in ("S004", "SHARD004", "shard004", "24T6440\\t3", "24T6769\\t90",
              "Length(S005_RECORDS)<>302", "14031", "14032", "43103232", "225287",
              '"SHARD\\t003\\tUNIT\\t"', "shard005 only; shard005 and later"):
    assert stale not in engine, stale
atomic_write(ENGINE, engine.encode("ascii"))
engine_sha = digest(ENGINE.read_bytes())

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
summary: dict[str, str] | None = None
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[:2] == ["SHARD", "5"]:
        summary = fields(parts, 2)
    elif parts[:2] == ["WORK", "5"]:
        row = fields(parts, 2)
        work.append((int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), row))
assert summary is not None
assert (len(work), work[0][:3], work[-1][:3]) == (283, (6769, 91, 108), (7070, 1, 2))
assert all(work[i][0] < work[i + 1][0] for i in range(len(work) - 1))
expected_summary = {
    "KEYS_TOUCHED": "283", "CLASS_UNITS": "14648", "RAW_PAIRS": "44998656",
    "PROFILE_REBUILD_MS": "151674", "PAIR_MODEL_MS": "599983",
    "POINT_MODEL_MS": "751657", "FRACTION_INTERNAL_GUARD": "0.569437",
}
for name, value in expected_summary.items():
    assert summary[name] == value

records: list[dict[str, int | str]] = []
slice_lines = [
    "CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD005",
    f"PROFILE_SHA256\t{PROFILE_SHA}", f"PLAN_SHA256\t{PLAN_SHA}",
    "FIRST\t24T6769\t91", "LAST\t24T7070\t2",
]
unit = 1
for key, first, last, plan_row in work:
    p = profile[key]
    order = int(p["ORDER"])
    classes = int(p["ORDER8_CLASSES"])
    units = last - first + 1
    assert order == 3072 and classes > 0 and 1 <= first <= last <= classes
    assert int(p["RAW_PAIRS"]) == order * classes
    assert int(plan_row["ORDER"]) == order and int(plan_row["CLASS_UNITS"]) == units
    assert int(plan_row["RAW_PAIRS"]) == order * units
    route = p["ROUTE"]
    representation = p["REPRESENTATION"]
    pc_order = int(p["PC_ORDER"])
    assert (route, representation, pc_order) in {
        ("pc", "legacy_sealed_pc", order), ("native", "legacy_original_native", 0),
    }
    rec: dict[str, int | str] = {
        "k": key, "first": first, "last": last, "unitFirst": unit,
        "unitLast": unit + units - 1, "order": order, "autOrder": int(p["AUT_ORDER"]),
        "parity": int(p["PARITY_MAPS"]), "classes": classes,
        "raw": int(p["RAW_PAIRS"]), "method": route,
        "representation": representation, "pcOrder": pc_order,
        "profileMs": int(p["PROFILE_COST_MS"]),
    }
    records.append(rec)
    slice_lines.append(
        "WORK\tUNIT_FIRST\t{unitFirst}\tUNIT_LAST\t{unitLast}\tKEY\t24T{k}"
        "\tALPHA_FIRST\t{first}\tALPHA_LAST\t{last}\tORDER\t{order}\tAUT_ORDER\t{autOrder}"
        "\tPARITY_MAPS\t{parity}\tMETHOD\t{method}\tREPRESENTATION\t{representation}"
        "\tPC_ORDER\t{pcOrder}\tORDER8_CLASSES\t{classes}\tFULL_RAW_PAIRS\t{raw}"
        "\tPLANNED_RAW_PAIRS\t{planned}\tPROFILE_COST_MS\t{profileMs}".format(
            **rec, planned=order * units
        )
    )
    unit += units
assert unit == 14649
assert sum(int(r["order"]) * (int(r["last"]) - int(r["first"]) + 1) for r in records) == 44998656
assert sum(int(r["profileMs"]) for r in records) == 151674
slice_lines += [
    "CHECKSUM\tKEYS\t283\tCLASS_UNITS\t14648\tRAW_PAIRS\t44998656\tPROFILE_REBUILD_MS\t151674\tPAIR_MODEL_MS\t599983\tPOINT_MODEL_MS\t751657\tFRACTION_INTERNAL_GUARD\t0.569437",
    "SEED_PREDICATES\tNOT_RUN_BY_BUILDER", "DONE", "",
]
slice_data = "\n".join(slice_lines).encode("ascii")
atomic_write(SLICE, slice_data)

record_lines = [
    ('rec(k:={k},first:={first},last:={last},unitFirst:={unitFirst},unitLast:={unitLast},'
     'order:={order},autOrder:={autOrder},parity:={parity},classes:={classes},raw:={raw},'
     'method:"{method}",representation:"{representation}",pcOrder:={pcOrder},profileMs:={profileMs})').format(**r)
    for r in records
]
wrapper_lines = [
    "# Exact wrapper for sealed degree-24 seed workload shard005.",
    f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "STOP_AFTER_UNIT:=fail;", "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";',
    'CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_CHECKPOINT_GPT56SOL.txt";',
    'CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD005_CHECKPOINT_TMP_GPT56SOL.txt";',
    f'EXPECTED_PROFILE_SHA256:="{PROFILE_SHA}";', f'EXPECTED_PLAN_SHA256:="{PLAN_SHA}";',
    f'PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/{PROFILE.name}";',
    f'PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/{PLAN.name}";',
    f'ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/{ENGINE.name}";',
    f'EXPECTED_ENGINE_SHA256:="{engine_sha}";', "S005_RECORDS:=[", ",\n".join(record_lines), "];",
    f'Read("/mnt/d/work/revise/production_code/escalations/{ENGINE.name}");', "",
]
wrapper_data = "\n".join(wrapper_lines).encode("ascii")
runner_data = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n"
).encode("ascii")
parse_data = (
    f'f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}");\n'
    'if f=fail then Error("S005 wrapper parse failed"); fi;\n'
    f'g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{ENGINE.name}");\n'
    'if g=fail then Error("S005 engine parse failed"); fi;\n'
    'Print("SHARD005_V7_WRAPPER_ENGINE_PARSE_PASS\\n");\nQUIT_GAP(0);\n'
).encode("ascii")
atomic_write(WRAPPER, wrapper_data)
atomic_write(RUNNER, runner_data)
atomic_write(PARSE, parse_data)

native = sum(r["method"] == "native" for r in records)
print(f"PASS keys=283 units=14648 raw=44998656 profileMs=151674 native={native} engine_sha256={engine_sha}")
print(f"SLICE\t{SLICE.name}\tBYTES\t{len(slice_data)}\tSHA256\t{digest(slice_data)}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{digest(wrapper_data)}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{digest(runner_data)}")
print(f"PARSE\t{PARSE.name}\tSHA256\t{digest(parse_data)}")
