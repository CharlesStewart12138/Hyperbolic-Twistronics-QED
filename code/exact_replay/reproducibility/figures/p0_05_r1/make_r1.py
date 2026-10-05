from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
GEOM = ROOT / "reproducibility/data/hyperbolic_geometry_reconstruction/bolza_vertices.csv"
PARAMS = ROOT / "reproducibility/data/hyperbolic_hamiltonian_reconstruction/parameters.json"
RUN_ID = "P0-05-R1-reexec-20260903T103828+0800"

BLUE = "#2864DC"
CORAL = "#E45756"
TEAL = "#188977"
DARK = "#172033"
GRAY = "#6B7280"
LIGHT = "#EEF2F7"
GOLD = "#D89922"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def panel_label(ax, text: str) -> None:
    ax.text(
        -0.03, 1.04, text, transform=ax.transAxes, ha="left", va="bottom",
        fontsize=11, fontweight="bold", color=DARK,
    )


def load_vertices() -> np.ndarray:
    rows = []
    with GEOM.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append((float(row["disk_x"]), float(row["disk_y"])))
    return np.asarray(rows)


def draw_octagon(ax, xy: np.ndarray, color: str, offset=(0.0, 0.0), angle=0.0,
                 alpha=1.0, zorder=2) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    rot = np.array([[c, -s], [s, c]])
    pts = xy @ rot.T + np.asarray(offset)
    closed = np.vstack([pts, pts[0]])
    ax.plot(closed[:, 0], closed[:, 1], color=color, lw=1.8, alpha=alpha, zorder=zorder)
    ax.scatter(pts[:, 0], pts[:, 1], s=28, facecolor="white", edgecolor=color,
               linewidth=1.4, zorder=zorder + 1)
    return pts


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    vertices = load_vertices()
    params = json.loads(PARAMS.read_text(encoding="utf-8"))
    fixture = params["clean_room_validation_fixture"]
    h_over_a = float(fixture["h_over_a"])
    lam_over_a = float(fixture["lambda_perp_over_a"])

    d = np.linspace(0.0, 3.0, 301)
    t_over_w = np.exp(-(np.sqrt(h_over_a**2 + d**2) - h_over_a) / lam_over_a)
    source_csv = OUT / "P0-05-R1_source_data.csv"
    with source_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "panel_id", "d_over_a", "T_over_w_positive_control",
            "T_over_w_w0_negative_control", "h_over_a", "lambda_perp_over_a",
            "parameter_status",
        ])
        for di, ti in zip(d, t_over_w):
            writer.writerow([
                "C", f"{di:.8f}", f"{ti:.12g}", "0",
                f"{h_over_a:.8g}", f"{lam_over_a:.8g}",
                "CLEAN_ROOM_VALIDATION_FIXTURE_NOT_PRODUCTION",
            ])

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.edgecolor": DARK,
        "axes.linewidth": 0.8,
        "xtick.color": DARK,
        "ytick.color": DARK,
        "text.color": DARK,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })

    fig = plt.figure(figsize=(12.0, 7.2), facecolor="white", layout="constrained")
    gs = fig.add_gridspec(2, 6, height_ratios=[1.03, 0.97])

    ax_a = fig.add_subplot(gs[0, 0:2])
    panel_label(ax_a, "a")
    ax_a.set_title("Twisted two-layer resonator network", pad=9, fontweight="bold")
    p1 = draw_octagon(ax_a, vertices * 0.82, BLUE, offset=(-0.13, -0.12), angle=0.0)
    p2 = draw_octagon(ax_a, vertices * 0.82, CORAL, offset=(0.13, 0.14),
                      angle=math.pi / 16)
    for idx in [0, 2, 4, 6]:
        ax_a.plot([p1[idx, 0], p2[idx, 0]], [p1[idx, 1], p2[idx, 1]],
                  color=TEAL, lw=1.1, ls=(0, (3, 2)), alpha=0.9, zorder=1)
    arc = patches.Arc((0.0, 0.0), 0.75, 0.75, theta1=5, theta2=25,
                      color=GOLD, lw=1.8)
    ax_a.add_patch(arc)
    ax_a.text(0.39, 0.10, r"$\theta$", color=GOLD, fontweight="bold")
    ax_a.text(-0.94, -0.98, "Layer 1: intralayer $t$", color=BLUE, fontweight="bold")
    ax_a.text(-0.94, -1.12, "Layer 2: rotated by $g_\\theta$", color=CORAL, fontweight="bold")
    ax_a.text(-0.94, -1.26, "dashed: programmed $T_{ij}(\\theta)$", color=TEAL)
    ax_a.set_xlim(-1.08, 1.08)
    ax_a.set_ylim(-1.34, 1.15)
    ax_a.set_aspect("equal")
    ax_a.axis("off")

    ax_b = fig.add_subplot(gs[0, 2:4])
    panel_label(ax_b, "b")
    ax_b.set_title("Finite quotient and declared scope", pad=9, fontweight="bold")
    for i in range(4):
        for j in range(4):
            rect = patches.FancyBboxPatch(
                (i, j), 0.82, 0.82, boxstyle="round,pad=0.02,rounding_size=0.06",
                facecolor=LIGHT if (i + j) % 2 == 0 else "white",
                edgecolor=BLUE, lw=0.8,
            )
            ax_b.add_patch(rect)
            ax_b.scatter(i + 0.41, j + 0.41, s=12, color=CORAL, zorder=3)
    ax_b.annotate("", xy=(3.9, 1.9), xytext=(-0.1, 1.9),
                  arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.4))
    ax_b.annotate("", xy=(1.9, 3.9), xytext=(1.9, -0.1),
                  arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.4))
    ax_b.text(1.91, 4.12, "identified boundaries", ha="center", color=TEAL)
    ax_b.text(0.02, -0.55, r"validation: $Q_{\rm val}=(\mathbb{Z}/4\mathbb{Z})^4$, degree 256",
              fontsize=8)
    ax_b.text(0.02, -0.88, r"production quotient: not yet fixed", fontsize=8,
              color=CORAL, fontweight="bold")
    ax_b.set_xlim(-0.35, 4.2)
    ax_b.set_ylim(-1.0, 4.45)
    ax_b.set_aspect("equal")
    ax_b.axis("off")

    ax_c = fig.add_subplot(gs[0, 4:6])
    panel_label(ax_c, "c")
    ax_c.set_title("Distance-programmed interlayer coupling", pad=9, fontweight="bold")
    ax_c.plot(d, t_over_w, color=TEAL, lw=2.4,
              label=r"$T(d)/w=e^{-[\sqrt{h^2+d^2}-h]/\lambda_\perp}$")
    ax_c.plot(d, np.zeros_like(d), color=GRAY, lw=1.8, ls="--",
              label=r"negative control: $w=0$")
    ax_c.set_xlabel(r"geodesic in-plane separation $d/a$")
    ax_c.set_ylabel(r"normalized coupling $T/w$")
    ax_c.set_xlim(0, 3)
    ax_c.set_ylim(-0.035, 1.05)
    ax_c.grid(color="#D8DEE9", lw=0.6, alpha=0.8)
    ax_c.legend(loc="upper right", frameon=False, fontsize=7.2)
    ax_c.text(
        0.03, 0.18, r"validation fixture only" "\n"
        r"$h/a=0.5,\ \lambda_\perp/a=0.125$",
        transform=ax_c.transAxes, fontsize=7.5,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CBD5E1"),
    )

    ax_d = fig.add_subplot(gs[1, 0:3])
    panel_label(ax_d, "d")
    ax_d.set_title("Hardware-to-hopping calibration", pad=9, fontweight="bold")
    ax_d.axis("off")
    boxes = [
        (0.02, 0.45, 0.23, 0.29, BLUE, "coupling capacitor\n$C^c_{\\alpha\\beta}$"),
        (0.385, 0.45, 0.23, 0.29, TEAL, "calibrated hopping\n$|J_{\\alpha\\beta}|$"),
        (0.75, 0.45, 0.23, 0.29, CORAL, "matrix element\n$T_{ij}(\\theta)$"),
    ]
    for x, y, w, h, color, label in boxes:
        box = patches.FancyBboxPatch(
            (x, y), w, h, transform=ax_d.transAxes,
            boxstyle="round,pad=0.02,rounding_size=0.025",
            facecolor="white", edgecolor=color, lw=1.8,
        )
        ax_d.add_patch(box)
        ax_d.text(x + w / 2, y + h / 2, label, transform=ax_d.transAxes,
                  ha="center", va="center", color=color, fontweight="bold")
    for x1, x2 in [(0.26, 0.38), (0.625, 0.745)]:
        ax_d.annotate("", xy=(x2, 0.595), xytext=(x1, 0.595),
                      xycoords=ax_d.transAxes,
                      arrowprops=dict(arrowstyle="->", color=DARK, lw=1.4))
    ax_d.text(
        0.5, 0.22,
        r"$C^c_{\alpha\beta}=\dfrac{2\bar C}{\omega_0}"
        r"|J^{\rm tar}_{\alpha\beta}|"
        r"+O\!\left[\bar C(J^{\rm tar}_{\alpha\beta}/\omega_0)^2\right]$",
        transform=ax_d.transAxes, ha="center", va="center", fontsize=10,
    )
    ax_d.text(
        0.5, 0.05,
        r"controlled rotating-wave regime: $z_{\rm eff}J_{\max}/\omega_0\ll1$",
        transform=ax_d.transAxes, ha="center", color=GRAY,
    )

    ax_e = fig.add_subplot(gs[1, 3:6])
    panel_label(ax_e, "e")
    ax_e.set_title("Microscopic bilayer Hamiltonian", pad=9, fontweight="bold")
    ax_e.axis("off")
    ax_e.text(
        0.5, 0.72,
        r"$h_N(\theta)=\omega_0 I_{2N}+\mathcal{H}_{\rm intra}+\mathcal{T}_{\rm inter}(\theta)$",
        transform=ax_e.transAxes, ha="center", va="center", fontsize=13,
        bbox=dict(boxstyle="round,pad=0.5", fc=LIGHT, ec=BLUE, lw=1.2),
    )
    ax_e.text(
        0.5, 0.40,
        r"$T_N=0\ (w=0)\ \Longrightarrow\ "
        r"h_N=(\omega_0I-tA_N)\oplus(\omega_0I-tA_N)$",
        transform=ax_e.transAxes, ha="center", va="center", fontsize=10.5,
        color=GRAY,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=GRAY, lw=1.0, ls="--"),
    )
    ax_e.text(
        0.5, 0.18,
        "Negative control: two uncoupled layers cannot display\n"
        "twist-induced interlayer reconstruction.",
        transform=ax_e.transAxes, ha="center", va="center",
        color=CORAL, fontweight="bold",
    )
    ax_e.text(
        0.5, 0.03,
        "Scope: circuit-to-Hamiltonian mapping; no production spectrum is shown.",
        transform=ax_e.transAxes, ha="center", color=DARK, fontsize=7.8,
    )

    base = OUT / "P0-05-R1_platform_hamiltonian"
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    plot_config = {
        "task_id": "P0-05-R1",
        "run_id": RUN_ID,
        "figure_role": "THEORY_AND_PLATFORM_SCHEMATIC",
        "claim_id": "C01",
        "negative_control": "w=0 uncoupled bilayer",
        "parameter_status": "CLEAN_ROOM_VALIDATION_FIXTURE_NOT_PRODUCTION",
        "h_over_a": h_over_a,
        "lambda_perp_over_a": lam_over_a,
        "output_formats": ["pdf", "svg", "png_600dpi"],
    }
    config_path = OUT / "P0-05-R1_plot_config.json"
    config_path.write_text(json.dumps(plot_config, indent=2), encoding="utf-8")

    tracked = [
        GEOM, PARAMS, Path(__file__).resolve(), source_csv, config_path,
        base.with_suffix(".pdf"), base.with_suffix(".svg"), base.with_suffix(".png"),
    ]
    record = {
        "task_id": "P0-05-R1",
        "run_id": RUN_ID,
        "terminal_scientific_status": "DONE_SCHEMATIC_NO_PRODUCTION_SPECTRUM",
        "observable": "normalized analytical interlayer kernel and block Hamiltonian",
        "units": "d/a and T/w; Hamiltonian in angular-frequency units",
        "target_projector_id": "NOT_APPLICABLE",
        "representation_scope": "finite regular matrix; no spectral decomposition",
        "cover_tower": "validation quotient only; production quotient missing",
        "cutoff": "not used in schematic",
        "broadening": "not applicable",
        "solver": "not applicable",
        "uncertainty": "no fitted or production numerical claim",
        "negative_control": "w=0 uncoupled layers",
        "files": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in tracked
        ],
    }
    record_path = OUT / "P0-05-R1_run_record.json"
    record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
