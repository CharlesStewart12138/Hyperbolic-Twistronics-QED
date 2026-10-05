from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "reproducibility/data/hyperbolic_finite_cover_convergence"
PARAMS = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/parameters.json"
RUN_ID = "P0-05-R9-reexec-20260903T110328+0800"
BLUE, CORAL, TEAL, GOLD, DARK, GRAY = (
    "#2864DC", "#E45756", "#188977", "#D89922", "#172033", "#6B7280"
)
TOWER_STYLE = {
    "A_power_of_two": (BLUE, "o", r"tower A: $(Z/2^n Z)^4$"),
    "B_three_multiple": (TEAL, "s", r"tower B: $(Z/(6\,3^n)Z)^4$"),
}


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
    ax.text(-0.13, 1.04, value, transform=ax.transAxes, fontsize=10.5,
            fontweight="bold", ha="left", va="bottom", color=DARK)


def grouped(records):
    result = defaultdict(list)
    for row in records:
        result[row["tower_id"]].append(row)
    for values in result.values():
        values.sort(key=lambda row: int(row["level"]))
    return result


def finite_target_gaps(spectrum_rows, w_star):
    by_cover = defaultdict(list)
    for row in spectrum_rows:
        key = (row["tower_id"], int(row["level"]), int(row["modulus"]))
        by_cover[key].append(float(row["energy_over_t"]))
    gaps = {}
    for key, energies in by_cover.items():
        array = np.asarray(energies)
        target = array[np.argmin(np.abs(array - w_star))]
        separated = np.abs(array - target)
        separated = separated[separated > 1e-8]
        gaps[key] = float(np.min(separated)) if separated.size else float("nan")
    return gaps


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cover = rows(DATA / "cover_sequence.csv")
    cross = rows(DATA / "cross_cover_diagnostics.csv")
    edges = rows(DATA / "no_loss_no_pollution.csv")
    shells = rows(DATA / "shell_budgets.csv")
    spectra = rows(DATA / "cover_spectral_sets.csv")
    params = json.loads(PARAMS.read_text(encoding="utf-8"))
    w_star = float(params["clean_room_validation_fixture"]["w_star_over_t"])
    cover_groups = grouped(cover)
    edge_groups = grouped(edges)
    gaps = finite_target_gaps(spectra, w_star)

    source_csv = OUT / "P0-05-R9_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "record_type", "tower_id", "level", "modulus", "cover_degree",
            "word_injectivity_radius", "minimum_kernel_word_length",
            "balanced_shell_depth", "cdf_kolmogorov_distance",
            "C0_no_loss_error_over_t", "C0_no_pollution_error_over_t",
            "finite_target_gap_over_t", "layer_factor_projector_distance",
            "shell_depth", "C0_tail_over_t", "C1_tail_over_t",
            "C2_tail_over_t", "negative_control", "scope",
        ])
        cross_lookup = {}
        for row in cross:
            key = (row["left_tower"], int(row["left_level"]),
                   row["right_tower"], int(row["right_level"]))
            cross_lookup[key] = float(row["cdf_kolmogorov_distance"])
        for row in cover:
            key = (row["tower_id"], int(row["level"]), int(row["modulus"]))
            writer.writerow([
                "cover", row["tower_id"], row["level"], row["modulus"],
                row["cover_degree"], row["word_injectivity_radius"],
                row["minimum_kernel_word_length"], row["balanced_shell_depth"],
                "", row["C0_no_loss_error_over_t"],
                row["C0_no_pollution_error_over_t"], f"{gaps[key]:.12g}",
                "0", "", "", "", "", "true",
                "FIRST_SHELL_ABELIAN_CHARACTER_TOWERS_FULL_GROUP_INCONCLUSIVE",
            ])
        for row in cross:
            writer.writerow([
                "cdf_comparison", f"{row['left_tower']}->{row['right_tower']}",
                f"{row['left_level']}->{row['right_level']}",
                f"{row['left_modulus']}->{row['right_modulus']}", "", "", "", "",
                row["cdf_kolmogorov_distance"], "", "", "", "", "", "", "", "",
                "true", row["matching_status"],
            ])
        for row in shells:
            writer.writerow([
                "shell_budget", "", "", "", "", "", "", "", "", "", "", "", "",
                row["retained_word_depth"], row["C0_operator_tail_bound_over_t"],
                row["C1_derivative_tail_bound_over_t"],
                row["C2_Hessian_tail_bound_over_t"], "false", row["budget_scope"],
            ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 7.6,
        "axes.titlesize": 8.8, "axes.labelsize": 8.0,
        "axes.edgecolor": DARK, "axes.linewidth": 0.8,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 4, figsize=(12.0, 6.8), layout="constrained")
    axes = axes.ravel()

    ax = axes[0]
    panel_label(ax, "a")
    ax.set_title("Two explicit validation towers", fontweight="bold")
    for tower, values in cover_groups.items():
        color, marker, label = TOWER_STYLE[tower]
        ax.semilogy([int(r["level"]) for r in values],
                    [int(r["cover_degree"]) for r in values],
                    marker=marker, color=color, lw=1.8, label=label)
    ax.set_xlabel("tower level")
    ax.set_ylabel(r"cover degree $|Q_N|$")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.2)

    ax = axes[1]
    panel_label(ax, "b")
    ax.set_title("Injectivity obstruction", fontweight="bold")
    for tower, values in cover_groups.items():
        color, marker, label = TOWER_STYLE[tower]
        degree = [int(r["cover_degree"]) for r in values]
        ax.semilogx(degree, [float(r["word_injectivity_radius"]) for r in values],
                    marker=marker, color=color, lw=1.8, label=label.split(":")[0])
    ax.axhline(2, color=CORAL, ls="--", lw=1.2)
    ax.text(0.5, 0.09, r"negative control: $[a_1,b_1]$ remains in every kernel",
            transform=ax.transAxes, ha="center", color=CORAL, fontsize=6.5,
            fontweight="bold")
    ax.set_xlabel(r"cover degree $|Q_N|$")
    ax.set_ylabel(r"word radius $r_{\rm inj}^{\rm word}$")
    ax.set_ylim(0, 3.1)
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)

    ax = axes[2]
    panel_label(ax, "c")
    ax.set_title("Balanced shell depth does not grow", fontweight="bold")
    for tower, values in cover_groups.items():
        color, marker, label = TOWER_STYLE[tower]
        degree = [int(r["cover_degree"]) for r in values]
        ax.semilogx(degree, [float(r["balanced_shell_depth"]) for r in values],
                    marker=marker, color=color, lw=1.8, label=label.split(":")[0])
    ax.axhline(1, color=CORAL, ls="--", lw=1.2)
    ax.set_xlabel(r"cover degree $|Q_N|$")
    ax.set_ylabel(r"retained depth $L_N$")
    ax.set_ylim(0, 2.1)
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)

    ax = axes[3]
    panel_label(ax, "d")
    ax.set_title("CDF diagnostics decrease", fontweight="bold")
    x = np.arange(len(cross))
    y = [float(r["cdf_kolmogorov_distance"]) for r in cross]
    colors = [BLUE if r["comparison_type"] == "SUCCESSIVE_COVER" else GOLD for r in cross]
    ax.bar(x, y, color=colors)
    ax.set_xticks(x, [f"{r['left_modulus']}→{r['right_modulus']}" for r in cross], rotation=35)
    ax.set_ylabel(r"CDF distance $d_K$")
    ax.grid(axis="y", color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.text(0.5, 0.92, "not a bulk certificate: radius stays fixed",
            transform=ax.transAxes, ha="center", color=CORAL, fontsize=6.4)

    ax = axes[4]
    panel_label(ax, "e")
    ax.set_title("One-sided spectral edges", fontweight="bold")
    for tower, values in edge_groups.items():
        color, marker, label = TOWER_STYLE[tower]
        degree = [int(cover_groups[tower][i]["cover_degree"]) for i in range(len(values))]
        ax.loglog(degree, [float(r["no_loss_error_over_t"]) for r in values],
                  marker=marker, color=color, lw=1.8, label="no-loss " + label.split(":")[0])
        ax.loglog(degree, np.maximum([float(r["no_pollution_error_over_t"]) for r in values], 1e-15),
                  marker=marker, color=color, lw=1.0, ls=":")
    ax.set_xlabel(r"cover degree $|Q_N|$")
    ax.set_ylabel(r"one-sided edge error$/t$")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.0)

    ax = axes[5]
    panel_label(ax, "f")
    ax.set_title("Finite target isolation", fontweight="bold")
    for tower, values in cover_groups.items():
        color, marker, label = TOWER_STYLE[tower]
        degree = [int(r["cover_degree"]) for r in values]
        gap_values = [gaps[(tower, int(r["level"]), int(r["modulus"]))] for r in values]
        ax.semilogx(degree, gap_values, marker=marker, color=color, lw=1.8,
                    label=label.split(":")[0])
    ax.set_xlabel(r"cover degree $|Q_N|$")
    ax.set_ylabel(r"nearest finite gap $\Delta_N/t$")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.0)

    ax = axes[6]
    panel_label(ax, "g")
    ax.set_title("Projector: exact layer factor only", fontweight="bold")
    all_degree = [int(r["cover_degree"]) for r in cover]
    ax.semilogx(all_degree, np.zeros(len(all_degree)), color=TEAL, marker="o", lw=1.8)
    ax.set_xlabel(r"cover degree $|Q_N|$")
    ax.set_ylabel(r"$\|P_{+,N}^{\rm layer}-P_+^{\rm layer}\|$")
    ax.set_ylim(-0.05, 0.25)
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.text(0.5, 0.78, "full cross-cover spectral-projector\ntransport is not available",
            transform=ax.transAxes, ha="center", color=CORAL, fontsize=6.5,
            fontweight="bold")

    ax = axes[7]
    panel_label(ax, "h")
    ax.set_title(r"Separate $C^0/C^1/C^2$ shell budgets", fontweight="bold")
    depth = [int(r["retained_word_depth"]) for r in shells]
    ax.semilogy(depth, np.maximum([float(r["C0_operator_tail_bound_over_t"]) for r in shells], 1e-16),
                color=BLUE, marker="o", lw=1.8, label=r"$C^0$")
    ax.semilogy(depth, np.maximum([float(r["C1_derivative_tail_bound_over_t"]) for r in shells], 1e-16),
                color=TEAL, marker="s", lw=1.8, label=r"$C^1$")
    ax.semilogy(depth, np.maximum([float(r["C2_Hessian_tail_bound_over_t"]) for r in shells], 1e-16),
                color=CORAL, marker="^", lw=1.8, label=r"$C^2$")
    ax.set_xlabel("retained word depth")
    ax.set_ylabel("finite-patch tail bound")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.3)
    ax.text(0.5, 0.06, "infinite tail unknown beyond depth 3",
            transform=ax.transAxes, ha="center", color=CORAL, fontsize=6.3)

    fig.text(
        0.5, -0.015,
        "Scope: two finite Abelian character towers. Diagnostics are complete, but constant word injectivity radius "
        "and the missing geometric radius prohibit a full surface-group or bulk-convergence claim.",
        ha="center", fontsize=7.7, color=DARK,
    )
    base = OUT / "P0-05-R9_finite_cover_convergence"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    config = {
        "task_id": "P0-05-R9",
        "run_id": RUN_ID,
        "claim_id": "C0-finite-Abelian-diagnostics-negative-bulk-control",
        "observable": "two towers, word injectivity, balanced depth, CDF, one-sided edges, finite gap, layer-factor projector, and C0/C1/C2 budgets",
        "units": "cover degree and word depth dimensionless; spectral quantities normalized by t",
        "negative_control": "persistent commutator kernel witness [a1,b1] with word injectivity radius 2 at every level",
        "target_projector_id": "layer-even first-shell target; projector panel restricted to exact 2x2 layer factor",
        "representation_scope": "complete duals of the two finite Abelian validation towers",
        "cover_tower": "A moduli 4,8,16; B moduli 6,18",
        "cutoff": "balanced depth 1; shell-budget patch through word depth 3",
        "broadening": "CDF uses exact discrete weighted spectra; no smoothing",
        "solver": "analytic finite Fourier character spectra and direct weighted diagnostics",
        "uncertainty": "deterministic validation data; full-group and infinite-tail channels explicitly unresolved",
        "scope": "DIAGNOSTICS_COMPLETE_FULL_SURFACE_GROUP_CONVERGENCE_INCONCLUSIVE",
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R9_plot_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    tracked = [
        DATA / "cover_sequence.csv", DATA / "cross_cover_diagnostics.csv",
        DATA / "no_loss_no_pollution.csv", DATA / "shell_budgets.csv",
        DATA / "cover_spectral_sets.csv", DATA / "convergence_audit.json",
        Path(__file__).resolve(), source_csv, config_path,
        base.with_suffix(".pdf"), base.with_suffix(".svg"), base.with_suffix(".png"),
    ]
    record = {
        **config,
        "terminal_scientific_status": "DONE_RESTRICTED_DIAGNOSTIC_WITH_FALSIFYING_BULK_CONTROL",
        "files": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in tracked
        ],
    }
    (OUT / "P0-05-R9_run_record.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

