from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]
PLOT_DATA = OUT / "01_PLOTTING_DATA"
WORKING = OUT / "02_WORKING"
QA_DIR = OUT / "03_QA"
PDF_DIR = OUT / "04_PDF"
SVG_DIR = OUT / "05_SVG"
PNG_DIR = OUT / "06_PNG"
FIG_DATA = OUT / "07_FIGURE_DATA"
SCRIPT_DIR = OUT / "08_SCRIPTS"
CAPTION_DIR = OUT / "09_CAPTIONS"
REPORT_DIR = OUT / "10_REPORTS"

FIGURE_IDS = [f"FIG{i:02d}" for i in range(1, 7)] + [f"FIG{i:02d}" for i in range(11, 45)]

WARM = [
    "#3B2219", "#6F2D1F", "#9E3D2B", "#B85C3B", "#C96A4A",
    "#D47B42", "#E09B3D", "#C28A28", "#E0B04B", "#D97A6C",
]
NEUTRAL = "#5A514C"
LIGHT = "#EFE6DE"
WHITE = "#FFFEFC"
WARM_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "warm_numeric", ["#FFFDF8", "#F5D7B2", "#DB8B55", "#A13F2A", "#4A2118"]
)
DIVERGING = matplotlib.colors.LinearSegmentedColormap.from_list(
    "warm_diverging", ["#60301F", "#D1845C", "#F9F5EE", "#D9A53B", "#6B431D"]
)


def ensure_dirs() -> None:
    for path in (PLOT_DATA, WORKING, QA_DIR, PDF_DIR, SVG_DIR, PNG_DIR, FIG_DATA, SCRIPT_DIR, CAPTION_DIR, REPORT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def configure_matplotlib() -> str:
    from matplotlib import font_manager

    font_path = font_manager.findfont("Times New Roman", fallback_to_default=False)
    plt.rcParams.update({
        "font.family": "Times New Roman",
        "mathtext.fontset": "stix",
        "font.size": 7.1,
        "axes.titlesize": 8.1,
        "axes.labelsize": 7.4,
        "axes.linewidth": 0.55,
        "axes.edgecolor": WARM[0],
        "axes.facecolor": WHITE,
        "figure.facecolor": WHITE,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.minor.width": 0.4,
        "ytick.minor.width": 0.4,
        "legend.frameon": False,
        "legend.fontsize": 6.2,
        "grid.linewidth": 0.4,
        "grid.alpha": 0.18,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.bbox": "tight",
        "savefig.facecolor": WHITE,
    })
    return font_path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path, delimiter: str | None = None) -> list[dict[str, str]]:
    if delimiter is None:
        delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def as_float(value, default=float("nan")) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def make_figure(title: str, nrows: int = 2, ncols: int = 2, figsize=(7.20, 5.30)):
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, layout="constrained")
    axes = np.atleast_1d(axes).ravel()
    fig.suptitle(title, fontsize=9.2, fontweight="bold", color=WARM[0])
    return fig, axes


def panel(ax, letter: str, title: str, xlabel: str, ylabel: str, grid: bool = True) -> None:
    ax.text(-0.13, 1.06, f"({letter})", transform=ax.transAxes, fontsize=8.2,
            fontweight="bold", ha="left", va="bottom", color=WARM[0])
    ax.set_title(title, fontweight="bold", pad=4.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if grid:
        ax.grid(True, color=WARM[0], alpha=0.14, lw=0.4)
    for spine in ax.spines.values():
        spine.set_linewidth(0.55)


def add_zero(ax, axis: str = "y", value: float = 0.0) -> None:
    if axis == "y":
        ax.axhline(value, color=NEUTRAL, lw=0.7, ls="-.", zorder=0)
    else:
        ax.axvline(value, color=NEUTRAL, lw=0.7, ls="-.", zorder=0)


def series_records(panel_id: str, series: str, x: Sequence, y: Sequence,
                   x_name: str, y_name: str, parameter_values: str = "") -> list[dict[str, str]]:
    records = []
    for xv, yv in zip(np.asarray(x).ravel(), np.asarray(y).ravel()):
        records.append({
            "panel": panel_id,
            "series": series,
            "x_variable": x_name,
            "x_value": f"{float(xv):.16g}" if np.isfinite(float(xv)) else str(xv),
            "y_variable": y_name,
            "y_value": f"{float(yv):.16g}" if np.isfinite(float(yv)) else str(yv),
            "parameter_values": parameter_values,
        })
    return records


DATA_HEADERS = ["panel", "series", "x_variable", "x_value", "y_variable", "y_value", "parameter_values"]


def save_long_data(fig_id: str, records: list[dict[str, str]], sources: Sequence[Path],
                   source_type: str, transformations: Sequence[str]) -> tuple[Path, Path]:
    normalized = PLOT_DATA / f"{fig_id}_normalized.csv"
    final_data = FIG_DATA / f"{fig_id}_data.csv"
    for path in (normalized, final_data):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=DATA_HEADERS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(records)
    provenance = {
        "figure_id": fig_id,
        "source_type": source_type,
        "sources": [
            {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(path)}
            for path in sources
        ],
        "selected_columns": sorted({r["x_variable"] for r in records} | {r["y_variable"] for r in records}),
        "filter": "figure-specific deterministic selection documented by series labels",
        "normalization": "as stated in variable names and parameter_values",
        "plot_transformation": list(transformations),
        "interpolation_policy": "DISPLAY ONLY where explicitly labeled; no inferred physics",
        "expensive_algorithm_rerun": False,
    }
    provenance_path = PLOT_DATA / f"{fig_id}_provenance.json"
    provenance_path.write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.copy2(provenance_path, FIG_DATA / f"{fig_id}_provenance.json")
    return final_data, provenance_path


def _axis_has_numeric_content(ax) -> bool:
    return bool(ax.lines or ax.collections or ax.images or ax.patches or ax.containers)


def export_figure(
    fig_id: str,
    fig,
    axes: Sequence,
    title: str,
    panel_descriptions: Sequence[str],
    sources: Sequence[Path],
    source_type: str,
    exactness: str,
    tier: str,
    x_variables: str,
    y_variables: str,
    parameter_values: str,
    observation: str,
    data_path: Path,
    transformations: Sequence[str],
) -> dict[str, str]:
    for index, ax in enumerate(axes):
        if not _axis_has_numeric_content(ax):
            raise RuntimeError(f"{fig_id} axis {index} has no numeric content")
        if not ax.get_title():
            raise RuntimeError(f"{fig_id} axis {index} has no title")
        if not ax.get_xlabel() or not ax.get_ylabel():
            raise RuntimeError(f"{fig_id} axis {index} lacks an axis label")

    stem = f"{fig_id}_{slugify(title)}"
    pdf = PDF_DIR / f"{stem}.pdf"
    svg = SVG_DIR / f"{stem}.svg"
    png = PNG_DIR / f"{stem}.png"
    fig.savefig(pdf)
    fig.savefig(svg)
    fig.savefig(png, dpi=600)
    plt.close(fig)

    caption = (
        f"**{fig_id} | {title}.** "
        + " ".join(f"({chr(97+i)}) {text}" for i, text in enumerate(panel_descriptions))
        + f" Parameters: {parameter_values}. Data provenance: {source_type}; "
          f"solid lines/filled markers denote the principal frozen or exact result, dash-dot lines denote analytic/reference laws, "
          f"dotted lines denote certified bounds or thresholds, and open markers denote controls when present. "
          f"Main numerical observation: {observation}"
    )
    caption_path = CAPTION_DIR / f"{fig_id}_CAPTION.md"
    caption_path.write_text(caption + "\n", encoding="utf-8")
    metadata = {
        "figure_id": fig_id,
        "title": title,
        "panels": len(axes),
        "panel_descriptions": list(panel_descriptions),
        "source_type": source_type,
        "exactness": exactness,
        "tier": tier,
        "x_variables": x_variables,
        "y_variables": y_variables,
        "parameter_values": parameter_values,
        "observation": observation,
        "sources": [
            {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(p)} for p in sources
        ],
        "transformations": list(transformations),
        "paths": {
            "pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
            "svg": str(svg.relative_to(ROOT)).replace("\\", "/"),
            "png": str(png.relative_to(ROOT)).replace("\\", "/"),
            "script": str((SCRIPT_DIR / f"plot_{fig_id.lower()}.py").relative_to(ROOT)).replace("\\", "/"),
            "data": str(data_path.relative_to(ROOT)).replace("\\", "/"),
            "caption": str(caption_path.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    (WORKING / f"{fig_id}_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {
        "Figure ID": fig_id,
        "Title": title,
        "Panels": str(len(axes)),
        "Source dataset": "; ".join(str(p.relative_to(ROOT)).replace("\\", "/") for p in sources),
        "Source hashes": "; ".join(sha256(p) for p in sources),
        "X variables": x_variables,
        "Y variables": y_variables,
        "Parameter values": parameter_values,
        "Analytic/numerical": source_type,
        "Exact/approximate": exactness,
        "Main-text tier": tier,
        "PDF path": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "SVG path": str(svg.relative_to(ROOT)).replace("\\", "/"),
        "PNG path": str(png.relative_to(ROOT)).replace("\\", "/"),
        "Script path": str((SCRIPT_DIR / f"plot_{fig_id.lower()}.py").relative_to(ROOT)).replace("\\", "/"),
        "Data path": str(data_path.relative_to(ROOT)).replace("\\", "/"),
        "Caption path": str(caption_path.relative_to(ROOT)).replace("\\", "/"),
        "QA status": "PENDING_BATCH_QA",
    }


def slugify(value: str) -> str:
    keep = []
    for char in value.lower():
        if char.isalnum():
            keep.append(char)
        elif char in {" ", "-", "/"}:
            keep.append("_")
    slug = "".join(keep)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_")[:80]


def finalize_manifest(entries: Sequence[dict[str, str]], font_path: str) -> Path:
    manifest = {
        "suite_status": "GENERATED_PENDING_QA",
        "figure_count": len(entries),
        "figure_ids": [entry["Figure ID"] for entry in entries],
        "omitted_ids": ["FIG07", "FIG08", "FIG09", "FIG10"],
        "omission_reason": "No complete frozen centered exact arithmetic sequence supports local exponent/scaling plots without fabrication.",
        "schematic_figures": 0,
        "expensive_algorithm_rerun": False,
        "font_path": font_path,
        "entries": list(entries),
    }
    path = WORKING / "NUMERICAL_FIGURE_MANIFEST.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def geometric_derivative(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.gradient(np.log(np.maximum(y, 1e-300)), np.log(np.maximum(x, 1e-300)))


def set_log_ticks(ax) -> None:
    ax.tick_params(which="both", direction="in")

