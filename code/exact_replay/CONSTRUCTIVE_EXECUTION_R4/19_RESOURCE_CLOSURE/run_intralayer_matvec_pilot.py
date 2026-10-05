"""Safe bounded matrix-free pilot for the certified intralayer shell only."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import psutil


R4 = Path(__file__).resolve().parents[1]
TABLE = R4 / "17_FINAL_FREEZE/artifacts/CAND-R4-0005.right_generators_u32le.bin"
OUT = R4 / "19_RESOURCE_CLOSURE/INTRALAYER_MATRIX_FREE_PILOT.json"
Q = 46080
LAYERS = 2
N = Q * LAYERS
REPETITIONS = 9


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


setup_start = time.perf_counter()
transitions = np.memmap(TABLE, mode="r", dtype="<u4", shape=(8, Q))
setup_seconds = time.perf_counter() - setup_start
process = psutil.Process(os.getpid())
results = []

for dtype in (np.complex64, np.complex128):
    rng = np.random.default_rng(20260915)
    vector = (rng.standard_normal((LAYERS, Q)) + 1j * rng.standard_normal((LAYERS, Q))).astype(dtype)
    output = np.empty_like(vector)
    timings = []
    peak_rss = process.memory_info().rss
    checksum = 0.0
    for repetition in range(REPETITIONS + 1):
        started = time.perf_counter()
        output.fill(0)
        for direction in range(8):
            output += vector[:, transitions[direction]]
        elapsed = time.perf_counter() - started
        peak_rss = max(peak_rss, process.memory_info().rss)
        checksum += float(np.real(output[0, repetition]))
        vector, output = output, vector
        if repetition:
            timings.append(elapsed)
    results.append({
        "precision": np.dtype(dtype).name,
        "bytes_per_scalar": np.dtype(dtype).itemsize,
        "state_vector_bytes": N * np.dtype(dtype).itemsize,
        "repetitions_measured": REPETITIONS,
        "minimum_seconds": min(timings),
        "median_seconds": statistics.median(timings),
        "maximum_seconds": max(timings),
        "peak_process_rss_bytes": peak_rss,
        "checksum_nonzero": checksum != 0.0,
    })

payload = {
    "schema_version": "1.0",
    "classification": "PASS_SAFE_BOUNDED_INTRALAYER_ONLY_PILOT",
    "scope": "two-layer degree-eight intralayer shell matvec only",
    "not_in_scope": [
        "full D_c-supported interlayer operator",
        "Krylov eigensolver",
        "KPM/SLQ",
        "parameter-grid concurrency",
        "production resource upper bound",
    ],
    "candidate_id": "CAND-R4-0005",
    "quotient_vertices": Q,
    "layers": LAYERS,
    "Hilbert_dimension": N,
    "directed_intralayer_entries": LAYERS * Q * 8,
    "transition_table": "17_FINAL_FREEZE/artifacts/CAND-R4-0005.right_generators_u32le.bin",
    "transition_table_sha256": sha256(TABLE),
    "setup_seconds": setup_seconds,
    "results": results,
    "software": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "psutil": psutil.__version__,
    },
    "measured_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    "interpretation": "empirical local timing only; cannot promote Resource Gate while the full interlayer support and mandatory solver/runtime coordinates are unset",
}
OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "classification": payload["classification"],
    "complex64_median_seconds": results[0]["median_seconds"],
    "complex128_median_seconds": results[1]["median_seconds"],
    "max_peak_rss_bytes": max(row["peak_process_rss_bytes"] for row in results),
}, indent=2))
