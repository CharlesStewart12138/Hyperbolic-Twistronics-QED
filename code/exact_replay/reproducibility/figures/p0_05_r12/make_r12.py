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
DATA = ROOT / "reproducibility/data/hyperbolic_dos_reconstruction"
RUN_ID = "P0-05-R12-reexec-20260903T111537+0800"
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


def panel_label(ax, value):
    ax.text(-0.09, 1.04, value, transform=ax.transAxes, fontsize=11,
            fontweight="bold", ha="left", va="bottom", color=DARK)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = rows(DATA / "resolved_dos.csv")
    by_id = defaultdict(list)
    for row in records:
        by_id[row["resolution_id"]].append(row)
    for values in by_id.values():
        values.sort(key=lambda row: int(row["grid_index"]))

    def curve(name):
        values = by_id[name]
        return (
            np.asarray([float(row["energy_over_t"]) for row in values]),
            np.asarray([float(row["density_over_t_inverse"]) for row in values]),
        )

    local1 = curve("local_layer_1_origin")
    local2 = curve("local_layer_2_origin")
    layer1 = curve("layer_1")
    layer2 = curve("layer_2")
    even = curve("layer_even_projector")
    odd = curve("layer_odd_projector")
    target = curve("target_root_projector")
    eta = float(by_id["global"][0]["eta_over_t"])
    audit = json.loads((DATA / "dos_audit.json").read_text(encoding="utf-8"))
    exact_bounds = audit["exact_spectral_bounds_over_t"]
    target_energy = float(exact_bounds["upper"])
    target_rank = int(audit["target_root_rank"])
    cell_count = target_rank
    cell_weight = 1.0 / cell_count

    source_csv = OUT / "P0-05-R12_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "record_type", "channel", "energy_over_t", "density_over_t_inverse",
            "cell_index", "normalized_projector_cell_weight", "eta_over_t",
            "negative_control", "scope",
        ])
        for channel, (energy, density) in [
            ("local_layer_1_origin", local1), ("local_layer_2_origin", local2),
            ("layer_1", layer1), ("layer_2", layer2),
            ("layer_even_projector", even), ("layer_odd_projector", odd),
            ("target_root_projector", target),
        ]:
            negative = "true" if channel == "layer_odd_projector" else "false"
            for e_value, d_value in zip(energy, density):
                writer.writerow([
                    "resolved_dos", channel, f"{e_value:.12g}", f"{d_value:.12g}",
                    "", "", f"{eta:.12g}", negative,
                    "REGISTERED_512D_VALIDATION_HAMILTONIAN",
                ])
        for cell in range(cell_count):
            writer.writerow([
                "projector_profile", "target_root_projector", "", "", cell,
                f"{cell_weight:.12g}", "", "false",
                "EXACT_LAYER_EVEN_RANK_256_CELL_PROFILE",
            ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.0,
        "axes.titlesize": 9.5, "axes.labelsize": 8.6,
        "axes.edgecolor": DARK, "axes.linewidth": 0.8,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 6.8), layout="constrained")
    axes = axes.ravel()

    ax = axes[0]
    panel_label(ax, "a")
    ax.set_title("Origin LDOS in the two layers", fontweight="bold")
    ax.plot(local1[0], local1[1], color=BLUE, lw=1.8, label="layer 1 origin")
    ax.plot(local2[0], local2[1], color=CORAL, lw=1.2, ls="--", label="layer 2 origin")
    ax.axvline(target_energy, color=GOLD, lw=1.2, ls=":")
    ax.set_xlim(exact_bounds["lower"] - 8, exact_bounds["upper"] + 8)
    ax.set_xlabel(r"angular-frequency shift $\Omega/t$")
    ax.set_ylabel(r"local density $t\rho_x$")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=7)

    ax = axes[1]
    panel_label(ax, "b")
    ax.set_title("Layer-resolved spectral response", fontweight="bold")
    ax.plot(layer1[0], layer1[1], color=BLUE, lw=1.8, label="layer 1")
    ax.plot(layer2[0], layer2[1], color=CORAL, lw=1.2, ls="--", label="layer 2")
    ax.axvline(target_energy, color=GOLD, lw=1.2, ls=":")
    ax.set_xlim(exact_bounds["lower"] - 8, exact_bounds["upper"] + 8)
    ax.set_xlabel(r"$\Omega/t$")
    ax.set_ylabel(r"layer measure $t\rho_L$")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=7)
    residual = float(np.max(np.abs(layer1[1] - layer2[1])))
    ax.text(0.98, 0.06, rf"max layer mismatch $={residual:.1e}$",
            transform=ax.transAxes, ha="right", color=TEAL, fontsize=7,
            fontweight="bold")

    ax = axes[2]
    panel_label(ax, "c")
    ax.set_title("Exact target-projector cell profile", fontweight="bold")
    cells = np.arange(cell_count)
    ax.plot(cells, np.full(cell_count, cell_weight), color=TEAL, lw=2.0)
    ax.fill_between(cells, 0, cell_weight, color=TEAL, alpha=0.22)
    ax.set_xlabel("validation cell index")
    ax.set_ylabel(r"$Q_x(P_C)=\mathrm{Tr}_{x}P_C/r_C$")
    ax.set_ylim(0, 1.35 * cell_weight)
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.text(0.5, 0.83, rf"rank $r_C={target_rank}$; $Q_x=1/{cell_count}$",
            transform=ax.transAxes, ha="center", color=TEAL, fontweight="bold")
    ax.text(0.5, 0.70, "uniform character-level projector; no geometric embedding",
            transform=ax.transAxes, ha="center", color=GRAY, fontsize=7)

    ax = axes[3]
    panel_label(ax, "d")
    ax.set_title("Ideal representation-selective drive", fontweight="bold")
    zoom = (even[0] >= target_energy - 18) & (even[0] <= target_energy + 6)
    ax.plot(even[0][zoom], even[1][zoom], color=TEAL, lw=2.0,
            label="layer-even drive")
    ax.plot(target[0][zoom], target[1][zoom], color=GOLD, lw=1.3, ls=":",
            label="target projector")
    ax.plot(odd[0][zoom], odd[1][zoom], color=CORAL, lw=1.7, ls="--",
            label="layer-odd negative control")
    ax.axvline(target_energy, color=DARK, lw=0.9)
    ax.set_xlabel(r"$\Omega/t$")
    ax.set_ylabel(r"projected density $t\rho_P$")
    ax.grid(color="#D8DEE9", lw=0.5, alpha=0.8)
    ax.legend(frameon=False, fontsize=6.8)
    ax.text(0.97, 0.06, "odd drive suppresses the positive target pole",
            transform=ax.transAxes, ha="right", color=CORAL, fontsize=7,
            fontweight="bold")

    fig.text(
        0.5, -0.012,
        f"Scope: registered 512-dimensional clean-room validation Hamiltonian; Lorentzian eta/t={eta:.6g}. "
        "Projected-drive curves are ideal spectral responses, not calibrated multiport measurements or bulk tomography.",
        ha="center", fontsize=7.7, color=DARK,
    )
    base = OUT / "P0-05-R12_ldos_projector_tomography"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    config = {
        "task_id": "P0-05-R12",
        "run_id": RUN_ID,
        "claim_id": "validation-LDOS-projector-resolution",
        "observable": "two origin LDOS curves, layer-resolved DOS, normalized target-projector cell profile, and ideal even/odd projected responses",
        "units": "energy normalized by t; densities in inverse t; normalized cell weights dimensionless",
        "negative_control": "ideal layer-odd projector drive at the positive layer-even target root",
        "target_projector_id": "rank-256 layer-even target-root projector",
        "representation_scope": "registered 512-dimensional finite Abelian validation Hamiltonian",
        "cover_tower": "single (Z/4Z)^4 validation quotient; no tower",
        "cutoff": "registered validation Hamiltonian",
        "broadening": f"Lorentzian eta/t={eta:.12g}",
        "solver": "exact registered eigenspectrum and exact resolved spectral measures",
        "uncertainty": f"resolved sum-rule Linf residual {audit['metrics']['resolved_sum_rule_linf']:.12g}",
        "scope": "NO_CALIBRATED_PORT_OR_PRODUCTION_OR_BULK_TOMOGRAPHY_CLAIM",
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R12_plot_config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    tracked = [
        DATA / "resolved_dos.csv", DATA / "dos_audit.json",
        DATA / "parameters.json", Path(__file__).resolve(), source_csv,
        config_path, base.with_suffix(".pdf"), base.with_suffix(".svg"),
        base.with_suffix(".png"),
    ]
    record = {
        **config,
        "terminal_scientific_status": "DONE_RESTRICTED_FINITE_VALIDATION_TOMOGRAPHY",
        "files": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in tracked
        ],
    }
    (OUT / "P0-05-R12_run_record.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

