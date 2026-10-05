"""Hash the complete R5 authority/input set without editing R4 artifacts."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R5 = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "R5_FROZEN_INPUT_MANIFEST.json"
TSV = Path(__file__).resolve().parent / "R5_FROZEN_INPUT_MANIFEST.tsv"

DIRECT_FILES = (
    "source_current_195/main.tex",
    "source_current_195/main.pdf",
    "source_companion_471/main.tex",
    "CONSTRUCTIVE_EXECUTION_R4/00_FROZEN_INPUTS/theory_authority/R4_MAIN_AND_SUPPLEMENTS.tex",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/H_FINAL.txt",
    "CONSTRUCTIVE_EXECUTION_R4/99_FINAL_PROJECT_FREEZE/FINAL_ROOT_MANIFEST.json",
    "production_code/MODEL_CONTRACT.md",
    "production_code/config/model.yaml",
    "production_code/config/kernel.yaml",
    "production_code/config/theory_production_benchmark.yaml",
    "production_code/contract_rules/mc_002.py",
    "production_code/contract_rules/mc_006.py",
    "production_code/tests/test_model_contract_mc002.py",
    "production_code/tests/test_model_contract_mc006.py",
    "production_code/group/matrix_free_bilayer.py",
    "production_code/group/physical_adjacency.py",
    "production_code/geometry/hyperbolic.py",
    "production_code/kernel/radial.py",
    "P0-03-02_CHAPTER_STATUS_AUDIT.md",
    "CODE_WORK_LOG.md",
    "data/production/universal_cover/UNIVERSAL_COVER_MANIFEST.json",
    "data/production/universal_cover/INJECTIVITY_BRIDGE_CONTRACT.json",
    "data/production/universal_cover/ball_radius_6_exact.jsonl.gz",
)

TREE_ROOTS = (
    "CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE",
    "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE",
    "CONSTRUCTIVE_EXECUTION_R4/22_OPERATOR_CONSISTENCY",
    "CONSTRUCTIVE_EXECUTION_R4/23_INDEPENDENT_BLOCKER_REVIEW",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


selected: dict[str, Path] = {}
for relative in DIRECT_FILES:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(relative)
    selected[path.relative_to(ROOT).as_posix()] = path
for relative in TREE_ROOTS:
    base = ROOT / relative
    if not base.is_dir():
        raise FileNotFoundError(relative)
    for path in base.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            selected[path.relative_to(ROOT).as_posix()] = path
for path in (ROOT / "out").glob("*.zip"):
    selected[path.relative_to(ROOT).as_posix()] = path

records = []
for relative, path in sorted(selected.items()):
    records.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})

directive = Path(r"C:\Users\charl\.codex\attachments\53094de1-01b7-45aa-b2fa-91bf83246fd9\pasted-text.txt")
if not directive.is_file():
    raise FileNotFoundError(str(directive))
records.append({"path": str(directive), "bytes": directive.stat().st_size, "sha256": sha256(directive)})

canonical = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
input_root = hashlib.sha256(canonical).hexdigest().upper()
payload = {
    "schema_version": "1.0",
    "classification": "R5_FROZEN_INPUTS_COMPLETE",
    "candidate_id": "CAND-R4-0005",
    "R4_mathematical_root": "AEEE9C3AB53239DDD6231A870AEAA88C61881DF4B6D187F4CAA5B0F550549618",
    "R4_operator_contradiction_root": "C1DCA0C5926D15B7689BCEF54AEDEA537B7CF4FE9BCE2692AF97CB594B80995B",
    "selection_rule": {
        "direct_files": list(DIRECT_FILES),
        "recursive_trees": list(TREE_ROOTS),
        "reference_archives": "out/*.zip",
        "directive": str(directive),
    },
    "file_count": len(records),
    "total_bytes": sum(record["bytes"] for record in records),
    "files": records,
    "H_R5_INPUT": input_root,
    "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}

temporary = OUT.with_suffix(".json.tmp")
temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
temporary.replace(OUT)
lines = ["Path\tBytes\tSHA256"] + [f"{row['path']}\t{row['bytes']}\t{row['sha256']}" for row in records]
temporary_tsv = TSV.with_suffix(".tsv.tmp")
temporary_tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
temporary_tsv.replace(TSV)
print(json.dumps({"classification": payload["classification"], "file_count": len(records), "total_bytes": payload["total_bytes"], "H_R5_INPUT": input_root}, indent=2))
