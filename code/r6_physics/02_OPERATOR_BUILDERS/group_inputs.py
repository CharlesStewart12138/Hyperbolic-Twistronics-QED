"""Load immutable R4/R5 inputs without recomputing their mathematics."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FROZEN = Path(os.environ.get("R6_FROZEN_ROOT", str(ROOT / "00_FROZEN_INPUTS"))).expanduser()
SOURCE_CODE = Path(
    os.environ.get(
        "R6_SOURCE_CODE_ROOT",
        str(Path(__file__).resolve().parents[2]),
    )
).expanduser()
QSTAR_ORDER = 46_080
QSTAR_TABLE = Path(os.environ.get(
    "R6_QSTAR_TABLE",
    str(FROZEN / "QSTAR_ARTIFACTS" / "CAND-R4-0005.right_generators_u32le.bin"),
)).expanduser()
QSTAR_MANIFEST = Path(os.environ.get(
    "R6_QSTAR_MANIFEST",
    str(FROZEN / "QSTAR_ARTIFACTS" / "CAND-R4-0005_GROUP_ARTIFACT_MANIFEST.json"),
)).expanduser()
R5_CERTIFICATE = Path(os.environ.get(
    "R6_R5_CERTIFICATE",
    str(FROZEN / "R5_COMMENSURATOR" / "R5_COMM_EXAMPLE_CERTIFICATE.json"),
)).expanduser()


def file_sha256(path: Path) -> str:
    value = sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def load_qstar_generators() -> np.memmap:
    if not QSTAR_TABLE.is_file():
        raise FileNotFoundError(
            "The large Q* generator table is not bundled in the source-only release. "
            "Set R6_QSTAR_TABLE to CAND-R4-0005.right_generators_u32le.bin."
        )
    expected = 8 * QSTAR_ORDER * 4
    if QSTAR_TABLE.stat().st_size != expected:
        raise ValueError(f"Q* generator table has {QSTAR_TABLE.stat().st_size} bytes, expected {expected}")
    return np.memmap(QSTAR_TABLE, dtype="<u4", mode="r", shape=(8, QSTAR_ORDER))


def load_r5_certificate() -> dict[str, object]:
    payload = json.loads(R5_CERTIFICATE.read_text(encoding="ascii"))
    if payload.get("status") != "PASS":
        raise ValueError("R5 explicit commensurator certificate is not PASS")
    return payload


def write_frozen_manifest(output: Path | None = None) -> Path:
    output = Path(output or os.environ.get(
        "R6_FROZEN_MANIFEST_OUTPUT",
        str(ROOT.parent.parent / "outputs" / "r6" / "FROZEN_INPUT_MANIFEST.tsv"),
    ))
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(item for item in FROZEN.rglob("*") if item.is_file() and item != output):
        rows.append((path.relative_to(FROZEN).as_posix(), path.stat().st_size, file_sha256(path)))
    lines = ["relative_path\tbytes\tsha256"]
    lines.extend(f"{name}\t{size}\t{digest}" for name, size, digest in rows)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
