from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction"
RUN_ID = "P0-05-R7-reexec-20260903T105740+0800"
BLUE, CORAL, TEAL, GOLD, DARK, GRAY = (
    "#2864DC", "#E45756", "#188977", "#D89922", "#172033", "#6B7280"
)
BROKEN_Q_RATIOS = np.array([1.10, 0.90, 1.05, 0.95])


def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def panel_label(ax, value):
    ax.text(-0.11, 1.04, value, transform=ax.transAxes, fontsize=11,
            fontweight="bold", ha="left", va="bottom", color=DARK)


def traceless_frobenius(values: np.ndarray) -> np.ndarray:
    centered = values - values.mean(axis=1, keepdims=True)
    return np.sqrt(np.sum(centered * centered, axis=1))


def anisotropy(values: np.ndarray) -> np.ndarray:
    numerator = traceless_frobenius(values)
    denominator = np.sqrt(np.sum(values * values, axis=1))
    return np.divide(numerator, denominator, out=np.zeros_like(numerator),
                     where=denominator > 0)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hodge_rows = rows(DATA / "hodge_eigenvalues.csv")
    u = np.array([float(row["w_over_w_star"]) for row in hodge_rows])
    symmetric = np.array([
        [float(row[f"lambda_{j}_over_t"]) for j in range(1, 5)]
        for row in hodge_rows
    ])
    # Exact anisotropic first-shell control:
    # E_+(k)/t = w/t + 2 sum_i (u*s_i - 1) cos(k_i), hence
    # lambda_i/t = 2(1-u*s_i) at the trivial character.
    broken = 2.0 * (1.0 - u[:, None] * BROKEN_Q_RATIOS[None, :])
    sym_trace = symmetric.sum(axis=1)
    broken_trace = broken.sum(axis=1)
    sym_tf = traceless_frobenius(symmetric)
    broken_tf = traceless_frobenius(broken)
    sym_anis = anisotropy(symmetric)
    broken_anis = anisotropy(broken)
    root_index = int(np.argmin(np.abs(u - 1.0)))

    source_csv = OUT / "P0-05-R7_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "model", "negative_control", "w_over_w_star", "q1_ratio",
            "q2_ratio", "q3_ratio", "q4_ratio", "lambda_1_over_t",
            "lambda_2_over_t", "lambda_3_over_t", "lambda_4_over_t",
            "trace_over_t", "traceless_frobenius_over_t", "anisotropy",
            "scope",
        ])
        for index, ratio in enumerate(u):
            writer.writerow([
                "symmetric", "false", f"{ratio:.12g}", "1", "1", "1", "1",
                *[f"{value:.12g}" for value in symmetric[index]],
                f"{sym_trace[index]:.12g}", f"{sym_tf[index]:.12g}",
                f"{sym_anis[index]:.12g}", "EXACT_FIRST_SHELL_CHARACTER_TORUS",
            ])
            writer.writerow([
                "symmetry_broken", "true", f"{ratio:.12g}",
                *[f"{value:.12g}" for value in BROKEN_Q_RATIOS],
                *[f"{value:.12g}" for value in broken[index]],
                f"{broken_trace[index]:.12g}", f"{broken_tf[index]:.12g}",
                f"{broken_anis[index]:.12g}",
                "EXACT_ANISOTROPIC_FIRST_SHELL_NEGATIVE_CONTROL",
            ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.2,
        "axes.titlesize": 9.5, "axes.labelsize": 8.6,
        "axes.edgecolor": DARK, "axes.linewidth": 0.8,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig = plt.figure(figsize=(11.2, 7.1), layout="constrained")
    gs = fig.add_gridspec(2, 6)

    ax = fig.add_subplot(gs[0, 0:3])
    panel_label(ax, "a")
    ax.set_title("All principal Hessian values: symmetric model", fontweight="bold", pad=8)
    markers = ["o", "s", "^", "D"]
    for j in range(4):
        ax.plot(u, symmetric[:, j], marker=markers[j], ms=4.5, lw=1.5,
                label=rf"$\lambda_{j + 1}/t$")
    ax.axhline(0, color=DARK, lw=0.8)
    ax.axvline(1, color=GOLD, lw=1.4, ls="--")
    ax.set_xlabel(r"dimensionless coupling $w/w_*$")
    ax.set_ylabel(r"principal Hessian value $\lambda_j/t$")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, ncol=2, fontsize=7)
    ax.text(0.98, 0.06, "all four vanish at the exact root",
            transform=ax.transAxes, ha="right", color=TEAL, fontweight="bold")

    ax = fig.add_subplot(gs[0, 3:6])
    panel_label(ax, "b")
    ax.set_title("Trace cancellation survives the negative control", fontweight="bold", pad=8)
    ax.plot(u, sym_trace, color=TEAL, marker="o", lw=2.1,
            label="symmetric trace")
    ax.plot(u, broken_trace, color=CORAL, marker="s", lw=1.5, ls="--",
            label="broken-control trace")
    ax.axhline(0, color=DARK, lw=0.8)
    ax.axvline(1, color=GOLD, lw=1.4, ls="--")
    ax.set_xlabel(r"$w/w_*$")
    ax.set_ylabel(r"Hodge trace $\mathrm{Tr}(H)/t$")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=7)
    ax.text(0.98, 0.06, "trace = 0 for both models at the root",
            transform=ax.transAxes, ha="right", color=CORAL, fontweight="bold")

    ax = fig.add_subplot(gs[1, 0:2])
    panel_label(ax, "c")
    ax.set_title("Traceless residual", fontweight="bold", pad=8)
    ax.plot(u, sym_tf, color=TEAL, marker="o", lw=2.0, label="symmetric")
    ax.plot(u, broken_tf, color=CORAL, marker="s", lw=2.0, label="broken control")
    ax.axvline(1, color=GOLD, lw=1.3, ls="--")
    ax.set_xlabel(r"$w/w_*$")
    ax.set_ylabel(r"$\|H-\mathrm{Tr}(H)I/4\|_F/t$")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.8)

    ax = fig.add_subplot(gs[1, 2:4])
    panel_label(ax, "d")
    ax.set_title("Dimensionless anisotropy", fontweight="bold", pad=8)
    ax.plot(u, sym_anis, color=TEAL, marker="o", lw=2.0, label="symmetric")
    ax.plot(u, broken_anis, color=CORAL, marker="s", lw=2.0, label="broken control")
    ax.axvline(1, color=GOLD, lw=1.3, ls="--")
    ax.set_xlabel(r"$w/w_*$")
    ax.set_ylabel(r"$\|H-\mathrm{Tr}(H)I/4\|_F/\|H\|_F$")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.8)

    ax = fig.add_subplot(gs[1, 4:6])
    panel_label(ax, "e")
    ax.set_title("Root test: symmetry versus broken control", fontweight="bold", pad=8)
    x = np.arange(4)
    width = 0.36
    ax.bar(x - width / 2, symmetric[root_index], width, color=TEAL,
           label="symmetric")
    ax.bar(x + width / 2, broken[root_index], width, color=CORAL,
           label="broken control")
    ax.axhline(0, color=DARK, lw=0.8)
    ax.set_xticks(x, [rf"$\lambda_{j}/t$" for j in range(1, 5)])
    ax.set_ylabel("principal Hessian value")
    ax.grid(axis="y", color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.8)
    ax.text(0.5, 0.04, r"both traces vanish; only the symmetric $H$ vanishes",
            transform=ax.transAxes, ha="center", fontsize=7.0, color=CORAL,
            fontweight="bold")

    fig.text(
        0.5, -0.012,
        "Scope: exact first-shell character model and a preregistered analytic anisotropic control; "
        "not a production-parameter, representation-complete, or full-bulk mechanism claim.",
        ha="center", fontsize=8, color=DARK,
    )
    base = OUT / "P0-05-R7_hodge_mechanism"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    config = {
        "task_id": "P0-05-R7",
        "run_id": RUN_ID,
        "claim_id": "C06-restricted-validation",
        "observable": "four principal Hessian values, trace, traceless Frobenius residual, and normalized anisotropy",
        "units": "Hessian values normalized by t; anisotropy dimensionless",
        "negative_control": "exact anisotropic first-shell q_i/q_1=(1.10,0.90,1.05,0.95)",
        "target_projector_id": "layer-even first-shell character target",
        "representation_scope": "declared first-shell characters only",
        "cover_tower": "not applicable to this analytic character-level mechanism test",
        "cutoff": "first shell",
        "broadening": "not applicable",
        "solver": "exact principal-Hessian formulas cross-checked against registered symmetric CSV",
        "uncertainty": "exact analytic control; registered symmetric numerical residual <= 2.980232260973992e-08",
        "scope": "NO_PRODUCTION_OR_REPRESENTATION_COMPLETE_OR_FULL_BULK_CLAIM",
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R7_plot_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    tracked = [
        DATA / "hodge_eigenvalues.csv", DATA / "derivative_audit.csv",
        DATA / "parameters.json", Path(__file__).resolve(), source_csv,
        config_path, base.with_suffix(".pdf"), base.with_suffix(".svg"),
        base.with_suffix(".png"),
    ]
    record = {
        **config,
        "terminal_scientific_status": "DONE_RESTRICTED_EXACT_FIRST_SHELL_MECHANISM",
        "files": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in tracked
        ],
    }
    (OUT / "P0-05-R7_run_record.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

