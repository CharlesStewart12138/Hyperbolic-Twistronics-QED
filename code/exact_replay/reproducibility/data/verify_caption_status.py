"""Verify that every released figure caption carries its terminal scope qualifier."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEX = ROOT / "source_current_195/main.tex"
REGISTRY = ROOT / "reproducibility/data/figure_data_manifest.json"
OUTPUT = ROOT / "reproducibility/data/caption_status_verification.json"

REQUIRED = {
    "P0-05-R1": ["contains no production spectrum, band gap, or bulk claim"],
    "P0-05-R2": ["makes no hybridized-band claim"],
    "P1-09-Q5": ["not a substitute for the missing coupled spectra"],
    "P0-05-R4": ["establishes reciprocal geometry only", "remain uncomputed"],
    "P0-05-R5": ["does not establish production parameters", "full-bulk flat band"],
    "P0-05-R7": ["not a production parameter", "representation-complete", "full-bulk claim"],
    "P0-05-R9": ["not a production-tower or bulk-convergence result"],
    "P0-05-R12": ["not calibrated multiport measurements", "or bulk ldos"],
}

def balanced_argument(text: str, command_pos: int) -> str:
    start = text.find("{", command_pos)
    if start < 0:
        return ""
    depth = 0
    out: list[str] = []
    for char in text[start:]:
        if char == "{":
            depth += 1
            if depth == 1:
                continue
        elif char == "}":
            depth -= 1
            if depth == 0:
                break
        if depth >= 1:
            out.append(char)
    return "".join(out)

def main() -> int:
    tex = TEX.read_text(encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    figures = registry["figures"]
    entries = []
    for item in figures:
        task = item["task_id"]
        label_token = "\\label{" + item["latex_label"] + "}"
        label_pos = tex.find(label_token)
        begin = tex.rfind("\\begin{figure", 0, label_pos)
        end = tex.find("\\end{figure", label_pos)
        block = tex[begin:end]
        caption = re.sub(r"\s+", " ", balanced_argument(block, block.find("\\caption"))).strip()
        lowered = caption.casefold()
        required = REQUIRED.get(task, [])
        missing = [phrase for phrase in required if phrase.casefold() not in lowered]
        entries.append({
            "task_id": task,
            "latex_label": item["latex_label"],
            "scientific_scope": item["scientific_scope"],
            "required_terminal_qualifiers": required,
            "missing_qualifiers": missing,
            "status": "PASS" if label_pos >= 0 and caption and not missing else "FAIL",
        })
    checks = {
        "eight_registered_captions_found": len(entries) == 8 and all(e["status"] == "PASS" for e in entries),
        "one_scope_per_caption": all(bool(e["scientific_scope"]) for e in entries),
        "all_terminal_qualifiers_present": all(not e["missing_qualifiers"] for e in entries),
    }
    report = {
        "task_id": "P3-20-12",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "caption_count": len(entries),
        "entries": entries,
    }
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
