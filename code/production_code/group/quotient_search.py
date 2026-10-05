"""Bounded finite-quotient search inventory utilities.

The inventory is append-only by quotient identifier: rejected candidates are
never removed or overwritten.  Search orchestration may add later Q1/Q2 fields
only by writing a new, uniquely identified candidate record.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping


INVENTORY_FIELDS = (
    "quotient_id",
    "construction_method",
    "order_N",
    "stage_reached",
    "q0_status",
    "q1_status",
    "q2_status",
    "production_status",
    "rejection_reasons",
    "systole_word_length",
    "word_r_inj",
    "active_Dc_over_a",
    "no_wraparound",
    "parity",
    "c8",
    "representation_complete",
    "cpu_seconds",
    "peak_memory_bytes",
    "certificate_path",
)


def append_inventory_row(path: str | Path, row: Mapping[str, Any]) -> None:
    """Append one candidate and reject duplicate quotient identifiers."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    existing: set[str] = set()
    if target.exists():
        with target.open("r", encoding="utf-8", newline="") as handle:
            existing = {record["quotient_id"] for record in csv.DictReader(handle)}
    quotient_id = str(row["quotient_id"])
    if quotient_id in existing:
        raise ValueError(f"candidate {quotient_id} already exists; inventory is append-only")
    extras = set(row) - set(INVENTORY_FIELDS)
    if extras:
        raise ValueError(f"unknown inventory fields: {sorted(extras)}")
    values = {field: row.get(field, "") for field in INVENTORY_FIELDS}
    write_header = not target.exists()
    with target.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INVENTORY_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(values)
