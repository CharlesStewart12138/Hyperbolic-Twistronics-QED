"""Exact theta=0 Q* matrix-free periodic operator.

Only theta=0 has certified same-cover covariance.  The implementation uses
the frozen regular right action and never constructs a dense 92,160 matrix.
"""

from __future__ import annotations

from dataclasses import dataclass
import gzip
import json
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator

from group_inputs import FROZEN, QSTAR_ORDER, load_qstar_generators
from local_operator import ScalarBilayerParameters


@dataclass(frozen=True)
class KernelSupport:
    words: tuple[tuple[str, ...], ...]
    distances_over_a: np.ndarray
    weights_over_t: np.ndarray

    @property
    def size(self) -> int:
        return len(self.words)


def load_kernel_support(parameters: ScalarBilayerParameters, maximum_word_depth: int = 6) -> KernelSupport:
    if abs(parameters.theta) > 1e-15:
        raise ValueError("Q* same-cover periodic operator is certified only at theta=0")
    path = FROZEN / "UNIVERSAL_COVER" / "ball_radius_6_exact.jsonl.gz"
    words: list[tuple[str, ...]] = []
    distances: list[float] = []
    weights: list[float] = []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if int(row["minimum_geometric_word_length"]) > int(maximum_word_depth):
                break
            planar = float(row["distance_over_a_B"])
            physical = float(np.sqrt(parameters.h_over_a**2 + planar**2))
            if physical <= parameters.cutoff_over_a + 64 * np.finfo(float).eps:
                words.append(tuple(row["representative"]))
                distances.append(physical)
                weights.append(parameters.w_over_t * np.exp(-(physical - parameters.h_over_a) / parameters.lambda_perp_over_a))
    return KernelSupport(tuple(words), np.asarray(distances), np.asarray(weights))


def _word_permutation(word: tuple[str, ...], generators: np.ndarray) -> np.ndarray:
    permutation = np.arange(QSTAR_ORDER, dtype=np.uint32)
    for token in word:
        permutation = generators[int(token[1]), permutation]
    return permutation


def build_kernel_permutation_memmap(support: KernelSupport, path: Path) -> np.memmap:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    expected = support.size * QSTAR_ORDER * 4
    if path.exists() and path.stat().st_size == expected:
        return np.memmap(path, dtype="<u4", mode="r", shape=(support.size, QSTAR_ORDER))
    generators = load_qstar_generators()
    temporary = path.with_suffix(path.suffix + ".partial")
    if temporary.exists():
        temporary.unlink()
    output = np.memmap(temporary, dtype="<u4", mode="w+", shape=(support.size, QSTAR_ORDER))
    for index, word in enumerate(support.words):
        output[index] = _word_permutation(word, generators)
    output.flush()
    del output
    temporary.replace(path)
    return np.memmap(path, dtype="<u4", mode="r", shape=(support.size, QSTAR_ORDER))


class QStarThetaZeroOperator(LinearOperator):
    def __init__(self, parameters: ScalarBilayerParameters, cache_directory: Path, maximum_word_depth: int = 6, chunk_terms: int = 12):
        if abs(parameters.theta) > 1e-15:
            raise ValueError("same-cover Q* action is available only at theta=0")
        self.parameters = parameters
        self.generators = load_qstar_generators()
        self.support = load_kernel_support(parameters, maximum_word_depth)
        cache = Path(cache_directory) / f"qstar_kernel_permutations_d{maximum_word_depth}.u32"
        self.kernel_permutations = build_kernel_permutation_memmap(self.support, cache)
        self.chunk_terms = int(chunk_terms)
        super().__init__(dtype=np.dtype(np.complex128), shape=(2 * QSTAR_ORDER, 2 * QSTAR_ORDER))

    def _intra(self, vector: np.ndarray) -> np.ndarray:
        return -self.parameters.intralayer_hopping_over_t * np.sum(vector[self.generators], axis=0)

    def _cross(self, vector: np.ndarray) -> np.ndarray:
        output = np.zeros(QSTAR_ORDER, dtype=np.result_type(vector, np.float64))
        for start in range(0, self.support.size, self.chunk_terms):
            stop = min(start + self.chunk_terms, self.support.size)
            permutations = self.kernel_permutations[start:stop]
            output += np.sum(self.support.weights_over_t[start:stop, None] * vector[permutations], axis=0)
        return output

    def _matvec(self, vector: np.ndarray) -> np.ndarray:
        value = np.asarray(vector)
        lower, upper = value[:QSTAR_ORDER], value[QSTAR_ORDER:]
        return np.concatenate([self._intra(lower) + self._cross(upper), self._cross(lower) + self._intra(upper)])

    def action_metadata(self) -> dict[str, object]:
        return {
            "dimension": int(self.shape[0]),
            "qstar_order": QSTAR_ORDER,
            "kernel_terms": self.support.size,
            "maximum_physical_distance_over_a": float(np.max(self.support.distances_over_a)),
            "matrix_free": True,
            "theta": 0.0,
            "boundary_semantics": "exact Q* same-cover periodic action",
        }

