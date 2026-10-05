"""Verify deterministic replay and namespace separation for the seed policy."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from seed_registry import config_sha256, load_seed_config, numpy_rng, python_random


def _fingerprint(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def verify(config_path: Path) -> dict[str, object]:
    config = load_seed_config(config_path)
    fingerprints: dict[str, str] = {}
    checks: dict[str, bool] = {}

    for namespace in config["numpy_namespaces"]:
        sample_a = numpy_rng(namespace, 0, config_path=config_path).integers(
            0, np.iinfo(np.uint64).max, size=32, dtype=np.uint64
        )
        sample_b = numpy_rng(namespace, 0, config_path=config_path).integers(
            0, np.iinfo(np.uint64).max, size=32, dtype=np.uint64
        )
        checks[f"replay:{namespace}"] = bool(np.array_equal(sample_a, sample_b))
        fingerprints[namespace] = _fingerprint(sample_a)

    checks["all_numpy_namespaces_distinct"] = len(set(fingerprints.values())) == len(fingerprints)
    checks["kpm_streams_distinct"] = _fingerprint(
        numpy_rng("kpm.random_vectors", 0, config_path=config_path).standard_normal(64)
    ) != _fingerprint(
        numpy_rng("kpm.random_vectors", 1, config_path=config_path).standard_normal(64)
    )
    checks["slq_streams_distinct"] = _fingerprint(
        numpy_rng("slq.random_vectors", 0, config_path=config_path).standard_normal(64)
    ) != _fingerprint(
        numpy_rng("slq.random_vectors", 1, config_path=config_path).standard_normal(64)
    )

    python_rng_a = python_random(0, config_path=config_path)
    python_rng_b = python_random(0, config_path=config_path)
    python_rng_c = python_random(1, config_path=config_path)
    python_a = [python_rng_a.random() for _ in range(16)]
    python_b = [python_rng_b.random() for _ in range(16)]
    python_c = [python_rng_c.random() for _ in range(16)]
    checks["replay:python.random"] = python_a == python_b
    checks["python_streams_distinct"] = python_a != python_c

    split_names = ["split.training", "split.validation", "split.holdout"]
    split_fingerprints = {
        name: _fingerprint(numpy_rng(name, 0, config_path=config_path).permutation(256))
        for name in split_names
    }
    checks["training_validation_holdout_distinct"] = len(set(split_fingerprints.values())) == 3
    checks["kpm_slq_distinct"] = fingerprints["kpm.random_vectors"] != fingerprints["slq.random_vectors"]

    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "policy_version": config["policy_version"],
        "config_sha256": config_sha256(config_path),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "numpy_bit_generator": config["numpy_bit_generator"],
        "checks": checks,
        "namespace_fingerprints": fingerprints,
        "split_fingerprints": split_fingerprints,
        "failed_checks": failed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("seeds.json"),
        help="Path to the shared seed registry",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON path for the verification record",
    )
    args = parser.parse_args()
    report = verify(args.config)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

