from __future__ import annotations

import hashlib
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()


def must(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest().upper()


def kv(parts: list[str], start: int) -> dict[str, str]:
    must((len(parts) - start) % 2 == 0, "malformed key/value record")
    out: dict[str, str] = {}
    for i in range(start, len(parts), 2):
        must(parts[i] not in out, f"duplicate label {parts[i]}")
        out[parts[i]] = parts[i + 1]
    return out


def after(parts: list[str], label: str) -> str:
    i = parts.index(label)
    return parts[i + 1]


profile = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
plan = base / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
manifest = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AND_SEED_PLAN_GPT56SOL_MANIFEST.sha256"

profile_lines = profile.read_text(encoding="utf-8").splitlines()
must(profile_lines[0] == "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-MERGED", "profile header")
must(profile_lines[-1] == "DONE", "profile DONE")
must(sum(line.startswith("TOTAL\t") for line in profile_lines) == 1, "unique profile TOTAL")

entries: dict[int, dict[str, str]] = {}
ordered_keys: list[int] = []
total_parts: list[str] | None = None
for line in profile_lines:
    parts = line.split("\t")
    if parts[0] == "ENTRY":
        match = re.fullmatch(r"24T(\d+)", parts[1])
        must(match is not None, "profile key syntax")
        key = int(match.group(1))
        must(key not in entries, f"duplicate profile key {key}")
        entries[key] = kv(parts, 2)
        ordered_keys.append(key)
    elif parts[0] == "TOTAL":
        total_parts = parts

must(total_parts is not None, "profile TOTAL")
must(ordered_keys == sorted(ordered_keys), "deterministic profile key order")
must(len(entries) == int(after(total_parts, "PARITY_KEYS")) == 10714, "profile key total")
must(int(after(total_parts, "ORDER_WINDOW")) == 10829, "order-window total")
must(int(after(total_parts, "SCAN_CHECKPOINTS")) == 1000, "scan-checkpoint total")

classes: dict[int, int] = {}
raws: dict[int, int] = {}
orders: dict[int, int] = {}
costs: dict[int, int] = {}
routes: Counter[str] = Counter()
solvability: Counter[str] = Counter()
for key, row in entries.items():
    order = int(row["ORDER"])
    count = int(row["ORDER8_CLASSES"])
    raw = int(row["RAW_PAIRS"])
    cost = int(row["PROFILE_COST_MS"])
    must(raw == order * count, f"RAW_PAIRS=Size(G)*classes 24T{key}")
    must(cost == int(row["ISO_MS"]) + int(row["AUT_MS"]) + int(row["CLASS_MS"]), f"profile cost 24T{key}")
    must(int(row["PC_ORDER"]) == order, f"transport identity 24T{key}")
    must(int(row["PARITY_MAPS"]) > 0, f"parity existence 24T{key}")
    must(row["ROUTE"] in ("pc", "native"), f"route 24T{key}")
    must(row["SOLVABLE_G"] in ("true", "false"), f"solvability 24T{key}")
    if row["SOLVABLE_G"] == "false":
        must(row["ROUTE"] == "native", f"nonsolvable native 24T{key}")
    classes[key], raws[key], orders[key], costs[key] = count, raw, order, cost
    routes[row["ROUTE"]] += 1
    solvability[row["SOLVABLE_G"]] += 1

must(sum(classes.values()) == int(after(total_parts, "ORDER8_CLASSES")) == 1474201, "profile class sum")
must(sum(raws.values()) == int(after(total_parts, "RAW_PAIRS")) == 40656212448, "profile raw sum")
must(sum(costs.values()) == int(after(total_parts, "PROFILE_COST_MS")) == 12311118, "profile cost sum")
must(sum(v > 0 for v in classes.values()) == 9962, "positive keys")
must(sum(v == 0 for v in classes.values()) == 752, "zero keys")
must(routes == Counter({"pc": 10493, "native": 221}), "route totals")
must(solvability == Counter({"true": 10537, "false": 177}), "solvability totals")

plan_lines = plan.read_text(encoding="utf-8").splitlines()
must(plan_lines[0] == "CERTIFICATE_PLAN\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-C8-SEED-WORKLOAD", "plan header")
must(plan_lines[-1] == "DONE", "plan DONE")
must(sum(line.startswith("CHECKSUM\t") for line in plan_lines) == 1, "unique CHECKSUM")

shards: dict[int, dict[str, str]] = {}
work: list[tuple[int, int, int, int, int, int]] = []
checksum: dict[str, str] | None = None
for line in plan_lines:
    parts = line.split("\t")
    if parts[0] == "SHARD":
        number = int(parts[1])
        must(number not in shards, f"duplicate shard {number}")
        shards[number] = kv(parts, 2)
    elif parts[0] == "WORK":
        row = kv(parts, 2)
        work.append((int(parts[1]), int(row["KEY"]), int(row["ALPHA_FIRST"]), int(row["ALPHA_LAST"]), int(row["ORDER"]), int(row["RAW_PAIRS"])))
    elif parts[0] == "CHECKSUM":
        checksum = kv(parts, 1)

must(checksum is not None, "plan checksum")
must(sorted(shards) == list(range(1, 906)), "shard numbering")
must(len(work) == 10864, "work segment count")

assigned_classes: Counter[int] = Counter()
assigned_raw: Counter[int] = Counter()
work_by_shard: dict[int, list[tuple[int, int, int, int, int]]] = defaultdict(list)
previous: tuple[int, int] | None = None
for number, key, first, last, order, raw in work:
    must(number in shards and key in entries and classes[key] > 0, "work target")
    must(1 <= first <= last <= classes[key], f"alpha interval 24T{key}")
    must(order == orders[key], f"work order 24T{key}")
    units = last - first + 1
    must(raw == units * order, f"work raw 24T{key}")
    if previous:
        pkey, plast = previous
        must(key > pkey or (key == pkey and first == plast + 1), f"lex order 24T{key}")
        if key > pkey:
            must(plast == classes[pkey] and first == 1, f"key boundary 24T{key}")
    assigned_classes[key] += units
    assigned_raw[key] += raw
    work_by_shard[number].append((key, first, last, order, raw))
    previous = (key, last)

positive = {key for key, value in classes.items() if value > 0}
must(set(assigned_classes) == positive, "positive key union")
for key in positive:
    must(assigned_classes[key] == classes[key], f"class coverage 24T{key}")
    must(assigned_raw[key] == raws[key], f"raw coverage 24T{key}")

raw_values: list[int] = []
point_values: list[int] = []
repeated_profile = 0
split_occurrences: Counter[int] = Counter()
for number in range(1, 906):
    row = shards[number]
    rows = work_by_shard[number]
    must(rows, f"empty shard {number}")
    touched = sorted({item[0] for item in rows})
    for key in touched:
        split_occurrences[key] += 1
    raw = sum(item[4] for item in rows)
    units = sum(item[2] - item[1] + 1 for item in rows)
    profile_cost = sum(costs[key] for key in touched)
    pair_cost = math.ceil(raw / 75)
    point = profile_cost + pair_cost
    must((int(row["FIRST_KEY"]), int(row["FIRST_ALPHA"])) == (rows[0][0], rows[0][1]), f"shard first {number}")
    must((int(row["LAST_KEY"]), int(row["LAST_ALPHA"])) == (rows[-1][0], rows[-1][2]), f"shard last {number}")
    must(int(row["KEYS_TOUCHED"]) == len(touched), f"shard key count {number}")
    must(int(row["CLASS_UNITS"]) == units, f"shard class count {number}")
    must(int(row["RAW_PAIRS"]) == raw <= 45000000, f"shard raw {number}")
    must(int(row["PROFILE_REBUILD_MS"]) == profile_cost, f"shard profile cost {number}")
    must(int(row["PAIR_MODEL_MS"]) == pair_cost, f"shard pair cost {number}")
    must(int(row["POINT_MODEL_MS"]) == point <= 800000, f"shard point cost {number}")
    raw_values.append(raw)
    point_values.append(point)
    repeated_profile += profile_cost

must(sum(1 for count in split_occurrences.values() if count > 1) == 806, "split-key count")
must(int(checksum["SHARDS"]) == 905 and int(checksum["WORK_SEGMENTS"]) == 10864, "plan dimensions")
must(int(checksum["CLASS_UNITS"]) == sum(assigned_classes.values()) == 1474201, "plan class total")
must(int(checksum["RAW_PAIRS"]) == sum(raw_values) == 40656212448, "plan raw total")
must(int(checksum["REPEATED_PROFILE_MS"]) == repeated_profile == 15397849, "plan repeated profile")
must(int(checksum["TOTAL_POINT_MODEL_MS"]) == sum(point_values) == 557481315, "plan model total")
must((min(raw_values), max(raw_values)) == (20889600, 44999712), "plan raw extrema")
must((min(point_values), max(point_values)) == (280846, 799997), "plan point extrema")

manifest_lines = manifest.read_text(encoding="ascii").splitlines()
must(len(manifest_lines) == 170, "manifest count")
manifest_names: set[str] = set()
for line in manifest_lines:
    match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
    must(match is not None, "manifest syntax")
    name = match.group(2)
    must(name not in manifest_names, f"manifest duplicate {name}")
    must(sha256(base / name) == match.group(1), f"manifest mismatch {name}")
    manifest_names.add(name)

for record in (
    "CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-SECOND-AUDIT-V2",
    "AUDIT_METHOD\tIndependent parser; merge builder code not imported.",
    "PROFILE_KEYS\t10714\tDUPLICATES\t0\tPASS",
    "ORDER_WINDOW\t10829\tPASS",
    "ORDER8_CLASSES\t1474201\tPASS",
    "RAW_PAIRS\t40656212448\tPASS",
    "FROZEN_RAW_IDENTITIES\t10714\tPASS",
    "SEED_PLAN_SHARDS\t905\tPASS",
    "WORK_SEGMENTS\t10864\tPASS",
    "POSITIVE_ALPHA_KEY_COVERAGE\t9962\tGAPS\t0\tDUPLICATES\t0\tPASS",
    "SHARD_RAW_MIN_MAX\t20889600\t44999712\tCAP\t45000000\tPASS",
    "SHARD_POINT_MIN_MAX_MS\t280846\t799997\tCAP\t800000\tPASS",
    "TOTAL_POINT_MODEL_MS\t557481315\tPASS",
    "CANONICAL_MANIFEST_ENTRIES\t170\tMISMATCHES\t0\tPASS",
    "SEED_PREDICATES_RUN\t0\tPASS",
    "VERIFY\tPASS",
    "DONE",
):
    print(record)
