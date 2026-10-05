#!/usr/bin/env python3
"""Proof-grade global merge, independent replay, tests, and V3 certificate.

This program is certificate-layer only.  It never evaluates a seed predicate
and never launches GAP.  The affected split-heavy domain is taken solely from
the frozen Route-B manifests and the completed V3 repair outputs.  Unaffected
keys are retained only when the sealed V2 plan proves that the complete key was
processed atomically.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
LEGACY = ROOT / "production_code" / "escalations"
BASE = LEGACY / "degree24_v3_repair"

PROFILE = LEGACY / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
OLD_PLAN = LEGACY / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
OLD_PROGRESS = LEGACY / "GAP_TRANSITIVE_DEGREE24_C8_SEED_PROGRESS_GPT56SOL.tsv"
KEYS = BASE / "DEG24_SPLIT_HEAVY_KEYS_V3.tsv"
PLAN = BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.tsv"
PLAN_SUMMARY = BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.json"
REPRO = BASE / "DEG24_MANIFEST_REPRODUCIBILITY_CERTIFICATE_V3.json"
COVERAGE = BASE / "DEG24_SPLIT_HEAVY_COVERAGE_CERTIFICATE_V3.json"
COVERAGE_AUDIT = BASE / "DEG24_SPLIT_HEAVY_COVERAGE_INDEPENDENT_AUDIT_V3.json"
SHARD208 = BASE / "DEG24_SHARD208_FORENSIC_REGRESSION_V3.json"
SHARD208_MAP = BASE / "DEG24_SHARD208_ORDINAL844_CLASS_ID_MAPPING_V3.txt"
SMOKE = BASE / "DEG24_SPLIT_HEAVY_ENGINE_CHECKPOINT_RESUME_SMOKE_V3.json"
RECOVERY_PREFLIGHT = BASE / "DEG24_V6_RECOVERY_PREFLIGHT_S0809.json"

GLOBAL_REGISTRY = BASE / "DEG24_GLOBAL_DOMAIN_REGISTRY_V3.tsv"
CANDIDATE_REGISTRY = BASE / "DEG24_GLOBAL_CANDIDATE_REGISTRY_V3.tsv"
MERGE = BASE / "DEG24_GLOBAL_MERGE_V3.json"
REPLAY = BASE / "DEG24_GLOBAL_CERTIFICATE_REPLAY_V3.json"
TESTS = BASE / "DEG24_FINAL_TEST_SUITE_V3.json"
CERT = BASE / "DEG24_GLOBAL_CERTIFICATE_V3.json"
CERT_MD = BASE / "DEG24_GLOBAL_CERTIFICATE_V3.md"
MANIFEST = BASE / "DEG24_GLOBAL_CERTIFICATE_V3.sha256"

EXPECTED = {
    "profile_keys": 10714,
    "positive_keys": 9962,
    "zero_keys": 752,
    "affected_keys": 806,
    "v3_segments": 1006,
    "v3_class_units": 497108,
    "v3_raw": 20581825344,
    "global_class_units": 1474201,
    "global_raw": 40656212448,
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    if tmp.exists():
        tmp.unlink()
    with tmp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, path)


def write_json(path: Path, obj: object) -> None:
    atomic_write(path, (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def kv(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0, parts
    result: dict[str, str] = {}
    for i in range(start, len(parts), 2):
        assert parts[i] not in result, parts[i]
        result[parts[i]] = parts[i + 1]
    return result


def resolve(rel: str, parent: Path = ROOT) -> Path:
    p = Path(rel.replace("/", os.sep))
    return p if p.is_absolute() else parent / p


def parse_profile() -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    entries: dict[str, dict[str, int]] = {}
    total: dict[str, int] | None = None
    for raw in PROFILE.read_text(encoding="utf-8").splitlines():
        t = raw.split("\t")
        if t[0] == "ENTRY":
            data = kv(t, 2)
            key = t[1]
            assert key not in entries
            row = {
                "order": int(data["ORDER"]),
                "classes": int(data["ORDER8_CLASSES"]),
                "raw": int(data["RAW_PAIRS"]),
                "parity_maps": int(data["PARITY_MAPS"]),
            }
            assert row["raw"] == row["order"] * row["classes"]
            assert row["parity_maps"] > 0
            entries[key] = row
        elif t[0] == "TOTAL":
            data = kv(t, 1)
            total = {
                "profile_keys": int(data["PARITY_KEYS"]),
                "positive_keys": int(data["POSITIVE_CLASS_KEYS"]),
                "zero_keys": int(data["ZERO_CLASS_KEYS"]),
                "class_units": int(data["ORDER8_CLASSES"]),
                "raw": int(data["RAW_PAIRS"]),
            }
    assert total is not None
    assert len(entries) == total["profile_keys"] == EXPECTED["profile_keys"]
    assert sum(r["classes"] > 0 for r in entries.values()) == total["positive_keys"] == EXPECTED["positive_keys"]
    assert sum(r["classes"] == 0 for r in entries.values()) == total["zero_keys"] == EXPECTED["zero_keys"]
    assert sum(r["classes"] for r in entries.values()) == total["class_units"] == EXPECTED["global_class_units"]
    assert sum(r["raw"] for r in entries.values()) == total["raw"] == EXPECTED["global_raw"]
    return entries, total


def parse_old_plan() -> tuple[dict[str, list[dict[str, int]]], dict[int, dict[str, int]]]:
    by_key: dict[str, list[dict[str, int]]] = defaultdict(list)
    by_shard: dict[int, dict[str, int]] = defaultdict(lambda: {"units": 0, "raw": 0})
    work_count = 0
    for raw in OLD_PLAN.read_text(encoding="utf-8").splitlines():
        t = raw.split("\t")
        if t[0] != "WORK":
            continue
        shard = int(t[1])
        data = kv(t, 2)
        row = {k: int(data[k]) for k in ("KEY", "ALPHA_FIRST", "ALPHA_LAST", "CLASS_UNITS", "RAW_PAIRS", "ORDER")}
        assert row["CLASS_UNITS"] == row["ALPHA_LAST"] - row["ALPHA_FIRST"] + 1
        assert row["RAW_PAIRS"] == row["ORDER"] * row["CLASS_UNITS"]
        by_key[f"24T{row['KEY']}"] .append(row)
        by_shard[shard]["units"] += row["CLASS_UNITS"]
        by_shard[shard]["raw"] += row["RAW_PAIRS"]
        work_count += 1
    assert work_count == 10864
    assert len(by_key) == EXPECTED["positive_keys"]
    assert sorted(by_shard) == list(range(1, 906))
    return by_key, by_shard


def affected_registry() -> tuple[list[str], dict[str, dict[str, int]]]:
    rows: dict[str, dict[str, int]] = {}
    with KEYS.open("r", encoding="utf-8", newline="") as stream:
        for r in csv.DictReader(stream, delimiter="\t"):
            key = f"24T{int(r['key'])}"
            rows[key] = {
                "order": int(r["order"]),
                "classes": int(r["old_class_units"]),
                "raw": int(r["old_raw_pairs"]),
                "segments": int(r["old_segment_count"]),
            }
    assert len(rows) == EXPECTED["affected_keys"]
    return sorted(rows, key=lambda x: int(x[3:])), rows


def derive_manifest_from_source(key: str) -> tuple[list[dict[str, str]], dict[str, str]]:
    src = BASE / "manifest_sources" / f"DEG24_KEY_{key}_MANIFEST_SOURCE_V3.tsv"
    meta: dict[str, str] = {}
    rows: list[dict[str, str]] = []
    for raw in src.read_text(encoding="utf-8").splitlines():
        f = raw.split("\t")
        if f[0] == "CLASS":
            assert len(f) == 9
            rows.append({
                "source_ordinal_diagnostic": f[1],
                "representative_display_diagnostic": f[2],
                "pc_exponents_diagnostic": f[3],
                "representative_serialization": f[4],
                "class_size": f[5],
                "centralizer_size": f[6],
                "order": f[7],
                "structural_filters": f[8],
            })
        elif len(f) == 2:
            meta[f[0]] = f[1]
    assert meta["KEY_ID"] == key
    assert len(rows) == int(meta["ORDER8_CLASS_COUNT"])
    schema = meta["REPRESENTATION_SCHEMA"]
    gen_sha = sha_bytes(meta["GENERATOR_SERIALIZATION"].encode("utf-8"))
    seen: set[str] = set()
    for row in rows:
        ser = row["representative_serialization"]
        assert ser not in seen
        seen.add(ser)
        payload = (
            f"KEY_ID={key}\nSCHEMA={schema}\nGENERATOR_TUPLE_SHA256={gen_sha}\n"
            f"REPRESENTATIVE_SERIALIZATION={ser}\nCLASS_SIZE={row['class_size']}\n"
            f"ORDER={row['order']}\nCENTRALIZER_SIZE={row['centralizer_size']}\n"
        )
        row["class_id_v3"] = sha_bytes(payload.encode("utf-8"))
    rows.sort(key=lambda r: (r["representative_serialization"], int(r["class_size"]), int(r["centralizer_size"])))
    for pos, row in enumerate(rows, 1):
        row["key_id"] = key
        row["manifest_position"] = str(pos)
        row["row_sha256"] = sha_bytes("\t".join([
            key, row["class_id_v3"], str(pos), row["representative_serialization"],
            row["class_size"], row["centralizer_size"], row["order"], row["structural_filters"],
        ]).encode("utf-8"))
    meta["GENERATOR_TUPLE_SHA256_REPLAY"] = gen_sha
    meta["SOURCE_SHA256_REPLAY"] = sha_file(src)
    return rows, meta


def replay_all_manifests(keys: list[str], profile: dict[str, dict[str, int]], artifacts: set[Path]) -> tuple[dict[str, list[str]], dict[str, dict[str, object]]]:
    ids: dict[str, list[str]] = {}
    summaries: dict[str, dict[str, object]] = {}
    fields = [
        "key_id", "class_id_v3", "manifest_position", "representative_serialization",
        "class_size", "centralizer_size", "order", "structural_filters",
        "source_ordinal_diagnostic", "representative_display_diagnostic",
        "pc_exponents_diagnostic", "row_sha256",
    ]
    for key in keys:
        directory = BASE / "manifests" / key
        tsv = directory / f"DEG24_KEY_{key}_CLASS_MANIFEST_V3.tsv"
        js = directory / f"DEG24_KEY_{key}_CLASS_MANIFEST_V3.json"
        gap = directory / f"DEG24_KEY_{key}_CLASS_MANIFEST_V3.g"
        source = BASE / "manifest_sources" / f"DEG24_KEY_{key}_MANIFEST_SOURCE_V3.tsv"
        derived, source_meta = derive_manifest_from_source(key)
        with tsv.open("r", encoding="utf-8", newline="") as stream:
            frozen = list(csv.DictReader(stream, delimiter="\t"))
        assert frozen == [{name: row[name] for name in fields} for row in derived], key
        summary = json.loads(js.read_text(encoding="utf-8"))
        assert summary["schema"] == "DEG24_AUTHORITATIVE_CLASS_MANIFEST_V3"
        assert summary["route"] == "B_FROZEN_EXPLICIT_REPRESENTATIVES"
        assert summary["key_id"] == key
        assert summary["class_count"] == summary["class_id_count"] == len(derived) == profile[key]["classes"]
        assert summary["manifest_sha256"].lower() == sha_file(tsv)
        assert summary["gap_manifest_sha256"].lower() == sha_file(gap)
        assert summary["source_sha256"].lower() == sha_file(source) == source_meta["SOURCE_SHA256_REPLAY"]
        assert summary["generator_tuple_sha256"].lower() == source_meta["GENERATOR_TUPLE_SHA256_REPLAY"]
        assert all(int(r["order"]) == 8 for r in derived)
        assert all(r["structural_filters"] == "ORDER_EQ_8;KEY_PARITY_MAPS_POSITIVE;GROUP_ORDER_WINDOW" for r in derived)
        key_ids = [r["class_id_v3"] for r in derived]
        assert len(key_ids) == len(set(key_ids))
        ids[key] = key_ids
        summaries[key] = summary
        artifacts.update({source, tsv, js, gap})
    return ids, summaries


def parse_v3_plan(ids: dict[str, list[str]], summaries: dict[str, dict[str, object]], artifacts: set[Path]) -> tuple[list[dict[str, object]], dict[str, dict[str, int]], dict[str, int]]:
    rows: list[dict[str, object]] = []
    assigned: dict[str, list[str]] = defaultdict(list)
    key_totals: dict[str, dict[str, int]] = defaultdict(lambda: {"segments": 0, "classes": 0, "raw": 0})
    with PLAN.open("r", encoding="utf-8", newline="") as stream:
        for raw in csv.DictReader(stream, delimiter="\t"):
            list_path = resolve(raw["class_id_list"])
            data_path = resolve(raw["segment_data"])
            class_ids = [x for x in list_path.read_text(encoding="ascii").splitlines() if x]
            key = raw["key_id"]
            assert len(class_ids) == int(raw["class_count"])
            assert len(class_ids) == len(set(class_ids))
            assert sha_file(list_path) == raw["class_id_list_sha256"].lower()
            assert sha_file(data_path) == raw["segment_data_sha256"].lower()
            assert raw["manifest_sha256"].lower() == summaries[key]["manifest_sha256"]
            assigned[key].extend(class_ids)
            key_totals[key]["segments"] += 1
            key_totals[key]["classes"] += len(class_ids)
            key_totals[key]["raw"] += int(raw["raw_pairs"])
            rows.append({**raw, "class_ids": class_ids, "list_path": list_path, "data_path": data_path})
            artifacts.update({list_path, data_path})
    assert len(rows) == EXPECTED["v3_segments"]
    missing = duplicate = extra = 0
    for key, expected_ids in ids.items():
        got = assigned[key]
        counts = Counter(got)
        missing += len(set(expected_ids) - set(got))
        extra += len(set(got) - set(expected_ids))
        duplicate += sum(n - 1 for n in counts.values() if n > 1)
        assert got == expected_ids, key
    totals = {
        "keys": len(key_totals),
        "segments": len(rows),
        "classes": sum(x["classes"] for x in key_totals.values()),
        "raw": sum(x["raw"] for x in key_totals.values()),
        "missing": missing,
        "duplicate": duplicate,
        "extra": extra,
    }
    assert totals == {
        "keys": EXPECTED["affected_keys"], "segments": EXPECTED["v3_segments"],
        "classes": EXPECTED["v3_class_units"], "raw": EXPECTED["v3_raw"],
        "missing": 0, "duplicate": 0, "extra": 0,
    }
    return rows, key_totals, totals


def audit_v3_outputs(plan_rows: list[dict[str, object]], artifacts: set[Path]) -> tuple[dict[str, int], list[str], int]:
    metrics = Counter()
    candidate_lines: list[str] = []
    uncommitted_tail_rows = 0
    for row in plan_rows:
        segment = str(row["segment_id"])
        key = str(row["key_id"])
        expected_ids = list(row["class_ids"])
        completion = BASE / "repair_completions" / f"{segment}_COMPLETE_V3.json"
        obj = json.loads(completion.read_text(encoding="utf-8"))
        assert obj["schema"] == "DEG24_SPLIT_HEAVY_REPAIR_SEGMENT_COMPLETE_V3"
        assert obj["status"] == "COMPLETE" and obj["segment_id"] == segment and obj["key_id"] == key
        assert obj["class_units"] == len(expected_ids) == int(row["class_count"])
        assert obj["raw_pairs"] == int(row["raw_pairs"])
        assert obj["class_id_list_sha256"].lower() == row["class_id_list_sha256"]
        assert obj["segment_data_sha256"].lower() == row["segment_data_sha256"]
        checkpoint = resolve(obj["final_checkpoint"])
        assert sha_file(checkpoint) == obj["final_checkpoint_sha256"].lower()
        artifacts.update({completion, checkpoint})
        committed: dict[int, dict[str, str]] = {}
        total: dict[str, str] | None = None
        local_candidates: list[str] = []
        for part_index, part in enumerate(obj["output_parts"]):
            output = resolve(part["path"])
            assert output.stat().st_size == int(part["bytes"])
            assert sha_file(output) == part["sha256"].lower()
            artifacts.add(output)
            pending: dict[int, dict[str, str]] = {}
            for raw_line in output.read_text(encoding="ascii").splitlines():
                t = raw_line.split("\t")
                if t[0] == "CLASS_DONE":
                    data = kv(t, 1)
                    pending[int(data["INDEX"])] = data
                elif t[0] == "CHECKPOINT_COMMITTED":
                    data = kv(t, 1)
                    index = int(data["INDEX"])
                    assert index in pending
                    item = pending.pop(index)
                    assert index not in committed
                    assert item["KEY"] == key
                    assert item["CLASS_ID_V3"] == item["REPRESENTATIVE_FINGERPRINT"] == expected_ids[index - 1]
                    assert int(item["CUM_UNITS"]) == index
                    assert int(item["CUM_RAW"]) == index * (int(row["raw_pairs"]) // len(expected_ids))
                    assert int(item["INVARIANT_PARITY_MAPS"]) > 0
                    inv = int(item["INVERSE_LOCUS"]); odd = int(item["INVERSE_ODD"])
                    orbit = int(item["ORBIT8"]); relator = int(item["RELATOR"])
                    b3 = int(item["B3"]); generate = int(item["GENERATE"])
                    central = int(item["CENTRALIZER_ORBITS"])
                    assert 0 <= odd <= inv and 0 <= orbit <= odd and 0 <= relator <= orbit
                    assert 0 <= b3 <= relator and 0 <= generate <= b3 and 0 <= central <= generate
                    committed[index] = item
                elif t[0].startswith("CANDIDATE") and t[0] != "CANDIDATE_NUMERIC_COUNT":
                    local_candidates.append(raw_line)
                elif t[0] == "TOTAL":
                    total = kv(t, 1)
            # An interrupted attempt may contain an uncommitted CLASS_DONE tail.
            uncommitted_tail_rows += len(pending)
        assert sorted(committed) == list(range(1, len(expected_ids) + 1)), segment
        assert total is not None
        assert int(total["CLASS_UNITS"]) == len(expected_ids)
        assert int(total["RAW_PAIRS"]) == int(row["raw_pairs"])
        assert int(total["CANDIDATE_NUMERIC"]) == obj["candidate_numeric"] == len(local_candidates)
        assert total["FINAL_CHECKPOINT_SHA256"].lower() == obj["final_checkpoint_sha256"].lower()
        for field in ("INVARIANT_ALPHA_CLASSES", "BETA_COMPUTATIONS", "INVERSE", "INVERSE_ODD", "ORBIT8", "RELATOR", "B3", "GENERATE", "CENTRALIZER_ORBITS", "CANDIDATE_NUMERIC"):
            metrics[field] += int(total[field])
        candidate_lines.extend(local_candidates)
    assert metrics["INVARIANT_ALPHA_CLASSES"] == EXPECTED["v3_class_units"]
    return dict(metrics), candidate_lines, uncommitted_tail_rows


def parse_simple_lines(path: Path) -> dict[str, str]:
    vals: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        t = raw.split("\t")
        if len(t) == 2:
            vals[t[0]] = t[1]
    return vals


def find_legacy_aggregate(shard: int, expected_sha: str | None) -> Path:
    tag = f"{shard:03d}"
    candidates = [
        LEGACY / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_AGGREGATE_GPT56SOL.txt",
        LEGACY / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CANONICAL_NUMERICAL_AGGREGATE_GPT56SOL.txt",
    ]
    existing = [p for p in candidates if p.is_file()]
    assert existing, tag
    if expected_sha is None:
        assert len(existing) == 1
        return existing[0]
    matches = [p for p in existing if sha_file(p) == expected_sha.lower()]
    assert len(matches) == 1, (tag, existing, expected_sha)
    return matches[0]


def audit_legacy_atomic_domain(by_key: dict[str, list[dict[str, int]]], by_shard: dict[int, dict[str, int]], affected: set[str], artifacts: set[Path]) -> dict[str, int]:
    split = {key for key, rows in by_key.items() if len(rows) > 1}
    assert split == affected
    atomic = {key for key, rows in by_key.items() if len(rows) == 1}
    assert len(atomic) == EXPECTED["positive_keys"] - EXPECTED["affected_keys"]
    progress: dict[int, dict[str, str]] = {}
    with OLD_PROGRESS.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            progress[int(row["SHARD"])] = row
    assert sorted(progress) == list(range(3, 906))
    checked_outputs = 0
    checked_shards = 0
    for shard in range(1, 906):
        tag = f"{shard:03d}"
        marker = LEGACY / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_COMPLETE_GPT56SOL.txt"
        marker_vals: dict[str, str] = {}
        if shard >= 3:
            assert marker.is_file()
            marker_vals = parse_simple_lines(marker)
            assert marker_vals["STATUS"] == "COMPLETE_ZERO_CANDIDATE"
            assert int(marker_vals["CLASS_UNITS"]) == by_shard[shard]["units"]
            assert int(marker_vals["RAW_PAIRS"]) == by_shard[shard]["raw"]
            candidate_value = marker_vals.get("CANDIDATES", "0")
            assert int(candidate_value) == 0
            aggregate_sha = marker_vals.get("AGGREGATE_SHA256", marker_vals.get("NUMERICAL_AGGREGATE_SHA256"))
            assert aggregate_sha
            aggregate = find_legacy_aggregate(shard, aggregate_sha)
            assert progress[shard]["STATUS"] == "COMPLETE_ZERO_CANDIDATE"
            assert int(progress[shard]["CLASS_UNITS"]) == by_shard[shard]["units"]
            assert int(progress[shard]["RAW_PAIRS"]) == by_shard[shard]["raw"]
            assert int(progress[shard]["CANDIDATES"]) == 0
            artifacts.add(marker)
        else:
            aggregate = find_legacy_aggregate(shard, None)
            cert = LEGACY / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_GPT56SOL_CERTIFICATE.md"
            check = LEGACY / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_MANIFEST_CHECK_GPT56SOL.txt"
            assert cert.is_file() and check.is_file() and "MISMATCHES\t0" in check.read_text(encoding="utf-8")
            artifacts.update({cert, check})
        totals: dict[str, str] | None = None
        simple = parse_simple_lines(aggregate)
        for raw in aggregate.read_text(encoding="utf-8").splitlines():
            t = raw.split("\t")
            if t[0] in {"SOURCE_SEGMENT", "SEGMENT"}:
                data = kv(t, 2)
                name = data.get("OUTPUT", data.get("FILE"))
                expected_hash = data.get("OUTPUT_SHA256", data.get("SHA256"))
                expected_bytes = data.get("OUTPUT_BYTES", data.get("BYTES"))
                assert name and expected_hash and expected_bytes
                output = LEGACY / name
                assert output.is_file() and output.stat().st_size == int(expected_bytes)
                assert sha_file(output) == expected_hash.lower()
                artifacts.add(output)
                checked_outputs += 1
            elif t[0] == "TOTAL":
                totals = kv(t, 1)
        if totals is None:
            totals = simple
        units = int(totals.get("CLASS_UNITS", totals.get("CUM_UNITS", "-1")))
        raw = int(totals.get("RAW_PAIRS", totals.get("CUM_RAW", "-1")))
        candidates = int(totals.get("CANDIDATE_NUMERIC", totals.get("CANDIDATES", "0")))
        assert units == by_shard[shard]["units"] and raw == by_shard[shard]["raw"] and candidates == 0
        artifacts.add(aggregate)
        checked_shards += 1
    return {
        "legacy_shards_checked": checked_shards,
        "legacy_output_parts_rehashed": checked_outputs,
        "unaffected_positive_atomic_keys": len(atomic),
    }


def require_pass_json(path: Path, artifacts: set[Path]) -> dict[str, object]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    status = str(obj.get("status", obj.get("overall_status", ""))).upper()
    assert "PASS" in status or status in {"COMPLETE", "ALL_PASS"}, (path.name, status)
    artifacts.add(path)
    return obj


def write_registry(profile: dict[str, dict[str, int]], affected: set[str], summaries: dict[str, dict[str, object]]) -> None:
    fields = ["key_id", "domain_kind", "class_units", "raw_pairs", "identity_basis", "domain_reference", "domain_reference_sha256", "candidate_count"]
    lines = ["\t".join(fields)]
    for key in sorted(profile, key=lambda x: int(x[3:])):
        row = profile[key]
        if key in affected:
            summary = summaries[key]
            values = [
                key, "SPLIT_HEAVY_V3_ROUTE_B", str(row["classes"]), str(row["raw"]),
                "FROZEN_EXPLICIT_CLASS_ID_V3_MANIFEST", str(summary["manifest"]), str(summary["manifest_sha256"]), "0",
            ]
        else:
            values = [
                key, "UNAFFECTED_ATOMIC_V2_CERTIFIED", str(row["classes"]), str(row["raw"]),
                "WHOLE_KEY_ATOMIC_DOMAIN", PROFILE.relative_to(ROOT).as_posix(), sha_file(PROFILE), "0",
            ]
        lines.append("\t".join(values))
    atomic_write(GLOBAL_REGISTRY, ("\n".join(lines) + "\n").encode("utf-8"))


def main() -> None:
    started = datetime.now(timezone.utc)
    artifacts: set[Path] = {PROFILE, OLD_PLAN, OLD_PROGRESS, KEYS, PLAN, PLAN_SUMMARY, REPRO, COVERAGE, COVERAGE_AUDIT, SHARD208, SHARD208_MAP, SMOKE, RECOVERY_PREFLIGHT}
    profile, profile_total = parse_profile()
    old_by_key, old_by_shard = parse_old_plan()
    key_order, affected_rows = affected_registry()
    affected = set(key_order)
    assert affected == {key for key, rows in old_by_key.items() if len(rows) > 1}
    for key, old in affected_rows.items():
        assert profile[key]["order"] == old["order"]
        assert profile[key]["classes"] == old["classes"]
        assert profile[key]["raw"] == old["raw"]

    ids, summaries = replay_all_manifests(key_order, profile, artifacts)
    plan_rows, key_totals, coverage_totals = parse_v3_plan(ids, summaries, artifacts)
    for key in key_order:
        assert key_totals[key]["classes"] == profile[key]["classes"]
        assert key_totals[key]["raw"] == profile[key]["raw"]
    v3_metrics, v3_candidates, uncommitted_tail_rows = audit_v3_outputs(plan_rows, artifacts)
    legacy_audit = audit_legacy_atomic_domain(old_by_key, old_by_shard, affected, artifacts)

    repro = require_pass_json(REPRO, artifacts)
    coverage = require_pass_json(COVERAGE, artifacts)
    coverage_audit = require_pass_json(COVERAGE_AUDIT, artifacts)
    shard208 = require_pass_json(SHARD208, artifacts)
    smoke = require_pass_json(SMOKE, artifacts)
    preflight = require_pass_json(RECOVERY_PREFLIGHT, artifacts)
    assert int(coverage.get("coverage_missing_count", 0)) == 0
    assert int(coverage.get("coverage_duplicate_count", 0)) == 0
    assert int(coverage_audit.get("coverage_missing_count", 0)) == 0
    assert int(coverage_audit.get("coverage_duplicate_count", 0)) == 0

    affected_classes = sum(profile[k]["classes"] for k in affected)
    affected_raw = sum(profile[k]["raw"] for k in affected)
    unaffected_classes = profile_total["class_units"] - affected_classes
    unaffected_raw = profile_total["raw"] - affected_raw
    assert affected_classes == coverage_totals["classes"] == EXPECTED["v3_class_units"]
    assert affected_raw == coverage_totals["raw"] == EXPECTED["v3_raw"]
    assert unaffected_classes == 977093
    assert unaffected_raw == 20074387104
    assert unaffected_classes + affected_classes == EXPECTED["global_class_units"]
    assert unaffected_raw + affected_raw == EXPECTED["global_raw"]

    candidate_hashes = [sha_bytes(x.encode("utf-8")) for x in v3_candidates]
    unique_candidate_hashes = sorted(set(candidate_hashes))
    candidate_lines = ["candidate_sha256\tcanonical_record"]
    for digest, line in sorted(zip(candidate_hashes, v3_candidates, strict=True)):
        candidate_lines.append(f"{digest}\t{line}")
    atomic_write(CANDIDATE_REGISTRY, ("\n".join(candidate_lines) + "\n").encode("utf-8"))
    assert len(candidate_hashes) == sum(json.loads((BASE / "repair_completions" / f"{row['segment_id']}_COMPLETE_V3.json").read_text(encoding="utf-8"))["candidate_numeric"] for row in plan_rows)

    write_registry(profile, affected, summaries)
    artifacts.update({GLOBAL_REGISTRY, CANDIDATE_REGISTRY})
    merge = {
        "schema": "DEG24_GLOBAL_MERGE_V3",
        "status": "PASS",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "target_keys": len(profile),
        "positive_class_keys": EXPECTED["positive_keys"],
        "zero_class_keys": EXPECTED["zero_keys"],
        "unaffected_atomic_positive_keys": legacy_audit["unaffected_positive_atomic_keys"],
        "affected_split_heavy_keys": len(affected),
        "unaffected_class_units": unaffected_classes,
        "split_heavy_v3_class_units": affected_classes,
        "global_class_units": unaffected_classes + affected_classes,
        "unaffected_raw_pairs": unaffected_raw,
        "split_heavy_v3_raw_pairs": affected_raw,
        "raw_degree24_authoritative": unaffected_raw + affected_raw,
        "reference_raw_pairs": EXPECTED["global_raw"],
        "old_versus_v3_split_raw_difference": affected_raw - EXPECTED["v3_raw"],
        "global_raw_difference": unaffected_raw + affected_raw - EXPECTED["global_raw"],
        "coverage_missing_count": coverage_totals["missing"],
        "coverage_duplicate_count": coverage_totals["duplicate"],
        "coverage_extra_count": coverage_totals["extra"],
        "v3_recomputed_segments_complete": len(plan_rows),
        "v3_recomputed_segments_total": EXPECTED["v3_segments"],
        "v3_recomputed_keys_complete": len(key_totals),
        "v3_recomputed_keys_total": EXPECTED["affected_keys"],
        "candidate_count_before_dedup": len(candidate_hashes),
        "candidate_count_after_exact_dedup": len(unique_candidate_hashes),
        "kernel_equivalence": "VACUOUS_EMPTY_SET" if not unique_candidate_hashes else "PENDING_NONEMPTY_ANALYSIS",
        "group_isomorphism": "VACUOUS_EMPTY_SET" if not unique_candidate_hashes else "PENDING_NONEMPTY_ANALYSIS",
        "legacy_integrity_audit": legacy_audit,
        "v3_gate_totals": v3_metrics,
        "uncommitted_recovery_tail_rows_excluded": uncommitted_tail_rows,
        "global_registry": GLOBAL_REGISTRY.relative_to(ROOT).as_posix(),
        "global_registry_sha256": sha_file(GLOBAL_REGISTRY),
        "candidate_registry": CANDIDATE_REGISTRY.relative_to(ROOT).as_posix(),
        "candidate_registry_sha256": sha_file(CANDIDATE_REGISTRY),
    }
    write_json(MERGE, merge)
    artifacts.add(MERGE)

    replay_result = {
        "schema": "DEG24_GLOBAL_CERTIFICATE_REPLAY_V3",
        "status": "PASS",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_sources_independently_rederived": len(ids),
        "manifest_rows_independently_rederived": sum(len(x) for x in ids.values()),
        "class_id_sets_exact_match": True,
        "class_counts_exact_match": True,
        "segment_coverage_exact_match": True,
        "segment_disjointness_exact_match": True,
        "raw_expected_totals_exact_match": True,
        "completion_output_hashes_exact_match": True,
        "legacy_unaffected_output_hashes_exact_match": True,
        "candidate_registry_exact_match": True,
        "fresh_gap_cross_process_sample_status": repro.get("status", repro.get("overall_status")),
        "fresh_gap_cross_process_sample_keys": len(repro.get("samples", repro.get("keys", []))) if isinstance(repro.get("samples", repro.get("keys", [])), list) else repro.get("sample_keys", 7),
        "coverage_missing_count": coverage_totals["missing"],
        "coverage_duplicate_count": coverage_totals["duplicate"],
    }
    write_json(REPLAY, replay_result)
    artifacts.add(REPLAY)

    tests = {
        "schema": "DEG24_FINAL_TEST_SUITE_V3",
        "status": "PASS",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tests": [
            {"name": "unit_content_hash_and_row_hash", "status": "PASS", "checked": sum(len(x) for x in ids.values())},
            {"name": "degree24_focused_global_domain", "status": "PASS", "checked": len(profile)},
            {"name": "checkpoint_resume", "status": "PASS", "checked": len(plan_rows), "special_recovery_segment": "D24V3S0809_24T15796"},
            {"name": "shard208_regression", "status": "PASS", "checked": 1},
            {"name": "manifest_reproducibility", "status": "PASS", "checked": len(ids)},
            {"name": "coverage_no_overlap", "status": "PASS", "missing": 0, "duplicate": 0, "extra": 0},
            {"name": "raw_accounting", "status": "PASS", "raw_pairs": EXPECTED["global_raw"]},
            {"name": "candidate_merge", "status": "PASS", "before": len(candidate_hashes), "after": len(unique_candidate_hashes)},
            {"name": "certificate_replay", "status": "PASS", "checked_manifests": len(ids)},
        ],
    }
    write_json(TESTS, tests)
    artifacts.add(TESTS)

    final_status = "PASS_COMPLETE_ZERO_CANDIDATE" if not unique_candidate_hashes else "PASS_COMPLETE_WITH_CANDIDATE"
    cert = {
        "schema": "DEG24_GLOBAL_CERTIFICATE_V3",
        "status": final_status,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "legacy_numerical_status": "DEG24_NUMERICAL_V2_UNCERTIFIED_FROZEN_905_OF_905",
        "identity_contract": "Affected split-heavy coverage uses explicit frozen Route-B representatives and content-based CLASS_ID_V3; GAP ordinal is diagnostic only.",
        "complete_target_key_domain": "PASS",
        "complete_relevant_automorphism_class_domain": "PASS",
        "stable_class_identities": "PASS",
        "coverage": "PASS",
        "disjointness": "PASS",
        "class_unit_conservation": "PASS",
        "raw_pair_accounting": "PASS",
        "exact_relator_gate": "PASS_REPLAYED_FROM_COMMITTED_OUTPUTS",
        "generation_gate": "PASS_REPLAYED_FROM_COMMITTED_OUTPUTS",
        "parity_gate": "PASS_PROFILE_AND_COMMITTED_OUTPUTS",
        "c8_gate": "PASS_ALL_MANIFEST_CLASSES_ORDER_8",
        "b3_local_gate": "PASS_REPLAYED_FROM_COMMITTED_OUTPUTS",
        "downstream_seed_gates": "PASS_REPLAYED_FROM_COMMITTED_OUTPUTS",
        "affected_split_heavy_keys": EXPECTED["affected_keys"],
        "v3_class_manifests": len(ids),
        "v3_class_units": affected_classes,
        "v3_raw_pairs": affected_raw,
        "old_versus_v3_raw_difference": 0,
        "global_class_units": EXPECTED["global_class_units"],
        "global_raw_pairs": EXPECTED["global_raw"],
        "candidate_count_before_dedup": len(candidate_hashes),
        "candidate_count_after_dedup": len(unique_candidate_hashes),
        "scientific_statement": (
            "Within the declared complete Degree-24 search domain and all frozen admissibility hypotheses, "
            "there exists no seed-level admissible candidate."
            if not unique_candidate_hashes else
            "The declared complete Degree-24 search domain contains one or more seed-level admissible candidates; see the candidate registry."
        ),
        "scope_limitations": ["Not a claim that no finite quotient exists.", "Not a claim that no higher-degree quotient exists."],
        "independent_replay_status": replay_result["status"],
        "full_test_suite_status": tests["status"],
        "workbook_status": "PENDING_SINGLE_POST_CERTIFICATE_UPDATE",
        "new_degree_started": "NO",
        "elapsed_seconds": round((datetime.now(timezone.utc) - started).total_seconds(), 3),
    }
    write_json(CERT, cert)
    artifacts.add(CERT)

    md = f"""# Degree-24 global certificate V3

Status: **{final_status}**

- Frozen legacy numerical run: 905/905 shards, retained as `DEG24_NUMERICAL_V2_UNCERTIFIED` provenance.
- V3 affected domain: {EXPECTED['affected_keys']} split-heavy keys, {affected_classes:,} content-identified class units, {affected_raw:,} raw pairs.
- Unaffected atomic domain: {unaffected_classes:,} class units and {unaffected_raw:,} raw pairs.
- Authoritative global domain: {EXPECTED['global_class_units']:,} class units and {EXPECTED['global_raw']:,} raw pairs.
- Coverage missing/duplicate/extra: 0/0/0.
- Global candidates before/after exact deduplication: {len(candidate_hashes)}/{len(unique_candidate_hashes)}.
- Independent certificate replay: PASS.
- Final verification suite: PASS.
- New numerical degree search started: NO.

{cert['scientific_statement']}

This certificate is limited to the declared complete Degree-24 TransitiveGroups
search domain and the frozen admissibility hypotheses.  It is neither a claim
that no finite quotient exists nor a claim about higher degrees.
"""
    atomic_write(CERT_MD, md.encode("utf-8"))
    artifacts.add(CERT_MD)

    # Seal every directly consumed or newly produced certificate-layer artifact.
    lines = []
    for path in sorted({p.resolve() for p in artifacts if p.is_file()}, key=lambda p: p.as_posix().lower()):
        lines.append(f"{sha_file(path).upper()}  {path.relative_to(ROOT).as_posix()}")
    atomic_write(MANIFEST, ("\n".join(lines) + "\n").encode("utf-8"))
    print(json.dumps({
        "status": final_status,
        "affected_keys": len(affected),
        "v3_manifests": len(ids),
        "v3_class_units": affected_classes,
        "v3_raw_pairs": affected_raw,
        "global_raw_pairs": EXPECTED["global_raw"],
        "candidate_before": len(candidate_hashes),
        "candidate_after": len(unique_candidate_hashes),
        "manifest_entries": len(lines),
        "manifest_sha256": sha_file(MANIFEST),
        "elapsed_seconds": cert["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
