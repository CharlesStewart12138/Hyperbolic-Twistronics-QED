"""Mandatory R6 warm publication style and three-format export."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


WARM = ["#3B2417", "#7F351D", "#B14A2A", "#D26A3A", "#E29B49", "#F1C36A", "#FFF1C1"]
WARM_CMAP = LinearSegmentedColormap.from_list("r6_warm", WARM)
SIGNED_CMAP = LinearSegmentedColormap.from_list("r6_signed", ["#5B4037", "#F6E9D7", "#A33A25"])


def configure_style() -> None:
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.linewidth": 0.65,
        "lines.linewidth": 1.05,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "savefig.bbox": "tight",
        "figure.dpi": 140,
    })


def export_figure(fig, directory: Path, figure_id: str, metadata: dict[str, object]) -> dict[str, str]:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for suffix, options in (("pdf", {}), ("svg", {}), ("png", {"dpi": 600})):
        path = directory / f"{figure_id}.{suffix}"
        fig.savefig(path, **options)
        outputs[suffix] = str(path)
    (directory / f"{figure_id}.manifest.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    plt.close(fig)
    return outputs


configure_style()

