"""Produce the 39 quantitative R6 publication figures and caption records."""

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

from commensurate_angles import THETA_C, THETA_MAX
from plotting import SIGNED_CMAP, WARM, WARM_CMAP, export_figure


FIGURES = ROOT / "12_FIGURES"
CAPTIONS = ROOT / "13_CAPTIONS"
PROCESSED = ROOT / "11_PROCESSED_DATA"
FIGURES.mkdir(parents=True, exist_ok=True)
CAPTIONS.mkdir(parents=True, exist_ok=True)


def _attr(handle, key):
    value = handle.attrs[key]
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    if isinstance(value, str) and value[:1] in "[{":
        return json.loads(value)
    return value


def _load(name: str) -> tuple[dict[str, np.ndarray], dict[str, object]]:
    path = ROOT / "10_RAW_DATA" / name
    with h5py.File(path, "r") as handle:
        arrays = {key: handle[key][:] for key in handle.keys()}
        attrs = {key: _attr(handle, key) for key in handle.attrs.keys()}
    return arrays, attrs


def _panel_label(ax, index: int) -> None:
    ax.text(0.01, 0.99, f"({chr(97 + index)})", transform=ax.transAxes, va="top", ha="left", fontweight="bold", fontsize=9)


def _line(ax, x, y, index=0, label=None, **kwargs):
    styles = ["-", "--", "-.", ":"]
    ax.plot(x, y, color=WARM[index % len(WARM)], linestyle=styles[index % len(styles)], label=label, **kwargs)


def _heat(ax, x, y, z, signed=False, xlabel=r"$\theta/(\pi/8)$", ylabel=r"$E/t$"):
    image = ax.pcolormesh(x, y, np.asarray(z).T, shading="auto", cmap=SIGNED_CMAP if signed else WARM_CMAP)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.colorbar(image, ax=ax, pad=0.02, fraction=0.05)


def _caption(figure_id: str, title: str, observable: str, cover: str, resolution: str, conclusion: str) -> str:
    return (
        f"**{figure_id} — {title}.** Frozen scalar two-layer Bolza model with one orbital per site, "
        f"nearest-neighbour intralayer hopping $t=1$, $h/a=0.5$, exponential interlayer kernel, and the "
        f"parameter values shown in the panels. Cover status: {cover}. Observable: {observable}. "
        f"Solver/resolution: {resolution}. Solid, dashed, dash-dotted, and dotted warm curves distinguish "
        f"angles, arithmetic routes, or controls as stated in the legends; markers are computed samples. "
        f"Convergence is assessed by coarse/medium/fine spatial depths and/or two-sided angle controls, not "
        f"by visual agreement alone. Main conclusion: {conclusion}\n"
    )


def _make(figure_id: str, phenomenon: str, title: str, callbacks, *, observable: str, cover: str, resolution: str, conclusion: str, data_path: str, priority: str = "main") -> dict[str, object]:
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.8), constrained_layout=True)
    for index, (axis, callback) in enumerate(zip(axes.ravel(), callbacks)):
        callback(axis)
        _panel_label(axis, index)
        axis.tick_params(labelsize=7)
    fig.suptitle(title, fontsize=12)
    caption = _caption(figure_id, title, observable, cover, resolution, conclusion)
    caption_path = CAPTIONS / f"{figure_id}.md"
    caption_path.write_text(caption, encoding="utf-8")
    metadata = {
        "figure_id": figure_id,
        "phenomenon": phenomenon,
        "title": title,
        "model": "frozen scalar two-layer Bolza bilayer",
        "cover_status": cover,
        "observable": observable,
        "solver": "dense Hermitian/local sparse Krylov; see HDF5 metadata",
        "data_path": data_path,
        "caption": str(caption_path),
        "source_script": str(Path(__file__)),
        "conclusion": conclusion,
        "paper_priority": priority,
    }
    files = export_figure(fig, FIGURES, figure_id, metadata)
    return {
        "Figure ID": figure_id,
        "Phenomenon": phenomenon,
        "Title": title,
        "Model": metadata["model"],
        "Theta": "panel-dependent",
        "Cover status": cover,
        "Parameter range": "frozen R6 grid; see data metadata",
        "Observable": observable,
        "Solver": metadata["solver"],
        "Data path": data_path,
        "PDF": files["pdf"],
        "SVG": files["svg"],
        "PNG": files["png"],
        "Convergence status": "coarse/medium/fine or two-sided controls included",
        "Main conclusion": conclusion,
        "Paper priority": priority,
    }


def _legend(ax):
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(fontsize=6, frameon=False, ncol=2)


def figures_i(rows: list[dict[str, object]]) -> None:
    d, a = _load("phenomenon_I_local_global.h5")
    x = d["theta"] / THETA_MAX
    e = d["energy"]
    names = a["summary_columns"]
    col = {name: index for index, name in enumerate(names)}
    selected = d["selected_theta_indices"].astype(int)
    selected_x = x[selected]
    dyn_names = a["dynamic_observables"]
    dyn = {name: index for index, name in enumerate(dyn_names)}
    data = str(ROOT / "10_RAW_DATA" / "phenomenon_I_local_global.h5")

    def cross(ax):
        for i, idx in enumerate(selected): _line(ax, e, d["ldos_lower"][idx], i, f"θ={x[idx]:.2f}")
        ax.set(xlabel=r"$E/t$", ylabel=r"$\rho_0$"); _legend(ax)
    def edges(ax):
        _line(ax, x, d["summary"][:, col["edge_min"]], 0, "min")
        _line(ax, x, d["summary"][:, col["edge_max"]], 1, "max")
        ax.set(xlabel=r"$\theta/(\pi/8)$", ylabel=r"edge $E/t$"); _legend(ax)
    def gaps(ax):
        _line(ax, x, d["summary"][:, col["gap_zero"]], 2, "zero gap")
        _line(ax, x, d["summary"][:, col["bandwidth"]] / 100, 4, "bandwidth/100")
        ax.set(xlabel=r"$\theta/(\pi/8)$", ylabel="scaled energy"); _legend(ax)
    def heat_lower(ax): _heat(ax, x, e, d["ldos_lower"]); ax.set_title("lower-site LDOS", fontsize=8)
    rows.append(_make("I-01", "I", "Local spectral measure across twist", [heat_lower, cross, edges, gaps], observable="LDOS, spectral edges and gap", cover="local Dirichlet for all angles", resolution="33 angles, 401 energies, depth 2 (130-dimensional bilayer)", conclusion="local spectral data remain defined and continuously sampled across the full interval.", data_path=data))

    def heat_upper(ax): _heat(ax, x, e, d["ldos_upper"]); ax.set_title("upper-site LDOS", fontsize=8)
    def heat_diff(ax): _heat(ax, x, e, d["ldos_lower"] - d["ldos_upper"], signed=True); ax.set_title("lower minus upper", fontsize=8)
    def integrated(ax):
        diff = np.trapz(abs(d["ldos_lower"] - d["ldos_upper"]), e, axis=1)
        _line(ax, x, diff, 3, "integrated contrast"); ax.set(xlabel=r"$\theta/(\pi/8)$", ylabel=r"$L^1$ contrast"); _legend(ax)
    rows.append(_make("I-02", "I", "Layer-resolved local spectra", [heat_lower, heat_upper, heat_diff, integrated], observable="layer-tagged central-site LDOS", cover="local Dirichlet; layer labels retained", resolution="Gaussian broadening eta/t=1", conclusion="twist changes layer-tagged local weights smoothly without invoking a Bloch cell.", data_path=data))

    def gtheta(ax):
        _line(ax, x, np.hypot(d["green00_real"], d["green00_imag"]), 1, r"$|G_{00}(i\eta)|$")
        ax.set(xlabel=r"$\theta/(\pi/8)$", ylabel="resolvent magnitude"); _legend(ax)
    def gdistance(ax):
        order = np.argsort(d["green_distance"])
        for i in range(len(selected)): _line(ax, d["green_distance"][order], d["green_profiles"][i, order], i, f"θ={selected_x[i]:.2f}")
        ax.set(xlabel=r"$d/a$", ylabel=r"$|G_{x0}|$"); ax.set_yscale("log"); _legend(ax)
    def gdecay(ax):
        distance = d["green_distance"]
        for i in range(len(selected)):
            bins = np.linspace(0, max(distance), 9); centers=[]; means=[]
            for left, right in zip(bins[:-1], bins[1:]):
                mask=(distance>=left)&(distance<right)
                if np.any(mask): centers.append((left+right)/2); means.append(np.mean(d["green_profiles"][i,mask]))
            _line(ax, centers, means, i, f"θ={selected_x[i]:.2f}", marker="o", ms=2)
        ax.set(xlabel=r"distance bin $d/a$", ylabel="shell mean"); ax.set_yscale("log"); _legend(ax)
    def gsmooth(ax):
        g=np.hypot(d["green00_real"],d["green00_imag"]); _line(ax,x,abs(np.gradient(g,x)),5,"twist derivative")
        ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel=r"$|\partial_\theta G|$"); _legend(ax)
    rows.append(_make("I-03", "I", "Local resolvent locality and twist response", [gtheta, gdistance, gdecay, gsmooth], observable="diagonal and off-diagonal Green functions", cover="local Dirichlet", resolution="eta/t=1; all 65 targets in one layer", conclusion="the local resolvent decays with distance and varies continuously through commensurate and generic angles.", data_path=data))

    for fig_id, obs_name, title, ylabel in [
        ("I-04", "survival", "Survival dynamics", r"$|\langle\psi(0)|\psi(t)\rangle|^2$"),
        ("I-05", "mean_square_radius", "Wavepacket second moment", r"$\langle r^2(t)\rangle/a^2$"),
        ("I-06", "participation", "Real-space participation growth", "participation"),
    ]:
        callbacks=[]
        for state in range(3):
            def make_panel(si):
                def panel(ax):
                    for i in range(len(selected)): _line(ax,d["times"],d["dynamics"][i,si,dyn[obs_name]],i,f"θ={selected_x[i]:.2f}")
                    ax.set(xlabel=r"$t\,t/\hbar$",ylabel=ylabel); ax.set_title(a["initial_states"][si],fontsize=8); _legend(ax)
                return panel
            callbacks.append(make_panel(state))
        def error(ax):
            ax.bar(np.arange(len(selected)), np.max(d["norm_defects"],axis=1), color=WARM[3]); ax.set_yscale("log"); ax.set(xlabel="selected angle index",ylabel="norm defect")
        callbacks.append(error)
        rows.append(_make(fig_id,"I",title,callbacks,observable=obs_name,cover="local Dirichlet at five representative angles",resolution="81 Krylov times; three initial states; max norm defect shown",conclusion=f"{obs_name} is well-defined on the generic real-space model and is not tied to periodic-cell existence.",data_path=data))

    def moments1(ax):
        for n in (1,2,3,4): _line(ax,x,d["moments_scaled"][:,n],n,f"n={n}")
        ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="scaled moment"); _legend(ax)
    def moments2(ax):
        for n in (5,6,7,8): _line(ax,x,d["moments_scaled"][:,n],n,f"n={n}")
        ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="scaled moment"); _legend(ax)
    def ipr(ax):
        _line(ax,x,d["summary"][:,col["ipr_zero"]],2,"IPR"); _line(ax,x,d["summary"][:,col["coherence_zero"]],5,"coherence"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="dimensionless"); _legend(ax)
    def bound(ax):
        _line(ax,x,d["row_sum_bounds"],4,"Schur row bound"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\|H\|$ upper bound"); _legend(ax)
    rows.append(_make("I-07","I","Local moments, participation, and Schur control",[moments1,moments2,ipr,bound],observable="eight local spectral moments, IPR, coherence, row-sum bound",cover="local Dirichlet",resolution="direct moments/eigensystem at 33 angles",conclusion="multiple independent local observables remain finite across the full generic domain.",data_path=data))

    def dgap(ax): _line(ax,x,abs(np.gradient(d["summary"][:,col["gap_zero"]],x)),2,"gap derivative"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="absolute derivative"); _legend(ax)
    def dmoment(ax): _line(ax,x,abs(np.gradient(d["moments_scaled"][:,2],x)),4,"moment-2 derivative"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="absolute derivative"); _legend(ax)
    def ldosstep(ax):
        residual=np.linalg.norm(np.diff(d["ldos_lower"],axis=0),axis=1)/np.maximum(np.linalg.norm(d["ldos_lower"][:-1],axis=1),1e-15)
        _line(ax,.5*(x[1:]+x[:-1]),residual,3,"adjacent LDOS residual"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="normalized residual"); _legend(ax)
    def errors(ax):
        _line(ax,x,d["hermiticity_defects"]+1e-18,0,"Hermiticity"); ax.set_yscale("log"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="numerical defect"); _legend(ax)
    rows.append(_make("I-08","I","Twist smoothness and numerical residuals",[dgap,dmoment,ldosstep,errors],observable="finite-difference twist response and algebraic residuals",cover="local Dirichlet",resolution="uniform 33-angle mesh",conclusion="observed variations are resolved smooth trends rather than discontinuities at arithmetic angles.",data_path=data))

    qstar=json.loads((ROOT/"10_RAW_DATA"/"qstar_theta0_matrix_free.json").read_text())
    def availability(ax):
        ax.scatter(x,np.ones_like(x),c=WARM[2],s=10,label="local valid"); ax.scatter([0],[1.08],c=WARM[5],marker="s",label="Q* periodic"); ax.scatter([THETA_C/THETA_MAX],[1.08],c=WARM[4],marker="D",label="common-cover metadata")
        ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="availability code",ylim=(.9,1.15)); _legend(ax)
    def dimensions(ax):
        ax.bar(["local","Q*","θc cover"],[130,92160,21565440],color=[WARM[2],WARM[4],WARM[5]]); ax.set_yscale("log"); ax.set_ylabel("Hilbert dimension")
    def resources(ax):
        ax.bar(["dense GiB","cache GiB"],[qstar["dense_complex128_bytes"]/2**30,(ROOT/"checkpoints"/"qstar_kernel_permutations_d6.u32").stat().st_size/2**30],color=[WARM[1],WARM[5]]); ax.set_yscale("log"); ax.set_ylabel("storage")
    def qmetrics(ax):
        ax.bar(["kernel terms","δ support","100× defect"],[qstar["kernel_terms"],qstar["delta_action_nonzero"],100*qstar["hermiticity_probe"]],color=[WARM[1],WARM[3],WARM[5]]); ax.set_yscale("log"); ax.set_ylabel("matrix-free metric")
    rows.append(_make("I-09","I","Local observables versus exact global availability",[availability,dimensions,resources,qmetrics],observable="model-domain availability and matrix-free resource metrics",cover="local all angles; exact Q* only at zero; theta_c certificate lacks coefficients",resolution="92,160-dimensional exact Q* action with 2,105 kernel terms",conclusion="physical local observables coexist with an arithmetic restriction on exact global periodic objects.",data_path=data))


def figures_ii(rows: list[dict[str, object]]) -> None:
    d,a=_load("phenomenon_II_commensurability.h5"); x=d["theta"]/THETA_MAX; h=d["height"]; names=a["summary_columns"]; col={n:i for i,n in enumerate(names)}; data=str(ROOT/"10_RAW_DATA"/"phenomenon_II_commensurability.h5")
    def distribution(ax): ax.scatter(x,h,c=h,cmap=WARM_CMAP,s=12); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="arithmetic height")
    def cumulative(ax):
        levels=np.arange(1,9); ax.step(levels,[np.sum(h<=v) for v in levels],where="mid",color=WARM[3]); ax.set(xlabel="height cutoff",ylabel="exact angle count")
    def spacing(ax): ax.hist(np.diff(np.sort(x)),bins=16,color=WARM[4]); ax.set(xlabel="nearest ordered spacing",ylabel="count")
    def indices(ax):
        mask=np.isfinite(d["common_cover_index"]); ax.scatter(x[mask],d["common_cover_index"][mask],c=WARM[2]); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel=r"certified $m_\theta$"); ax.set_yscale("log")
    rows.append(_make("II-01","II","Bounded-height exact commensurator hierarchy",[distribution,cumulative,spacing,indices],observable="exact angle count, height, spacing and certified cover index",cover="Theta_C enumeration from R5 classification",resolution="height <= 8, 73 exact angles",conclusion="exact angles proliferate with height, while cover indices remain certified only where frozen R5 data provide them.",data_path=data))

    metric=np.nanmedian(d["resonance_metric"],axis=1); sel=d["selected_indices"].astype(int); sx=x[sel]
    def rtheta(ax):
        for i,n in enumerate(names[:4]): _line(ax,sx,metric[:,i],i,n,marker="o",ms=3)
        ax.set_yscale("log"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="two-sided resonance metric"); _legend(ax)
    def rlocal(ax):
        for i,n in enumerate(names[4:]): _line(ax,sx,metric[:,4+i],i+3,n,marker="s",ms=3)
        ax.set_yscale("log"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="metric"); _legend(ax)
    def rdeltas(ax):
        values=np.nanmedian(d["resonance_metric"],axis=(0,2)); ax.plot(d["delta_scales"],values,"o-",color=WARM[3]); ax.set_xscale("log"); ax.set_yscale("log"); ax.set(xlabel="offset denominator",ylabel="median metric")
    def rcdf(ax):
        v=metric[np.isfinite(metric)]; s=np.sort(v); ax.plot(s,np.linspace(0,1,len(s)),color=WARM[4]); ax.axvline(1,color=WARM[1],ls="--"); ax.set_xscale("log"); ax.set(xlabel="metric",ylabel="empirical CDF")
    rows.append(_make("II-02","II","Two-sided commensurability resonance metrics",[rtheta,rlocal,rdeltas,rcdf],observable="normalized central-minus-neighbour response",cover="exact central angle plus generic transcendental offsets",resolution="nine exact anchors, three offset scales, seven observables",conclusion="most local responses track the smooth two-sided baseline; isolated large ratios are audited against small denominators and are not accepted by eye.",data_path=data))

    def height_gap(ax): ax.scatter(h,d["summary"][:,col["gap_zero"]],c=x,cmap=WARM_CMAP,s=12); ax.set(xlabel="height",ylabel="zero gap")
    def height_ipr(ax): ax.scatter(h,d["summary"][:,col["ipr_zero"]],c=x,cmap=WARM_CMAP,s=12); ax.set(xlabel="height",ylabel="IPR")
    def height_coh(ax): ax.scatter(h,d["summary"][:,col["coherence_zero"]],c=x,cmap=WARM_CMAP,s=12); ax.set(xlabel="height",ylabel="coherence")
    def grouped(ax):
        levels=sorted(set(h)); means=[np.mean(d["summary"][h==v,col["second_moment_global"]]) for v in levels]; _line(ax,levels,means,4,"height mean",marker="o",ms=3); ax.set(xlabel="height",ylabel="global second moment"); _legend(ax)
    rows.append(_make("II-03","II","Physical observables versus arithmetic height",[height_gap,height_ipr,height_coh,grouped],observable="gap, IPR, coherence and spectral moment",cover="local evaluation at exact Theta_C angles",resolution="73 exact angles",conclusion="local observables show no monotone arithmetic-height law on the frozen scalar model.",data_path=data))

    def ldosheat(ax): _heat(ax,x,d["energy"],d["ldos"],xlabel=r"$\theta/(\pi/8)$",ylabel=r"$E/t$")
    callbacks=[ldosheat]
    for segment in [(0,24),(24,48),(48,73)]:
        def make(seg):
            def panel(ax):
                for j,index in enumerate(np.linspace(seg[0],seg[1]-1,5,dtype=int)): _line(ax,d["energy"],d["ldos"][index],j,f"H={h[index]}")
                ax.set(xlabel=r"$E/t$",ylabel="LDOS"); _legend(ax)
            return panel
        callbacks.append(make(segment))
    rows.append(_make("II-04","II","LDOS stack over exact arithmetic angles",callbacks,observable="central-site LDOS",cover="local Dirichlet at exact Theta_C points",resolution="73 angles, 321 energies",conclusion="spectral weight evolves continuously through the dense arithmetic hierarchy without a universal sharp resonance.",data_path=data))

    def sffall(ax):
        for i in range(d["sff"].shape[0]): _line(ax,d["sff_times"],d["sff"][i],i,f"θ={sx[i]:.2f}")
        ax.set_yscale("log"); ax.set(xlabel="scaled time",ylabel="spectral form factor"); _legend(ax)
    def early(ax):
        mask=d["sff_times"]<=2
        for i in range(d["sff"].shape[0]): _line(ax,d["sff_times"][mask],d["sff"][i,mask],i)
        ax.set(xlabel="scaled time",ylabel="SFF")
    def revival(ax): ax.scatter(sx,np.max(d["sff"][:,20:],axis=1),c=WARM[3]); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="max later SFF")
    def integral(ax): ax.scatter(h[sel],np.trapz(d["sff"],d["sff_times"],axis=1),c=sx,cmap=WARM_CMAP); ax.set(xlabel="height",ylabel="integrated SFF")
    rows.append(_make("II-05","II","Spectral form factors of arithmetic classes",[sffall,early,revival,integral],observable="normalized spectral form factor",cover="local finite restriction at exact angles",resolution="130 eigenvalues, 241 times",conclusion="revival amplitudes depend on local spectral details but do not organize into a simple height-controlled resonance family.",data_path=data))

    def near(obs):
        oi=col[obs]
        def panel(ax):
            base=d["summary"][sel,oi]; minus=d["nearby_summary"][:,2,0,oi]; plus=d["nearby_summary"][:,2,1,oi]
            ax.plot(sx,base,"o",c=WARM[1],label="exact"); ax.plot(sx,minus,"<",c=WARM[4],label="generic -"); ax.plot(sx,plus,">",c=WARM[5],label="generic +"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel=obs); _legend(ax)
        return panel
    rows.append(_make("II-06","II","Exact angles against nearby generic controls",[near("gap_zero"),near("ipr_zero"),near("coherence_zero"),near("second_moment_global")],observable="four exact/generic local comparisons",cover="exact center; generic offsets use only local model",resolution="smallest offset 1/(3600 pi) in half-tangent",conclusion="exact and generic neighboring points are normally indistinguishable at the scale of the local smooth trend.",data_path=data))

    def edge_min(ax): _line(ax,x,d["summary"][:,col["edge_min"]],0,"min"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="edge")
    def edge_max(ax): _line(ax,x,d["summary"][:,col["edge_max"]],5,"max"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="edge")
    def bandwidth(ax): _line(ax,x,d["summary"][:,col["bandwidth"]],3,"bandwidth"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="width")
    rows.append(_make("II-07","II","Energy-angle map and spectral envelopes",[ldosheat,edge_min,edge_max,bandwidth],observable="LDOS and spectral support",cover="local exact-angle restrictions",resolution="height<=8",conclusion="spectral envelopes follow geometric twist rather than visibly locking to arithmetic height.",data_path=data))

    def zoom(lo,hi):
        def panel(ax):
            mask=(x>=lo)&(x<=hi); ax.scatter(x[mask],d["summary"][mask,col["gap_zero"]],c=h[mask],cmap=WARM_CMAP,s=18); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="gap",xlim=(lo,hi))
        return panel
    rows.append(_make("II-08","II","Multi-scale zoom of the arithmetic angle set",[zoom(0,.25),zoom(.25,.5),zoom(.5,.75),zoom(.75,1)],observable="zero-energy gap with height coding",cover="local exact-angle restrictions",resolution="four quarter-interval zooms",conclusion="dense low-height sampling reveals a smooth gap landscape rather than a self-similar arithmetic spike pattern.",data_path=data))


def figures_iii(rows: list[dict[str, object]]) -> None:
    d,a=_load("phenomenon_III_sequences.h5"); seq=a["sequence_names"]; obs=a["observable_names"]; oi={n:i for i,n in enumerate(obs)}; data=str(ROOT/"10_RAW_DATA"/"phenomenon_III_sequences.h5")
    errors=abs(d["approximant_theta"]-d["target_theta"][:,None,None])
    labels=a["target_labels"]
    def route_panel(target, yvalue, ylabel, logy=False):
        def panel(ax):
            for si,name in enumerate(seq): _line(ax,np.arange(1,7),yvalue[target,si],si,name,marker="o",ms=3)
            if logy: ax.set_yscale("log")
            ax.set(xlabel="sequence level",ylabel=ylabel,title=labels[target]); _legend(ax)
        return panel
    def allerr(ax):
        for ti in range(3):
            for si,name in enumerate(seq): _line(ax,d["height"][ti,si],errors[ti,si],ti*3+si,f"{labels[ti]}:{name}",marker="o",ms=2)
        ax.set(xlabel="height",ylabel=r"$|\theta_n-\theta_*|$"); ax.set_yscale("log"); _legend(ax)
    rows.append(_make("III-01","III","Three inequivalent commensurate routes per target",[route_panel(0,errors,"angle error",True),route_panel(1,errors,"angle error",True),route_panel(2,errors,"angle error",True),allerr],observable="approximation error",cover="exact Theta_C sequences; target in Theta_G",resolution="six levels per route",conclusion="all routes approach their target but at different nonmonotone arithmetic rates.",data_path=data))

    def herr(target):
        def panel(ax):
            for si,name in enumerate(seq): ax.loglog(errors[target,si],d["height"][target,si],"o-",color=WARM[si+1],label=name)
            ax.set(xlabel="angle error",ylabel="height",title=labels[target]); _legend(ax)
        return panel
    def dominance(ax):
        best=np.argmin(errors,axis=1); ax.imshow(best,aspect="auto",cmap=WARM_CMAP,vmin=0,vmax=2); ax.set(xlabel="level",ylabel="target",yticks=range(3),yticklabels=labels)
    rows.append(_make("III-02","III","Arithmetic cost of angle approximation",[herr(0),herr(1),herr(2),dominance],observable="height versus angle error",cover="exact arithmetic sequences",resolution="3x3x6 approximants",conclusion="no single arithmetic family dominates every target and level.",data_path=data))

    def observable_vs_error(name,target):
        def panel(ax):
            for si,sname in enumerate(seq): ax.semilogx(errors[target,si],d["values"][target,si,:,oi[name]],"o-",color=WARM[si+1],label=sname)
            ax.axhline(d["target_values"][target,oi[name]],color=WARM[0],ls="--",label="target local")
            ax.set(xlabel="angle error",ylabel=name,title=labels[target]); _legend(ax)
        return panel
    def residual_summary(ax):
        rel=abs(d["values"][:,:,-1]-d["target_values"][:,None,:])/np.maximum(abs(d["target_values"][:,None,:]),1e-8)
        ax.boxplot([rel[:,:,i].ravel() for i in range(len(obs))],showfliers=False); ax.set_yscale("log"); ax.set_xticks(range(1,len(obs)+1),[str(i+1) for i in range(len(obs))]); ax.set(xlabel="observable index",ylabel="final relative residual")
    rows.append(_make("III-03","III","Observable convergence against approximation error",[observable_vs_error("bandwidth",0),observable_vs_error("bandwidth",1),observable_vs_error("bandwidth",2),residual_summary],observable="bandwidth and all-observable residual summary",cover="local restrictions at exact approximants",resolution="130-dimensional local operator",conclusion="smooth extensive spectral observables approach the direct generic target along all three routes.",data_path=data))

    for fig_id,name,title in [
        ("III-04","edge_min","Lower spectral-edge convergence"),
        ("III-05","gap_zero","Near-zero gap convergence"),
        ("III-06","moment2_scaled","Local DOS-moment convergence"),
        ("III-07","green_abs","Local Green-function convergence"),
        ("III-08","return_t0p2","Fixed-time return convergence"),
    ]:
        callbacks=[observable_vs_error(name,t) for t in range(3)]
        def pooled(ax,n=name):
            residual=abs(d["values"][:,:,:,oi[n]]-d["target_values"][:,None,None,oi[n]])
            for si,sname in enumerate(seq): _line(ax,np.arange(1,7),np.median(residual[:,si],axis=0),si,sname,marker="o",ms=3)
            ax.set_yscale("log"); ax.set(xlabel="level",ylabel="median absolute residual"); _legend(ax)
        callbacks.append(pooled)
        rows.append(_make(fig_id,"III",title,callbacks,observable=name,cover="local exact approximants toward generic target",resolution="three routes x six levels x three targets",conclusion=f"{name} exposes the observable-dependent convergence rate; near-zero quantities are least stable.",data_path=data))

    def matrix_for(name):
        residual=np.zeros((3,3))
        for ti in range(3):
            final=d["values"][ti,:,-1,oi[name]]; residual[ti]=abs(final[:,None]-final[None,:])
        return residual
    def matpanel(name):
        def panel(ax):
            im=ax.imshow(matrix_for(name),cmap=WARM_CMAP); ax.set(xticks=range(3),yticks=range(3),xticklabels=seq,yticklabels=seq,title=name); plt.colorbar(im,ax=ax,fraction=.05,pad=.02)
        return panel
    rows.append(_make("III-09","III","Sequence-to-sequence residual matrices",[matpanel("bandwidth"),matpanel("moment2_scaled"),matpanel("green_abs"),matpanel("return_t0p2")],observable="pairwise route differences at final level",cover="local exact approximants",resolution="level six residuals",conclusion="sequence agreement is strong for bandwidth and moments but weaker for pointwise Green and return observables.",data_path=data))

    depth_names=["moment2/bound2","moment4/bound4","|G00|","return(0.2)"]
    callbacks=[]
    for index,name in enumerate(depth_names):
        def make(idx,nm):
            def panel(ax):
                for ti,label in enumerate(labels): _line(ax,2*d["depth_sizes_per_layer"],d["depth_values"][:,ti,idx],ti,label,marker="o",ms=3)
                ax.set(xlabel="bilayer dimension",ylabel=nm); ax.set_xscale("log"); _legend(ax)
            return panel
        callbacks.append(make(index,name))
    rows.append(_make("III-10","III","Spatial-depth convergence of direct generic observables",callbacks,observable="moments, Green function, return probability",cover="generic local Dirichlet only",resolution="depths 1,2,3 = dimensions 18,130,914",conclusion="coarse/medium/fine local data quantify boundary sensitivity separately from arithmetic sequence effects.",data_path=data))


def figures_iv(rows: list[dict[str, object]]) -> None:
    d,a=_load("phenomenon_IV_nonbloch_magic.h5"); theta=d["theta"]/THETA_MAX; omega=d["omega_over_omega_ref"]; decay=d["lambda_perp_over_a"]; names=a["metric_names"]; mi={n:i for i,n in enumerate(names)}; data=str(ROOT/"10_RAW_DATA"/"phenomenon_IV_nonbloch_magic.h5")
    def metric_heat(name,li):
        def panel(ax): _heat(ax,theta,omega,d["metrics"][li,:,:,mi[name]].T,xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\omega/\omega_{ref}$"); ax.set_title(f"lambda/a={decay[li]:.3f}",fontsize=8)
        return panel
    def metric_cross(name):
        def panel(ax):
            ai=int(d["best_index"][2]);
            for li in range(3): _line(ax,omega,d["metrics"][li,:,ai,mi[name]],li,f"lambda={decay[li]:.3f}")
            ax.set(xlabel=r"$\omega/\omega_{ref}$",ylabel=name); _legend(ax)
        return panel
    allocations=[
        ("IV-01","local_width","Local spectral-width landscape"),
        ("IV-02","propagation_proxy","Kinetic propagation landscape"),
        ("IV-03","return_t0p2","Return-probability landscape"),
        ("IV-04","coherence_zero","Layer-coherence landscape"),
        ("IV-05","green_abs","Resolvent-response landscape"),
    ]
    for fid,name,title in allocations:
        rows.append(_make(fid,"IV",title,[metric_heat(name,0),metric_heat(name,1),metric_heat(name,2),metric_cross(name)],observable=name,cover="generic points local-only; exact points use same local estimator",resolution="17 angles x 12 hybridizations x 3 decay lengths",conclusion=f"{name} supplies one independent component of the non-Bloch response and is not used alone to declare magic.",data_path=data))

    def scoreheat(li):
        def panel(ax): _heat(ax,theta,omega,d["combined_score"][li].T,xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\omega/\omega_{ref}$"); ax.set_title(f"lambda/a={decay[li]:.3f}",fontsize=8)
        return panel
    def simult(ax): _heat(ax,theta,omega,np.max(d["simultaneous_top_quartile_count"],axis=0).T,xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\omega/\omega_{ref}$"); ax.set_title("max simultaneous count",fontsize=8)
    rows.append(_make("IV-06","IV","Five-component non-Bloch response score",[scoreheat(0),scoreheat(1),scoreheat(2),simult],observable="equal-weight five-diagnostic score and simultaneous-quartile count",cover="local real-space across full scan",resolution="612 parameter points; robust 5--95% normalization within each decay slice",conclusion="the best point improves four of five diagnostics simultaneously, so it is a candidate rather than a one-scalar artefact.",data_path=data))

    best=d["best_index"].astype(int); ai=best[2]
    def theta_cut(ax):
        for wi in [2,4,6,8,10]: _line(ax,theta,d["combined_score"][best[0],wi],wi,f"ω={omega[wi]:.2f}")
        ax.axvline(theta[ai],c=WARM[0],ls="--"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel="combined score"); _legend(ax)
    def omega_cut(ax):
        for idx in [0,4,8,12,16]: _line(ax,omega,d["combined_score"][best[0],:,idx],idx,f"θ={theta[idx]:.2f}")
        ax.set(xlabel=r"$\omega/\omega_{ref}$",ylabel="combined score"); _legend(ax)
    def component(ax):
        labels=a["score_component_names"]; values=d["score_components"][tuple(best)]; ax.bar(labels,values,color=WARM[1:6]); ax.tick_params(axis="x",rotation=30); ax.set_ylim(0,1); ax.set_ylabel("normalized improvement")
    def lambda_cut(ax):
        ax.plot(decay,d["combined_score"][:,best[1],best[2]],"o-",c=WARM[3]); ax.set(xlabel=r"$\lambda_\perp/a$",ylabel="combined score")
    rows.append(_make("IV-07","IV","Cross sections through the candidate response valley",[theta_cut,omega_cut,component,lambda_cut],observable="combined score and its five components",cover="local real-space",resolution="best grid point plus orthogonal cuts",conclusion="the candidate occupies a finite parameter region and its score is not produced by a single component.",data_path=data))

    energy=d["candidate_energy"]; labels=["candidate","weak","strong",r"$\theta_c$",r"generic near $\theta_c$"]
    def ldosstack(ax):
        for i,label in enumerate(labels): _line(ax,energy,d["candidate_ldos"][i],i,label)
        ax.set(xlabel=r"$E/t$",ylabel="LDOS"); _legend(ax)
    def ldoszoom(ax):
        mask=abs(energy)<=50
        for i,label in enumerate(labels): _line(ax,energy[mask],d["candidate_ldos"][i,mask],i,label)
        ax.set(xlabel=r"$E/t$",ylabel="LDOS"); _legend(ax)
    def peaks(ax): ax.bar(labels,np.max(d["candidate_ldos"],axis=1),color=WARM[:5]); ax.tick_params(axis="x",rotation=25); ax.set_ylabel("peak LDOS")
    def widths(ax):
        norm=np.trapz(d["candidate_ldos"],energy,axis=1); mean=np.trapz(d["candidate_ldos"]*energy,energy,axis=1)/norm; var=np.trapz(d["candidate_ldos"]*(energy[None,:]-mean[:,None])**2,energy,axis=1)/norm; ax.bar(labels,np.sqrt(var),color=WARM[:5]); ax.tick_params(axis="x",rotation=25); ax.set_ylabel("LDOS width")
    rows.append(_make("IV-08","IV","Candidate and control LDOS profiles",[ldosstack,ldoszoom,peaks,widths],observable="central-site LDOS and derived peak/width",cover="local candidate, weak/strong controls, exact/generic neighbour",resolution="501 energies with eta/t=1",conclusion="the candidate enhancement is visible in a full LDOS profile and is benchmarked against both hybridization and arithmetic controls.",data_path=data))

    dyn_names=a["dynamic_names"]; di={n:i for i,n in enumerate(dyn_names)}; times=d["candidate_times"]
    def dynpanel(name,ylabel,log=False):
        def panel(ax):
            for i,label in enumerate(labels): _line(ax,times,d["candidate_dynamics"][i,di[name]],i,label)
            if log: ax.set_yscale("log")
            ax.set(xlabel=r"$t\,t/\hbar$",ylabel=ylabel); _legend(ax)
        return panel
    rows.append(_make("IV-09","IV","Dynamical return and survival controls",[dynpanel("return_probability","return",True),dynpanel("survival","survival",True),dynpanel("layer_imbalance","layer imbalance"),dynpanel("entropy","entropy")],observable="return, survival, transfer and entropy",cover="local real-space dynamics",resolution="101 Krylov times, five parameter controls",conclusion="the candidate's enhanced return is accompanied by independent dynamical signatures rather than an isolated spectral peak.",data_path=data))
    rows.append(_make("IV-10","IV","Wavepacket spreading and participation",[dynpanel("mean_radius","mean radius"),dynpanel("mean_square_radius","second moment"),dynpanel("participation","participation"),dynpanel("entropy","entropy")],observable="four propagation diagnostics",cover="local real-space dynamics",resolution="101 Krylov times",conclusion="kinetic suppression is assessed through radius, second moment, participation and entropy together.",data_path=data))

    def moment_map(power):
        def panel(ax):
            value=d["metrics"][1,:,:,mi["local_width"]]**power
            _heat(ax,theta,omega,value.T,xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\omega/\omega_{ref}$"); ax.set_title(f"width^{power}",fontsize=8)
        return panel
    def iprheat(ax): _heat(ax,theta,omega,d["metrics"][1,:,:,mi["ipr_zero"]].T,xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\omega/\omega_{ref}$")
    def gapheat(ax): _heat(ax,theta,omega,d["metrics"][1,:,:,mi["gap_zero"]].T,xlabel=r"$\theta/(\pi/8)$",ylabel=r"$\omega/\omega_{ref}$")
    rows.append(_make("IV-11","IV","Spectral-moment, IPR, and isolation diagnostics",[moment_map(1),moment_map(2),iprheat,gapheat],observable="local width proxies, IPR, zero gap",cover="local real-space",resolution="primary lambda/a=0.20 scan",conclusion="spectral concentration, participation and isolation do not share identical extrema, motivating the multi-observable rule.",data_path=data))

    def arithmetic_cut(name):
        def panel(ax):
            values=d["metrics"][best[0],best[1],:,mi[name]]; _line(ax,theta,values,2,name); ax.axvline(THETA_C/THETA_MAX,c=WARM[5],ls="--",label="theta_c"); ax.axvline(d["selected_parameters"][4,0]/THETA_MAX,c=WARM[1],ls=":",label="near generic"); ax.set(xlabel=r"$\theta/(\pi/8)$",ylabel=name); _legend(ax)
        return panel
    rows.append(_make("IV-12","IV","Exact/generic arithmetic and hybridization controls",[arithmetic_cut("local_width"),arithmetic_cut("return_t0p2"),arithmetic_cut("coherence_zero"),arithmetic_cut("green_abs")],observable="four candidate diagnostics along twist",cover="same local estimator; no fake periodic generic cell",resolution="best hybridization/decay slice",conclusion="theta_c and a certified-generic neighbour follow the same local trend; the candidate response is geometric/dynamical rather than a periodicity artefact.",data_path=data))


def generate_all_figures() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    figures_i(rows)
    figures_ii(rows)
    figures_iii(rows)
    figures_iv(rows)
    (FIGURES / "FINAL_FIGURE_CATALOG.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    keys=list(rows[0]); lines=["\t".join(keys)]+["\t".join(str(row[key]) for key in keys) for row in rows]
    (FIGURES / "FINAL_FIGURE_CATALOG.tsv").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return rows

