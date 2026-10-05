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
DATA = ROOT / "reproducibility/data/euclidean_topic1_reconstruction"
RUN_ID = "P0-05-R4-reexec-20260903T104807+0800"
BLUE, CORAL, TEAL, DARK, GRAY = "#2864DC", "#E45756", "#188977", "#172033", "#6B7280"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def label(ax, value: str):
    ax.text(-0.08, 1.04, value, transform=ax.transAxes, fontsize=11,
            fontweight="bold", ha="left", va="bottom", color=DARK)


def peak_panel(ax, rows, title, panel, control=False):
    label(ax, panel)
    ax.set_title(title, fontweight="bold", pad=8)
    for layer, color, marker in [(1, BLUE, "o"), (2, CORAL, "^")]:
        rr = [r for r in rows if int(r["layer"]) == layer]
        x = [float(r["qx_a_over_2pi"]) for r in rr]
        y = [float(r["qy_a_over_2pi"]) for r in rr]
        ax.scatter(x, y, s=85, marker=marker, facecolor="white",
                   edgecolor=color, lw=1.7, label=f"layer {layer}")
        for xx, yy in zip(x, y):
            ax.plot([0, xx], [0, yy], color=color, lw=0.7, alpha=0.45)
    circle = plt.Circle((0, 0), 1.0, fill=False, ec=GRAY, lw=0.8, ls=":")
    ax.add_patch(circle)
    ax.scatter([0], [0], s=18, color=DARK)
    ax.axhline(0, color="#D8DEE9", lw=0.6)
    ax.axvline(0, color="#D8DEE9", lw=0.6)
    ax.set_xlabel(r"$q_x a/(2\pi)$")
    ax.set_ylabel(r"$q_y a/(2\pi)$")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    scope = "beat-only control\nno exact finite square CSL" if control else "exact ideal delta peaks\nunit form factor"
    ax.text(0.98, 0.03, scope, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7, color=CORAL if control else DARK)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    peaks = read_csv(DATA / "diffraction_peaks.csv")
    metrics = read_csv(DATA / "diffraction_metrics.csv")
    exact = [r for r in metrics if r["site_count"]]
    exact.sort(key=lambda r: float(r["angle_degrees"]))
    theta = np.array([float(r["angle_degrees"]) for r in exact])
    split = np.array([float(r["first_shell_split_a_over_2pi"]) for r in exact])
    mbz = np.array([float(r["mbz_reciprocal_magnitude_a_over_2pi"]) for r in exact])

    source_csv = OUT / "P0-05-R4_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "record_type", "case", "site_count", "layer", "qx_a_over_2pi",
            "qy_a_over_2pi", "angle_degrees", "first_shell_split_a_over_2pi",
            "mbz_reciprocal_magnitude_a_over_2pi", "scope", "negative_control_tag",
        ])
        for r in peaks:
            writer.writerow([
                "peak", r["case"], r["site_count"], r["layer"],
                r["qx_a_over_2pi"], r["qy_a_over_2pi"], "", "", "",
                r["scope"], "true" if r["case"] == "incommensurate_c8_control" else "false",
            ])
        for r in metrics:
            writer.writerow([
                "metric", r["case"], r["site_count"], "", "", "",
                r["angle_degrees"], r["first_shell_split_a_over_2pi"],
                r["mbz_reciprocal_magnitude_a_over_2pi"],
                r["scope"], "true" if r["case"] == "incommensurate_c8_control" else "false",
            ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5,
        "axes.titlesize": 10, "axes.labelsize": 9,
        "axes.edgecolor": DARK, "axes.linewidth": 0.8,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 7.7), layout="constrained")

    ten = [r for r in peaks if r["case"] == "commensurate_10_site"]
    peak_panel(axes[0, 0], ten, r"Two reciprocal lattices: $\Sigma=5$", "a")

    ax = axes[0, 1]
    label(ax, "b")
    ax.set_title("Exact first-shell splitting", fontweight="bold", pad=8)
    ax.plot(theta, split, color=TEAL, marker="o", lw=2,
            label=r"$|\Delta\mathbf{G}|a/(2\pi)$")
    ax.plot(theta, mbz, color=BLUE, marker="s", lw=1.6,
            label=r"$G_{\rm MBZ}a/(2\pi)$")
    for x, y, r in zip(theta, split, exact):
        ax.annotate(rf"$N={r['site_count']}$", (x, y), xytext=(3, 4),
                    textcoords="offset points", fontsize=6.5)
    ax.set_xlabel(r"twist angle $\widehat\theta$ (degrees)")
    ax.set_ylabel("reciprocal scale")
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=7)
    ax.text(0.03, 0.95, "exact rigid first-shell geometry",
            transform=ax.transAxes, va="top", fontsize=7.2)

    thirty_four = [r for r in peaks if r["case"] == "commensurate_34_site"]
    peak_panel(axes[1, 0], thirty_four,
               r"Commensurate pattern: $\Sigma=17$", "c")

    c8 = [r for r in peaks if r["case"] == "incommensurate_c8_control"]
    peak_panel(axes[1, 1], c8,
               r"$45^\circ$ $C_8$ union control", "d", control=True)

    fig.text(
        0.5, -0.012,
        "Claim scope: exact ideal peak locations only; finite-window intensities "
        "and reconstruction satellites are not evaluated.",
        ha="center", color=DARK, fontsize=8,
    )
    base = OUT / "P0-05-R4_diffraction_fourier_reconstruction"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    config = {
        "task_id": "P0-05-R4",
        "run_id": RUN_ID,
        "claim_id": "C04",
        "observable": "ideal first-shell reciprocal peak positions and splitting",
        "units": "q a/(2 pi); angles in degrees",
        "negative_control": "45 degree C8 beat-only union without exact finite square CSL",
        "scope": "IDEAL_RIGID_DELTA_PEAK_GEOMETRY_ONLY",
        "excluded": "finite-window intensity and reconstruction satellites",
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R4_plot_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    tracked = [
        DATA / "diffraction_peaks.csv", DATA / "diffraction_metrics.csv",
        DATA / "diffraction_checks.json", Path(__file__).resolve(),
        source_csv, config_path, base.with_suffix(".pdf"),
        base.with_suffix(".svg"), base.with_suffix(".png"),
    ]
    record = {
        **config,
        "terminal_scientific_status": "DONE_IDEAL_DIFFRACTION_GEOMETRY",
        "target_projector_id": "NOT_APPLICABLE",
        "representation_scope": "Euclidean reciprocal lattices",
        "cover_tower": "NOT_APPLICABLE",
        "cutoff": "first reciprocal shell",
        "broadening": "none; delta-peak locations",
        "solver": "exact rigid square reciprocal geometry",
        "uncertainty": "roundoff only for plotted locations",
        "files": [
            {
                "path": str(p.relative_to(ROOT)).replace("\\", "/"),
                "bytes": p.stat().st_size,
                "sha256": sha256(p),
            }
            for p in tracked
        ],
    }
    (OUT / "P0-05-R4_run_record.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
