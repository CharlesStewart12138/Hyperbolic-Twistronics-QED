"""Certify CAND-R4-0001 at its first failing mandatory gate: local B3."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from pathlib import Path

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, enumerate_ball, matrix_from_word


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0001")
arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0001.certificate.json"
CANDIDATE_LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
DANGER_REGISTRY = R4 / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
WITNESS_LEDGER = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
SEPARATOR_MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
SEPARATOR_LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"
POSTHOC_SCAN = R4 / "10_CANDIDATES" / "CAND-R4-0001.global_witness.tsv"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def inverse_word(word: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(f"g{(int(token[1]) + 4) % 8}" for token in reversed(word))


def least_local_collision() -> tuple[dict, int]:
    ball = enumerate_ball(3)
    fibers: dict[tuple[int, ...], list[tuple[str, ...]]] = {}
    for element in ball.elements:
        fibers.setdefault(candidate.cword(element.representative), []).append(element.representative)
    witnesses = []
    for words in fibers.values():
        if len(words) < 2:
            continue
        for left_index in range(len(words)):
            for right_index in range(left_index):
                raw = words[left_index] + inverse_word(words[right_index])
                canonical = d0.canonical_c8_inverse_word(raw)
                matrix = matrix_from_word(canonical)
                key = projective_key(matrix)
                if key == projective_key(IDENTITY_MATRIX):
                    raise RuntimeError("local collision difference is unexpectedly identity in Gamma_B")
                if candidate.cword(canonical) != candidate.cidentity():
                    raise RuntimeError("local collision difference does not replay to candidate identity")
                payload = json.dumps(key, separators=(",", ":"))
                witnesses.append((len(canonical), canonical, words[right_index], words[left_index], payload))
    if not witnesses:
        raise RuntimeError("no local B_geom(3) collision found")
    _, canonical, left, right, payload = min(witnesses, key=lambda row: (row[0], row[1], row[2], row[3]))
    key_hash = hashlib.sha256(payload.encode("ascii")).hexdigest().upper()
    record = {
        "canonical_word": list(canonical),
        "colliding_ball_words": [list(left), list(right)],
        "colliding_candidate_image": list(candidate.cword(left)),
        "difference_candidate_image_identity": True,
        "difference_nonidentity_in_Gamma_B": True,
        "exact_group_key": payload,
        "exact_group_key_sha256": key_hash,
        "type": "D_local(3)",
        "proof": "two distinct exact Gamma_B elements of B_geom(3) have the same candidate image",
    }
    return record, len(fibers)


def rewrite_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def register_witness(local: dict, candidate_id: str) -> tuple[str, str]:
    word = tuple(local["canonical_word"])
    key_hash = local["exact_group_key_sha256"]
    witness_id = f"W-{key_hash[:20]}"
    orbit_id = f"C8-{hashlib.sha256(' '.join(word).encode('ascii')).hexdigest().upper()[:20]}"

    with DANGER_REGISTRY.open(encoding="utf-8", newline="") as handle:
        danger_rows = list(csv.DictReader(handle, delimiter="\t"))
        danger_fields = list(danger_rows[0])
    danger_id = f"DLOCAL-R3-C0001-{witness_id}"
    if not any(row["danger_id"] == danger_id for row in danger_rows):
        danger_rows.append({
            "danger_id": danger_id,
            "type": "D_local(3)",
            "constraint_word_geometric": " ".join(word),
            "canonical_word_geometric": " ".join(word),
            "canonical_word_standard": " ".join(d0.standard_word(word)),
            "exact_group_key": local["exact_group_key"],
            "exact_group_key_sha256": key_hash,
            "witness_id": witness_id,
            "word_depth": str(len(word)),
            "based_displacement_over_a_B": "",
            "translation_length_over_a_B": "",
            "translation_length_interval": "",
            "c8_orbit_id": orbit_id,
            "legacy_source_orbit_id": "",
            "nonidentity_in_Gamma_B": "PASS_EXACT_KEY",
            "geometry_status": "PASS_EXACT_BALL_DIFFERENCE",
            "geometry_statement": "difference of two distinct B_geom(3) elements",
            "source_certificate": "10_CANDIDATES/CAND-R4-0001.certificate.json",
            "registry_status": "ACTIVE_CEGAR",
        })
        rewrite_tsv(DANGER_REGISTRY, danger_fields, sorted(danger_rows, key=lambda row: row["danger_id"]))

    with SEPARATOR_LIBRARY.open(encoding="utf-8", newline="") as handle:
        factors = list(csv.DictReader(handle, delimiter="\t"))
    known = []
    factor_values = {}
    for factor in factors:
        prime = int(factor["parameters"].split("p=", 1)[1].split(";", 1)[0])
        value = int(arith.word_image(word, prime) != arith.aidentity(prime))
        factor_values[factor["factor_id"]] = value
        if value:
            known.append(factor["factor_id"])

    with WITNESS_LEDGER.open(encoding="utf-8", newline="") as handle:
        witness_rows = list(csv.DictReader(handle, delimiter="\t"))
        witness_fields = list(witness_rows[0])
    if not any(row["Witness ID"] == witness_id for row in witness_rows):
        witness_rows.append({
            "Witness ID": witness_id,
            "Canonical word": " ".join(word),
            "Exact group key": local["exact_group_key"],
            "Type": "D_local(3)",
            "Word depth": str(len(word)),
            "Based displacement if relevant": "",
            "Translation length interval/exact expression": "",
            "C8 orbit ID": orbit_id,
            "First candidate killed": candidate_id,
            "Separator factors known": ",".join(known),
            "Currently separated by candidate": "NO",
            "Certificate path": "10_CANDIDATES/CAND-R4-0001.certificate.json",
        })
        rewrite_tsv(WITNESS_LEDGER, witness_fields, sorted(witness_rows, key=lambda row: row["Witness ID"]))

    with SEPARATOR_MATRIX.open(encoding="utf-8", newline="") as handle:
        matrix_rows = list(csv.DictReader(handle, delimiter="\t"))
    matrix_fields = ["witness_id"] + [factor["factor_id"] for factor in factors]
    if not any(row["witness_id"] == witness_id for row in matrix_rows):
        matrix_rows.append({"witness_id": witness_id, **factor_values})
        rewrite_tsv(SEPARATOR_MATRIX, matrix_fields, sorted(matrix_rows, key=lambda row: row["witness_id"]))
    return witness_id, orbit_id


def append_candidate(certificate: dict, witness_id: str, orbit_id: str) -> None:
    with CANDIDATE_LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    row = {
        "Candidate ID": certificate["candidate_id"],
        "Parent Candidate": "NONE",
        "Construction family": "arithmetic p=5 actual image with independent parity factor",
        "Parameters": "p=5; K=F5[s]/(s^2-2)",
        "Factor IDs": "ARITH-P5-C0CA0BF862D52B5A,PARITY-C2",
        "Marked quotient hash": certificate["marked_quotient_hash"],
        "|Q|": str(certificate["actual_order"]),
        "Minimum known faithful degree": "UNVERIFIED",
        "C8 status": "PASS",
        "Parity status": "PASS",
        "Shell status": "PASS",
        "Local status": "FAIL_B_GEOM_3",
        "Based status": "NOT_RUN",
        "Global status": "NOT_RUN_GATE_ORDER",
        "Shortest failure witness": witness_id,
        "Witness orbit ID": orbit_id,
        "Resource estimate": json.dumps(certificate["resource"], separators=(",", ":")),
        "Resource status": "PASS_CONSTRUCTION_ONLY",
        "Representation status": "NOT_REQUESTED",
        "Final disposition": "REJECTED_LOCAL_COLLISION",
        "Certificate hash": file_hash(CERT),
    }
    rows = [existing for existing in rows if existing["Candidate ID"] != row["Candidate ID"]]
    rows.append(row)
    rewrite_tsv(CANDIDATE_LEDGER, fields, rows)


def main() -> None:
    elements = candidate.enumerate_candidate()
    local, distinct_images = least_local_collision()
    identity = candidate.cidentity()
    shell = tuple(candidate.cg(index) for index in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    certificate = {
        "schema_version": "1.1",
        "candidate_id": "CAND-R4-0001",
        "parent_candidate": None,
        "construction": "actual generated image of diagonal map (rho_arithmetic_p5,chi)",
        "factor_ids": ["ARITH-P5-C0CA0BF862D52B5A", "PARITY-C2"],
        "actual_order": len(elements),
        "order_window": [2338, 50000],
        "marked_quotient_hash": candidate.marked_hash(elements),
        "gates": {
            "surface_relation": candidate.cword(relator) == identity,
            "generation": True,
            "C8_covariance": all(candidate.csigma(shell[index]) == shell[(index + 1) % 8] for index in range(8)),
            "C8_exact_order": len(set(shell)) == 8,
            "parity": all(generator[8] == 1 for generator in shell),
            "physical_shell_distinct_nonidentity": len(set(shell)) == 8 and identity not in shell,
            "local_B_geom_3": "FAIL",
            "based": "NOT_RUN",
            "global_systole": "NOT_RUN_GATE_ORDER",
        },
        "local_ball": {"exact_elements": 457, "distinct_candidate_images": distinct_images},
        "local_failure_witness": local,
        "quarantined_posthoc_global_scan": {
            "used_for_candidate_disposition": False,
            "reason": "produced before the local-gate failure was detected; later gates are not authoritative after an earlier failure",
            "artifact": str(POSTHOC_SCAN.relative_to(R4)).replace("\\", "/"),
            "artifact_sha256": file_hash(POSTHOC_SCAN),
        },
        "resource": {
            "enumerated_candidate_elements": len(elements),
            "frozen_order_ceiling": 50000,
            "complete_global_registry_authoritatively_scanned": False,
        },
        "classification": "REJECTED_LOCAL_COLLISION",
    }
    required = ["surface_relation", "generation", "C8_covariance", "C8_exact_order", "parity", "physical_shell_distinct_nonidentity"]
    if len(elements) != 31200 or not all(certificate["gates"][key] is True for key in required):
        raise RuntimeError("candidate structural replay failed")
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    witness_id, orbit_id = register_witness(local, certificate["candidate_id"])
    append_candidate(certificate, witness_id, orbit_id)


if __name__ == "__main__":
    main()
