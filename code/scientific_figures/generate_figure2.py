"""Reproducible scientific Figure 2 from frozen R4/R5 results.

Inputs:
  data/figure2/FROZEN_R4_R5_FIGURE_DATA.json
  data/figure2/THETA_C_VISUALIZATION_SAMPLE.tsv

No image synthesis or manual digitization is used. Panels are plotted from
certified values, an existing arithmetic-angle sample, and explicit formulas.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "figure2"
FIG = ROOT / "figures"
STEM = FIG / "figure2_finite_without_generic_periodicity"

# Warm, low-saturation palette used by the preceding production figures.
INK = "#3A2B25"
MUTED = "#6F625B"
GRID = "#DED8D2"
PAPER = "#FFFFFF"
RUST = "#9D4E2F"
COPPER = "#B8733A"
OCHRE = "#C28A4A"
UMBER = "#72513E"
SAND = "#D3AA7B"


def load_inputs():
    frozen = json.loads(
        (DATA / "FROZEN_R4_R5_FIGURE_DATA.json").read_text(encoding="utf-8")
    )
    with (DATA / "THETA_C_VISUALIZATION_SAMPLE.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        theta_c_sample = np.array(
            [
                float(row["theta_radians"])
                for row in csv.DictReader(handle, delimiter="\t")
            ],
            dtype=float,
        )
    return frozen, theta_c_sample


def configure_style():
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "Nimbus Roman"],
            "mathtext.fontset": "stix",
            "text.usetex": False,
            "font.size": 8.2,
            "axes.titlesize": 9.0,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.2,
            "ytick.labelsize": 7.2,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "axes.titleweight": "normal",
            "axes.spines.top": True,
            "axes.spines.right": True,
            "axes.linewidth": 0.55,
            "grid.linewidth": 0.35,
            "grid.alpha": 0.50,
            "lines.linewidth": 0.85,
            "patch.linewidth": 0.55,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def title(ax, letter, label):
    ax.set_title(label, loc="center", pad=6)
    ax.text(
        0.018,
        0.965,
        f"({letter})",
        transform=ax.transAxes,
        fontsize=8.8,
        fontweight="bold",
        va="top",
        ha="left",
        zorder=10,
    )


def panel_a(ax, frozen):
    q = frozen["quotient"]
    labels = [r"$\mu(Q_*)$", r"$\mu_{\rm tr}(Q_*)$", r"$|Q_*|$"]
    values = np.array([q["mu"], q["mu_tr"], q["order"]], dtype=float)
    colors = [SAND, COPPER, RUST]
    y = np.arange(3)
    title(ax, "a", "Certified boundaryless quotient")
    ax.set_xscale("log")
    ax.set_xlim(10, 100000)
    ax.set_ylim(-0.65, 2.7)
    ax.set_yticks(y, labels)
    ax.grid(axis="x", which="major", color=GRID, linestyle="-", zorder=0)
    for yi, value, color in zip(y, values, colors):
        ax.hlines(yi, 10, value, color=color, linewidth=0.9,
                  linestyle="dashdot", zorder=2)
        ax.plot(value, yi, marker="*", markersize=7.0, color=color,
                markeredgecolor=INK, markeredgewidth=0.30, linestyle="none", zorder=3)
        ax.annotate(
            f"{int(value):,}",
            (value, yi),
            xytext=(-5 if value > 20000 else 6, 0),
            textcoords="offset points",
            ha="right" if value > 20000 else "left",
            va="center",
            color=color,
            fontsize=7.1,
        )
    ax.set_xlabel("permutation or quotient degree")
    ax.text(
        0.12,
        0.96,
        r"$\mathrm{sys}/a_B>6$",
        transform=ax.transAxes,
        va="top",
        ha="left",
        color=RUST,
        fontsize=7.4,
    )
    ax.text(
        0.98,
        0.96,
        r"$C_8$  |  parity  |  physical shell",
        transform=ax.transAxes,
        va="top",
        ha="right",
        color=UMBER,
        fontsize=6.4,
    )


def panel_b(ax, frozen, theta_c_sample):
    theta = frozen["theta"]
    theta_max = theta["theta_max"]
    x = theta_c_sample / theta_max
    title(ax, "b", "Exact centered-angle classification")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.55, 2.55)
    ax.set_yticks(
        [2, 1, 0],
        [r"$\Theta_N=\Theta_{\rm cov}$", r"$\Theta_C$", r"$\Theta_G=I\setminus\Theta_C$"],
    )
    ax.set_xticks([0, 0.5, 1], ["0", r"$1/2$", "1"])
    ax.set_xlabel(r"normalized angle $\theta/(\pi/8)$")
    ax.grid(axis="x", color=GRID, linestyle="-", zorder=0)
    ax.hlines([2, 1, 0], 0, 1, color=[RUST, COPPER, UMBER],
              linewidth=0.65, linestyle="dashdot", alpha=0.72, zorder=1)
    ax.plot([0], [2], marker="*", markersize=7.5, color=RUST,
            markeredgecolor=INK, markeredgewidth=0.3, linestyle="none", zorder=4)
    ax.text(0.075, 2.15, "same cover only", color=RUST,
            fontsize=6.4, fontstyle="italic")
    ax.plot(x, np.full_like(x, 1.0), linestyle="none", marker="|",
            markersize=3.2, markeredgewidth=0.38, color=COPPER,
            alpha=0.70, rasterized=True, zorder=2,
            label=r"stored $\Theta_C$ sample")
    xc = theta["theta_c"] / theta_max
    ax.plot([xc], [1], marker="*", markersize=8.0, color=RUST,
            markeredgecolor=INK, markeredgewidth=0.3, linestyle="none", zorder=5)
    ax.annotate(
        r"$\theta_c$",
        (xc, 1),
        xytext=(-2, 9),
        textcoords="offset points",
        ha="center",
        color=RUST,
    )
    ax.text(0.5, -0.02, "dense and conull", ha="center", va="center",
            color=UMBER, fontsize=6.3, fontstyle="italic",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.3))
    ax.text(
        0.98,
        0.95,
        r"$\Theta_C:\ \tan(\theta/2)\in\mathbb{Q}(\sqrt{2})$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.6,
        color=UMBER,
    )
    ax.text(
        0.02,
        0.05,
        f"{len(theta_c_sample)} stored arithmetic angles shown",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=5.9,
        color=MUTED,
    )


def panel_c(ax, frozen):
    q = frozen["quotient"]
    cc = frozen["common_cover"]
    dims = [q["same_q_bilayer_dimension"], cc["hilbert_dimension"]]
    x = np.arange(2)
    title(ax, "c", "Cost of a nontrivial exact twist")
    bars = ax.bar(x, dims, width=0.52, color=[SAND, COPPER],
                  edgecolor=INK, linewidth=0.55, zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(1e4, 1e8)
    ax.set_xticks(x, ["same $Q_*$", "common cover"])
    ax.set_ylabel("Hilbert dimension")
    ax.grid(axis="y", which="major", color=GRID, linestyle="-", zorder=0)
    ax.axhline(dims[0], color=UMBER, linestyle="dashdot", linewidth=0.70, zorder=2)
    for index, (bar, value, color) in enumerate(zip(bars, dims, [UMBER, RUST])):
        ax.annotate(
            f"{value:,}",
            (bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, -13 if index == 1 else 5),
            textcoords="offset points",
            ha="center",
            va="top" if index == 1 else "bottom",
            color="white" if index == 1 else color,
            fontsize=7.0,
        )
    ax.annotate(
        rf"$m_{{\theta_c}}={cc['index']}$  ($\times {cc['index']}$)",
        xy=(1, dims[1] * 0.92),
        xytext=(0.43, 0.92),
        textcoords="axes fraction",
        ha="left",
        va="top",
        color=RUST,
        arrowprops=dict(arrowstyle="-|>", color=RUST, lw=0.65,
                        linestyle="dashdot"),
    )
    ax.text(
        0.5,
        -0.16,
        r"$\theta_c=2\arctan[(4+\sqrt{2})^{-1}]$",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.5,
        color=MUTED,
        clip_on=False,
    )


def panel_d(ax, frozen, theta_c_sample):
    """Plot certified common-cover samples against an exact generic family.

    t_j = j/5000 + pi/10^6 is transcendental for every integer j. Therefore
    t_j is not in Q(sqrt(2)), and theta_j = 2 arctan(t_j) is outside Theta_C.
    """
    theta_max = frozen["theta"]["theta_max"]
    j = np.arange(1, 995, 5, dtype=float)
    t_generic = j / 5000.0 + np.pi / 1_000_000.0
    if np.max(t_generic) >= math.tan(math.pi / 16):
        raise ValueError("Explicit generic family left the reduced interval")
    theta_generic = 2.0 * np.arctan(t_generic)
    x_generic = theta_generic / theta_max
    x_comm = theta_c_sample[::4] / theta_max

    title(ax, "d", "Generic angle: no finite common cover")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.55, 1.55)
    ax.set_xticks([0, 0.5, 1], ["0", r"$1/2$", "1"])
    ax.set_yticks([1, 0], ["finite common cover", "no finite common cover"])
    ax.set_xlabel(r"normalized angle $\theta/(\pi/8)$")
    ax.grid(axis="x", color=GRID, linestyle="-", zorder=0)
    ax.hlines([1, 0], 0, 1, color=[COPPER, RUST], linewidth=0.70,
              linestyle="dashdot", alpha=0.76, zorder=1)
    ax.plot(x_comm, np.ones_like(x_comm), linestyle="none", marker="|",
            markersize=3.8, markeredgewidth=0.42, color=COPPER, alpha=0.75,
            label=r"$\tan(\theta/2)\in\mathbb{Q}(\sqrt{2})$", zorder=2)
    ax.plot(x_generic, np.zeros_like(x_generic), linestyle="none", marker="x",
            markersize=3.0, markeredgewidth=0.48, color=RUST,
            label=r"$t_j=j/5000+\pi/10^6$", zorder=3)
    ax.legend(
        loc="center right",
        frameon=False,
        fontsize=5.8,
        handletextpad=0.35,
        borderaxespad=0.3,
    )
    ax.text(
        0.02,
        0.47,
        r"$t_j\notin\mathbb{Q}(\sqrt{2})$ exactly",
        transform=ax.transAxes,
        ha="left",
        va="center",
        color=RUST,
        fontsize=6.2,
    )
    ax.text(
        0.5,
        0.04,
        r"$\theta\notin\Theta_C\Rightarrow\overline{K r_\theta K}=G$",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=6.6,
        color=INK,
    )


def main():
    configure_style()
    frozen, theta_c_sample = load_inputs()
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.55), constrained_layout=False)
    fig.suptitle("Finite Hyperbolic Realization without Generic Periodicity",
                 fontsize=11.0, fontweight="normal", y=0.982)
    fig.subplots_adjust(
        left=0.095,
        right=0.985,
        bottom=0.12,
        top=0.90,
        wspace=0.60,
        hspace=0.48,
    )
    panel_a(axes[0, 0], frozen)
    panel_b(axes[0, 1], frozen, theta_c_sample)
    panel_c(axes[1, 0], frozen)
    panel_d(axes[1, 1], frozen, theta_c_sample)
    for ax in axes.flat:
        ax.tick_params(direction="in", top=True, right=True, length=3.0, width=0.50)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.55)
            spine.set_color(INK)
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        STEM.with_suffix(".pdf"),
        bbox_inches="tight",
        facecolor="white",
        transparent=False,
        metadata={
            "Title": "Finite hyperbolic realization without generic periodicity",
            "Author": "5203 project",
            "Subject": "R4/R5 certified data and exact angle formulas",
        },
    )
    fig.savefig(STEM.with_suffix(".svg"), bbox_inches="tight",
                facecolor="white", transparent=False)
    fig.savefig(STEM.with_suffix(".png"), dpi=450, bbox_inches="tight",
                facecolor="white", transparent=False)
    plt.close(fig)
    print(STEM.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
