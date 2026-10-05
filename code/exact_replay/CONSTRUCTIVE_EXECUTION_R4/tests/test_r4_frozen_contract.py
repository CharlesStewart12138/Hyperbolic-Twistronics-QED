from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "00_FROZEN_INPUTS"
MANIFEST = FROZEN / "FROZEN_INPUT_MANIFEST.tsv"
CONTRACT = FROZEN / "FROZEN_INPUT_CONTRACT.json"
ROOT_HASH = FROZEN / "FROZEN_INPUT_ROOT_HASH.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest().upper()


def contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_manifest_has_unique_ids_and_paths() -> None:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 22
    assert len({row["logical_id"] for row in rows}) == len(rows)
    assert len({row["relative_path"] for row in rows}) == len(rows)


def test_every_frozen_file_matches_manifest() -> None:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = FROZEN / row["relative_path"]
        assert path.is_file(), row["relative_path"]
        assert path.stat().st_size == int(row["bytes"]), row["relative_path"]
        assert sha256(path) == row["sha256"], row["relative_path"]


def test_root_hash_binds_exact_manifest_bytes() -> None:
    fields = ROOT_HASH.read_text(encoding="ascii").split()
    assert fields == ["sha256", sha256(MANIFEST), "FROZEN_INPUT_MANIFEST.tsv"]


def test_exact_group_and_strict_global_target_are_frozen() -> None:
    c = contract()
    assert c["group"]["presentation"] == "<a1,b1,a2,b2 | [a1,b1][a2,b2]=e>"
    assert c["group"]["basepoint"] == "o=0"
    assert c["target"]["domain"] == "global closed geodesics"
    assert c["target"]["strict_systole"] == "sys(Gamma')>6*a_B"
    assert c["target"]["boundary_policy"] == "equality at 6*a_B fails"
    assert (c["target"]["order_lower_inclusive"], c["target"]["order_upper_inclusive"]) == (2338, 50000)


def test_shell_phi8_and_parity_contracts_are_not_conflated() -> None:
    c = contract()
    assert c["shells"]["shells_equal"] is False
    assert c["shells"]["unqualified_S8_forbidden"] is True
    assert c["phi8"]["exact_order"] == 8
    assert c["phi8"]["standard_presentation_shell_invariant"] is False
    assert c["phi8"]["physical_shell_invariant"] is True
    assert c["parity"]["physical_shell_images"] == [1] * 8
    assert c["parity"]["quotient_requirement"] == "ker(q) subset ker(chi)"


def test_exact_key_semantics_are_frozen() -> None:
    key = contract()["exact_identity"]
    assert key["exact_key_bytes"] == 130
    assert key["external_registry_record_bytes"] == 147
    assert key["projective_sign"].startswith("choose lexicographically smaller")
    assert key["approximate_identity_forbidden"] is True


def test_large_registry_hashes_are_pinned_without_copying_payloads() -> None:
    balls = contract()["exact_ball_authorities"]
    assert balls["closed_axis_displacement_ball"]["elements_including_identity"] == 785_639_753
    assert balls["closed_geometric_center_ball"]["elements_including_identity"] == 23_129_593
    assert balls["closed_axis_displacement_ball"]["complete"] is True
    assert balls["closed_geometric_center_ball"]["complete"] is True


def test_missing_numerical_budget_components_fail_closed_only_at_resource_gate() -> None:
    resources = contract()["resource_contract"]
    assert resources["construction_search"]["maximum_new_peak_working_set_bytes"] == 8 * 1024**3
    assert resources["construction_search"]["broad_transitive_degree_sweeps_forbidden"] is True
    numerical = resources["numerical_A1"]
    assert numerical["resource_status"] == "UNVERIFIED_UNSET_COMPONENTS"
    assert numerical["matvec_budget"] is None
    assert "does not block exact construction" in numerical["scope_effect"]
