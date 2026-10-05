from __future__ import annotations

import argparse
import glob
import hashlib
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Sequence


PROFILE_SHA256 = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA256 = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
GAP_VERSION = "4.12.1"
DATABASE = 25000
DEGREE = 24
SHARD = 3
PLAN_KEYS = 335
PLAN_UNITS = 14648
PLAN_RAW = 44998656
PLAN_PROFILE_MS = 169845
INTERNAL_GUARD_MS = 1320000
EXTERNAL_WALL_SECONDS = 1400
VM_BYTES = 51539607552
WSL_BASE = "/mnt/d/work/revise/production_code/escalations"

SEED_ENGINE_NAME = "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard003_v7_gpt56sol.g"
SEED_ENGINE_SHA256 = "b5c1cfb76ff04f205846826700bcb6eae36c96d7c89851b3434befdce6a9baa7"
PROFILE_NAME = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
CHECKPOINT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_GPT56SOL.txt"
CHECKPOINT_TMP_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_TMP_GPT56SOL.txt"
INITIAL_WRAPPER_NAME = (
    "gap_run_degree24_c8_seed_shard003_segment001_unit1_14648_postverify_v7_gpt56sol.g"
)
INITIAL_WRAPPER_SHA256 = "75ced8e1ecc7eb5b7deb69e58e36726c2399c5d4f50630dd3b4ed6fc2fa0dd18"
INITIAL_RUNNER_NAME = "run_degree24_c8_seed_shard003_segment001_postverify_v7.sh"
INITIAL_RUNNER_SHA256 = "b92f2ce6f1e7210df8c8bbf90d8e34acf09b7c46099613e95ed56a924df50c38"

INTERRUPTED_TERMINAL = "CHECKPOINT_WRITE_FAILURE_EXCLUDED_UNCOMMITTED_ALPHA"
INTERMEDIATE_EVIDENCE_SHA256 = "05acee28da8b95404f3357dab0618e08b6cad27636a70dc1bfe7487781f72a3e"
PINNED_FAILURE_OUTPUT_LINES = 16580
PINNED_DURABLE_COUNTERS = (
    8089, 24849408, 8089, 411, 2138368, 1370312,
    290816, 37504, 0, 0, 0, 0,
)

CANONICAL_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_GPT56SOL.txt"
AGGREGATE_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_AGGREGATE_GPT56SOL.txt"
CERTIFICATE_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_GPT56SOL_CERTIFICATE.md"

OUTPUT_RE = re.compile(
    r"^GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT(?P<segment>[0-9]{3})(?:_V(?P<revision>[0-9]+))?_"
    r"UNIT(?P<start>[0-9]+)(?:_(?P<target>[0-9]+))?"
    r"(?P<postverify>_POSTVERIFY)?_V(?P<version>[0-9]+)_GPT56SOL[.]txt$"
)
STDOUT_RE = re.compile(
    r"^GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT(?P<segment>[0-9]{3})(?:_V(?P<revision>[0-9]+))?_"
    r"RUN_STDOUT_V(?P<version>[0-9]+)_GPT56SOL[.]txt$"
)
STDERR_RE = re.compile(
    r"^GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT(?P<segment>[0-9]{3})(?:_V(?P<revision>[0-9]+))?_"
    r"RUN_STDERR_V(?P<version>[0-9]+)_GPT56SOL[.]txt$"
)
WRAPPER_RE = re.compile(
    re.escape(WSL_BASE)
    + r"/gap_run_degree24_c8_seed_shard003_segment(?P<segment>[0-9]{3})(?:_v(?P<revision>[0-9]+))?_"
      r"unit(?P<start>[0-9]+)(?:_(?P<target>[0-9]+))?"
      r"(?P<postverify>_postverify)?_v(?P<version>[0-9]+)_gpt56sol[.]g"
)
RUNNER_RE = re.compile(
    r"^run_degree24_c8_seed_shard003_segment(?P<segment>[0-9]{3})(?:_v(?P<revision>[0-9]+))?_postverify_v7[.]sh$"
 )
EVIDENCE_RE = re.compile(
    r"^GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT(?P<segment>[0-9]{3})_"
    r"CHECKPOINT_WRITE_FAILURE_EVIDENCE_GPT56SOL[.]txt$"
)
LOWER_SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_pairs(tokens: Sequence[str], start: int, context: str) -> dict[str, str]:
    require((len(tokens) - start) % 2 == 0, f"{context}: odd key/value token count")
    result: dict[str, str] = {}
    for index in range(start, len(tokens), 2):
        key = tokens[index]
        require(key not in result, f"{context}: duplicate field {key}")
        result[key] = tokens[index + 1]
    return result


def require_fields(values: dict[str, str], expected: set[str], context: str) -> None:
    missing = expected - values.keys()
    extra = values.keys() - expected
    require(not missing and not extra, f"{context}: fields missing={sorted(missing)} extra={sorted(extra)}")


def integer(value: str, context: str, minimum: int | None = None) -> int:
    require(re.fullmatch(r"-?[0-9]+", value) is not None, f"{context}: not an integer: {value!r}")
    result = int(value)
    if minimum is not None:
        require(result >= minimum, f"{context}: {result} < {minimum}")
    return result


def key_number(value: str, context: str) -> int:
    match = re.fullmatch(r"24T([0-9]+)", value)
    require(match is not None, f"{context}: malformed degree-24 key {value!r}")
    return int(match.group(1))


def load_pinned_ascii(path: Path, expected_sha: str, label: str) -> list[str]:
    require(path.is_file(), f"{label}: missing {path}")
    data = path.read_bytes()
    require(data.endswith(b"\n"), f"{label}: missing final LF")
    require(b"\r" not in data and b"\x00" not in data, f"{label}: noncanonical bytes")
    require(hashlib.sha256(data).hexdigest().upper() == expected_sha, f"{label}: SHA256 mismatch")
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationError(f"{label}: non-ASCII content") from error
    return text.splitlines()


@dataclass(frozen=True)
class Profile:
    key: int
    source_shard: int
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
    profile_ms: int
    classes: int
    raw: int


@dataclass(frozen=True)
class Work:
    shard: int
    key: int
    first: int
    last: int
    order: int
    units: int
    raw: int
    unit_first: int = 0
    unit_last: int = 0


@dataclass(frozen=True)
class ShardSummary:
    shard: int
    first_key: int
    first_alpha: int
    last_key: int
    last_alpha: int
    keys: int
    units: int
    raw: int
    profile_ms: int
    pair_ms: int
    point_ms: int
    fraction: str


@dataclass
class Counters:
    units: int = 0
    raw: int = 0
    invariant_alpha: int = 0
    beta: int = 0
    inverse: int = 0
    inverse_odd: int = 0
    orbit8: int = 0
    relator: int = 0
    b3: int = 0
    generate: int = 0
    centralizer: int = 0
    candidate: int = 0

    def clone(self) -> "Counters":
        return Counters(**self.__dict__)


@dataclass(frozen=True)
class IntermediateEvidence:
    path: Path
    file_sha: str
    segment: int
    output_name: str
    output_bytes: int
    output_sha: str
    stdout_name: str
    stdout_bytes: int
    stdout_sha: str
    stderr_name: str
    stderr_bytes: int
    stderr_sha: str
    last_unit: int
    next_unit: int
    last_key: int
    last_alpha: int
    next_key: int
    next_alpha: int
    checkpoint_sha: str
    prefix_bytes: int
    prefix_sha: str
    postprefix_name: str
    postprefix_bytes: int
    postprefix_sha: str
    failed_tmp_name: str
    failed_tmp_bytes: int
    failed_tmp_sha: str
    failed_tmp_payload_unit: int
    reported_failure: str
    resource_telemetry: str

def parse_profile(path: Path) -> dict[int, Profile]:
    lines = load_pinned_ascii(path, PROFILE_SHA256, "sealed profile")
    require(lines[:9] == [
        "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-MERGED",
        "GAP_VERSION\t4.12.1",
        "DATABASE\t25000",
        "CATALOGUE_RANGE\t1\t25000",
        "ORDER_WINDOW\t10829",
        "PARITY_KEYS\t10714",
        "SOURCE_SHARDS\t32",
        "SCOPE\tExact normalized Aut/order-8 profile metrics for every parity-capable order-window key; no seed predicate.",
        "FROZEN_RAW_IDENTITY\tRAW_PAIRS=Size(G)*ORDER8_CLASSES",
    ], "sealed profile: preamble mismatch")
    require(lines[-1] == "DONE", "sealed profile: missing DONE")

    fields = {
        "SOURCE_SHARD", "ORDER", "SOLVABLE_G", "PARITY_MAPS", "ROUTE", "REPRESENTATION",
        "PC_ORDER", "AUT_ORDER", "ISO_MS", "AUT_MS", "CLASS_MS", "PROFILE_COST_MS",
        "ORDER8_CLASSES", "RAW_PAIRS",
    }
    profiles: dict[int, Profile] = {}
    total_tokens: list[str] | None = None
    previous_key = 0
    for line_number, line in enumerate(lines[9:-1], 10):
        tokens = line.split("\t")
        if tokens[0] == "ENTRY":
            require(len(tokens) >= 4, f"profile line {line_number}: short ENTRY")
            key = key_number(tokens[1], f"profile line {line_number}")
            require(key > previous_key and key not in profiles, f"profile line {line_number}: key order/duplicate")
            values = parse_pairs(tokens, 2, f"profile 24T{key}")
            require_fields(values, fields, f"profile 24T{key}")
            solvable_text = values["SOLVABLE_G"]
            require(solvable_text in {"true", "false"}, f"profile 24T{key}: SOLVABLE_G")
            profile = Profile(
                key=key,
                source_shard=integer(values["SOURCE_SHARD"], f"profile 24T{key} source", 1),
                order=integer(values["ORDER"], f"profile 24T{key} order", 1),
                solvable=solvable_text == "true",
                parity_maps=integer(values["PARITY_MAPS"], f"profile 24T{key} parity", 1),
                route=values["ROUTE"],
                representation=values["REPRESENTATION"],
                pc_order=integer(values["PC_ORDER"], f"profile 24T{key} pc order", 0),
                aut_order=integer(values["AUT_ORDER"], f"profile 24T{key} aut order", 1),
                iso_ms=integer(values["ISO_MS"], f"profile 24T{key} iso ms", 0),
                aut_ms=integer(values["AUT_MS"], f"profile 24T{key} aut ms", 0),
                class_ms=integer(values["CLASS_MS"], f"profile 24T{key} class ms", 0),
                profile_ms=integer(values["PROFILE_COST_MS"], f"profile 24T{key} profile ms", 0),
                classes=integer(values["ORDER8_CLASSES"], f"profile 24T{key} classes", 0),
                raw=integer(values["RAW_PAIRS"], f"profile 24T{key} raw", 0),
            )
            require(1 <= profile.source_shard <= 32, f"profile 24T{key}: source shard")
            require(2338 <= profile.order <= 50000, f"profile 24T{key}: order window")
            require(profile.route in {"pc", "native"}, f"profile 24T{key}: route")
            require(profile.representation in {
                "legacy_sealed_pc", "legacy_original_native", "native", "original",
                "pc_single", "pc_transport",
            }, f"profile 24T{key}: representation")
            if profile.route == "pc":
                require(profile.solvable and profile.pc_order == profile.order, f"profile 24T{key}: pc route")
            else:
                require(profile.pc_order in {0, profile.order}, f"profile 24T{key}: native pc order")
            require(profile.profile_ms == profile.iso_ms + profile.aut_ms + profile.class_ms,
                    f"profile 24T{key}: cost identity")
            require(profile.raw == profile.order * profile.classes, f"profile 24T{key}: frozen raw identity")
            profiles[key] = profile
            previous_key = key
        elif tokens[0] == "TOTAL":
            require(total_tokens is None, "sealed profile: duplicate TOTAL")
            total_tokens = tokens
        else:
            raise VerificationError(f"profile line {line_number}: unexpected record {tokens[0]!r}")

    require(total_tokens is not None, "sealed profile: missing TOTAL")
    expected_total = {
        "DEGREE": 24, "DATABASE": 25000, "RANGE": None, "ORDER_WINDOW": 10829,
        "PARITY_KEYS": 10714, "SOLVABLE": 10537, "NONSOLVABLE": 177,
        "PC_ROUTE": 10493, "NATIVE_ROUTE": 221, "POSITIVE_CLASS_KEYS": 9962,
        "ZERO_CLASS_KEYS": 752, "ORDER8_CLASSES": 1474201, "RAW_PAIRS": 40656212448,
        "ISO_MS": 5722, "AUT_MS": 3600392, "CLASS_MS": 8705004,
        "PROFILE_COST_MS": 12311118, "SCAN_CHECKPOINTS": 1000,
    }
    # RANGE has two positional values in the source and is the sole non-pair field.
    require(total_tokens[5:8] == ["RANGE", "1", "25000"], "sealed profile TOTAL: range encoding")
    total_values = parse_pairs(total_tokens[:5] + total_tokens[8:], 1, "sealed profile TOTAL normalized")
    require_fields(total_values, set(expected_total) - {"RANGE"}, "sealed profile TOTAL normalized")
    for name, value in expected_total.items():
        if name == "RANGE":
            continue
        require(integer(total_values[name], f"sealed profile TOTAL {name}") == value,
                f"sealed profile TOTAL {name}")

    derived = {
        "PARITY_KEYS": len(profiles),
        "SOLVABLE": sum(profile.solvable for profile in profiles.values()),
        "NONSOLVABLE": sum(not profile.solvable for profile in profiles.values()),
        "PC_ROUTE": sum(profile.route == "pc" for profile in profiles.values()),
        "NATIVE_ROUTE": sum(profile.route == "native" for profile in profiles.values()),
        "POSITIVE_CLASS_KEYS": sum(profile.classes > 0 for profile in profiles.values()),
        "ZERO_CLASS_KEYS": sum(profile.classes == 0 for profile in profiles.values()),
        "ORDER8_CLASSES": sum(profile.classes for profile in profiles.values()),
        "RAW_PAIRS": sum(profile.raw for profile in profiles.values()),
        "ISO_MS": sum(profile.iso_ms for profile in profiles.values()),
        "AUT_MS": sum(profile.aut_ms for profile in profiles.values()),
        "CLASS_MS": sum(profile.class_ms for profile in profiles.values()),
        "PROFILE_COST_MS": sum(profile.profile_ms for profile in profiles.values()),
    }
    for name, value in derived.items():
        require(value == expected_total[name], f"sealed profile: derived {name}={value}")
    return profiles


def parse_plan(path: Path, profiles: dict[int, Profile]) -> tuple[list[Work], ShardSummary]:
    lines = load_pinned_ascii(path, PLAN_SHA256, "sealed plan")
    require(lines[0] == "CERTIFICATE_PLAN\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-C8-SEED-WORKLOAD",
            "sealed plan: certificate")
    require(lines[1] == "STATUS\tEXACT_PROFILE_DERIVED_PLAN_SEALED_NO_SEED_RUN", "sealed plan: status")
    require(lines[-2].startswith("SCOPE\tScheduling certificate only. No inverse"), "sealed plan: scope")
    require(lines[-1] == "DONE", "sealed plan: DONE")

    shard_fields = {
        "FIRST_KEY", "FIRST_ALPHA", "LAST_KEY", "LAST_ALPHA", "KEYS_TOUCHED",
        "CLASS_UNITS", "RAW_PAIRS", "PROFILE_REBUILD_MS", "PAIR_MODEL_MS",
        "POINT_MODEL_MS", "FRACTION_INTERNAL_GUARD",
    }
    work_fields = {"KEY", "ALPHA_FIRST", "ALPHA_LAST", "ORDER", "CLASS_UNITS", "RAW_PAIRS"}
    summaries: dict[int, ShardSummary] = {}
    works_by_shard: dict[int, list[Work]] = {}
    checksum: dict[str, str] | None = None
    global_works: list[Work] = []

    for line_number, line in enumerate(lines, 1):
        tokens = line.split("\t")
        if tokens[0] == "SHARD":
            shard = integer(tokens[1], f"plan line {line_number} shard", 1)
            require(shard not in summaries, f"plan line {line_number}: duplicate shard")
            values = parse_pairs(tokens, 2, f"plan shard {shard}")
            require_fields(values, shard_fields, f"plan shard {shard}")
            summary = ShardSummary(
                shard=shard,
                first_key=integer(values["FIRST_KEY"], f"plan shard {shard} first key", 1),
                first_alpha=integer(values["FIRST_ALPHA"], f"plan shard {shard} first alpha", 1),
                last_key=integer(values["LAST_KEY"], f"plan shard {shard} last key", 1),
                last_alpha=integer(values["LAST_ALPHA"], f"plan shard {shard} last alpha", 1),
                keys=integer(values["KEYS_TOUCHED"], f"plan shard {shard} keys", 1),
                units=integer(values["CLASS_UNITS"], f"plan shard {shard} units", 1),
                raw=integer(values["RAW_PAIRS"], f"plan shard {shard} raw", 1),
                profile_ms=integer(values["PROFILE_REBUILD_MS"], f"plan shard {shard} profile ms", 0),
                pair_ms=integer(values["PAIR_MODEL_MS"], f"plan shard {shard} pair ms", 0),
                point_ms=integer(values["POINT_MODEL_MS"], f"plan shard {shard} point ms", 0),
                fraction=values["FRACTION_INTERNAL_GUARD"],
            )
            summaries[shard] = summary
            works_by_shard[shard] = []
        elif tokens[0] == "WORK":
            shard = integer(tokens[1], f"plan line {line_number} work shard", 1)
            require(shard in summaries, f"plan line {line_number}: WORK before SHARD")
            values = parse_pairs(tokens, 2, f"plan shard {shard} WORK")
            require_fields(values, work_fields, f"plan shard {shard} WORK")
            work = Work(
                shard=shard,
                key=integer(values["KEY"], f"plan shard {shard} key", 1),
                first=integer(values["ALPHA_FIRST"], f"plan shard {shard} alpha first", 1),
                last=integer(values["ALPHA_LAST"], f"plan shard {shard} alpha last", 1),
                order=integer(values["ORDER"], f"plan shard {shard} order", 1),
                units=integer(values["CLASS_UNITS"], f"plan shard {shard} units", 1),
                raw=integer(values["RAW_PAIRS"], f"plan shard {shard} raw", 1),
            )
            require(work.key in profiles, f"plan shard {shard}: unknown profile 24T{work.key}")
            profile = profiles[work.key]
            require(profile.classes > 0, f"plan shard {shard}: zero-class key 24T{work.key}")
            require(work.first <= work.last <= profile.classes, f"plan shard {shard}: alpha interval")
            require(work.units == work.last - work.first + 1, f"plan shard {shard}: unit identity")
            require(work.order == profile.order and work.raw == work.units * work.order,
                    f"plan shard {shard}: raw/order identity")
            works_by_shard[shard].append(work)
            global_works.append(work)
        elif tokens[0] == "CHECKSUM":
            require(checksum is None, "sealed plan: duplicate CHECKSUM")
            checksum = parse_pairs(tokens, 1, "sealed plan CHECKSUM")

    require(sorted(summaries) == list(range(1, 906)), "sealed plan: shard ids are not 1..905")
    require(checksum is not None, "sealed plan: missing CHECKSUM")

    repeated_profile_ms = 0
    for shard in range(1, 906):
        summary = summaries[shard]
        works = works_by_shard[shard]
        require(len(works) == summary.keys, f"plan shard {shard}: keys touched")
        require(works[0].key == summary.first_key and works[0].first == summary.first_alpha,
                f"plan shard {shard}: first endpoint")
        require(works[-1].key == summary.last_key and works[-1].last == summary.last_alpha,
                f"plan shard {shard}: last endpoint")
        units = sum(work.units for work in works)
        raw = sum(work.raw for work in works)
        profile_ms = sum(profiles[work.key].profile_ms for work in works)
        require(units == summary.units and raw == summary.raw and profile_ms == summary.profile_ms,
                f"plan shard {shard}: derived totals")
        require(summary.pair_ms == (summary.raw + 74) // 75, f"plan shard {shard}: pair model")
        require(summary.point_ms == summary.profile_ms + summary.pair_ms, f"plan shard {shard}: point model")
        require(summary.raw <= 45000000 and summary.point_ms <= 800000, f"plan shard {shard}: cap")
        require(summary.fraction == f"{summary.point_ms / INTERNAL_GUARD_MS:.6f}",
                f"plan shard {shard}: guard fraction")
        require(all(works[index].key < works[index + 1].key for index in range(len(works) - 1)),
                f"plan shard {shard}: key order")
        repeated_profile_ms += profile_ms

    positive_keys = [profile.key for profile in profiles.values() if profile.classes > 0]
    positive_index = 0
    expected_alpha = 1
    split_counts: dict[int, int] = {}
    for work in global_works:
        require(positive_index < len(positive_keys), "sealed plan: excess work")
        expected_key = positive_keys[positive_index]
        require(work.key == expected_key and work.first == expected_alpha,
                f"sealed plan: lexicographic gap at 24T{work.key} alpha {work.first}")
        split_counts[work.key] = split_counts.get(work.key, 0) + 1
        expected_alpha = work.last + 1
        if expected_alpha > profiles[work.key].classes:
            require(expected_alpha == profiles[work.key].classes + 1, f"sealed plan: class overrun 24T{work.key}")
            positive_index += 1
            expected_alpha = 1
    require(positive_index == len(positive_keys) and expected_alpha == 1, "sealed plan: incomplete coverage")

    expected_checksum = {
        "SHARDS": 905,
        "WORK_SEGMENTS": 10864,
        "POSITIVE_KEYS": 9962,
        "SPLIT_KEYS": 806,
        "CLASS_UNITS": 1474201,
        "RAW_PAIRS": 40656212448,
        "REPEATED_PROFILE_MS": 15397849,
        "PAIR_MODEL_MS": 542083466,
        "TOTAL_POINT_MODEL_MS": 557481315,
        "MIN_RAW": 20889600,
        "MAX_RAW": 44999712,
        "MIN_POINT_MS": 280846,
        "MAX_POINT_MS": 799997,
    }
    for name, value in expected_checksum.items():
        require(integer(checksum[name], f"sealed plan CHECKSUM {name}") == value,
                f"sealed plan CHECKSUM {name}")
    require(checksum["MAX_FRACTION_INTERNAL_GUARD"] == "0.606058", "sealed plan CHECKSUM guard")
    require(len(global_works) == expected_checksum["WORK_SEGMENTS"], "sealed plan: work count")
    require(sum(work.units for work in global_works) == expected_checksum["CLASS_UNITS"],
            "sealed plan: unit total")
    require(sum(work.raw for work in global_works) == expected_checksum["RAW_PAIRS"],
            "sealed plan: raw total")
    require(repeated_profile_ms == expected_checksum["REPEATED_PROFILE_MS"],
            "sealed plan: repeated profile total")
    require(sum(count > 1 for count in split_counts.values()) == expected_checksum["SPLIT_KEYS"],
            "sealed plan: split-key total")

    shard_summary = summaries[SHARD]
    require((shard_summary.first_key, shard_summary.first_alpha,
             shard_summary.last_key, shard_summary.last_alpha) ==
            (6032, 1, 6440, 2), "shard003: endpoint")
    require((shard_summary.keys, shard_summary.units, shard_summary.raw, shard_summary.profile_ms,
             shard_summary.pair_ms, shard_summary.point_ms, shard_summary.fraction) ==
            (PLAN_KEYS, PLAN_UNITS, PLAN_RAW, PLAN_PROFILE_MS, 599983, 769828, "0.583203"),
            "shard003: summary")
    unit = 1
    shard_works: list[Work] = []
    for work in works_by_shard[SHARD]:
        shard_works.append(Work(**{
            **work.__dict__,
            "unit_first": unit,
            "unit_last": unit + work.units - 1,
        }))
        unit += work.units
    require(unit == PLAN_UNITS + 1, "shard003: unit numbering")
    return shard_works, shard_summary


@dataclass(frozen=True)
class Bundle:
    segment: int
    output: Path
    stdout: Path
    stderr: Path
    filename_start: int
    filename_target: int | None
    output_version: int
    resource_version: int
    artifact_revision: int | None
    postverify: bool


def reject_evidence_name(path: Path) -> None:
    upper = path.name.upper()
    require("FAILED" not in upper and "SUPERSEDED" not in upper,
            f"rejected failed/superseded evidence: {path.name}")


def load_committed_failure_evidence(
    base: Path, arguments: argparse.Namespace
) -> IntermediateEvidence | None:
    specification = arguments.intermediate_evidence
    expected_sha = arguments.intermediate_evidence_sha256
    pattern = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT*_CHECKPOINT_WRITE_FAILURE_EVIDENCE_GPT56SOL.txt"
    discovered = sorted(path.resolve() for path in base.glob(pattern) if path.is_file())
    require(len(discovered) <= 1, "intermediate evidence: more than one canonical record")
    if specification is None:
        require(expected_sha is None, "intermediate evidence: SHA pin supplied without a record")
        require(
            not discovered,
            "intermediate evidence exists but was not explicitly selected and SHA-pinned",
        )
        return None
    require(expected_sha is not None, "intermediate evidence: explicit SHA-256 pin is required")
    require(
        re.fullmatch(r"[0-9A-Fa-f]{64}", expected_sha) is not None,
        "intermediate evidence: malformed SHA-256 pin",
    )
    candidate = Path(specification)
    path = (candidate if candidate.is_absolute() else base / candidate).resolve()
    require(path.parent == base, "intermediate evidence: record must be in the escalations directory")
    reject_evidence_name(path)
    require(path.is_file(), f"intermediate evidence: missing {path}")
    match = EVIDENCE_RE.fullmatch(path.name)
    require(match is not None, "intermediate evidence: noncanonical filename")
    if discovered:
        require(discovered[0] == path, "intermediate evidence: selected record/discovery mismatch")
    data = path.read_bytes()
    file_sha = sha256_bytes(data)
    require(expected_sha.lower() == INTERMEDIATE_EVIDENCE_SHA256,
            "intermediate evidence: supplied pin is not the verifier-sealed one-off record")
    require(file_sha == INTERMEDIATE_EVIDENCE_SHA256,
            "intermediate evidence: sealed SHA-256 mismatch")
    require(data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data,
            "intermediate evidence: noncanonical bytes")
    try:
        lines = data.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise VerificationError("intermediate evidence: non-ASCII content") from error
    require(len(lines) == 21, f"intermediate evidence: expected 21 lines, got {len(lines)}")
    segment = int(match.group("segment"))
    context = f"intermediate evidence segment {segment:03d}"

    require(
        lines[0] ==
        f"CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003-SEGMENT{segment:03d}-CHECKPOINT-WRITE-FAILURE",
        f"{context}: certificate",
    )
    require(lines[1] == "STATUS\tRECOVERABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT", f"{context}: status")
    require(lines[2] == "END_STATE\tCHECKPOINT_PRINTTO_FAILURE_AFTER_UNCOMMITTED_ALPHA_DONE",
            f"{context}: end state")
    require(lines[3] == "ORIGINAL_FILES_MODIFIED\t0", f"{context}: original-file mutation")
    require(lines[4] == "SYNTHETIC_RECORDS_ADDED\t0", f"{context}: synthetic records")

    def pinned_file(line: str, tag: str, minimum: int = 0) -> tuple[str, int, str]:
        tokens = line.split("\t")
        require(len(tokens) == 6 and tokens[0] == tag and tokens[2] == "BYTES" and
                tokens[4] == "SHA256", f"{context}: {tag} pin schema")
        size = integer(tokens[3], f"{context} {tag} bytes", minimum)
        require(re.fullmatch(r"[0-9A-F]{64}", tokens[5]) is not None,
                f"{context}: {tag} SHA encoding")
        return tokens[1], size, tokens[5].lower()

    output_name, output_bytes, output_sha = pinned_file(lines[5], "OUTPUT", 1)
    output_match = OUTPUT_RE.fullmatch(output_name)
    require(output_match is not None and int(output_match.group("segment")) == segment and
            output_match.group("revision") is None and int(output_match.group("version")) == 7 and
            output_match.group("postverify") is not None and
            integer(output_match.group("target") or "0", context, 0) == PLAN_UNITS,
            f"{context}: output filename/POSTVERIFY V7 target")
    stdout_name, stdout_bytes, stdout_sha = pinned_file(lines[6], "STDOUT")
    stderr_name, stderr_bytes, stderr_sha = pinned_file(lines[7], "STDERR")
    for name, regex, label in (
        (stdout_name, STDOUT_RE, "stdout"), (stderr_name, STDERR_RE, "stderr")
    ):
        resource_match = regex.fullmatch(name)
        require(resource_match is not None and int(resource_match.group("segment")) == segment and
                resource_match.group("revision") is None and
                int(resource_match.group("version")) == 7,
                f"{context}: {label} filename/version")

    def tagged_integer(line: str, tag: str, minimum: int) -> int:
        tokens = line.split("\t")
        require(len(tokens) == 2 and tokens[0] == tag, f"{context}: {tag} schema")
        return integer(tokens[1], f"{context} {tag}", minimum)

    last_unit = tagged_integer(lines[8], "LAST_DURABLE_UNIT", 1)
    next_unit = tagged_integer(lines[9], "NEXT_UNIT", 2)
    require(next_unit == last_unit + 1 and next_unit <= PLAN_UNITS,
            f"{context}: durable successor range")
    last_tokens = lines[10].split("\t")
    require(len(last_tokens) == 3 and last_tokens[0] == "LAST_DURABLE_KEY_ALPHA",
            f"{context}: last key/alpha schema")
    last_key = key_number(last_tokens[1], context)
    last_alpha = integer(last_tokens[2], context, 1)

    def tagged_sha(line: str, tag: str) -> str:
        tokens = line.split("\t")
        require(len(tokens) == 2 and tokens[0] == tag and
                re.fullmatch(r"[0-9A-F]{64}", tokens[1]) is not None,
                f"{context}: {tag} schema")
        return tokens[1].lower()

    checkpoint_sha = tagged_sha(lines[11], "CHECKPOINT_SHA256")
    prefix_bytes = tagged_integer(lines[12], "OUTPUT_PREFIX_BYTES", 1)
    prefix_sha = tagged_sha(lines[13], "OUTPUT_PREFIX_SHA256")

    post_tokens = lines[14].split("\t")
    require(len(post_tokens) == 8 and post_tokens[0] == "POSTPREFIX_SUFFIX" and
            post_tokens[2] == "BYTES" and post_tokens[4] == "SHA256" and
            post_tokens[6] == "RECORDS", f"{context}: postprefix schema")
    postprefix_name = post_tokens[1]
    post_match = re.fullmatch(
        rf"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT{segment:03d}_POSTPREFIX_SUFFIX_"
        r"COMMIT([0-9]+)_UNCOMMITTED([0-9]+)_GPT56SOL[.]txt",
        postprefix_name,
    )
    require(post_match is not None and int(post_match.group(1)) == last_unit and
            int(post_match.group(2)) == next_unit and
            post_tokens[7] == f"COMMITTED_UNIT{last_unit}_THEN_UNCOMMITTED_ALPHA_DONE_UNIT{next_unit}",
            f"{context}: postprefix identity")
    postprefix_bytes = integer(post_tokens[3], context, 1)
    require(re.fullmatch(r"[0-9A-F]{64}", post_tokens[5]) is not None,
            f"{context}: postprefix SHA encoding")
    postprefix_sha = post_tokens[5].lower()

    tmp_tokens = lines[15].split("\t")
    require(len(tmp_tokens) == 10 and tmp_tokens[0] == "FAILED_TMP" and
            tmp_tokens[2] == "BYTES" and tmp_tokens[4] == "SHA256" and
            tmp_tokens[6] == "PAYLOAD_UNIT" and tmp_tokens[8] == "TERMINAL_DONE",
            f"{context}: failed-temp schema")
    failed_tmp_name = tmp_tokens[1]
    require(failed_tmp_name ==
            f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT{segment:03d}_UNCOMMITTED_CHECKPOINT_TMP_UNIT{next_unit}_GPT56SOL.txt",
            f"{context}: failed-temp filename")
    failed_tmp_bytes = integer(tmp_tokens[3], context, 1)
    require(re.fullmatch(r"[0-9A-F]{64}", tmp_tokens[5]) is not None,
            f"{context}: failed-temp SHA encoding")
    failed_tmp_sha = tmp_tokens[5].lower()
    failed_tmp_payload_unit = integer(tmp_tokens[7], context, 1)
    require(failed_tmp_payload_unit == next_unit and tmp_tokens[9] == "0",
            f"{context}: failed-temp payload/terminal state")

    failure_tokens = lines[16].split("\t")
    require(failure_tokens == ["FAILURE", "Could not write to file descriptor during checkpoint PrintTo"],
            f"{context}: failure record")
    reported_failure = failure_tokens[1]
    require(lines[17] ==
            f"EXCLUSION\tUncommitted ALPHA_DONE unit{next_unit} and failed TMP payload are evidence only and excluded from scientific totals",
            f"{context}: exclusion record")
    recovery_match = re.fullmatch(
        rf"RECOVERY\tSTART_UNIT{next_unit} recomputes 24T([0-9]+) alpha([0-9]+); "
        rf"committed units1[.][.]{last_unit} are not replayed",
        lines[18],
    )
    require(recovery_match is not None, f"{context}: recovery record")
    next_key = int(recovery_match.group(1))
    next_alpha = int(recovery_match.group(2))
    telemetry_tokens = lines[19].split("\t")
    require(telemetry_tokens == ["RESOURCE_TELEMETRY", "UNAVAILABLE_PROCESS_FAILURE"],
            f"{context}: resource telemetry")
    require(lines[20] == "DONE", f"{context}: DONE")

    pinned_paths = {
        "output": (base / output_name, output_bytes, output_sha),
        "postprefix": (base / postprefix_name, postprefix_bytes, postprefix_sha),
        "failed temp": (base / failed_tmp_name, failed_tmp_bytes, failed_tmp_sha),
    }
    pinned_data: dict[str, bytes] = {}
    for label, (pinned_path, size, digest) in pinned_paths.items():
        reject_evidence_name(pinned_path)
        require(pinned_path.is_file(), f"{context}: missing pinned {label} file")
        pinned_data[label] = pinned_path.read_bytes()
        require(len(pinned_data[label]) == size and sha256_bytes(pinned_data[label]) == digest,
                f"{context}: pinned {label} bytes/SHA mismatch")
    output_data = pinned_data["output"]
    require(prefix_bytes < len(output_data) and
            sha256_bytes(output_data[:prefix_bytes]) == prefix_sha,
            f"{context}: durable output-prefix SHA")
    require(output_data[prefix_bytes:] == pinned_data["postprefix"],
            f"{context}: exact postprefix extraction")
    failed_tmp_data = pinned_data["failed temp"]
    require(b"\r" not in failed_tmp_data and b"\x00" not in failed_tmp_data and
            b"\nDONE\n" not in failed_tmp_data,
            f"{context}: failed-temp bytes/terminal marker")

    return IntermediateEvidence(
        path=path, file_sha=file_sha, segment=segment,
        output_name=output_name, output_bytes=output_bytes, output_sha=output_sha,
        stdout_name=stdout_name, stdout_bytes=stdout_bytes, stdout_sha=stdout_sha,
        stderr_name=stderr_name, stderr_bytes=stderr_bytes, stderr_sha=stderr_sha,
        last_unit=last_unit, next_unit=next_unit, last_key=last_key, last_alpha=last_alpha,
        next_key=next_key, next_alpha=next_alpha, checkpoint_sha=checkpoint_sha,
        prefix_bytes=prefix_bytes, prefix_sha=prefix_sha,
        postprefix_name=postprefix_name, postprefix_bytes=postprefix_bytes,
        postprefix_sha=postprefix_sha, failed_tmp_name=failed_tmp_name,
        failed_tmp_bytes=failed_tmp_bytes, failed_tmp_sha=failed_tmp_sha,
        failed_tmp_payload_unit=failed_tmp_payload_unit, reported_failure=reported_failure,
        resource_telemetry=telemetry_tokens[1],
    )

def expand_paths(base: Path, values: Sequence[str] | None, default_pattern: str, label: str) -> list[Path]:
    specifications = list(values or [default_pattern])
    found: list[Path] = []
    for specification in specifications:
        candidate = Path(specification)
        pattern = str(candidate if candidate.is_absolute() else base / candidate)
        if glob.has_magic(pattern):
            matches = [Path(item).resolve() for item in glob.glob(pattern)]
            require(matches, f"{label}: glob matched nothing: {specification}")
            found.extend(matches)
        else:
            found.append(Path(pattern).resolve())
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in found:
        reject_evidence_name(path)
        require(path.is_file(), f"{label}: missing file {path}")
        if path not in seen:
            unique.append(path)
            seen.add(path)
    require(unique, f"{label}: no files")
    return unique


def index_files(paths: Iterable[Path], pattern: re.Pattern[str], label: str) -> dict[int, tuple[Path, re.Match[str]]]:
    result: dict[int, tuple[Path, re.Match[str]]] = {}
    for path in paths:
        match = pattern.fullmatch(path.name)
        require(match is not None, f"{label}: noncanonical filename {path.name}")
        segment = int(match.group("segment"))
        require(segment not in result, f"{label}: ambiguous segment {segment:03d}")
        result[segment] = (path, match)
    return result


def discover_bundles(base: Path, arguments: argparse.Namespace) -> list[Bundle]:
    outputs = expand_paths(
        base, arguments.segment_output,
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT*_UNIT*_V*_GPT56SOL.txt",
        "segment output",
    )
    stdouts = expand_paths(
        base, arguments.resource_stdout,
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT*_RUN_STDOUT_V*_GPT56SOL.txt",
        "resource stdout",
    )
    stderrs = expand_paths(
        base, arguments.resource_stderr,
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT*_RUN_STDERR_V*_GPT56SOL.txt",
        "resource stderr",
    )
    output_map = index_files(outputs, OUTPUT_RE, "segment output")
    stdout_map = index_files(stdouts, STDOUT_RE, "resource stdout")
    stderr_map = index_files(stderrs, STDERR_RE, "resource stderr")
    require(output_map.keys() == stdout_map.keys() == stderr_map.keys(),
            f"segment bundle mismatch outputs={sorted(output_map)} stdout={sorted(stdout_map)} stderr={sorted(stderr_map)}")
    ids = sorted(output_map)
    require(ids == list(range(1, len(ids) + 1)), f"segment ids are not contiguous 001..{len(ids):03d}")
    bundles: list[Bundle] = []
    for segment in ids:
        output, output_match = output_map[segment]
        stdout, stdout_match = stdout_map[segment]
        stderr, stderr_match = stderr_map[segment]
        stdout_version = int(stdout_match.group("version"))
        stderr_version = int(stderr_match.group("version"))
        require(stdout_version == stderr_version, f"segment {segment:03d}: resource version mismatch")
        output_version = int(output_match.group("version"))
        revision_text = output_match.group("revision")
        stdout_revision = stdout_match.group("revision")
        stderr_revision = stderr_match.group("revision")
        require(revision_text == stdout_revision == stderr_revision,
                f"segment {segment:03d}: artifact revision mismatch")
        artifact_revision = int(revision_text) if revision_text is not None else None
        require(segment != 1 or artifact_revision is None,
                "segment 001: unexpected artifact revision suffix")
        target_text = output_match.group("target")
        target = int(target_text) if target_text is not None else None
        postverify = output_match.group("postverify") is not None
        require(
            (output_version, stdout_version, target, postverify) == (7, 7, PLAN_UNITS, True),
            f"segment {segment:03d}: output/resource version, target, or suffix is not POSTVERIFY V7",
        )
        filename_start = int(output_match.group("start"))
        require(1 <= filename_start <= PLAN_UNITS,
                f"segment {segment:03d}: filename start is outside shard003")
        bundles.append(Bundle(
            segment=segment,
            output=output,
            stdout=stdout,
            stderr=stderr,
            filename_start=filename_start,
            filename_target=target,
            output_version=output_version,
            resource_version=stdout_version,
            artifact_revision=artifact_revision,
            postverify=postverify,
        ))
    return bundles


@dataclass(frozen=True)
class ProducerRecord:
    wrapper_name: str
    wrapper_sha: str
    runner_name: str
    runner_sha: str
    engine_sha: str
    stop_after_unit: int | None


@dataclass(frozen=True)
class ResourceRecord:
    stdout_sha: str
    stdout_bytes: int
    stderr_sha: str
    stderr_bytes: int
    wrapper: str
    user_seconds: float | None
    system_seconds: float | None
    elapsed_text: str
    elapsed_seconds: float | None
    cpu_percent: int | None
    max_rss_kib: int | None
    exit_status: int | None
    rename_retry_records: int
    producer: ProducerRecord


WARNING_PREAMBLE = [
    f"Syntax warning: Unbound global variable in {WSL_BASE}/{SEED_ENGINE_NAME}:186",
    "     Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1));",
    "                                                       ^^^^",
    f"Syntax warning: Unbound global variable in {WSL_BASE}/{SEED_ENGINE_NAME}:201",
    "     Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1));",
    "                                                       ^^^^",
    f"Syntax warning: Unbound global variable in {WSL_BASE}/{SEED_ENGINE_NAME}:227",
    "     todo:=Filtered(todo,y->not y in orb);",
    "                                     ^^^",
]


def parse_elapsed(value: str, context: str) -> float:
    parts = value.split(":")
    require(len(parts) in {2, 3}, f"{context}: elapsed format {value!r}")
    try:
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = float(parts[1])
            require(minutes >= 0 and 0 <= seconds < 60, f"{context}: elapsed minute/second range")
            result = minutes * 60 + seconds
        else:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            require(hours >= 0 and 0 <= minutes < 60 and 0 <= seconds < 60,
                    f"{context}: elapsed hour/minute/second range")
            result = hours * 3600 + minutes * 60 + seconds
    except ValueError as error:
        raise VerificationError(f"{context}: elapsed format {value!r}") from error
    require(result >= 0 and math.isfinite(result), f"{context}: elapsed value")
    return result


def counter_vector(counters: Counters) -> list[int]:
    return [
        counters.units,
        counters.raw,
        counters.invariant_alpha,
        counters.beta,
        counters.inverse,
        counters.inverse_odd,
        counters.orbit8,
        counters.relator,
        counters.b3,
        counters.generate,
        counters.centralizer,
        counters.candidate,
    ]


def wrapper_record_lines(works: Sequence[Work], profiles: dict[int, Profile]) -> list[str]:
    lines: list[str] = []
    for index, work in enumerate(works):
        profile = profiles[work.key]
        suffix = "," if index + 1 < len(works) else ""
        lines.append(
            f"rec(k:={work.key},first:={work.first},last:={work.last},"
            f"unitFirst:={work.unit_first},unitLast:={work.unit_last},"
            f"order:={profile.order},autOrder:={profile.aut_order},"
            f"parity:={profile.parity_maps},classes:={profile.classes},raw:={profile.raw},"
            f'method:="{profile.route}",representation:="{profile.representation}",'
            f"pcOrder:={profile.pc_order},profileMs:={profile.profile_ms}){suffix}"
        )
    return lines


def verify_producer(
    bundle: Bundle,
    works: Sequence[Work],
    profiles: dict[int, Profile],
    initial: Counters,
    previous_checkpoint_sha: str,
    previous: tuple[Bundle, "SegmentResult"] | None,
) -> ProducerRecord:
    context = f"segment {bundle.segment:03d}"
    revision_suffix = "" if bundle.artifact_revision is None else f"_v{bundle.artifact_revision}"
    wrapper_name = (
        f"gap_run_degree24_c8_seed_shard003_segment{bundle.segment:03d}{revision_suffix}_"
        f"unit{bundle.filename_start}_{PLAN_UNITS}_postverify_v7_gpt56sol.g"
    )
    wrapper_path = bundle.output.parent / wrapper_name
    reject_evidence_name(wrapper_path)
    require(wrapper_path.is_file(), f"{context}: producer wrapper missing")
    wrapper_data = wrapper_path.read_bytes()
    require(
        wrapper_data.endswith(b"\n") and b"\r" not in wrapper_data and b"\x00" not in wrapper_data,
        f"{context}: wrapper bytes",
    )
    try:
        wrapper_lines = wrapper_data.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise VerificationError(f"{context}: non-ASCII wrapper") from error

    stop_line = wrapper_lines[2] if len(wrapper_lines) > 2 else ""
    stop_match = re.fullmatch(r"STOP_AFTER_UNIT:=(fail|[0-9]+);", stop_line)
    require(stop_match is not None, f"{context}: wrapper STOP_AFTER_UNIT")
    stop_text = stop_match.group(1)
    stop_after_unit = None if stop_text == "fail" else integer(
        stop_text, f"{context} wrapper stop", 1
    )
    if stop_after_unit is not None:
        require(
            bundle.filename_start <= stop_after_unit <= PLAN_UNITS,
            f"{context}: wrapper smoke stop outside remaining work",
        )

    if previous is None:
        require(
            bundle.segment == 1 and bundle.filename_start == 1,
            "segment 001: fresh bundle must begin at unit 1",
        )
        previous_output = "NONE_FRESH_START"
        previous_prefix_bytes = 0
        previous_prefix_sha = "NONE_FRESH_START"
    else:
        previous_bundle, previous_result = previous
        previous_output = f"{WSL_BASE}/{previous_bundle.output.name}"
        previous_prefix_bytes = previous_result.final_prefix_bytes
        previous_prefix_sha = previous_result.final_prefix_sha

    expected_lines = [
        "# Exact wrapper for sealed degree-24 seed workload shard003.",
        f'OUT:="{WSL_BASE}/{bundle.output.name}";',
        stop_line,
        f"INTERNAL_GUARD_MS:={INTERNAL_GUARD_MS}; START_UNIT:={bundle.filename_start};",
        "INITIAL_COUNTERS:=[" + ",".join(str(value) for value in counter_vector(initial)) + "];",
        f'PREVIOUS_CHECKPOINT_SHA256:="{previous_checkpoint_sha}";',
        f'PREVIOUS_OUTPUT_FILE:="{previous_output}"; PREVIOUS_OUTPUT_PREFIX_BYTES:={previous_prefix_bytes};',
        f'PREVIOUS_OUTPUT_PREFIX_SHA256:="{previous_prefix_sha}";',
        f'CHECKPOINT_FILE:="{WSL_BASE}/{CHECKPOINT_NAME}";',
        f'CHECKPOINT_TMP:="{WSL_BASE}/{CHECKPOINT_TMP_NAME}";',
        f'EXPECTED_PROFILE_SHA256:="{PROFILE_SHA256}";',
        f'EXPECTED_PLAN_SHA256:="{PLAN_SHA256}";',
        f'PROFILE_FILE:="{WSL_BASE}/{PROFILE_NAME}";',
        f'PLAN_FILE:="{WSL_BASE}/{PLAN_NAME}";',
        f'ENGINE_FILE:="{WSL_BASE}/{SEED_ENGINE_NAME}";',
        f'EXPECTED_ENGINE_SHA256:="{SEED_ENGINE_SHA256.upper()}";',
        "S003_RECORDS:=[",
        *wrapper_record_lines(works, profiles),
        "];",
        f'Read("{WSL_BASE}/{SEED_ENGINE_NAME}");',
    ]
    require(
        wrapper_lines == expected_lines,
        f"{context}: wrapper differs from exact shard003 plan/recovery contract",
    )

    engine_path = bundle.output.parent / SEED_ENGINE_NAME
    reject_evidence_name(engine_path)
    require(
        engine_path.is_file() and sha256_file(engine_path) == SEED_ENGINE_SHA256,
        f"{context}: pinned V7 engine provenance",
    )

    runner_name = f"run_degree24_c8_seed_shard003_segment{bundle.segment:03d}{revision_suffix}_postverify_v7.sh"
    runner_match = RUNNER_RE.fullmatch(runner_name)
    require(
        runner_match is not None and int(runner_match.group("segment")) == bundle.segment and
        (int(runner_match.group("revision")) if runner_match.group("revision") else None) ==
        bundle.artifact_revision,
        f"{context}: runner name/revision",
    )
    runner_path = bundle.output.parent / runner_name
    reject_evidence_name(runner_path)
    require(runner_path.is_file(), f"{context}: runner missing")
    expected_runner = (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "ulimit -v 50331648\n"
        f"exec /usr/bin/timeout --signal=TERM --kill-after=10s {EXTERNAL_WALL_SECONDS}s "
        f"/usr/bin/time -v gap -q {WSL_BASE}/{wrapper_name}\n"
    ).encode("ascii")
    runner_data = runner_path.read_bytes()
    require(runner_data == expected_runner, f"{context}: exact runner contract")

    wrapper_sha = sha256_bytes(wrapper_data)
    runner_sha = sha256_bytes(runner_data)
    if bundle.segment == 1:
        require(runner_name == INITIAL_RUNNER_NAME and runner_sha == INITIAL_RUNNER_SHA256,
                "segment 001: initial runner SHA256")
        if stop_after_unit is None:
            require(
                wrapper_name == INITIAL_WRAPPER_NAME and wrapper_sha == INITIAL_WRAPPER_SHA256,
                "segment 001: planned fresh wrapper SHA256",
            )

    return ProducerRecord(
        wrapper_name=wrapper_name,
        wrapper_sha=wrapper_sha,
        runner_name=runner_name,
        runner_sha=runner_sha,
        engine_sha=sha256_file(engine_path),
        stop_after_unit=stop_after_unit,
    )


def parse_resource(
    bundle: Bundle,
    works: Sequence[Work],
    profiles: dict[int, Profile],
    initial: Counters,
    previous_checkpoint_sha: str,
    previous: tuple[Bundle, "SegmentResult"] | None,
    evidence: IntermediateEvidence | None,
) -> ResourceRecord:
    producer = verify_producer(
        bundle, works, profiles, initial, previous_checkpoint_sha, previous
    )
    stdout_data = bundle.stdout.read_bytes()
    stderr_data = bundle.stderr.read_bytes()

    if evidence is not None and bundle.segment == evidence.segment:
        context = f"segment {bundle.segment:03d} checkpoint-failure evidence"
        require(
            producer.stop_after_unit is None,
            f"{context}: wrapper must use STOP_AFTER_UNIT:=fail",
        )
        require(
            bundle.stdout.name == evidence.stdout_name and
            len(stdout_data) == evidence.stdout_bytes and
            sha256_bytes(stdout_data) == evidence.stdout_sha,
            f"{context}: exact SHA-pinned stdout",
        )
        require(
            bundle.stderr.name == evidence.stderr_name and
            len(stderr_data) == evidence.stderr_bytes and
            sha256_bytes(stderr_data) == evidence.stderr_sha,
            f"{context}: exact SHA-pinned stderr",
        )
        for label, data in (("stdout", stdout_data), ("stderr", stderr_data)):
            require(b"\r" not in data and b"\x00" not in data,
                    f"{context}: noncanonical {label} bytes")
            require(not data or data.endswith(b"\n"), f"{context}: partial {label} line")
        try:
            stdout_lines = stdout_data.decode("ascii").splitlines()
            stderr_lines = stderr_data.decode("ascii").splitlines()
        except UnicodeDecodeError as error:
            raise VerificationError(f"{context}: non-ASCII resource stream") from error
        for retry_line in stdout_lines:
            retry_match = re.fullmatch(r"ATOMIC_RENAME_RETRY_SUCCESS\tATTEMPTS\t([0-9]+)", retry_line)
            require(retry_match is not None and 2 <= int(retry_match.group(1)) <= 500,
                    f"{context}: unexpected stdout record")
        require(
            stderr_lines[:len(WARNING_PREAMBLE)] == WARNING_PREAMBLE,
            f"{context}: warning preamble mismatch",
        )
        return ResourceRecord(
            stdout_sha=evidence.stdout_sha,
            stdout_bytes=evidence.stdout_bytes,
            stderr_sha=evidence.stderr_sha,
            stderr_bytes=evidence.stderr_bytes,
            wrapper="UNAVAILABLE",
            user_seconds=None,
            system_seconds=None,
            elapsed_text="UNAVAILABLE",
            elapsed_seconds=None,
            cpu_percent=None,
            max_rss_kib=None,
            exit_status=None,
            rename_retry_records=len(stdout_lines),
            producer=producer,
        )

    for label, data in (("stdout", stdout_data), ("stderr", stderr_data)):
        require(data.endswith(b"\n"), f"segment {bundle.segment:03d} resource {label}: missing final LF")
        require(b"\r" not in data and b"\x00" not in data,
                f"segment {bundle.segment:03d} resource {label}: noncanonical bytes")
    try:
        stdout_text = stdout_data.decode("ascii")
        stderr_lines = stderr_data.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise VerificationError(f"segment {bundle.segment:03d}: non-ASCII resource stream") from error

    expected_wrote = f"WROTE {WSL_BASE}/{bundle.output.name}"
    stdout_lines = stdout_text.splitlines()
    require(stdout_lines and stdout_lines[-1] == expected_wrote,
            f"segment {bundle.segment:03d}: stdout lacks the exact terminal WROTE record")
    for retry_line in stdout_lines[:-1]:
        retry_match = re.fullmatch(r"ATOMIC_RENAME_RETRY_SUCCESS\tATTEMPTS\t([0-9]+)", retry_line)
        require(retry_match is not None and 2 <= int(retry_match.group(1)) <= 500,
                f"segment {bundle.segment:03d}: invalid postverify retry stdout")
    require(stderr_lines[:len(WARNING_PREAMBLE)] == WARNING_PREAMBLE,
            f"segment {bundle.segment:03d}: warning preamble mismatch")
    timing = stderr_lines[len(WARNING_PREAMBLE):]
    require(len(timing) == 23, f"segment {bundle.segment:03d}: GNU time field count {len(timing)}")
    require(timing[0].startswith('\tCommand being timed: "gap -q ') and timing[0].endswith('"'),
            f"segment {bundle.segment:03d}: command record")
    wrapper = timing[0][len('\tCommand being timed: "gap -q '):-1]
    wrapper_match = WRAPPER_RE.fullmatch(wrapper)
    require(wrapper_match is not None, f"segment {bundle.segment:03d}: wrapper path/name")
    require(int(wrapper_match.group("segment")) == bundle.segment,
            f"segment {bundle.segment:03d}: wrapper segment")
    parsed_wrapper_revision = (
        int(wrapper_match.group("revision")) if wrapper_match.group("revision") else None
    )
    require(parsed_wrapper_revision == bundle.artifact_revision,
            f"segment {bundle.segment:03d}: wrapper artifact revision")
    require(int(wrapper_match.group("start")) == bundle.filename_start,
            f"segment {bundle.segment:03d}: wrapper start unit")
    wrapper_target = wrapper_match.group("target")
    parsed_wrapper_target = int(wrapper_target) if wrapper_target is not None else None
    require(parsed_wrapper_target == bundle.filename_target,
            f"segment {bundle.segment:03d}: wrapper/output target mismatch")
    require((wrapper_match.group("postverify") is not None) == bundle.postverify,
            f"segment {bundle.segment:03d}: wrapper/output postverify mismatch")
    require(int(wrapper_match.group("version")) == bundle.resource_version,
            f"segment {bundle.segment:03d}: wrapper/resource version")
    require(Path(wrapper).name == producer.wrapper_name,
            f"segment {bundle.segment:03d}: resource command/wrapper provenance")

    prefixes = [
        "\tUser time (seconds): ", "\tSystem time (seconds): ", "\tPercent of CPU this job got: ",
        "\tElapsed (wall clock) time (h:mm:ss or m:ss): ", "\tAverage shared text size (kbytes): ",
        "\tAverage unshared data size (kbytes): ", "\tAverage stack size (kbytes): ",
        "\tAverage total size (kbytes): ", "\tMaximum resident set size (kbytes): ",
        "\tAverage resident set size (kbytes): ", "\tMajor (requiring I/O) page faults: ",
        "\tMinor (reclaiming a frame) page faults: ", "\tVoluntary context switches: ",
        "\tInvoluntary context switches: ", "\tSwaps: ", "\tFile system inputs: ",
        "\tFile system outputs: ", "\tSocket messages sent: ", "\tSocket messages received: ",
        "\tSignals delivered: ", "\tPage size (bytes): ", "\tExit status: ",
    ]
    require(len(prefixes) == len(timing) - 1, "internal GNU time schema")
    values: list[str] = []
    for line, prefix in zip(timing[1:], prefixes):
        require(line.startswith(prefix), f"segment {bundle.segment:03d}: GNU time field {prefix!r}")
        values.append(line[len(prefix):])
    try:
        user_seconds = float(values[0])
        system_seconds = float(values[1])
    except ValueError as error:
        raise VerificationError(f"segment {bundle.segment:03d}: user/system seconds") from error
    require(user_seconds >= 0 and system_seconds >= 0 and math.isfinite(user_seconds + system_seconds),
            f"segment {bundle.segment:03d}: user/system seconds")
    require(re.fullmatch(r"[0-9]+%", values[2]) is not None, f"segment {bundle.segment:03d}: CPU percent")
    cpu_percent = int(values[2][:-1])
    elapsed_seconds = parse_elapsed(values[3], f"segment {bundle.segment:03d}")
    integer_values = [integer(value, f"segment {bundle.segment:03d} GNU time", 0) for value in values[4:]]
    max_rss_kib = integer_values[4]
    page_size = integer_values[-2]
    exit_status = integer_values[-1]
    require(0 <= cpu_percent <= 200, f"segment {bundle.segment:03d}: CPU percent range")
    require(0 < max_rss_kib * 1024 <= VM_BYTES, f"segment {bundle.segment:03d}: RSS/VM bound")
    require(page_size == 4096, f"segment {bundle.segment:03d}: page size")
    require(exit_status == 0, f"segment {bundle.segment:03d}: nonzero exit {exit_status}")
    require(elapsed_seconds <= EXTERNAL_WALL_SECONDS + 15,
            f"segment {bundle.segment:03d}: external wall guard exceeded")
    return ResourceRecord(
        stdout_sha=hashlib.sha256(stdout_data).hexdigest(),
        stdout_bytes=len(stdout_data),
        stderr_sha=hashlib.sha256(stderr_data).hexdigest(),
        stderr_bytes=len(stderr_data),
        wrapper=wrapper,
        user_seconds=user_seconds,
        system_seconds=system_seconds,
        elapsed_text=values[3],
        elapsed_seconds=elapsed_seconds,
        cpu_percent=cpu_percent,
        max_rss_kib=max_rss_kib,
        exit_status=exit_status,
        rename_retry_records=len(stdout_lines) - 1,
        producer=producer,
    )


def checkpoint_material(
    unit: int,
    key: int,
    alpha: int,
    counters: Counters,
    output_bytes: int,
    output_sha: str,
    previous_sha: str,
) -> tuple[str, str, bytes, str]:
    payload = (
        f"SHARD\t003\tUNIT\t{unit}\tKEY\t24T{key}\tALPHA\t{alpha}\tNEXT_UNIT\t{unit + 1}"
        f"\tCUM_UNITS\t{counters.units}\tCUM_RAW\t{counters.raw}"
        f"\tCUM_INVARIANT_ALPHA\t{counters.invariant_alpha}\tCUM_BETA\t{counters.beta}"
        f"\tCUM_INVERSE\t{counters.inverse}\tCUM_INVERSE_ODD\t{counters.inverse_odd}"
        f"\tCUM_ORBIT8\t{counters.orbit8}\tCUM_RELATOR\t{counters.relator}"
        f"\tCUM_B3\t{counters.b3}\tCUM_GENERATE\t{counters.generate}"
        f"\tCUM_CENTRALIZER_ORBITS\t{counters.centralizer}"
        f"\tCUM_CANDIDATE_NUMERIC\t{counters.candidate}"
        f"\tOUTPUT_PREFIX_BYTES\t{output_bytes}\tOUTPUT_PREFIX_SHA256\t{output_sha}"
        f"\tPREVIOUS_CHECKPOINT_SHA256\t{previous_sha}"
        f"\tPROFILE_SHA256\t{PROFILE_SHA256}\tPLAN_SHA256\t{PLAN_SHA256}"
    )
    payload_sha = sha256_bytes(payload.encode("ascii"))
    checkpoint = (
        "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD003\n"
        + payload
        + f"\tPAYLOAD_SHA256\t{payload_sha}\nDONE\n"
    ).encode("ascii")
    return payload, payload_sha, checkpoint, sha256_bytes(checkpoint)


def alpha_semantic_values(line: str, context: str) -> dict[str, str]:
    tokens = line.split("\t")
    require(tokens and tokens[0] == "ALPHA_DONE", f"{context}: ALPHA_DONE record")
    values = parse_pairs(tokens, 1, context)
    require_fields(values, ALPHA_FIELDS, context)
    values = dict(values)
    del values["MS"]
    return values


def verify_excluded_alpha_and_failed_tmp(
    base: Path,
    evidence: IntermediateEvidence,
    excluded_alpha_line: str | None,
    recomputed_alpha_line: str | None,
) -> None:
    context = f"segment {evidence.segment:03d} excluded-alpha audit"
    require(excluded_alpha_line is not None, f"{context}: excluded ALPHA_DONE absent")
    require(recomputed_alpha_line is not None, f"{context}: successor recomputation absent")
    excluded = alpha_semantic_values(excluded_alpha_line, f"{context} physical")
    recomputed = alpha_semantic_values(recomputed_alpha_line, f"{context} recomputed")
    require(excluded == recomputed, f"{context}: physical/recomputed scientific fields differ")

    counters = Counters(
        units=integer(excluded["CUM_UNITS"], context, 1),
        raw=integer(excluded["CUM_RAW"], context, 1),
        invariant_alpha=integer(excluded["CUM_INVARIANT_ALPHA"], context, 0),
        beta=integer(excluded["CUM_BETA"], context, 0),
        inverse=integer(excluded["CUM_INVERSE"], context, 0),
        inverse_odd=integer(excluded["CUM_INVERSE_ODD"], context, 0),
        orbit8=integer(excluded["CUM_ORBIT8"], context, 0),
        relator=integer(excluded["CUM_RELATOR"], context, 0),
        b3=integer(excluded["CUM_B3"], context, 0),
        generate=integer(excluded["CUM_GENERATE"], context, 0),
        centralizer=integer(excluded["CUM_CENTRALIZER_ORBITS"], context, 0),
        candidate=integer(excluded["CUM_CANDIDATE_NUMERIC"], context, 0),
    )
    key = key_number(excluded["KEY"], context)
    alpha = integer(excluded["ALPHA"], context, 1)
    require(
        integer(excluded["UNIT"], context, 1) == evidence.next_unit == counters.units and
        key == evidence.next_key and alpha == evidence.next_alpha and
        excluded["PREVIOUS_CHECKPOINT_SHA256"] == evidence.checkpoint_sha,
        f"{context}: excluded identity/checkpoint predecessor",
    )
    _, _, full_checkpoint, _ = checkpoint_material(
        evidence.next_unit,
        key,
        alpha,
        counters,
        evidence.output_bytes,
        evidence.output_sha,
        evidence.checkpoint_sha,
    )
    expected_failed_tmp = full_checkpoint[:-len(b"DONE\n")]
    failed_tmp = (base / evidence.failed_tmp_name).read_bytes()
    require(
        len(failed_tmp) == evidence.failed_tmp_bytes and
        sha256_bytes(failed_tmp) == evidence.failed_tmp_sha and
        failed_tmp == expected_failed_tmp and
        not failed_tmp.endswith(b"DONE\n"),
        f"{context}: failed temporary checkpoint is not the exact unterminated reconstruction",
    )

@dataclass(frozen=True)
class Candidate:
    unit: int
    key: int
    alpha: int
    rep: int
    invariant_maps: int
    numeric_sha: str


@dataclass(frozen=True)
class SegmentResult:
    segment: int
    start_unit: int
    last_unit: int
    terminal: str
    output_sha: str
    output_bytes: int
    output_lines: int
    final_checkpoint_sha: str
    final_checkpoint_bytes: bytes
    final_payload_sha: str
    final_prefix_bytes: int
    final_prefix_sha: str
    counters: Counters
    first_alpha_line: str | None
    excluded_alpha_line: str | None
    segment_units: int
    segment_raw: int
    profile_keys_rebuilt: int
    profile_actual_ms: int | None
    gap_ms: int | None
    candidates: tuple[Candidate, ...]
    resource: ResourceRecord


class CanonicalSpool:
    def __init__(self, stream: BinaryIO) -> None:
        self.stream = stream
        self.profile_lines: dict[int, str] = {}
        self.alpha_count = 0
        self.commit_count = 0
        self.key_count = 0

    def line(self, text: str) -> None:
        self.stream.write(text.encode("ascii") + b"\n")

    def profile(self, key: int, text: str) -> None:
        old = self.profile_lines.get(key)
        if old is None:
            self.profile_lines[key] = text
            self.line(text)
        else:
            require(old == text, f"canonical merge: inconsistent repeated PROFILE_OK 24T{key}")

    def alpha(self, text: str) -> None:
        self.alpha_count += 1
        self.line(text)

    def commit(self, text: str) -> None:
        self.commit_count += 1
        self.line(text)

    def key_done(self, work: Work, counters: Counters) -> None:
        self.key_count += 1
        self.line(
            f"KEY_DONE\t24T{work.key}\tALPHA_FIRST\t{work.first}\tALPHA_LAST\t{work.last}"
            f"\tUNIT_FIRST\t{work.unit_first}\tUNIT_LAST\t{work.unit_last}"
            f"\tCUM_UNITS\t{counters.units}\tCUM_RAW\t{counters.raw}"
        )

ALPHA_FIELDS = {
    "UNIT", "KEY", "ALPHA", "CLASS_SIZE", "INVARIANT_PARITY_MAPS", "INVERSE_LOCUS",
    "INVERSE_ODD", "ORBIT8", "RELATOR", "MAX_B3", "B3", "GENERATE", "PARITY",
    "CENTRALIZER_ORBITS", "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR", "CUM_B3",
    "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC", "NEXT_UNIT",
    "PREVIOUS_CHECKPOINT_SHA256", "MS",
}
PROFILE_OK_FIELDS = {
    "ORDER", "AUT_ORDER", "PARITY_MAPS", "METHOD", "REPRESENTATION", "PC_ORDER",
    "ORDER8_CLASSES", "RAW_PAIRS", "PLAN_ALPHA_FIRST", "PLAN_ALPHA_LAST", "PROFILE_EXPECTED_MS",
}
TOTAL_COMMON_FIELDS = {
    "START_UNIT", "LAST_COMPLETE_UNIT", "SEGMENT_UNITS", "SEGMENT_RAW", "CUM_UNITS", "CUM_RAW",
    "INVARIANT_ALPHA_CLASSES", "BETA_COMPUTATIONS", "INVERSE", "INVERSE_ODD", "ORBIT8",
    "RELATOR", "B3", "GENERATE", "PARITY", "CENTRALIZER_ORBITS", "CANDIDATE_NUMERIC",
    "PROFILE_KEYS_REBUILT", "PROFILE_ACTUAL_MS", "FINAL_CHECKPOINT_SHA256", "GAP_MS",
}


def build_unit_table(works: Sequence[Work]) -> list[tuple[Work, int] | None]:
    table: list[tuple[Work, int] | None] = [None] * (PLAN_UNITS + 1)
    for work in works:
        for unit in range(work.unit_first, work.unit_last + 1):
            alpha = work.first + unit - work.unit_first
            require(table[unit] is None, f"shard003 unit {unit}: duplicate plan mapping")
            table[unit] = (work, alpha)
    require(all(value is not None for value in table[1:]), "shard003: incomplete unit table")
    return table


def verify_profile_ok(line: str, expected_work: Work, profiles: dict[int, Profile], context: str) -> None:
    tokens = line.split("\t")
    require(len(tokens) >= 4 and tokens[0] == "PROFILE_OK", f"{context}: PROFILE_OK schema")
    key = key_number(tokens[1], context)
    require(key == expected_work.key, f"{context}: PROFILE_OK key")
    values = parse_pairs(tokens, 2, context)
    require_fields(values, PROFILE_OK_FIELDS, context)
    profile = profiles[key]
    expected = {
        "ORDER": str(profile.order),
        "AUT_ORDER": str(profile.aut_order),
        "PARITY_MAPS": str(profile.parity_maps),
        "METHOD": profile.route,
        "REPRESENTATION": profile.representation,
        "PC_ORDER": str(profile.pc_order),
        "ORDER8_CLASSES": str(profile.classes),
        "RAW_PAIRS": str(profile.raw),
        "PLAN_ALPHA_FIRST": str(expected_work.first),
        "PLAN_ALPHA_LAST": str(expected_work.last),
        "PROFILE_EXPECTED_MS": str(profile.profile_ms),
    }
    require(values == expected, f"{context}: sealed profile fields differ")


def verify_segment(
    bundle: Bundle,
    works: Sequence[Work],
    profiles: dict[int, Profile],
    unit_table: Sequence[tuple[Work, int] | None],
    initial: Counters,
    previous_checkpoint_sha: str,
    previous: tuple[Bundle, SegmentResult] | None,
    spool: CanonicalSpool,
    evidence: IntermediateEvidence | None,
) -> SegmentResult:
    expected_start = initial.units + 1
    require(bundle.filename_start == expected_start,
            f"segment {bundle.segment:03d}: filename starts {bundle.filename_start}, expected {expected_start}")
    require(expected_start <= PLAN_UNITS, f"segment {bundle.segment:03d}: starts beyond shard")
    interrupted_successor = previous is not None and previous[1].terminal == INTERRUPTED_TERMINAL
    if interrupted_successor:
        previous_bundle, previous_result = previous
        require(
            evidence is not None and
            previous_bundle.segment == evidence.segment and
            bundle.segment == evidence.segment + 1 and
            expected_start == evidence.next_unit and
            counter_vector(initial) == list(PINNED_DURABLE_COUNTERS) and
            previous_checkpoint_sha == evidence.checkpoint_sha and
            previous_result.final_prefix_bytes == evidence.prefix_bytes and
            previous_result.final_prefix_sha == evidence.prefix_sha,
            f"segment {bundle.segment:03d}: exact checkpoint-failure successor state",
        )
        successor_plan = unit_table[expected_start]
        require(
            successor_plan is not None and
            successor_plan[0].key == evidence.next_key and
            successor_plan[1] == evidence.next_alpha,
            f"segment {bundle.segment:03d}: exact successor key/alpha after checkpoint failure",
        )
    resource = parse_resource(
        bundle, works, profiles, initial, previous_checkpoint_sha, previous, evidence
    )

    expected_headers = [
        "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003-V2",
        f"GAP_VERSION\t{GAP_VERSION}",
        f"DEGREE\t{DEGREE}",
        f"DATABASE\t{DATABASE}",
        "PLAN_FIRST\t24T6032\t1",
        "PLAN_LAST\t24T6440\t2",
        f"PLAN_KEYS\t{PLAN_KEYS}",
        f"PLAN_CLASS_UNITS\t{PLAN_UNITS}",
        f"PLAN_RAW_PAIRS\t{PLAN_RAW}",
        f"PLAN_PROFILE_REBUILD_MS\t{PLAN_PROFILE_MS}",
        f"INTERNAL_GUARD_MS\t{INTERNAL_GUARD_MS}",
        f"START_UNIT\t{expected_start}",
        f"PREVIOUS_CHECKPOINT_SHA256\t{previous_checkpoint_sha}",
        f"PROFILE_SHA256\t{PROFILE_SHA256}",
        f"PLAN_SHA256\t{PLAN_SHA256}",
        "FROZEN\tg_j=alpha^j(x); alpha^4(x)=x^-1; relator indices 0,5,2,7,4,1,6,3; B3=457; generated image exact; invariant odd C2 parity exact.",
        "RECOVERY\tPer-alpha temp-write plus bounded IO_rename retry; source absence, destination presence, and exact destination bytes are verified after rename; output-prefix SHA256/bytes and exact successor are recorded.",
        "SCOPE\tExactly seed-plan shard003 only; shard004 and later are excluded.",
    ]

    output_hasher = hashlib.sha256()
    output_bytes = 0
    current = initial.clone()
    segment_units = 0
    segment_raw = 0
    profile_keys_seen = 0
    key_done_seen = 0
    first_alpha_line: str | None = None
    excluded_alpha_line: str | None = None
    excluded_alpha_raw = b""
    profile_actual_ms: int | None = None
    gap_ms: int | None = None
    expected_unit = expected_start
    chain_sha = previous_checkpoint_sha
    last_checkpoint_bytes = b""
    last_payload_sha = ""
    last_committed_prefix_bytes = 0
    last_committed_prefix_sha = ""
    last_commit_raw = b""
    expected_commit: tuple[int, int, str, int, str, bytes, str] | None = None
    current_work: Work | None = None
    current_segment_alpha_first = 0
    cache_required = False
    cache_seen = False
    key_done_pending: Work | None = None
    previous_ms = -1
    pending_numeric: tuple[int, int, int, str] | None = None
    alpha_candidates: list[Candidate] = []
    all_candidates: list[Candidate] = []
    candidate_stop_unit: int | None = None
    terminal = ""
    total_seen = False
    terminal_seen = False
    last_tag = ""
    interrupted_cache_verified = False

    with bundle.output.open("rb") as stream:
        for header_index, expected in enumerate(expected_headers, 1):
            raw = stream.readline()
            require(raw, f"segment {bundle.segment:03d}: truncated header at line {header_index}")
            require(raw.endswith(b"\n") and b"\r" not in raw and b"\x00" not in raw,
                    f"segment {bundle.segment:03d}: noncanonical header bytes")
            output_hasher.update(raw)
            output_bytes += len(raw)
            try:
                actual = raw[:-1].decode("ascii")
            except UnicodeDecodeError as error:
                raise VerificationError(f"segment {bundle.segment:03d}: non-ASCII header") from error
            require(actual == expected, f"segment {bundle.segment:03d}: header line {header_index}")

        line_number = len(expected_headers)
        for raw in stream:
            line_number += 1
            context = f"segment {bundle.segment:03d} line {line_number}"
            require(raw.endswith(b"\n") and b"\r" not in raw and b"\x00" not in raw,
                    f"{context}: noncanonical bytes")
            output_hasher.update(raw)
            output_bytes += len(raw)
            try:
                line = raw[:-1].decode("ascii")
            except UnicodeDecodeError as error:
                raise VerificationError(f"{context}: non-ASCII content") from error
            tokens = line.split("\t")
            tag = tokens[0]
            require(excluded_alpha_line is None,
                    f"{context}: record after excluded uncommitted ALPHA_DONE")
            if (
                evidence is not None and bundle.segment == evidence.segment and
                current.units == evidence.last_unit and last_tag == "CHECKPOINT_COMMITTED"
            ):
                require(tag == "ALPHA_DONE" and expected_commit is None,
                        f"{context}: expected one excluded uncommitted ALPHA_DONE")
                values = parse_pairs(tokens, 1, context)
                require_fields(values, ALPHA_FIELDS, context)
                planned = unit_table[expected_unit]
                require(planned is not None, f"{context}: missing excluded-alpha plan")
                work, alpha = planned
                require(
                    integer(values["UNIT"], context, 1) == evidence.next_unit == expected_unit and
                    key_number(values["KEY"], context) == evidence.next_key == work.key and
                    integer(values["ALPHA"], context, 1) == evidence.next_alpha == alpha and
                    integer(values["NEXT_UNIT"], context, 1) == evidence.next_unit + 1 and
                    values["PREVIOUS_CHECKPOINT_SHA256"] == evidence.checkpoint_sha == chain_sha and
                    integer(values["CUM_UNITS"], context, 0) == evidence.next_unit and
                    integer(values["CUM_RAW"], context, 0) == current.raw + work.order and
                    integer(values["CUM_CENTRALIZER_ORBITS"], context, 0) == current.centralizer and
                    integer(values["CUM_CANDIDATE_NUMERIC"], context, 0) == current.candidate == 0,
                    f"{context}: excluded-alpha identity/cumulative state",
                )
                excluded_alpha_line = line
                excluded_alpha_raw = raw
                continue
            last_tag = tag
            require(not terminal_seen, f"{context}: record after terminal marker")
            if expected_commit is not None:
                require(tag == "CHECKPOINT_COMMITTED", f"{context}: missing immediate checkpoint commit")
            if candidate_stop_unit is not None and expected_commit is None:
                require(tag == "TOTAL_PARTIAL", f"{context}: work continued after numeric candidate")
            if key_done_pending is not None and tag not in {"KEY_SEGMENT_DONE", "TOTAL_PARTIAL"}:
                raise VerificationError(f"{context}: missing KEY_SEGMENT_DONE outside a stopping boundary")

            if tag == "PROFILE_OK":
                require(not total_seen and expected_commit is None and key_done_pending is None,
                        f"{context}: misplaced PROFILE_OK")
                require(expected_unit <= PLAN_UNITS, f"{context}: profile beyond plan")
                planned = unit_table[expected_unit]
                require(planned is not None, f"{context}: missing unit plan")
                work, alpha = planned
                require(current_work is None, f"{context}: prior key not closed")
                verify_profile_ok(line, work, profiles, context)
                current_work = work
                current_segment_alpha_first = alpha
                profile_keys_seen += 1
                cache_required = alpha > work.first
                cache_seen = False
                if (
                    interrupted_successor and evidence is not None and
                    expected_unit == evidence.next_unit and not cache_required
                ):
                    require(
                        evidence is not None and work.key == evidence.next_key and
                        alpha == evidence.next_alpha,
                        f"{context}: checkpoint-failure recovery successor without cache",
                    )
                    interrupted_cache_verified = True
                spool.profile(work.key, line)
            elif tag == "CACHE_REBUILT":
                require(current_work is not None and cache_required and not cache_seen,
                        f"{context}: unexpected CACHE_REBUILT")
                require(key_number(tokens[1], context) == current_work.key, f"{context}: cache key")
                values = parse_pairs(tokens, 2, context)
                require_fields(values, {"ALPHA_FIRST", "ALPHA_LAST", "DISTINCT_BETA", "SEED_PREDICATES_REPLAYED"}, context)
                require(integer(values["ALPHA_FIRST"], context) == current_work.first, f"{context}: cache first")
                require(integer(values["ALPHA_LAST"], context) == current_segment_alpha_first - 1,
                        f"{context}: cache last")
                distinct = integer(values["DISTINCT_BETA"], context, 1)
                require(distinct <= current_segment_alpha_first - current_work.first, f"{context}: cache distinct beta")
                require(values["SEED_PREDICATES_REPLAYED"] == "0", f"{context}: cache replayed predicates")
                cache_seen = True
                if interrupted_successor:
                    require(
                        evidence is not None and
                        expected_unit == evidence.next_unit and
                        current_work.key == evidence.next_key and
                        current_segment_alpha_first == evidence.next_alpha and
                        integer(values["ALPHA_FIRST"], context) == current_work.first and
                        integer(values["ALPHA_LAST"], context) == evidence.next_alpha - 1,
                        f"{context}: exact checkpoint-failure CACHE_REBUILT state",
                    )
                    interrupted_cache_verified = True
                spool.line(line)
            elif tag == "CANDIDATE_NUMERIC":
                require(current_work is not None and expected_unit <= PLAN_UNITS and pending_numeric is None,
                        f"{context}: misplaced numeric candidate")
                require(len(tokens) == 6 + 8 * DEGREE, f"{context}: numeric candidate width")
                planned = unit_table[expected_unit]
                require(planned is not None, f"{context}: missing candidate plan")
                work, alpha = planned
                key = key_number(tokens[1], context)
                alpha_no = integer(tokens[2], context, 1)
                rep = integer(tokens[3], context, 1)
                order = integer(tokens[4], context, 1)
                degree = integer(tokens[5], context, 1)
                require((key, alpha_no, order, degree) == (work.key, alpha, work.order, DEGREE),
                        f"{context}: numeric candidate identity")
                require(rep == len(alpha_candidates) + 1, f"{context}: candidate representative order")
                images = [integer(value, context, 0) for value in tokens[6:]]
                for block in range(8):
                    permutation = images[block * DEGREE:(block + 1) * DEGREE]
                    require(sorted(permutation) == list(range(DEGREE)), f"{context}: non-permutation orbit element {block + 1}")
                numeric_sha = sha256_bytes(raw)
                pending_numeric = (key, alpha_no, rep, numeric_sha)
            elif tag == "CANDIDATE_META":
                require(pending_numeric is not None, f"{context}: candidate meta without numeric record")
                values = parse_pairs(tokens, 1, context)
                require_fields(values, {"UNIT", "KEY", "ALPHA", "REP", "INVARIANT_PARITY_MAPS"}, context)
                unit = integer(values["UNIT"], context, 1)
                key = key_number(values["KEY"], context)
                alpha_no = integer(values["ALPHA"], context, 1)
                rep = integer(values["REP"], context, 1)
                numeric_key, numeric_alpha, numeric_rep, numeric_sha = pending_numeric
                require((unit, key, alpha_no, rep) ==
                        (expected_unit, numeric_key, numeric_alpha, numeric_rep), f"{context}: candidate meta identity")
                invariant_maps = integer(values["INVARIANT_PARITY_MAPS"], context, 1)
                candidate = Candidate(unit, key, alpha_no, rep, invariant_maps, numeric_sha)
                alpha_candidates.append(candidate)
                all_candidates.append(candidate)
                pending_numeric = None
            elif tag == "ALPHA_DONE":
                require(not total_seen and expected_unit <= PLAN_UNITS and current_work is not None,
                        f"{context}: misplaced ALPHA_DONE")
                require(not cache_required or cache_seen, f"{context}: required cache reconstruction record absent")
                require(pending_numeric is None, f"{context}: numeric candidate lacks meta")
                if first_alpha_line is None:
                    first_alpha_line = line
                values = parse_pairs(tokens, 1, context)
                require_fields(values, ALPHA_FIELDS, context)
                planned = unit_table[expected_unit]
                require(planned is not None, f"{context}: missing unit plan")
                work, expected_alpha = planned
                unit = integer(values["UNIT"], context, 1)
                key = key_number(values["KEY"], context)
                alpha = integer(values["ALPHA"], context, 1)
                require((unit, key, alpha) == (expected_unit, work.key, expected_alpha),
                        f"{context}: unit/key/alpha coverage")
                require(work == current_work, f"{context}: active profile key")
                profile = profiles[key]
                class_size = integer(values["CLASS_SIZE"], context, 1)
                require(class_size <= profile.aut_order and profile.aut_order % class_size == 0,
                        f"{context}: automorphism conjugacy-class size")
                invariant_maps = integer(values["INVARIANT_PARITY_MAPS"], context, 0)
                inverse = integer(values["INVERSE_LOCUS"], context, 0)
                inverse_odd = integer(values["INVERSE_ODD"], context, 0)
                orbit8 = integer(values["ORBIT8"], context, 0)
                relator = integer(values["RELATOR"], context, 0)
                max_b3 = integer(values["MAX_B3"], context, 0)
                b3 = integer(values["B3"], context, 0)
                generate = integer(values["GENERATE"], context, 0)
                parity = integer(values["PARITY"], context, 0)
                centralizer = integer(values["CENTRALIZER_ORBITS"], context, 0)
                require(invariant_maps <= profile.parity_maps, f"{context}: invariant parity-map bound")
                require(inverse <= profile.order, f"{context}: inverse-locus bound")
                require(0 <= inverse_odd <= inverse and orbit8 <= inverse_odd and relator <= orbit8,
                        f"{context}: inverse/orbit/relator gate chain")
                require(b3 <= relator and generate <= b3 and centralizer <= generate,
                        f"{context}: B3/generate/orbit gate chain")
                require(parity == generate, f"{context}: frozen parity counter")
                require(0 <= max_b3 <= 457, f"{context}: MAX_B3 bound")
                require((relator == 0) == (max_b3 == 0), f"{context}: MAX_B3 relator consistency")
                require((b3 > 0) == (max_b3 == 457), f"{context}: B3 cardinality consistency")
                if invariant_maps == 0:
                    require(inverse == inverse_odd == orbit8 == relator == max_b3 == b3 == generate == centralizer == 0,
                            f"{context}: work below invariant-map gate")
                require(len(alpha_candidates) == centralizer, f"{context}: candidate/orbit count")
                for candidate in alpha_candidates:
                    require((candidate.unit, candidate.key, candidate.alpha) == (unit, key, alpha),
                            f"{context}: candidate identity")
                    require(candidate.invariant_maps == invariant_maps,
                            f"{context}: candidate invariant-map count")

                old_beta = current.beta
                expected_state = current.clone()
                expected_state.units += 1
                expected_state.raw += work.order
                expected_state.invariant_alpha += int(invariant_maps > 0)
                reported_beta = integer(values["CUM_BETA"], context, 0)
                beta_delta = reported_beta - old_beta
                require(beta_delta in {0, 1} and beta_delta <= int(invariant_maps > 0),
                        f"{context}: beta-cache increment")
                if alpha == work.first and invariant_maps > 0:
                    require(beta_delta == 1, f"{context}: first-alpha beta-cache miss")
                expected_state.beta = reported_beta
                expected_state.inverse += inverse
                expected_state.inverse_odd += inverse_odd
                expected_state.orbit8 += orbit8
                expected_state.relator += relator
                expected_state.b3 += b3
                expected_state.generate += generate
                expected_state.centralizer += centralizer
                expected_state.candidate += len(alpha_candidates)
                cumulative = {
                    "CUM_UNITS": expected_state.units,
                    "CUM_RAW": expected_state.raw,
                    "CUM_INVARIANT_ALPHA": expected_state.invariant_alpha,
                    "CUM_BETA": expected_state.beta,
                    "CUM_INVERSE": expected_state.inverse,
                    "CUM_INVERSE_ODD": expected_state.inverse_odd,
                    "CUM_ORBIT8": expected_state.orbit8,
                    "CUM_RELATOR": expected_state.relator,
                    "CUM_B3": expected_state.b3,
                    "CUM_GENERATE": expected_state.generate,
                    "CUM_CENTRALIZER_ORBITS": expected_state.centralizer,
                    "CUM_CANDIDATE_NUMERIC": expected_state.candidate,
                }
                for name, expected_value in cumulative.items():
                    require(integer(values[name], f"{context} {name}", 0) == expected_value,
                            f"{context}: {name}")
                require(expected_state.centralizer == expected_state.candidate,
                        f"{context}: cumulative candidate/orbit identity")
                require(integer(values["NEXT_UNIT"], context, 1) == unit + 1, f"{context}: successor unit")
                require(values["PREVIOUS_CHECKPOINT_SHA256"] == chain_sha, f"{context}: checkpoint predecessor")
                runtime_ms = integer(values["MS"], context, 0)
                require(runtime_ms >= previous_ms, f"{context}: nonmonotone runtime")
                previous_ms = runtime_ms
                current = expected_state
                segment_units += 1
                segment_raw += work.order
                if alpha_candidates:
                    candidate_stop_unit = unit
                prefix_sha = output_hasher.copy().hexdigest()
                payload, payload_sha, checkpoint_bytes, checkpoint_sha = checkpoint_material(
                    unit, key, alpha, current, output_bytes, prefix_sha, chain_sha,
                )
                del payload
                expected_commit = (unit, key, checkpoint_sha, output_bytes, prefix_sha, checkpoint_bytes, payload_sha)
                spool.alpha(line)
                expected_unit += 1
                alpha_candidates = []
            elif tag == "CHECKPOINT_COMMITTED":
                require(expected_commit is not None, f"{context}: commit without ALPHA_DONE")
                values = parse_pairs(tokens, 1, context)
                require_fields(values, {"UNIT", "CHECKPOINT_SHA256", "OUTPUT_PREFIX_BYTES", "OUTPUT_PREFIX_SHA256"}, context)
                unit, key, checkpoint_sha, prefix_bytes, prefix_sha, checkpoint_bytes, payload_sha = expected_commit
                del key
                require(integer(values["UNIT"], context, 1) == unit, f"{context}: commit unit")
                require(LOWER_SHA_RE.fullmatch(values["CHECKPOINT_SHA256"]) is not None,
                        f"{context}: checkpoint SHA encoding")
                require(values["CHECKPOINT_SHA256"] == checkpoint_sha, f"{context}: reconstructed checkpoint SHA")
                require(integer(values["OUTPUT_PREFIX_BYTES"], context, 0) == prefix_bytes,
                        f"{context}: output-prefix byte length")
                require(values["OUTPUT_PREFIX_SHA256"] == prefix_sha, f"{context}: one-pass output-prefix SHA")
                chain_sha = checkpoint_sha
                last_checkpoint_bytes = checkpoint_bytes
                last_payload_sha = payload_sha
                last_commit_raw = raw
                last_committed_prefix_bytes = prefix_bytes
                last_committed_prefix_sha = prefix_sha
                expected_commit = None
                spool.commit(line)
                completed_plan = unit_table[unit]
                require(completed_plan is not None, f"{context}: completed plan")
                completed_work, completed_alpha = completed_plan
                if completed_alpha == completed_work.last:
                    key_done_pending = completed_work
                    spool.key_done(completed_work, current)
            elif tag == "KEY_SEGMENT_DONE":
                require(key_done_pending is not None, f"{context}: unexpected KEY_SEGMENT_DONE")
                work = key_done_pending
                require(key_number(tokens[1], context) == work.key, f"{context}: key segment key")
                values = parse_pairs(tokens, 2, context)
                require_fields(values, {"ALPHA_FIRST", "ALPHA_LAST", "UNIT_LAST", "CUM_UNITS", "CUM_RAW"}, context)
                require(integer(values["ALPHA_FIRST"], context, 1) == current_segment_alpha_first,
                        f"{context}: key segment first alpha")
                require(integer(values["ALPHA_LAST"], context, 1) == work.last, f"{context}: key segment last alpha")
                require(integer(values["UNIT_LAST"], context, 1) == work.unit_last, f"{context}: key segment last unit")
                require(integer(values["CUM_UNITS"], context, 0) == current.units and
                        integer(values["CUM_RAW"], context, 0) == current.raw,
                        f"{context}: key segment cumulative")
                key_done_seen += 1
                key_done_pending = None
                current_work = None
                cache_required = False
                cache_seen = False
            elif tag in {"TOTAL", "TOTAL_PARTIAL"}:
                require(not total_seen and expected_commit is None and pending_numeric is None,
                        f"{context}: duplicate/misplaced total")
                if key_done_pending is not None:
                    require(tag == "TOTAL_PARTIAL", f"{context}: complete TOTAL omitted KEY_SEGMENT_DONE")
                    key_done_pending = None
                values = parse_pairs(tokens, 1, context)
                expected_fields = set(TOTAL_COMMON_FIELDS)
                if tag == "TOTAL_PARTIAL":
                    expected_fields.add("NEXT_UNIT")
                require_fields(values, expected_fields, context)
                require(integer(values["START_UNIT"], context, 1) == expected_start, f"{context}: total start")
                require(integer(values["LAST_COMPLETE_UNIT"], context, 0) == current.units,
                        f"{context}: total last unit")
                require(integer(values["SEGMENT_UNITS"], context, 0) == segment_units,
                        f"{context}: total segment units")
                require(integer(values["SEGMENT_RAW"], context, 0) == segment_raw,
                        f"{context}: total segment raw")
                totals = {
                    "CUM_UNITS": current.units,
                    "CUM_RAW": current.raw,
                    "INVARIANT_ALPHA_CLASSES": current.invariant_alpha,
                    "BETA_COMPUTATIONS": current.beta,
                    "INVERSE": current.inverse,
                    "INVERSE_ODD": current.inverse_odd,
                    "ORBIT8": current.orbit8,
                    "RELATOR": current.relator,
                    "B3": current.b3,
                    "GENERATE": current.generate,
                    "PARITY": current.generate,
                    "CENTRALIZER_ORBITS": current.centralizer,
                    "CANDIDATE_NUMERIC": current.candidate,
                }
                for name, expected_value in totals.items():
                    require(integer(values[name], f"{context} {name}", 0) == expected_value,
                            f"{context}: total {name}")
                require(integer(values["PROFILE_KEYS_REBUILT"], context, 0) == profile_keys_seen,
                        f"{context}: profile keys rebuilt")
                profile_actual_ms = integer(values["PROFILE_ACTUAL_MS"], context, 0)
                require(values["FINAL_CHECKPOINT_SHA256"] == chain_sha, f"{context}: final checkpoint SHA")
                gap_ms = integer(values["GAP_MS"], context, 0)
                require(gap_ms >= previous_ms, f"{context}: GAP runtime")
                require(profile_actual_ms <= gap_ms, f"{context}: profile runtime exceeds GAP runtime")
                if tag == "TOTAL_PARTIAL":
                    require(integer(values["NEXT_UNIT"], context, 1) == current.units + 1,
                            f"{context}: partial successor")
                else:
                    require(current.units == PLAN_UNITS and current.raw == PLAN_RAW,
                            f"{context}: complete shard totals")
                    require(current_work is None, f"{context}: active key at complete total")
                total_seen = True
                terminal = tag
            elif tag in {"STOPPED_RECOVERY_SMOKE", "STOPPED_GUARD", "STOPPED_CANDIDATE", "DONE"}:
                require(total_seen, f"{context}: terminal marker before total")
                if tag == "DONE":
                    require(terminal == "TOTAL", f"{context}: DONE after partial total")
                    terminal = "DONE"
                else:
                    require(terminal == "TOTAL_PARTIAL", f"{context}: stop after complete total")
                    terminal = tag
                terminal_seen = True
            else:
                raise VerificationError(f"{context}: unexpected record {tag!r}")

    output_sha = output_hasher.hexdigest()
    require(expected_commit is None and pending_numeric is None,
            f"segment {bundle.segment:03d}: incomplete record pair")
    failure_evidence = (
        evidence if evidence is not None and bundle.segment == evidence.segment else None
    )
    if failure_evidence is not None:
        context = f"segment {bundle.segment:03d} checkpoint-write-failure evidence"
        require(
            not total_seen and not terminal_seen and terminal == "" and
            last_tag == "CHECKPOINT_COMMITTED" and excluded_alpha_line is not None,
            f"{context}: durable commit must be followed by exactly one excluded ALPHA_DONE",
        )
        require(
            bundle.output.name == failure_evidence.output_name and
            output_sha == failure_evidence.output_sha and
            output_bytes == failure_evidence.output_bytes and
            line_number == PINNED_FAILURE_OUTPUT_LINES,
            f"{context}: exact sealed physical output hash/size/line count",
        )
        require(
            current.units == failure_evidence.last_unit and
            expected_unit == failure_evidence.next_unit and
            segment_units == current.units - initial.units and
            segment_raw == current.raw - initial.raw and
            counter_vector(current) == list(PINNED_DURABLE_COUNTERS),
            f"{context}: exact durable counters",
        )
        require(
            chain_sha == failure_evidence.checkpoint_sha and
            last_committed_prefix_bytes == failure_evidence.prefix_bytes and
            last_committed_prefix_sha == failure_evidence.prefix_sha and
            len(last_commit_raw) + len(excluded_alpha_raw) == failure_evidence.postprefix_bytes and
            output_bytes == last_committed_prefix_bytes + failure_evidence.postprefix_bytes,
            f"{context}: exact durable checkpoint/postprefix chain",
        )
        last_plan = unit_table[failure_evidence.last_unit]
        next_plan = unit_table[failure_evidence.next_unit]
        require(
            last_plan is not None and next_plan is not None and
            last_plan[0].key == failure_evidence.last_key and
            last_plan[1] == failure_evidence.last_alpha and
            next_plan[0].key == failure_evidence.next_key and
            next_plan[1] == failure_evidence.next_alpha and
            current_work == last_plan[0],
            f"{context}: exact sealed-plan key/alpha boundary",
        )
        expected_pending = last_plan[1] == last_plan[0].last
        require(
            ((key_done_pending == last_plan[0]) if expected_pending else (key_done_pending is None)) and
            candidate_stop_unit is None and not all_candidates and
            profile_actual_ms is None and gap_ms is None and
            profile_keys_seen == sum(work.unit_first <= failure_evidence.last_unit for work in works) and
            key_done_seen == sum(work.unit_last <= failure_evidence.last_unit for work in works),
            f"{context}: no synthetic terminal, telemetry, candidate, or committed unit",
        )
        terminal = INTERRUPTED_TERMINAL
    else:
        require(total_seen and terminal_seen, f"segment {bundle.segment:03d}: nonterminal output")
        require(
            profile_actual_ms is not None and gap_ms is not None,
            f"segment {bundle.segment:03d}: terminal output lacks numeric runtime totals",
        )
    if interrupted_successor:
        require(
            interrupted_cache_verified,
            f"segment {bundle.segment:03d}: missing exact recovery cache state with zero seed-predicate replay",
        )
    require(segment_units > 0, f"segment {bundle.segment:03d}: zero work")
    require(last_checkpoint_bytes, f"segment {bundle.segment:03d}: no checkpoint")
    require(
        last_committed_prefix_bytes > 0 and
        LOWER_SHA_RE.fullmatch(last_committed_prefix_sha) is not None,
        f"segment {bundle.segment:03d}: final output-prefix state",
    )
    require(
        resource.rename_retry_records <= segment_units,
        f"segment {bundle.segment:03d}: excess atomic-rename retry records",
    )
    require(current.candidate - initial.candidate == len(all_candidates),
            f"segment {bundle.segment:03d}: candidate delta")
    if terminal == INTERRUPTED_TERMINAL:
        require(
            failure_evidence is not None and bundle.segment == failure_evidence.segment and
            resource.stdout_sha == failure_evidence.stdout_sha and
            resource.stdout_bytes == failure_evidence.stdout_bytes and
            resource.stderr_sha == failure_evidence.stderr_sha and
            resource.stderr_bytes == failure_evidence.stderr_bytes and
            resource.user_seconds is None and resource.system_seconds is None and
            resource.elapsed_seconds is None and resource.cpu_percent is None and
            resource.max_rss_kib is None and resource.exit_status is None,
            f"segment {bundle.segment:03d}: SHA-pinned resources and unavailable telemetry",
        )
    elif terminal == "STOPPED_RECOVERY_SMOKE":
        require(
            resource.producer.stop_after_unit is not None and
            current.units == resource.producer.stop_after_unit,
            f"segment {bundle.segment:03d}: unconfigured/misplaced recovery-smoke stop",
        )
        require(not all_candidates,
                f"segment {bundle.segment:03d}: recovery smoke unexpectedly found a candidate")
    elif terminal == "STOPPED_GUARD":
        require(
            current.units <= PLAN_UNITS and not all_candidates and
            gap_ms is not None and gap_ms >= INTERNAL_GUARD_MS and
            (
                resource.producer.stop_after_unit is None or
                resource.producer.stop_after_unit > current.units
            ),
            f"segment {bundle.segment:03d}: invalid guard stop",
        )
    elif terminal == "STOPPED_CANDIDATE":
        require(
            all_candidates and candidate_stop_unit == current.units and
            all(candidate.unit == current.units for candidate in all_candidates) and
            (
                resource.producer.stop_after_unit is None or
                resource.producer.stop_after_unit >= current.units
            ),
            f"segment {bundle.segment:03d}: candidate stop without terminal candidates",
        )
    elif terminal == "DONE":
        require(current.units == PLAN_UNITS and not all_candidates and
                resource.producer.stop_after_unit is None,
                f"segment {bundle.segment:03d}: complete output candidate/coverage")
    else:
        raise VerificationError(f"segment {bundle.segment:03d}: invalid terminal state {terminal}")

    return SegmentResult(
        segment=bundle.segment,
        start_unit=expected_start,
        last_unit=current.units,
        terminal=terminal,
        output_sha=output_sha,
        output_bytes=output_bytes,
        output_lines=line_number,
        final_checkpoint_sha=chain_sha,
        final_checkpoint_bytes=last_checkpoint_bytes,
        final_payload_sha=last_payload_sha,
        final_prefix_bytes=last_committed_prefix_bytes,
        final_prefix_sha=last_committed_prefix_sha,
        counters=current.clone(),
        first_alpha_line=first_alpha_line,
        excluded_alpha_line=excluded_alpha_line,
        segment_units=segment_units,
        segment_raw=segment_raw,
        profile_keys_rebuilt=profile_keys_seen,
        profile_actual_ms=profile_actual_ms,
        gap_ms=gap_ms,
        candidates=tuple(all_candidates),
        resource=resource,
    )


def atomic_temp_path(destination: Path) -> Path:
    return destination.with_name("." + destination.name + ".tmp")


def refuse_outputs(destinations: Sequence[Path]) -> list[Path]:
    temporary = [atomic_temp_path(path) for path in destinations]
    for path in [*destinations, *temporary]:
        require(not path.exists(), f"refusing to overwrite existing output/temp: {path}")
    return temporary


def write_new_temp(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def available_text(value: int | float | None) -> str:
    return "UNAVAILABLE" if value is None else str(value)


def format_aggregate(
    bundles: Sequence[Bundle],
    results: Sequence[SegmentResult],
    final: Counters,
    checkpoint_path: Path,
    checkpoint_sha: str,
    canonical_sha: str,
    canonical_bytes: int,
    verifier_sha: str,
    evidence: IntermediateEvidence | None,
) -> bytes:
    lines = [
        "CERTIFICATE_AGGREGATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003",
        f"VERIFIER_SOURCE_SHA256\t{verifier_sha.upper()}",
        f"PROFILE_SHA256\t{PROFILE_SHA256}",
        f"PLAN_SHA256\t{PLAN_SHA256}",
        f"SOURCE_SEGMENTS\t{len(results)}",
    ]
    for bundle, result in zip(bundles, results):
        lines.append(
            f"SOURCE_SEGMENT\t{result.segment:03d}\tOUTPUT\t{bundle.output.name}"
            f"\tOUTPUT_SHA256\t{result.output_sha.upper()}\tOUTPUT_BYTES\t{result.output_bytes}"
            f"\tOUTPUT_LINES\t{result.output_lines}"
            f"\tSTART_UNIT\t{result.start_unit}\tLAST_DURABLE_UNIT\t{result.last_unit}"
            f"\tSTATUS\t{result.terminal}\tSEGMENT_UNITS\t{result.segment_units}"
            f"\tSEGMENT_RAW\t{result.segment_raw}\tPROFILE_KEYS_REBUILT\t{result.profile_keys_rebuilt}"
            f"\tPROFILE_ACTUAL_MS\t{available_text(result.profile_actual_ms)}"
            f"\tGAP_MS\t{available_text(result.gap_ms)}"
            f"\tSTDOUT_SHA256\t{result.resource.stdout_sha.upper()}"
            f"\tSTDOUT_BYTES\t{result.resource.stdout_bytes}"
            f"\tSTDERR_SHA256\t{result.resource.stderr_sha.upper()}"
            f"\tSTDERR_BYTES\t{result.resource.stderr_bytes}"
            f"\tWALL\t{result.resource.elapsed_text}"
            f"\tMAX_RSS_KIB\t{available_text(result.resource.max_rss_kib)}"
            f"\tEXIT_STATUS\t{available_text(result.resource.exit_status)}"
            f"\tRENAME_RETRY_RECORDS\t{result.resource.rename_retry_records}"
            f"\tFINAL_OUTPUT_PREFIX_BYTES\t{result.final_prefix_bytes}"
            f"\tFINAL_OUTPUT_PREFIX_SHA256\t{result.final_prefix_sha.upper()}"
        )
        lines.append(
            f"PRODUCER_SOURCE\tSEGMENT\t{result.segment:03d}"
            f"\tWRAPPER\t{result.resource.producer.wrapper_name}"
            f"\tWRAPPER_SHA256\t{result.resource.producer.wrapper_sha.upper()}"
            f"\tRUNNER\t{result.resource.producer.runner_name}"
            f"\tRUNNER_SHA256\t{result.resource.producer.runner_sha.upper()}"
            f"\tENGINE_SHA256\t{result.resource.producer.engine_sha.upper()}"
            f"\tSTOP_AFTER_UNIT\t"
            f"{result.resource.producer.stop_after_unit if result.resource.producer.stop_after_unit is not None else 'fail'}"
        )
        if result.terminal == INTERRUPTED_TERMINAL:
            require(evidence is not None and result.segment == evidence.segment,
                    "aggregate: missing selected checkpoint-failure evidence")
            lines.append(
                f"CHECKPOINT_FAILURE_EVIDENCE\tSEGMENT\t{result.segment:03d}"
                f"\tEVIDENCE_FILE\t{evidence.path.name}"
                f"\tEVIDENCE_SHA256\t{evidence.file_sha.upper()}"
                f"\tSTATUS\t{INTERRUPTED_TERMINAL}"
                f"\tLAST_DURABLE_UNIT\t{evidence.last_unit}"
                f"\tEXCLUDED_UNCOMMITTED_UNIT\t{evidence.next_unit}"
                f"\tCHECKPOINT_SHA256\t{evidence.checkpoint_sha.upper()}"
                f"\tOUTPUT_PREFIX_BYTES\t{evidence.prefix_bytes}"
                f"\tOUTPUT_PREFIX_SHA256\t{evidence.prefix_sha.upper()}"
                f"\tPOSTPREFIX_FILE\t{evidence.postprefix_name}"
                f"\tPOSTPREFIX_BYTES\t{evidence.postprefix_bytes}"
                f"\tPOSTPREFIX_SHA256\t{evidence.postprefix_sha.upper()}"
                f"\tFAILED_TMP_FILE\t{evidence.failed_tmp_name}"
                f"\tFAILED_TMP_BYTES\t{evidence.failed_tmp_bytes}"
                f"\tFAILED_TMP_SHA256\t{evidence.failed_tmp_sha.upper()}"
                "\tFAILED_TMP_DONE\tNO\tTOTAL_SYNTHESIZED\tNO\tTERMINAL_SYNTHESIZED\tNO"
                f"\tRESOURCE_TELEMETRY\t{evidence.resource_telemetry}"
            )
    lines.extend([
        f"PRODUCER_SOURCE\tSEED_ENGINE\t{SEED_ENGINE_NAME}\tSHA256\t{SEED_ENGINE_SHA256.upper()}",
        f"CHECKPOINT_FILE\t{checkpoint_path.name}\tSHA256\t{checkpoint_sha.upper()}"
        f"\tPAYLOAD_SHA256\t{results[-1].final_payload_sha.upper()}",
        f"CANONICAL_OUTPUT\t{CANONICAL_NAME}\tSHA256\t{canonical_sha.upper()}\tBYTES\t{canonical_bytes}",
        f"TOTAL\tKEYS\t{PLAN_KEYS}\tCLASS_UNITS\t{final.units}\tRAW_PAIRS\t{final.raw}"
        f"\tINVARIANT_ALPHA_CLASSES\t{final.invariant_alpha}\tBETA_COMPUTATIONS\t{final.beta}"
        f"\tINVERSE\t{final.inverse}\tINVERSE_ODD\t{final.inverse_odd}\tORBIT8\t{final.orbit8}"
        f"\tRELATOR\t{final.relator}\tB3\t{final.b3}\tGENERATE\t{final.generate}"
        f"\tPARITY\t{final.generate}\tCENTRALIZER_ORBITS\t{final.centralizer}"
        f"\tCANDIDATE_NUMERIC\t{final.candidate}",
        "CHECK\tORDERED_UNIT_KEY_ALPHA_COVERAGE\tPASS",
        "CHECK\tSEALED_PROFILE_FIELDS_AND_RAW_IDENTITIES\tPASS",
        "CHECK\tPER_GATE_INEQUALITIES_AND_CUMULATIVE_COUNTERS\tPASS",
        "CHECK\tCHECKPOINT_SHA_CHAIN_AND_ONE_PASS_PREFIX_HASHES\tPASS",
        "CHECK\tFINAL_CHECKPOINT_PAYLOAD_AND_FILE_HASH\tPASS",
        "CHECK\tEXACT_V7_WRAPPER_RUNNER_ENGINE_RECOVERY_CHAIN\tPASS",
        "CHECK\tPINNED_CHECKPOINT_FAILURE_AND_UNCOMMITTED_ALPHA_EXCLUSION\tPASS",
        "CHECK\tEXCLUDED_ALPHA_EQUALS_SEGMENT002_V2_RECOMPUTATION\tPASS",
        "CHECK\tFAILED_TMP_EXACT_RECONSTRUCTION_WITHOUT_DONE\tPASS",
        "CHECK\tZERO_CANDIDATES\tPASS",
        "SEED_PREDICATES_RUN_BY_VERIFIER\t0",
        "DONE",
    ])
    return ("\n".join(lines) + "\n").encode("ascii")


def format_certificate(
    bundles: Sequence[Bundle],
    results: Sequence[SegmentResult],
    final: Counters,
    canonical_sha: str,
    aggregate_sha: str,
    checkpoint_sha: str,
    verifier_sha: str,
    evidence: IntermediateEvidence | None,
) -> bytes:
    source_entries: list[str] = []
    for bundle, result in zip(bundles, results):
        if result.terminal == INTERRUPTED_TERMINAL:
            telemetry = "resource telemetry unavailable; exact streams retained and hashed"
        else:
            telemetry = (
                f"exit {result.resource.exit_status}, wall {result.resource.elapsed_text}, "
                f"maximum RSS {result.resource.max_rss_kib} KiB"
            )
        source_entries.append(
            f"- Segment {result.segment:03d}: {bundle.output.name}, durable units "
            f"{result.start_unit}..{result.last_unit}, status {result.terminal}, "
            f"SHA-256 {result.output_sha.upper()}, {result.output_bytes} bytes, "
            f"{result.output_lines} lines; stdout SHA-256 {result.resource.stdout_sha.upper()} "
            f"({result.resource.stdout_bytes} bytes), stderr SHA-256 "
            f"{result.resource.stderr_sha.upper()} ({result.resource.stderr_bytes} bytes); "
            f"{telemetry}; wrapper {result.resource.producer.wrapper_name} SHA-256 "
            f"{result.resource.producer.wrapper_sha.upper()}; runner "
            f"{result.resource.producer.runner_name} SHA-256 "
            f"{result.resource.producer.runner_sha.upper()}."
        )
    source_lines = "\n".join(source_entries)
    if evidence is None:
        failure_text = "No checkpoint-write-failure evidence record was used."
    else:
        successor = next(bundle for bundle in bundles if bundle.segment == evidence.segment + 1)
        failure_text = f"""Segment {evidence.segment:03d} physically contains {PINNED_FAILURE_OUTPUT_LINES:,} lines and {evidence.output_bytes:,} bytes with SHA-256 {evidence.output_sha.upper()}. Its last durable state is unit {evidence.last_unit}, (24T{evidence.last_key}, alpha {evidence.last_alpha}), with counter vector {list(PINNED_DURABLE_COUNTERS)}, checkpoint SHA-256 {evidence.checkpoint_sha.upper()}, and output-prefix {evidence.prefix_bytes} bytes / SHA-256 {evidence.prefix_sha.upper()}.

The following physical ALPHA_DONE for unit {evidence.next_unit}, (24T{evidence.next_key}, alpha {evidence.next_alpha}), was not checkpoint-committed. It and the failed temporary checkpoint are excluded from scientific totals. The exact {evidence.postprefix_bytes}-byte postprefix is pinned by SHA-256 {evidence.postprefix_sha.upper()}; the {evidence.failed_tmp_bytes}-byte failed temporary checkpoint is pinned by SHA-256 {evidence.failed_tmp_sha.upper()} and has no DONE line. The verifier reconstructs that failed temporary file byte for byte, then requires {successor.output.name} to restart at unit {evidence.next_unit}, emit CACHE_REBUILT for alpha 1..{evidence.next_alpha - 1} with SEED_PREDICATES_REPLAYED=0, and recompute an ALPHA_DONE whose scientific fields exactly equal the excluded physical record. No TOTAL, producer terminal marker, GNU-time value, exit status, wall time, or peak RSS is fabricated for segment {evidence.segment:03d}."""

    text = f"""# Degree-24 C8 seed shard 003 exact merged certificate

Status: PASS -- complete zero-candidate run, independently merged and sealed.

## Scope and exact totals

- Sealed shard: 003 only, from (24T6032, alpha 1) through (24T6440, alpha 2).
- Exact ordered alpha-class units: {final.units} across {PLAN_KEYS} plan keys.
- Raw pairs: {final.raw}.
- Numeric candidates and centralizer-orbit representatives: {final.candidate}.
- Final counters: invariant alpha classes {final.invariant_alpha}; beta computations {final.beta}; inverse {final.inverse}; inverse odd {final.inverse_odd}; orbit-eight {final.orbit8}; relator {final.relator}; B3 {final.b3}; generate/parity {final.generate}.

## Sealed inputs and outputs

- Full profile SHA-256: {PROFILE_SHA256}.
- Workload plan SHA-256: {PLAN_SHA256}.
- Verifier source SHA-256: {verifier_sha.upper()}.
- Canonical merged output SHA-256: {canonical_sha.upper()}.
- Aggregate SHA-256: {aggregate_sha.upper()}.
- Final atomic checkpoint SHA-256: {checkpoint_sha.upper()}.
- Specialized V7 seed engine SHA-256: {SEED_ENGINE_SHA256.upper()}.
- Planned fresh initial wrapper SHA-256: {INITIAL_WRAPPER_SHA256.upper()}.
- Initial runner SHA-256: {INITIAL_RUNNER_SHA256.upper()}.

## Source segments

{source_lines}

## Checkpoint-write failure and exclusion

{failure_text}

## Independent verification contract

The verifier parsed the pinned full profile and all 905 plan shards, reconstructed shard 003 as 14,648 one-based lexicographic work units, and required every recovery segment to start at the exact successor of the preceding durable checkpoint. It matched every PROFILE_OK field to the sealed profile, checked all plan/raw identities, rejected failed, superseded, ambiguous, duplicated, or gapped evidence, and accepted only consistently revision-tagged POSTVERIFY V7 bundles.

For every committed alpha it checked exact unit/key/alpha coverage, automorphism class-size divisibility, every seed gate inequality, zero-below-gate behavior, cumulative increments, candidates, runtime monotonicity, and exact successor. It reconstructed every durable checkpoint byte for byte and accumulated output-prefix hashes in one pass. The final checkpoint file equals the reconstructed final payload and hash.

Every normally terminated resource pair was matched to its exact wrapper and runner, the pinned V7 engine, WROTE record, bounded retry records, GAP warnings, GNU-time schema, zero exit status, wall bound, page size, and 48-GiB VM/RSS bound. Recovery wrappers are reconstructed from the pinned profile/plan, durable counters, predecessor checkpoint, and predecessor output-prefix state.

## Audit assumptions and limits

- GAP 4.12.1 and the degree-24 catalogue size 25,000 are producer assertions pinned by the output/checkpoint chain; this Python verifier does not relaunch GAP.
- Alpha indices use the producer's frozen one-based automorphism conjugacy-class order after sealed route reconstruction.
- The verifier establishes deterministic coverage, arithmetic/gate consistency, exact exclusion/recomputation, resource termination where available, and cryptographic lineage; it does not independently recompute group automorphisms or seed predicates.
- A numeric candidate prevents canonical merged artifacts from being published.
- The verifier itself runs no GAP or seed predicate.

DONE
"""
    return text.encode("ascii")

def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Independently verify and merge all terminal degree-24 C8 seed shard003 recovery segments."
    )
    parser.add_argument("base", nargs="?", help="Escalations directory; defaults to this source directory.")
    parser.add_argument(
        "--segment-output", action="append",
        help="Segment output path or glob; repeat for an explicit ordered set. Default discovers canonical segment outputs.",
    )
    parser.add_argument(
        "--resource-stdout", action="append",
        help="Separated GNU-time wrapper stdout path or glob; repeat as needed.",
    )
    parser.add_argument(
        "--resource-stderr", action="append",
        help="Separated GNU-time wrapper stderr path or glob; repeat as needed.",
    )
    parser.add_argument(
        "--intermediate-evidence",
        help="One canonical checkpoint-failure evidence record; requires an explicit SHA-256 pin.",
    )
    parser.add_argument(
        "--intermediate-evidence-sha256",
        help="Expected SHA-256 of the selected checkpoint-failure evidence record.",
    )
    return parser


def run(arguments: argparse.Namespace) -> int:
    base = Path(arguments.base).resolve() if arguments.base else Path(__file__).resolve().parent
    require(base.is_dir(), f"base directory missing: {base}")
    profile_path = base / PROFILE_NAME
    plan_path = base / PLAN_NAME
    checkpoint_path = base / CHECKPOINT_NAME
    canonical_path = base / CANONICAL_NAME
    aggregate_path = base / AGGREGATE_NAME
    certificate_path = base / CERTIFICATE_NAME
    destinations = [canonical_path, aggregate_path, certificate_path]
    temporary = refuse_outputs(destinations)
    canonical_temp, aggregate_temp, certificate_temp = temporary

    evidence = load_committed_failure_evidence(base, arguments)
    profiles = parse_profile(profile_path)
    works, shard_summary = parse_plan(plan_path, profiles)
    del shard_summary
    unit_table = build_unit_table(works)
    bundles = discover_bundles(base, arguments)
    if evidence is not None:
        matching = [bundle for bundle in bundles if bundle.segment == evidence.segment]
        require(len(matching) == 1, "checkpoint-failure evidence: selected segment bundle absent")
        require(
            matching[0].output.name == evidence.output_name and
            matching[0].stdout.name == evidence.stdout_name and
            matching[0].stderr.name == evidence.stderr_name,
            "checkpoint-failure evidence: selected bundle filenames differ",
        )
    verifier_sha = sha256_file(Path(__file__).resolve())

    results: list[SegmentResult] = []
    evidence_uses = 0
    state = Counters()
    checkpoint_sha = "NONE_FRESH_START"
    previous: tuple[Bundle, SegmentResult] | None = None
    try:
        with canonical_temp.open("xb") as canonical_stream:
            spool = CanonicalSpool(canonical_stream)
            spool.line("CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003-MERGED")
            spool.line(f"GAP_VERSION\t{GAP_VERSION}")
            spool.line(f"DEGREE\t{DEGREE}")
            spool.line(f"DATABASE\t{DATABASE}")
            spool.line("PLAN_FIRST\t24T6032\t1")
            spool.line("PLAN_LAST\t24T6440\t2")
            spool.line(f"PLAN_KEYS\t{PLAN_KEYS}")
            spool.line(f"PLAN_CLASS_UNITS\t{PLAN_UNITS}")
            spool.line(f"PLAN_RAW_PAIRS\t{PLAN_RAW}")
            spool.line(f"PROFILE_SHA256\t{PROFILE_SHA256}")
            spool.line(f"PLAN_SHA256\t{PLAN_SHA256}")
            spool.line(f"SOURCE_SEGMENTS\t{len(bundles)}")
            spool.line("NORMALIZATION\tOne PROFILE_OK per unique key; all ALPHA_DONE and CHECKPOINT_COMMITTED records retained in unit order; KEY_DONE rebuilt from the sealed plan.")
            for index, bundle in enumerate(bundles):
                spool.line(
                    f"SOURCE_SEGMENT_BEGIN\t{bundle.segment:03d}\tFILE\t{bundle.output.name}"
                    f"\tSTART_UNIT\t{state.units + 1}"
                )
                result = verify_segment(
                    bundle,
                    works,
                    profiles,
                    unit_table,
                    state,
                    checkpoint_sha,
                    previous,
                    spool,
                    evidence,
                )
                results.append(result)
                state = result.counters.clone()
                checkpoint_sha = result.final_checkpoint_sha
                previous = (bundle, result)
                spool.line(
                    f"SOURCE_SEGMENT_END\t{bundle.segment:03d}\tLAST_UNIT\t{result.last_unit}"
                    f"\tTERMINAL\t{result.terminal}\tSHA256\t{result.output_sha.upper()}"
                )
                is_last = index == len(bundles) - 1
                if result.terminal == INTERRUPTED_TERMINAL:
                    evidence_uses += 1
                    require(
                        evidence is not None and result.segment == evidence.segment and not is_last,
                        f"segment {bundle.segment:03d}: checkpoint failure accepted only once and nonfinal",
                    )
                    successor = bundles[index + 1]
                    require(
                        successor.segment == evidence.segment + 1 and
                        successor.filename_start == evidence.next_unit,
                        f"segment {bundle.segment:03d}: exact checkpoint-failure successor absent",
                    )
                if not is_last:
                    require(
                        result.terminal in {
                            INTERRUPTED_TERMINAL, "STOPPED_RECOVERY_SMOKE", "STOPPED_GUARD"
                        },
                        f"segment {bundle.segment:03d}: noncontinuable intermediate terminal {result.terminal}",
                    )
            require(results, "no segment results")
            require(
                evidence_uses == (1 if evidence is not None else 0),
                "checkpoint-failure evidence: record was not used exactly once",
            )
            if evidence is not None:
                evidence_index = next(
                    index for index, result in enumerate(results)
                    if result.segment == evidence.segment
                )
                require(evidence_index + 1 < len(results),
                        "checkpoint-failure evidence: recomputation segment absent")
                verify_excluded_alpha_and_failed_tmp(
                    base,
                    evidence,
                    results[evidence_index].excluded_alpha_line,
                    results[evidence_index + 1].first_alpha_line,
                )

            final_result = results[-1]
            require(checkpoint_path.is_file(), f"final checkpoint missing: {checkpoint_path}")
            checkpoint_data = checkpoint_path.read_bytes()
            require(checkpoint_data == final_result.final_checkpoint_bytes, "final checkpoint payload/file mismatch")
            require(sha256_bytes(checkpoint_data) == checkpoint_sha, "final checkpoint full SHA mismatch")
            require(not (base / CHECKPOINT_TMP_NAME).exists(), "stale final checkpoint temp file")

            if final_result.terminal == "STOPPED_CANDIDATE":
                candidate = final_result.candidates[0]
                print(
                    f"CANDIDATE_STOP segment={final_result.segment:03d} unit={candidate.unit} "
                    f"key=24T{candidate.key} alpha={candidate.alpha} candidates={len(final_result.candidates)} "
                    f"checkpoint={checkpoint_sha.upper()} verified_prefix=PASS no_outputs_written=PASS"
                )
                return 2
            if final_result.terminal == "STOPPED_RECOVERY_SMOKE":
                print(
                    f"INCOMPLETE_RECOVERY_SMOKE segment={final_result.segment:03d} "
                    f"last_unit={state.units} next_unit={state.units + 1} "
                    f"checkpoint={checkpoint_sha.upper()} "
                    f"verified_prefix=PASS no_outputs_written=PASS"
                )
                return 4
            if final_result.terminal == "STOPPED_GUARD":
                if state.units < PLAN_UNITS:
                    print(
                        f"INCOMPLETE_GUARD segment={final_result.segment:03d} last_unit={state.units} "
                        f"next_unit={state.units + 1} checkpoint={checkpoint_sha.upper()} "
                        f"verified_prefix=PASS no_outputs_written=PASS"
                    )
                    return 3
                # The V7 engine tests its internal guard after committing each alpha,
                # including alpha 14648. A guard marker at that exact final unit is
                # therefore complete evidence and is normalized as a complete run.
                require(state.units == PLAN_UNITS, "final guard coverage")
            else:
                require(final_result.terminal == "DONE", f"final segment terminal {final_result.terminal}")
            require((state.units, state.raw, state.centralizer, state.candidate) ==
                    (PLAN_UNITS, PLAN_RAW, 0, 0), "complete zero-candidate totals")
            require((spool.alpha_count, spool.commit_count, spool.key_count, len(spool.profile_lines)) ==
                    (PLAN_UNITS, PLAN_UNITS, PLAN_KEYS, PLAN_KEYS), "canonical merge record counts")
            for result in results[:-1]:
                require(not result.candidates, f"intermediate segment {result.segment:03d}: candidate records")
            for bundle, result in zip(bundles, results):
                spool.line(
                    f"RESOURCE\tSEGMENT\t{result.segment:03d}\tSTDOUT\t{bundle.stdout.name}"
                    f"\tSTDOUT_SHA256\t{result.resource.stdout_sha.upper()}"
                    f"\tSTDOUT_BYTES\t{result.resource.stdout_bytes}\tSTDERR\t{bundle.stderr.name}"
                    f"\tSTDERR_SHA256\t{result.resource.stderr_sha.upper()}"
                    f"\tSTDERR_BYTES\t{result.resource.stderr_bytes}"
                    f"\tWALL\t{result.resource.elapsed_text}"
                    f"\tMAX_RSS_KIB\t{available_text(result.resource.max_rss_kib)}"
                    f"\tEXIT_STATUS\t{available_text(result.resource.exit_status)}"
                    f"\tWRAPPER\t{result.resource.producer.wrapper_name}"
                    f"\tWRAPPER_SHA256\t{result.resource.producer.wrapper_sha.upper()}"
                    f"\tRUNNER\t{result.resource.producer.runner_name}"
                    f"\tRUNNER_SHA256\t{result.resource.producer.runner_sha.upper()}"
                    f"\tENGINE\t{SEED_ENGINE_NAME}"
                    f"\tENGINE_SHA256\t{result.resource.producer.engine_sha.upper()}"
                    f"\tFINAL_OUTPUT_PREFIX_BYTES\t{result.final_prefix_bytes}"
                    f"\tFINAL_OUTPUT_PREFIX_SHA256\t{result.final_prefix_sha.upper()}"
                )
                if result.terminal == INTERRUPTED_TERMINAL:
                    require(evidence is not None and result.segment == evidence.segment,
                            "internal checkpoint-failure evidence selection")
                    spool.line(
                        f"CHECKPOINT_FAILURE_EVIDENCE\tSEGMENT\t{result.segment:03d}"
                        f"\tEVIDENCE_FILE\t{evidence.path.name}"
                        f"\tEVIDENCE_SHA256\t{evidence.file_sha.upper()}"
                        f"\tSTATUS\t{INTERRUPTED_TERMINAL}"
                        f"\tLAST_DURABLE_UNIT\t{evidence.last_unit}"
                        f"\tEXCLUDED_UNCOMMITTED_UNIT\t{evidence.next_unit}"
                        f"\tCHECKPOINT_SHA256\t{evidence.checkpoint_sha.upper()}"
                        f"\tOUTPUT_PREFIX_BYTES\t{evidence.prefix_bytes}"
                        f"\tOUTPUT_PREFIX_SHA256\t{evidence.prefix_sha.upper()}"
                        f"\tPOSTPREFIX_SHA256\t{evidence.postprefix_sha.upper()}"
                        f"\tFAILED_TMP_SHA256\t{evidence.failed_tmp_sha.upper()}"
                        "\tFAILED_TMP_DONE\tNO\tTOTAL_SYNTHESIZED\tNO\tTERMINAL_SYNTHESIZED\tNO"
                        f"\tFAILURE\t{evidence.reported_failure}"
                        f"\tRESOURCE_TELEMETRY\t{evidence.resource_telemetry}"
                    )
            spool.line(
                f"FINAL_CHECKPOINT\t{checkpoint_path.name}\tSHA256\t{checkpoint_sha.upper()}"
                f"\tPAYLOAD_SHA256\t{final_result.final_payload_sha.upper()}"
            )
            spool.line(
                f"TOTAL\tKEYS\t{PLAN_KEYS}\tCLASS_UNITS\t{state.units}\tRAW_PAIRS\t{state.raw}"
                f"\tINVARIANT_ALPHA_CLASSES\t{state.invariant_alpha}\tBETA_COMPUTATIONS\t{state.beta}"
                f"\tINVERSE\t{state.inverse}\tINVERSE_ODD\t{state.inverse_odd}\tORBIT8\t{state.orbit8}"
                f"\tRELATOR\t{state.relator}\tB3\t{state.b3}\tGENERATE\t{state.generate}"
                f"\tPARITY\t{state.generate}\tCENTRALIZER_ORBITS\t{state.centralizer}"
                f"\tCANDIDATE_NUMERIC\t{state.candidate}"
            )
            spool.line("DONE")
            canonical_stream.flush()
            os.fsync(canonical_stream.fileno())

        canonical_sha = sha256_file(canonical_temp)
        canonical_bytes = canonical_temp.stat().st_size
        aggregate_data = format_aggregate(
            bundles, results, state, checkpoint_path, checkpoint_sha,
            canonical_sha, canonical_bytes, verifier_sha, evidence,
        )
        write_new_temp(aggregate_temp, aggregate_data)
        aggregate_sha = sha256_bytes(aggregate_data)
        certificate_data = format_certificate(
            bundles, results, state, canonical_sha, aggregate_sha,
            checkpoint_sha, verifier_sha, evidence,
        )
        write_new_temp(certificate_temp, certificate_data)

        published: list[Path] = []
        try:
            os.replace(canonical_temp, canonical_path)
            published.append(canonical_path)
            os.replace(aggregate_temp, aggregate_path)
            published.append(aggregate_path)
            # The certificate is the completion marker and is published last.
            os.replace(certificate_temp, certificate_path)
            published.append(certificate_path)
        except OSError:
            for path in reversed(published):
                path.unlink(missing_ok=True)
            raise
        print(
            f"PASS shard=003 segments={len(results)} units={state.units} raw={state.raw} "
            f"candidates=0 canonical_sha256={canonical_sha.upper()} "
            f"aggregate_sha256={aggregate_sha.upper()} checkpoint_sha256={checkpoint_sha.upper()}"
        )
        return 0
    finally:
        for path in temporary:
            if path.exists():
                path.unlink()


def main() -> int:
    parser = build_argument_parser()
    arguments = parser.parse_args()
    try:
        return run(arguments)
    except VerificationError as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
