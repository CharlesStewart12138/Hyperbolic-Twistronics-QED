#!/usr/bin/env python3
"""Build one exact checkpoint-safe degree-24 seed shard from the sealed plan."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path


B = Path(__file__).resolve().parent
PROFILE = B / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
BASE_ENGINE = B / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard005_v7_v2_gpt56sol.g"
PROFILE_SHA = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
BASE_ENGINE_SHA = "83A61C41F09F2B8ED03416742A2D98AFFA8AB71B3C015732631108177FCBB165"


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


parser = argparse.ArgumentParser()
parser.add_argument("--shard", type=int, required=True)
args = parser.parse_args()
shard = args.shard
assert 6 <= shard <= 905
tag = f"{shard:03d}"

assert digest(PROFILE.read_bytes()) == PROFILE_SHA
assert digest(PLAN.read_bytes()) == PLAN_SHA
assert digest(BASE_ENGINE.read_bytes()) == BASE_ENGINE_SHA

profile: dict[int, dict[str, str]] = {}
for line in PROFILE.read_text(encoding="ascii").splitlines():
    if line.startswith("ENTRY\t"):
        parts = line.split("\t")
        match = re.fullmatch(r"24T([0-9]+)", parts[1])
        assert match
        profile[int(match.group(1))] = fields(parts, 2)
assert len(profile) == 10714

summary: dict[str, str] | None = None
work: list[tuple[int, int, int, dict[str, str]]] = []
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[:2] == ["SHARD", str(shard)]:
        summary = fields(parts, 2)
    elif parts[:2] == ["WORK", str(shard)]:
        row = fields(parts, 2)
        work.append((int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), row))
assert summary is not None
keys = int(summary["KEYS_TOUCHED"])
units_total = int(summary["CLASS_UNITS"])
raw_total = int(summary["RAW_PAIRS"])
profile_ms = int(summary["PROFILE_REBUILD_MS"])
first_key = int(summary["FIRST_KEY"])
first_alpha = int(summary["FIRST_ALPHA"])
last_key = int(summary["LAST_KEY"])
last_alpha = int(summary["LAST_ALPHA"])
assert len(work) == keys and work[0][:3] == (first_key, first_alpha, work[0][2])
assert work[-1][0] == last_key and work[-1][2] == last_alpha
assert all(work[i][0] < work[i + 1][0] for i in range(len(work) - 1))

records: list[dict[str, int | str]] = []
slice_lines = [
    f"CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD{tag}",
    f"PROFILE_SHA256\t{PROFILE_SHA}", f"PLAN_SHA256\t{PLAN_SHA}",
    f"FIRST\t24T{first_key}\t{first_alpha}", f"LAST\t24T{last_key}\t{last_alpha}",
]
unit = 1
for key, first, last, plan_row in work:
    p = profile[key]
    order = int(p["ORDER"])
    classes = int(p["ORDER8_CLASSES"])
    count = last - first + 1
    assert classes > 0 and 1 <= first <= last <= classes
    assert int(p["RAW_PAIRS"]) == order * classes
    assert int(plan_row["ORDER"]) == order and int(plan_row["CLASS_UNITS"]) == count
    assert int(plan_row["RAW_PAIRS"]) == order * count
    route = p["ROUTE"]
    representation = p["REPRESENTATION"]
    pc_order = int(p["PC_ORDER"])
    # Both labels below certify the same Aut(G)-then-pc class reconstruction.
    assert (route == "pc" and representation in {"legacy_sealed_pc", "original", "pc_transport"} and pc_order == order) or (
        route == "native" and representation == "legacy_original_native" and pc_order == 0
    ) or (
        route == "native" and representation in {"pc_single", "pc_transport"} and pc_order == order
    )
    rec: dict[str, int | str] = {
        "k": key, "first": first, "last": last, "unitFirst": unit,
        "unitLast": unit + count - 1, "order": order, "autOrder": int(p["AUT_ORDER"]),
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
            **rec, planned=order * count
        )
    )
    unit += count
assert unit == units_total + 1
assert sum(int(r["order"]) * (int(r["last"]) - int(r["first"]) + 1) for r in records) == raw_total
assert sum(int(r["profileMs"]) for r in records) == profile_ms

slice_lines += [
    f"CHECKSUM\tKEYS\t{keys}\tCLASS_UNITS\t{units_total}\tRAW_PAIRS\t{raw_total}"
    f"\tPROFILE_REBUILD_MS\t{profile_ms}\tPAIR_MODEL_MS\t{summary['PAIR_MODEL_MS']}"
    f"\tPOINT_MODEL_MS\t{summary['POINT_MODEL_MS']}\tFRACTION_INTERNAL_GUARD\t{summary['FRACTION_INTERNAL_GUARD']}",
    "SEED_PREDICATES\tNOT_RUN_BY_BUILDER", "DONE", "",
]
slice_data = "\n".join(slice_lines).encode("ascii")

engine = BASE_ENGINE.read_text(encoding="ascii")
engine = engine.replace("S005", f"S{tag}").replace("SHARD005", f"SHARD{tag}").replace("shard005", f"shard{tag}")
fixed_changes = {
    f"Length(S{tag}_RECORDS)<>283": f"Length(S{tag}_RECORDS)<>{keys}",
    f"S{tag}_RECORDS[1].k<>6769 or S{tag}_RECORDS[1].first<>91":
        f"S{tag}_RECORDS[1].k<>{first_key} or S{tag}_RECORDS[1].first<>{first_alpha}",
    f"S{tag}_RECORDS[Length(S{tag}_RECORDS)].k<>7070":
        f"S{tag}_RECORDS[Length(S{tag}_RECORDS)].k<>{last_key}",
    f"S{tag}_RECORDS[Length(S{tag}_RECORDS)].last<>2":
        f"S{tag}_RECORDS[Length(S{tag}_RECORDS)].last<>{last_alpha}",
    "planUnits<>14648 or planRaw<>44998656 or planProfileMs<>151674 or expectedUnitFirst<>14649":
        f"planUnits<>{units_total} or planRaw<>{raw_total} or planProfileMs<>{profile_ms} or expectedUnitFirst<>{units_total + 1}",
    f"START_UNIT<1 or START_UNIT>14649 or INITIAL_COUNTERS[1]<>START_UNIT-1":
        f"START_UNIT<1 or START_UNIT>{units_total + 1} or INITIAL_COUNTERS[1]<>START_UNIT-1",
    '"PLAN_FIRST\\t24T6769\\t91\\nPLAN_LAST\\t24T7070\\t2\\nPLAN_KEYS\\t283\\n",':
        f'"PLAN_FIRST\\t24T{first_key}\\t{first_alpha}\\nPLAN_LAST\\t24T{last_key}\\t{last_alpha}\\nPLAN_KEYS\\t{keys}\\n",',
    '"PLAN_CLASS_UNITS\\t14648\\nPLAN_RAW_PAIRS\\t44998656\\nPLAN_PROFILE_REBUILD_MS\\t151674\\n",':
        f'"PLAN_CLASS_UNITS\\t{units_total}\\nPLAN_RAW_PAIRS\\t{raw_total}\\nPLAN_PROFILE_REBUILD_MS\\t{profile_ms}\\n",',
    f'"SCOPE\\tExactly seed-plan shard{tag} only; shard006 and later are excluded.\\n");':
        f'"SCOPE\\tExactly seed-plan shard{tag} only; shard{shard + 1:03d} and later are excluded.\\n");',
    "START_UNIT<=14648": f"START_UNIT<={units_total}",
    '"SHARD\\t005\\tUNIT\\t"': f'"SHARD\\t{tag}\\tUNIT\\t"',
    "completedUnits<>14648 or rawPairs<>44998656 or lastUnit<>14648":
        f"completedUnits<>{units_total} or rawPairs<>{raw_total} or lastUnit<>{units_total}",
    f'if row.representation<>"legacy_sealed_pc" or row.pcOrder<>row.order then Error("S{tag} pc representation"); fi;':
        f'if (row.representation<>"legacy_sealed_pc" and row.representation<>"original" and row.representation<>"pc_transport") or row.pcOrder<>row.order then Error("S{tag} pc representation"); fi;',
    f'if row.representation<>"legacy_original_native" or row.pcOrder<>0 then Error("S{tag} native representation"); fi;':
        f'if not ((row.representation="legacy_original_native" and row.pcOrder=0) or ((row.representation="pc_single" or row.representation="pc_transport") and row.pcOrder=row.order)) then Error("S{tag} native representation"); fi;',
    """G:=TransitiveGroup(24,row.k); n:=Size(G); keyStart:=Runtime();
  if n<>row.order or n<2338 or n>50000 then Error("profile order/window mismatch"); fi;
  maps:=GQuotients(G,CyclicGroup(2));
  if Length(maps)<>row.parity or Length(maps)=0 then Error("profile parity mismatch"); fi;
  A:=AutomorphismGroup(G);""":
        """G0:=TransitiveGroup(24,row.k); n:=Size(G0); keyStart:=Runtime();
  if n<>row.order or n<2338 or n>50000 then Error("profile order/window mismatch"); fi;
  transportG:=row.representation="pc_single" or row.representation="pc_transport";
  if transportG then
   isoG:=IsomorphismPcGroup(G0); G:=Image(isoG);
   if Size(G)<>n or row.pcOrder<>Size(G) then Error("profile transported-domain mismatch"); fi;
   mapsOriginal:=GQuotients(G0,CyclicGroup(2)); maps:=GQuotients(G,CyclicGroup(2));
   if Length(mapsOriginal)<>row.parity or Length(maps)<>row.parity or Length(maps)=0 then Error("profile transported parity mismatch"); fi;
   AppendTo(OUT,"TRANSPORT_OK\\t24T",row.k,"\\tREPRESENTATION\\t",row.representation,
    "\\tORIGINAL_ORDER\\t",n,"\\tPC_ORDER\\t",Size(G),"\\tPARITY_ORIGINAL\\t",Length(mapsOriginal),
    "\\tPARITY_PC\\t",Length(maps),"\\n");
  else
   G:=G0; maps:=GQuotients(G,CyclicGroup(2));
   if Length(maps)<>row.parity or Length(maps)=0 then Error("profile parity mismatch"); fi;
  fi;
  A:=AutomorphismGroup(G);""",
    'for x in reps do\n    repNo:=repNo+1; PrintNumericCandidate(OUT,row.k,alphaNo,repNo,n,PhysicalOrbit(alpha,x));':
        'for x in reps do\n    repNo:=repNo+1; seedCandidateXs:=PhysicalOrbit(alpha,x); candidateXs:=seedCandidateXs;\n    if transportG then\n     candidateXs:=List(seedCandidateXs,y->PreImagesRepresentative(isoG,y));\n     if ForAny(candidateXs,y->y=fail or not IsPerm(y) or not (y in G0)) or not ForAll([1..8],j->Image(isoG,candidateXs[j])=seedCandidateXs[j]) then Error("candidate transport mismatch"); fi;\n    fi;\n    PrintNumericCandidate(OUT,row.k,alphaNo,repNo,n,candidateXs);',
}
for old, new in fixed_changes.items():
    assert engine.count(old) == 1, old
    engine = engine.replace(old, new)

engine_name = f"gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard{tag}_v7_gpt56sol.g"
slice_name = f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PLAN_SLICE_GPT56SOL.tsv"
wrapper_name = f"gap_run_degree24_c8_seed_shard{tag}_segment001_unit1_{units_total}_postverify_v7_gpt56sol.g"
runner_name = f"run_degree24_c8_seed_shard{tag}_segment001_postverify_v7.sh"
parse_name = f"gap_parse_smoke_degree24_c8_seed_shard{tag}_v7_gpt56sol.g"
output_name = f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT001_UNIT1_{units_total}_POSTVERIFY_V7_GPT56SOL.txt"
checkpoint_name = f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CHECKPOINT_GPT56SOL.txt"
checkpoint_tmp_name = f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CHECKPOINT_TMP_GPT56SOL.txt"
paths = [B / name for name in (engine_name, slice_name, wrapper_name, runner_name, parse_name,
                                output_name, checkpoint_name, checkpoint_tmp_name)]
for path in paths:
    assert not path.exists(), f"no-clobber {path}"
atomic_write(B / engine_name, engine.encode("ascii"))
atomic_write(B / slice_name, slice_data)
engine_sha = digest(engine.encode("ascii"))

record_lines = [
    ('rec(k:={k},first:={first},last:={last},unitFirst:={unitFirst},unitLast:={unitLast},'
     'order:={order},autOrder:={autOrder},parity:={parity},classes:={classes},raw:={raw},'
     'method:="{method}",representation:="{representation}",pcOrder:={pcOrder},profileMs:={profileMs})').format(**r)
    for r in records
]
wrapper_lines = [
    f"# Exact wrapper for sealed degree-24 seed workload shard{tag}.",
    f'OUT:="/mnt/d/work/revise/production_code/escalations/{output_name}";',
    "STOP_AFTER_UNIT:=fail;", "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";',
    f'CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/{checkpoint_name}";',
    f'CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/{checkpoint_tmp_name}";',
    f'EXPECTED_PROFILE_SHA256:="{PROFILE_SHA}";', f'EXPECTED_PLAN_SHA256:="{PLAN_SHA}";',
    f'PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/{PROFILE.name}";',
    f'PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/{PLAN.name}";',
    f'ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/{engine_name}";',
    f'EXPECTED_ENGINE_SHA256:="{engine_sha}";', f"S{tag}_RECORDS:=[", ",\n".join(record_lines), "];",
    f'Read("/mnt/d/work/revise/production_code/escalations/{engine_name}");', "",
]
wrapper_data = "\n".join(wrapper_lines).encode("ascii")
runner_data = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{wrapper_name}\n"
).encode("ascii")
parse_data = (
    f'f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{wrapper_name}");\n'
    f'if f=fail then Error("S{tag} wrapper parse failed"); fi;\n'
    f'g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{engine_name}");\n'
    f'if g=fail then Error("S{tag} engine parse failed"); fi;\n'
    f'Print("SHARD{tag}_V7_WRAPPER_ENGINE_PARSE_PASS\\n");\nQUIT_GAP(0);\n'
).encode("ascii")
atomic_write(B / wrapper_name, wrapper_data)
atomic_write(B / runner_name, runner_data)
atomic_write(B / parse_name, parse_data)
native = sum(r["method"] == "native" for r in records)
print(f"PASS SHARD={tag} KEYS={keys} UNITS={units_total} RAW={raw_total} PROFILE_MS={profile_ms} NATIVE={native}")
print(f"BOUNDARY=24T{first_key}:a{first_alpha}..24T{last_key}:a{last_alpha}")
print(f"ENGINE={engine_name} SHA256={engine_sha}")
print(f"SLICE={slice_name} BYTES={len(slice_data)} SHA256={digest(slice_data)}")
print(f"WRAPPER={wrapper_name} SHA256={digest(wrapper_data)}")
print(f"RUNNER={runner_name} SHA256={digest(runner_data)}")
print(f"PARSE={parse_name} SHA256={digest(parse_data)}")
