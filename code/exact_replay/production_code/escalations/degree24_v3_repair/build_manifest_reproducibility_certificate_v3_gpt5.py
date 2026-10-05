#!/usr/bin/env python3
"""Seal the independent, cross-process acceptance gate for V3 class manifests."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
OUT = BASE / "DEG24_MANIFEST_REPRODUCIBILITY_CERTIFICATE_V3.json"
GENERAL = {
    14186: BASE / "manifest_replay/DEG24_KEY_24T14186_MANIFEST_REPLAY_SEED12345_V3.txt",
    11589: BASE / "manifest_replay/DEG24_KEY_24T11589_MANIFEST_REPLAY_SEED12345_V3.txt",
    15981: BASE / "manifest_replay/DEG24_KEY_24T15981_MANIFEST_REPLAY_SEED12345_V3.txt",
    15902: BASE / "manifest_replay/DEG24_KEY_24T15902_MANIFEST_REPLAY_SEED12345_V3.txt",
    8491: BASE / "manifest_replay/DEG24_KEY_24T8491_MANIFEST_REPLAY_SEED12345_V3.txt",
}
SHARD208 = (
    BASE / "DEG24_SHARD208_MANIFEST_REPLAY_SEED12345_V4.txt",
    BASE / "DEG24_SHARD208_MANIFEST_REPLAY_SEED987654321_V4.txt",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_certificate(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[-1] != "DONE":
        raise ValueError(f"certificate envelope failure: {path}")
    fields: dict[str, str] = {}
    for line in lines[:-1]:
        parts = line.split("\t", 1)
        if len(parts) == 2:
            if parts[0] in fields:
                raise ValueError(f"duplicate field {parts[0]}: {path}")
            fields[parts[0]] = parts[1]
    if fields.get("STATUS") != "PASS":
        raise ValueError(f"non-PASS replay: {path}")
    return fields


def exact_zero(fields: dict[str, str], names: tuple[str, ...], path: Path) -> None:
    for name in names:
        if int(fields[name]) != 0:
            raise ValueError(f"{name} is nonzero: {path}")


def validate_manifest_binding(key: int, class_count: int) -> dict:
    directory = BASE / f"manifests/24T{key}"
    summary_path = directory / f"DEG24_KEY_24T{key}_CLASS_MANIFEST_V3.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    manifest = ROOT / summary["manifest"]
    gap_manifest = ROOT / summary["gap_manifest"]
    if (
        summary["key_id"] != f"24T{key}"
        or summary["class_count"] != class_count
        or summary["class_id_count"] != class_count
        or sha256(manifest) != summary["manifest_sha256"]
        or sha256(gap_manifest) != summary["gap_manifest_sha256"]
    ):
        raise ValueError(f"manifest binding failure: 24T{key}")
    return summary


def main() -> None:
    if OUT.exists():
        raise SystemExit(f"refusing to overwrite {OUT}")
    missing = [str(path) for path in (*GENERAL.values(), *SHARD208) if not path.exists()]
    if missing:
        raise FileNotFoundError("missing required replay evidence: " + ", ".join(missing))
    evidence = []
    routes = set()
    representations = set()
    total_missing = 0
    total_duplicates = 0
    for key, path in GENERAL.items():
        fields = parse_certificate(path)
        if fields.get("CERTIFICATE") != "DEG24_KEY_MANIFEST_INDEPENDENT_REPLAY_V3" or fields.get("KEY_ID") != f"24T{key}":
            raise ValueError(f"identity mismatch: {path}")
        manifest_count = int(fields["MANIFEST_CLASS_COUNT"])
        fresh_count = int(fields["FRESH_CLASS_COUNT"])
        if manifest_count != fresh_count or fields.get("CLASS_SIZE_MULTISET_MATCH") != "true":
            raise ValueError(f"class-set exhaustion failure: {path}")
        exact_zero(
            fields,
            ("RECONSTRUCTION_FAILURES", "ORDER_FAILURES", "CLASS_METADATA_MISMATCHES", "DUPLICATE_MATCHES", "MISSING_MATCHES"),
            path,
        )
        summary = validate_manifest_binding(key, manifest_count)
        routes.add(fields["ROUTE"])
        representations.add(fields["REPRESENTATION"])
        total_missing += int(fields["MISSING_MATCHES"])
        total_duplicates += int(fields["DUPLICATE_MATCHES"])
        evidence.append(
            {
                "key_id": f"24T{key}",
                "role": {
                    14186: "smallest_class_count",
                    11589: "median_class_count",
                    15981: "largest_group_order",
                    15902: "highest_class_count",
                    8491: "native_route",
                }[key],
                "route": fields["ROUTE"],
                "representation": fields["REPRESENTATION"],
                "class_count": manifest_count,
                "seed": int(fields["VERIFY_SEED"]),
                "certificate": path.relative_to(ROOT).as_posix(),
                "certificate_sha256": sha256(path),
                "manifest_sha256": summary["manifest_sha256"],
                "status": "PASS",
            }
        )
    shard_positions = []
    for path in SHARD208:
        fields = parse_certificate(path)
        if fields.get("CERTIFICATE") != "DEG24_SHARD208_MANIFEST_INDEPENDENT_REPLAY_V3" or fields.get("KEY_ID") != "24T13493":
            raise ValueError(f"shard208 identity mismatch: {path}")
        manifest_count = int(fields["MANIFEST_CLASS_COUNT"])
        if manifest_count != int(fields["FRESH_CLASS_COUNT"]):
            raise ValueError(f"shard208 class-count mismatch: {path}")
        exact_zero(
            fields,
            ("RECONSTRUCTION_FAILURES", "MEMBERSHIP_FAILURES", "CLASS_METADATA_MISMATCHES", "DUPLICATE_MATCHES", "MISSING_MATCHES", "EXTRA_MATCHES"),
            path,
        )
        validate_manifest_binding(13493, manifest_count)
        total_missing += int(fields["MISSING_MATCHES"])
        total_duplicates += int(fields["DUPLICATE_MATCHES"])
        shard_positions.append(int(fields["AUTHORITATIVE_SOURCE_ORDINAL844_FRESH_POSITION"]))
        evidence.append(
            {
                "key_id": "24T13493",
                "role": "shard208_regression",
                "class_count": manifest_count,
                "seed": int(fields["VERIFY_SEED"]),
                "fresh_position_of_authoritative_source_ordinal844": shard_positions[-1],
                "ordinal_changes": int(fields["ORDINAL_CHANGES"]),
                "certificate": path.relative_to(ROOT).as_posix(),
                "certificate_sha256": sha256(path),
                "status": "PASS",
            }
        )
    if len(set(shard_positions)) != len(shard_positions):
        raise ValueError("shard208 independent processes did not expose ordinal reordering")
    certificate = {
        "schema": "DEG24_MANIFEST_REPRODUCIBILITY_CERTIFICATE_V3",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "route_b_contract": "Workers consume frozen explicit representatives; GAP ordinals are diagnostic only.",
        "sample_key_count": len(GENERAL) + 1,
        "independent_replay_count": len(evidence),
        "routes_covered": sorted(routes),
        "representations_covered": sorted(representations),
        "coverage_missing_count": total_missing,
        "coverage_duplicate_count": total_duplicates,
        "unmatched_class_count": total_missing,
        "duplicate_match_count": total_duplicates,
        "shard208_source_ordinal844_fresh_positions": shard_positions,
        "shard208_ordinal_instability_reproduced": True,
        "same_mathematical_class_sets_reconstructed": True,
        "evidence": evidence,
        "status": "PASS" if total_missing == 0 and total_duplicates == 0 else "FAIL",
    }
    with OUT.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(certificate, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"certificate": OUT.relative_to(ROOT).as_posix(), "status": certificate["status"], "sample_key_count": certificate["sample_key_count"], "replays": certificate["independent_replay_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
