from pathlib import Path

import pdfplumber


pdf_path = Path(r"D:\work\revise\output\pdf\R5_OPERATOR_CLOSURE_THEOREM.pdf")
records = []
with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        for index, char in enumerate(page.chars):
            size = float(char.get("size", 0.0))
            if 0.0 < size < 6.1:
                records.append(
                    {
                        "page": page_number,
                        "index": index,
                        "text": char.get("text"),
                        "fontname": char.get("fontname"),
                        "size": size,
                        "x0": char.get("x0"),
                        "top": char.get("top"),
                    }
                )

print(f"count={len(records)}")
for record in records[:80]:
    print(record)
