from pathlib import Path

import pdfplumber


pdf_path = Path(r"D:\work\revise\output\pdf\R5_OPERATOR_CLOSURE_THEOREM.pdf")
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[3]
    chars = page.chars
    print("".join(char.get("text", "") for char in chars[620:760]))
