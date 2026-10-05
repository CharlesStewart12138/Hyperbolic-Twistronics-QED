"""Portable wall-time and process-memory measurement helpers."""

from __future__ import annotations

import gc
import math
import statistics
import time
import tracemalloc
from collections.abc import Callable
from typing import TypeVar

import psutil


Result = TypeVar("Result")


def profile_callable(
    function: Callable[[], Result],
    *,
    label: str,
    matrix_dimension: int,
    matrix_storage_bytes: int,
    repeats: int,
) -> tuple[dict[str, object], Result]:
    """Profile repeated calls while recording wall time and memory fields."""
    if matrix_dimension < 1 or matrix_storage_bytes < 0 or repeats < 1:
        raise ValueError("dimension/repeats must be positive and storage nonnegative")
    process = psutil.Process()
    gc.collect()
    memory_before = process.memory_info()
    tracemalloc.start()
    durations = []
    result: Result | None = None
    for _ in range(repeats):
        started = time.perf_counter_ns()
        result = function()
        finished = time.perf_counter_ns()
        durations.append((finished - started) / 1.0e9)
    _, traced_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_after = process.memory_info()
    peak_working_set = int(getattr(memory_after, "peak_wset", max(memory_before.rss, memory_after.rss)))
    checks = {
        "wall_times_finite_positive": bool(all(math.isfinite(value) and value > 0.0 for value in durations)),
        "rss_values_nonnegative": bool(memory_before.rss >= 0 and memory_after.rss >= 0),
        "peak_working_set_consistent": bool(peak_working_set >= max(memory_before.rss, memory_after.rss)),
        "traced_peak_nonnegative": bool(traced_peak >= 0),
    }
    record: dict[str, object] = {
        "label": label,
        "matrix_dimension": matrix_dimension,
        "matrix_storage_bytes": matrix_storage_bytes,
        "repeat_count": repeats,
        "wall_time_seconds_each": durations,
        "wall_time_seconds_min": min(durations),
        "wall_time_seconds_median": statistics.median(durations),
        "wall_time_seconds_mean": statistics.fmean(durations),
        "wall_time_seconds_max": max(durations),
        "wall_time_seconds_population_stdev": statistics.pstdev(durations),
        "rss_before_bytes": int(memory_before.rss),
        "rss_after_bytes": int(memory_after.rss),
        "rss_delta_bytes": int(memory_after.rss - memory_before.rss),
        "process_peak_working_set_bytes": peak_working_set,
        "python_traced_peak_bytes": int(traced_peak),
        "checks": checks,
        "failed_checks": sorted(name for name, passed in checks.items() if not passed),
    }
    assert result is not None
    return record, result
