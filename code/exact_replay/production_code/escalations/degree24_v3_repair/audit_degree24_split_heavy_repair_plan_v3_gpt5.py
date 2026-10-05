#!/usr/bin/env python3
"""Independently audit V3 plan coverage and segment-data/list identity."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
PLAN = BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.tsv"
PLAN_META = BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.json"
COVERAGE = BASE / "DEG24_SPLIT_HEAVY_COVERAGE_CERTIFICATE_V3.json"
OUT = BASE / "DEG24_SPLIT_HEAVY_COVERAGE_INDEPENDENT_AUDIT_V3.json"
CLASS_ID_PATTERN = re.compile(r'classId:="([0-9a-f]{64})"')


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    if OUT.exists():
        raise SystemExit(f"refusing to overwrite {OUT}")
    meta = json.loads(PLAN_META.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    if meta.get("status") != "PASS" or coverage.get("status") != "PASS":
        raise ValueError("upstream plan/coverage is not PASS")
    if sha_file(PLAN) != meta["plan_sha256"] or sha_file(COVERAGE) != meta["coverage_certificate_sha256"]:
        raise ValueError("upstream plan/coverage hash mismatch")
    rows = list(csv.DictReader(PLAN.open(encoding="utf-8"), delimiter="\t"))
    if len(rows) != meta["segments"] or len({row["segment_id"] for row in rows}) != len(rows):
        raise ValueError("segment registry cardinality failure")
    assigned_by_key: dict[str, list[str]] = defaultdict(list)
    segment_audits = []
    for row in rows:
        id_path = ROOT / row["class_id_list"]
        data_path = ROOT / row["segment_data"]
        if sha_file(id_path) != row["class_id_list_sha256"] or sha_file(data_path) != row["segment_data_sha256"]:
            raise ValueError(f"segment input hash mismatch: {row['segment_id']}")
        ids = id_path.read_text(encoding="ascii").splitlines()
        data_ids = CLASS_ID_PATTERN.findall(data_path.read_text(encoding="utf-8"))
        if ids != data_ids:
            raise ValueError(f"segment data/list CLASS_ID order mismatch: {row['segment_id']}")
        if len(ids) != int(row["class_count"]) or len(set(ids)) != len(ids):
            raise ValueError(f"segment class count/uniqueness failure: {row['segment_id']}")
        if ids[0] != row["class_id_first"] or ids[-1] != row["class_id_last"]:
            raise ValueError(f"segment boundary diagnostics mismatch: {row['segment_id']}")
        expected_segment_hash = sha_text(
            row["segment_id"]
            + "\n"
            + row["class_id_list_sha256"]
            + "\n"
            + row["segment_data_sha256"]
            + "\n"
            + row["raw_pairs"]
            + "\n"
        )
        if expected_segment_hash != row["segment_sha256"]:
            raise ValueError(f"segment binding hash mismatch: {row['segment_id']}")
        assigned_by_key[row["key_id"]].extend(ids)
        segment_audits.append(
            {
                "segment_id": row["segment_id"],
                "key_id": row["key_id"],
                "class_count": len(ids),
                "raw_pairs": int(row["raw_pairs"]),
                "class_id_list_sha256": row["class_id_list_sha256"],
                "segment_data_sha256": row["segment_data_sha256"],
                "status": "PASS",
            }
        )
    if len(assigned_by_key) != 806:
        raise ValueError("affected key count is not 806")
    per_key = []
    global_namespaced = []
    total_manifest_units = 0
    total_assigned_units = 0
    total_raw = 0
    for key_id, assigned in sorted(assigned_by_key.items(), key=lambda item: int(item[0][3:])):
        key = int(key_id[3:])
        manifest_dir = BASE / f"manifests/{key_id}"
        manifest_meta_path = manifest_dir / f"DEG24_KEY_{key_id}_CLASS_MANIFEST_V3.json"
        manifest_tsv_path = manifest_dir / f"DEG24_KEY_{key_id}_CLASS_MANIFEST_V3.tsv"
        manifest_meta = json.loads(manifest_meta_path.read_text(encoding="utf-8"))
        if sha_file(manifest_tsv_path) != manifest_meta["manifest_sha256"]:
            raise ValueError(f"manifest hash mismatch: {key_id}")
        manifest_ids = [row["class_id_v3"] for row in csv.DictReader(manifest_tsv_path.open(encoding="utf-8"), delimiter="\t")]
        counts = Counter(assigned)
        missing = sorted(set(manifest_ids) - set(assigned))
        extra = sorted(set(assigned) - set(manifest_ids))
        duplicate_count = sum(count - 1 for count in counts.values() if count > 1)
        if missing or extra or duplicate_count or len(assigned) != len(manifest_ids):
            raise ValueError(f"coverage/disjointness failure: {key_id}")
        key_rows = [row for row in rows if row["key_id"] == key_id]
        key_raw = sum(int(row["raw_pairs"]) for row in key_rows)
        expected_raw = manifest_meta["group_order"] * len(manifest_ids)
        if key_raw != expected_raw:
            raise ValueError(f"raw identity failure: {key_id}")
        global_namespaced.extend(f"{key_id}:{class_id}" for class_id in assigned)
        total_manifest_units += len(manifest_ids)
        total_assigned_units += len(assigned)
        total_raw += key_raw
        per_key.append(
            {
                "key_id": key_id,
                "manifest_class_count": len(manifest_ids),
                "assigned_class_count": len(assigned),
                "segment_count": len(key_rows),
                "raw_pairs": key_raw,
                "coverage_missing_count": 0,
                "coverage_extra_count": 0,
                "coverage_duplicate_count": 0,
                "status": "PASS",
            }
        )
    global_counter = Counter(global_namespaced)
    global_duplicate_count = sum(count - 1 for count in global_counter.values() if count > 1)
    if (
        global_duplicate_count != 0
        or total_manifest_units != total_assigned_units
        or total_manifest_units != meta["class_units"]
        or total_manifest_units != coverage["manifest_class_units"]
        or total_raw != meta["raw_pairs"]
        or total_raw != coverage["v3_raw_pairs"]
    ):
        raise ValueError("global coverage/raw conservation failure")
    certificate = {
        "schema": "DEG24_SPLIT_HEAVY_COVERAGE_INDEPENDENT_AUDIT_V3",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "affected_keys": len(per_key),
        "segments": len(rows),
        "manifest_class_units": total_manifest_units,
        "assigned_class_units": total_assigned_units,
        "raw_pairs": total_raw,
        "coverage_missing_count": 0,
        "coverage_extra_count": 0,
        "coverage_duplicate_count": global_duplicate_count,
        "every_class_id_occurs_exactly_once": True,
        "segment_data_matches_class_id_lists": True,
        "plan_sha256": sha_file(PLAN),
        "coverage_certificate_sha256": sha_file(COVERAGE),
        "per_key": per_key,
        "segments_audited": segment_audits,
        "status": "PASS",
    }
    with OUT.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(certificate, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"certificate": OUT.relative_to(ROOT).as_posix(), "keys": len(per_key), "segments": len(rows), "class_units": total_manifest_units, "raw_pairs": total_raw, "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
