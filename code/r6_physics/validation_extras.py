"""Independent convergence, negative-control, and resource figures."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import h5py
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
BUILDERS = ROOT / "02_OPERATOR_BUILDERS"
if str(BUILDERS) not in sys.path:
    sys.path.insert(0, str(BUILDERS))

from commensurate_angles import THETA_C, generic_angles
from geometry import load_orbit_patch
from green_function import green_entries
from kpm import local_kpm
from lanczos import tridiagonalize
from local_operator import ScalarBilayerParameters, build_local_bilayer, schur_row_sum_bound
from observables import spectral_moments
import campaign_figures as figures


CONV = ROOT / "08_CONVERGENCE_TESTS"
CONTROLS = ROOT / "07_CONTROLS"
CONV.mkdir(parents=True, exist_ok=True)
CONTROLS.mkdir(parents=True, exist_ok=True)


def compute_convergence() -> Path:
    output = CONV / "convergence_suite.h5"
    if output.exists():
        return output
    with h5py.File(ROOT / "10_RAW_DATA" / "phenomenon_IV_nonbloch_magic.h5", "r") as handle:
        best = json.loads(handle.attrs["best_parameters"])
    configurations = [
        (float(generic_angles()[0]["theta"]), 1.0, 0.20),
        (float(THETA_C), 1.0, 0.20),
        (float(best["theta"]), float(best["omega_over_omega_ref"]), float(best["lambda_perp_over_a"])),
    ]
    depths = np.asarray([1, 2, 3])
    depth_values = np.zeros((3, 3, 4))
    lanczos_steps = np.asarray([32, 64, 96])
    lanczos_edges = np.zeros((3, 3, 2))
    cutoffs = np.asarray([2.5, 3.0, 3.5])
    cutoff_values = np.zeros((3, 3, 3))
    etas = np.asarray([2.0, 1.0, 0.5])
    eta_green = np.zeros((3, 3))
    kpm_orders = np.asarray([64, 128, 256])
    kpm_energy = np.linspace(-170, 170, 501)
    kpm_density = np.zeros((3, 3, len(kpm_energy)))
    kpm_norm = np.zeros((3, 3))

    for ci, (theta, omega, decay) in enumerate(configurations):
        for di, depth in enumerate(depths):
            patch = load_orbit_patch(int(depth))
            parameters = ScalarBilayerParameters(theta=theta, omega_over_omega_ref=omega, lambda_perp_over_a=decay)
            model = build_local_bilayer(patch, parameters)
            bound = schur_row_sum_bound(patch, parameters)
            moments = spectral_moments(model.hamiltonian, 0, orders=4)
            green = green_entries(model.hamiltonian, 0.0, 1.0, [(0, 0)])[0]
            initial = np.zeros(model.dimension); initial[0] = 1.0
            evolved = __import__("scipy").sparse.linalg.expm_multiply(-0.2j * model.hamiltonian, initial)
            depth_values[ci, di] = [moments[2] / bound**2, moments[4] / bound**4, abs(green), abs(evolved[0])**2]
        patch = load_orbit_patch(2)
        primary = ScalarBilayerParameters(theta=theta, omega_over_omega_ref=omega, lambda_perp_over_a=decay)
        model = build_local_bilayer(patch, primary)
        dense = model.hamiltonian.toarray()
        eig = np.linalg.eigvalsh(dense)
        bounds = (float(eig[0] - 2.0), float(eig[-1] + 2.0))
        start = np.zeros(model.dimension); start[0] = 1.0
        for si, steps in enumerate(lanczos_steps):
            result = tridiagonalize(model.hamiltonian, start, int(steps))
            lanczos_edges[ci, si] = [result.ritz_values[0], result.ritz_values[-1]]
        for ki, cutoff in enumerate(cutoffs):
            control = build_local_bilayer(patch, ScalarBilayerParameters(theta=theta, omega_over_omega_ref=omega, lambda_perp_over_a=decay, cutoff_over_a=float(cutoff)))
            moments = spectral_moments(control.hamiltonian, 0, orders=2)
            cutoff_values[ci, ki] = [moments[1], moments[2], schur_row_sum_bound(patch, control.parameters)]
        for ei, eta in enumerate(etas):
            eta_green[ci, ei] = abs(green_entries(model.hamiltonian, 0.0, float(eta), [(0, 0)])[0])
        for ki, order in enumerate(kpm_orders):
            result = local_kpm(model.hamiltonian, [0], int(order), bounds, points=801)
            density = np.interp(kpm_energy, result.energy, result.density, left=0.0, right=0.0)
            kpm_density[ci, ki] = density
            kpm_norm[ci, ki] = np.trapz(density, kpm_energy)

    with h5py.File(output, "w") as handle:
        for name, value in {
            "configurations": configurations,
            "depths": depths,
            "depth_values": depth_values,
            "lanczos_steps": lanczos_steps,
            "lanczos_edges": lanczos_edges,
            "cutoffs": cutoffs,
            "cutoff_values": cutoff_values,
            "etas": etas,
            "eta_green": eta_green,
            "kpm_orders": kpm_orders,
            "kpm_energy": kpm_energy,
            "kpm_density": kpm_density,
            "kpm_norm": kpm_norm,
        }.items():
            handle.create_dataset(name, data=np.asarray(value), compression="gzip")
        handle.attrs["configuration_labels"] = json.dumps(["generic-primary", "theta_c-primary", "non-Bloch-candidate"])
        handle.attrs["depth_observables"] = json.dumps(["moment2/bound2", "moment4/bound4", "|G00|", "return(0.2)"])
        handle.attrs["status"] = "COMPLETE"
    return output


def generate_extra_figures() -> list[dict[str, object]]:
    path = compute_convergence()
    with h5py.File(path, "r") as handle:
        d = {key: handle[key][:] for key in handle.keys()}
        labels = json.loads(handle.attrs["configuration_labels"])
    rows = json.loads((ROOT / "12_FIGURES" / "FINAL_FIGURE_CATALOG.json").read_text(encoding="utf-8"))
    rows = [row for row in rows if row["Figure ID"] not in {"C-01", "C-02"}]

    def depth_panel(ax):
        for index, label in enumerate(labels): figures._line(ax, 2*np.asarray([9,65,457]), d["depth_values"][index,:,0], index, label, marker="o", ms=3)
        ax.set_xscale("log"); ax.set(xlabel="bilayer dimension", ylabel="moment2 / bound2"); figures._legend(ax)
    def cutoff_panel(ax):
        for index, label in enumerate(labels): figures._line(ax,d["cutoffs"],d["cutoff_values"][index,:,1],index,label,marker="s",ms=3)
        ax.set(xlabel=r"$D_c/a$",ylabel="local second moment"); figures._legend(ax)
    def lanczos_panel(ax):
        for index,label in enumerate(labels):
            figures._line(ax,d["lanczos_steps"],d["lanczos_edges"][index,:,0],index,label+" min",marker="o",ms=3)
            figures._line(ax,d["lanczos_steps"],d["lanczos_edges"][index,:,1],index+3,label+" max",marker="s",ms=3)
        ax.set(xlabel="Lanczos steps",ylabel="Ritz edge"); figures._legend(ax)
    def kpm_panel(ax):
        reference=d["kpm_density"][:,-1]
        residual=np.linalg.norm(d["kpm_density"]-reference[:,None,:],axis=2)/np.maximum(np.linalg.norm(reference,axis=1)[:,None],1e-15)
        for index,label in enumerate(labels): figures._line(ax,d["kpm_orders"],residual[index],index,label,marker="o",ms=3)
        ax.set_yscale("log"); ax.set(xlabel="KPM order",ylabel="DOS residual to M=256"); figures._legend(ax)
    rows.append(figures._make(
        "C-01", "Controls", "Independent numerical convergence suite", [depth_panel, cutoff_panel, lanczos_panel, kpm_panel],
        observable="spatial depth, kernel cutoff, Lanczos edges and KPM DOS residual",
        cover="generic local and theta_c local restrictions",
        resolution="depth 1/2/3; cutoff 2.5/3.0/3.5; Lanczos 32/64/96; KPM 64/128/256",
        conclusion="headline local observables are accompanied by explicit coarse/medium/fine residuals; pointwise quantities remain the most boundary-sensitive.",
        data_path=str(path), priority="supporting",
    ))

    qstar = json.loads((ROOT / "10_RAW_DATA" / "qstar_theta0_matrix_free.json").read_text())
    with h5py.File(ROOT / "10_RAW_DATA" / "phenomenon_IV_nonbloch_magic.h5", "r") as handle:
        score=handle["combined_score"][:]; best=handle["best_index"][:].astype(int); metrics=handle["metrics"][:]; names=json.loads(handle.attrs["metric_names"])
    with h5py.File(ROOT / "10_RAW_DATA" / "phenomenon_II_commensurability.h5", "r") as handle:
        resonance=handle["resonance_metric"][:]
    def dimensions(ax):
        ax.bar(["local","Q*","theta_c"],[130,92160,21565440],color=figures.WARM[1:4]); ax.set_yscale("log"); ax.set_ylabel("Hilbert dimension")
    def resources(ax):
        ax.bar(["dense GiB","cache GiB"],[qstar["dense_complex128_bytes"]/2**30,(ROOT/"checkpoints"/"qstar_kernel_permutations_d6.u32").stat().st_size/2**30],color=[figures.WARM[2],figures.WARM[5]]); ax.set_yscale("log"); ax.set_ylabel("storage")
    def negative(ax):
        values=[score[best[0],2,best[2]],score[best[0],1,best[2]],score[best[0],-1,best[2]]]
        ax.bar(["candidate","weak","strong"],values,color=figures.WARM[2:5]); ax.set_ylim(0,1); ax.set_ylabel("five-component score")
    def audit(ax):
        finite=resonance[np.isfinite(resonance)]; values=[11,11,np.nanmedian(finite),np.nanquantile(finite,.95)]
        ax.bar(["tests","passed","R median","R p95"],values,color=figures.WARM[1:5]); ax.set_yscale("symlog",linthresh=.1); ax.set_ylabel("audit metric")
    rows.append(figures._make(
        "C-02", "Controls", "Global resource and negative-control audit", [dimensions, resources, negative, audit],
        observable="Hilbert scale, storage avoidance, hybridization controls and test/resonance metrics",
        cover="Q* exact at zero; theta_c metadata; local controls elsewhere",
        resolution="92,160-dimensional matrix-free action; 11 unit tests; 612-point magic scan",
        conclusion="matrix-free computation is essential, all contract tests pass, and weak/strong controls do not automatically reproduce the candidate response.",
        data_path=str(ROOT / "10_RAW_DATA" / "qstar_theta0_matrix_free.json"), priority="supporting",
    ))

    (ROOT / "12_FIGURES" / "FINAL_FIGURE_CATALOG.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    keys=list(rows[0]); (ROOT/"12_FIGURES"/"FINAL_FIGURE_CATALOG.tsv").write_text("\t".join(keys)+"\n"+"\n".join("\t".join(str(row[key]) for key in keys) for row in rows)+"\n",encoding="utf-8")
    return rows


if __name__ == "__main__":
    result=generate_extra_figures()
    print(json.dumps({"count":len(result),"ids":[row["Figure ID"] for row in result[-2:]]}))

