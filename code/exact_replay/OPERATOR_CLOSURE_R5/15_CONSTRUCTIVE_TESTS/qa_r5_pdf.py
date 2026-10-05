from __future__ import annotations

import json
from pathlib import Path

import pdfplumber
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
pdf_path = ROOT / "output" / "pdf" / "R5_OPERATOR_CLOSURE_THEOREM.pdf"
render_dir = ROOT / "tmp" / "pdfs" / "r5_render"
out_path = Path(__file__).resolve().parent / "R5_PDF_QA.json"

page_records = []
all_text = []
outside = 0
minimum_font = None
with pdfplumber.open(pdf_path) as pdf:
    for index, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        all_text.append(text)
        chars = page.chars
        for ch in chars:
            if ch["x0"] < -0.5 or ch["x1"] > page.width + 0.5 or ch["top"] < -0.5 or ch["bottom"] > page.height + 0.5:
                outside += 1
            size = float(ch.get("size", 0))
            if size > 0:
                minimum_font = size if minimum_font is None else min(minimum_font, size)
        page_records.append({
            "page": index,
            "width": float(page.width),
            "height": float(page.height),
            "characters": len(chars),
            "text_characters": len(text),
        })

renders = []
for path in sorted(render_dir.glob("page-*.png")):
    with Image.open(path) as image:
        renders.append({"name": path.name, "width": image.width, "height": image.height})

joined = "\n".join(all_text)
checks = {
    "pdf_exists": pdf_path.is_file(),
    "page_count_9": len(page_records) == 9,
    "all_pages_a4_portrait": all(abs(p["width"] - 595.276) < 1 and abs(p["height"] - 841.89) < 1 for p in page_records),
    "no_characters_outside_media_box": outside == 0,
    "minimum_font_legible": minimum_font is not None and minimum_font >= 6.0,
    "nine_rendered_pages": len(renders) == 9,
    "uniform_render_dimensions": len({(x["width"], x["height"]) for x in renders}) == 1,
    "main_theorem_present": "Theorem R5-D" in joined,
    "ratner_argument_present": "Ratner" in joined,
    "normalizer_present": "normalizer" in joined.lower(),
    "commensurator_present": "commensurator" in joined.lower(),
    "no_replacement_character": "\ufffd" not in joined,
    "no_nul_character": "\x00" not in joined,
}
payload = {
    "schema_version": "1.0",
    "pdf": str(pdf_path),
    "checks": checks,
    "status": "PASS" if all(checks.values()) else "FAIL",
    "minimum_font_points": minimum_font,
    "characters_outside_media_box": outside,
    "pages": page_records,
    "renders": renders,
    "visual_viewer_status": "BLOCKED_BY_WINDOWS_DENY_READ_ACL; quantitative render and character-boundary QA used",
}
out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"status": payload["status"], "checks": sum(checks.values()), "total": len(checks), "minimum_font_points": minimum_font, "outside": outside}))
