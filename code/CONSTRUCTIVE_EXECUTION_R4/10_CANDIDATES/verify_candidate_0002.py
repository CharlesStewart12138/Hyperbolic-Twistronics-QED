"""Independent exact replay of CAND-R4-0002 through its local gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from production_code.group.universal_cover import enumerate_ball

from .build_candidate_0002 import (
    R4,
    identity,
    generator,
    phi,
    word_image,
    enumerate_image,
)


CERT = R4 / "10_CANDIDATES" / "CAND-R4-0002.certificate.json"
RESULT = R4 / "11_CERTIFICATES" / "CAND-R4-0002.local_independent_replay.json"


def main() -> None:
    certificate_bytes = CERT.read_bytes()
    certificate = json.loads(certificate_bytes)
    elements = enumerate_image()
    shell = tuple(generator(index) for index in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball = enumerate_ball(3)
    checks = {
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest().upper(),
        "actual_order_matches": len(elements) == certificate["actual_order"],
        "order_interval": 2338 <= len(elements) <= 50000,
        "surface_relation": word_image(relator) == identity(),
        "shell": len(set(shell)) == 8 and identity() not in shell,
        "C8": all(phi(shell[index]) == shell[(index + 1) % 8] for index in range(8)),
        "parity": all((element[8].bit_count() % 2) == 1 for element in shell),
        "local_B_geom_3": len({word_image(element.representative) for element in ball.elements}) == 457,
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"candidate 0002 independent replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "CAND-R4-0002-LOCAL-INDEPENDENT-REPLAY",
        "classification": "PASS",
        "checks": checks,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
