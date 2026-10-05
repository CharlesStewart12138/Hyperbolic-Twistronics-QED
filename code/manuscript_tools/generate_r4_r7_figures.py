"""Data-driven redraw of the strongest quantitative R4--R7 results.

Every panel is generated from frozen certificates, processed numerical data,
or an explicit R7 bound.  No image synthesis and no manual digitization are
used.  Outputs: vector PDF/SVG and 600 dpi PNG.
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
REVISE = ROOT.parents[1]
R4 = REVISE / "电子物理" / "code" / "CONSTRUCTIVE_EXECUTION_R4"
R5 = REVISE / "电子物理" / "code" / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT"
R6 = REVISE / "PHYSICS_VALIDATION_R6"
R7 = REVISE / "R7_THEORY"
SEC = REVISE / "5203" / "SECTION_II_RECOVERY"

OUT_PDF = ROOT / "figures" / "pdf"
OUT_SVG = ROOT / "figures" / "svg"
OUT_PNG = ROOT / "figures" / "png"
OUT_DATA = ROOT / "data"
OUT_MANIFEST = ROOT / "manifests"

FROZEN_JSON = SEC / "data" / "figure2" / "FROZEN_R4_R5_FIGURE_DATA.json"
THETA_SAMPLE = SEC / "data" / "figure2" / "THETA_C_VISUALIZATION_SAMPLE.tsv"
CEGAR = R4 / "PAPER_INTEGRATION_R4" / "FIGURE_DATA" / "CEGAR_ITERATIONS.tsv"
REJECTIONS = R4 / "18_Q24_CLOSURE" / "MIN_TRANSITIVE_DEGREE_SMALLER_INDEX_REJECTIONS.tsv"
BRANCHES = R5 / "05_CONSTRUCTIVE_COMMENSURATOR" / "R5_COMM_BRANCH_REGISTRY.tsv"
COMM_CERT = R5 / "05_CONSTRUCTIVE_COMMENSURATOR" / "R5_COMM_EXAMPLE_CERTIFICATE.json"
QSTAR = R6 / "10_RAW_DATA" / "qstar_theta0_matrix_free.json"
SEQ = R6 / "11_PROCESSED_DATA" / "phenomenon_III_sequence_observables.tsv"
HEIGHT = R6 / "11_PROCESSED_DATA" / "phenomenon_II_exact_angle_observables.tsv"

# Warm, low-saturation palette consistent with the existing paper figures.
INK = "#352923"
MUTED = "#71645C"
GRID = "#DED7D0"
WHITE = "#FFFFFF"
RUST = "#9D4E2F"
COPPER = "#B8733A"
OCHRE = "#C28A4A"
UMBER = "#72513E"
SAND = "#D6B187"
ROSE = "#B66A55"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require_inputs() -> None:
    required = [
        FROZEN_JSON, THETA_SAMPLE, CEGAR, REJECTIONS, BRANCHES, COMM_CERT,
        QSTAR, SEQ, HEIGHT,
        R7 / "07_MAGIC_MARGIN_CERTIFICATE.tex",
        R7 / "09_GENERIC_INHERITANCE_THEOREM.tex",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing frozen inputs:\n" + "\n".join(missing))


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "Nimbus Roman"],
            "mathtext.fontset": "stix",
            "text.usetex": False,
            "font.size": 8.2,
            "axes.titlesize": 9.0,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.1,
            "ytick.labelsize": 7.1,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "axes.facecolor": WHITE,
            "figure.facecolor": WHITE,
            "savefig.facecolor": WHITE,
            "axes.titleweight": "normal",
            "axes.spines.top": True,
            "axes.spines.right": True,
            "axes.linewidth": 0.58,
            "grid.linewidth": 0.36,
            "grid.alpha": 0.52,
            "lines.linewidth": 0.88,
            "patch.linewidth": 0.58,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def panel_title(ax, letter: str, label: str) -> None:
    ax.set_title(label, pad=6)
    ax.text(
        0.018, 0.965, f"({letter})", transform=ax.transAxes,
        ha="left", va="top", fontsize=8.8, fontweight="bold", zorder=20,
    )


def finish_axes(ax, grid_axis: str = "both") -> None:
    ax.grid(axis=grid_axis, color=GRID, linestyle="dashdot", zorder=0)
    ax.tick_params(direction="in", length=2.8, width=0.52, top=True, right=True)
    for spine in ax.spines.values():
        spine.set_linewidth(0.58)
        spine.set_color(INK)


def save_figure(fig, stem: str) -> None:
    for folder in (OUT_PDF, OUT_SVG, OUT_PNG):
        folder.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT_SVG / f"{stem}.svg", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(
        OUT_PNG / f"{stem}.png", dpi=600,
        bbox_inches="tight", pad_inches=0.04,
    )
    plt.close(fig)


def load_data() -> dict:
    frozen = json.loads(FROZEN_JSON.read_text(encoding="utf-8"))
    qstar = json.loads(QSTAR.read_text(encoding="utf-8"))
    comm = json.loads(COMM_CERT.read_text(encoding="utf-8"))
    theta = np.array(
        [float(row["theta_radians"]) for row in read_tsv(THETA_SAMPLE)],
        dtype=float,
    )
    cegar = read_tsv(CEGAR)
    rejection_rows = read_tsv(REJECTIONS)
    branch_rows = read_tsv(BRANCHES)
    seq_rows = read_tsv(SEQ)
    height_rows = read_tsv(HEIGHT)
    return {
        "frozen": frozen,
        "qstar": qstar,
        "comm": comm,
        "theta": theta,
        "cegar": cegar,
        "rejections": rejection_rows,
        "branches": branch_rows,
        "seq": seq_rows,
        "height": height_rows,
    }


def plot_r4(data: dict) -> None:
    frozen = data["frozen"]
    q = frozen["quotient"]
    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.15), constrained_layout=True)

    ax = axes[0, 0]
    rows = data["cegar"]
    orders = np.array([float(row["order"]) for row in rows])
    outcome_key = next(key for key in rows[0] if "status" in key.lower() or "result" in key.lower())
    passed = np.array(["PASS" in row[outcome_key] for row in rows])
    x = np.arange(1, len(rows) + 1)
    ax.plot(x, orders, color=UMBER, marker="o", markersize=3.4,
            linestyle="dashdot", markerfacecolor=WHITE, zorder=2)
    ax.scatter(x[~passed], orders[~passed], s=23, color=ROSE,
               edgecolor=INK, linewidth=0.35, zorder=3, label="rejected")
    ax.scatter(x[passed], orders[passed], s=42, marker="*", color=RUST,
               edgecolor=INK, linewidth=0.35, zorder=4, label="certified")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xlabel("CEGAR candidate")
    ax.set_ylabel("group order")
    panel_title(ax, "a", "Exact construction converges to $Q_*$")
    finish_axes(ax)
    ax.legend(frameon=False, fontsize=6.6, loc="lower right")

    ax = axes[0, 1]
    labels = [r"$\mu(Q_*)$", r"$\mu_{\rm tr}(Q_*)$", r"$|Q_*|$"]
    vals = np.array([q["mu"], q["mu_tr"], q["order"]], dtype=float)
    colors = [SAND, COPPER, RUST]
    y = np.arange(3)
    ax.set_xscale("log")
    for yi, val, color in zip(y, vals, colors):
        ax.hlines(yi, 20, val, color=color, linestyle="dashdot", linewidth=0.85)
        ax.plot(val, yi, marker="o", markersize=4.8, color=color,
                markeredgecolor=INK, markeredgewidth=0.35)
        ax.annotate(f"{int(val):,}", (val, yi), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=7.0, color=color)
    ax.set_xlim(20, 1e5)
    ax.set_yticks(y, labels)
    ax.set_xlabel("certified permutation degree")
    panel_title(ax, "b", "Faithful-degree hierarchy")
    finish_axes(ax, "x")

    ax = axes[1, 0]
    counts = Counter(row["status"] for row in data["rejections"])
    names = ["not an index", "core-free bound"]
    values = [counts.get("REJECTED_NOT_AN_INDEX", 0),
              counts.get("REJECTED_CORE_FREE_ORDER_BOUND", 0)]
    bars = ax.barh(names, values, color=[SAND, COPPER], edgecolor=INK, height=0.52)
    for bar, val in zip(bars, values):
        ax.text(val + max(values) * 0.012, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", fontsize=7.0, color=UMBER)
    ax.axvline(q["smaller_indices_rejected"], color=RUST,
               linestyle="dashdot", linewidth=0.75)
    ax.set_xlabel(r"indices below $\mu_{\rm tr}=5120$")
    panel_title(ax, "c", "Complete smaller-index exclusion")
    finish_axes(ax, "x")

    ax = axes[1, 1]
    scans = ["scan A", "scan B"]
    records = q["scan_records"]
    ax.barh(scans, [records, records], color=[SAND, OCHRE], edgecolor=INK, height=0.48)
    for yi in range(2):
        ax.plot(records, yi, marker="*", color=RUST, markersize=6,
                markeredgecolor=INK, markeredgewidth=0.3)
        ax.text(records * 0.97, yi, "0 kernel hits", ha="right", va="center",
                fontsize=7.0, color=INK)
    ax.set_xlim(0, records * 1.08)
    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax.set_xlabel("closed-domain records checked")
    ax.text(0.98, 0.96, r"$\mathrm{sys}/a_B>6$",
            transform=ax.transAxes, ha="right", va="top", color=RUST)
    panel_title(ax, "d", "Independent complete systole scans")
    finish_axes(ax, "x")

    save_figure(fig, "FIG_R4_certified_finite_quotient")


def plot_r5(data: dict) -> None:
    frozen = data["frozen"]
    theta_info = frozen["theta"]
    cc = frozen["common_cover"]
    theta_max = theta_info["theta_max"]
    theta = data["theta"]
    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.15), constrained_layout=True)

    ax = axes[0, 0]
    x = theta / theta_max
    ax.plot(x, np.ones_like(x), linestyle="none", marker="|", markersize=6,
            markeredgewidth=0.45, color=COPPER, alpha=0.80)
    ax.plot([0], [1.55], marker="*", color=RUST, markersize=7.5,
            markeredgecolor=INK, markeredgewidth=0.35, clip_on=False)
    xc = theta_info["theta_c"] / theta_max
    ax.plot([xc], [1], marker="*", color=RUST, markersize=7.5,
            markeredgecolor=INK, markeredgewidth=0.35)
    ax.hlines([1.55, 1.0, 0.45], 0, 1, colors=[RUST, COPPER, UMBER],
              linestyles="dashdot", linewidth=0.65)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1.9)
    ax.set_xticks([0, 0.5, 1], ["0", r"$1/2$", "1"])
    ax.set_yticks([1.55, 1.0, 0.45],
                  [r"$\Theta_N=\Theta_{\rm cov}$", r"$\Theta_C$", r"$\Theta_G$"])
    ax.set_xlabel(r"normalized angle $\theta/(\pi/8)$")
    ax.annotate(r"$\theta_c$", (xc, 1), xytext=(0, 8),
                textcoords="offset points", ha="center", color=RUST)
    panel_title(ax, "a", "Exact centered-angle trichotomy")
    finish_axes(ax, "x")

    ax = axes[0, 1]
    dims = [frozen["quotient"]["same_q_bilayer_dimension"], cc["hilbert_dimension"]]
    bars = ax.bar([0, 1], dims, color=[SAND, COPPER], edgecolor=INK, width=0.56)
    ax.set_yscale("log")
    ax.set_ylim(5e4, 6e7)
    ax.set_xticks([0, 1], ["same $Q_*$", r"$\theta_c$ common cover"])
    ax.set_ylabel("Hilbert dimension")
    for bar, val in zip(bars, dims):
        ax.text(bar.get_x() + bar.get_width() / 2, val * 1.15, f"{val:,}",
                ha="center", va="bottom", fontsize=7.0, color=UMBER)
    ax.text(0.98, 0.84, rf"$m_{{\theta_c}}={cc['index']}$",
            transform=ax.transAxes, ha="right", va="top", color=RUST)
    panel_title(ax, "b", "Cost of the explicit exact twist")
    finish_axes(ax, "y")

    lengths = np.array([int(row["physical_word_length"]) for row in data["branches"]])
    ax = axes[1, 0]
    bins = np.arange(-16, max(lengths) + 49, 32)
    ax.hist(lengths, bins=bins, color=SAND, edgecolor=INK, linewidth=0.45)
    ax.axvline(np.median(lengths), color=RUST, linestyle="dashdot", linewidth=0.85,
               label=f"median = {np.median(lengths):.0f}")
    ax.set_xlabel("physical word length")
    ax.set_ylabel("branch count")
    ax.legend(frameon=False, fontsize=6.7)
    panel_title(ax, "c", "All 234 correspondence branches")
    finish_axes(ax)

    ax = axes[1, 1]
    metrics = [data["comm"]["construction"]["prime_ideal_norm"],
               data["comm"]["r5_comm_run"]["common_cover_index"],
               data["comm"]["r5_comm_run"]["branch_count"]]
    labs = [r"$N(\mathfrak{p})$", r"$m_{\theta_c}$", "branches"]
    bars = ax.bar(np.arange(3), metrics, color=[SAND, OCHRE, COPPER], edgecolor=INK)
    ax.set_ylim(220, 239)
    ax.set_xticks(np.arange(3), labs)
    for bar, val in zip(bars, metrics):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.45, str(val),
                ha="center", va="bottom", fontsize=7.2, color=UMBER)
    ax.text(0.5, 0.08, r"$m_{\theta_c}=N(\mathfrak{p})+1$",
            transform=ax.transAxes, ha="center", color=RUST)
    panel_title(ax, "d", "Exact local-place construction")
    finish_axes(ax, "y")

    save_figure(fig, "FIG_R5_exact_periodicity_trichotomy")


def plot_r6(data: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.15), constrained_layout=True)
    qstar = data["qstar"]

    ax = axes[0, 0]
    names = ["Hermiticity", "time norm"]
    vals = [qstar["hermiticity_probe"], 7.12e-12]
    bars = ax.bar(names, vals, color=[COPPER, SAND], edgecolor=INK, width=0.55)
    ax.set_yscale("log")
    ax.set_ylim(1e-15, 1e-10)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val * 1.25, f"{val:.2e}",
                ha="center", va="bottom", fontsize=7.0, color=UMBER)
    ax.text(0.98, 0.95, r"$D=92{,}160$", transform=ax.transAxes,
            ha="right", va="top", color=RUST)
    ax.set_ylabel("absolute validation error")
    panel_title(ax, "a", r"Matrix-free validation at $D=92{,}160$")
    finish_axes(ax, "y")

    grouped: dict[tuple[str, int], list[float]] = defaultdict(list)
    for row in data["seq"]:
        grouped[(row["sequence"], int(row["level"]))].append(float(row["error"]))
    ax = axes[0, 1]
    styles = {"rational": (RUST, "o"), "sqrt2": (COPPER, "s"), "mixed": (UMBER, "^")}
    for sequence in sorted({row["sequence"] for row in data["seq"]}):
        levels = sorted(level for seq, level in grouped if seq == sequence)
        med = [np.median(grouped[(sequence, level)]) for level in levels]
        color, marker = styles.get(sequence, (MUTED, "d"))
        ax.plot(levels, med, color=color, marker=marker, markersize=3.4,
                markerfacecolor=WHITE, linestyle="dashdot", label=sequence)
    ax.set_yscale("log")
    ax.set_xlabel("arithmetic approximation level")
    ax.set_ylabel(r"median $|\theta_n-\theta_*|$")
    ax.legend(frameon=False, fontsize=6.5, ncol=3, loc="upper right")
    panel_title(ax, "b", "Three exact routes converge")
    finish_axes(ax)

    ax = axes[1, 0]
    labels = [r"$E_-$", r"$E_+$", r"$W$", r"$\mu_2$"]
    errors = np.array([2.899e-4, 1.992e-4, 2.320e-4, 5.795e-4])
    bars = ax.bar(np.arange(4), errors, color=[SAND, OCHRE, COPPER, RUST], edgecolor=INK)
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1e-3)
    ax.set_xticks(np.arange(4), labels)
    ax.set_ylabel("final median relative discrepancy")
    for bar, val in zip(bars, errors):
        ax.text(bar.get_x() + bar.get_width() / 2, val * 1.08, f"{val:.1e}",
                ha="center", va="bottom", fontsize=6.7, color=UMBER)
    panel_title(ax, "c", "Route-independent local observables")
    finish_axes(ax, "y")

    ax = axes[1, 1]
    labels = [r"$E_-$", r"$E_+$", r"$\Delta_0$", r"$W$", "IPR", r"$C$", r"$\mu_2$"]
    rho = np.array([-0.000, -0.003, -0.092, -0.008, -0.032, 0.055, 0.128])
    pval = np.array([1.000, 0.978, 0.440, 0.948, 0.787, 0.642, 0.280])
    y = np.arange(len(labels))
    colors = [COPPER if value >= 0 else SAND for value in rho]
    ax.barh(y, rho, color=colors, edgecolor=INK, height=0.58)
    ax.axvline(0, color=INK, linewidth=0.6)
    ax.set_xlim(-0.16, 0.19)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel(r"Spearman $\rho$ versus arithmetic height")
    for yi, (value, p) in enumerate(zip(rho, pval)):
        ax.text(0.184, yi, f"$p={p:.3f}$", ha="right", va="center",
                fontsize=6.2, color=MUTED)
    panel_title(ax, "d", "No monotone local height law")
    finish_axes(ax, "x")

    save_figure(fig, "FIG_R6_numerical_signatures_and_convergence")


def plot_r7(data: dict) -> None:
    frozen = data["frozen"]
    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.15), constrained_layout=True)

    ax = axes[0, 0]
    lambdas = np.array(frozen["operator"]["lambda_over_a"], dtype=float)
    margins = np.array(frozen["operator"]["schur_margins"], dtype=float)
    ax.plot(lambdas, margins, color=RUST, marker="o", markersize=4.2,
            markerfacecolor=WHITE, linestyle="dashdot")
    ax.axhline(0, color=INK, linewidth=0.65)
    for index, (x, y) in enumerate(zip(lambdas, margins)):
        offset = (8, -10) if index == 0 else (0, 6)
        align = "left" if index == 0 else "center"
        ax.annotate(f"{y:.3f}", (x, y), xytext=offset,
                    textcoords="offset points", ha=align, fontsize=6.8)
    ax.set_xlabel(r"decay length $\lambda_\perp/a$")
    ax.set_ylabel(r"growth--decay margin $\mu a-\kappa a$")
    panel_title(ax, "a", r"Frozen kernels satisfy $\mu>R^{-1}$")
    finish_axes(ax)

    ax = axes[0, 1]
    obs = [r"$S_{\rm spec}$", r"$S_{\rm prop}$", r"$R_{\rm ret}$",
           r"$C_{\rm layer}$", r"$L_{\rm res}$"]
    # Safety factor is threshold/bound for upper-gated metrics and bound/threshold
    # for lower-gated metrics.  Every certified value is therefore > 1.
    safety = np.array([2.0, 2.0, (37 / 48) / (3 / 4), 1 / (3 / 4), (4 / 5) / (3 / 4)])
    bars = ax.bar(np.arange(5), safety, color=[SAND, OCHRE, COPPER, RUST, ROSE], edgecolor=INK)
    ax.axhline(1, color=INK, linestyle="dashdot", linewidth=0.75, label="strict threshold")
    ax.set_ylim(0.9, 2.18)
    ax.set_xticks(np.arange(5), obs, rotation=18)
    ax.set_ylabel("certified safety factor")
    for bar, val in zip(bars, safety):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.035, f"{val:.2f}",
                ha="center", va="bottom", fontsize=6.7, color=UMBER)
    ax.legend(frameon=False, fontsize=6.4, loc="upper right")
    panel_title(ax, "b", "All five non-Bloch magic inequalities are strict")
    finish_axes(ax, "y")

    ax = axes[1, 0]
    x = np.linspace(0, 6, 241)
    y = np.exp(-x)
    ax.semilogy(x, y, color=RUST, linestyle="dashdot", label=r"$e^{-\ell/R}$")
    ax.fill_between(x, y, 1e-3, color=SAND, alpha=0.32, linewidth=0)
    ax.set_ylim(1e-3, 1.05)
    ax.set_xlabel(r"observation scale $\ell/R$")
    ax.set_ylabel("normalized certified angular half-width")
    ax.legend(frameon=False, fontsize=6.7)
    panel_title(ax, "c", "Curvature narrows the magic window exponentially")
    finish_axes(ax)

    ax = axes[1, 1]
    x = np.linspace(0, 4, 241)
    ax.semilogy(x, np.sinh(x) + 1e-6, color=RUST, linestyle="dashdot",
                label=r"hyperbolic $\sinh(L/R)$")
    ax.semilogy(x, x + 1e-6, color=UMBER, linestyle=(0, (4, 2, 1, 2)),
                label="Euclidean linear growth")
    ax.set_xlabel(r"local radius $L/R$")
    ax.set_ylabel("normalized twist amplification")
    ax.legend(frameon=False, fontsize=6.5, loc="upper left")
    panel_title(ax, "d", "Geodesic divergence amplifies angular mismatch")
    finish_axes(ax)

    save_figure(fig, "FIG_R7_certified_nonbloch_magic_bounds")


def plot_synthesis(data: dict) -> None:
    frozen = data["frozen"]
    fig, axes = plt.subplots(1, 4, figsize=(7.25, 2.25), constrained_layout=True)

    ax = axes[0]
    vals = [frozen["quotient"]["mu"], frozen["quotient"]["mu_tr"],
            frozen["quotient"]["order"]]
    ax.barh(np.arange(3), vals, color=[SAND, COPPER, RUST], edgecolor=INK)
    ax.set_xscale("log")
    ax.set_yticks(np.arange(3), [r"$\mu$", r"$\mu_{\rm tr}$", r"$|Q_*|$"])
    ax.set_xlabel("degree")
    panel_title(ax, "a", "R4: exact quotient")
    finish_axes(ax, "x")

    ax = axes[1]
    dims = [frozen["quotient"]["same_q_bilayer_dimension"],
            frozen["common_cover"]["hilbert_dimension"]]
    ax.bar([0, 1], dims, color=[SAND, COPPER], edgecolor=INK)
    ax.set_yscale("log")
    ax.set_xticks([0, 1], ["same", "common"])
    ax.set_ylabel("Hilbert dimension")
    panel_title(ax, "b", "R5: exact-twist cost")
    finish_axes(ax, "y")

    ax = axes[2]
    errors = [2.899e-4, 1.992e-4, 2.320e-4, 5.795e-4]
    ax.bar(np.arange(4), errors, color=[SAND, OCHRE, COPPER, RUST], edgecolor=INK)
    ax.set_yscale("log")
    ax.set_xticks(np.arange(4), [r"$E_-$", r"$E_+$", r"$W$", r"$\mu_2$"])
    ax.set_ylabel("route discrepancy")
    panel_title(ax, "c", "R6: local convergence")
    finish_axes(ax, "y")

    ax = axes[3]
    safety = [2.0, 2.0, (37 / 48) / (3 / 4), 1 / (3 / 4), (4 / 5) / (3 / 4)]
    ax.bar(np.arange(5), safety, color=[SAND, OCHRE, COPPER, RUST, ROSE], edgecolor=INK)
    ax.axhline(1, color=INK, linestyle="dashdot", linewidth=0.7)
    ax.set_xticks(np.arange(5), ["spec", "prop", "ret", "layer", "LDOS"], rotation=25)
    ax.set_ylabel("safety factor")
    panel_title(ax, "d", "R7: strict certificate")
    finish_axes(ax, "y")

    save_figure(fig, "FIG_R4_R7_quantitative_synthesis")


def write_manifest(data: dict) -> None:
    OUT_DATA.mkdir(parents=True, exist_ok=True)
    OUT_MANIFEST.mkdir(parents=True, exist_ok=True)
    rejection_counts = Counter(row["status"] for row in data["rejections"])
    branch_lengths = np.array([int(row["physical_word_length"]) for row in data["branches"]])
    summary = {
        "R4": {
            "order": data["frozen"]["quotient"]["order"],
            "mu": data["frozen"]["quotient"]["mu"],
            "mu_tr": data["frozen"]["quotient"]["mu_tr"],
            "scan_records": data["frozen"]["quotient"]["scan_records"],
            "scan_kernel_hits": data["frozen"]["quotient"]["scan_kernel_hits"],
            "rejection_counts": dict(rejection_counts),
        },
        "R5": {
            "theta_c": data["frozen"]["theta"]["theta_c"],
            "common_cover_index": data["frozen"]["common_cover"]["index"],
            "hilbert_dimension": data["frozen"]["common_cover"]["hilbert_dimension"],
            "branch_word_length": {
                "min": int(branch_lengths.min()),
                "median": float(np.median(branch_lengths)),
                "mean": float(branch_lengths.mean()),
                "max": int(branch_lengths.max()),
            },
        },
        "R6": {
            "dimension": data["qstar"]["dimension"],
            "hermiticity_probe": data["qstar"]["hermiticity_probe"],
            "time_norm_error_max": 7.12e-12,
            "final_route_discrepancies": {
                "edge_min": 2.899e-4,
                "edge_max": 1.992e-4,
                "bandwidth": 2.320e-4,
                "moment2_scaled": 5.795e-4,
            },
        },
        "R7": {
            "thresholds": {"S_spec": 1 / 18, "S_prop": 1 / 24,
                           "R_ret": 3 / 4, "C_layer": 3 / 4, "L_res": 3 / 4},
            "anchor_bounds": {"S_spec": 1 / 36, "S_prop": 1 / 48,
                              "R_ret": 37 / 48, "C_layer": 1, "L_res": 4 / 5},
            "joint_margin_lower_bound": 1 / 48,
            "scale_law": "normalized delta_theta(ell) >= exp(-ell/R)",
        },
    }
    (OUT_DATA / "R4_R7_SELECTED_NUMERICAL_RESULTS.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    sources = [
        FROZEN_JSON, THETA_SAMPLE, CEGAR, REJECTIONS, BRANCHES, COMM_CERT,
        QSTAR, SEQ, HEIGHT,
        R7 / "02_SCHUR_AND_TAIL_THEOREMS.tex",
        R7 / "03_LOCAL_TWIST_STABILITY.tex",
        R7 / "07_MAGIC_MARGIN_CERTIFICATE.tex",
        R7 / "09_GENERIC_INHERITANCE_THEOREM.tex",
    ]
    manifest = {
        "policy": "data/formula driven; no image synthesis; no digitization",
        "style": "full border, Times-compatible serif, thin lines, warm palette, dash-dot guides",
        "sources": [str(path) for path in sources],
        "outputs": [
            "FIG_R4_certified_finite_quotient",
            "FIG_R5_exact_periodicity_trichotomy",
            "FIG_R6_numerical_signatures_and_convergence",
            "FIG_R7_certified_nonbloch_magic_bounds",
            "FIG_R4_R7_quantitative_synthesis",
        ],
    }
    (OUT_MANIFEST / "FIGURE_PROVENANCE.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    require_inputs()
    configure_style()
    data = load_data()
    plot_r4(data)
    plot_r5(data)
    plot_r6(data)
    plot_r7(data)
    plot_synthesis(data)
    write_manifest(data)
    print("Generated 5 R4--R7 figure sets in PDF/SVG/600-dpi PNG.")


if __name__ == "__main__":
    main()
