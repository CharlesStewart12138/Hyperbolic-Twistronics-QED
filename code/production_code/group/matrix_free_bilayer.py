"""Matrix-free right-regular and row-sharded full interlayer actions.

The implementation is a reference/validation kernel.  Production backends may
replace its Python loops, but must preserve the manifest and algebra exactly.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from math import ceil
from pathlib import Path
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def right_regular_action(
    vector: ArrayLike,
    right_permutations: ArrayLike,
    coefficients: ArrayLike | None = None,
) -> NDArray[np.complex128]:
    """Apply ``sum_s c_s R(s)`` without assembling its sparse matrix.

    ``right_permutations[s, q]`` is the column sampled by row ``q`` for
    generator ``s``.  Each row must be a permutation of ``0,...,N-1``.
    """

    x = np.asarray(vector, dtype=np.complex128)
    permutations = np.asarray(right_permutations)
    if x.ndim != 1 or permutations.ndim != 2 or permutations.shape[1] != x.size:
        raise ValueError("require a vector and a (degree,N) permutation table")
    if not np.issubdtype(permutations.dtype, np.integer):
        raise TypeError("right permutations must have integer dtype")
    expected = np.arange(x.size)
    if any(not np.array_equal(np.sort(row), expected) for row in permutations):
        raise ValueError("each right-action row must be a permutation")
    weights = np.ones(permutations.shape[0], dtype=np.complex128) if coefficients is None else np.asarray(coefficients, dtype=np.complex128)
    if weights.shape != (permutations.shape[0],):
        raise ValueError("one coefficient is required per generator")
    result = np.zeros_like(x)
    for permutation, weight in zip(permutations, weights, strict=True):
        result += weight * x[permutation]
    return result


def write_full_interlayer_row_shards(
    directory: str | Path,
    *,
    order: int,
    rows: ArrayLike,
    columns: ArrayLike,
    weights: ArrayLike,
    rows_per_shard: int,
) -> Path:
    """Write every supplied real radial pair to atomic CSR row shards.

    No same-label or first-shell filtering is performed.  The caller supplies
    the complete supported pair list produced by exact cover geometry.
    """

    if order <= 0 or rows_per_shard <= 0:
        raise ValueError("order and rows_per_shard must be positive")
    row = np.asarray(rows, dtype=np.int64)
    column = np.asarray(columns, dtype=np.int64)
    value = np.asarray(weights, dtype=np.float64)
    if row.ndim != 1 or row.shape != column.shape or row.shape != value.shape:
        raise ValueError("rows, columns and weights must be equal one-dimensional arrays")
    if np.any(row < 0) or np.any(row >= order) or np.any(column < 0) or np.any(column >= order):
        raise ValueError("interlayer index outside quotient")
    if not np.all(np.isfinite(value)):
        raise ValueError("interlayer weights must be finite")
    ordering = np.lexsort((column, row))
    row, column, value = row[ordering], column[ordering], value[ordering]
    if row.size and np.any((row[1:] == row[:-1]) & (column[1:] == column[:-1])):
        raise ValueError("duplicate interlayer pair")

    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    shard_records: list[dict[str, object]] = []
    for start in range(0, order, rows_per_shard):
        stop = min(order, start + rows_per_shard)
        lo, hi = np.searchsorted(row, [start, stop])
        local_rows = row[lo:hi] - start
        row_pointer = np.zeros(stop - start + 1, dtype="<u8")
        np.add.at(row_pointer, local_rows + 1, 1)
        np.cumsum(row_pointer, out=row_pointer)
        arrays = {
            "row_pointer": row_pointer,
            "columns": column[lo:hi].astype("<u4", copy=False),
            "weights": value[lo:hi].astype("<f8", copy=False),
        }
        files: dict[str, dict[str, object]] = {}
        stem = f"rows_{start:012d}_{stop:012d}"
        for name, array in arrays.items():
            final = root / f"{stem}.{name}.npy"
            temporary = root / f"{stem}.{name}.tmp.npy"
            np.save(temporary, array, allow_pickle=False)
            temporary.replace(final)
            files[name] = {"path": final.name, "bytes": final.stat().st_size, "sha256": _sha256(final)}
        shard_records.append({"row_start": start, "row_stop": stop, "entries": int(hi - lo), "files": files})

    manifest = {
        "schema_version": "1.0",
        "format": "full_real_interlayer_csr_row_shards",
        "order": order,
        "entries": int(row.size),
        "rows_per_shard": rows_per_shard,
        "preserves_all_supplied_supported_pairs": True,
        "same_label_reduction": False,
        "first_shell_reduction": False,
        "shards": shard_records,
    }
    path = root / "manifest.json"
    temporary_manifest = root / "manifest.json.tmp"
    temporary_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary_manifest.replace(path)
    return path


def streamed_hermitian_interlayer_action(
    manifest_path: str | Path,
    layer_one: ArrayLike,
    layer_two: ArrayLike,
    *,
    verify_hashes: bool = True,
) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    """Apply ``(T x_2, T^* x_1)`` by reading one immutable row shard at a time."""

    path = Path(manifest_path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    order = int(manifest["order"])
    x1, x2 = np.asarray(layer_one, dtype=np.complex128), np.asarray(layer_two, dtype=np.complex128)
    if x1.shape != (order,) or x2.shape != (order,):
        raise ValueError("layer vectors do not match manifest order")
    y1, y2 = np.zeros_like(x1), np.zeros_like(x2)
    seen_entries = 0
    for shard in manifest["shards"]:
        arrays: dict[str, NDArray[np.generic]] = {}
        for name, record in shard["files"].items():
            file_path = path.parent / record["path"]
            if verify_hashes and _sha256(file_path) != record["sha256"]:
                raise ValueError(f"interlayer shard hash mismatch: {file_path.name}")
            arrays[name] = np.load(file_path, mmap_mode="r", allow_pickle=False)
        row_pointer = arrays["row_pointer"]
        columns = arrays["columns"]
        weights = arrays["weights"]
        start, stop = int(shard["row_start"]), int(shard["row_stop"])
        for local_row, global_row in enumerate(range(start, stop)):
            lo, hi = int(row_pointer[local_row]), int(row_pointer[local_row + 1])
            if lo == hi:
                continue
            cols = columns[lo:hi]
            vals = weights[lo:hi]
            y1[global_row] += np.dot(vals, x2[cols])
            np.add.at(y2, cols, vals * x1[global_row])
        seen_entries += int(shard["entries"])
    if seen_entries != int(manifest["entries"]):
        raise ValueError("interlayer manifest entry-count mismatch")
    return y1, y2


@dataclass(frozen=True)
class ProductionLowerBound:
    quotient_order: int
    zero_twist_degree: int
    one_sided_entries: int
    compact_csr_bytes: int
    complex128_bilayer_vector_bytes: int
    probe_batch: int
    kpm_passes_per_parameter: int
    stream_bytes_per_parameter: int
    primary_parameter_points: int
    primary_grid_stream_bytes: int
    primary_grid_years_at_10_GBps: float
    complex_multiply_adds_per_parameter: int

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def production_lower_bound(
    *,
    quotient_order: int,
    zero_twist_degree: int,
    kpm_moments: int,
    probes: int,
    probe_batch: int,
    theta_points: int,
    coupling_points: int,
) -> ProductionLowerBound:
    """Resource lower bound for the frozen zero-twist full interlayer block.

    Storage uses the most favorable real CSR payload: uint32 column plus
    float64 weight, with uint64 row pointers.  Only the preregistered primary
    grid is counted; SLQ, cutoff/lambda holdouts, refinements and construction
    are deliberately excluded.
    """

    if min(quotient_order, zero_twist_degree, kpm_moments, probes, probe_batch, theta_points, coupling_points) <= 0:
        raise ValueError("all resource parameters must be positive")
    entries = quotient_order * zero_twist_degree
    compact_bytes = entries * (4 + 8) + (quotient_order + 1) * 8
    vector_bytes = 2 * quotient_order * 16
    passes = kpm_moments * ceil(probes / probe_batch)
    bytes_per_parameter = compact_bytes * passes
    points = theta_points * coupling_points
    grid_bytes = bytes_per_parameter * points
    return ProductionLowerBound(
        quotient_order=quotient_order,
        zero_twist_degree=zero_twist_degree,
        one_sided_entries=entries,
        compact_csr_bytes=compact_bytes,
        complex128_bilayer_vector_bytes=vector_bytes,
        probe_batch=probe_batch,
        kpm_passes_per_parameter=passes,
        stream_bytes_per_parameter=bytes_per_parameter,
        primary_parameter_points=points,
        primary_grid_stream_bytes=grid_bytes,
        primary_grid_years_at_10_GBps=grid_bytes / 10_000_000_000 / (365.25 * 86400),
        complex_multiply_adds_per_parameter=2 * entries * probes * kpm_moments,
    )
