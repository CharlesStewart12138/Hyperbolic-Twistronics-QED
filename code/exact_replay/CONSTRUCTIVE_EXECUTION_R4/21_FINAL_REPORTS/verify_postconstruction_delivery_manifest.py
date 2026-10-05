from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
MANIFEST = R4 / "21_FINAL_REPORTS/POSTCONSTRUCTION_DELIVERY_MANIFEST.json"
OUTPUT = R4 / "21_FINAL_REPORTS/POSTCONSTRUCTION_DELIVERY_VERIFICATION.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    manifest_hash = sha256(MANIFEST)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    for spec in manifest["files"]:
        path = R4 / spec["path"]
        if not path.is_file():
            failures.append({"path": spec["path"], "reason": "missing"})
            continue
        if path.stat().st_size != spec["bytes"]:
            failures.append({"path": spec["path"], "reason": "size mismatch"})
            continue
        actual = sha256(path)
        if actual != spec["sha256"]:
            failures.append({"path": spec["path"], "reason": "hash mismatch", "actual": actual})
    result = {
        "schema_version": "1.0",
        "classification": "PASS" if not failures else "FAIL",
        "manifest_sha256": manifest_hash,
        "declared_files": manifest["file_count"],
        "verified_files": manifest["file_count"] - len(failures),
        "failed_files": len(failures),
        "failures": failures,
        "verified_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
