from __future__ import annotations

import json
from pathlib import Path

from production_code.streaming.run_cm_stream_001 import shard_plan


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "production_code" / "streaming" / "CM_STREAM_001_CERTIFICATE.json"


def test_prefix_partition_is_exact_and_disjoint() -> None:
    plan = shard_plan()
    assert len(plan) == 50
    prefixes = [prefix for _, prefix, _, _ in plan]
    assert len(prefixes) == len(set(prefixes))
    assert prefixes[0] == (0,)
    assert all(prefix[0] == 0 for prefix in prefixes)
    assert all(prefix[i] != (prefix[i - 1] + 4) % 8 for prefix in prefixes for i in range(1, len(prefix)))


def test_certificate_closes_frozen_regression() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["classification"] == "STREAMING_INFRASTRUCTURE_CERTIFIED"
    assert record["primary_totals"]["raw_leaves"] == 5_884_905
    assert record["primary_totals"]["accepted"] == 336_367
    assert record["checks"]["all_shards_complete"] is True
    assert record["checks"]["deterministic_rerun"] is True
    assert record["checks"]["rss_at_or_below_16_GiB"] is True
    assert record["next_gate"]["CM-STREAM-002_released"] is True


def test_resource_forecast_precedes_large_enumeration_artifacts() -> None:
    forecast = json.loads((ROOT / "production_code" / "streaming" / "RESOURCE_FORECAST.json").read_text(encoding="utf-8"))
    assert forecast["expected_states"]["retained_states"] == 0
    assert forecast["hard_rss_ceiling_bytes"] == 48 * 1024**3
    assert "split" in forecast["fallback"]
