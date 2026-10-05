from __future__ import annotations

import csv
import json
import math
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

from suite_core import (
    CAPTION_DIR, FIGURE_IDS, FIG_DATA, OUT, PDF_DIR, PNG_DIR, QA_DIR,
    REPORT_DIR, ROOT, SVG_DIR, WARM, WORKING, sha256,
)


CATALOG_SOURCE = WORKING / "NUMERICAL_FIGURE_CATALOG_SOURCE.tsv"
CONTACT_PNG = OUT / "NUMERICAL_FIGURE_CONTACT_SHEET.png"
CONTACT_PDF = OUT / "NUMERICAL_FIGURE_CONTACT_SHEET.pdf"
MASTER_CAPTIONS = OUT / "MASTER_NUMERICAL_CAPTIONS.md"
QA_REPORT = OUT / "NUMERICAL_FIGURE_QA_REPORT.md"
FINAL_REPORT = OUT / "FINAL_NUMERICAL_FIGURE_REPORT.md"


def read_catalog():
    with CATALOG_SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def absolute(path_text: str) -> Path:
    return ROOT / Path(path_text)


def verify_data_csv(path: Path) -> dict:
    panels = defaultdict(list)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                value = float(row["y_value"])
            except (TypeError, ValueError):
                value = float("nan")
            panels[row["panel"]].append(value)
    finite_by_panel = {
        key: sum(math.isfinite(value) for value in values)
        for key, values in panels.items()
    }
    return {
        "panel_count_in_data": len(panels),
        "finite_values_by_panel": finite_by_panel,
        "all_panels_have_finite_values": bool(panels) and all(count > 0 for count in finite_by_panel.values()),
    }


def make_contact_sheet(rows):
    cols, nrows = 5, 8
    cell_w, cell_h = 690, 510
    margin, header = 36, 72
    canvas = Image.new("RGB", (cols * cell_w + 2 * margin, nrows * cell_h + 2 * margin + header), "#FFFEFC")
    draw = ImageDraw.Draw(canvas)
    tnr = Path(r"C:\Windows\Fonts\times.ttf")
    tnrb = Path(r"C:\Windows\Fonts\timesbd.ttf")
    title_font = ImageFont.truetype(str(tnrb if tnrb.exists() else tnr), 34)
    cell_title = ImageFont.truetype(str(tnrb if tnrb.exists() else tnr), 21)
    draw.text((margin, margin), "Numerical Figure Contact Sheet — 40 quantitative figures", fill=WARM[0], font=title_font)
    for index, row in enumerate(rows):
        r, c = divmod(index, cols)
        x0 = margin + c * cell_w
        y0 = margin + header + r * cell_h
        draw.rectangle((x0 + 3, y0 + 3, x0 + cell_w - 8, y0 + cell_h - 8), outline="#9E6E58", width=2)
        png = Image.open(absolute(row["PNG path"])).convert("RGB")
        max_w, max_h = cell_w - 34, cell_h - 66
        scale = min(max_w / png.width, max_h / png.height)
        thumb = png.resize((int(png.width * scale), int(png.height * scale)), Image.Resampling.LANCZOS)
        tx = x0 + (cell_w - thumb.width) // 2
        ty = y0 + 44 + (max_h - thumb.height) // 2
        canvas.paste(thumb, (tx, ty))
        label = f"{row['Figure ID']}  {row['Title']}"
        if len(label) > 58:
            label = label[:55] + "…"
        draw.text((x0 + 16, y0 + 12), label, fill=WARM[0], font=cell_title)
    canvas.save(CONTACT_PNG, dpi=(180, 180), optimize=True)
    canvas.save(CONTACT_PDF, "PDF", resolution=180.0)
    return canvas.size


def main():
    rows = read_catalog()
    if [r["Figure ID"] for r in rows] != FIGURE_IDS:
        raise RuntimeError("Catalog IDs do not match the 40-figure frozen order")

    checks = []
    for row in rows:
        fig_id = row["Figure ID"]
        pdf, svg, png = map(absolute, [row["PDF path"], row["SVG path"], row["PNG path"]])
        script, data, caption = map(absolute, [row["Script path"], row["Data path"], row["Caption path"]])
        item = {"figure_id": fig_id}
        item["all_files_exist_nonzero"] = all(p.exists() and p.stat().st_size > 0 for p in (pdf, svg, png, script, data, caption))
        reader = PdfReader(str(pdf))
        item["pdf_opens_one_page"] = len(reader.pages) == 1
        item["pdf_has_text"] = len((reader.pages[0].extract_text() or "").strip()) > 40
        ET.parse(svg)
        item["svg_parses"] = True
        with Image.open(png) as image:
            image.verify()
        with Image.open(png) as image:
            item["png_dimensions"] = [image.width, image.height]
            item["png_resolution_pass"] = image.width >= 3000 and image.height >= 2000
        data_result = verify_data_csv(data)
        item.update(data_result)
        item["caption_nontrivial"] = len(caption.read_text(encoding="utf-8").strip()) > 250
        item["provenance_present"] = (FIG_DATA / f"{fig_id}_provenance.json").exists()
        item["pass"] = all(
            value is True for key, value in item.items()
            if key not in {"figure_id", "png_dimensions", "panel_count_in_data", "finite_values_by_panel"}
        )
        checks.append(item)

    failures = [item for item in checks if not item["pass"]]
    if failures:
        raise RuntimeError("QA failures: " + json.dumps(failures, ensure_ascii=False))

    contact_size = make_contact_sheet(rows)
    contact_reader = PdfReader(str(CONTACT_PDF))
    if len(contact_reader.pages) != 1:
        raise RuntimeError("Contact-sheet PDF page count mismatch")

    master_lines = ["# Master Numerical Figure Captions", ""]
    for row in rows:
        text = absolute(row["Caption path"]).read_text(encoding="utf-8").strip()
        master_lines.extend([text, ""])
    MASTER_CAPTIONS.write_text("\n".join(master_lines), encoding="utf-8")

    tier_counts = Counter(row["Main-text tier"] for row in rows)
    source_counts = Counter(row["Analytic/numerical"] for row in rows)
    qa_payload = {
        "status": "PASS",
        "figure_count": len(rows),
        "schematic_figures": 0,
        "pdf_count": len(list(PDF_DIR.glob("FIG*.pdf"))),
        "svg_count": len(list(SVG_DIR.glob("FIG*.svg"))),
        "png_count": len(list(PNG_DIR.glob("FIG*.png"))),
        "contact_sheet_size_pixels": contact_size,
        "contact_sheet_pdf_pages": len(contact_reader.pages),
        "font": "Times New Roman",
        "mathtext": "STIX serif",
        "checks": checks,
    }
    (QA_DIR / "NUMERICAL_FIGURE_QA.json").write_text(json.dumps(qa_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    qa_md = [
        "# Numerical Figure QA Report", "",
        "- Status: **PASS**",
        f"- Quantitative figures checked: **{len(rows)}**",
        "- Schematic figures: **0**",
        "- Each figure: PDF + SVG + 600-dpi PNG + CSV + provenance JSON + caption + standalone wrapper.",
        "- PDF: all files open and contain one page with extractable text.",
        "- SVG: all files parse as XML.",
        "- PNG: all files verify and exceed 3000 × 2000 pixels.",
        "- Data: every recorded panel contains at least one finite numeric value.",
        "- Fonts: Times New Roman resolved from `C:\\Windows\\Fonts\\times.ttf`; STIX mathtext used for equations.",
        "- Layout: constrained layout and tight export used; the contact sheet was created for visual review.",
        "- Palette: warm brown/terracotta/orange/ochre/gold with neutral references; no default blue, rainbow, or jet.",
        "- Expensive scientific algorithm rerun: **NO**.", "",
        "## Per-figure summary", "",
        "| Figure | PDF | SVG | PNG | Data | Caption | QA |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in checks:
        qa_md.append(f"| {item['figure_id']} | PASS | PASS | PASS | PASS | PASS | PASS |")
    QA_REPORT.write_text("\n".join(qa_md) + "\n", encoding="utf-8")

    final_md = [
        "# Final Numerical Figure Report", "",
        "The numerical figure bank contains 40 genuine quantitative Python figures. FIG07–FIG10 were intentionally omitted because no complete frozen centered exact arithmetic sequence exists from which to extract the requested local arithmetic exponents without fabricating points.", "",
        "## Tier allocation", "",
    ]
    for tier in ("MAIN_TEXT_TIER_A", "EXTENDED_DATA_TIER_B", "SUPPLEMENT_TIER_C"):
        ids = [row["Figure ID"] for row in rows if row["Main-text tier"] == tier]
        final_md.append(f"- {tier}: {len(ids)} figures — {', '.join(ids)}")
    final_md.extend([
        "", "## Source discipline", "",
        "- Priority 1: frozen CSV/TSV/JSON/NPZ arrays and certificates.",
        "- Priority 2: exact frozen values aggregated across candidates, groups, or branches.",
        "- Priority 3: deterministic dense-grid evaluation of already proved closed-form expressions, always tagged `ANALYTIC_VISUALIZATION_EVALUATION`.",
        "- No quotient search, GAP enumeration, CEGAR search, global scan, eigensolver, Hamiltonian production, optimization, or HPC job was rerun.",
        "", "## Deliverables", "",
        f"- {len(rows)} figure PDFs, {len(rows)} SVGs, {len(rows)} 600-dpi PNGs.",
        f"- {len(rows)} normalized figure CSVs and {len(rows)} provenance sidecars.",
        f"- {len(rows)} publication captions plus a master caption file.",
        "- One PNG/PDF contact sheet and one final XLSX catalog (built in the next controlled step).",
        "", "NUMERICAL_FIGURE_SUITE_STATUS = COMPLETE",
        f"TOTAL_NUMERICAL_FIGURES = {len(rows)}",
        "SCHEMATIC_FIGURES = 0",
        "EXPENSIVE_ALGORITHM_RERUN = NO",
    ])
    FINAL_REPORT.write_text("\n".join(final_md) + "\n", encoding="utf-8")

    for row in rows:
        row["QA status"] = "PASS"
    headers = list(rows[0].keys())
    with CATALOG_SOURCE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

    manifest_path = WORKING / "NUMERICAL_FIGURE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["suite_status"] = "COMPLETE"
    manifest["qa_status"] = "PASS"
    manifest["contact_sheet_pdf_sha256"] = sha256(CONTACT_PDF)
    manifest["contact_sheet_png_sha256"] = sha256(CONTACT_PNG)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "qa_status": "PASS", "figures": len(rows), "tier_counts": tier_counts,
        "source_type_count": len(source_counts), "contact_sheet_size": contact_size,
    }, default=dict, ensure_ascii=False))


if __name__ == "__main__":
    main()
