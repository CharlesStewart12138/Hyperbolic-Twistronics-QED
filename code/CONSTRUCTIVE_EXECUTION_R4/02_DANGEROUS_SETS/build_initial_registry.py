"""Build the small typed D0 constraint registry for Constructive R4.

This deliberately does not materialize the complete global dangerous set.
It records the mandatory physical-shell constraints, injectivity of the
radius-one physical word ball, and five legacy based witnesses whose explicit
words and geometry are present in the certified based registry.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.surface_group import free_reduce
from production_code.group.universal_cover import (
    GEOMETRIC_INVERSE,
    IDENTITY_MATRIX,
    matrix_from_word,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
REGISTRY = OUT / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
WITNESSES = OUT / "09_CEGAR" / "WITNESS_LEDGER.tsv"
MATRIX = OUT / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
CANDIDATES = OUT / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
CERTIFICATE = OUT / "02_DANGEROUS_SETS" / "INITIAL_REGISTRY_CERTIFICATE.json"

G_TO_STANDARD = {
    "g0": ("a1",),
    "g1": ("b1_inv",),
    "g2": ("a1_inv", "b1_inv", "a2"),
    "g3": ("a1_inv", "b1_inv", "b2_inv"),
    "g4": ("a1_inv",),
    "g5": ("b1",),
    "g6": ("a2_inv", "b1", "a1"),
    "g7": ("b2", "b1", "a1"),
}

LEGACY_BASED = {
    "B00000457": {
        "word": ("g0", "g0", "g0", "g0"),
        "depth": 4,
        "displacement": "4",
        "translation": "4",
        "interval": "[3.99999999999999999978,4.00000000000000000043]",
        "source_orbit": "O00000457",
    },
    "B00022289": {
        "word": ("g0", "g0", "g0", "g0", "g0", "g0"),
        "depth": 6,
        "displacement": "6",
        "translation": "6",
        "interval": "[5.99999999999999999957,6.00000000000000000043]",
        "source_orbit": "O00022289",
    },
    "B00022638": {
        "word": ("g0", "g0", "g1", "g0", "g0", "g7"),
        "depth": 6,
        "displacement": "5.84975953484839505643",
        "translation": "5.80288659569967913863",
        "interval": "[5.849759534848395056,5.84975953484839505687]",
        "source_orbit": "O00022638",
    },
    "B00022802": {
        "word": ("g0", "g0", "g1", "g3", "g3", "g2"),
        "depth": 6,
        "displacement": "5.65755560067046571427",
        "translation": "5.41862569234585681821",
        "interval": "[5.65755560067046571384,5.65755560067046571471]",
        "source_orbit": "O00022802",
    },
    "B00028799": {
        "word": ("g0", "g2", "g5", "g0", "g2", "g5"),
        "depth": 6,
        "displacement": "3.10165332482290270148",
        "translation": "2",
        "interval": "[3.10165332482290270126,3.10165332482290270169]",
        "source_orbit": "O00028799",
    },
}


def inverse_word(word: Iterable[str]) -> tuple[str, ...]:
    return tuple(GEOMETRIC_INVERSE[token] for token in reversed(tuple(word)))


def phi_geometric(word: Iterable[str], power: int) -> tuple[str, ...]:
    return tuple(f"g{(int(token[1]) + power) % 8}" for token in word)


def canonical_c8_inverse_word(word: Iterable[str]) -> tuple[str, ...]:
    reduced = tuple(word)
    orbit = []
    for power in range(8):
        image = phi_geometric(reduced, power)
        orbit.extend((image, inverse_word(image)))
    return min(orbit, key=lambda item: (len(item), item))


def standard_word(word: Iterable[str]) -> tuple[str, ...]:
    expanded = tuple(token for generator in word for token in G_TO_STANDARD[generator])
    return free_reduce(expanded)


def exact_key_payload(word: Iterable[str]) -> str:
    key = projective_key(matrix_from_word(tuple(word)))
    return json.dumps(key, separators=(",", ":"))


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest().upper()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest().upper()


def make_record(
    danger_id: str,
    danger_type: str,
    word: tuple[str, ...],
    source: str,
    geometry_statement: str,
    based_displacement: str = "",
    translation_length: str = "",
    translation_interval: str = "",
    source_orbit: str = "",
) -> dict[str, str]:
    canonical = canonical_c8_inverse_word(word)
    payload = exact_key_payload(canonical)
    identity = json.dumps(projective_key(IDENTITY_MATRIX), separators=(",", ":"))
    if payload == identity:
        raise RuntimeError(f"dangerous constraint collapsed to identity: {danger_id}")
    key_hash = digest_text(payload)
    return {
        "danger_id": danger_id,
        "type": danger_type,
        "constraint_word_geometric": " ".join(word),
        "canonical_word_geometric": " ".join(canonical),
        "canonical_word_standard": " ".join(standard_word(canonical)),
        "exact_group_key": payload,
        "exact_group_key_sha256": key_hash,
        "witness_id": f"W-{key_hash[:20]}",
        "word_depth": str(len(canonical)),
        "based_displacement_over_a_B": based_displacement,
        "translation_length_over_a_B": translation_length,
        "translation_length_interval": translation_interval,
        "c8_orbit_id": f"C8-{digest_text(' '.join(canonical))[:20]}",
        "legacy_source_orbit_id": source_orbit,
        "nonidentity_in_Gamma_B": "PASS_EXACT_KEY",
        "geometry_status": "PASS",
        "geometry_statement": geometry_statement,
        "source_certificate": source,
        "registry_status": "ACTIVE_D0",
    }


def build_records() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    frozen = "00_FROZEN_INPUTS/contracts/BOLZA_GENERATOR_SHELL_REGISTRY.yaml"
    for index in range(8):
        word = (f"g{index}",)
        rows.append(make_record(
            f"DSHELL-NONIDENTITY-G{index}", "D_shell", word, frozen,
            "physical nearest-neighbour generator must not map to identity",
        ))
        rows.append(make_record(
            f"DLOCAL-R1-NONIDENTITY-G{index}", "D_local(1)", word, frozen,
            "identity and the indicated radius-one word must remain distinct",
        ))

    for left in range(8):
        for right in range(left + 1, 8):
            word = (f"g{left}", f"g{(right + 4) % 8}")
            rows.append(make_record(
                f"DSHELL-COLLISION-G{left}-G{right}", "D_shell", word, frozen,
                f"physical shell images g{left} and g{right} must remain distinct",
            ))
            rows.append(make_record(
                f"DLOCAL-R1-COLLISION-G{left}-G{right}", "D_local(1)", word, frozen,
                f"radius-one word-ball images g{left} and g{right} must remain distinct",
            ))

    for source_id, item in LEGACY_BASED.items():
        rows.append(make_record(
            f"DLEGACY-BASED-{source_id}", "D_based(6a_B)", item["word"],
            "data/production/short_geodesics/dangerous_based.csv",
            "stored exact based-displacement witness with d_H(o,g.o)<=6*a_B",
            item["displacement"], item["translation"], item["interval"], item["source_orbit"],
        ))
    return sorted(rows, key=lambda row: row["danger_id"])


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = build_records()
    write_tsv(REGISTRY, list(rows[0]), rows)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["witness_id"]].append(row)
    witness_rows = []
    for witness_id, members in sorted(grouped.items()):
        first = members[0]
        based = next((row for row in members if row["based_displacement_over_a_B"]), first)
        witness_rows.append({
            "Witness ID": witness_id,
            "Canonical word": first["canonical_word_geometric"],
            "Exact group key": first["exact_group_key"],
            "Type": "|".join(sorted({row["type"] for row in members})),
            "Word depth": first["word_depth"],
            "Based displacement if relevant": based["based_displacement_over_a_B"],
            "Translation length interval/exact expression": (
                based["translation_length_over_a_B"] or based["translation_length_interval"]
            ),
            "C8 orbit ID": first["c8_orbit_id"],
            "First candidate killed": "",
            "Separator factors known": "",
            "Currently separated by candidate": "NO_CANDIDATE",
            "Certificate path": "02_DANGEROUS_SETS/INITIAL_REGISTRY_CERTIFICATE.json",
        })
    write_tsv(WITNESSES, list(witness_rows[0]), witness_rows)

    write_tsv(MATRIX, ["witness_id"], [{"witness_id": row["Witness ID"]} for row in witness_rows])
    candidate_fields = [
        "Candidate ID", "Parent Candidate", "Construction family", "Parameters", "Factor IDs",
        "Marked quotient hash", "|Q|", "Minimum known faithful degree", "C8 status", "Parity status",
        "Shell status", "Local status", "Based status", "Global status", "Shortest failure witness",
        "Witness orbit ID", "Resource estimate", "Resource status", "Representation status",
        "Final disposition", "Certificate hash",
    ]
    write_tsv(CANDIDATES, candidate_fields, [])

    type_counts = defaultdict(int)
    for row in rows:
        type_counts[row["type"]] += 1
    certificate = {
        "schema_version": "1.0",
        "task_id": "CONSTRUCTIVE-R4-D0",
        "classification": "INITIAL_TYPED_CONSTRAINT_SET_BUILT",
        "root_input_hash": "E3B93E439DFE6D2CCA6EC7185F5E466D851DD7F47341C0C07A928CE09204557B",
        "constraint_rows": len(rows),
        "unique_exact_witnesses": len(witness_rows),
        "type_counts": dict(sorted(type_counts.items())),
        "legacy_based_source_ids": sorted(LEGACY_BASED),
        "global_materialization_performed": False,
        "global_domain_status": "NOT_MATERIALIZED_BY_DESIGN",
        "outputs": {
            str(REGISTRY.relative_to(OUT)).replace("\\", "/"): file_hash(REGISTRY),
            str(WITNESSES.relative_to(OUT)).replace("\\", "/"): file_hash(WITNESSES),
            str(MATRIX.relative_to(OUT)).replace("\\", "/"): file_hash(MATRIX),
            str(CANDIDATES.relative_to(OUT)).replace("\\", "/"): file_hash(CANDIDATES),
        },
        "independent_verification": "PENDING",
    }
    CERTIFICATE.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
