from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
profile_name = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
plan_name = "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
slice_name = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_PLAN_SLICE_GPT56SOL.tsv"
wrapper_name = "gap_run_degree24_c8_seed_shard001_gpt56sol.g"
engine_name = "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_gpt56sol.g"


def must(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest().upper()


def fields(parts: list[str], start: int) -> dict[str, str]:
    must((len(parts) - start) % 2 == 0, "malformed fields")
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        must(parts[index] not in result, f"duplicate {parts[index]}")
        result[parts[index]] = parts[index + 1]
    return result


profile_path = base / profile_name
plan_path = base / plan_name
engine_path = base / engine_name
must(engine_path.is_file(), "missing engine")
profile_sha = digest(profile_path)
plan_sha = digest(plan_path)
must(profile_sha == "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2", "profile hash")
must(plan_sha == "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2", "plan hash")

profile: dict[int, dict[str, str]] = {}
for line in profile_path.read_text(encoding="utf-8").splitlines():
    if line.startswith("ENTRY\t"):
        parts = line.split("\t")
        match = re.fullmatch(r"24T(\d+)", parts[1])
        must(match is not None, "profile key")
        key = int(match.group(1))
        must(key not in profile, f"duplicate profile key {key}")
        profile[key] = fields(parts, 2)
must(len(profile) == 10714, "profile key count")

work: list[tuple[int, int, int, dict[str, str]]] = []
shard_record: dict[str, str] | None = None
for line in plan_path.read_text(encoding="utf-8").splitlines():
    parts = line.split("\t")
    if parts[0] == "SHARD" and parts[1] == "1":
        shard_record = fields(parts, 2)
    elif parts[0] == "WORK" and parts[1] == "1":
        row = fields(parts, 2)
        work.append((int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), row))

must(shard_record is not None, "missing shard row")
must(len(work) == 466, "work segment count")
must(work[0][:3] == (5155, 1, 88), "first segment")
must(work[-1][:3] == (5715, 1, 66), "last segment")
must(all(work[i][0] < work[i + 1][0] for i in range(len(work) - 1)), "strict key order")
must(int(shard_record["KEYS_TOUCHED"]) == 466, "shard key count")
must(int(shard_record["CLASS_UNITS"]) == 14622, "shard class units")
must(int(shard_record["RAW_PAIRS"]) == 43149024, "shard raw")
must(int(shard_record["PROFILE_REBUILD_MS"]) == 224649, "shard profile model")
must(int(shard_record["PAIR_MODEL_MS"]) == 575321, "shard pair model")
must(int(shard_record["POINT_MODEL_MS"]) == 799970, "shard point model")

unit = 1
records: list[dict[str, int | str]] = []
slice_lines = [
    "CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD001",
    f"PROFILE_SHA256\t{profile_sha}",
    f"PLAN_SHA256\t{plan_sha}",
    "FIRST\t24T5155\t1",
    "LAST\t24T5715\t66",
]
for key, first, last, work_row in work:
    must(key in profile, f"missing profile key {key}")
    row = profile[key]
    order = int(row["ORDER"])
    classes = int(row["ORDER8_CLASSES"])
    raw = int(row["RAW_PAIRS"])
    units = last - first + 1
    must(classes > 0 and 1 <= first <= last <= classes, f"alpha bounds {key}")
    must(raw == order * classes, f"profile raw {key}")
    must(int(work_row["ORDER"]) == order, f"work order {key}")
    must(int(work_row["CLASS_UNITS"]) == units, f"work units {key}")
    must(int(work_row["RAW_PAIRS"]) == order * units, f"work raw {key}")
    must(row["ROUTE"] in ("pc", "native"), f"route {key}")
    unit_first, unit_last = unit, unit + units - 1
    record: dict[str, int | str] = {
        "k": key, "first": first, "last": last, "unitFirst": unit_first,
        "unitLast": unit_last, "order": order, "autOrder": int(row["AUT_ORDER"]),
        "parity": int(row["PARITY_MAPS"]), "classes": classes, "raw": raw,
        "method": row["ROUTE"], "profileMs": int(row["PROFILE_COST_MS"]),
    }
    records.append(record)
    slice_lines.append(
        "WORK\tUNIT_FIRST\t{}\tUNIT_LAST\t{}\tKEY\t24T{}\tALPHA_FIRST\t{}\tALPHA_LAST\t{}"
        "\tORDER\t{}\tAUT_ORDER\t{}\tPARITY_MAPS\t{}\tMETHOD\t{}\tORDER8_CLASSES\t{}"
        "\tFULL_RAW_PAIRS\t{}\tPLANNED_RAW_PAIRS\t{}\tPROFILE_COST_MS\t{}".format(
            unit_first, unit_last, key, first, last, order, record["autOrder"], record["parity"],
            record["method"], classes, raw, order * units, record["profileMs"]
        )
    )
    unit = unit_last + 1

must(unit == 14623, "unit endpoint")
must(sum(int(r["order"]) * (int(r["last"]) - int(r["first"]) + 1) for r in records) == 43149024, "raw checksum")
must(sum(int(r["profileMs"]) for r in records) == 224649, "profile checksum")
slice_lines.extend([
    "CHECKSUM\tKEYS\t466\tCLASS_UNITS\t14622\tRAW_PAIRS\t43149024\tPROFILE_REBUILD_MS\t224649\tPAIR_MODEL_MS\t575321\tPOINT_MODEL_MS\t799970",
    "SEED_PREDICATES\tNOT_RUN_BY_BUILDER",
    "DONE",
])

record_lines = []
for r in records:
    record_lines.append(
        'rec(k:={k},first:={first},last:={last},unitFirst:={unitFirst},unitLast:={unitLast},'
        'order:={order},autOrder:={autOrder},parity:={parity},classes:={classes},raw:={raw},'
        'method:="{method}",profileMs:={profileMs})'.format(**r)
    )

wrapper = "\n".join([
    "# Generated exact wrapper for sealed degree-24 seed workload shard001.",
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL.txt";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    f'EXPECTED_PROFILE_SHA256:="{profile_sha}";',
    f'EXPECTED_PLAN_SHA256:="{plan_sha}";',
    "S001_RECORDS:=[",
    ",\n".join(record_lines),
    "];",
    'Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_gpt56sol.g");',
    "",
])

slice_path = base / slice_name
wrapper_path = base / wrapper_name
if slice_path.exists() or wrapper_path.exists():
    raise FileExistsError("shard001 generated file already exists")
slice_path.write_text("\n".join(slice_lines) + "\n", encoding="utf-8", newline="\n")
wrapper_path.write_text(wrapper, encoding="utf-8", newline="\n")
print(
    f"PASS wrapper={wrapper_name} slice={slice_name} keys=466 units=14622 raw=43149024 "
    f"profileMs=224649 first=24T5155:1 last=24T5715:66 profileSha={profile_sha} planSha={plan_sha} noSeeds=PASS"
)
