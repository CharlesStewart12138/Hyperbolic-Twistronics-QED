"""Independent structural and witness replay for arithmetic R4 factors."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from .build_arithmetic_separators import (
    R4,
    SEPARATOR_MATRIX,
    WITNESS_LEDGER,
    aidentity,
    amul,
    enumerate_image,
    generator,
    sigma,
    word_image,
)


OUT_DIR = R4 / "04_ARITHMETIC"
LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"
RESULT = OUT_DIR / "ARITHMETIC_SEPARATOR_INDEPENDENT_REPLAY.json"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    with LIBRARY.open(encoding="utf-8", newline="") as handle:
        factors = list(csv.DictReader(handle, delimiter="\t"))
    with WITNESS_LEDGER.open(encoding="utf-8", newline="") as handle:
        witnesses = list(csv.DictReader(handle, delimiter="\t"))
    with SEPARATOR_MATRIX.open(encoding="utf-8", newline="") as handle:
        matrix_rows = {row["witness_id"]: row for row in csv.DictReader(handle, delimiter="\t")}

    replay_rows = []
    for factor in factors:
        p = int(factor["parameters"].split("p=", 1)[1].split(";", 1)[0])
        cert_path = R4 / factor["certificate_path"]
        certificate = json.loads(cert_path.read_text(encoding="utf-8"))
        assert file_hash(cert_path) == factor["certificate_sha256"]
        elements, labels, bipartite = enumerate_image(p)
        identity = aidentity(p)
        shell = [generator(index, p) for index in range(8)]
        assert len(elements) == int(factor["actual_order"])
        assert len(elements) == certificate["finite_image"]["actual_generated_order"]
        assert all(amul(shell[index], shell[(index + 4) % 8], p) == identity for index in range(8))
        assert all(sigma(shell[index], p) == shell[(index + 1) % 8] for index in range(8))
        assert word_image(tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3)), p) == identity
        assert labels[0] == 0
        assert bipartite == certificate["proof_rows"]["parity_factors"]

        coverage = 0
        for witness in witnesses:
            image = word_image(tuple(witness["Canonical word"].split()), p)
            separated = int(image != identity)
            assert int(matrix_rows[witness["Witness ID"]][factor["factor_id"]]) == separated
            coverage += separated
        assert coverage == int(factor["coverage_count"])
        replay_rows.append({
            "factor_id": factor["factor_id"],
            "prime": p,
            "actual_order": len(elements),
            "coverage_count": coverage,
            "surface_relation": "PASS",
            "generation": "PASS",
            "C8": "PASS",
            "parity": "PASS" if bipartite else "FAIL",
            "certificate_sha256": factor["certificate_sha256"],
        })

    RESULT.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "CONSTRUCTIVE-R4-ARITHMETIC-INDEPENDENT-REPLAY",
        "classification": "PASS",
        "factor_replays": replay_rows,
        "catalogue_enumeration_used": False,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
