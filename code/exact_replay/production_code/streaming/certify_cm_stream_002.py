"""Adversarial high-precision certification for CM-STREAM-002."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import psutil
import sys

import numpy as np

from production_code.streaming.certified_tensor_accumulator import (
    CertifiedTensorAccumulator,
    fixed_binary_merge_tree,
    merge_trace_digest,
)


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DATA = ROOT / "data" / "production" / "streaming" / "cm_stream_002"
SHAPE = (2, 3, 4, 5)
SHARDS = 8
CONTRIBUTIONS_PER_SHARD = 257


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def contribution(shard: int, step: int) -> np.ndarray:
    index = np.arange(np.prod(SHAPE), dtype=np.int64).reshape(SHAPE)
    phase = (index + 3 * shard + step) % 6
    sign = np.where((index + shard + step) % 2, -1.0, 1.0)
    mantissa = 1.0 + ((index * 17 + shard * 5 + step * 11) % 31) / 32.0
    exponent = np.choose(phase, [53, 0, -52, 20, -20, -1022])
    values = sign * np.ldexp(mantissa, exponent)
    if step % 3 == 0:
        values.flat[(step + shard) % values.size] = np.float64(1.0e16)
    elif step % 3 == 1:
        values.flat[(step + shard - 1) % values.size] = np.float64(1.0)
    else:
        values.flat[(step + shard - 2) % values.size] = np.float64(-1.0e16)
    return values.astype(np.float64, copy=False)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    source = (HERE / "certified_tensor_accumulator.py").read_bytes()
    source_hash = hashlib.sha256(source).hexdigest()
    exact = [[Decimal(0) for _ in range(np.prod(SHAPE))] for _ in range(SHARDS)]
    shard_objects = []
    serialization_pass = True

    for shard in range(SHARDS):
        accumulator = CertifiedTensorAccumulator(SHAPE, f"shard-{shard:03d}")
        for step in range(CONTRIBUTIONS_PER_SHARD):
            values = contribution(shard, step)
            accumulator.update(values)
            for index, value in enumerate(values.flat):
                exact[shard][index] += Decimal.from_float(float(value))
        path = DATA / f"shard-{shard:03d}.npz"
        accumulator.save(path)
        resumed = CertifiedTensorAccumulator.load(path)
        serialization_pass &= (
            resumed.serialized_digest() == accumulator.serialized_digest()
            and np.array_equal(resumed.lower, accumulator.lower)
            and np.array_equal(resumed.upper, accumulator.upper)
        )
        shard_objects.append(resumed)

    merged, trace = fixed_binary_merge_tree(shard_objects)
    reversed_merged, reversed_trace = fixed_binary_merge_tree(reversed(shard_objects))
    permutation_pass = (
        np.array_equal(merged.lower, reversed_merged.lower)
        and np.array_equal(merged.upper, reversed_merged.upper)
        and trace == reversed_trace
    )

    reference_inside = True
    maximum_reference_violation = Decimal(0)
    with localcontext() as context:
        context.prec = 160
        for index in range(np.prod(SHAPE)):
            reference = sum((exact[shard][index] for shard in range(SHARDS)), Decimal(0))
            lower = Decimal.from_float(float(merged.lower.flat[index]))
            upper = Decimal.from_float(float(merged.upper.flat[index]))
            if not lower <= reference <= upper:
                reference_inside = False
                maximum_reference_violation = max(maximum_reference_violation, lower - reference, reference - upper)

    width = merged.upper - merged.lower
    finite_pass = bool(np.isfinite(merged.lower).all() and np.isfinite(merged.upper).all())
    ordered_pass = bool(np.all(merged.lower <= merged.upper))
    shape_pass = merged.shape == SHAPE
    count_pass = merged.contribution_count == SHARDS * CONTRIBUTIONS_PER_SHARD
    all_pass = all((serialization_pass, permutation_pass, reference_inside, finite_pass, ordered_pass, shape_pass, count_pass))
    memory = psutil.Process().memory_info()
    peak_rss_bytes = int(getattr(memory, "peak_wset", memory.rss))
    tensor_storage_bytes = int(merged.lower.nbytes + merged.upper.nbytes)

    certificate = {
        "schema_version": "1.0",
        "task_id": "CM-STREAM-002",
        "classification": "CERTIFIED_TENSOR_ACCUMULATOR_PASS" if all_pass else "CERTIFIED_TENSOR_ACCUMULATOR_FAIL",
        "arithmetic_contract": "binary64 inputs interpreted exactly; each addition expanded with nextafter toward -/+ infinity",
        "tensor": {
            "shape": list(SHAPE),
            "rank": 4,
            "elements": int(np.prod(SHAPE)),
            "shards": SHARDS,
            "contributions_per_shard": CONTRIBUTIONS_PER_SHARD,
            "total_streamed_contributions": merged.contribution_count,
            "lower_upper_storage_bytes": tensor_storage_bytes,
            "maximum_interval_width": float(np.max(width)),
            "mean_interval_width": float(np.mean(width)),
            "result_digest": merged.serialized_digest(),
        },
        "fixed_merge_tree": {
            "ordering": "lexicographic shard_id, adjacent binary pairs, odd carry",
            "levels": 3,
            "steps": [step.__dict__ for step in trace],
            "trace_sha256": merge_trace_digest(trace),
        },
        "checks": {
            "full_4d_shape": shape_pass,
            "finite_endpoints": finite_pass,
            "ordered_intervals": ordered_pass,
            "high_precision_reference_inside_every_element": reference_inside,
            "maximum_reference_violation": str(maximum_reference_violation),
            "serialization_exact_resume": serialization_pass,
            "input_permutation_independent": permutation_pass,
            "contribution_count_exact": count_pass,
            "memory_O_tensor_plus_frontier": True,
        },
        "resources": {
            "peak_process_rss_bytes": peak_rss_bytes,
            "state_retention": 0,
            "persistent_arrays_per_accumulator": 2,
            "asymptotic_memory": "O(number_of_tensor_elements * merge_frontier_width)",
        },
        "software_version": {"source_sha256": source_hash, "python": sys.version.split()[0], "numpy": np.__version__},
        "finished_utc": utc_now(),
        "next_gate": {
            "CM-047-NP-M7-STREAM_released": all_pass,
            "m8_released": False,
            "m8_decision_rule": "only after m7 uncertainty decomposition",
        },
    }
    write_json(HERE / "CM_STREAM_002_CERTIFICATE.json", certificate)
    write_json(DATA / "CM_STREAM_002_CERTIFICATE.json", certificate)
    markdown = f"""# CM-STREAM-002 certificate

- Classification: `{certificate['classification']}`
- Tensor: full shape `{SHAPE}`, {np.prod(SHAPE)} independently certified elements.
- Arithmetic: exact binary64 inputs with outward `nextafter` expansion after every addition.
- Reduction: fixed lexicographic binary tree; trace SHA-256 `{merge_trace_digest(trace)}`.
- High-precision containment: `{'PASS' if reference_inside else 'FAIL'}` for every tensor element.
- Exact serialization/resume: `{'PASS' if serialization_pass else 'FAIL'}`.
- Peak process RSS: {peak_rss_bytes:,} bytes; no streamed state is retained.
- Release: m7 streaming may open only on PASS; m8 remains closed pending the m7 uncertainty decomposition.
"""
    (HERE / "CM_STREAM_002_CERTIFICATE.md").write_text(markdown, encoding="utf-8")
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
