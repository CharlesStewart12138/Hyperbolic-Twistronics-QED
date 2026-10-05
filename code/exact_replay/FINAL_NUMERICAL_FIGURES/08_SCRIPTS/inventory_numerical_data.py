from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\work\revise")
OUT_ROOT = ROOT / "FINAL_NUMERICAL_FIGURES"
CATALOG = OUT_ROOT / "00_DATA_INVENTORY" / "NUMERICAL_DATA_CATALOG.tsv"
SUMMARY = OUT_ROOT / "00_DATA_INVENTORY" / "NUMERICAL_DATA_INVENTORY_SUMMARY.json"

EXTENSIONS = {
    ".csv", ".tsv", ".json", ".yaml", ".yml", ".txt", ".log", ".dat",
    ".npy", ".npz", ".h5", ".hdf5", ".zarr", ".xlsx", ".xls", ".parquet",
}

HEADERS = [
    "Data ID", "File path", "File type", "Scientific quantity",
    "Independent variable(s)", "Dependent variable(s)", "Number of records",
    "Parameter range", "Exact / numerical", "Frozen status",
    "Candidate figure IDs", "Notes",
]


def infer_quantity(path: Path) -> str:
    text = str(path).lower()
    rules = [
        (("resolved_dos", "dos_cdf", "broadening_dos", "kpm_moments", "slq_atoms"), "density of states / spectral density"),
        (("spectrum", "spectra", "eigenvalue"), "spectrum / eigenvalues"),
        (("hodge", "hessian", "tensor"), "Hodge/Hessian response"),
        (("root", "magic"), "magic-root response / root certificate"),
        (("cegar", "candidate", "quotient_search"), "constructive quotient-search history"),
        (("scan", "checkpoint", "stream"), "certification scan / checkpoint statistics"),
        (("subgroup", "degree", "orbit", "transitive", "faithful"), "group/permutation complexity"),
        (("commens", "common_cover"), "commensurator / common-cover arithmetic"),
        (("systole", "injectivity", "geodesic"), "hyperbolic length / injectivity geometry"),
        (("moire", "twist", "local_moire"), "moiré geometry / twist response"),
        (("operator", "schur", "hopping", "kernel", "shell"), "operator kernel / row-sum / shell data"),
        (("runtime", "timing", "resource", "profile"), "runtime / resource statistics"),
        (("validation", "audit", "certificate"), "validation / exact certification data"),
    ]
    for keys, label in rules:
        if any(key in text for key in keys):
            return label
    return "numerical or certificate data (unclassified)"


def infer_figures(path: Path, quantity: str) -> str:
    text = (str(path) + " " + quantity).lower()
    ids: list[str] = []
    mappings = [
        (("moire", "twist"), range(1, 6)),
        (("commensurate", "arithmetic", "height", "denominator"), range(6, 11)),
        (("magic", "root", "five_state", "first_shell", "gap"), range(11, 17)),
        (("hodge", "hessian", "tensor"), range(17, 21)),
        (("cegar", "candidate", "separator", "quotient_search"), range(21, 26)),
        (("scan", "checkpoint", "throughput"), range(26, 30)),
        (("subgroup", "degree", "orbit", "faithful", "transitive"), range(30, 33)),
        (("commensurator", "commens", "common-cover", "common_cover"), range(33, 37)),
        (("schur", "operator", "hopping", "shell", "tail"), range(37, 41)),
        (("spectrum", "spectra", "dos", "eigenvalue", "finite_cover"), range(41, 45)),
    ]
    for keys, nums in mappings:
        if any(key in text for key in keys):
            ids.extend(f"FIG{n:02d}" for n in nums)
    return ",".join(dict.fromkeys(ids))


def exactness(path: Path) -> str:
    text = str(path).lower()
    if any(k in text for k in ("certificate", "exact", "audit", "manifest", "group", "arithmetic", "commens")):
        return "exact/certified metadata"
    if any(k in text for k in ("spectrum", "dos", "numerical", "simulation", "scan", "checkpoint", "root", "hodge")):
        return "numerical/frozen computation"
    return "mixed/undetermined"


def frozen_status(path: Path) -> str:
    text = str(path).lower()
    if any(k in text for k in ("freeze", "frozen", "certificate", "reproducibility", "data\\production", "final_")):
        return "FROZEN_OR_CERTIFIED"
    if "tmp\\" in text or text.startswith("tmp\\"):
        return "INTERMEDIATE_CHECKPOINT"
    return "EXISTING_UNMODIFIED"


def safe_text_line_count(path: Path, size: int) -> str:
    if size > 256 * 1024 * 1024:
        return "not counted (>256 MiB)"
    count = 0
    last = b""
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
                count += block.count(b"\n")
                last = block[-1:] if block else last
        if size and last not in (b"\n", b"\r"):
            count += 1
        if path.suffix.lower() in {".csv", ".tsv"} and count > 0:
            count -= 1
        return str(max(count, 0))
    except OSError:
        return "unreadable"


def json_record_count(path: Path, size: int) -> tuple[str, str]:
    if size > 12 * 1024 * 1024:
        return "1 large JSON document", "content not parsed during lightweight inventory"
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            obj: Any = json.load(handle)
        if isinstance(obj, list):
            return str(len(obj)), "top-level JSON list"
        if isinstance(obj, dict):
            candidates = []
            for key, value in obj.items():
                if isinstance(value, list):
                    candidates.append((len(value), key))
            if candidates:
                length, key = max(candidates)
                return str(length), f"largest list field: {key}"
            return "1", f"JSON object with {len(obj)} top-level keys"
        return "1", "scalar JSON document"
    except Exception as exc:  # inventory must not fail on one damaged certificate
        return "parse failed", f"JSON parse note: {type(exc).__name__}"


def array_metadata(path: Path) -> tuple[str, str]:
    try:
        import numpy as np
        if path.suffix.lower() == ".npy":
            arr = np.load(path, mmap_mode="r", allow_pickle=False)
            records = str(arr.shape[0] if arr.ndim else 1)
            return records, f"shape={arr.shape}; dtype={arr.dtype}"
        with np.load(path, allow_pickle=False) as archive:
            shapes = {name: archive[name].shape for name in archive.files}
        records = str(max((shape[0] if shape else 1) for shape in shapes.values()) if shapes else 0)
        return records, "arrays=" + json.dumps(shapes, default=str, separators=(",", ":"))
    except Exception as exc:
        return "parse failed", f"array metadata note: {type(exc).__name__}"


def infer_columns(path: Path, size: int) -> tuple[str, str, str]:
    suffix = path.suffix.lower()
    if suffix not in {".csv", ".tsv"} or size > 64 * 1024 * 1024:
        return "see source schema", "see source schema", "not summarized"
    delimiter = "\t" if suffix == ".tsv" else ","
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
            row = next(csv.reader(handle, delimiter=delimiter), [])
        columns = [re.sub(r"\s+", " ", col.strip()) for col in row if col.strip()]
        if not columns:
            return "unlabeled", "unlabeled", "header unavailable"
        x = ", ".join(columns[:2])
        y = ", ".join(columns[2:8]) if len(columns) > 2 else columns[-1]
        return x, y, "columns=" + " | ".join(columns[:20])
    except OSError:
        return "unreadable", "unreadable", "header read failed"


def main() -> None:
    rows: list[dict[str, str]] = []
    extension_counts: dict[str, int] = {}
    quantity_counts: dict[str, int] = {}
    total_bytes = 0

    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        current = Path(dirpath)
        dirnames[:] = [
            name for name in dirnames
            if (current / name).resolve() != OUT_ROOT.resolve()
            and name not in {".git", "node_modules", "__pycache__"}
        ]
        for filename in filenames:
            path = current / filename
            suffix = path.suffix.lower()
            if suffix in EXTENSIONS or (path.is_dir() and suffix == ".zarr"):
                paths.append(path)

    paths.sort(key=lambda p: str(p).lower())
    for index, path in enumerate(paths, 1):
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        total_bytes += size
        suffix = path.suffix.lower() or "(none)"
        extension_counts[suffix] = extension_counts.get(suffix, 0) + 1
        quantity = infer_quantity(path)
        quantity_counts[quantity] = quantity_counts.get(quantity, 0) + 1
        independent, dependent, schema_note = infer_columns(path, size)
        note_parts = [f"size_bytes={size}", schema_note]

        if suffix in {".csv", ".tsv", ".txt", ".log", ".dat", ".yaml", ".yml"}:
            records = safe_text_line_count(path, size)
        elif suffix == ".json":
            records, note = json_record_count(path, size)
            note_parts.append(note)
        elif suffix in {".npy", ".npz"}:
            records, note = array_metadata(path)
            note_parts.append(note)
        elif suffix in {".xlsx", ".xls"}:
            records = "workbook"
            note_parts.append("workbook indexed without modification")
        elif suffix in {".h5", ".hdf5", ".parquet", ".zarr"}:
            records = "container"
            note_parts.append("container indexed; dataset shapes deferred to source-specific extraction")
        else:
            records = "unknown"

        relative = path.relative_to(ROOT)
        rows.append({
            "Data ID": f"DATA-{index:05d}",
            "File path": str(relative),
            "File type": suffix.lstrip(".").upper(),
            "Scientific quantity": quantity,
            "Independent variable(s)": independent,
            "Dependent variable(s)": dependent,
            "Number of records": records,
            "Parameter range": "see source / source-specific extraction",
            "Exact / numerical": exactness(relative),
            "Frozen status": frozen_status(relative),
            "Candidate figure IDs": infer_figures(relative, quantity),
            "Notes": "; ".join(part for part in note_parts if part and part != "not summarized"),
        })

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    with CATALOG.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "inventory_status": "COMPLETE_BEFORE_PLOTTING",
        "workspace_root": str(ROOT),
        "catalog_path": str(CATALOG),
        "data_file_count": len(rows),
        "total_bytes_indexed": total_bytes,
        "extension_counts": dict(sorted(extension_counts.items(), key=lambda item: (-item[1], item[0]))),
        "quantity_counts": dict(sorted(quantity_counts.items(), key=lambda item: (-item[1], item[0]))),
        "plotting_started": False,
        "expensive_algorithm_rerun": False,
    }
    with SUMMARY.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
