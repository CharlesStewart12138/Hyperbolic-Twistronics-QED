from __future__ import annotations

import hashlib
import math
import re
import sys
from collections import Counter
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest().upper()


def fields(parts: list[str], start: int) -> dict[str, str]:
    require((len(parts) - start) % 2 == 0, "odd field/value column count")
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        require(parts[index] not in result, f"duplicate field {parts[index]}")
        result[parts[index]] = parts[index + 1]
    return result


dataset_path = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
plan_path = base / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
manifest_path = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AND_SEED_PLAN_GPT56SOL_MANIFEST.sha256"

entries: dict[int, dict[str, str]] = {}
entry_order: list[int] = []
dataset_total: dict[str, str] | None = None
dataset_lines = dataset_path.read_text(encoding="utf-8").splitlines()
require(dataset_lines[0] == "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-MERGED", "dataset header")
require(dataset_lines[-1] == "DONE", "dataset terminal")
for line in dataset_lines:
    parts = line.split("\t")
    if parts[0] == "ENTRY":
        match = re.fullmatch(r"24T(\d+)", parts[1])
        require(match is not None, "entry key")
        key = int(match.group(1))
        require(key not in entries, f"duplicate key {key}")
        entries[key] = fields(parts, 2)
        entry_order.append(key)
    elif parts[0] == "TOTAL":
        require(dataset_total is None, "multiple dataset TOTAL")
        dataset_total = fields(parts, 1)

require(dataset_total is not None, "missing dataset TOTAL")
require(entry_order == sorted(entry_order), "dataset deterministic key order")
require(len(entries) == 10714, "eligible key count")
require(int(dataset_total["ORDER_WINDOW"]) == 10829, "window total")
require(int(dataset_total["PARITY_KEYS"]) == 10714, "parity total")
require(int(dataset_total["SCAN_CHECKPOINTS"]) == 1000, "scan checkpoint total")

classes_by_key: dict[int, int] = {}
raw_by_key: dict[int, int] = {}
order_by_key: dict[int, int] = {}
profile_by_key: dict[int, int] = {}
route_counts: Counter[str] = Counter()
solvable_counts: Counter[str] = Counter()
for key, data in entries.items():
    order = int(data["ORDER"])
    classes = int(data["ORDER8_CLASSES"])
    raw = int(data["RAW_PAIRS"])
    profile = int(data["PROFILE_COST_MS"])
    require(raw == order * classes, f"frozen raw identity 24T{key}")
    require(profile == int(data["ISO_MS"]) + int(data["AUT_MS"]) + int(data["CLASS_MS"]), f"profile cost 24T{key}")
    require(int(data["PC_ORDER"]) == order, f"transport order 24T{key}")
    require(int(data["PARITY_MAPS"]) > 0, f"parity map 24T{key}")
    require(data["ROUTE"] in {"pc", "native"}, f"route 24T{key}")
    if data["SOLVABLE_G"] == "false":
        require(data["ROUTE"] == "native", f"nonsolvable route 24T{key}")
    classes_by_key[key] = classes
    raw_by_key[key] = raw
    order_by_key[key] = order
    profile_by_key[key] = profile
    route_counts[data["ROUTE"]] += 1
    solvable_counts[data["SOLVABLE_G"]] += 1

require(sum(classes_by_key.values()) == 1474201, "class sum")
require(sum(raw_by_key.values()) == 40656212448, "raw sum")
require(sum(profile_by_key.values()) == 12311118, "profile time sum")
require(sum(value > 0 for value in classes_by_key.values()) == 9962, "positive class keys")
require(sum(value == 0 for value in classes_by_key.values()) == 752, "zero class keys")
require(route_counts == Counter({"pc": 10493, "native": 221}), "route counts")
require(solvable_counts == Counter({"true": 10537, "false": 177}), "solvability counts")

shard_rows: dict[int, dict[str, str]] = {}
work_rows: list[tuple[int, int, int, int, int, int]] = []
checksum: dict[str, str] | None = None
plan_lines = plan_path.read_text(encoding="utf-8").splitlines()
require(plan_lines[0] == "CERTIFICATE_PLAN\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-C8-SEED-WORKLOAD", "plan header")
require(plan_lines[-1] == "DONE", "plan terminal")
for line in plan_lines:
    parts = line.split("\t")
    if parts[0] == "SHARD":
        number = int(parts[1])
        require(number not in shard_rows, f"duplicate shard {number}")
        shard_rows[number] = fields(parts, 2)
    elif parts[0] == "WORK":
        number = int(parts[1])
        data = fields(parts, 2)
        work_rows.append((number, int(data["KEY"]), int(data["ALPHA_FIRST"]), int(data["ALPHA_LAST"]), int(data["ORDER"]), int(data["RAW_PAIRS"])))
    elif parts[0] == "CHECKSUM":
        require(checksum is None, "multiple plan CHECKSUM")
        checksum = fields(parts, 1)

require(checksum is not None, "missing plan checksum")
require(sorted(shard_rows) == list(range(1, 906)), "shard numbering")
require(len(work_rows) == 10864, "work segment count")

assigned_classes: Counter[int] = Counter()
assigned_raw: Counter[int] = Counter()
previous: tuple[int, int] | None = None
work_by_shard: dict[int, list[tuple[int, int, int, int, int]]] = {number: [] for number in shard_rows}
for number, key, first, last, order, raw in work_rows:
    require(number in shard_rows, f"unknown shard {number}")
    require(key in entries and classes_by_key[key] > 0, f"unknown/zero key 24T{key}")
    require(1 <= first <= last <= classes_by_key[key], f"alpha bounds 24T{key}")
    require(order == order_by_key[key], f"work order 24T{key}")
    units = last - first + 1
    require(raw == units * order, f"work raw 24T{key}")
    if previous is not None:
        prev_key, prev_last = previous
        require(key > prev_key or (key == prev_key and first == prev_last + 1), f"lexicographic discontinuity 24T{key}")
        if key > prev_key:
            require(first == 1, f"new key alpha start 24T{key}")
            require(prev_last == classes_by_key[prev_key], f"previous key alpha end 24T{prev_key}")
    assigned_classes[key] += units
    assigned_raw[key] += raw
    work_by_shard[number].append((key, first, last, order, raw))
    previous = (key, last)

positive_keys = {key for key, value in classes_by_key.items() if value > 0}
require(set(assigned_classes) == positive_keys, "positive key union")
for key in positive_keys:
    require(assigned_classes[key] == classes_by_key[key], f"class coverage 24T{key}")
    require(assigned_raw[key] == raw_by_key[key], f"raw coverage 24T{key}")

point_values: list[int] = []
raw_values: list[int] = []
repeated_profile = 0
for number in range(1, 906):
    row = shard_rows[number]
    work = work_by_shard[number]
    require(work, f"empty shard {number}")
    touched = sorted({item[0] for item in work})
    raw = sum(item[4] for item in work)
    units = sum(item[2] - item[1] + 1 for item in work)
    profile = sum(profile_by_key[key] for key in touched)
    pair_model = math.ceil(raw / 75)
    point = profile + pair_model
    require(int(row["FIRST_KEY"]) == work[0][0] and int(row["FIRST_ALPHA"]) == work[0][1], f"shard {number} first")
    require(int(row["LAST_KEY"]) == work[-1][0] and int(row["LAST_ALPHA"]) == work[-1][2], f"shard {number} last")
    require(int(row["KEYS_TOUCHED"]) == len(touched), f"shard {number} keys")
    require(int(row["CLASS_UNITS"]) == units, f"shard {number} class units")
    require(int(row["RAW_PAIRS"]) == raw <= 45000000, f"shard {number} raw cap")
    require(int(row["PROFILE_REBUILD_MS"]) == profile, f"shard {number} profile model")
    require(int(row["PAIR_MODEL_MS"]) == pair_model, f"shard {number} pair model")
    require(int(row["POINT_MODEL_MS"]) == point <= 800000, f"shard {number} point cap")
    raw_values.append(raw)
    point_values.append(point)
    repeated_profile += profile

require(int(checksum["SHARDS"]) == 905, "checksum shards")
require(int(checksum["WORK_SEGMENTS"]) == 10864, "checksum segments")
require(int(checksum["CLASS_UNITS"]) == sum(assigned_classes.values()) == 1474201, "checksum classes")
require(int(checksum["RAW_PAIRS"]) == sum(raw_values) == 40656212448, "checksum raw")
require(int(checksum["REPEATED_PROFILE_MS"]) == repeated_profile == 15397849, "checksum profile")
require(int(checksum["TOTAL_POINT_MODEL_MS"]) == sum(point_values) == 557481315, "checksum point")
require(int(checksum["MIN_RAW"]) == min(raw_values) == 20889600, "minimum raw")
require(int(checksum["MAX_RAW"]) == max(raw_values) == 44999712, "maximum raw")
require(int(checksum["MIN_POINT_MS"]) == min(point_values) == 280846, "minimum point")
require(int(checksum["MAX_POINT_MS"]) == max(point_values) == 799997, "maximum point")

manifest_lines = manifest_path.read_text(encoding="ascii").splitlines()
require(len(manifest_lines) == 170, "manifest entry count")
seen_manifest: set[str] = set()
for line in manifest_lines:
    match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
    require(match is not None, "manifest syntax")
    name = match.group(2)
    require(name not in seen_manifest, f"manifest duplicate {name}")
    require(digest(base / name) == match.group(1), f"manifest hash {name}")
    seen_manifest.add(name)

result = [
    "CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-SECOND-AUDIT",
    "AUDIT_METHOD\tIndependent parser over canonical full dataset, lexicographic plan, and manifest; builder logic not imported.",
    "PROFILE_KEYS\t10714\tDUPLICATES\t0\tORDERED\tPASS",
    "ORDER_WINDOW\t10829\tPASS",
    "SOLVABLE_NONSOLVABLE\t10537\t177\tPASS",
    "PC_NATIVE_ROUTES\t10493\t221\tPASS",
    "FROZEN_RAW_IDENTITIES\t10714\tPASS",
    "ORDER8_CLASSES\t1474201\tPASS",
    "RAW_PAIRS\t40656212448\tPASS",
    "PROFILE_COST_MS\t12311118\tPASS",
    "SEED_PLAN_SHARDS\t905\tPASS",
    "WORK_SEGMENTS\t10864\tPASS",
    "POSITIVE_KEY_ALPHA_COVERAGE\t9962\tDUPLICATES\t0\tGAPS\t0\tPASS",
    "SEED_CLASS_UNITS\t1474201\tPASS",
    "SEED_RAW_PAIRS\t40656212448\tPASS",
    "SHARD_RAW_MIN_MAX\t20889600\t44999712\tCAP\t45000000\tPASS",
    "SHARD_POINT_MIN_MAX_MS\t280846\t799997\tCAP\t800000\tPASS",
    "TOTAL_POINT_MODEL_MS\t557481315\tPASS",
    "CANONICAL_MANIFEST_ENTRIES\t170\tMISMATCHES\t0\tPASS",
    "SEED_PREDICATES_RUN\t0\tPASS",
    "VERIFY\tPASS",
    "DONE",
]
out = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_GPT56SOL.txt"
if out.exists():
    raise FileExistsError(out)
out.write_text("\n".join(result) + "\n", encoding="utf-8", newline="\n")
print("PASS independent second audit keys=10714 classes=1474201 raw=40656212448 shards=905 work=10864 manifest=170 mismatches=0 noSeeds=PASS")
