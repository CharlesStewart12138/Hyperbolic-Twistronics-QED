from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from production_code.group.core import in_core
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.quotient_search_v2 import V2Seed, base_s4_candidate
from production_code.group.quotient_search_v3_geometric import base_candidate, symmetric_group_data


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "production" / "quotient_separator"


def _tree():
    dtype = np.dtype([("parent", "<u4"), ("generator", "u1"), ("depth", "u1"), ("reserved", "<u2")])
    return np.memmap(OUT / "based_tree_meta.bin", mode="r", dtype=dtype, offset=20, shape=(23_129_593,))


def _word(tree, element_id: int):
    reverse = []
    current = element_id
    while current:
        reverse.append(int(tree[current]["generator"]))
        current = int(tree[current]["parent"])
    return tuple(reversed(reverse))


def _standard(indices):
    return tuple(token for index in indices for token in GEOMETRIC_TO_STANDARD_WORD[index])


def _candidate(candidate_id: str):
    for line in (ROOT / "data" / "production" / "quotient_reaudit_geometric_shell_final" / "candidates_geometric_shell_reaudit.jsonl").read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["candidate_id"] == candidate_id:
            return base_s4_candidate(V2Seed(candidate_id, tuple(record["base_generator_indices"])))
    for line in (ROOT / "data" / "production" / "quotient_search_v3" / "candidates_v3.jsonl").read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["candidate_id"] == candidate_id:
            degree = int(record["base_group"][1:])
            return base_candidate(symmetric_group_data(degree), candidate_id, tuple(record["base_generator_indices"]))
    raise KeyError(candidate_id)


def test_npz_is_a_lossless_default_one_element_matrix():
    with np.load(OUT / "separator_matrix.npz") as matrix:
        assert matrix["encoding"].item() == "default_one_with_zero_kernel_exceptions_csc"
        assert matrix["element_matrix_shape"].tolist() == [23_129_592, 1182]
        assert matrix["orbit_matrix_shape"].tolist() == [1_446_488, 1182]
        assert matrix["element_ids"][0] == 1 and matrix["element_ids"][-1] == 23_129_592
        mapping = matrix["element_to_orbit_row"]
        weights = matrix["orbit_weight"]
        assert mapping.shape == (23_129_592,)
        assert int(mapping.max()) + 1 == len(weights)
        assert np.array_equal(np.bincount(mapping, minlength=len(weights)), weights)
        indptr = matrix["zero_indptr"]
        indices = matrix["zero_orbit_indices"]
        assert len(indptr) == 1183 and int(indptr[-1]) == 430_394 == len(indices)
        assert np.all(indptr[1:] >= indptr[:-1])
        assert matrix["selected_columns"].tolist() == [973]
        assert int(indptr[974] - indptr[973]) == 0


def test_csc_zero_exceptions_equal_independent_core_membership_samples():
    tree = _tree()
    with np.load(OUT / "separator_matrix.npz") as matrix:
        ids = matrix["candidate_ids"]
        reps = matrix["orbit_representative_element_id"]
        indptr = matrix["zero_indptr"]
        zeros = matrix["zero_orbit_indices"]

        first = _candidate(str(ids[0]))
        first_zero_rows = zeros[int(indptr[0]):int(indptr[1])]
        assert len(first_zero_rows) == 2242
        for row in first_zero_rows[:20]:
            word = _word(tree, int(reps[int(row)]))
            assert in_core(first, _standard(word))
        first_zero_set = set(map(int, first_zero_rows))
        checked = 0
        for row in np.linspace(0, len(reps) - 1, 80, dtype=int):
            if int(row) in first_zero_set:
                continue
            word = _word(tree, int(reps[row]))
            assert not in_core(first, _standard(word))
            checked += 1
        assert checked >= 60

        selected = _candidate(str(ids[973]))
        for row in np.linspace(0, len(reps) - 1, 100, dtype=int):
            word = _word(tree, int(reps[row]))
            assert not in_core(selected, _standard(word))


def test_human_counts_and_solution_match_matrix():
    solution = json.loads((OUT / "based_separator_solution.json").read_text(encoding="utf-8"))
    summary = json.loads((OUT / "BASED_SEPARATOR_SUMMARY.json").read_text(encoding="utf-8"))
    assert solution["solution_status"] == "OPTIMAL_CARDINALITY_AND_IMAGE_ORDER_WITHIN_CARDINALITY_ONE"
    assert solution["selected_columns"] == [973]
    assert solution["cardinality_one_cover_count"] == 137
    assert solution["all_candidates_uncovered_elements"] == 0
    assert summary["separator_solution"]["kernel_hits_in_based_set"] == 0
    assert summary["separator_solution"]["practical_core_image_order"] == 25_920_000
    with (OUT / "candidate_kernel_counts.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1182
    assert rows[973]["candidate_id"] == "V3_S5_MATCHED_COMMUTATOR_0071"
    assert int(rows[973]["kernel_elements"]) == 0
