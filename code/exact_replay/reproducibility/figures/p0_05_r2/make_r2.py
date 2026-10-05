from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "reproducibility/data/euclidean_topic1_reconstruction"
RUN_ID = "P0-05-R2-reexec-20260903T104401+0800"
BLUE, CORAL, TEAL, DARK, GRAY, LIGHT = (
    "#2864DC", "#E45756", "#188977", "#172033", "#6B7280", "#EEF2F7"
)


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


def geometry_panel(ax, site_count: int, sites, bases, panel: str):
    label(ax, panel)
    ax.set_title(f"Exact {site_count}-site coincidence cell", fontweight="bold", pad=8)
    rows = [r for r in sites if int(r["site_count"]) == site_count]
    b = [r for r in bases if int(r["site_count"]) == site_count and r["space"] == "direct"]
    vec = {r["vector"]: np.array([float(r["x_component"]), float(r["y_component"])]) for r in b}
    t1, t2 = vec["T1"], vec["T2"]
    cell = np.vstack([np.zeros(2), t1, t1 + t2, t2, np.zeros(2)])
    ax.plot(cell[:, 0], cell[:, 1], color=DARK, lw=1.2)
    for layer, color, marker in [(1, BLUE, "o"), (2, CORAL, "^")]:
        lr = [r for r in rows if int(r["layer"]) == layer]
        x = [float(r["x_over_a"]) for r in lr]
        y = [float(r["y_over_a"]) for r in lr]
        ax.scatter(x, y, s=28 if site_count == 10 else 18, marker=marker,
                   facecolor="white", edgecolor=color, linewidth=1.1,
                   label=f"layer {layer}")
    ax.arrow(0, 0, t1[0], t1[1], color=TEAL, width=0.015,
             head_width=0.16, length_includes_head=True)
    ax.arrow(0, 0, t2[0], t2[1], color=TEAL, width=0.015,
             head_width=0.16, length_includes_head=True)
    ax.text(*(0.53 * t1), r"$\mathbf{T}_1$", color=TEAL, fontweight="bold")
    ax.text(*(0.53 * t2), r"$\mathbf{T}_2$", color=TEAL, fontweight="bold")
    ax.set_xlabel(r"$x/a$")
    ax.set_ylabel(r"$y/a$")
    ax.set_aspect("equal")
    ax.grid(color="#D8DEE9", lw=0.45, alpha=0.65)
    ax.legend(frameon=False, fontsize=7, loc="best")
    sigma = site_count // 2
    ax.text(0.03, 0.03, rf"$N_{{\rm sc}}={site_count},\ \Sigma={sigma}$",
            transform=ax.transAxes, fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CBD5E1"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cells = read_csv(DATA / "commensurate_cells.csv")
    sites = read_csv(DATA / "real_space_sites.csv")
    bases = read_csv(DATA / "lattice_bases.csv")
    diff = read_csv(DATA / "diffraction_metrics.csv")

    exact = sorted(cells, key=lambda r: float(r["angle_degrees"]))
    theta = np.array([float(r["angle_degrees"]) for r in exact])
    nsc = np.array([int(r["site_count"]) for r in exact])
    sigma = np.array([int(r["sigma"]) for r in exact])
    lsc = np.array([float(r["supercell_length_over_a"]) for r in exact])
    dmap = {int(r["site_count"]): r for r in diff if r["site_count"]}
    beat = np.array([float(dmap[int(n)]["beat_length_over_a"]) for n in nsc])
    c8 = next(r for r in diff if r["case"] == "incommensurate_c8_control")

    source_csv = OUT / "P0-05-R2_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "case", "site_count", "sigma", "angle_degrees",
            "supercell_length_over_a", "beat_length_over_a",
            "exact_cell_status", "negative_control_tag",
        ])
        for r, b in zip(exact, beat):
            writer.writerow([
                f"commensurate_{r['site_count']}_site", r["site_count"], r["sigma"],
                r["angle_degrees"], r["supercell_length_over_a"], f"{b:.15g}",
                "EXACT_SQUARE_CSL", "false",
            ])
        writer.writerow([
            "incommensurate_c8_control", "", "", c8["angle_degrees"], "",
            c8["beat_length_over_a"], "NO_EXACT_FINITE_COINCIDENCE_CELL", "true",
        ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5,
        "axes.titlesize": 10, "axes.labelsize": 9,
        "axes.edgecolor": DARK, "axes.linewidth": 0.8,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6), layout="constrained")
    geometry_panel(axes[0, 0], 10, sites, bases, "a")
    geometry_panel(axes[0, 1], 34, sites, bases, "b")

    ax = axes[1, 0]
    label(ax, "c")
    ax.set_title("Complete nontrivial inventory below 100 sites", fontweight="bold", pad=8)
    ax.scatter(theta, nsc, s=48, color=BLUE, zorder=3)
    for x, y, s in zip(theta, nsc, sigma):
        ax.annotate(rf"$\Sigma={s}$", (x, y), xytext=(4, 4),
                    textcoords="offset points", fontsize=6.8, color=DARK)
    ax.axvline(float(c8["angle_degrees"]), color=CORAL, ls="--", lw=1.5)
    ax.text(44.6, 94, r"$45^\circ$: $C_8$ beat control" "\n" "no finite square CSL",
            color=CORAL, ha="right", va="top", fontsize=7.2)
    ax.set_xlabel(r"twist angle $\widehat\theta$ (degrees)")
    ax.set_ylabel(r"bilayer sites $N_{\rm sc}=2\Sigma$")
    ax.set_xlim(10, 46)
    ax.set_ylim(0, 102)
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)

    ax = axes[1, 1]
    label(ax, "d")
    ax.set_title("Exact supercell scale is not the beat scale", fontweight="bold", pad=8)
    ax.plot(theta, lsc, color=BLUE, marker="o", lw=1.8,
            label=r"exact $L_{\rm sc}/a=\sqrt{\Sigma}$")
    ax.plot(theta, beat, color=TEAL, marker="s", lw=1.8,
            label=r"local beat $\ell_{\rm beat}/a$")
    ax.scatter([float(c8["angle_degrees"])], [float(c8["beat_length_over_a"])],
               marker="D", s=52, facecolor="white", edgecolor=CORAL, lw=1.5,
               label=r"$45^\circ$ beat-only control")
    ax.text(44.4, float(c8["beat_length_over_a"]) + 0.4,
            "no exact $L_{\\rm sc}$", color=CORAL, ha="right", fontsize=7)
    ax.set_xlabel(r"twist angle $\widehat\theta$ (degrees)")
    ax.set_ylabel("length / $a$")
    ax.set_xlim(10, 46)
    ax.grid(color="#D8DEE9", lw=0.55, alpha=0.8)
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    ax.text(
        0.03, 0.04,
        "Exact arithmetic geometry; no fitted parameters\n"
        "and no hybridized band claim.",
        transform=ax.transAxes, fontsize=7.2,
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#CBD5E1"),
    )

    base = OUT / "P0-05-R2_euclidean_commensurate_benchmark"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    config = {
        "task_id": "P0-05-R2",
        "run_id": RUN_ID,
        "claim_id": "C02",
        "observable": "exact square coincidence geometry and scale comparison",
        "units": "angles in degrees; lengths in a; site counts dimensionless",
        "negative_control": "45 degree C8 local beat with no exact finite square CSL",
        "scope": "EXACT_EUCLIDEAN_GEOMETRY_NO_HYBRIDIZED_BANDS",
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R2_plot_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    tracked = [
        DATA / "commensurate_cells.csv", DATA / "real_space_sites.csv",
        DATA / "lattice_bases.csv", DATA / "diffraction_metrics.csv",
        Path(__file__).resolve(), source_csv, config_path,
        base.with_suffix(".pdf"), base.with_suffix(".svg"), base.with_suffix(".png"),
    ]
    record = {
        **config,
        "terminal_scientific_status": "DONE_EXACT_EUCLIDEAN_BENCHMARK",
        "target_projector_id": "NOT_APPLICABLE",
        "representation_scope": "Euclidean exact coincidence cells",
        "cover_tower": "NOT_APPLICABLE",
        "cutoff": "NOT_APPLICABLE",
        "broadening": "NOT_APPLICABLE",
        "solver": "exact arithmetic formulas",
        "uncertainty": "roundoff only; tabulated values follow exact formulas",
        "files": [
            {
                "path": str(p.relative_to(ROOT)).replace("\\", "/"),
                "bytes": p.stat().st_size,
                "sha256": sha256(p),
            }
            for p in tracked
        ],
    }
    (OUT / "P0-05-R2_run_record.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
