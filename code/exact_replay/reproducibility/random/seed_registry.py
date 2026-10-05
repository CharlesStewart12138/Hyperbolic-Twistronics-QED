"""Single project entry point for deterministic random-number streams.

Scientific code must request a named stream from this module. Seed values belong
only in seeds.json and must not be copied into compute or plotting scripts.
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any, Mapping

import numpy as np


DEFAULT_CONFIG_PATH = Path(__file__).with_name("seeds.json")


class SeedConfigurationError(ValueError):
    """Raised when the shared seed registry is malformed or misused."""


def load_seed_config(path: str | Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load and validate the project seed registry."""

    config_path = Path(path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "policy_version",
        "master_entropy",
        "numpy_bit_generator",
        "python_random",
        "numpy_namespaces",
    }
    missing = sorted(required.difference(config))
    if missing:
        raise SeedConfigurationError(f"Missing seed-config keys: {missing}")

    entropy = config["master_entropy"]
    if not isinstance(entropy, list) or not entropy or not all(
        isinstance(value, int) and value >= 0 for value in entropy
    ):
        raise SeedConfigurationError("master_entropy must be a non-empty list of non-negative integers")

    namespaces = config["numpy_namespaces"]
    if not isinstance(namespaces, dict) or not namespaces:
        raise SeedConfigurationError("numpy_namespaces must be a non-empty object")

    observed_keys: set[tuple[int, ...]] = set()
    for name, entry in namespaces.items():
        if not isinstance(name, str) or not name:
            raise SeedConfigurationError("Every namespace must have a non-empty string name")
        if not isinstance(entry, Mapping):
            raise SeedConfigurationError(f"Namespace {name!r} must be an object")
        spawn_key = entry.get("spawn_key")
        block_size = entry.get("block_size")
        if not isinstance(spawn_key, list) or not spawn_key or not all(
            isinstance(value, int) and value >= 0 for value in spawn_key
        ):
            raise SeedConfigurationError(f"Namespace {name!r} has an invalid spawn_key")
        if not isinstance(block_size, int) or block_size <= 0:
            raise SeedConfigurationError(f"Namespace {name!r} has an invalid block_size")
        key_tuple = tuple(spawn_key)
        if key_tuple in observed_keys:
            raise SeedConfigurationError(f"Duplicate namespace spawn_key: {spawn_key}")
        observed_keys.add(key_tuple)

    python_config = config["python_random"]
    if not isinstance(python_config, Mapping):
        raise SeedConfigurationError("python_random must be an object")
    if not isinstance(python_config.get("base_seed"), int):
        raise SeedConfigurationError("python_random.base_seed must be an integer")
    if not isinstance(python_config.get("block_size"), int) or python_config["block_size"] <= 0:
        raise SeedConfigurationError("python_random.block_size must be a positive integer")

    bit_generator_name = config["numpy_bit_generator"]
    if not isinstance(bit_generator_name, str) or not hasattr(np.random, bit_generator_name):
        raise SeedConfigurationError(f"Unsupported NumPy bit generator: {bit_generator_name!r}")
    return config


def config_sha256(path: str | Path = DEFAULT_CONFIG_PATH) -> str:
    """Return the SHA-256 identity of the exact seed registry bytes."""

    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _checked_stream_index(stream_index: int, block_size: int, namespace: str) -> int:
    if not isinstance(stream_index, int):
        raise SeedConfigurationError("stream_index must be an integer")
    if not 0 <= stream_index < block_size:
        raise SeedConfigurationError(
            f"stream_index {stream_index} is outside namespace {namespace!r} block [0, {block_size})"
        )
    return stream_index


def numpy_rng(
    namespace: str,
    stream_index: int = 0,
    *,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> np.random.Generator:
    """Return a fresh deterministic NumPy Generator for a named stream."""

    config = load_seed_config(config_path)
    namespaces = config["numpy_namespaces"]
    if namespace not in namespaces:
        raise SeedConfigurationError(f"Unknown NumPy namespace: {namespace!r}")
    entry = namespaces[namespace]
    checked_index = _checked_stream_index(stream_index, entry["block_size"], namespace)
    sequence = np.random.SeedSequence(
        entropy=config["master_entropy"],
        spawn_key=tuple(entry["spawn_key"]) + (checked_index,),
    )
    bit_generator_type = getattr(np.random, config["numpy_bit_generator"])
    return np.random.Generator(bit_generator_type(sequence))


def python_random(
    stream_index: int = 0,
    *,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> random.Random:
    """Return a fresh deterministic Python random.Random instance."""

    config = load_seed_config(config_path)
    entry = config["python_random"]
    checked_index = _checked_stream_index(stream_index, entry["block_size"], "python.random")
    seed_material = f"{entry['base_seed']}:{checked_index}".encode("ascii")
    derived_seed = int.from_bytes(hashlib.sha256(seed_material).digest(), "big")
    return random.Random(derived_seed)
