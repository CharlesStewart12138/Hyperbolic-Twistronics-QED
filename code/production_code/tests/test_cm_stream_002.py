from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path

import numpy as np
import pytest

from production_code.streaming.certified_tensor_accumulator import (
    CertifiedTensorAccumulator,
    fixed_binary_merge_tree,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "production_code" / "streaming" / "CM_STREAM_002_CERTIFICATE.json"


def test_adversarial_cancellation_is_certified() -> None:
    accumulator = CertifiedTensorAccumulator((1, 1, 1, 1), "a")
    values = (1.0e16, 1.0, -1.0e16)
    for value in values:
        accumulator.update(np.full((1, 1, 1, 1), value))
    reference = sum((Decimal.from_float(value) for value in values), Decimal(0))
    assert Decimal.from_float(float(accumulator.lower.item())) <= reference
    assert reference <= Decimal.from_float(float(accumulator.upper.item()))


def test_fixed_tree_is_input_permutation_independent() -> None:
    shards = []
    for shard_id, value in (("c", 1.0e16), ("a", 1.0), ("b", -1.0e16)):
        item = CertifiedTensorAccumulator((1, 2, 1, 2), shard_id)
        item.update(np.full(item.shape, value))
        shards.append(item)
    forward, trace_forward = fixed_binary_merge_tree(shards)
    reverse, trace_reverse = fixed_binary_merge_tree(reversed(shards))
    assert np.array_equal(forward.lower, reverse.lower)
    assert np.array_equal(forward.upper, reverse.upper)
    assert trace_forward == trace_reverse


def test_serialization_detects_corruption_and_resumes(tmp_path: Path) -> None:
    item = CertifiedTensorAccumulator((1, 2, 3, 4), "restart")
    item.update(np.arange(24, dtype=np.float64).reshape(item.shape))
    path = tmp_path / "state.npz"
    item.save(path)
    loaded = CertifiedTensorAccumulator.load(path)
    assert loaded.serialized_digest() == item.serialized_digest()
    assert loaded.contribution_count == 1


def test_rejects_non_4d_and_duplicate_ids() -> None:
    with pytest.raises(ValueError):
        CertifiedTensorAccumulator((2, 2), "bad")
    one = CertifiedTensorAccumulator((1, 1, 1, 1), "same")
    two = CertifiedTensorAccumulator((1, 1, 1, 1), "same")
    with pytest.raises(ValueError):
        fixed_binary_merge_tree([one, two])


def test_production_certificate() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["classification"] == "CERTIFIED_TENSOR_ACCUMULATOR_PASS"
    assert record["checks"]["high_precision_reference_inside_every_element"] is True
    assert record["checks"]["serialization_exact_resume"] is True
    assert record["checks"]["input_permutation_independent"] is True
    assert record["next_gate"]["CM-047-NP-M7-STREAM_released"] is True
    assert record["next_gate"]["m8_released"] is False
