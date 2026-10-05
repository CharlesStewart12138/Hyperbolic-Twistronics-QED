"""Independent replay verifier for the Constructive R4 D0 registry."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, matrix_from_word


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
REGISTRY = OUT / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
SOURCE = ROOT / "data" / "production" / "short_geodesics" / "dangerous_based.csv"
RESULT = OUT / "02_DANGEROUS_SETS" / "INITIAL_REGISTRY_INDEPENDENT_REPLAY.json"
LEGACY_IDS = {"B00000457", "B00022289", "B00022638", "B00022802", "B00028799"}


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest().upper()


def key_payload(word: tuple[str, ...]) -> str:
    return json.dumps(projective_key(matrix_from_word(word)), separators=(",", ":"))


def load_legacy_source() -> dict[str, dict[str, str]]:
    found: dict[str, dict[str, str]] = {}
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            source_id = row["canonical_id"]
            if source_id in LEGACY_IDS:
                found[source_id] = row
            if source_id == "B00028799":
                break
    if set(found) != LEGACY_IDS:
        raise AssertionError(f"missing legacy source rows: {sorted(LEGACY_IDS - set(found))}")
    return found


def main() -> None:
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    identity = key_payload(())
    exact_replays = 0
    for row in rows:
        word = tuple(row["canonical_word_geometric"].split())
        payload = key_payload(word)
        assert payload != identity, row["danger_id"]
        assert payload == row["exact_group_key"], row["danger_id"]
        assert digest(payload) == row["exact_group_key_sha256"], row["danger_id"]
        assert row["witness_id"] == f"W-{digest(payload)[:20]}"
        exact_replays += 1

    legacy = load_legacy_source()
    legacy_replays = 0
    for source_id, source in legacy.items():
        row = next(item for item in rows if item["danger_id"] == f"DLEGACY-BASED-{source_id}")
        assert tuple(source["s8_geometric_reduced_word"].split()) == tuple(row["constraint_word_geometric"].split())
        assert int(source["geometric_word_length"]) == int(row["word_depth"])
        assert source["displacement_over_a_B"] == row["based_displacement_over_a_B"]
        assert source["translation_length_over_a_B"] == row["translation_length_over_a_B"]
        assert source["numerical_error_interval"] == row["translation_length_interval"]
        assert source["c8_orbit_id"] == row["legacy_source_orbit_id"]
        assert float(source["displacement_over_a_B"]) <= 6.0
        legacy_replays += 1

    type_counts = {}
    for kind in ("D_shell", "D_local(1)", "D_based(6a_B)"):
        type_counts[kind] = sum(row["type"] == kind for row in rows)
    assert type_counts == {"D_shell": 36, "D_local(1)": 36, "D_based(6a_B)": 5}

    result = {
        "schema_version": "1.0",
        "task_id": "CONSTRUCTIVE-R4-D0-INDEPENDENT-REPLAY",
        "classification": "PASS",
        "exact_nonidentity_and_key_replays": exact_replays,
        "legacy_based_geometry_replays": legacy_replays,
        "type_counts": type_counts,
        "complete_global_set_materialized": False,
        "scope": "D0 only: mandatory shell, B_geom(1) injectivity, and five explicit certified legacy based witnesses",
    }
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
