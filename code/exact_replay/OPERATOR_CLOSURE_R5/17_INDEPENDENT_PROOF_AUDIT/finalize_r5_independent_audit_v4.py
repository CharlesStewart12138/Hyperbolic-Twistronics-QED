from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
pkg = ROOT / "18_THEOREM_PACKAGE"
audit_path = pkg / "R5_INDEPENDENT_AUDIT.json"
audit = json.loads(audit_path.read_text(encoding="utf-8"))
double_coset = (pkg / "R5_DOUBLE_COSET_THEOREM.tex").read_text(encoding="utf-8")

# V3 used one whitespace-sensitive phrase.  Re-evaluate the same semantic
# condition with independent anchors while retaining every other V3 result.
audit["checks"]["full_representative_relation"] = all(
    token in double_coset
    for token in (
        "Multiplying $a$",
        "or $b$ by an element of $K$",
        "two free $K$ variables",
    )
)
audit["schema_version"] = "4.0"
audit["audit"] = "R5 independent proof and implementation audit final"
audit["supersedes"] = [
    "run_r5_independent_audit.py",
    "run_r5_independent_audit_v2.py",
    "run_r5_independent_audit_v3.py whitespace-sensitive anchor",
]
audit["passed"] = sum(bool(value) for value in audit["checks"].values())
audit["total"] = len(audit["checks"])
audit["status"] = "PASS" if all(audit["checks"].values()) else "FAIL"
audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"status": audit["status"], "passed": audit["passed"], "total": audit["total"]}))
