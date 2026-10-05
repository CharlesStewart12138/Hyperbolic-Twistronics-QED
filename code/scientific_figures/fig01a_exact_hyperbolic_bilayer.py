"""Exact-data Figure 1a for the hyperbolic twisted-bilayer manuscript.

Scientific geometry is loaded from the frozen R6 universal-cover archive.
No lattice coordinate, graph edge, twist angle, or physical parameter is
invented. The circuit-QED inset is explicitly labelled as schematic.
"""
from __future__ import annotations

import csv
import math
import sys
from fractions import Fraction
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Arc, Circle, FancyArrowPatch
import numpy as np


HERE = Path(__file__).resolve().parent
REVISE = HERE.parents[2]
R6 = REVISE / "PHYSICS_VALIDATION_R6"
BUILDERS = R6 / "02_OPERATOR_BUILDERS"
FROZEN = R6 / "00_FROZEN_INPUTS"
SCAN = R6 / "11_PROCESSED_DATA" / "phenomenon_IV_magic_scan.tsv"

if str(BUILDERS) not in sys.path:
    sys.path.insert(0, str(BUILDERS))

from geometry import KAPPA_B_A, R_OVER_A, load_orbit_patch, rotate  # noqa: E402


# Warm palette used by the preceding production figures.
INK = "#342A25"
NEUTRAL = "#B9B2AC"
LIGHT = "#DED9D4"
LAYER1 = "#D18A32"
LAYER1_DARK = "#9C5B20"
LAYER2 = "#A74232"
LAYER2_DARK = "#762B24"
COUPLER = "#6B5B52"

THETA_TARGET = 11.0 * math.pi / 128.0
PLOT_DEPTH = 3
DISK_CLIP = 0.997
A_REG_OVER_A = 1.0
H_OVER_A = 0.5


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "Nimbus Roman"],
            "mathtext.fontset": "stix",
            "font.size": 8.0,
            "axes.titlesize": 8.7,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def load_representative_scan_row() -> dict[str, float]:
    """Recover the actual nonzero R6 candidate row from processed data."""
    with SCAN.open(encoding="utf-8", newline="") as handle:
        rows = [
            {key: float(value) for key, value in row.items()}
            for row in csv.DictReader(handle, delimiter="\t")
        ]
    nonzero = [row for row in rows if row["theta"] > 0.0]
    row = max(nonzero, key=lambda item: item["combined_score"])
    if not math.isclose(row["theta"], THETA_TARGET, rel_tol=0.0, abs_tol=2e-15):
        raise RuntimeError("R6 maximum no longer matches the frozen 11*pi/128 candidate")
    fraction = Fraction(row["theta"] / math.pi).limit_denominator(1024)
    if (fraction.numerator, fraction.denominator) != (11, 128):
        raise RuntimeError("Frozen representative twist lost its exact grid identity")
    return row


def geodesic_arc(z1: complex, z2: complex, samples: int = 28) -> np.ndarray:
    """Sample the Poincare geodesic joining two exact disk coordinates."""
    z1 = complex(z1)
    z2 = complex(z2)
    cross = z1.real * z2.imag - z1.imag * z2.real
    if abs(cross) < 1e-12:
        t = np.linspace(0.0, 1.0, samples)
        return (1.0 - t) * z1 + t * z2

    matrix = 2.0 * np.array([[z1.real, z1.imag], [z2.real, z2.imag]])
    rhs = np.array([abs(z1) ** 2 + 1.0, abs(z2) ** 2 + 1.0])
    center_xy = np.linalg.solve(matrix, rhs)
    center = complex(center_xy[0], center_xy[1])
    radius = math.sqrt(max(abs(center) ** 2 - 1.0, 0.0))
    a1 = math.atan2((z1 - center).imag, (z1 - center).real)
    a2 = math.atan2((z2 - center).imag, (z2 - center).real)
    delta = (a2 - a1 + math.pi) % (2.0 * math.pi) - math.pi
    angles = a1 + np.linspace(0.0, delta, samples)
    arc = center + radius * np.exp(1j * angles)
    if np.max(np.abs(arc)) > 1.000001:
        alt = delta - math.copysign(2.0 * math.pi, delta)
        angles = a1 + np.linspace(0.0, alt, samples)
        arc = center + radius * np.exp(1j * angles)
    if np.max(np.abs(arc)) > 1.000001:
        raise ArithmeticError("Poincare geodesic arc left the unit disk")
    return arc


def unique_visible_edges(adjacency, visible: np.ndarray) -> np.ndarray:
    rows, cols = adjacency.nonzero()
    pairs = [
        (int(i), int(j))
        for i, j in zip(rows, cols)
        if i < j and visible[i] and visible[j]
    ]
    return np.asarray(pairs, dtype=np.int32)


def arc_segments(points: np.ndarray, edges: np.ndarray) -> list[np.ndarray]:
    return [
        np.column_stack((arc.real, arc.imag))
        for i, j in edges
        for arc in [geodesic_arc(points[i], points[j])]
    ]


def draw_disk_panel(ax, coordinates, rotated, depths, edges, theta, xi_over_a):
    ax.set_aspect("equal")
    ax.set_xlim(-1.045, 1.045)
    ax.set_ylim(-1.045, 1.045)
    ax.axis("off")

    # The circle is the Poincare boundary, not a periodic boundary.
    ax.add_patch(Circle((0, 0), 1.0, fill=False, ec=NEUTRAL, lw=0.65, zorder=0))
    for angle in np.arange(8) * math.pi / 4.0:
        ax.plot(
            [0, 0.985 * math.cos(angle)],
            [0, 0.985 * math.sin(angle)],
            color=LIGHT,
            lw=0.28,
            ls="dashdot",
            zorder=0,
        )

    ax.add_collection(
        LineCollection(
            arc_segments(rotated, edges),
            colors=LAYER2,
            linewidths=0.34,
            alpha=0.70,
            zorder=1,
        )
    )
    ax.add_collection(
        LineCollection(
            arc_segments(coordinates, edges),
            colors=LAYER1,
            linewidths=0.42,
            alpha=0.82,
            zorder=2,
        )
    )

    for depth in range(PLOT_DEPTH + 1):
        mask = depths == depth
        if depth == 0:
            continue
        size = {1: 12.0, 2: 7.0, 3: 4.0}[depth]
        ax.scatter(
            rotated[mask].real,
            rotated[mask].imag,
            s=size,
            marker="o",
            facecolors="white",
            edgecolors=LAYER2_DARK,
            linewidths=0.36,
            zorder=3,
        )
        ax.scatter(
            coordinates[mask].real,
            coordinates[mask].imag,
            s=size,
            marker="o",
            color=LAYER1,
            edgecolors=LAYER1_DARK,
            linewidths=0.26,
            zorder=4,
        )

    ax.scatter([0], [0], s=19, color=INK, zorder=7)
    ax.text(-1.035, 1.025, "a", fontsize=16, fontweight="bold", ha="left", va="top")
    ax.text(
        0,
        1.025,
        r"exact $\{8,8\}$ centre-orbit bilayer",
        ha="center",
        va="bottom",
        fontsize=9.1,
    )

    # Mark one actual S8 nearest-neighbour bond: center -> g0.
    neighbor = coordinates[np.flatnonzero(depths == 1)[0]]
    midpoint = 0.48 * neighbor
    ax.annotate(
        "",
        xy=(neighbor.real, neighbor.imag),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="|-|", color=INK, lw=0.55),
    )
    ax.text(
        midpoint.real - 0.03,
        midpoint.imag + 0.045,
        r"$a_B$",
        ha="center",
        va="bottom",
        fontsize=8.2,
    )

    guide_r = 0.20
    ax.add_patch(
        Arc(
            (0, 0),
            2 * guide_r,
            2 * guide_r,
            theta1=0,
            theta2=math.degrees(theta),
            color=INK,
            lw=0.55,
            linestyle="dashdot",
            zorder=8,
        )
    )
    ax.text(0.23, 0.055, r"$\theta_{\rm plot}$", fontsize=7.5, ha="left", va="bottom")

    ax.plot([], [], color=LAYER1, lw=1.1, marker="o", markersize=3.2, label="layer 1")
    ax.plot(
        [],
        [],
        color=LAYER2,
        lw=1.0,
        marker="o",
        markerfacecolor="white",
        markersize=3.2,
        label="layer 2",
    )
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0.03, 0.03),
        frameon=False,
        fontsize=7.1,
        handlelength=1.5,
        ncol=2,
        columnspacing=0.9,
    )
    ax.text(
        0.97,
        -1.005,
        rf"$\theta_{{\rm plot}}=11\pi/128$; $\xi_M={xi_over_a:.3f}\,a_B$",
        ha="right",
        va="bottom",
        fontsize=7.4,
    )
    ax.text(
        0.97,
        -1.035,
        "generic twist: no exact finite common cover",
        ha="right",
        va="top",
        fontsize=6.8,
        fontstyle="italic",
        color=INK,
    )


def draw_twist_inset(ax, theta, xi_over_a, rho_xi, nearest_neighbor):
    ax.set_aspect("equal")
    ax.set_xlim(-0.06, 1.04)
    ax.set_ylim(-0.08, 0.48)
    ax.axis("off")
    ax.set_title("Exact local twist geometry", pad=2.0)

    z0 = 0.0 + 0.0j
    z_nn = complex(nearest_neighbor)
    z_nn_rot = z_nn * np.exp(1j * theta)
    z_xi = rho_xi + 0.0j
    z_xi_rot = z_xi * np.exp(1j * theta)

    for z, color in ((z_nn, LAYER1), (z_nn_rot, LAYER2)):
        arc = geodesic_arc(z0, z)
        ax.plot(arc.real, arc.imag, color=color, lw=1.0)
    ax.scatter([0], [0], s=12, color=INK, zorder=5)
    ax.scatter(
        [z_nn.real],
        [z_nn.imag],
        s=18,
        color=LAYER1,
        edgecolor=LAYER1_DARK,
        lw=0.35,
        zorder=5,
    )
    ax.scatter(
        [z_nn_rot.real],
        [z_nn_rot.imag],
        s=18,
        facecolor="white",
        edgecolor=LAYER2_DARK,
        lw=0.55,
        zorder=5,
    )

    disp = geodesic_arc(z_xi, z_xi_rot)
    ax.plot(disp.real, disp.imag, color=INK, lw=0.70, ls="dashdot", zorder=3)
    ax.scatter(
        [z_xi.real, z_xi_rot.real],
        [z_xi.imag, z_xi_rot.imag],
        s=11,
        facecolor="white",
        edgecolor=INK,
        lw=0.45,
        zorder=4,
    )

    wedge_r = 0.22
    ax.add_patch(
        Arc(
            (0, 0),
            2 * wedge_r,
            2 * wedge_r,
            theta1=0,
            theta2=math.degrees(theta),
            color=INK,
            lw=0.55,
        )
    )
    ax.text(
        0.25,
        0.045,
        rf"$\theta={math.degrees(theta):.3f}^\circ$",
        fontsize=7.0,
        ha="left",
    )
    ax.annotate(
        "",
        xy=(z_xi.real, 0.0),
        xytext=(0.0, 0.0),
        arrowprops=dict(arrowstyle="->", color=COUPLER, lw=0.55),
    )
    ax.text(0.48 * z_xi.real, -0.035, r"$\xi_M$", fontsize=7.1, ha="center", va="top")
    ax.annotate(
        r"$d_\theta(\xi_M)=a_B$",
        xy=(disp[len(disp) // 2].real, disp[len(disp) // 2].imag),
        xytext=(0.72, 0.34),
        textcoords="data",
        fontsize=6.8,
        ha="center",
        arrowprops=dict(arrowstyle="->", lw=0.45, color=COUPLER),
    )
    ax.text(
        0.03,
        0.91,
        r"$d_\theta(r)=2R\,\mathrm{arsinh}"
        r"\!\left[\sinh(r/R)|\sin(\theta/2)|\right]$",
        transform=ax.transAxes,
        fontsize=6.25,
        ha="left",
        va="top",
    )
    ax.text(
        0.03,
        0.78,
        rf"$a_{{\rm reg}}=a_B:\quad \xi_M={xi_over_a:.3f}\,a_B$",
        transform=ax.transAxes,
        fontsize=6.7,
        ha="left",
        va="top",
    )


def resonator_path(x0: float, x1: float, y: float, phase: float = 0.0):
    x = np.linspace(x0, x1, 120)
    envelope = np.sin(np.pi * (x - x0) / (x1 - x0)) ** 2
    yy = y + 0.025 * envelope * np.sin(
        14 * np.pi * (x - x0) / (x1 - x0) + phase
    )
    return x, yy


def draw_circuit_inset(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("schematic circuit-QED implementation", pad=2.0)

    centers = [0.20, 0.48, 0.76]
    for center in centers:
        x, y = resonator_path(center - 0.105, center + 0.105, 0.72)
        ax.plot(x, y, color=LAYER1, lw=1.25, solid_capstyle="round")
        x, y = resonator_path(center - 0.105, center + 0.105, 0.30, phase=0.7)
        ax.plot(x, y, color=LAYER2, lw=1.25, solid_capstyle="round")

    for center in centers:
        ax.plot([center, center], [0.35, 0.67], color=COUPLER, lw=0.75, ls="dashdot")
        ax.add_patch(Circle((center, 0.51), 0.018, ec=COUPLER, fc="white", lw=0.55))
    ax.text(0.50, 0.84, "layer 1 resonators", color=LAYER1_DARK,
            fontsize=7.0, ha="center", va="center")
    ax.text(0.50, 0.19, "layer 2 resonators", color=LAYER2_DARK,
            fontsize=7.0, ha="center", va="center")
    ax.add_patch(
        FancyArrowPatch(
            (0.91, 0.34),
            (0.91, 0.68),
            arrowstyle="<->",
            mutation_scale=7,
            lw=0.55,
            color=INK,
        )
    )
    ax.text(0.94, 0.51, r"$h$", fontsize=8.0, va="center", ha="left")
    ax.annotate(
        r"$T_{ij}(\theta)$",
        xy=(0.48, 0.51),
        xytext=(0.58, 0.49),
        fontsize=7.4,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=INK, lw=0.45),
    )
    ax.text(
        0.50,
        0.025,
        "programmable interlayer couplers",
        fontsize=6.8,
        ha="center",
        va="bottom",
        color=INK,
    )


def main() -> None:
    configure_style()
    scan_row = load_representative_scan_row()
    theta = float(scan_row["theta"])

    patch = load_orbit_patch(PLOT_DEPTH)
    visible = np.abs(patch.coordinates) <= DISK_CLIP
    edges_full = unique_visible_edges(patch.adjacency, visible)
    coordinates = patch.coordinates[visible]
    depths = patch.word_depths[visible]
    original_index = np.flatnonzero(visible)
    reindex = -np.ones(patch.size, dtype=np.int32)
    reindex[original_index] = np.arange(original_index.size, dtype=np.int32)
    edges = reindex[edges_full]
    rotated = rotate(coordinates, theta)

    a_b_over_a = 2.0 * R_OVER_A * math.acosh(1.0 + math.sqrt(2.0))
    if not math.isclose(a_b_over_a, 1.0, rel_tol=0.0, abs_tol=2e-15):
        raise ArithmeticError("Bolza nearest-neighbour normalization is inconsistent")
    xi_over_a = R_OVER_A * math.asinh(
        math.sinh(A_REG_OVER_A / (2.0 * R_OVER_A))
        / abs(math.sin(theta / 2.0))
    )
    rho_xi = math.tanh(xi_over_a / (2.0 * R_OVER_A))

    first_shell = np.flatnonzero(depths == 1)
    nearest_neighbor = coordinates[
        first_shell[np.argmin(np.angle(coordinates[first_shell]) % (2 * math.pi))]
    ]

    fig = plt.figure(figsize=(7.20, 4.35))
    grid = fig.add_gridspec(
        2,
        2,
        width_ratios=[2.20, 1.0],
        height_ratios=[1.08, 0.92],
        wspace=0.08,
        hspace=0.18,
        left=0.015,
        right=0.985,
        bottom=0.045,
        top=0.965,
    )
    ax_disk = fig.add_subplot(grid[:, 0])
    ax_twist = fig.add_subplot(grid[0, 1])
    ax_circuit = fig.add_subplot(grid[1, 1])

    draw_disk_panel(ax_disk, coordinates, rotated, depths, edges, theta, xi_over_a)
    draw_twist_inset(ax_twist, theta, xi_over_a, rho_xi, nearest_neighbor)
    draw_circuit_inset(ax_circuit)

    np.savez_compressed(
        HERE / "fig01a_plot_data.npz",
        layer1_coordinates=coordinates,
        layer2_coordinates=rotated,
        word_depths=depths,
        adjacency_edges=edges,
        source_element_ids=original_index,
        theta_plot=theta,
        theta_plot_over_pi=theta / math.pi,
        theta_exact_numerator=11,
        theta_exact_denominator=128,
        kappa_B_a=KAPPA_B_A,
        R_over_a=R_OVER_A,
        a_B_over_a=a_b_over_a,
        a_reg_over_a=A_REG_OVER_A,
        xi_M_over_a=xi_over_a,
        xi_M_disk_radius=rho_xi,
        h_over_a=H_OVER_A,
        lambda_perp_over_a=scan_row["lambda_perp_over_a"],
        omega_over_omega_ref=scan_row["omega_over_omega_ref"],
        combined_score=scan_row["combined_score"],
        disk_visual_clip=DISK_CLIP,
    )

    metadata = {
        "Title": "Exact-data rendering of the twisted Bolza hyperbolic bilayer",
        "Author": "5203 project",
        "Subject": "Frozen R6 Bolza centre-orbit geometry at theta=11*pi/128",
    }
    fig.savefig(
        HERE / "fig01a_exact_hyperbolic_bilayer.pdf",
        bbox_inches="tight",
        facecolor="white",
        metadata=metadata,
    )
    fig.savefig(
        HERE / "fig01a_exact_hyperbolic_bilayer.svg",
        bbox_inches="tight",
        facecolor="white",
    )
    fig.savefig(
        HERE / "fig01a_exact_hyperbolic_bilayer_600dpi.png",
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    print(f"theta_plot={theta:.15f}")
    print("theta_plot/pi=11/128")
    print(f"xi_M/a_B={xi_over_a:.15f}")
    print(f"plotted_points_per_layer={coordinates.size}")
    print(f"plotted_S8_edges_per_layer={edges.shape[0]}")
    print(f"R6_candidate_score={scan_row['combined_score']:.15f}")


if __name__ == "__main__":
    main()
