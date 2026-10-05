from __future__ import annotations

import hashlib
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent
PROFILE = BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SOURCE_ENGINE = BASE / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v5_gpt56sol.g"
ENGINE = BASE / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard002_v7_gpt56sol.g"
SLICE = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_PLAN_SLICE_GPT56SOL.tsv"
WRAPPER = BASE / "gap_run_degree24_c8_seed_shard002_segment001_unit1_14513_postverify_v7_gpt56sol.g"
RUNNER = BASE / "run_degree24_c8_seed_shard002_segment001_postverify_v7.sh"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt"

PROFILE_SHA = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
SOURCE_ENGINE_SHA = "D0A86DBFE4067D4089D1D01BA6F06CAC6B90416763527883A2B287A23CDFA96D"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def field_map(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0
    result: dict[str, str] = {}
    for i in range(start, len(parts), 2):
        assert parts[i] not in result
        result[parts[i]] = parts[i + 1]
    return result


for path in (PROFILE, PLAN, SOURCE_ENGINE):
    assert path.is_file(), path
for path in (ENGINE, SLICE, WRAPPER, RUNNER, BASE / OUTPUT_NAME,
             BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt",
             BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_TMP_GPT56SOL.txt"):
    assert not path.exists(), f"no-clobber {path}"
assert sha(PROFILE) == PROFILE_SHA and sha(PLAN) == PLAN_SHA and sha(SOURCE_ENGINE) == SOURCE_ENGINE_SHA

# Mechanically specialize the already certified frozen S001 predicate to S002.
engine = SOURCE_ENGINE.read_text(encoding="ascii")
engine = engine.replace("S001", "S002").replace("SHARD001", "SHARD002")
old_endpoint = '''if S002_RECORDS[1].k<>5155 or S002_RECORDS[1].first<>1 or
   S002_RECORDS[Length(S002_RECORDS)].k<>5715 or
   S002_RECORDS[Length(S002_RECORDS)].last<>66 then Error("S002 endpoint"); fi;'''
new_endpoint = '''if S002_RECORDS[1].k<>5715 or S002_RECORDS[1].first<>67 or
   S002_RECORDS[Length(S002_RECORDS)].k<>6031 or
   S002_RECORDS[Length(S002_RECORDS)].last<>8 then Error("S002 endpoint"); fi;'''
assert engine.count(old_endpoint) == 1
engine = engine.replace(old_endpoint, new_endpoint)
old_plan_header = ' "PLAN_FIRST\\t24T5155\\t1\\nPLAN_LAST\\t24T5715\\t66\\nPLAN_KEYS\\t466\\n",'
new_plan_header = ' "PLAN_FIRST\\t24T5715\\t67\\nPLAN_LAST\\t24T6031\\t8\\nPLAN_KEYS\\t297\\n",'
assert engine.count(old_plan_header) == 1
engine = engine.replace(old_plan_header, new_plan_header)
engine = engine.replace("Length(S002_RECORDS)<>466", "Length(S002_RECORDS)<>297")
engine = engine.replace("14623", "14514").replace("14622", "14513")
engine = engine.replace("43149024", "44583936").replace("224649", "194398")
engine = engine.replace('"SHARD\\t001\\tUNIT\\t"', '"SHARD\\t002\\tUNIT\\t"')
engine = engine.replace(
    '"SCOPE\\tExactly seed-plan shard001 only; shard002 and later are excluded.\\n");',
    '"SCOPE\\tExactly seed-plan shard002 only; shard003 and later are excluded.\\n");',
)
anchor = 'required:=["S002_RECORDS","OUT","CHECKPOINT_FILE","CHECKPOINT_TMP","INTERNAL_GUARD_MS",'
assert engine.count(anchor) == 1
atomic_helper = r'''
S002AtomicReplaceVerified:=function(oldpath,newpath)
 local attempt,result,expectedText;
 if not IsExistingFile(oldpath) then return false; fi;
 expectedText:=StringFile(oldpath);
 for attempt in [1..500] do
  result:=IO_rename(oldpath,newpath);
  if result=true then
   if IsExistingFile(oldpath) or not IsExistingFile(newpath) or StringFile(newpath)<>expectedText then
    Print("ATOMIC_RENAME_POSTVERIFY_FAIL\tATTEMPTS\t",attempt,"\n");
    return false;
   fi;
   if attempt>1 then Print("ATOMIC_RENAME_RETRY_SUCCESS\tATTEMPTS\t",attempt,"\n"); fi;
   return true;
  fi;
  IO_select([],[],[],0,20000);
 od;
 Print("ATOMIC_RENAME_RETRY_EXHAUSTED\tATTEMPTS\t500\n");
 return false;
end;
'''.strip() + "\n"
engine = engine.replace(anchor, atomic_helper + anchor)
old_rename = 'if not IO_rename(CHECKPOINT_TMP,CHECKPOINT_FILE) then Error("atomic checkpoint rename failed"); fi;'
new_rename = 'if not S002AtomicReplaceVerified(CHECKPOINT_TMP,CHECKPOINT_FILE) then Error("atomic checkpoint rename/postverify failed"); fi;'
assert engine.count(old_rename) == 1
engine = engine.replace(old_rename, new_rename)
old_recovery = '"RECOVERY\\tAtomic checkpoint is temp-write then same-directory IO_rename after every ALPHA_DONE; it records output-prefix SHA256/bytes and the exact lexicographic successor.\\n",'
new_recovery = '"RECOVERY\\tPer-alpha temp-write plus bounded IO_rename retry; source absence, destination presence, and exact destination bytes are verified after rename; output-prefix SHA256/bytes and exact successor are recorded.\\n",'
assert engine.count(old_recovery) == 1
engine = engine.replace(old_recovery, new_recovery)
for stale in ("S001", "SHARD001", "24T5155", "24T5715\\t66", "14622", "14623", "43149024", "224649"):
    assert stale not in engine, stale
ENGINE.write_text(engine, encoding="ascii", newline="\n")
engine_sha = sha(ENGINE)

profile: dict[int, dict[str, str]] = {}
for line in PROFILE.read_text(encoding="ascii").splitlines():
    if line.startswith("ENTRY\t"):
        parts = line.split("\t")
        match = re.fullmatch(r"24T([0-9]+)", parts[1])
        assert match
        key = int(match.group(1))
        assert key not in profile
        profile[key] = field_map(parts, 2)
assert len(profile) == 10714

work: list[tuple[int, int, int, dict[str, str]]] = []
shard: dict[str, str] | None = None
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[0:2] == ["SHARD", "2"]:
        shard = field_map(parts, 2)
    elif parts[0:2] == ["WORK", "2"]:
        row = field_map(parts, 2)
        work.append((int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), row))
assert shard is not None
assert (len(work), work[0][:3], work[-1][:3]) == (297, (5715, 67, 84), (6031, 1, 8))
assert all(work[i][0] < work[i + 1][0] for i in range(len(work) - 1))
expected_shard = {
    "KEYS_TOUCHED": "297", "CLASS_UNITS": "14513", "RAW_PAIRS": "44583936",
    "PROFILE_REBUILD_MS": "194398", "PAIR_MODEL_MS": "594453",
    "POINT_MODEL_MS": "788851", "FRACTION_INTERNAL_GUARD": "0.597614",
}
for name, value in expected_shard.items():
    assert shard[name] == value

records: list[dict[str, int | str]] = []
slice_lines = [
    "CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD002",
    f"PROFILE_SHA256\t{PROFILE_SHA}", f"PLAN_SHA256\t{PLAN_SHA}",
    "FIRST\t24T5715\t67", "LAST\t24T6031\t8",
]
unit = 1
for key, first, last, work_row in work:
    p = profile[key]
    order = int(p["ORDER"]); classes = int(p["ORDER8_CLASSES"]); units = last - first + 1
    assert classes > 0 and 1 <= first <= last <= classes
    assert int(p["RAW_PAIRS"]) == order * classes
    assert int(work_row["ORDER"]) == order and int(work_row["CLASS_UNITS"]) == units
    assert int(work_row["RAW_PAIRS"]) == order * units
    assert p["ROUTE"] in ("pc", "native")
    if p["ROUTE"] == "pc":
        assert p["REPRESENTATION"] == "legacy_sealed_pc" and int(p["PC_ORDER"]) == order
    else:
        assert p["REPRESENTATION"] == "legacy_original_native" and int(p["PC_ORDER"]) == 0
    rec: dict[str, int | str] = {
        "k": key, "first": first, "last": last, "unitFirst": unit,
        "unitLast": unit + units - 1, "order": order, "autOrder": int(p["AUT_ORDER"]),
        "parity": int(p["PARITY_MAPS"]), "classes": classes, "raw": int(p["RAW_PAIRS"]),
        "method": p["ROUTE"], "representation": p["REPRESENTATION"],
        "pcOrder": int(p["PC_ORDER"]), "profileMs": int(p["PROFILE_COST_MS"]),
    }
    records.append(rec)
    slice_lines.append(
        "WORK\tUNIT_FIRST\t{unitFirst}\tUNIT_LAST\t{unitLast}\tKEY\t24T{k}"
        "\tALPHA_FIRST\t{first}\tALPHA_LAST\t{last}\tORDER\t{order}\tAUT_ORDER\t{autOrder}"
        "\tPARITY_MAPS\t{parity}\tMETHOD\t{method}\tREPRESENTATION\t{representation}"
        "\tPC_ORDER\t{pcOrder}\tORDER8_CLASSES\t{classes}\tFULL_RAW_PAIRS\t{raw}"
        "\tPLANNED_RAW_PAIRS\t{planned}\tPROFILE_COST_MS\t{profileMs}".format(
            **rec, planned=order * units,
        )
    )
    unit += units
assert unit == 14514
assert sum(int(r["order"]) * (int(r["last"]) - int(r["first"]) + 1) for r in records) == 44583936
assert sum(int(r["profileMs"]) for r in records) == 194398
slice_lines.extend([
    "CHECKSUM\tKEYS\t297\tCLASS_UNITS\t14513\tRAW_PAIRS\t44583936\tPROFILE_REBUILD_MS\t194398\tPAIR_MODEL_MS\t594453\tPOINT_MODEL_MS\t788851\tFRACTION_INTERNAL_GUARD\t0.597614",
    "SEED_PREDICATES\tNOT_RUN_BY_BUILDER", "DONE", "",
])
SLICE.write_text("\n".join(slice_lines), encoding="ascii", newline="\n")

record_lines = [
    ('rec(k:={k},first:={first},last:={last},unitFirst:={unitFirst},unitLast:={unitLast},'
     'order:={order},autOrder:={autOrder},parity:={parity},classes:={classes},raw:={raw},'
     'method:="{method}",representation:="{representation}",pcOrder:={pcOrder},profileMs:={profileMs})').format(**r)
    for r in records
]
wrapper = "\n".join([
    "# Exact wrapper for sealed degree-24 seed workload shard002.",
    f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "STOP_AFTER_UNIT:=fail;", "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";',
    'CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt";',
    'CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_TMP_GPT56SOL.txt";',
    f'EXPECTED_PROFILE_SHA256:="{PROFILE_SHA}";', f'EXPECTED_PLAN_SHA256:="{PLAN_SHA}";',
    f'PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/{PROFILE.name}";',
    f'PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/{PLAN.name}";',
    f'ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/{ENGINE.name}";',
    f'EXPECTED_ENGINE_SHA256:="{engine_sha}";', "S002_RECORDS:=[",
    ",\n".join(record_lines), "];",
    f'Read("/mnt/d/work/revise/production_code/escalations/{ENGINE.name}");', "",
])
WRAPPER.write_text(wrapper, encoding="ascii", newline="\n")
RUNNER.write_text(
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n",
    encoding="ascii", newline="\n",
)
print(f"PASS keys=297 units=14513 raw=44583936 profileMs=194398 engine_sha256={engine_sha}")
print(f"SLICE\t{SLICE.name}\tSHA256\t{sha(SLICE)}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{sha(WRAPPER)}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{sha(RUNNER)}")
