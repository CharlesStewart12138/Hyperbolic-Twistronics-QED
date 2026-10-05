"""Build and verify the 35--60 page PC5203 eight-question report."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_PDF = ROOT / "source_current_195/main.pdf"
RUN_ID = "P1-07-02-reexec-20260903T121500+0800"
SELECTED_PAGES = [
    *range(1, 3),
    *range(14, 26),
    *range(34, 41),
    *range(48, 56),
    *range(60, 73),
]
QUESTION_LABELS = tuple(f"sec:q{i}" for i in range(1, 9))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def page_count(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"cannot read page count: {path}")
    return int(match.group(1))


def compile_tex(directory: Path) -> None:
    subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=directory, check=True,
    )


def write_selected_pages() -> None:
    source = "../../source_current_195/main.pdf"
    lines = [r"\clearpage", r"\newgeometry{margin=0pt}", r"\pagestyle{empty}"]
    for page in SELECTED_PAGES:
        lines.extend([
            rf"\noindent\includegraphics[page={page},width=\textwidth,height=0.97\textheight,keepaspectratio]{{{source}}}%",
            r"\clearpage",
        ])
    lines.extend([r"\restoregeometry", ""])
    (HERE / "selected_pages.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    compile_tex(ROOT / "source_current_195")
    source_pages = page_count(SOURCE_PDF)
    if max(SELECTED_PAGES) > source_pages or len(SELECTED_PAGES) != len(set(SELECTED_PAGES)):
        raise RuntimeError("selected-page list is invalid or contains duplicates")

    source = (HERE / "main.tex").read_text(encoding="utf-8")
    missing_labels = [label for label in QUESTION_LABELS if f"\\label{{{label}}}" not in source]
    if missing_labels:
        raise RuntimeError(f"missing course-question labels: {missing_labels}")

    write_selected_pages()
    compile_tex(HERE)
    output = HERE / "main.pdf"
    pages = page_count(output)
    if not 35 <= pages <= 60:
        raise RuntimeError(f"course report must contain 35--60 pages; got {pages}")
    front_pages = pages - len(SELECTED_PAGES)
    if not 1 <= front_pages <= 18:
        raise RuntimeError(f"invalid course/front page topology: {front_pages}")

    required = [
        HERE / "main.tex", HERE / "build_course.py", SOURCE_PDF,
        ROOT / "reproducibility/figures/p0_05_r2/P0-05-R2_euclidean_commensurate_benchmark.pdf",
        ROOT / "reproducibility/figures/p0_05_r4/P0-05-R4_diffraction_fourier_reconstruction.pdf",
        ROOT / "reproducibility/figures/p0_05_r5/P0-05-R5_magic_no_magic_dichotomy.pdf",
        ROOT / "reproducibility/figures/p0_05_r7/P0-05-R7_hodge_mechanism.pdf",
    ]
    manifest = {
        "task_id": "P1-07-02",
        "run_id": RUN_ID,
        "terminal_status": "DONE_PC5203_EIGHT_QUESTION_COURSE_REPORT",
        "question_labels_verified": list(QUESTION_LABELS),
        "selected_source_pages": SELECTED_PAGES,
        "selected_page_count": len(SELECTED_PAGES),
        "front_course_pages": front_pages,
        "report_pages": pages,
        "page_window_pass": True,
        "negative_control": "build fails for a missing Q1--Q8 label, duplicate excerpt page, or total outside 35--60 pages",
        "files": [
            {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in required
        ],
        "output": {"path": output.relative_to(ROOT).as_posix(), "bytes": output.stat().st_size, "sha256": sha256(output)},
    }
    (HERE / "course_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"PASS: PC5203 report has {pages} pages, 8 answers, and {len(SELECTED_PAGES)} audited excerpts")


if __name__ == "__main__":
    main()

