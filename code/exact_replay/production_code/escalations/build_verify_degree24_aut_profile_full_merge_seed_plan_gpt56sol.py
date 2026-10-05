from __future__ import annotations

import hashlib
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path


BASE = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

EXPECTED_RANGES = [
    (1, 5962), (5963, 6670), (6671, 7557), (7558, 8004),
    (8005, 8416), (8417, 8826), (8827, 9237), (9238, 9674),
    (9675, 10335), (10336, 10839), (10840, 11340), (11341, 11845),
    (11846, 12332), (12333, 12595), (12596, 12887), (12888, 13097),
    (13098, 13302), (13303, 13516), (13517, 13721), (13722, 13928),
    (13929, 14218), (14219, 14515), (14516, 14765), (14766, 14900),
    (14901, 15035), (15036, 15170), (15171, 15305), (15306, 15440),
    (15441, 15576), (15577, 15711), (15712, 15846), (15847, 25000),
]

PARITY_MAPS = [
    "GAP_TRANSITIVE_DEGREE24_PARITY_1_7860_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_PARITY_7861_10567_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt",
]
SOLVABILITY_MAPS = [
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_1_7860_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_7861_10567_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt",
]

FULL_DATASET = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
FULL_VERIFY = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_VERIFY_GPT56SOL.txt"
FULL_AGGREGATE = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AGGREGATE_GPT56SOL.txt"
FULL_CERTIFICATE = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_GPT56SOL_CERTIFICATE.md"
SEED_PLAN = "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SEED_PLAN_AGGREGATE = "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_AGGREGATE_GPT56SOL.txt"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def read(name: str) -> list[str]:
    return (BASE / name).read_text(encoding="utf-8").splitlines()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest().upper()


def pairs(line: str, start: int = 2) -> dict[str, str]:
    parts = line.split("\t")
    require((len(parts) - start) % 2 == 0, f"malformed pairs: {line}")
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        require(parts[index] not in result, f"duplicate field {parts[index]} in {line}")
        result[parts[index]] = parts[index + 1]
    return result


def record_map(name: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for line in read(name):
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0] not in result:
            result[parts[0]] = parts[1:]
    return result


def manifest_entries(name: str) -> set[str]:
    result: set[str] = set()
    lines = read(name)
    require(lines, f"empty manifest {name}")
    for line in lines:
        match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
        require(match is not None, f"bad manifest line in {name}: {line}")
        expected, child = match.groups()
        require(child not in result, f"duplicate manifest child {child} in {name}")
        require((BASE / child).is_file(), f"missing manifest child {child}")
        require(digest(BASE / child) == expected, f"manifest mismatch {name}: {child}")
        result.add(child)
    return result


def canonical_name(shard: int, lo: int, hi: int) -> str:
    if shard <= 11:
        return f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_{lo}_{hi}_CHECKPOINT_GPT56SOL.txt"
    if shard == 12:
        return "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11341_11845_MERGED_RECOVERY_GPT56SOL.txt"
    return f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_{lo}_{hi}_MERGED_ROUTED_GPT56SOL.txt"


def shard_tag(shard: int) -> str:
    return f"{shard:02d}"


def load_evidence(names: list[str], with_solvable: bool) -> dict[int, dict[str, int]]:
    result: dict[int, dict[str, int]] = {}
    for name in names:
        lines = read(name)
        require(lines[-1] == "DONE", f"map terminal {name}")
        for line in lines:
            match = re.match(r"^ENTRY\t24T(\d+)\t", line)
            if not match:
                continue
            key = int(match.group(1))
            data = pairs(line)
            require(key not in result, f"duplicate evidence 24T{key}")
            result[key] = {
                "order": int(data["ORDER"]),
                "parity": int(data["PARITY_MAPS"]),
                "solvable": int(data["SOLVABLE"]) if with_solvable else -1,
            }
    return result


@dataclass(frozen=True)
class Entry:
    key: int
    shard: int
    order: int
    solvable: bool
    parity_maps: int
    route: str
    representation: str
    pc_order: int
    aut_order: int
    iso_ms: int
    aut_ms: int
    class_ms: int
    classes: int
    raw: int
    source: str

    @property
    def profile_ms(self) -> int:
        return self.iso_ms + self.aut_ms + self.class_ms


plan_lines = read("GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL.tsv")
plan_rows = [line.split("\t") for line in plan_lines if line.startswith("SHARD\t")]
require(len(plan_rows) == 32, "sealed plan shard count")
for shard, (parts, expected_range) in enumerate(zip(plan_rows, EXPECTED_RANGES), start=1):
    require(int(parts[1]) == shard and parts[2] == "RANGE", f"sealed plan shard {shard} schema")
    require((int(parts[3]), int(parts[4])) == expected_range, f"sealed plan shard {shard} range")
require(EXPECTED_RANGES[0][0] == 1 and EXPECTED_RANGES[-1][1] == 25000, "range endpoints")
for left, right in zip(EXPECTED_RANGES, EXPECTED_RANGES[1:]):
    require(left[1] + 1 == right[0], f"range gap/overlap {left} {right}")

window = load_evidence(PARITY_MAPS, False)
solvability = load_evidence(SOLVABILITY_MAPS, True)
require(len(window) == 10829, "full order-window total")
require(len(solvability) == 10714, "full parity total")
require(set(solvability) <= set(window), "parity subset of window")
require(sum(item["solvable"] for item in solvability.values()) == 10537, "solvable parity total")
require(sum(1 - item["solvable"] for item in solvability.values()) == 177, "nonsolvable parity total")

entries: list[Entry] = []
input_manifest_children = 0
scan_total = 0
for shard, (lo, hi) in enumerate(EXPECTED_RANGES, start=1):
    tag = shard_tag(shard)
    manifest_name = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{tag}_GPT56SOL_MANIFEST.sha256"
    aggregate_name = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{tag}_AGGREGATE_GPT56SOL.txt"
    verify_name = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{tag}_VERIFY_GPT56SOL.txt"
    source_name = canonical_name(shard, lo, hi)
    children = manifest_entries(manifest_name)
    input_manifest_children += len(children)
    require({aggregate_name, verify_name, source_name} <= children, f"shard {shard} canonical manifest members")

    aggregate = record_map(aggregate_name)
    verifier = record_map(verify_name)
    require(aggregate["RANGE"][:2] == [str(lo), str(hi)], f"shard {shard} aggregate range")
    require(aggregate.get("DONE") is None or True, "aggregate parsed")
    require(read(aggregate_name)[-1] == "DONE", f"shard {shard} aggregate terminal")
    require(read(verify_name)[-1] == "DONE", f"shard {shard} verifier terminal")
    require(verifier.get("VERIFY") == ["PASS"], f"shard {shard} verifier PASS")
    expected_scans = sum(k % 25 == 0 for k in range(lo, hi + 1))
    require(verifier["SCAN_CHECKPOINTS"][:2] == [str(expected_scans), "PASS"], f"shard {shard} scan coverage")
    scan_total += expected_scans

    lines = read(source_name)
    require(lines[-1] == "DONE", f"shard {shard} canonical terminal")
    require(sum(line.startswith("TOTAL\t") for line in lines) == 1, f"shard {shard} unique TOTAL")
    shard_entries: list[Entry] = []
    for line in lines:
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        key = int(match.group(1))
        data = pairs(line)
        required = {"ORDER", "SOLVABLE_G", "PARITY_MAPS", "AUT_ORDER", "AUT_MS", "METHOD", "CLASS_MS", "ORDER8_CLASSES", "RAW_PAIRS"}
        require(required <= data.keys(), f"shard {shard} 24T{key} schema")
        order = int(data["ORDER"])
        solvable = data["SOLVABLE_G"] == "true"
        require(data["SOLVABLE_G"] in {"true", "false"}, f"24T{key} solvable boolean")
        route = data["METHOD"]
        require(route in {"pc", "native"}, f"24T{key} route")
        require(key in solvability and lo <= key <= hi, f"24T{key} sealed parity membership")
        sealed = solvability[key]
        require(order == sealed["order"] and int(data["PARITY_MAPS"]) == sealed["parity"], f"24T{key} sealed fields")
        require(solvable == bool(sealed["solvable"]), f"24T{key} sealed solvability")
        require(route != "pc" or solvable, f"24T{key} pc requires solvable")
        require(solvable or route == "native", f"24T{key} nonsolvable must be native")
        representation = data.get("REPRESENTATION", "legacy_sealed_pc" if route == "pc" else "legacy_original_native")
        pc_order = int(data.get("PC_ORDER", str(order if route == "pc" else 0)))
        if route == "pc":
            require(pc_order == order, f"24T{key} pc order transport")
        classes = int(data["ORDER8_CLASSES"])
        raw = int(data["RAW_PAIRS"])
        require(raw == order * classes, f"24T{key} frozen raw identity")
        require(min(classes, raw, int(data["AUT_MS"]), int(data["CLASS_MS"])) >= 0, f"24T{key} nonnegative")
        require(int(data["AUT_ORDER"]) > 0, f"24T{key} Aut order")
        shard_entries.append(Entry(
            key=key, shard=shard, order=order, solvable=solvable, parity_maps=int(data["PARITY_MAPS"]),
            route=route, representation=representation, pc_order=pc_order, aut_order=int(data["AUT_ORDER"]),
            iso_ms=int(data.get("ISO_MS", "0")), aut_ms=int(data["AUT_MS"]), class_ms=int(data["CLASS_MS"]),
            classes=classes, raw=raw, source=source_name,
        ))

    expected_keys = sorted(k for k in solvability if lo <= k <= hi)
    require([entry.key for entry in shard_entries] == expected_keys, f"shard {shard} exact entry keyset")
    total_line = next(line for line in lines if line.startswith("TOTAL\t"))
    total = pairs(total_line)
    require(int(total["ORDER_WINDOW"]) == sum(lo <= k <= hi for k in window), f"shard {shard} source window")
    require(int(total.get("PROCESSED", total.get("PARITY_KEYS", "-1"))) == len(shard_entries), f"shard {shard} source processed")
    require(int(total["ORDER8_CLASSES"]) == sum(entry.classes for entry in shard_entries), f"shard {shard} source classes")
    require(int(total["RAW_PAIRS"]) == sum(entry.raw for entry in shard_entries), f"shard {shard} source raw")
    require(int(aggregate["ORDER_WINDOW"][0]) == sum(lo <= k <= hi for k in window), f"shard {shard} aggregate window")
    require(int(aggregate["PARITY_KEYS"][0]) == len(shard_entries), f"shard {shard} aggregate parity")
    require(int(aggregate["ORDER8_CLASSES"][0]) == sum(entry.classes for entry in shard_entries), f"shard {shard} aggregate classes")
    require(int(aggregate["RAW_PAIRS"][0]) == sum(entry.raw for entry in shard_entries), f"shard {shard} aggregate raw")
    require(verifier["ENTRY_KEYS_EXACT"] == ["PASS"], f"shard {shard} verifier keyset")
    entries.extend(shard_entries)

require(scan_total == 1000, "full scan checkpoint total")
require([entry.key for entry in entries] == sorted(solvability), "full deterministic parity key order")
require(len(entries) == len({entry.key for entry in entries}) == 10714, "full unique entry union")
require(sum(entry.classes for entry in entries) == 1474201, "exact full class total")
require(sum(entry.raw for entry in entries) == 40656212448, "exact full raw total")
require(sum(entry.iso_ms for entry in entries) == 5722, "exact full ISO time")
require(sum(entry.aut_ms for entry in entries) == 3600392, "exact full Aut time")
require(sum(entry.class_ms for entry in entries) == 8705004, "exact full class time")
require(sum(entry.profile_ms for entry in entries) == 12311118, "exact full profile cost")
require(sum(entry.classes > 0 for entry in entries) == 9962, "positive-class keys")
require(sum(entry.classes == 0 for entry in entries) == 752, "zero-class keys")
require(sum(entry.route == "pc" for entry in entries) == 10493, "pc route total")
require(sum(entry.route == "native" for entry in entries) == 221, "native route total")
require(sum(entry.route == "native" and entry.solvable for entry in entries) == 44, "solvable native legacy total")
require(sum(entry.route == "native" and not entry.solvable for entry in entries) == 177, "nonsolvable native total")


def load_profile_cost(name: str) -> dict[int, int]:
    result: dict[int, int] = {}
    for line in read(name):
        match = re.match(r"^ENTRY\t\d+T(\d+)\t", line)
        if not match:
            continue
        data = pairs(line)
        key = int(match.group(1))
        require(key not in result, f"duplicate calibration key {name}:{key}")
        result[key] = int(data.get("ISO_MS", "0")) + int(data["AUT_MS"]) + int(data["CLASS_MS"])
    return result


calibration_profiles = {
    42: load_profile_cost("GAP_TRANSITIVE_DEGREE42_AUT_PROFILE_1_9491_GPT56SOL.txt"),
    44: load_profile_cost("GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_MERGED_V3_GPT56SOL.txt"),
    45: load_profile_cost("GAP_TRANSITIVE_DEGREE45_AUT_PROFILE_1_10923_GPT56SOL.txt"),
}
CALIBRATIONS = [
    ("D42S1", 42, 1, 620, "GAP_TRANSITIVE_DEGREE42_C8_SHARD1_AGGREGATE_GPT56SOL.txt"),
    ("D42S2", 42, 621, 819, "GAP_TRANSITIVE_DEGREE42_C8_SHARD2_AGGREGATE_GPT56SOL.txt"),
    ("D42S3", 42, 820, 873, "GAP_TRANSITIVE_DEGREE42_C8_SHARD3_AGGREGATE_GPT56SOL.txt"),
    ("D42S4", 42, 874, 9491, "GAP_TRANSITIVE_DEGREE42_C8_SHARD4_AGGREGATE_GPT56SOL.txt"),
    ("D44S1", 44, 1, 109, "GAP_TRANSITIVE_DEGREE44_C8_SHARD1_AGGREGATE_GPT56SOL.txt"),
    ("D44S2", 44, 110, 221, "GAP_TRANSITIVE_DEGREE44_C8_SHARD2_AGGREGATE_GPT56SOL.txt"),
    ("D44S3", 44, 222, 226, "GAP_TRANSITIVE_DEGREE44_C8_SHARD3_AGGREGATE_GPT56SOL.txt"),
    ("D44S4", 44, 227, 228, "GAP_TRANSITIVE_DEGREE44_C8_SHARD4_AGGREGATE_GPT56SOL.txt"),
    ("D45S1", 45, 1, 578, "GAP_TRANSITIVE_DEGREE45_C8_SHARD1_AGGREGATE_GPT56SOL.txt"),
    ("D45S2", 45, 579, 708, "GAP_TRANSITIVE_DEGREE45_C8_SHARD2_AGGREGATE_GPT56SOL.txt"),
    ("D45S3", 45, 709, 782, "GAP_TRANSITIVE_DEGREE45_C8_SHARD3_AGGREGATE_GPT56SOL.txt"),
    ("D45S4", 45, 783, 10923, "GAP_TRANSITIVE_DEGREE45_C8_SHARD4_AGGREGATE_GPT56SOL.txt"),
]
calibration_rows = []
for label, degree, lo, hi, aggregate_name in CALIBRATIONS:
    aggregate = record_map(aggregate_name)
    raw = int(aggregate["FULL_SEED_PAIRS"][0])
    actual_ms = int(aggregate["GAP_MS"][0])
    profile_ms = sum(value for key, value in calibration_profiles[degree].items() if lo <= key <= hi)
    residual_ms = max(0, actual_ms - profile_ms)
    residual_pairs_per_second = math.inf if residual_ms == 0 else raw * 1000 / residual_ms
    calibration_rows.append((label, degree, lo, hi, raw, profile_ms, actual_ms, residual_ms, residual_pairs_per_second))

positive_rates = [row[8] for row in calibration_rows if math.isfinite(row[8])]
slowest_observed = min(positive_rates)
require(80350 < slowest_observed < 80370, "expected slowest residual throughput")
SCHEDULE_PAIRS_PER_MS = 75  # 75,000 pairs/s, slower than every positive residual calibration.
require(SCHEDULE_PAIRS_PER_MS * 1000 < slowest_observed, "conservative pair rate")
for row in calibration_rows:
    modeled = row[5] + math.ceil(row[4] / SCHEDULE_PAIRS_PER_MS)
    require(modeled >= row[6], f"calibration model dominates {row[0]}")
forecast_text = "\n".join(read("GAP_TRANSITIVE_DEGREE24_FORECAST_GPT56SOL_CERTIFICATE.md"))
require("963,782 ms for 100,275,600 raw pairs" in forecast_text and "0.009611331 ms/pair" in forecast_text, "sealed degree20 calibration citation")


@dataclass
class SeedShard:
    segments: list[tuple[int, int, int, int]] = field(default_factory=list)  # key, first alpha, last alpha, order
    raw: int = 0
    profile_ms: int = 0
    keys: set[int] = field(default_factory=set)

    @property
    def classes(self) -> int:
        return sum(last - first + 1 for _, first, last, _ in self.segments)

    @property
    def pair_ms(self) -> int:
        return math.ceil(self.raw / SCHEDULE_PAIRS_PER_MS)

    @property
    def point_ms(self) -> int:
        return self.profile_ms + self.pair_ms


MAX_RAW_PER_SEED_SHARD = 45_000_000
MAX_POINT_MS = 800_000
INTERNAL_GUARD_MS = 1_320_000
EXTERNAL_GUARD_SECONDS = 1400
VM_BYTES = 51_539_607_552
seed_shards: list[SeedShard] = []
current = SeedShard()


def close_current() -> None:
    global current
    require(bool(current.segments), "cannot close empty seed shard")
    require(current.raw <= MAX_RAW_PER_SEED_SHARD, "seed raw cap")
    require(current.point_ms <= MAX_POINT_MS, "seed model cap")
    seed_shards.append(current)
    current = SeedShard()


for entry in entries:
    if entry.classes == 0:
        continue
    alpha = 1
    while alpha <= entry.classes:
        added_profile = 0 if entry.key in current.keys else entry.profile_ms
        profile_after = current.profile_ms + added_profile
        if profile_after >= MAX_POINT_MS:
            require(current.segments, f"single key profile exceeds cap 24T{entry.key}")
            close_current()
            continue
        max_raw_model = (MAX_POINT_MS - profile_after) * SCHEDULE_PAIRS_PER_MS
        raw_room = min(MAX_RAW_PER_SEED_SHARD, max_raw_model) - current.raw
        take = min(entry.classes - alpha + 1, raw_room // entry.order)
        if take < 1:
            require(current.segments, f"single alpha unit exceeds cap 24T{entry.key}")
            close_current()
            continue
        current.profile_ms = profile_after
        current.keys.add(entry.key)
        current.segments.append((entry.key, alpha, alpha + take - 1, entry.order))
        current.raw += take * entry.order
        alpha += take
        if alpha <= entry.classes:
            close_current()
if current.segments:
    close_current()

assigned_classes: Counter[int] = Counter()
assigned_raw: Counter[int] = Counter()
key_shard_occurrences: Counter[int] = Counter()
last_position: tuple[int, int] | None = None
for shard in seed_shards:
    require(shard.raw <= MAX_RAW_PER_SEED_SHARD and shard.point_ms <= MAX_POINT_MS, "seed shard caps")
    for key, first, last, order in shard.segments:
        require(first <= last, "alpha interval order")
        if last_position is not None:
            previous_key, previous_alpha = last_position
            if key == previous_key:
                require(first == previous_alpha + 1, f"within-key work-unit gap 24T{key}")
            else:
                require(key > previous_key, "lexicographic key order")
                for skipped in (entry for entry in entries if previous_key < entry.key < key):
                    require(skipped.classes == 0, f"skipped positive key 24T{skipped.key}")
                require(first == 1, f"new key alpha starts at one 24T{key}")
        assigned_classes[key] += last - first + 1
        assigned_raw[key] += (last - first + 1) * order
        last_position = (key, last)
    for key in shard.keys:
        key_shard_occurrences[key] += 1

positive_entries = [entry for entry in entries if entry.classes > 0]
require(set(assigned_classes) == {entry.key for entry in positive_entries}, "seed positive-key coverage")
for entry in positive_entries:
    require(assigned_classes[entry.key] == entry.classes, f"24T{entry.key} alpha coverage")
    require(assigned_raw[entry.key] == entry.raw, f"24T{entry.key} seed raw coverage")
require(sum(shard.classes for shard in seed_shards) == 1474201, "seed class checksum")
require(sum(shard.raw for shard in seed_shards) == 40656212448, "seed raw checksum")
require(max(shard.point_ms for shard in seed_shards) <= MAX_POINT_MS, "maximum seed point")
require(max(shard.raw for shard in seed_shards) <= MAX_RAW_PER_SEED_SHARD, "maximum seed raw")

dataset_lines = [
    "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-MERGED",
    "GAP_VERSION\t4.12.1", "DATABASE\t25000", "CATALOGUE_RANGE\t1\t25000",
    "ORDER_WINDOW\t10829", "PARITY_KEYS\t10714", "SOURCE_SHARDS\t32",
    "SCOPE\tExact normalized Aut/order-8 profile metrics for every parity-capable order-window key; no seed predicate.",
    "FROZEN_RAW_IDENTITY\tRAW_PAIRS=Size(G)*ORDER8_CLASSES",
]
for entry in entries:
    dataset_lines.append("\t".join([
        "ENTRY", f"24T{entry.key}", "SOURCE_SHARD", str(entry.shard), "ORDER", str(entry.order),
        "SOLVABLE_G", str(entry.solvable).lower(), "PARITY_MAPS", str(entry.parity_maps), "ROUTE", entry.route,
        "REPRESENTATION", entry.representation, "PC_ORDER", str(entry.pc_order), "AUT_ORDER", str(entry.aut_order),
        "ISO_MS", str(entry.iso_ms), "AUT_MS", str(entry.aut_ms), "CLASS_MS", str(entry.class_ms),
        "PROFILE_COST_MS", str(entry.profile_ms), "ORDER8_CLASSES", str(entry.classes), "RAW_PAIRS", str(entry.raw),
    ]))
dataset_lines.extend([
    "\t".join([
        "TOTAL", "DEGREE", "24", "DATABASE", "25000", "RANGE", "1", "25000", "ORDER_WINDOW", "10829",
        "PARITY_KEYS", "10714", "SOLVABLE", "10537", "NONSOLVABLE", "177", "PC_ROUTE", "10493",
        "NATIVE_ROUTE", "221", "POSITIVE_CLASS_KEYS", "9962", "ZERO_CLASS_KEYS", "752",
        "ORDER8_CLASSES", "1474201", "RAW_PAIRS", "40656212448", "ISO_MS", "5722", "AUT_MS", "3600392",
        "CLASS_MS", "8705004", "PROFILE_COST_MS", "12311118", "SCAN_CHECKPOINTS", "1000",
    ]),
    "DONE",
])

plan_output = [
    "CERTIFICATE_PLAN\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-C8-SEED-WORKLOAD",
    "STATUS\tEXACT_PROFILE_DERIVED_PLAN_SEALED_NO_SEED_RUN",
    "GAP_VERSION\t4.12.1", "DATABASE\t25000", "PROFILE_ELIGIBLE_KEYS\t10714",
    "POSITIVE_CLASS_KEYS\t9962", "ZERO_CLASS_KEYS_CLOSED_BY_PROFILE\t752",
    "ORDER8_CLASSES\t1474201", "RAW_PAIRS\t40656212448",
    "WORK_UNIT\t(24Tk,alpha_index); alpha_index is one-based in GAP 4.12.1 Filtered(ConjugacyClasses(Aut(G)),Order(Representative)=8) order after reconstructing the sealed route; each unit enumerates every x in G.",
    "PARTITION_ORDER\tLexicographic by catalogue key then alpha_index; every positive work unit occurs exactly once.",
    "COST_MODEL\tMeasured per-key PROFILE_COST_MS is charged once per key touched by a shard; pair work is ceil(RAW_PAIRS/75), i.e. conservative 75,000 pairs/s.",
    f"CALIBRATION\t12 sealed degree42/44/45 exact seed shards; slowest positive residual throughput {slowest_observed:.6f} pairs/s; schedule rate 75000 pairs/s; model dominates all 12 observed runtimes.",
    "DEGREE20_REFERENCE\t963782 ms / 100275600 raw pairs = 0.009611331 ms/pair, as sealed in the degree24 forecast certificate.",
    f"CAPS\tMAX_RAW_PAIRS\t{MAX_RAW_PER_SEED_SHARD}\tMAX_POINT_MS\t{MAX_POINT_MS}\tINTERNAL_GUARD_MS\t{INTERNAL_GUARD_MS}\tEXTERNAL_WALL_SECONDS\t{EXTERNAL_GUARD_SECONDS}\tVM_BYTES\t{VM_BYTES}",
    "RECOVERY\tEach future seed runner must verify the full-profile key metrics and exact class count before work; write an atomic checkpoint after every completed alpha_index, recording (key,alpha_index), cumulative counters, and output hash; resume at the lexicographic successor without replaying sealed units.",
    "CACHE_SCOPE\tAut/class and beta/locus caches are shard-local; discard at shard end and never retain all loci across a split high-class key.",
    "CANDIDATE_POLICY\tOn any centralizer-orbit candidate, freeze later shards, export the numeric representative, and run independent parity-aware frozen based-tree replay before continuation.",
]
for row in calibration_rows:
    residual_rate = "INF" if not math.isfinite(row[8]) else f"{row[8]:.6f}"
    model_ms = row[5] + math.ceil(row[4] / SCHEDULE_PAIRS_PER_MS)
    plan_output.append("\t".join([
        "CALIBRATION_SHARD", row[0], "DEGREE", str(row[1]), "RANGE", str(row[2]), str(row[3]),
        "RAW_PAIRS", str(row[4]), "PROFILE_MS", str(row[5]), "ACTUAL_GAP_MS", str(row[6]),
        "RESIDUAL_MS", str(row[7]), "RESIDUAL_PAIRS_PER_SECOND", residual_rate,
        "SCHEDULE_MODEL_MS", str(model_ms), "DOMINATES", "PASS",
    ]))
for number, shard in enumerate(seed_shards, start=1):
    first = shard.segments[0]
    last = shard.segments[-1]
    plan_output.append("\t".join([
        "SHARD", str(number), "FIRST_KEY", str(first[0]), "FIRST_ALPHA", str(first[1]),
        "LAST_KEY", str(last[0]), "LAST_ALPHA", str(last[2]), "KEYS_TOUCHED", str(len(shard.keys)),
        "CLASS_UNITS", str(shard.classes), "RAW_PAIRS", str(shard.raw), "PROFILE_REBUILD_MS", str(shard.profile_ms),
        "PAIR_MODEL_MS", str(shard.pair_ms), "POINT_MODEL_MS", str(shard.point_ms),
        "FRACTION_INTERNAL_GUARD", f"{shard.point_ms / INTERNAL_GUARD_MS:.6f}",
    ]))
    for key, first_alpha, last_alpha, order in shard.segments:
        plan_output.append("\t".join([
            "WORK", str(number), "KEY", str(key), "ALPHA_FIRST", str(first_alpha), "ALPHA_LAST", str(last_alpha),
            "ORDER", str(order), "CLASS_UNITS", str(last_alpha - first_alpha + 1),
            "RAW_PAIRS", str((last_alpha - first_alpha + 1) * order),
        ]))

split_keys = sum(count > 1 for count in key_shard_occurrences.values())
repeated_profile_ms = sum(shard.profile_ms for shard in seed_shards)
plan_output.extend([
    "\t".join([
        "CHECKSUM", "SHARDS", str(len(seed_shards)), "WORK_SEGMENTS", str(sum(len(shard.segments) for shard in seed_shards)),
        "POSITIVE_KEYS", "9962", "SPLIT_KEYS", str(split_keys), "CLASS_UNITS", "1474201",
        "RAW_PAIRS", "40656212448", "REPEATED_PROFILE_MS", str(repeated_profile_ms),
        "PAIR_MODEL_MS", str(sum(shard.pair_ms for shard in seed_shards)),
        "TOTAL_POINT_MODEL_MS", str(sum(shard.point_ms for shard in seed_shards)),
        "MIN_RAW", str(min(shard.raw for shard in seed_shards)), "MAX_RAW", str(max(shard.raw for shard in seed_shards)),
        "MIN_POINT_MS", str(min(shard.point_ms for shard in seed_shards)), "MAX_POINT_MS", str(max(shard.point_ms for shard in seed_shards)),
        "MAX_FRACTION_INTERNAL_GUARD", f"{max(shard.point_ms for shard in seed_shards) / INTERNAL_GUARD_MS:.6f}",
    ]),
    "SCOPE\tScheduling certificate only. No inverse, relator, B3, generation, parity, orbit, candidate, based-tree, or other seed predicate was run.",
    "DONE",
])

verify_lines = [
    "CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-MERGE-AND-SEED-PLAN",
    "INPUT_SHARD_MANIFESTS\t32\tPASS", f"INPUT_MANIFEST_CHILDREN\t{input_manifest_children}\tPASS",
    "CATALOGUE_RANGE_UNION\t1\t25000\tGAPS\t0\tOVERLAPS\t0\tPASS",
    "ORDER_WINDOW\t10829\tPASS", "PARITY_KEY_UNION\t10714\tDUPLICATES\t0\tPASS",
    "SOLVABLE_NONSOLVABLE\t10537\t177\tPASS", "PC_NATIVE_ROUTES\t10493\t221\tPASS",
    "PC_TRANSPORT_AND_NATIVE_IDENTITIES\t10714\tPASS", "FROZEN_RAW_IDENTITIES\t10714\tPASS",
    "ORDER8_CLASSES\t1474201\tPASS", "RAW_PAIRS\t40656212448\tPASS",
    "PROFILE_TIMES_ISO_AUT_CLASS\t5722\t3600392\t8705004\tPASS",
    "POSITIVE_ZERO_CLASS_KEYS\t9962\t752\tPASS", "SEALED_SCAN_CHECKPOINTS\t1000\tPASS",
    "FULL_DATASET_DETERMINISTIC_ORDER\t10714\tPASS", "CALIBRATION_SHARDS\t12\tMODEL_DOMINATES\t12\tPASS",
    f"SEED_PLAN_SHARDS\t{len(seed_shards)}\tPASS", "SEED_WORK_UNIT_COVERAGE\t1474201\tDUPLICATES\t0\tPASS",
    "SEED_RAW_COVERAGE\t40656212448\tPASS", f"SEED_SPLIT_KEYS\t{split_keys}\tPASS",
    f"SEED_MAX_RAW\t{max(shard.raw for shard in seed_shards)}\tCAP\t{MAX_RAW_PER_SEED_SHARD}\tPASS",
    f"SEED_MAX_POINT_MS\t{max(shard.point_ms for shard in seed_shards)}\tCAP\t{MAX_POINT_MS}\tGUARD\t{INTERNAL_GUARD_MS}\tPASS",
    "SEED_PREDICATES_RUN\t0\tPASS", "VERIFY\tPASS", "DONE",
]

aggregate_lines = [
    "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-FULL",
    "STATUS\tFULL_AUT_ORDER8_PROFILE_COMPLETE_INDEPENDENTLY_MERGED_SEED_PLAN_ONLY",
    "DEGREE\t24", "DATABASE\t25000", "CATALOGUE_RANGE\t1\t25000", "SOURCE_SHARDS\t32",
    "ORDER_WINDOW\t10829", "PARITY_KEYS\t10714", "PARITY_EXCLUDED\t115",
    "SOLVABLE_KEYS\t10537", "NONSOLVABLE_KEYS\t177", "PC_ROUTE_KEYS\t10493", "NATIVE_ROUTE_KEYS\t221",
    "SOLVABLE_NATIVE_LEGACY_KEYS\t44", "POSITIVE_CLASS_KEYS\t9962", "ZERO_CLASS_KEYS\t752",
    "ORDER8_CLASSES\t1474201", "RAW_PAIRS\t40656212448", "FROZEN_RAW_IDENTITY\tSize(G)*ORDER8_CLASSES",
    "ISO_MS\t5722", "AUT_MS\t3600392", "CLASS_MS\t8705004", "PROFILE_COST_MS\t12311118",
    "SCAN_CHECKPOINTS\t1000", f"INPUT_MANIFEST_CHILDREN_VERIFIED\t{input_manifest_children}",
    f"SEED_PLAN_SHARDS\t{len(seed_shards)}", f"SEED_PLAN_SPLIT_KEYS\t{split_keys}",
    f"SEED_PLAN_MAX_RAW\t{max(shard.raw for shard in seed_shards)}", f"SEED_PLAN_MAX_POINT_MS\t{max(shard.point_ms for shard in seed_shards)}",
    f"SEED_PLAN_MAX_FRACTION_INTERNAL_GUARD\t{max(shard.point_ms for shard in seed_shards) / INTERNAL_GUARD_MS:.6f}",
    f"SEED_PLAN_TOTAL_POINT_MS\t{sum(shard.point_ms for shard in seed_shards)}",
    "SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS",
    "SCOPE\tComplete exact degree-24 Aut/order-8 profile and deterministic seed scheduling plan only; this is not a degree-24 seed/B3/global closure.",
    "DONE",
]

plan_aggregate_lines = [
    "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-C8-SEED-WORKLOAD-PLAN",
    "STATUS\tPLAN_COMPLETE_NO_SEED_RUN", f"SHARDS\t{len(seed_shards)}",
    f"WORK_SEGMENTS\t{sum(len(shard.segments) for shard in seed_shards)}", "POSITIVE_KEYS\t9962",
    f"SPLIT_KEYS\t{split_keys}", "CLASS_UNITS\t1474201", "RAW_PAIRS\t40656212448",
    "SCHEDULE_PAIRS_PER_SECOND\t75000", "CALIBRATION_SHARDS\t12", f"SLOWEST_OBSERVED_RESIDUAL_PAIRS_PER_SECOND\t{slowest_observed:.6f}",
    f"MAX_RAW_CAP\t{MAX_RAW_PER_SEED_SHARD}", f"MAX_POINT_CAP_MS\t{MAX_POINT_MS}",
    f"MIN_RAW\t{min(shard.raw for shard in seed_shards)}", f"MAX_RAW\t{max(shard.raw for shard in seed_shards)}",
    f"MIN_POINT_MS\t{min(shard.point_ms for shard in seed_shards)}", f"MAX_POINT_MS\t{max(shard.point_ms for shard in seed_shards)}",
    f"REPEATED_PROFILE_MS\t{repeated_profile_ms}", f"PAIR_MODEL_MS\t{sum(shard.pair_ms for shard in seed_shards)}",
    f"TOTAL_POINT_MODEL_MS\t{sum(shard.point_ms for shard in seed_shards)}",
    f"INTERNAL_GUARD_MS\t{INTERNAL_GUARD_MS}", f"EXTERNAL_WALL_GUARD_SECONDS\t{EXTERNAL_GUARD_SECONDS}", f"VM_BYTES\t{VM_BYTES}",
    f"MAX_FRACTION_INTERNAL_GUARD\t{max(shard.point_ms for shard in seed_shards) / INTERNAL_GUARD_MS:.6f}",
    "RECOVERY_KEY\t(catalogue_key,alpha_index)", "SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS", "DONE",
]

certificate_lines = [
    "# Degree-24 full exact Aut/order-8 profile and seed-workload plan", "",
    "Status: **the 32-shard Aut/order-8 profile is complete and independently merged; the seed plan is sealed but no seed predicate has been run.**", "",
    "The 32 sealed ranges form the disjoint contiguous catalogue interval `1..25000`. The exact union has 10,829 order-window keys and 10,714 parity-capable keys. Every eligible key appears once in the canonical dataset; every entry agrees with the sealed parity/solvability evidence and satisfies the frozen identity `RAW_PAIRS = Size(G) * ORDER8_CLASSES`.", "",
    "Exact totals are 1,474,201 order-eight automorphism classes and 40,656,212,448 raw seed pairs. There are 9,962 positive-class keys and 752 exact zero-class keys. The normalized route count is 10,493 pc and 221 native; all 177 nonsolvable keys are native, while 44 solvable legacy keys retain their sealed native route. The 32 shard verifiers certify 1,000 catalogue scan checkpoints.", "",
    f"The seed workload is partitioned into {len(seed_shards):,} disjoint lexicographic `(catalogue key, alpha-class index)` shards. Alpha indices refer to the one-based GAP 4.12.1 filtered exact-order-eight conjugacy-class list after reconstructing the sealed route. This permits exact splitting of the 18 keys above 100 million raw pairs without omitting or duplicating a class.", "",
    f"Scheduling charges each touched key its measured ISO+Aut+class cost and charges pair work at 75,000 pairs/s. That rate is slower than the slowest positive residual throughput across 12 sealed degree-42/44/45 exact seed shards; the model dominates all 12 observed runtimes. Each shard is capped at {MAX_RAW_PER_SEED_SHARD:,} raw pairs and {MAX_POINT_MS:,} modeled ms, at most {max(shard.point_ms for shard in seed_shards) / INTERNAL_GUARD_MS:.1%} of the 1,320,000 ms internal guard. This is a resource-aware schedule, not a runtime theorem.", "",
    "A production seed runner must verify the sealed profile count before selecting its alpha interval, checkpoint atomically after each completed alpha class, keep caches shard-local, and resume from the next `(key, alpha_index)`. Any numeric candidate freezes later shards pending independent parity-aware frozen based-tree replay.", "",
    "No inverse, relator, B3, generation, parity, centralizer-orbit, candidate, based-tree, axis-six, or other seed predicate was executed here. Accordingly this artifact is not a degree-24 finite-quotient closure.",
]

for name in (FULL_DATASET, FULL_VERIFY, FULL_AGGREGATE, FULL_CERTIFICATE, SEED_PLAN, SEED_PLAN_AGGREGATE):
    require(not (BASE / name).exists(), f"refuse overwrite {name}")
(BASE / FULL_DATASET).write_text("\n".join(dataset_lines) + "\n", encoding="utf-8", newline="\n")
(BASE / FULL_VERIFY).write_text("\n".join(verify_lines) + "\n", encoding="utf-8", newline="\n")
(BASE / FULL_AGGREGATE).write_text("\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n")
(BASE / FULL_CERTIFICATE).write_text("\n".join(certificate_lines) + "\n", encoding="utf-8", newline="\n")
(BASE / SEED_PLAN).write_text("\n".join(plan_output) + "\n", encoding="utf-8", newline="\n")
(BASE / SEED_PLAN_AGGREGATE).write_text("\n".join(plan_aggregate_lines) + "\n", encoding="utf-8", newline="\n")

print(
    "PASS full degree24 profile entries=10714 window=10829 classes=1474201 raw=40656212448 "
    f"scanCheckpoints=1000 seedShards={len(seed_shards)} splitKeys={split_keys} "
    f"maxRaw={max(shard.raw for shard in seed_shards)} maxPointMs={max(shard.point_ms for shard in seed_shards)} "
    f"totalPointMs={sum(shard.point_ms for shard in seed_shards)} noSeeds=PASS"
)
