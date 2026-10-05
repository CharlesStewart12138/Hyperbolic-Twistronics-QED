#!/usr/bin/env python3
"""Create a sealed, read-only inventory of the pre-repair Degree-24 state."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
OUTDIR = ROOT / "production_code" / "escalations" / "degree24_v3_repair"
MANIFEST = OUTDIR / "DEG24_NUMERICAL_V2_UNCERTIFIED_ARCHIVE_MANIFEST.jsonl"
SUMMARY = OUTDIR / "DEG24_NUMERICAL_V2_UNCERTIFIED_ARCHIVE_SUMMARY.json"
SEAL = OUTDIR / "DEG24_NUMERICAL_V2_UNCERTIFIED_ARCHIVE_SEAL.sha256"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relevant(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if relative.parts[:4] == (
        "production_code",
        "escalations",
        "degree24_v3_repair",
    ):
        return False
    lowered = relative.as_posix().lower()
    if "degree24" in lowered or "degree_24" in lowered or "degree-24" in lowered:
        return True
    return relative.as_posix() in {
        "Hyperbolic_Bilayer_Parameter_Freeze_and_Exact_Code_Plan.xlsx",
        "CODE_WORK_LOG.md",
        "WORK_LOG.md",
        "source_current_195/main.tex",
    }


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists() or SUMMARY.exists() or SEAL.exists():
        raise SystemExit("refusing to overwrite an existing V2 archive seal")

    paths = sorted(
        (path for path in ROOT.rglob("*") if path.is_file() and relevant(path)),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    records = []
    total_bytes = 0
    for path in paths:
        stat = path.stat()
        total_bytes += stat.st_size
        records.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "sha256": sha256_file(path),
            }
        )

    with MANIFEST.open("x", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")

    manifest_sha256 = sha256_file(MANIFEST)
    summary = {
        "label": "DEG24_NUMERICAL_V2_UNCERTIFIED",
        "scientific_status": "NUMERICALLY_COMPLETE_NOT_PROOF_GRADE_CERTIFIED",
        "legacy_shards_complete": 905,
        "files": len(records),
        "bytes": total_bytes,
        "manifest": MANIFEST.relative_to(ROOT).as_posix(),
        "manifest_sha256": manifest_sha256,
        "automation_id": "degree-24",
        "automation_state_before_v3_modification": "PAUSED",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "contract": "V2 files are provenance only; V3 repair files must not overwrite them.",
    }
    SUMMARY.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    summary_sha256 = sha256_file(SUMMARY)
    SEAL.write_text(
        f"{manifest_sha256}  {MANIFEST.name}\n{summary_sha256}  {SUMMARY.name}\n",
        encoding="ascii",
        newline="\n",
    )
    os.chmod(MANIFEST, 0o444)
    os.chmod(SUMMARY, 0o444)
    os.chmod(SEAL, 0o444)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
