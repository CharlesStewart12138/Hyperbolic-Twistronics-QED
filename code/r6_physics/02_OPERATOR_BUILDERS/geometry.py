"""Exact-input Bolza orbit patches and vectorized hyperbolic distances."""

from __future__ import annotations

from dataclasses import dataclass
import gzip
import json
import os
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

from group_inputs import FROZEN, SOURCE_CODE


if str(SOURCE_CODE) not in sys.path:
    sys.path.insert(0, str(SOURCE_CODE))

from production_code.group.universal_cover import (  # noqa: E402
    GENERATOR_MATRICES,
    matrix_multiply,
)


KAPPA_B_A = 3.057141838961996
R_OVER_A = 1.0 / KAPPA_B_A


def _matrix_key(payload: list[list[int]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return tuple(payload[0]), tuple(payload[1])


@dataclass(frozen=True)
class OrbitPatch:
    depth: int
    coordinates: np.ndarray
    radii_over_a: np.ndarray
    word_depths: np.ndarray
    words: tuple[tuple[str, ...], ...]
    adjacency: sp.csr_matrix
    center: int

    @property
    def size(self) -> int:
        return int(self.coordinates.size)


def load_orbit_patch(depth: int) -> OrbitPatch:
    requested = int(depth)
    if requested != depth or not 0 <= requested <= 6:
        raise ValueError("depth must be an integer from 0 through 6")
    path = Path(os.environ.get(
        "R6_UNIVERSAL_COVER",
        str(FROZEN / "UNIVERSAL_COVER" / "ball_radius_6_exact.jsonl.gz"),
    )).expanduser()
    if not path.is_file():
        raise FileNotFoundError(
            "The exact universal-cover archive is not bundled in the source-only release. "
            "Set R6_UNIVERSAL_COVER to ball_radius_6_exact.jsonl.gz."
        )
    records: list[dict[str, object]] = []
    matrices = []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if int(row["minimum_geometric_word_length"]) > requested:
                break
            records.append(row)
            matrices.append(_matrix_key(row["matrix_top_row_exact"]))
    lookup = {matrix: index for index, matrix in enumerate(matrices)}
    rows: list[int] = []
    cols: list[int] = []
    for source, matrix in enumerate(matrices):
        for generator in GENERATOR_MATRICES:
            target = lookup.get(matrix_multiply(matrix, generator))
            if target is not None:
                rows.append(source)
                cols.append(target)
    data = np.ones(len(rows), dtype=np.float64)
    adjacency = sp.coo_matrix((data, (rows, cols)), shape=(len(records), len(records))).tocsr()
    adjacency.data[:] = 1.0
    adjacency.eliminate_zeros()
    if (adjacency - adjacency.T).nnz:
        raise ArithmeticError("restricted Bolza adjacency lost inverse symmetry")
    coords = np.array(
        [complex(float(row["orbit_coordinate_decimal"][0]), float(row["orbit_coordinate_decimal"][1])) for row in records],
        dtype=np.complex128,
    )
    radii = np.array([float(row["distance_over_a_B"]) for row in records], dtype=np.float64)
    depths = np.array([int(row["minimum_geometric_word_length"]) for row in records], dtype=np.int16)
    words = tuple(tuple(str(token) for token in row["representative"]) for row in records)
    return OrbitPatch(requested, coords, radii, depths, words, adjacency, 0)


def pairwise_hyperbolic_distance_over_a(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    z = np.asarray(left, dtype=np.complex128)[:, None]
    w = np.asarray(right, dtype=np.complex128)[None, :]
    denominator = np.sqrt(np.maximum((1.0 - np.abs(z) ** 2) * (1.0 - np.abs(w) ** 2), 1e-300))
    return 2.0 * R_OVER_A * np.arcsinh(np.abs(z - w) / denominator)


def rotate(points: np.ndarray, theta: float) -> np.ndarray:
    return np.asarray(points, dtype=np.complex128) * np.exp(1j * float(theta))
