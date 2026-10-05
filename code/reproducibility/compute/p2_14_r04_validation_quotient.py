"""Generate an explicit finite validation quotient and word injectivity certificate."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.hyperbolic.validation_quotient import build_quotient  # noqa: E402


def _csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path, *, modulus: int = 4) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    elements, edges, certificate = build_quotient(modulus)
    _csv(
        output_dir / "validation_quotient_elements.csv", elements,
        ["quotient_index", "x_a1", "x_b1", "x_a2", "x_b2", "parity", "c8_image_index"],
    )
    _csv(
        output_dir / "validation_quotient_edges.csv", edges,
        ["source_index", "target_index", "generator_index", "generator", "source_parity", "target_parity"],
    )
    (output_dir / "validation_quotient_certificate.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if certificate["status"] != "PASS":
        raise RuntimeError("clean-room validation quotient failed its internal checks")
    return certificate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--modulus", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, modulus=args.modulus), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
