"""Independent replay of the selected class-2 p=2 marginal separator."""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path


factor = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "05_P_QUOTIENT" / "P2C2_C8_MARGINAL_SEPARATOR.certificate.json"
RESULT = R4 / "11_CERTIFICATES" / "P2C2_C8_MARGINAL_SEPARATOR.independent_replay.json"


def main() -> None:
    certificate_bytes = CERT.read_bytes()
    certificate = json.loads(certificate_bytes)
    rows = tuple(certificate["construction"]["selected_dual_row_space_integers"])
    columns = factor.phi_central_columns()
    elements, rotation = factor.enumerate_q(rows)
    if rotation is None:
        raise RuntimeError("independent quotient rotation reconstruction failed")
    target = tuple("g0 g1 g3 g6 g3 g1 g6 g3 g1 g7 g1 g4".split())
    target_orbit = tuple(
        tuple(f"g{(int(token[1]) + power) % 8}" for token in target)
        for power in range(8)
    )
    shell = factor.q_physical_generators(rows)
    checks = {
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest().upper(),
        "dual_row_space_dimension_one": len(rows) == 1,
        "selected_row_is_19": rows == (19,),
        "C8_stable": factor.stable(rows, columns),
        "actual_order_32": len(elements) == 32,
        "generated_complete_normal_form": set(elements) == {(v, z) for v in range(16) for z in range(2)},
        "rotation_bijective": len(set(rotation.values())) == 32,
        "rotation_cycles_shell": all(rotation[shell[i]] == shell[(i + 1) % 8] for i in range(8)),
        "rotation_eighth_identity": all((lambda start: _iterate(rotation, start, 8))(element) == element for element in elements),
        "rotation_exact_order_eight": any(_iterate(rotation, element, 4) != element for element in elements),
        "parity": all((element[0].bit_count() & 1) == 1 for element in shell),
        "target_C8_orbit_separated": all(factor.q_word(word, rows) != (0, 0) for word in target_orbit),
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"independent p2 class2 replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "P2C2-C8-MARGINAL-INDEPENDENT-REPLAY",
        "classification": "PASS",
        "checks": checks,
    }, indent=2) + "\n", encoding="utf-8")


def _iterate(mapping: dict, value, count: int):
    for _ in range(count):
        value = mapping[value]
    return value


if __name__ == "__main__":
    main()
