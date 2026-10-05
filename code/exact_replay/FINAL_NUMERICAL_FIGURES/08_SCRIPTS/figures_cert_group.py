from __future__ import annotations

import math
from collections import Counter

import numpy as np

from suite_core import (
    ROOT, WARM, NEUTRAL, WARM_CMAP, as_float, export_figure, make_figure,
    panel, read_csv, read_json, save_long_data, series_records,
)


REGISTRY = {}


def register(fig_id):
    def deco(fn):
        REGISTRY[fig_id] = fn
        return fn
    return deco


R4_ROOT = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CAND_DIR = R4_ROOT / "10_CANDIDATES"
GLOBAL_SUM = R4_ROOT / "PAPER_INTEGRATION_R4/FIGURE_DATA/GLOBAL_SCAN_SUMMARY.tsv"
CEGAR = R4_ROOT / "PAPER_INTEGRATION_R4/FIGURE_DATA/CEGAR_ITERATIONS.tsv"
FALSE_POS = R4_ROOT / "11_CERTIFICATES/CAND-R4-0005.independent_v1_false_hit_quarantine.json"
SEP_NPZ = ROOT / "data/production/quotient_separator/separator_matrix.npz"
SEP_MANIFEST = ROOT / "data/production/quotient_separator/candidate_manifest.tsv"
SUBGROUP = R4_ROOT / "18_Q24_CLOSURE/SL2_9_SUBGROUP_CLASS_AUDIT.tsv"
FAITHFUL = R4_ROOT / "18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_CERTIFICATE.json"
TRANSITIVE = R4_ROOT / "18_Q24_CLOSURE/MIN_TRANSITIVE_DEGREE_CERTIFICATE.json"
COMM_CERT = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/05_CONSTRUCTIVE_COMMENSURATOR/R5_COMM_EXAMPLE_CERTIFICATE.json"
COMM_REG = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/05_CONSTRUCTIVE_COMMENSURATOR/R5_COMM_BRANCH_REGISTRY.tsv"
COMM_TEX = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/06_COMMENSURATOR_APPROXIMATION/COMMENSURATOR_APPROXIMATION.tex"


def finish(fig_id, fig, axes, title, panels, sources, source_type, exactness, tier,
           xvars, yvars, params, observation, records, transformations):
    data_path, _ = save_long_data(fig_id, records, sources, source_type, transformations)
    return export_figure(fig_id, fig, axes, title, panels, sources, source_type,
                         exactness, tier, xvars, yvars, params, observation,
                         data_path, transformations)


def candidates():
    rows = []
    for index in range(1, 6):
        obj = read_json(CAND_DIR / f"CAND-R4-{index:04d}.certificate.json")
        resource = obj.get("resource", {})
        witness = obj.get("accumulated_witness_invariant", {}).get("witness_count")
        if witness is None:
            witness = 1 if obj.get("local_failure_witness") or obj.get("global_failure_witness") else 0
        local = obj.get("local_ball", {})
        rows.append({
            "id": f"{index:04d}", "order": obj["actual_order"], "witnesses": witness,
            "records": resource.get("global_registry_scanned_records", local.get("exact_elements", 0)),
            "elapsed": resource.get("global_scan_elapsed_seconds", float("nan")),
            "local_exact": local.get("exact_elements", 0),
            "local_distinct": local.get("distinct_candidate_images", 0),
            "class": obj["classification"],
            "depth": obj.get("global_failure_witness", {}).get("record_depth", 0),
            "hit_index": obj.get("global_failure_witness", {}).get("record_index_zero_based", float("nan")),
        })
    return rows


@register("FIG21")
def fig21():
    title = "R4 candidate quotient progression"
    fig, ax = make_figure(title)
    data = candidates(); x=np.arange(1,6)
    order=np.array([r["order"] for r in data]); wit=np.array([r["witnesses"] for r in data])
    rec=np.array([r["records"] for r in data],float); local=np.array([r["local_distinct"] for r in data])
    ax[0].plot(x,order,marker="o",color=WARM[2],lw=1.2); ax[0].axhline(50000,color=NEUTRAL,ls="-.",lw=.7)
    ax[1].step(x,wit,where="mid",color=WARM[3],lw=1.2); ax[1].scatter(x,wit,color=WARM[3],s=22)
    ax[2].semilogy(x,rec,marker="s",color=WARM[4],lw=1.2)
    ax[3].plot(x,local,marker="D",color=WARM[5],lw=1.2); ax[3].axhline(457,color=NEUTRAL,ls="--",lw=.7)
    labels=[r["id"] for r in data]
    panel(ax[0],"a","Actual quotient order","candidate",r"$|Q|$")
    panel(ax[1],"b","Accumulated witness count","candidate","witnesses")
    panel(ax[2],"c","Authoritative records examined","candidate","records")
    panel(ax[3],"d","Distinct local-ball images","candidate",r"distinct images in $B_{\rm geom}(3)$")
    for a in ax: a.set_xticks(x,labels,rotation=25)
    records=series_records("a","order",x,order,"candidate_index","group_order")
    records+=series_records("b","witnesses",x,wit,"candidate_index","accumulated_witnesses")
    records+=series_records("c","records",x,rec,"candidate_index","records_examined")
    return finish("FIG21",fig,ax,title,
        ["Actual generated quotient order and the frozen 50,000 cap.","Cumulative exact witness growth.","Local or global records examined before disposition.","Local $B_{\rm geom}(3)$ image counts; 457 is complete."],
        [CEGAR]+[CAND_DIR/f"CAND-R4-{i:04d}.certificate.json" for i in range(1,6)],"FROZEN_NUMERICAL_SEARCH_HISTORY","exact certificate counts",
        "MAIN_TEXT_TIER_A","candidate ID","order; witnesses; records; local images","five sequential R4 candidates",
        "the successful fifth candidate preserves all 457 local images and survives the full 785,639,753-record closed domain.",records,
        ["certificate field extraction","log scaling"])


@register("FIG22")
def fig22():
    title="Global scan depth by R4 candidate"
    fig,ax=make_figure(title); data=candidates()[1:]
    x=np.arange(2,6); rec=np.array([r["records"] for r in data],float); frac=rec/785639753
    elapsed=np.array([r["elapsed"] for r in data]); throughput=rec/elapsed
    depth=np.array([r["depth"] for r in data])
    ax[0].semilogy(x,rec,marker="o",color=WARM[2],lw=1.2);ax[0].axhline(785639753,color=NEUTRAL,ls="--",lw=.7)
    ax[1].plot(x,frac,marker="s",color=WARM[3],lw=1.2)
    ax[2].semilogy(x,elapsed,marker="D",color=WARM[4],lw=1.2)
    ax[3].plot(x,throughput/1e6,marker="^",color=WARM[5],lw=1.2)
    labels=[f"{i:04d}" for i in x]
    panel(ax[0],"a","First hit or complete depth","candidate","scan records")
    panel(ax[1],"b","Fraction of closed domain scanned","candidate","scan fraction")
    panel(ax[2],"c","Elapsed scan time","candidate","seconds")
    panel(ax[3],"d","Average throughput","candidate","million records/s")
    for a in ax:a.set_xticks(x,labels)
    records=series_records("a","scan depth",x,rec,"candidate_index","records")
    records+=series_records("b","domain fraction",x,frac,"candidate_index","fraction")
    records+=series_records("d","throughput",x,throughput,"candidate_index","records_per_second")
    return finish("FIG22",fig,ax,title,
        ["First exact dangerous hit for candidates 0002–0004 and complete depth for 0005.","Fraction of the fixed registry examined.","Frozen elapsed times.","Derived average rates."],
        [CAND_DIR/f"CAND-R4-{i:04d}.certificate.json" for i in range(2,6)],"FROZEN_NUMERICAL_SEARCH_HISTORY","exact record counts; derived rates",
        "MAIN_TEXT_TIER_A","candidate ID","scan depth; time; throughput","closed domain=785,639,753 records",
        "only candidate 0005 reaches 100% of the closed registry; earlier candidates fail near 2.5–2.8 million records.",records,
        ["fraction","records/elapsed time","log scaling"])


@register("FIG23")
def fig23():
    title="CEGAR quotient-order growth and refinement efficiency"
    fig,ax=make_figure(title); data=candidates(); it=np.arange(1,6); order=np.array([r["order"] for r in data],float)
    growth=np.r_[np.nan,order[1:]/order[:-1]]; cap_margin=50000-order
    efficiency=np.array([r["witnesses"] for r in data])/order
    ax[0].plot(it,order,marker="o",color=WARM[2],lw=1.2);ax[0].axhline(50000,color=NEUTRAL,ls="-.",lw=.7)
    ax[1].plot(it[1:],growth[1:],marker="s",color=WARM[3],lw=1.2);ax[1].axhline(1,color=NEUTRAL,ls="--",lw=.7)
    ax[2].plot(it,cap_margin,marker="D",color=WARM[4],lw=1.2)
    ax[3].semilogy(it,np.maximum(efficiency,1e-8),marker="^",color=WARM[5],lw=1.2)
    panel(ax[0],"a","Actual order by CEGAR iteration","iteration",r"$|Q_i|$")
    panel(ax[1],"b","Successive order ratio","iteration",r"$|Q_i|/|Q_{i-1}|$")
    panel(ax[2],"c","Remaining order-cap margin","iteration",r"$50,000-|Q_i|$")
    panel(ax[3],"d","Witness density","iteration","witnesses per group element")
    records=series_records("a","group order",it,order,"iteration","group_order")
    records+=series_records("c","cap margin",it,cap_margin,"iteration","order_cap_margin")
    return finish("FIG23",fig,ax,title,
        ["Nonmonotone restart then strict refinements of the generated image order.","Multiplicative order change.","Distance to the frozen cap.","Exact witness count normalized by quotient order."],
        [CEGAR]+[CAND_DIR/f"CAND-R4-{i:04d}.certificate.json" for i in range(1,6)],"FROZEN_NUMERICAL_SEARCH_HISTORY","exact counts",
        "EXTENDED_DATA_TIER_B","iteration","order and derived ratios","order cap=50,000",
        "the final valid refinement reaches order 46,080 without exceeding the preregistered ceiling.",records,
        ["successive ratio","cap subtraction","normalization"])


@register("FIG24")
def fig24():
    title="Witness accumulation versus quotient complexity"
    fig,ax=make_figure(title); data=candidates(); order=np.array([r["order"] for r in data]); wit=np.array([r["witnesses"] for r in data])
    local=np.array([r["local_distinct"] for r in data]); rec=np.array([r["records"] for r in data],float)
    ax[0].scatter(order,wit,c=WARM[2:7],s=30);ax[0].plot(order,wit,color=WARM[0],lw=.7,ls="--")
    ax[1].scatter(order,local,c=WARM[2:7],s=30)
    ax[2].loglog(order,rec,marker="o",color=WARM[4],lw=1.2)
    ax[3].plot(wit,local,marker="D",color=WARM[5],lw=1.2)
    panel(ax[0],"a","Witness count versus group order",r"$|Q|$","accumulated witnesses")
    panel(ax[1],"b","Local injectivity versus order",r"$|Q|$","distinct local images")
    panel(ax[2],"c","Certification work versus order",r"$|Q|$","records examined")
    panel(ax[3],"d","Witness–local-coverage relation","witnesses","distinct local images")
    for i,r in enumerate(data): ax[0].annotate(r["id"],(order[i],wit[i]),xytext=(3,3),textcoords="offset points",fontsize=5.7)
    records=series_records("a","candidates",order,wit,"group_order","accumulated_witnesses")
    records+=series_records("b","candidates",order,local,"group_order","distinct_local_images")
    return finish("FIG24",fig,ax,title,
        ["Exact accumulated witnesses against actual group order.","Local-image coverage.","Records examined on log–log axes.","Relation between witness accumulation and local injectivity."],
        [CAND_DIR/f"CAND-R4-{i:04d}.certificate.json" for i in range(1,6)],"FROZEN_NUMERICAL_SEARCH_HISTORY","exact counts",
        "SUPPLEMENT_TIER_C","group order; witnesses","witnesses; local coverage; records","five candidates",
        "witness separation grows to fourteen while complete local injectivity is retained from candidate 0002 onward.",records,
        ["cross-variable comparison","log scaling"])


@register("FIG25")
def fig25():
    title="Frozen separator coverage matrix and exception statistics"
    fig,ax=make_figure(title)
    with np.load(SEP_NPZ,allow_pickle=False) as z:
        indptr=z["zero_indptr"].copy(); indices=z["zero_orbit_indices"].copy(); weights=z["orbit_weight"].copy()
        families=z["candidate_families"].astype(str); selected=z["selected_columns"].copy()
        n_orbits,n_cols=map(int,z["orbit_matrix_shape"])
    cols=np.unique(np.linspace(0,n_cols-1,80,dtype=int)); rows=np.unique(np.linspace(0,n_orbits-1,120,dtype=int))
    row_lookup={int(v):i for i,v in enumerate(rows)}; mat=np.ones((len(rows),len(cols)),dtype=np.uint8)
    zero_counts=np.diff(indptr)
    for j,c in enumerate(cols):
        for orbit in indices[indptr[c]:indptr[c+1]]:
            idx=row_lookup.get(int(orbit))
            if idx is not None: mat[idx,j]=0
    im=ax[0].imshow(mat,aspect="auto",origin="lower",cmap=WARM_CMAP,vmin=0,vmax=1,interpolation="nearest")
    ax[1].semilogy(np.arange(n_cols),zero_counts+1, color=WARM[2],lw=.8)
    family_counts=Counter(families.tolist()); names=list(family_counts); counts=np.array([family_counts[n] for n in names])
    order=np.argsort(counts)[::-1][:12]; ax[2].bar(np.arange(len(order)),counts[order],color=[WARM[2+i%7] for i in range(len(order))])
    weighted=np.array([weights[indices[indptr[c]:indptr[c+1]]].sum() for c in range(n_cols)],float)
    ax[3].semilogy(np.arange(n_cols),weighted+1,color=WARM[5],lw=.8);ax[3].scatter(selected,weighted[selected]+1,color=WARM[0],s=28,marker="D")
    panel(ax[0],"a","Sampled orbit-by-separator matrix","sampled separator column","sampled orbit row")
    panel(ax[1],"b","Zero-exception count by separator","separator column","zero orbit exceptions + 1")
    panel(ax[2],"c","Candidate-family distribution","family rank","number of separator columns")
    panel(ax[3],"d","Element-weighted uncovered mass","separator column","weighted exceptions + 1")
    ax[2].set_xticks(np.arange(len(order)),[names[i][:10] for i in order],rotation=55,ha="right")
    records=series_records("b","zero exceptions",np.arange(n_cols),zero_counts,"separator_column","zero_orbit_exceptions")
    records+=series_records("d","weighted exceptions",np.arange(n_cols),weighted,"separator_column","uncovered_element_weight")
    return finish("FIG25",fig,ax,title,
        ["Deterministic 120×80 sample of the actual 1,446,488×1,182 orbit matrix; one means separated.",
         "Exact sparse zero count for every column.","Counts of candidate families.","Orbit-weighted uncovered mass; the selected column is marked."],
        [SEP_NPZ,SEP_MANIFEST],"FROZEN_NUMERICAL_SPARSE_MATRIX","exact sparse exceptions; deterministic display sampling",
        "EXTENDED_DATA_TIER_B","orbit row; separator column","binary separation; exception counts","1,446,488 orbit rows; 1,182 columns",
        "the frozen matrix is overwhelmingly separating, while exception burdens vary by orders of magnitude across candidate columns.",records,
        ["sparse exception reconstruction","deterministic row/column sampling","weighted aggregation"])


@register("FIG26")
def fig26():
    title="CAND-R4-0005 complete-scan progress from frozen endpoints"
    fig,ax=make_figure(title)
    cand=read_json(CAND_DIR/"CAND-R4-0005.certificate.json"); total=785639753.0
    t_primary=171.573; t_ind=212.492
    frac=np.linspace(0,1,240)
    tp=frac*t_primary; ti=frac*t_ind; rec=frac*total
    ax[0].plot(tp,rec/1e6,color=WARM[2],lw=1.2,label="primary display interpolation")
    ax[0].plot(ti,rec/1e6,color=WARM[5],lw=1.0,ls="-.",label="independent display interpolation")
    ax[1].plot(frac,rec/total,color=WARM[3],lw=1.2)
    ax[2].plot(frac,np.full_like(frac,total/t_primary/1e6),color=WARM[2],lw=1.2,label="primary average")
    ax[2].plot(frac,np.full_like(frac,total/t_ind/1e6),color=WARM[5],lw=1.0,ls="--",label="independent average")
    ax[3].plot(frac,np.zeros_like(frac),color=WARM[4],lw=1.2);ax[3].axhline(1,color=NEUTRAL,lw=.7,ls=":")
    panel(ax[0],"a","Processed records versus elapsed time","elapsed seconds","records (millions)")
    panel(ax[1],"b","Closed-domain completion fraction","display progress fraction","registry fraction")
    panel(ax[2],"c","Endpoint-derived average throughput","display progress fraction","million records/s")
    panel(ax[3],"d","Kernel hits during certified scans","display progress fraction","kernel hits")
    ax[0].legend();ax[2].legend()
    records=series_records("a","primary linear display",tp,rec,"elapsed_seconds","records","DISPLAY_ONLY_INTERPOLATION")
    records+=series_records("a","independent linear display",ti,rec,"elapsed_seconds","records","DISPLAY_ONLY_INTERPOLATION")
    return finish("FIG26",fig,ax,title,
        ["Linear display interpolation between frozen start/end points for the primary and independent scans.","Normalized completion.",
         "Endpoint-derived average rates, not moving-rate measurements.","Both complete scans record zero kernel hits."],
        [CAND_DIR/"CAND-R4-0005.certificate.json",GLOBAL_SUM],"FROZEN_NUMERICAL_ENDPOINTS + DISPLAY_ONLY_INTERPOLATION","exact endpoints; interpolated display lines",
        "EXTENDED_DATA_TIER_B","elapsed time; progress fraction","records; throughput; hits","primary 171.573 s; independent 212.492 s",
        "two independent implementations scan the identical 785,639,753-record closed domain with zero kernel hits.",records,
        ["linear interpolation for display only","endpoint rate"])


@register("FIG27")
def fig27():
    title="Global certification throughput and efficiency"
    fig,ax=make_figure(title); data=candidates()[1:]
    labels=[r["id"] for r in data]; rec=np.array([r["records"] for r in data],float); elapsed=np.array([r["elapsed"] for r in data]); rate=rec/elapsed/1e6
    primary_ind=np.array([785639753/171.573/1e6,785639753/212.492/1e6])
    ax[0].bar(np.arange(4),rate,color=WARM[2:6])
    ax[1].bar([0,1],primary_ind,color=[WARM[2],WARM[5]])
    ax[2].plot(rec/1e6,rate,marker="o",color=WARM[3],lw=1.2)
    ax[3].plot(elapsed,rec/1e6,marker="D",color=WARM[4],lw=1.2)
    panel(ax[0],"a","Candidate-level average rates","candidate","million records/s")
    panel(ax[1],"b","Complete-scan implementation comparison","implementation","million records/s")
    panel(ax[2],"c","Rate versus scan depth","records examined (millions)","million records/s")
    panel(ax[3],"d","Certification work-time relation","elapsed seconds","records examined (millions)")
    ax[0].set_xticks(range(4),labels);ax[1].set_xticks([0,1],["primary","independent"])
    records=series_records("a","candidate rates",np.arange(2,6),rate,"candidate_index","million_records_per_second")
    records+=series_records("b","complete scans",[0,1],primary_ind,"implementation_index","million_records_per_second")
    return finish("FIG27",fig,ax,title,
        ["Average throughput for candidates 0002–0005.","Primary versus independent complete-scan rate.","Rate against examined depth.","Records against elapsed time."],
        [CAND_DIR/f"CAND-R4-{i:04d}.certificate.json" for i in range(2,6)],"FROZEN_NUMERICAL_SEARCH_HISTORY","derived averages from exact counts/times",
        "SUPPLEMENT_TIER_C","candidate; records; time","average throughput","no checkpoint-level moving rate asserted",
        "the primary and independent complete scans achieve 4.58 and 3.70 million records/s, respectively.",records,
        ["records/elapsed time","cross-plot"])


@register("FIG28")
def fig28():
    title="Independent certification agreement and quarantined false-positive geometry"
    fig,ax=make_figure(title); false=read_json(FALSE_POS)
    counts=np.array([785639753,785639753],float); hits=np.array([0,0])
    cutoff=2405+1700*math.sqrt(2); traces=np.array([2087+1476*math.sqrt(2),865+612*math.sqrt(2),11303+7992*math.sqrt(2)])
    deltas=traces-cutoff; sq=np.array([-2851304-2016176*math.sqrt(2),-10066712-7118240*math.sqrt(2),243937912+172490152*math.sqrt(2)])
    ax[0].bar([0,1],counts/1e6,color=[WARM[2],WARM[5]])
    ax[1].bar([0,1],hits,color=[WARM[2],WARM[5]]);ax[1].set_ylim(0,1)
    ax[2].scatter([0,1,2],traces,color=[WARM[3],WARM[4],WARM[6]],s=30);ax[2].axhline(cutoff,color=NEUTRAL,lw=.8,ls="--")
    ax[3].bar([0,1,2],np.sign(sq)*np.log10(np.abs(sq)),color=[WARM[3],WARM[4],WARM[6]]);ax[3].axhline(0,color=NEUTRAL,lw=.7,ls="-.")
    panel(ax[0],"a","Complete-domain record agreement","implementation","records (millions)")
    panel(ax[1],"b","Certified dangerous kernel hits","implementation","kernel hits")
    panel(ax[2],"c","Exact half-trace tests","case","absolute half trace")
    panel(ax[3],"d","Signed log squared-cutoff delta","case",r"$\mathrm{sgn}(\Delta_2)\log_{10}|\Delta_2|$")
    ax[0].set_xticks([0,1],["primary","independent"]);ax[1].set_xticks([0,1],["primary","independent"])
    ax[2].set_xticks([0,1,2],["fail 0002/3","fail 0004","quarantined v1"],rotation=20)
    ax[3].set_xticks([0,1,2],["fail 0002/3","fail 0004","quarantined v1"],rotation=20)
    records=series_records("a","complete scans",[0,1],counts,"implementation_index","records")
    records+=series_records("c","trace cases",[0,1,2],traces,"case_index","absolute_half_trace")
    records+=series_records("d","squared delta",[0,1,2],sq,"case_index","squared_cutoff_delta")
    return finish("FIG28",fig,ax,title,
        ["Identical primary and independent record counts.","Zero dangerous kernel hits in both.","Exact algebraic trace values relative to the dangerous threshold.",
         "Signed logarithmic squared deltas; the v1 hit lies strictly outside the dangerous domain."],
        [GLOBAL_SUM,FALSE_POS,CAND_DIR/"CAND-R4-0002.certificate.json",CAND_DIR/"CAND-R4-0004.certificate.json"],"FROZEN_EXACT_CERTIFICATION_VALUES","exact quadratic-field evaluations",
        "MAIN_TEXT_TIER_A","implementation; witness case","counts; traces; exact cutoff deltas","cutoff=2405+1700 sqrt(2)",
        "the apparent v1 hit is numerically and exactly on the safe side of the trace cutoff, while both corrected scans agree completely.",records,
        ["quadratic-field expression evaluation","signed log transform"])


@register("FIG29")
def fig29():
    title="Distribution of R4 failure positions and word depths"
    fig,ax=make_figure(title); data=candidates()[1:4]; false=read_json(FALSE_POS)
    positions=np.array([r["hit_index"] for r in data],float); depths=np.array([r["depth"] for r in data],float)
    all_pos=np.r_[positions,float(false["record_index_zero_based"])]
    ax[0].stem(np.arange(3),positions/1e6,linefmt="-",markerfmt="o",basefmt=" ")
    for line in ax[0].lines: line.set_color(WARM[2])
    ax[1].bar(np.arange(3),depths,color=WARM[3:6])
    ax[2].hist(all_pos/1e6,bins=np.linspace(0,3,7),color=WARM[4],edgecolor=WARM[0],lw=.5)
    sorted_pos=np.sort(all_pos);ax[3].step(sorted_pos/1e6,np.arange(1,5)/4,where="post",color=WARM[5],lw=1.2)
    panel(ax[0],"a","First dangerous-hit positions","failed candidate","record index (millions)")
    panel(ax[1],"b","Exact witness word depth","failed candidate","word depth")
    panel(ax[2],"c","Position histogram including quarantined v1","record index (millions)","count")
    panel(ax[3],"d","Empirical cumulative position distribution","record index (millions)","cumulative fraction")
    labels=["0002","0003","0004"];ax[0].set_xticks(range(3),labels);ax[1].set_xticks(range(3),labels)
    records=series_records("a","authoritative failures",[2,3,4],positions,"candidate_index","record_index")
    records+=series_records("b","word depth",[2,3,4],depths,"candidate_index","record_depth")
    records+=series_records("c","all positions",np.arange(4),all_pos,"case_index","record_index")
    return finish("FIG29",fig,ax,title,
        ["First authoritative global failures.","Their canonical word depths.","Histogram with the quarantined scanner-v1 position included only as a control.","Empirical cumulative distribution."],
        [CAND_DIR/f"CAND-R4-{i:04d}.certificate.json" for i in range(2,5)]+[FALSE_POS],"FROZEN_NUMERICAL_SEARCH_HISTORY","exact indices and depths",
        "SUPPLEMENT_TIER_C","candidate; record index","failure position; word depth","three authoritative failures plus one quarantined control",
        "all authoritative failed candidates are rejected within the first 2.83 million records of the 785.64 million-record domain.",records,
        ["histogram","empirical CDF"])


@register("FIG30")
def fig30():
    title="Permutation and Hilbert-space numerical scales"
    fig,ax=make_figure(title); names=["legacy degree","faithful $\mu$","transitive $\mu_{tr}$","group order","Hilbert dim."]; vals=np.array([24,92,5120,46080,92160],float)
    ax[0].bar(np.arange(5),vals,color=WARM[2:7]);ax[0].set_yscale("log")
    ax[1].plot(np.arange(5),np.log10(vals),marker="o",color=WARM[3],lw=1.2)
    ax[2].bar(np.arange(4),vals[1:]/vals[:-1],color=WARM[3:7]);ax[2].set_yscale("log")
    ax[3].plot(np.arange(5),np.cumsum(vals)/vals.sum(),marker="D",color=WARM[5],lw=1.2)
    panel(ax[0],"a","Certified scale hierarchy","quantity","value (log scale)")
    panel(ax[1],"b","Decimal complexity","quantity",r"$\log_{10}$ value")
    panel(ax[2],"c","Successive scale ratios","transition","ratio")
    panel(ax[3],"d","Cumulative share of listed scales","quantity rank","cumulative fraction")
    ax[0].set_xticks(range(5),names,rotation=30,ha="right");ax[1].set_xticks(range(5),names,rotation=30,ha="right")
    ax[2].set_xticks(range(4),["24→92","92→5120","5120→46080","46080→92160"],rotation=25,ha="right")
    records=series_records("a","scales",np.arange(5),vals,"quantity_index","value")
    return finish("FIG30",fig,ax,title,
        ["Logarithmic comparison of the five requested exact scales.","Their decimal logarithms.","Successive multiplicative jumps.","Cumulative numerical weight."],
        [FAITHFUL,TRANSITIVE],"FROZEN_EXACT_CERTIFICATION_VALUES","exact integers",
        "MAIN_TEXT_TIER_A","quantity","degree/order/dimension","24,92,5120,46080,92160",
        "the physical single-particle dimension is 3,840 times the legacy degree-24 search scale and twice the group order.",records,
        ["log scale","successive ratios","cumulative fraction"])


@register("FIG31")
def fig31():
    title="Complete SL(2,9) subgroup-class numerical audit"
    fig,ax=make_figure(title); rows=read_csv(SUBGROUP)
    orders=np.array([int(r["order"]) for r in rows]); indices=np.array([int(r["index_in_SL2_9"]) for r in rows]); center=np.array([r["contains_center"]=="TRUE" for r in rows]); corefree=np.array([r["eligible_as_core_free_projection"]=="TRUE" for r in rows])
    ax[0].hist(orders,bins=np.geomspace(1,721,14),color=WARM[2],edgecolor=WARM[0],lw=.4);ax[0].set_xscale("log")
    ax[1].hist(indices,bins=np.geomspace(1,721,14),color=WARM[3],edgecolor=WARM[0],lw=.4);ax[1].set_xscale("log")
    ax[2].scatter(orders[~center],indices[~center],facecolor="none",edgecolor=WARM[2],s=26,label="center-avoiding")
    ax[2].scatter(orders[center],indices[center],color=WARM[5],s=20,label="contains center");ax[2].set_xscale("log");ax[2].set_yscale("log")
    ax[3].bar([0,1,2],[len(rows),center.sum(),corefree.sum()],color=[WARM[2],WARM[4],WARM[6]])
    panel(ax[0],"a","Subgroup-order distribution","subgroup order","class count")
    panel(ax[1],"b","Subgroup-index distribution","index in $SL(2,9)$","class count")
    panel(ax[2],"c","Order–index classification","subgroup order","index")
    panel(ax[3],"d","Class counts by exact predicate","predicate","number of conjugacy classes")
    ax[2].legend();ax[3].set_xticks([0,1,2],["all","contains center","core-free eligible"],rotation=25,ha="right")
    records=series_records("c","all classes",orders,indices,"subgroup_order","index_in_SL2_9")
    records+=series_records("d","predicate counts",[0,1,2],[len(rows),center.sum(),corefree.sum()],"predicate_index","class_count")
    return finish("FIG31",fig,ax,title,
        ["Distribution of all 27 certified subgroup orders.","Distribution of subgroup indices.","Exact order–index points classified by center intersection.","Counts for all, center-containing, and core-free-eligible classes."],
        [SUBGROUP,TRANSITIVE],"FROZEN_EXACT_GROUP_AUDIT","exact subgroup enumeration",
        "EXTENDED_DATA_TIER_B","subgroup order/index","class counts and predicates","27 conjugacy classes",
        "only the center-avoiding classes can project to core-free stabilizers, and their maximum order is nine.",records,
        ["histogram","predicate classification","log scaling"])


@register("FIG32")
def fig32():
    title="Faithful permutation orbit-size distribution"
    fig,ax=make_figure(title); cert=read_json(FAITHFUL); sizes=np.array(cert["faithful_upper_witness"]["orbit_sizes"],float); x=np.arange(1,6)
    ax[0].bar(x,sizes,color=WARM[2:7]);ax[0].axhline(92,color=NEUTRAL,ls=":",lw=.7)
    ax[1].step(x,np.cumsum(sizes),where="mid",color=WARM[3],lw=1.2);ax[1].scatter(x,np.cumsum(sizes),color=WARM[3],s=22)
    ax[2].bar(x,sizes/92,color=WARM[3:8])
    ax[3].semilogy(x,sizes,marker="D",color=WARM[5],lw=1.2)
    panel(ax[0],"a","Orbit sizes in the exact faithful action","orbit index","orbit size")
    panel(ax[1],"b","Cumulative faithful degree","orbit index","cumulative degree")
    panel(ax[2],"c","Fractional contribution to $\mu=92$","orbit index","fraction")
    panel(ax[3],"d","Orbit-size dynamic range","orbit index","orbit size (log)")
    records=series_records("a","orbit sizes",x,sizes,"orbit_index","orbit_size")
    records+=series_records("b","cumulative",x,np.cumsum(sizes),"orbit_index","cumulative_degree")
    return finish("FIG32",fig,ax,title,
        ["Exact orbit sizes $(80,2,2,4,4)$.","Cumulative total reaching 92.","Fraction of the faithful degree carried by each orbit.","Log-scale comparison."],
        [FAITHFUL],"FROZEN_EXACT_CERTIFICATION_VALUES","exact integer orbit sizes",
        "MAIN_TEXT_TIER_A","orbit index","orbit size and cumulative degree","minimum faithful degree mu=92",
        "the 80-point $SL(2,9)$ orbit dominates, while four small central-factor orbits supply the remaining faithful information.",records,
        ["cumulative sum","normalization","log scale"])


def comm_samples(bounds=(2,3,5,8)):
    tmax=math.tan(math.pi/16); out={}
    root2=math.sqrt(2)
    for B in bounds:
        vals=set()
        for c in range(1,B+1):
            for a in range(-B,B+1):
                for b in range(-B,B+1):
                    t=(a+b*root2)/c
                    if -1e-15<=t<=tmax+1e-15:
                        vals.add(round(2*math.atan(max(0,t)),14))
        out[B]=np.array(sorted(vals))
    return out


@register("FIG33")
def fig33():
    title="Bounded-height samples of the centered commensurator"
    fig,ax=make_figure(title); samples=comm_samples(); records=[]
    for i,(B,vals) in enumerate(samples.items()):
        ax[0].vlines(vals,0,1+i*.08,color=WARM[i+2],lw=.55,label=f"height {B}")
        spac=np.diff(vals); ax[1].hist(spac,bins=24,histtype="step",color=WARM[i+2],lw=1.0,label=f"H={B}")
        ax[2].plot(vals,np.arange(1,len(vals)+1),color=WARM[i+2],lw=1.0)
        ax[3].scatter(np.full(len(vals),B),vals,s=5,color=WARM[i+2],alpha=.75)
        records+=series_records("a",f"height {B}",vals,np.full(len(vals),B),"theta_rad","height_cutoff",f"B={B}")
    panel(ax[0],"a","Angle sample on the reduced interval",r"$\theta$ (rad)","rug level")
    panel(ax[1],"b","Nearest-neighbor spacing","angle spacing (rad)","count")
    panel(ax[2],"c","Cumulative sampled-angle count",r"$\theta$ (rad)","cumulative count")
    panel(ax[3],"d","Height-resolved angle cloud","height cutoff",r"$\theta$ (rad)")
    ax[0].legend(ncol=2);ax[1].legend(ncol=2)
    return finish("FIG33",fig,ax,title,
        ["Rug plots for exact half-angle parameters $t=(a+b\sqrt{2})/c$ at four bounded heights.","Spacing histograms.","Cumulative counts.","Angle cloud versus cutoff."],
        [COMM_TEX],"ANALYTIC_VISUALIZATION_SAMPLE","exact parameterization; finite bounded-height sample",
        "MAIN_TEXT_TIER_A","theta; height cutoff","sample density and spacings","|a|,|b|,c<=B; B={2,3,5,8}",
        "bounded-height exact angles rapidly fill the reduced twist interval, numerically illustrating the proved density theorem.",records,
        ["exact Q(sqrt2) enumeration for visualization only","deduplication","spacing"])


@register("FIG34")
def fig34():
    title="Multi-scale zoom of centered commensurator angles"
    fig,ax=make_figure(title); vals=comm_samples((8,))[8]; windows=[math.pi/8,0.1,0.02,0.005];records=[]
    for i,w in enumerate(windows):
        sub=vals[vals<=w]; ax[i].vlines(sub,0,1,color=WARM[i+2],lw=.6)
        ax[i].scatter(sub,np.ones_like(sub),s=5,color=WARM[i+2])
        panel(ax[i],chr(97+i),fr"Window $0\leq\theta\leq{w:.4g}$",r"$\theta$ (rad)","sample occupancy")
        ax[i].set_ylim(0,1.2)
        records+=series_records(chr(97+i),f"window {w}",sub,np.ones_like(sub),"theta_rad","occupancy",f"theta_max={w}")
    return finish("FIG34",fig,ax,title,
        ["Full reduced interval.","Zoom below 0.1 rad.","Zoom below 0.02 rad.","Zoom below 0.005 rad."],
        [COMM_TEX],"ANALYTIC_VISUALIZATION_SAMPLE","exact bounded-height angles",
        "EXTENDED_DATA_TIER_B","theta","occupancy","height cutoff B=8",
        "new exact angles persist under successive zooms toward the aligned limit, consistent with the dense-intersection theorem.",records,
        ["window filtering","exact parameterization sample"])


@register("FIG35")
def fig35():
    title="Certified commensurator-but-not-normalizer example"
    fig,ax=make_figure(title); cert=read_json(COMM_CERT); theta=float(cert["construction"]["theta_c_radians"]);m=float(cert["r5_comm_run"]["common_cover_index"]);dim=float(cert["r5_comm_run"]["hilbert_dimension"])
    cases=np.arange(2); angles=np.array([0,theta]);indices=np.array([1,m]);dims=np.array([92160,dim]);blow=dims/dims[0]
    ax[0].bar(cases,angles,color=[WARM[2],WARM[5]])
    ax[1].bar(cases,indices,color=[WARM[2],WARM[5]]);ax[1].set_yscale("log")
    ax[2].bar(cases,dims,color=[WARM[2],WARM[5]]);ax[2].set_yscale("log")
    ax[3].bar(cases,blow,color=[WARM[2],WARM[5]]);ax[3].set_yscale("log")
    panel(ax[0],"a","Centered twist angle","case",r"$\theta$ (rad)")
    panel(ax[1],"b","Common-cover index","case",r"$m_\theta$")
    panel(ax[2],"c","Bilayer Hilbert dimension","case",r"$D_{\rm Hilbert}$")
    panel(ax[3],"d","Dimension blow-up relative to same cover","case","blow-up factor")
    for a in ax:a.set_xticks(cases,["same cover",r"certified $\theta_c$"])
    records=series_records("a","cases",cases,angles,"case_index","theta_rad")
    records+=series_records("b","cases",cases,indices,"case_index","common_cover_index")
    records+=series_records("c","cases",cases,dims,"case_index","hilbert_dimension")
    return finish("FIG35",fig,ax,title,
        ["Identity and certified non-normalizer angles.","Index increase from 1 to 234.","Hilbert dimension increase from 92,160 to 21,565,440.","Exact 234-fold blow-up."],
        [COMM_CERT,FAITHFUL],"FROZEN_EXACT_CERTIFICATION_VALUES","exact certificate values",
        "MAIN_TEXT_TIER_A","case","theta; index; Hilbert dimension","theta_c=0.3652814832; m=234",
        "the first explicit commensurator-only construction is exact but requires a 234-fold larger common-cover Hilbert space.",records,
        ["ratio","log scaling"])


@register("FIG36")
def fig36():
    title="Common-cover branch complexity and physical word lengths"
    fig,ax=make_figure(title); rows=read_csv(COMM_REG); lengths=np.array([int(r["physical_word_length"]) for r in rows]);idx=np.array([int(r["branch_index"]) for r in rows]);cert=read_json(COMM_CERT)
    ax[0].plot(idx,lengths,color=WARM[2],lw=.75);ax[0].scatter(idx,lengths,s=5,color=WARM[2])
    ax[1].hist(lengths,bins=24,color=WARM[3],edgecolor=WARM[0],lw=.4)
    sort=np.sort(lengths);ax[2].step(sort,np.arange(1,len(sort)+1)/len(sort),where="post",color=WARM[4],lw=1.2)
    ax[3].bar([0,1,2],[234,21565440,491905321],color=[WARM[2],WARM[4],WARM[6]]);ax[3].set_yscale("log")
    panel(ax[0],"a","Branch-resolved physical word length","branch index","physical word length")
    panel(ax[1],"b","Word-length distribution","physical word length","branch count")
    panel(ax[2],"c","Empirical cumulative distribution","physical word length","cumulative fraction")
    panel(ax[3],"d","Exact complexity scales","quantity","value")
    ax[3].set_xticks([0,1,2],["branches/index","Hilbert dim.","M7 ball elements"],rotation=25,ha="right")
    records=series_records("a","branches",idx,lengths,"branch_index","physical_word_length")
    records+=series_records("c","ECDF",sort,np.arange(1,len(sort)+1)/len(sort),"physical_word_length","cumulative_fraction")
    return finish("FIG36",fig,ax,title,
        ["All 234 exact correspondence branches.","Histogram of physical word lengths.","Their empirical cumulative distribution.","Common-cover index, Hilbert dimension, and M7 exact-ball scale."],
        [COMM_REG,COMM_CERT,ROOT/"production_code/hodge/CM_047_NP_M7_STREAM_RESULT.json"],"FROZEN_EXACT_CERTIFICATION_VALUES","exact integer branch data",
        "EXTENDED_DATA_TIER_B","branch index; word length","word lengths and complexity scales","234 branches; D=21,565,440",
        "the exact construction closes arithmetically but carries a broad physical-word burden and a large finite-state cost.",records,
        ["histogram","empirical CDF","log scale"])




