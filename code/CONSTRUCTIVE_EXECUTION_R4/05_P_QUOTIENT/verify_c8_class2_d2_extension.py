"""Independent replay of the dimension-two class-2 C8 extension."""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path


p2 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")
build = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_d2_extension")
ROOT = Path(__file__).resolve().parents[2]; R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "05_P_QUOTIENT" / "P2C2_C8_D2_EXTENSION.certificate.json"
RESULT = R4 / "11_CERTIFICATES" / "P2C2_C8_D2_EXTENSION.independent_replay.json"


def main() -> None:
    data = CERT.read_bytes(); cert = json.loads(data); rows = tuple(cert["construction"]["selected_dual_row_space_integers"])
    elements, rotation = p2.enumerate_q(rows)
    if rotation is None: raise RuntimeError("rotation replay failed")
    target = tuple("g0 g5 g2 g4 g3 g6 g4 g2 g4 g7 g2 g5".split())
    checks = {
        "certificate_sha256": hashlib.sha256(data).hexdigest().upper(),
        "dimension_two": len(rows) == 2 and len(build.span(rows)) == 4,
        "contains_parent_row_19": 19 in build.span(rows),
        "C8_stable": p2.stable(rows, p2.phi_central_columns()),
        "actual_order_64": len(elements) == 64,
        "complete_normal_form": set(elements) == {(v, z) for v in range(16) for z in range(4)},
        "target_separated": p2.q_word(target, rows) != (0, 0),
        "rotation_eighth": all(_iterate(rotation, element, 8) == element for element in elements),
        "rotation_exact_eight": any(_iterate(rotation, element, 4) != element for element in elements),
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"D2 extension replay failed: {checks}")
    RESULT.write_text(json.dumps({"schema_version": "1.0", "task_id": "P2C2-C8-D2-INDEPENDENT-REPLAY", "classification": "PASS", "checks": checks}, indent=2) + "\n", encoding="utf-8")


def _iterate(mapping, value, count):
    for _ in range(count): value = mapping[value]
    return value


if __name__ == "__main__": main()
