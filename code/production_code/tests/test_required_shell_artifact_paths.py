import csv
from pathlib import Path

import yaml


def test_required_registry_path_contains_two_distinct_shells() -> None:
    path = Path("production_code/group/BOLZA_SHELL_REGISTRY.yaml")
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    geometric = record["shells"]["S8_GEOMETRIC"]
    presentation = record["shells"]["S8_PRESENTATION"]
    assert geometric["use_in_physical_nearest_neighbour_hamiltonian"] is True
    assert presentation["use_in_physical_nearest_neighbour_hamiltonian"] is False
    assert geometric["members"] != presentation["members"]
    assert [row["parity"] for row in record["geometric_generators"]] == [1] * 8


def test_required_903_reaudit_path_has_all_rows() -> None:
    path = Path("data/production/quotient_search_v2_geometric_shell_reaudit/candidates_reaudited.csv")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 903
    assert sum(row["accept_reject"] == "REJECT" for row in rows) == 903


def test_required_contract_and_manuscript_audit_paths_exist() -> None:
    contract = Path("production_code/group/BOLZA_SHELL_CONTRACT_REPAIR.md").read_text(encoding="utf-8")
    audit = Path("production_code/group/MANUSCRIPT_SHELL_CORRECTION_REQUIRED.md").read_text(encoding="utf-8")
    assert "GSC-07" in contract
    assert "STANDARD-PRESENTATION-SHELL ONLY" in contract
    assert "16 affected Article/Methods locations" in audit
    assert "2 affected" in audit and "Supplementary locations" in audit

