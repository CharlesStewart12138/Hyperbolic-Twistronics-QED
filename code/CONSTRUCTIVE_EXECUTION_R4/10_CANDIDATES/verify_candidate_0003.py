"""Independent exact replay of CAND-R4-0003 through the local gate."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from pathlib import Path

from production_code.group.universal_cover import enumerate_ball


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0003")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0003.certificate.json"
WITNESSES = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
RESULT = R4 / "11_CERTIFICATES" / "CAND-R4-0003.local_independent_replay.json"


def main() -> None:
    certificate_bytes = CERT.read_bytes()
    certificate = json.loads(certificate_bytes)
    elements = candidate.enumerate_image()
    shell = tuple(candidate.generator(i) for i in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball = enumerate_ball(3)
    with WITNESSES.open(encoding="utf-8", newline="") as handle:
        witness_rows = list(csv.DictReader(handle, delimiter="\t"))
    checks = {
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest().upper(),
        "actual_order_matches": len(elements) == certificate["actual_order"] == 23040,
        "order_interval": 2338 <= len(elements) <= 50000,
        "surface_relation": candidate.word_image(relator) == candidate.identity(),
        "physical_shell": len(set(shell)) == 8 and candidate.identity() not in shell,
        "C8_covariance": all(candidate.phi(shell[i]) == shell[(i + 1) % 8] for i in range(8)),
        "C8_eighth_identity": all(_iterate_phi(element, 8) == element for element in elements),
        "C8_exact_order": any(_iterate_phi(element, 4) != element for element in elements),
        "parity": all((element[8].bit_count() & 1) == 1 for element in shell),
        "complete_local_B_geom_3": len({candidate.word_image(element.representative) for element in ball.elements}) == 457,
        "all_accumulated_witnesses_separated": all(candidate.word_image(tuple(row["Canonical word"].split())) != candidate.identity() for row in witness_rows),
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"candidate 0003 local replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "CAND-R4-0003-LOCAL-INDEPENDENT-REPLAY",
        "classification": "PASS",
        "checks": checks,
    }, indent=2) + "\n", encoding="utf-8")


def _iterate_phi(value, count: int):
    for _ in range(count):
        value = candidate.phi(value)
    return value


if __name__ == "__main__":
    main()
