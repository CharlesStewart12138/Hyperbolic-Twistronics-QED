"""Stream frozen exact geometry and record zero-twist support lower bounds."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/production/universal_cover/ball_radius_6_exact.jsonl.gz"
OUT = Path(__file__).resolve().parent / "ZERO_TWIST_SUPPORT_DIAGNOSTIC.json"
Q = 46_080
H_OVER_A = 0.5
CUTOFFS = (2.5, 3.0, 3.5)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


lateral = tuple(math.sqrt(cutoff * cutoff - H_OVER_A * H_OVER_A) for cutoff in CUTOFFS)
counts = [0] * len(CUTOFFS)
largest = [0.0] * len(CUTOFFS)
records = 0
with gzip.open(SOURCE, "rt", encoding="utf-8") as stream:
    for line in stream:
        row = json.loads(line)
        distance = float(row["distance_over_a_B"])
        records += 1
        for index, radius in enumerate(lateral):
            if distance <= radius + 1.0e-14:
                counts[index] += 1
                largest[index] = max(largest[index], distance)

rows = []
for cutoff, radius, count, maximum in zip(CUTOFFS, lateral, counts, largest, strict=True):
    rows.append(
        {
            "D_c_over_a_B": cutoff,
            "lateral_cutoff_over_a_B": radius,
            "support_per_row": count,
            "one_sided_entries_for_Q": Q * count,
            "largest_included_distance_over_a_B": maximum,
        }
    )

payload = {
    "schema_version": "1.0",
    "classification": "EXACT_ZERO_TWIST_DIAGNOSTIC_ONLY",
    "candidate_id": "CAND-R4-0005",
    "quotient_order": Q,
    "h_over_a_B": H_OVER_A,
    "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
    "source_sha256": sha256(SOURCE),
    "source_records": records,
    "support_rows": rows,
    "scope_guard": "These convolution counts apply at zero twist. They are not a generic-twist paired-cover support certificate and cannot close A1.",
    "computed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}

temporary = OUT.with_suffix(".json.tmp")
temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
temporary.replace(OUT)
print(json.dumps({"classification": payload["classification"], "support_per_row": counts}, indent=2))
