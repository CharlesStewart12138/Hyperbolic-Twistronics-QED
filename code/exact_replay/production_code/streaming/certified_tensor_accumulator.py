"""Outward-rounded full-tensor accumulation with a fixed reduction tree.

Each input float is interpreted as its exact IEEE-754 binary64 value.  Every
addition is expanded by one representable value in each direction, so the
stored interval encloses the exact real sum under round-to-nearest binary64.
The implementation stores two tensors and constant metadata, never streamed
per-state records.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import numpy as np


NEGATIVE_INFINITY = np.float64(-np.inf)
POSITIVE_INFINITY = np.float64(np.inf)


def _shape_tuple(shape: Sequence[int]) -> tuple[int, ...]:
    value = tuple(int(item) for item in shape)
    if len(value) != 4 or any(item <= 0 for item in value):
        raise ValueError("a positive four-dimensional tensor shape is required")
    return value


def _outward_add(left: np.ndarray, right: np.ndarray, direction: np.float64) -> np.ndarray:
    with np.errstate(over="raise", invalid="raise"):
        rounded = np.add(left, right, dtype=np.float64)
    return np.nextafter(rounded, direction)


@dataclass(frozen=True)
class MergeStep:
    level: int
    left: str
    right: str | None
    output: str


class CertifiedTensorAccumulator:
    """A resumable midpoint-independent lower/upper tensor accumulator."""

    schema_version = "1.0"

    def __init__(self, shape: Sequence[int], shard_id: str) -> None:
        self.shape = _shape_tuple(shape)
        if not shard_id or any(character.isspace() for character in shard_id):
            raise ValueError("shard_id must be a nonempty whitespace-free identifier")
        self.shard_id = shard_id
        self.lower = np.zeros(self.shape, dtype=np.float64)
        self.upper = np.zeros(self.shape, dtype=np.float64)
        self.contribution_count = 0

    def update(self, contribution: np.ndarray | Sequence[float]) -> None:
        values = np.asarray(contribution, dtype=np.float64)
        if values.shape != self.shape:
            raise ValueError(f"expected tensor shape {self.shape}, received {values.shape}")
        if not np.isfinite(values).all():
            raise ValueError("all contributions must be finite")
        self.lower = _outward_add(self.lower, values, NEGATIVE_INFINITY)
        self.upper = _outward_add(self.upper, values, POSITIVE_INFINITY)
        self.contribution_count += 1

    def update_stream(self, contributions: Iterable[np.ndarray]) -> None:
        for contribution in contributions:
            self.update(contribution)

    @property
    def midpoint(self) -> np.ndarray:
        return self.lower + (self.upper - self.lower) * np.float64(0.5)

    @property
    def radius(self) -> np.ndarray:
        return (self.upper - self.lower) * np.float64(0.5)

    def contains(self, reference: np.ndarray) -> np.ndarray:
        values = np.asarray(reference, dtype=np.float64)
        if values.shape != self.shape:
            raise ValueError("reference shape mismatch")
        return (self.lower <= values) & (values <= self.upper)

    def serialized_digest(self) -> str:
        digest = hashlib.sha256()
        digest.update(self.schema_version.encode("ascii"))
        digest.update(self.shard_id.encode("utf-8"))
        digest.update(np.asarray(self.shape, dtype="<i8").tobytes(order="C"))
        digest.update(np.asarray([self.contribution_count], dtype="<u8").tobytes(order="C"))
        digest.update(self.lower.astype("<f8", copy=False).tobytes(order="C"))
        digest.update(self.upper.astype("<f8", copy=False).tobytes(order="C"))
        return digest.hexdigest()

    def save(self, path: Path | str) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".tmp.npz")
        np.savez_compressed(
            temporary,
            schema_version=np.asarray([self.schema_version]),
            shard_id=np.asarray([self.shard_id]),
            shape=np.asarray(self.shape, dtype=np.int64),
            contribution_count=np.asarray([self.contribution_count], dtype=np.uint64),
            lower=self.lower,
            upper=self.upper,
            digest=np.asarray([self.serialized_digest()]),
        )
        temporary.replace(destination)

    @classmethod
    def load(cls, path: Path | str) -> "CertifiedTensorAccumulator":
        with np.load(Path(path), allow_pickle=False) as record:
            if str(record["schema_version"][0]) != cls.schema_version:
                raise ValueError("unsupported accumulator schema")
            result = cls(tuple(int(item) for item in record["shape"]), str(record["shard_id"][0]))
            result.contribution_count = int(record["contribution_count"][0])
            result.lower = np.asarray(record["lower"], dtype=np.float64)
            result.upper = np.asarray(record["upper"], dtype=np.float64)
            expected = str(record["digest"][0])
        if result.lower.shape != result.shape or result.upper.shape != result.shape:
            raise ValueError("serialized tensor shape mismatch")
        if not np.isfinite(result.lower).all() or not np.isfinite(result.upper).all():
            raise ValueError("serialized interval contains a nonfinite endpoint")
        if np.any(result.lower > result.upper):
            raise ValueError("serialized interval has reversed endpoints")
        if result.serialized_digest() != expected:
            raise ValueError("serialized accumulator digest mismatch")
        return result

    @classmethod
    def merged(cls, left: "CertifiedTensorAccumulator", right: "CertifiedTensorAccumulator",
               output_id: str) -> "CertifiedTensorAccumulator":
        if left.shape != right.shape:
            raise ValueError("cannot merge unlike tensor shapes")
        result = cls(left.shape, output_id)
        result.lower = _outward_add(left.lower, right.lower, NEGATIVE_INFINITY)
        result.upper = _outward_add(left.upper, right.upper, POSITIVE_INFINITY)
        result.contribution_count = left.contribution_count + right.contribution_count
        return result


def fixed_binary_merge_tree(
    shards: Iterable[CertifiedTensorAccumulator],
) -> tuple[CertifiedTensorAccumulator, tuple[MergeStep, ...]]:
    """Merge unique shards in lexicographic ID order using a fixed binary tree."""
    frontier = sorted(shards, key=lambda item: item.shard_id)
    if not frontier:
        raise ValueError("at least one shard is required")
    identifiers = [item.shard_id for item in frontier]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("shard IDs must be unique")
    if len({item.shape for item in frontier}) != 1:
        raise ValueError("all shard tensor shapes must agree")
    trace: list[MergeStep] = []
    level = 0
    while len(frontier) > 1:
        next_frontier: list[CertifiedTensorAccumulator] = []
        iterator: Iterator[CertifiedTensorAccumulator] = iter(frontier)
        for left in iterator:
            right = next(iterator, None)
            if right is None:
                trace.append(MergeStep(level, left.shard_id, None, left.shard_id))
                next_frontier.append(left)
                continue
            output_id = f"L{level}[{left.shard_id}+{right.shard_id}]"
            next_frontier.append(CertifiedTensorAccumulator.merged(left, right, output_id))
            trace.append(MergeStep(level, left.shard_id, right.shard_id, output_id))
        frontier = next_frontier
        level += 1
    return frontier[0], tuple(trace)


def merge_trace_digest(trace: Sequence[MergeStep]) -> str:
    payload = [step.__dict__ for step in trace]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
