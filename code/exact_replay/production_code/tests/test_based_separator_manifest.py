from __future__ import annotations

import csv
import json
from pathlib import Path
import random

from production_code.group.core import in_core
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.quotient_search_v2 import V2Seed, base_s4_candidate
from production_code.group.quotient_search_v3_geometric import base_candidate, symmetric_group_data


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "production" / "quotient_separator" / "candidate_manifest.tsv"
V2 = ROOT / "data" / "production" / "quotient_reaudit_geometric_shell_final" / "candidates_geometric_shell_reaudit.jsonl"
V3 = ROOT / "data" / "production" / "quotient_search_v3" / "candidates_v3.jsonl"


def _rows():
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, dialect="excel-tab"))


def _standard_word(indices):
    return tuple(token for index in indices for token in GEOMETRIC_TO_STANDARD_WORD[index])


def _orbit_core_decision(candidate, indices):
    if len(indices) % 2:
        return False
    return all(
        candidate.evaluate_word(_standard_word(tuple((index + shift) % 8 for index in indices))) == candidate.identity
        for shift in range(8)
    )


def test_manifest_has_every_registered_candidate_once():
    rows = _rows()
    v2 = [json.loads(line) for line in V2.read_text(encoding="utf-8").splitlines() if line]
    v3 = [json.loads(line) for line in V3.read_text(encoding="utf-8").splitlines() if line]
    assert len(rows) == 1182 == len(v2) + len(v3)
    assert [int(row["column_index"]) for row in rows] == list(range(1182))
    assert len({row["candidate_id"] for row in rows}) == 1182
    assert sum(int(row["degree"]) > 0 for row in rows) == 1158
    assert sum(int(row["degree"]) == 0 for row in rows) == 24


def test_manifest_generator_images_match_frozen_maps():
    rows = _rows()
    v2 = [json.loads(line) for line in V2.read_text(encoding="utf-8").splitlines() if line]
    v3 = [json.loads(line) for line in V3.read_text(encoding="utf-8").splitlines() if line and "base_generator_indices" in line]
    samples = []
    for index in (0, 127, 902):
        record = v2[index]
        samples.append((index, base_s4_candidate(V2Seed(record["candidate_id"], tuple(record["base_generator_indices"])))))
    for offset in (0, 101, 254):
        record = v3[offset]
        degree = int(record["base_group"][1:])
        samples.append((903 + offset, base_candidate(symmetric_group_data(degree), record["candidate_id"], tuple(record["base_generator_indices"]))))
    for column, candidate in samples:
        expected = [candidate.evaluate_word(GEOMETRIC_TO_STANDARD_WORD[i]) for i in range(8)]
        assert [int(rows[column][f"g{i}"]) for i in range(8)] == expected


def test_c8_orbit_kernel_rule_equals_practical_core_definition():
    rows = _rows()
    v2_first = json.loads(V2.read_text(encoding="utf-8").splitlines()[0])
    candidates = [base_s4_candidate(V2Seed(v2_first["candidate_id"], tuple(v2_first["base_generator_indices"])))]
    v3_records = [json.loads(line) for line in V3.read_text(encoding="utf-8").splitlines() if "base_generator_indices" in line]
    for record in (v3_records[0], v3_records[-1]):
        degree = int(record["base_group"][1:])
        candidates.append(base_candidate(symmetric_group_data(degree), record["candidate_id"], tuple(record["base_generator_indices"])))
    rng = random.Random(20260905)
    for candidate in candidates:
        for length in range(7):
            for _ in range(20):
                indices = tuple(rng.randrange(8) for _ in range(length))
                assert _orbit_core_decision(candidate, indices) == in_core(candidate, _standard_word(indices))
