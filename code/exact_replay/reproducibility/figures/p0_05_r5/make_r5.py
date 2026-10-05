from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction"
RUN_ID = "P0-05-R5-reexec-20260903T105039+0800"
BLUE, CORAL, TEAL, GOLD, DARK, GRAY = (
    "#2864DC", "#E45756", "#188977", "#D89922", "#172033", "#6B7280"
)


def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def label(ax, value):
    ax.text(-0.10, 1.04, value, transform=ax.transAxes, fontsize=11,
            fontweight="bold", ha="left", va="bottom", color=DARK)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    obs = rows(DATA / "target_observables.csv")
    proj = rows(DATA / "projector_tracking.csv")
    params = json.loads((DATA / "parameters.json").read_text(encoding="utf-8"))
    fixture = params["clean_room_validation_fixture"]
    tol = float(params["solver_configuration"]["dense_sparse_eigenvalue_tolerance_over_t"])

    u = np.array([float(r["w_over_w_star"]) for r in obs])
    bandwidth = np.array([float(r["even_bandwidth_over_t"]) for r in obs])
    gap = np.array([float(r["signed_lower_isolation_gap_over_t"]) for r in obs])
    velocity = np.array([float(r["maximum_generalized_velocity_t_over_hbar"]) for r in obs])
    proj_angle = np.array([float(r["maximum_principal_angle_rad"]) for r in proj])
    proj_defect = np.array([abs(1.0 - float(r["trace_overlap"])) for r in proj])

    alpha = np.linspace(0.0, 2.0, 600)
    rr = np.sqrt(1.0 + 16.0 * alpha**2)
    c_square = (rr**2 - rr + 2.0) / (rr * (rr + 1.0))
    cmin = 4.0 * math.sqrt(2.0) - 5.0
    alpha_pc = 1.0 / math.sqrt(8.0)
    root_tol_u = 2.0 * tol / 16.0

    source_csv = OUT / "P0-05-R5_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "record_type", "x", "square_c", "w_over_w_star",
            "bandwidth_over_t", "gap_over_t", "velocity_t_over_hbar",
            "projector_defect", "principal_angle_rad", "scope",
        ])
        for a, c in zip(alpha, c_square):
            writer.writerow([
                "square_exact_curve", f"{a:.10g}", f"{c:.12g}", "", "", "",
                "", "", "", "EXACT_FIVE_STATE_SQUARE_CONTROL",
            ])
        for idx, r in enumerate(obs):
            writer.writerow([
                "hyperbolic_validation", "", "", r["w_over_w_star"],
                r["even_bandwidth_over_t"], r["signed_lower_isolation_gap_over_t"],
                r["maximum_generalized_velocity_t_over_hbar"],
                f"{proj_defect[idx]:.12g}", f"{proj_angle[idx]:.12g}",
                r["observable_scope"],
            ])
        writer.writerow([
            "root_tolerance", "", "", "1", "", "", "", "", "",
            f"VALIDATION_SOLVER_ROOT_HALF_WIDTH={root_tol_u:.12g}",
        ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.2,
        "axes.titlesize": 9.6, "axes.labelsize": 8.7,
        "axes.edgecolor": DARK, "axes.linewidth": 0.8,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig = plt.figure(figsize=(11.2, 7.1), layout="constrained")
    gs = fig.add_gridspec(2, 6)

    ax = fig.add_subplot(gs[0, 0:3])
    label(ax, "a")
    ax.set_title("Square five-state control: no finite root", fontweight="bold", pad=8)
    ax.plot(alpha, c_square, color=CORAL, lw=2.4,
            label=r"exact $c_{\rm sq}(\alpha)$")
    ax.axhline(cmin, color=DARK, lw=1.2, ls=":",
               label=r"$4\sqrt{2}-5>0$")
    ax.axvline(alpha_pc, color=GRAY, lw=1.2, ls="--",
               label=r"formal quadratic-series zero $1/\sqrt{8}$")
    ax.scatter([alpha_pc], [3 - 4 * math.sqrt(3) / 3], color=CORAL, s=42, zorder=4)
    ax.set_xlabel(r"dimensionless coupling $\alpha$")
    ax.set_ylabel(r"quadratic coefficient $c_{\rm sq}$")
    ax.set_ylim(0, 1.05)
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    ax.text(0.03, 0.05, "negative control: folding and minimal\nhybridization never cancel curvature",
            transform=ax.transAxes, color=CORAL, fontsize=7.3, fontweight="bold")

    ax = fig.add_subplot(gs[0, 3:6])
    label(ax, "b")
    ax.set_title("Surface-group validation: positive simple root", fontweight="bold", pad=8)
    ax.plot(u, bandwidth, color=TEAL, marker="o", lw=2.2,
            label=r"target bandwidth $W_+/t$")
    ax.plot(u, velocity, color=BLUE, marker="s", lw=1.7,
            label=r"$v_{\max}\hbar/t$")
    ax.axvline(1.0, color=GOLD, lw=1.6, ls="--", label=r"$w=w_*=t/q_1$")
    ax.set_xlabel(r"coupling $w/w_*$")
    ax.set_ylabel("dimensionless response")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=7)
    ax.text(0.98, 0.07, r"$W_+(w_*)=v_{\max}(w_*)=0$",
            transform=ax.transAxes, ha="right", color=TEAL, fontweight="bold")

    ax = fig.add_subplot(gs[1, 0:2])
    label(ax, "c")
    ax.set_title("Protecting isolation gap", fontweight="bold", pad=8)
    ax.plot(u, gap, color=BLUE, marker="o", lw=2.2)
    ax.axvline(1.0, color=GOLD, lw=1.4, ls="--")
    root_gap = gap[np.argmin(abs(u - 1.0))]
    ax.scatter([1.0], [root_gap], color=GOLD, s=48, zorder=4)
    ax.text(0.98, 0.06, rf"$g_*/t={root_gap:.3f}>0$",
            transform=ax.transAxes, ha="right", color=BLUE, fontweight="bold")
    ax.set_xlabel(r"$w/w_*$")
    ax.set_ylabel(r"signed lower gap $\Delta^L/t$")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)

    ax = fig.add_subplot(gs[1, 2:4])
    label(ax, "d")
    ax.set_title("Validation root interval", fontweight="bold", pad=8)
    ax.errorbar([1.0], [0.52], xerr=[root_tol_u], fmt="o", ms=7,
                color=GOLD, ecolor=GOLD, capsize=5)
    ax.axvline(1.0, color=GOLD, lw=1.4, ls="--")
    ax.set_xlim(1 - 1.2e-9, 1 + 1.2e-9)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel(r"$w/w_*$")
    ax.text(
        0.5, 0.18,
        rf"$|w/w_*-1|\leq {root_tol_u:.2e}$" "\n"
        "from the registered eigensolver tolerance",
        transform=ax.transAxes, ha="center", fontsize=7.2,
    )
    ax.text(
        0.5, 0.88,
        "full-kernel shell interval not instantiated",
        transform=ax.transAxes, ha="center", color=CORAL, fontsize=7.0,
    )
    ax.grid(axis="x", color="#D8DEE9", lw=0.55, alpha=0.8)

    ax = fig.add_subplot(gs[1, 4:6])
    label(ax, "e")
    ax.set_title("Tracked rank-one projector", fontweight="bold", pad=8)
    ax.semilogy(u, np.maximum(proj_angle, 1e-18), color=TEAL, marker="o",
                lw=1.8, label="maximum principal angle")
    ax.semilogy(u, np.maximum(proj_defect, 1e-18), color=CORAL, marker="s",
                lw=1.6, label=r"$|1-\mathrm{Tr}(P_0P)|$")
    ax.set_xlabel(r"$w/w_*$")
    ax.set_ylabel("projector diagnostic")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.8)
    ax.text(0.03, 0.05, "rank = 1 throughout the validation scan",
            transform=ax.transAxes, fontsize=7.0)

    fig.text(
        0.5, -0.012,
        "Scope: exact square theorem plus clean-room surface-group validation fixture; "
        "not a production parameter or representation-complete bulk claim.",
        ha="center", fontsize=8, color=DARK,
    )
    base = OUT / "P0-05-R5_magic_no_magic_dichotomy"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    config = {
        "task_id": "P0-05-R5",
        "run_id": RUN_ID,
        "claim_id": "C05",
        "observable": "square quadratic coefficient; surface-group bandwidth, gap, and projector diagnostics",
        "units": "dimensionless or normalized by t",
        "negative_control": "exact square five-state no-root curve",
        "target_projector_id": "rank-one even character validation target",
        "representation_scope": "exact square control plus first-shell character validation",
        "cover_tower": "validation quotient only; no production tower",
        "cutoff": "first-shell validation",
        "broadening": "not applicable",
        "solver": "exact formulas plus registered dense/sparse validation",
        "uncertainty": f"validation root half-width {root_tol_u:.12g} in w/w_star",
        "scope": "NO_PRODUCTION_OR_FULL_BULK_CLAIM",
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R5_plot_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    tracked = [
        DATA / "target_observables.csv", DATA / "projector_tracking.csv",
        DATA / "derivative_audit.csv", DATA / "parameters.json",
        DATA / "finite_solver_checks.json", Path(__file__).resolve(),
        source_csv, config_path, base.with_suffix(".pdf"),
        base.with_suffix(".svg"), base.with_suffix(".png"),
    ]
    record = {
        **config,
        "terminal_scientific_status": "DONE_RESTRICTED_VALIDATION_DICHOTOMY",
        "files": [
            {
                "path": str(p.relative_to(ROOT)).replace("\\", "/"),
                "bytes": p.stat().st_size,
                "sha256": sha256(p),
            }
            for p in tracked
        ],
    }
    (OUT / "P0-05-R5_run_record.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
