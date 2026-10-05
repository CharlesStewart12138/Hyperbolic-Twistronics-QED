from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

from suite_core import (
    ROOT, WARM, NEUTRAL, as_float, export_figure, make_figure, panel,
    read_csv, read_json, save_long_data, series_records,
)


REGISTRY = {}


def register(fig_id):
    def deco(fn):
        REGISTRY[fig_id] = fn
        return fn
    return deco


FC_ROOT = ROOT / "reproducibility/data/hyperbolic_finite_cover_convergence"
SHELL = FC_ROOT / "shell_budgets.csv"
COVER = FC_ROOT / "cover_sequence.csv"
CROSS = FC_ROOT / "cross_cover_diagnostics.csv"
EDGES = FC_ROOT / "no_loss_no_pollution.csv"
COVER_SPEC = FC_ROOT / "cover_spectral_sets.csv"
ORBIT = ROOT / "reproducibility/data/hyperbolic_geometry_reconstruction/group_orbit_sample.csv"
INF_CERT = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/04_INFINITE_OPERATOR/INFINITE_OPERATOR_CERTIFICATE.tex"
SPEC_ROOT = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction"
FINITE_SPEC = SPEC_ROOT / "finite_spectrum.csv"
OBS = SPEC_ROOT / "target_observables.csv"
DOS_ROOT = ROOT / "reproducibility/data/hyperbolic_dos_reconstruction"
RESOLVED_DOS = DOS_ROOT / "resolved_dos.csv"
EXACT_SPEC = DOS_ROOT / "exact_spectrum.csv"
BROAD_DOS = DOS_ROOT / "broadening_dos.csv"
BROAD_SCHED = DOS_ROOT / "broadening_schedule.csv"
DOS_CDF = DOS_ROOT / "dos_cdf.csv"
DOS_AUDIT = DOS_ROOT / "dos_audit.json"


def finish(fig_id, fig, axes, title, panels, sources, source_type, exactness, tier,
           xvars, yvars, params, observation, records, transformations):
    data_path, _ = save_long_data(fig_id, records, sources, source_type, transformations)
    return export_figure(fig_id, fig, axes, title, panels, sources, source_type,
                         exactness, tier, xvars, yvars, params, observation,
                         data_path, transformations)


@register("FIG37")
def fig37():
    title="Finite-patch Schur row-sum convergence and derivative tails"
    fig,ax=make_figure(title); rows=read_csv(SHELL); depth=np.array([int(r["retained_word_depth"]) for r in rows])
    c0=np.array([as_float(r["C0_operator_tail_bound_over_t"]) for r in rows]);c1=np.array([as_float(r["C1_derivative_tail_bound_over_t"]) for r in rows]);c2=np.array([as_float(r["C2_Hessian_tail_bound_over_t"]) for r in rows])
    retained=np.array([int(r["retained_coefficient_count"]) for r in rows]);omitted=np.array([int(r["omitted_coefficient_count_within_patch"]) for r in rows])
    ax[0].semilogy(depth,np.maximum(c0,1e-16),marker="o",color=WARM[2],lw=1.2,label="$C^0$")
    ax[0].semilogy(depth,np.maximum(c1,1e-16),marker="s",color=WARM[4],lw=1.1,label="$C^1$")
    ax[0].semilogy(depth,np.maximum(c2,1e-16),marker="D",color=WARM[6],lw=1.1,label="$C^2$")
    ax[1].plot(depth,retained,marker="o",color=WARM[3],lw=1.2,label="retained");ax[1].plot(depth,omitted,marker="s",color=WARM[5],lw=1.1,ls="--",label="omitted")
    ax[2].plot(depth,retained/(retained+omitted),marker="D",color=WARM[4],lw=1.2)
    ax[3].plot(depth,c1/np.maximum(c0,1e-16),marker="o",color=WARM[3],lw=1.2,label="$C^1/C^0$")
    ax[3].plot(depth,c2/np.maximum(c0,1e-16),marker="s",color=WARM[6],lw=1.1,label="$C^2/C^0$")
    panel(ax[0],"a","Certified finite-patch tails","retained word depth","tail bound / $t$")
    panel(ax[1],"b","Retained and omitted coefficients","retained word depth","coefficient count")
    panel(ax[2],"c","Patch coverage fraction","retained word depth","retained fraction")
    panel(ax[3],"d","Derivative amplification of the tail","retained word depth","tail ratio")
    ax[0].legend();ax[1].legend();ax[3].legend()
    records=series_records("a","C0 tail",depth,c0,"retained_word_depth","tail_bound_over_t")
    records+=series_records("a","C1 tail",depth,c1,"retained_word_depth","tail_bound_over_t")
    records+=series_records("a","C2 tail",depth,c2,"retained_word_depth","tail_bound_over_t")
    return finish("FIG37",fig,ax,title,
        ["Frozen $C^0$, $C^1$, and $C^2$ finite-patch tail budgets.","Retained versus omitted coefficient counts.","Retained fraction of the available patch.","Derivative-tail amplification ratios."],
        [SHELL],"FROZEN_NUMERICAL_TAIL_TABLE","finite available-patch certificate",
        "EXTENDED_DATA_TIER_B","word depth","tail bounds and counts","available patch depth 3",
        "all three finite-patch tails vanish at depth three, but the source explicitly does not promote this to an infinite-kernel convergence certificate.",records,
        ["log scaling","ratios","coverage fraction"])


def schur_curves():
    n=np.arange(0,16,dtype=float);kappa_a=3.057141839;h=0.5;C=34.67406453;lams=np.array([0.125,0.20,0.25])
    curves=[]
    for lam in lams:
        growth=C*np.exp(n*kappa_a);decay=np.exp(h/lam)*np.exp(-n/lam);product=growth*decay
        tail=C*np.exp(h/lam)*np.exp(-n*(1/lam-kappa_a))/(1-np.exp(-(1/lam-kappa_a)))
        curves.append((lam,growth,decay,product,tail))
    return n,curves


@register("FIG38")
def fig38():
    title="Exponential hopping decay versus hyperbolic shell growth"
    fig,ax=make_figure(title);n,curves=schur_curves();records=[]
    growth=curves[0][1]
    ax[0].semilogy(n,growth,color=WARM[0],lw=1.2,label="shell-count bound")
    for i,(lam,g,d,p,t) in enumerate(curves):
        ax[0].semilogy(n,d,color=WARM[i+3],lw=1.0,ls="--",label=rf"decay $\lambda/a={lam}$")
        ax[1].semilogy(n,p,color=WARM[i+3],lw=1.15,label=rf"$\lambda/a={lam}$")
        ax[2].semilogy(n,t,color=WARM[i+3],lw=1.15)
        records+=series_records("b",f"lambda={lam}",n,p,"shell_index","growth_times_decay_bound",f"lambda_over_a={lam}")
    margins=np.array([4.942858161,1.942858161,.942858161]);ax[3].bar(np.arange(3),margins,color=WARM[3:6]);ax[3].axhline(0,color=NEUTRAL,lw=.7,ls="-.")
    panel(ax[0],"a","Competing exponentials","shell index $n$","individual factor")
    panel(ax[1],"b","Shell-weighted hopping majorant","shell index $n$","shell contribution / $|w|$")
    panel(ax[2],"c","Remaining geometric-series tail","cutoff shell $n$","tail bound / $|w|$")
    panel(ax[3],"d","Strict convergence margins",r"$\lambda_\perp/a_B$",r"$a/\lambda_\perp-\kappa_Ba$")
    ax[0].legend(ncol=2);ax[1].legend();ax[3].set_xticks(range(3),["0.125","0.20","0.25"])
    return finish("FIG38",fig,ax,title,
        ["Uniform shell-growth bound and three frozen hopping decays.","Their products, which determine Schur summability.","Rigorous remaining-tail majorants.","Positive exponent margins."],
        [INF_CERT],"ANALYTIC_VISUALIZATION_EVALUATION","proved upper-bound formula",
        "MAIN_TEXT_TIER_A","shell index; lambda_perp/a_B","growth; decay; shell product; tail","kappa_B a=3.057141839; h/a=0.5",
        "all three frozen decays beat hyperbolic shell growth, with the slowest decay retaining a positive margin 0.942858.",records,
        ["proved exponential bounds","geometric-series tail","log scale"])


@register("FIG39")
def fig39():
    title="Certified hopping-tail bounds versus cutoff"
    fig,ax=make_figure(title);n,curves=schur_curves();records=[]
    for i,(lam,g,d,p,t) in enumerate(curves):
        ax[0].semilogy(n,t,color=WARM[i+3],lw=1.2,label=rf"$\lambda/a={lam}$")
        ax[1].semilogy(n,t/t[0],color=WARM[i+3],lw=1.2)
        ax[2].semilogy(n,np.r_[t[1:]/t[:-1],np.nan],color=WARM[i+3],lw=1.2)
        ax[3].semilogy(n,p,color=WARM[i+3],lw=1.2)
        records+=series_records("a",f"lambda={lam}",n,t,"cutoff_shell","Schur_tail_over_abs_w",f"lambda_over_a={lam}")
    panel(ax[0],"a","Absolute Schur tail majorant","cutoff shell $n$","tail / $|w|$")
    panel(ax[1],"b","Normalized tail","cutoff shell $n$",r"$T_{>n}/T_{>0}$")
    panel(ax[2],"c","Successive tail ratio","cutoff shell $n$",r"$T_{>n+1}/T_{>n}$")
    panel(ax[3],"d","Single-shell contribution","shell index $n$","shell term / $|w|$")
    ax[0].legend()
    return finish("FIG39",fig,ax,title,
        ["Rigorous infinite-tail majorant.","Normalization by the zero-cutoff bound.","Constant geometric-series ratios.","Single-shell bound."],
        [INF_CERT],"ANALYTIC_VISUALIZATION_EVALUATION","proved upper-bound formula",
        "EXTENDED_DATA_TIER_B","cutoff shell","absolute and normalized tails","three frozen decay lengths",
        "the certified tail decreases geometrically for every frozen kernel, most slowly for $\lambda_\perp/a_B=0.25$.",records,
        ["geometric tail evaluation","normalization","successive ratio"])


@register("FIG40")
def fig40():
    title="Local finite-support counts versus geodesic radius"
    fig,ax=make_figure(title);rows=read_csv(ORBIT);rad=np.array([as_float(r["geodesic_radius_over_r"]) for r in rows]);depth=np.array([int(r["word_depth"]) for r in rows])
    finite=rad[np.isfinite(rad)];grid=np.linspace(0,max(finite),220);count=np.array([(finite<=x).sum() for x in grid])
    kappa_a=3.057141839;C=34.67406453;n=np.arange(0,5);shell_bound=C*np.exp(n*kappa_a);cum_bound=np.cumsum(shell_bound)
    unique_depth=np.arange(depth.max()+1);depth_count=np.array([(depth==d).sum() for d in unique_depth]);cum_depth=np.cumsum(depth_count)
    cutoffs=np.array([2.5,3.0,3.5]);rho=np.sqrt(cutoffs**2-.5**2)
    support=np.array([(finite<=r*kappa_a).sum() for r in rho])
    ax[0].step(grid,count,where="post",color=WARM[2],lw=1.2)
    ax[1].semilogy(unique_depth,depth_count,marker="o",color=WARM[3],lw=1.2,label="actual sample");ax[1].semilogy(n,shell_bound,ls="--",color=WARM[6],lw=1.0,label="uniform bound")
    ax[2].semilogy(unique_depth,cum_depth,marker="s",color=WARM[4],lw=1.2);ax[2].semilogy(n,cum_bound,ls=":",color=WARM[7],lw=1.0)
    ax[3].plot(cutoffs,support,marker="D",color=WARM[5],lw=1.2)
    panel(ax[0],"a","Actual cumulative orbit sample","geodesic radius $d/R$","sites with radius $\leq d$")
    panel(ax[1],"b","Shell cardinality and analytic bound","word/shell index","cardinality")
    panel(ax[2],"c","Cumulative count comparison","word/shell index","cumulative cardinality")
    panel(ax[3],"d","Frozen product-distance cutoffs",r"$D_c/a_B$","sample sites within projected radius")
    ax[1].legend()
    records=series_records("a","actual cumulative",grid,count,"geodesic_radius_over_R","cumulative_site_count")
    records+=series_records("d","cutoff support",cutoffs,support,"D_c_over_aB","sample_support_count")
    return finish("FIG40",fig,ax,title,
        ["Cumulative site count in the frozen exact orbit sample.","Actual depth counts and the proved uniform shell bound.","Cumulative actual/bound comparison.","Counts induced by the three frozen cutoffs."],
        [ORBIT,INF_CERT],"FROZEN_NUMERICAL_ORBIT_SAMPLE + ANALYTIC_BOUND","exact sample and rigorous upper bound",
        "EXTENDED_DATA_TIER_B","radius; depth; cutoff","site/shell counts","D_c/a_B={2.5,3.0,3.5}",
        "finite cutoffs retain finite support, while the rigorous shell bound remains deliberately conservative.",records,
        ["cumulative counts","shell aggregation","proved bound evaluation"])


@register("FIG41")
def fig41():
    title="Frozen 512-dimensional finite-cover spectrum"
    fig,ax=make_figure(title);rows=read_csv(FINITE_SPEC);e=np.array([as_float(r["energy_over_t"]) for r in rows]);idx=np.arange(len(e));target=np.array([r["target_island"]=="True" for r in rows])
    ax[0].scatter(idx,e,s=6,color=WARM[2],alpha=.75);ax[0].scatter(idx[target],e[target],s=12,color=WARM[6])
    ax[1].hist(e,bins=60,color=WARM[3],edgecolor=WARM[0],lw=.35)
    es=np.sort(e);ax[2].step(es,np.arange(1,len(es)+1)/len(es),where="post",color=WARM[4],lw=1.2)
    spac=np.diff(es);ax[3].hist(spac,bins=np.geomspace(max(spac[spac>1e-12].min(),1e-10),max(spac.max(),1e-9),36),color=WARM[5]);ax[3].set_xscale("log")
    panel(ax[0],"a","Eigenvalue index plot","eigenvalue index",r"$E/t$")
    panel(ax[1],"b","Eigenvalue density histogram",r"$E/t$","count")
    panel(ax[2],"c","Empirical spectral CDF",r"$E/t$","cumulative weight")
    panel(ax[3],"d","Positive level-spacing distribution",r"$\Delta E/t$","count")
    records=series_records("a","finite spectrum",idx,e,"eigenvalue_index","energy_over_t")
    records+=series_records("c","spectral CDF",es,np.arange(1,len(es)+1)/len(es),"energy_over_t","cdf")
    return finish("FIG41",fig,ax,title,
        ["All frozen finite eigenvalues; target-island states are highlighted.","Energy histogram.","Empirical cumulative distribution.","Positive nearest-level spacings."],
        [FINITE_SPEC],"FROZEN_NUMERICAL_SPECTRUM","registered dense eigensolver output",
        "MAIN_TEXT_TIER_A","eigenvalue index; energy","energy; density; CDF; spacing","512-dimensional validation Hamiltonian",
        "the finite spectrum contains a highly structured degenerate target island embedded between separated spectral clusters.",records,
        ["sorting","histogram","empirical CDF","positive spacing filter"])


@register("FIG42")
def fig42():
    title="Frozen density of states, projected channels, and broadening error"
    fig,ax=make_figure(title);rows=read_csv(RESOLVED_DOS);by=defaultdict(list)
    for r in rows: by[r["resolution_id"]].append(r)
    def curve(name):
        rr=by[name];return np.array([as_float(x["energy_over_t"]) for x in rr]),np.array([as_float(x["density_over_t_inverse"]) for x in rr])
    glob=curve("global");even=curve("layer_even_projector");odd=curve("layer_odd_projector");target=curve("target_root_projector")
    ax[0].plot(*glob,color=WARM[2],lw=1.0)
    ax[1].plot(*even,color=WARM[3],lw=1.0,label="even");ax[1].plot(*odd,color=WARM[5],lw=.9,ls="--",label="odd")
    mask=(target[0]>120)&(target[0]<150);ax[2].plot(target[0][mask],target[1][mask],color=WARM[6],lw=1.1,label="target projector");ax[2].plot(even[0][mask],even[1][mask],color=WARM[3],lw=.8,ls="-.",label="even")
    sched=read_csv(BROAD_SCHED);eta=np.array([as_float(r["eta_over_t"]) for r in sched]);kerr=np.array([as_float(r["kpm_exact_density_linf"]) for r in sched]);serr=np.array([as_float(r["slq_exact_density_linf"]) for r in sched])
    ax[3].loglog(eta,kerr,marker="o",color=WARM[4],lw=1.1,label="KPM–exact");ax[3].loglog(eta,serr,marker="s",color=WARM[7],lw=1.1,label="SLQ–exact")
    panel(ax[0],"a","Global resolved DOS",r"$E/t$",r"$t\rho(E)$")
    panel(ax[1],"b","Layer-parity projected DOS",r"$E/t$",r"$t\rho_P(E)$")
    panel(ax[2],"c","Target-root spectral window",r"$E/t$",r"$t\rho_P(E)$")
    panel(ax[3],"d","Broadening-error schedule",r"$\eta/t$",r"$L^\infty$ density error")
    ax[1].legend();ax[2].legend();ax[3].legend()
    records=series_records("a","global",glob[0],glob[1],"energy_over_t","density_over_t_inverse")
    records+=series_records("b","even",even[0],even[1],"energy_over_t","projected_density")
    records+=series_records("b","odd",odd[0],odd[1],"energy_over_t","projected_density")
    records+=series_records("d","KPM error",eta,kerr,"eta_over_t","density_linf_error")
    records+=series_records("d","SLQ error",eta,serr,"eta_over_t","density_linf_error")
    return finish("FIG42",fig,ax,title,
        ["Global Lorentzian-resolved DOS.","Even and odd layer-projector channels.","Target-root window.","Frozen KPM/SLQ errors versus broadening."],
        [RESOLVED_DOS,BROAD_SCHED,DOS_AUDIT],"FROZEN_NUMERICAL_DOS","registered 512-dimensional spectral measures",
        "MAIN_TEXT_TIER_A","energy; broadening","DOS; projected DOS; error","registered eta schedule",
        "the target pole is layer-even selective, and SLQ stays closer to the exact broadened DOS across the frozen schedule.",records,
        ["channel filtering","energy-window filtering","log error comparison"])


@register("FIG43")
def fig43():
    title="Coupling-resolved bandwidth, gap, curvature, and target DOS"
    fig,ax=make_figure(title);obs=read_csv(OBS);u=np.array([as_float(r["w_over_w_star"]) for r in obs]);bw=np.array([as_float(r["even_bandwidth_over_t"]) for r in obs]);gap=np.array([as_float(r["signed_lower_isolation_gap_over_t"]) for r in obs]);hess=np.array([as_float(r["maximum_absolute_hessian_over_t"]) for r in obs])
    rows=read_csv(RESOLVED_DOS);target=[r for r in rows if r["resolution_id"]=="target_root_projector"];e=np.array([as_float(r["energy_over_t"]) for r in target]);d=np.array([as_float(r["density_over_t_inverse"]) for r in target]);mask=(e>120)&(e<150)
    ax[0].plot(u,bw,marker="o",color=WARM[2],lw=1.2)
    ax[1].plot(u,gap,marker="s",color=WARM[3],lw=1.2)
    ax[2].plot(u,hess,marker="D",color=WARM[4],lw=1.2)
    ax[3].plot(e[mask],d[mask],color=WARM[6],lw=1.1);ax[3].axvline(140.36861265335298,color=NEUTRAL,lw=.7,ls="--")
    for a in ax[:3]:a.axvline(1,color=NEUTRAL,lw=.7,ls="--")
    panel(ax[0],"a","Even-sector bandwidth",r"$w/w_*$",r"$W_+/t$")
    panel(ax[1],"b","Signed isolation gap",r"$w/w_*$",r"$\Delta^L/t$")
    panel(ax[2],"c","Maximum Hodge curvature",r"$w/w_*$",r"$\max|\lambda_i|/t$")
    panel(ax[3],"d","Target-projector DOS at the frozen root",r"$E/t$",r"$t\rho_{P_*}(E)$")
    records=series_records("a","bandwidth",u,bw,"w_over_w_star","bandwidth_over_t")
    records+=series_records("b","gap",u,gap,"w_over_w_star","gap_over_t")
    records+=series_records("c","hessian",u,hess,"w_over_w_star","max_abs_hessian_over_t")
    records+=series_records("d","target DOS",e[mask],d[mask],"energy_over_t","target_projected_density")
    return finish("FIG43",fig,ax,title,
        ["Bandwidth closes at the root.","Isolation gap remains positive.","All Hodge curvature magnitudes vanish.","Target-projector DOS near the root energy."],
        [OBS,RESOLVED_DOS],"FROZEN_NUMERICAL_VALIDATION","exact first-shell observables plus frozen DOS",
        "EXTENDED_DATA_TIER_B","w/w_*; energy","bandwidth; gap; Hessian; DOS","w*/t=140.36861265335298",
        "the frozen validation fixture combines flat target dispersion, open isolation gap, zero Hessian, and a resolved target-projector spectral peak.",records,
        ["direct extraction","target energy window"])


@register("FIG44")
def fig44():
    title="Finite-cover validation towers and restricted convergence diagnostics"
    fig,ax=make_figure(title);cover=read_csv(COVER);cross=read_csv(CROSS);edges=read_csv(EDGES)
    by=defaultdict(list)
    for r in cover:by[r["tower_id"]].append(r)
    records=[]
    for i,(tower,rr) in enumerate(by.items()):
        rr.sort(key=lambda r:int(r["level"]));degree=np.array([int(r["cover_degree"]) for r in rr]);mod=np.array([int(r["modulus"]) for r in rr]);err=np.array([as_float(r["C0_Hausdorff_error_over_t"]) for r in rr]);radius=np.array([as_float(r["word_injectivity_radius"]) for r in rr])
        ax[0].loglog(mod,degree,marker="o",color=WARM[i+2],lw=1.2,label=tower)
        ax[1].loglog(degree,err,marker="s",color=WARM[i+2],lw=1.2)
        ax[2].semilogx(degree,radius,marker="D",color=WARM[i+2],lw=1.2)
        records+=series_records("a",tower,mod,degree,"modulus","cover_degree")
        records+=series_records("b",tower,degree,err,"cover_degree","C0_Hausdorff_error_over_t")
    dist=np.array([as_float(r["cdf_kolmogorov_distance"]) for r in cross]);ax[3].bar(np.arange(len(dist)),dist,color=[WARM[2+i%6] for i in range(len(dist))])
    panel(ax[0],"a","Explicit cover-degree growth","modulus","cover degree")
    panel(ax[1],"b","Declared-sector Hausdorff error","cover degree",r"$C^0$ error / $t$")
    panel(ax[2],"c","Word injectivity radius","cover degree","word injectivity radius")
    panel(ax[3],"d","Cross-cover spectral CDF distance","cover comparison","Kolmogorov distance")
    ax[0].legend();ax[2].axhline(2,color=NEUTRAL,lw=.7,ls="--");ax[3].set_xticks(range(len(dist)),[f"{r['left_modulus']}→{r['right_modulus']}" for r in cross],rotation=30)
    records+=series_records("d","CDF comparisons",np.arange(len(dist)),dist,"comparison_index","Kolmogorov_distance")
    return finish("FIG44",fig,ax,title,
        ["Two explicit Abelian validation towers.","Restricted-sector one-sided/Hausdorff error.","The word injectivity radius remains fixed at two.","Successive and cross-tower CDF distances."],
        [COVER,CROSS,EDGES],"FROZEN_NUMERICAL_FINITE_COVER_DATA","declared-sector validation values",
        "MAIN_TEXT_TIER_A","modulus; cover degree; comparison","degree; error; injectivity radius; CDF distance","two registered towers",
        "spectral diagnostics improve with cover degree, but the fixed injectivity radius prevents promotion to a full-group bulk-convergence claim.",records,
        ["grouping by tower","log scaling","cross-cover comparison"])

