from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from suite_core import (
    ROOT, WARM, NEUTRAL, DIVERGING, as_float, export_figure, geometric_derivative,
    make_figure, panel, read_csv, read_json, save_long_data, series_records,
)


REGISTRY = {}


def register(fig_id):
    def deco(fn):
        REGISTRY[fig_id] = fn
        return fn
    return deco


GEOM_CSV = ROOT / "reproducibility/data/hyperbolic_geometry_reconstruction/local_moire_geometry.csv"
GEOM_SRC = ROOT / "reproducibility/src/hyperbolic/local_twist.py"
GEOM_TEX = ROOT / "source_current_195/02_ATOMIC_TASKS/TASK-01_CLEAN.tex"
MAGIC_NO = ROOT / "data/validation/RUN-002/five_state_no_root.json"
MAGIC_YES = ROOT / "data/validation/RUN-002/first_shell_positive_root.json"
OBS_CSV = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/target_observables.csv"
HODGE_CSV = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/hodge_eigenvalues.csv"
DERIV_CSV = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/derivative_audit.csv"
PROJ_CSV = ROOT / "reproducibility/data/hyperbolic_spectral_reconstruction/projector_tracking.csv"
M7_CERT = ROOT / "production_code/hodge/CM_047_NP_M7_STREAM_RESULT.json"
M6_CERT = ROOT / "production_code/hodge/CM_047_NP_TENSOR_REASSESSMENT.json"
COMMUTANT_CERT = ROOT / "production_code/hodge/GEOMETRIC_SHELL_HODGE_COMMUTANT_CERTIFICATE.json"
INF_CERT = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/04_INFINITE_OPERATOR/INFINITE_OPERATOR_CERTIFICATE.tex"


def geom_arrays():
    theta = np.geomspace(1e-4, math.pi / 8, 500)
    r_over_a = np.array([0.25, 1.0 / 3.057141839, 0.50, 1.0, 5.0])
    arrays = []
    for r in r_over_a:
        b = np.sinh(1.0 / (2.0 * r))
        s = np.sin(theta / 2.0)
        chi = b / s
        xi = r * np.arcsinh(chi)
        area_r2 = 2.0 * np.pi * (np.sqrt(1.0 + chi * chi) - 1.0)
        area_a2 = area_r2 * r * r
        xi_e = 1.0 / (2.0 * s)
        q = 2.0 * np.pi / xi
        arrays.append((r, b, s, chi, xi, area_a2, xi_e, q))
    return theta, arrays


def finish(fig_id, fig, axes, title, panels, sources, source_type, exactness, tier,
           xvars, yvars, params, observation, records, transformations):
    data_path, _ = save_long_data(fig_id, records, sources, source_type, transformations)
    return export_figure(fig_id, fig, axes, title, panels, sources, source_type,
                         exactness, tier, xvars, yvars, params, observation,
                         data_path, transformations)


@register("FIG01")
def fig01():
    title = "Curvature-controlled hyperbolic moiré length"
    fig, ax = make_figure(title)
    theta, arrays = geom_arrays()
    records = []
    for i, (r, b, s, chi, xi, area, xi_e, q) in enumerate(arrays):
        label = rf"$R/a={r:.3g}$"
        ax[0].plot(theta, xi, color=WARM[i], lw=1.15, label=label)
        ax[1].loglog(theta, xi, color=WARM[i], lw=1.15)
        ax[2].semilogx(theta, xi / xi_e, color=WARM[i], lw=1.15)
        asym = r * np.log(4.0 * np.sinh(1.0 / (2.0 * r)) / theta)
        ax[3].semilogx(theta, (xi - asym) / np.maximum(xi, 1e-15), color=WARM[i], lw=1.15)
        records += series_records("a", label, theta, xi, "theta_rad", "xi_M_over_a", f"R_over_a={r}")
        records += series_records("c", label, theta, xi / xi_e, "theta_rad", "xi_H_over_xi_E", f"R_over_a={r}")
    frozen = read_csv(GEOM_CSV)
    fx = np.array([as_float(r["theta_radians"]) for r in frozen if r["status"] == "PASS"])
    fy = np.array([as_float(r["moire_radius_over_r"]) / 3.057141839 for r in frozen if r["status"] == "PASS"])
    ax[0].scatter(fx, fy, facecolor="none", edgecolor=WARM[0], s=23, lw=0.8, label="frozen dyadic points")
    panel(ax[0], "a", "Exact length across curvature radii", r"twist $\theta$ (rad)", r"$\xi_M/a$")
    panel(ax[1], "b", "Log–log crossover", r"$\theta$ (rad)", r"$\xi_M/a$")
    panel(ax[2], "c", "Suppression relative to Euclidean beat length", r"$\theta$ (rad)", r"$\xi_H/\xi_E$")
    panel(ax[3], "d", "Small-angle asymptotic residual", r"$\theta$ (rad)", r"$(\xi_H-\xi_{\rm as})/\xi_H$")
    ax[0].legend(ncol=2)
    ax[2].axhline(1, color=NEUTRAL, ls="-.", lw=0.7)
    return finish("FIG01", fig, ax, title,
        [r"Exact $\xi_M/a$ versus twist for five curvature radii; open circles are frozen dyadic checks.",
         "The same curves on log–log axes expose the logarithmic hyperbolic crossover.",
         r"Ratio to the Euclidean beat length $[2\sin(\theta/2)]^{-1}$.",
         "Relative residual from the proved small-angle logarithmic asymptotic."],
        [GEOM_CSV, GEOM_SRC, GEOM_TEX], "ANALYTIC_VISUALIZATION_EVALUATION + FROZEN_NUMERICAL_CHECKS",
        "exact formula; floating evaluation", "MAIN_TEXT_TIER_A", "theta", "xi_M",
        "a=1; R/a in {0.25,0.3271,0.5,1,5}",
        "negative curvature replaces the Euclidean power divergence by a logarithmic length growth.", records,
        ["closed-form evaluation", "ratio", "small-angle residual"])


@register("FIG02")
def fig02():
    title = "Effective hyperbolic moiré area and local exponent"
    fig, ax = make_figure(title)
    theta, arrays = geom_arrays()
    records = []
    for i, (r, b, s, chi, xi, area, xi_e, q) in enumerate(arrays):
        beta = -geometric_derivative(theta, area)
        eu_area = math.pi * xi_e**2
        collapse_x = s / b
        collapse_y = area / (2 * math.pi * r * r)
        ax[0].loglog(theta, area, color=WARM[i], lw=1.15, label=rf"$R/a={r:.3g}$")
        ax[1].semilogx(theta, beta, color=WARM[i], lw=1.15)
        ax[2].loglog(collapse_x, collapse_y, color=WARM[i], lw=1.15)
        ax[3].semilogx(theta, area / eu_area, color=WARM[i], lw=1.15)
        records += series_records("a", f"R/a={r}", theta, area, "theta_rad", "A_M_over_a2", f"R_over_a={r}")
        records += series_records("b", f"R/a={r}", theta, beta, "theta_rad", "minus_dlogA_dlogtheta", f"R_over_a={r}")
    panel(ax[0], "a", "Exact effective area", r"$\theta$ (rad)", r"$A_M/a^2$")
    panel(ax[1], "b", "Running area exponent", r"$\theta$ (rad)", r"$-d\ln A_M/d\ln\theta$")
    panel(ax[2], "c", "Parameter-free area collapse", r"$\sin(\theta/2)/\sinh(a/2R)$", r"$A_M/(2\pi R^2)$")
    panel(ax[3], "d", "Hyperbolic/Euclidean area ratio", r"$\theta$ (rad)", r"$A_H/(\pi\xi_E^2)$")
    ax[0].legend(ncol=2)
    ax[1].axhline(1, color=NEUTRAL, ls="--", lw=0.7)
    ax[1].axhline(2, color=NEUTRAL, ls=":", lw=0.7)
    return finish("FIG02", fig, ax, title,
        ["Effective area in units of $a^2$.", "Logarithmic derivative of the exact area curve.",
         "Curvature-normalized collapse on the proved variable $s/b_*$.", "Ratio to the Euclidean disk-area benchmark."],
        [GEOM_CSV, GEOM_SRC, GEOM_TEX], "ANALYTIC_VISUALIZATION_EVALUATION",
        "exact formula; numerical derivative of dense exact curve", "MAIN_TEXT_TIER_A", "theta; collapse variable",
        "A_M; local exponent; normalized area", "same as FIG01",
        "the area exponent crosses away from the Euclidean value 2 and approaches the curvature-dominated value 1.", records,
        ["closed-form evaluation", "logarithmic derivative", "normalization", "ratio"])


@register("FIG03")
def fig03():
    title = "Running geometric exponents across the curvature crossover"
    fig, ax = make_figure(title)
    theta, arrays = geom_arrays()
    records = []
    for i, (r, b, s, chi, xi, area, xi_e, q) in enumerate(arrays):
        x = s / b
        beta_xi = -geometric_derivative(s, xi)
        beta_area = -geometric_derivative(s, area)
        ax[0].semilogx(x, beta_xi, color=WARM[i], lw=1.15, label=rf"$R/a={r:.3g}$")
        ax[1].semilogx(x, beta_area, color=WARM[i], lw=1.15)
        ax[2].semilogx(x, beta_area - 2 * beta_xi, color=WARM[i], lw=1.15)
        ax[3].loglog(x, np.abs(beta_xi - 1.0) + 1e-14, color=WARM[i], lw=1.15)
        records += series_records("a", f"R/a={r}", x, beta_xi, "crossover_x", "beta_xi", f"R_over_a={r}")
        records += series_records("b", f"R/a={r}", x, beta_area, "crossover_x", "beta_area", f"R_over_a={r}")
    panel(ax[0], "a", "Length exponent", r"$x=\sin(\theta/2)/\sinh(a/2R)$", r"$\beta_\xi=-d\ln\xi/d\ln s$")
    panel(ax[1], "b", "Area exponent", r"$x$", r"$\beta_A=-d\ln A/d\ln s$")
    panel(ax[2], "c", "Area–length exponent mismatch", r"$x$", r"$\beta_A-2\beta_\xi$")
    panel(ax[3], "d", "Distance from Euclidean length exponent", r"$x$", r"$|\beta_\xi-1|$")
    ax[0].legend(ncol=2)
    for a in ax[:2]:
        a.axhline(1, color=NEUTRAL, lw=0.7, ls="--")
    ax[1].axhline(2, color=NEUTRAL, lw=0.7, ls=":")
    ax[2].axhline(0, color=NEUTRAL, lw=0.7, ls="-.")
    return finish("FIG03", fig, ax, title,
        ["Exact running exponent of moiré length.", "Exact running exponent of effective area.",
         r"Departure from the Euclidean disk identity $A\propto\xi^2$.", "Log residual from the Euclidean length exponent."],
        [GEOM_SRC, GEOM_TEX], "ANALYTIC_VISUALIZATION_EVALUATION", "exact curve; display derivative",
        "MAIN_TEXT_TIER_A", "crossover variable", "running exponents", "five R/a values",
        "all curvature families collapse on one crossover variable, while hyperbolic area and length acquire distinct running exponents.", records,
        ["closed-form evaluation", "dense-grid logarithmic derivative"])


@register("FIG04")
def fig04():
    title = "Parameter-free collapse of length, area, and reciprocal scale"
    fig, ax = make_figure(title)
    theta, arrays = geom_arrays()
    records = []
    exact_x = np.geomspace(1e-4, 5, 600)
    exact_length = np.arcsinh(1 / exact_x)
    exact_area = np.sqrt(1 + 1 / exact_x**2) - 1
    for i, (r, b, s, chi, xi, area, xi_e, q) in enumerate(arrays):
        x = s / b
        y1 = xi / r
        y2 = area / (2 * math.pi * r * r)
        y3 = q * r / (2 * math.pi)
        ax[0].loglog(x, y1, color=WARM[i], lw=1.0)
        ax[1].loglog(x, y2, color=WARM[i], lw=1.0)
        ax[2].loglog(x, y3, color=WARM[i], lw=1.0)
        residual = y1 - np.arcsinh(1 / x)
        ax[3].semilogx(x, residual, color=WARM[i], lw=1.0)
        records += series_records("a", f"R/a={r}", x, y1, "x", "xi_over_R", f"R_over_a={r}")
    ax[0].loglog(exact_x, exact_length, color=WARM[0], lw=0.8, ls="--", label="exact master curve")
    ax[1].loglog(exact_x, exact_area, color=WARM[0], lw=0.8, ls="--")
    ax[2].loglog(exact_x, 1 / exact_length, color=WARM[0], lw=0.8, ls="--")
    panel(ax[0], "a", "Length collapse", r"$x=s/b_*$", r"$\xi_M/R$")
    panel(ax[1], "b", "Area collapse", r"$x=s/b_*$", r"$A_M/(2\pi R^2)$")
    panel(ax[2], "c", "Reciprocal-scale collapse", r"$x=s/b_*$", r"$q_MR/(2\pi)$")
    panel(ax[3], "d", "Collapse residual", r"$x=s/b_*$", r"$\xi/R-\operatorname{arsinh}(1/x)$")
    ax[0].legend()
    return finish("FIG04", fig, ax, title,
        ["Five curvature radii collapse onto $\operatorname{arsinh}(1/x)$.",
         "Area data collapse onto $\sqrt{1+x^{-2}}-1$.", "Reciprocal lengths collapse onto the inverse master curve.",
         "Floating residual of all evaluated curves from the exact identity."],
        [GEOM_SRC, GEOM_TEX], "ANALYTIC_VISUALIZATION_EVALUATION", "exact master identities",
        "MAIN_TEXT_TIER_A", "s/b_*", "normalized length, area, reciprocal scale", "same as FIG01",
        "curvature and microscopic spacing enter only through the single scaling variable $s/b_*$.", records,
        ["dimensionless normalization", "master-curve residual"])


@register("FIG05")
def fig05():
    title = "Reciprocal moiré scale and inverse-logarithmic asymptotics"
    fig, ax = make_figure(title)
    theta, arrays = geom_arrays()
    records = []
    for i, (r, b, s, chi, xi, area, xi_e, q) in enumerate(arrays):
        q_e = 2 * math.pi / xi_e
        q_as = 2 * math.pi / (r * np.log(4 * b / theta))
        ax[0].plot(theta, q, color=WARM[i], lw=1.15, label=rf"$R/a={r:.3g}$")
        ax[1].semilogx(theta, q, color=WARM[i], lw=1.15)
        ax[2].semilogx(theta, q / q_as, color=WARM[i], lw=1.15)
        ax[3].semilogx(theta, q / q_e, color=WARM[i], lw=1.15)
        records += series_records("a", f"R/a={r}", theta, q, "theta_rad", "q_M_times_a", f"R_over_a={r}")
    panel(ax[0], "a", "Exact reciprocal scale", r"$\theta$ (rad)", r"$q_Ma$")
    panel(ax[1], "b", "Semilog small-angle view", r"$\theta$ (rad)", r"$q_Ma$")
    panel(ax[2], "c", "Inverse-log asymptotic ratio", r"$\theta$ (rad)", r"$q_M/q_{\mathrm{inv\!-\!log}}$")
    panel(ax[3], "d", "Ratio to Euclidean reciprocal beat scale", r"$\theta$ (rad)", r"$q_H/q_E$")
    ax[0].legend(ncol=2)
    ax[2].axhline(1, color=NEUTRAL, lw=0.7, ls="--")
    ax[3].axhline(1, color=NEUTRAL, lw=0.7, ls="-.")
    return finish("FIG05", fig, ax, title,
        [r"Intrinsic $q_M=2\pi/\xi_M$.", "Semilog view of the small-angle regime.",
         "Ratio to the proved inverse-log approximation.", "Curvature enhancement relative to the Euclidean reciprocal scale."],
        [GEOM_SRC, GEOM_TEX], "ANALYTIC_VISUALIZATION_EVALUATION", "exact formula; asymptotic comparison",
        "MAIN_TEXT_TIER_A", "theta", "q_M", "same as FIG01",
        "the hyperbolic reciprocal scale closes only inverse-logarithmically as twist vanishes.", records,
        ["closed-form evaluation", "asymptotic ratio"])


@register("FIG06")
def fig06():
    title = "Geometric–arithmetic locking scale and explicit common-cover point"
    fig, ax = make_figure(title)
    theta = np.geomspace(1e-4, math.pi / 8, 500)
    r = 1 / 3.057141839
    b = math.sinh(1 / (2 * r))
    s = np.sin(theta / 2)
    xi = r * np.arcsinh(b / s)
    d = 48.0
    q_match = (24 / d) * (np.sqrt(1 + (b / s) ** 2) - 1)
    r_sc = r * np.arccosh(1 + d * q_match / 24)
    delta = r_sc - xi
    theta_c, m_c = 0.3652814832319478, 234.0
    q_c = np.interp(theta_c, theta, q_match)
    ax[0].loglog(theta, q_match, color=WARM[2], lw=1.25, label="continuous locking index")
    ax[0].scatter([theta_c], [m_c], color=WARM[0], marker="D", s=28, label=r"certified $m_\theta=234$")
    ax[1].loglog(q_match, np.maximum(xi, 1e-12), color=WARM[3], lw=1.2)
    ax[2].semilogx(theta, delta, color=WARM[4], lw=1.2)
    ax[3].semilogx(theta, q_match * s, color=WARM[5], lw=1.2)
    ax[3].axhline(24 * b / d, color=NEUTRAL, lw=0.8, ls="--")
    panel(ax[0], "a", "Analytic matching index and certified point", r"$\theta$ (rad)", r"$q_{\rm match}$ or $m_\theta$")
    panel(ax[1], "b", "Index–radius scaling", r"$q_{\rm match}$", r"$\xi_M/a$")
    panel(ax[2], "c", "Area-equivalent radial locking residual", r"$\theta$ (rad)", r"$(r_M^{\rm sc}-\xi_M)/a$")
    panel(ax[3], "d", "Small-angle locking product", r"$\theta$ (rad)", r"$q_{\rm match}|\sin(\theta/2)|$")
    ax[0].legend()
    records = series_records("a", "analytic matching index", theta, q_match, "theta_rad", "q_match", "d=48")
    records += series_records("c", "locking defect", theta, delta, "theta_rad", "radial_defect_over_a", "d=48")
    records += series_records("a", "certified commensurator point", [theta_c], [m_c], "theta_rad", "common_cover_index", "exact certificate")
    comm = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT/05_CONSTRUCTIVE_COMMENSURATOR/R5_COMM_EXAMPLE_CERTIFICATE.json"
    return finish("FIG06", fig, ax, title,
        ["The proved continuous index required for exact area locking, with the independently certified commensurator point overlaid.",
         "Moiré radius against the matching index.", "Radial defect, numerically zero for the analytic locking construction.",
         "The product $q_{\rm match}s$ approaching its proved constant."],
        [GEOM_TEX, comm], "ANALYTIC_VISUALIZATION_EVALUATION + CERTIFIED_EXACT_POINT",
        "analytic matching law and exact certificate", "MAIN_TEXT_TIER_A", "theta; matching index", "index; radius; defect",
        "Bolza d=48; theta_c=0.3652814832; m_theta=234",
        "the area-locking index diverges as inverse twist, while the certified non-normalizer point incurs a finite 234-fold common-cover cost.", records,
        ["proved locking-law evaluation", "exact point overlay"])


def magic_arrays():
    no = read_json(MAGIC_NO)
    yes = read_json(MAGIC_YES)
    obs = read_csv(OBS_CSV)
    u = np.array([as_float(r["w_over_w_star"]) for r in obs])
    return no, yes, obs, u


@register("FIG11")
def fig11():
    title = "Exact square five-state no-magic curve"
    fig, ax = make_figure(title)
    no, yes, obs, u = magic_arrays()
    alpha = np.linspace(0, 3, 900)
    rr = np.sqrt(1 + 16 * alpha**2)
    c = (rr**2 - rr + 2) / (rr * (rr + 1))
    c_pert = 1 - 8 * alpha**2
    cmin = float(no["minimum"])
    residual = c - c_pert
    derivative = np.gradient(c, alpha)
    ax[0].plot(alpha, c, color=WARM[2], lw=1.3, label="exact coefficient")
    ax[0].plot(alpha, c_pert, color=WARM[7], lw=0.9, ls="-.", label="quadratic expansion")
    ax[0].axhline(cmin, color=WARM[0], lw=0.8, ls=":", label="exact lower bound")
    ax[1].plot(alpha, residual, color=WARM[3], lw=1.2)
    ax[2].plot(alpha, derivative, color=WARM[4], lw=1.2)
    ax[3].semilogy(alpha, np.maximum(c - cmin, 1e-15), color=WARM[5], lw=1.2)
    formal = float(no["formal_quadratic_alpha"])
    ax[0].axvline(formal, color=NEUTRAL, lw=0.7, ls="--")
    panel(ax[0], "a", "Exact versus perturbative coefficient", r"coupling $\alpha$", r"$c_{\mathrm{sq}}$")
    panel(ax[1], "b", "Perturbative residual", r"$\alpha$", r"$c_{\rm exact}-(1-8\alpha^2)$")
    panel(ax[2], "c", "Exact coupling derivative", r"$\alpha$", r"$dc_{\mathrm{sq}}/d\alpha$")
    panel(ax[3], "d", "Distance above the global lower bound", r"$\alpha$", r"$c_{\mathrm{sq}}-(4\sqrt{2}-5)$")
    ax[0].legend()
    records = series_records("a", "exact", alpha, c, "alpha", "c_square")
    records += series_records("a", "quadratic expansion", alpha, c_pert, "alpha", "c_square_perturbative")
    return finish("FIG11", fig, ax, title,
        ["Exact coefficient, its weak-coupling approximation, formal-series zero, and certified lower bound.",
         "Failure of the truncated series away from weak coupling.", "Derivative locating the finite global minimum.",
         "Strict positive margin above $4\sqrt{2}-5$."],
        [MAGIC_NO, ROOT / "reproducibility/figures/p0_05_r5/make_r5.py"], "ANALYTIC_VISUALIZATION_EVALUATION + FROZEN_CERTIFICATE",
        "exact five-state formula", "MAIN_TEXT_TIER_A", "alpha", "quadratic coefficient and derivatives",
        f"alpha_min^2={no['alpha_min_squared']}; formal alpha={formal}",
        "the formal perturbative zero is spurious; the exact coefficient remains bounded below by 0.656854.", records,
        ["closed-form evaluation", "perturbative residual", "numerical derivative"])


@register("FIG12")
def fig12():
    title = "Protected first-shell hyperbolic magic root"
    fig, ax = make_figure(title)
    no, yes, obs, u_data = magic_arrays()
    u = np.linspace(0.70, 1.30, 700)
    response = 1 - u
    bandwidth = 4 * np.abs(1 - u)
    derivative = np.gradient(response, u)
    local = response - (-(u - 1))
    ax[0].plot(u, response, color=WARM[2], lw=1.3)
    ax[1].plot(u, bandwidth, color=WARM[3], lw=1.2)
    ax[2].plot(u, derivative, color=WARM[4], lw=1.2)
    ax[3].semilogy(u, np.abs(local) + 1e-18, color=WARM[5], lw=1.2)
    for a in ax:
        a.axvline(1, color=NEUTRAL, lw=0.8, ls="--")
    ax[0].axhline(0, color=NEUTRAL, lw=0.7, ls="-.")
    panel(ax[0], "a", "Signed root function", r"$u=w/w_*$", r"$f(u)=1-u$")
    panel(ax[1], "b", "Target bandwidth", r"$u$", r"$W_+/t=4|1-u|$")
    panel(ax[2], "c", "Transversality derivative", r"$u$", r"$df/du$")
    panel(ax[3], "d", "Local-linearization residual", r"$u$", r"$|f(u)+u-1|$")
    records = series_records("a", "first-shell root function", u, response, "w_over_w_star", "root_function")
    records += series_records("b", "exact bandwidth", u, bandwidth, "w_over_w_star", "bandwidth_over_t")
    return finish("FIG12", fig, ax, title,
        ["Signed first-shell response with the unique zero at $w=w_*$.", "Exact cusp-like bandwidth suppression.",
         "Nonzero derivative certifying a simple crossing.", "Floating residual from the exact local linearization."],
        [MAGIC_YES, OBS_CSV], "ANALYTIC_VISUALIZATION_EVALUATION + FROZEN_ROOT_CERTIFICATE", "exact first-shell formula",
        "MAIN_TEXT_TIER_A", "w/w_*", "root function; bandwidth; derivative",
        f"q1={yes['q1']}; w*/t={yes['w_star_over_t']}",
        "the hyperbolic validation model has a simple root at $w_*/t=140.3686$ with a nonzero slope.", records,
        ["exact first-shell evaluation", "derivative", "linearization residual"])


@register("FIG13")
def fig13():
    title = "Magic–no-magic comparison on normalized coupling axes"
    fig, ax = make_figure(title)
    no, yes, obs, u_data = magic_arrays()
    x = np.linspace(0, 2, 800)
    rr = np.sqrt(1 + 16 * x**2)
    square = (rr**2 - rr + 2) / (rr * (rr + 1))
    hyper = 1 - x
    ax[0].plot(x, square, color=WARM[2], lw=1.3, label="square five-state")
    ax[0].plot(x, hyper, color=WARM[5], lw=1.1, ls="-.", label="hyperbolic first-shell")
    ax[1].plot(x, np.minimum(square, np.abs(hyper)), color=WARM[3], lw=1.2)
    ax[2].plot(x, square - hyper, color=WARM[4], lw=1.2)
    ax[3].semilogy(x, np.maximum(square, 1e-15), color=WARM[2], lw=1.1, label="square")
    ax[3].semilogy(x, np.maximum(np.abs(hyper), 1e-15), color=WARM[5], lw=1.1, ls="--", label="hyperbolic |f|")
    for a in ax:
        a.axvline(1, color=NEUTRAL, lw=0.7, ls=":")
    panel(ax[0], "a", "Response functions", "normalized coupling", "dimensionless response")
    panel(ax[1], "b", "Closest approach to cancellation", "normalized coupling", "minimum positive magnitude")
    panel(ax[2], "c", "Model-response separation", "normalized coupling", r"$c_{\mathrm{sq}}-f_H$")
    panel(ax[3], "d", "Log-magnitude contrast", "normalized coupling", "response magnitude")
    ax[0].legend(); ax[3].legend()
    records = series_records("a", "square", x, square, "normalized_coupling", "response")
    records += series_records("a", "hyperbolic", x, hyper, "normalized_coupling", "response")
    return finish("FIG13", fig, ax, title,
        ["Exact responses in their declared normalized coupling coordinates.", "Minimum response magnitude highlights the selective zero.",
         "Direct model separation.", "Log-magnitude view of the root versus the positive lower bound."],
        [MAGIC_NO, MAGIC_YES], "ANALYTIC_VISUALIZATION_EVALUATION", "two exact restricted models",
        "MAIN_TEXT_TIER_A", "normalized coupling", "model response", "validation-only normalized coordinates",
        "the hyperbolic first-shell response crosses zero whereas the square control stays strictly positive.", records,
        ["closed-form evaluation", "model comparison"])


@register("FIG14")
def fig14():
    title = "Magic-root sensitivity to anisotropic first-shell perturbations"
    fig, ax = make_figure(title)
    ratios = np.array([1.10, 0.90, 1.05, 0.95])
    u_roots = 1 / ratios
    shifts = u_roots - 1
    eps = np.linspace(0, 0.16, 240)
    patterns = np.array([1.0, -1.0, 0.5, -0.5])
    roots = np.vstack([1 / (1 + e * patterns) for e in eps])
    spread = roots.max(axis=1) - roots.min(axis=1)
    anis = np.sqrt(np.sum((roots - roots.mean(axis=1, keepdims=True))**2, axis=1))
    ax[0].bar(np.arange(4), ratios - 1, color=WARM[2:6])
    ax[1].bar(np.arange(4), shifts, color=WARM[3:7])
    for j in range(4):
        ax[2].plot(eps, roots[:, j], color=WARM[j + 2], lw=1.1, label=rf"sector {j+1}")
    ax[3].plot(eps, spread, color=WARM[2], lw=1.2, label="root spread")
    ax[3].plot(eps, anis, color=WARM[6], lw=1.0, ls="--", label="RMS anisotropy")
    panel(ax[0], "a", "Frozen anisotropic control", "principal direction", r"$q_i/q_1-1$")
    panel(ax[1], "b", "Individual root shifts", "principal direction", r"$u_i^*-1$")
    panel(ax[2], "c", "Continuous perturbation tracking", r"anisotropy amplitude $\epsilon$", r"$u_i^*$")
    panel(ax[3], "d", "Loss of common-root condition", r"$\epsilon$", "root separation")
    ax[0].set_xticks(range(4), [r"$q_1$", r"$q_2$", r"$q_3$", r"$q_4$"])
    ax[1].set_xticks(range(4), [r"$u_1$", r"$u_2$", r"$u_3$", r"$u_4$"])
    ax[2].legend(ncol=2); ax[3].legend()
    records = series_records("c", "root_1", eps, roots[:, 0], "anisotropy_epsilon", "root_w_over_w_star")
    for j in range(1, 4):
        records += series_records("c", f"root_{j+1}", eps, roots[:, j], "anisotropy_epsilon", "root_w_over_w_star")
    return finish("FIG14", fig, ax, title,
        ["Preregistered principal coupling ratios.", "Resulting four exact sector-root displacements.",
         "Analytic continuation of the same perturbation pattern.", "Root spread and RMS anisotropy."],
        [HODGE_CSV, ROOT / "reproducibility/figures/p0_05_r7/make_r7.py"], "ANALYTIC_VISUALIZATION_EVALUATION + FROZEN_CONTROL",
        "exact anisotropic first-shell control", "EXTENDED_DATA_TIER_B", "anisotropy amplitude", "sector roots and spread",
        "q_i/q_1=(1.10,0.90,1.05,0.95)",
        "even a modest trace-preserving anisotropy splits the single root into four distinct crossings.", records,
        ["exact root evaluation", "spread", "RMS anisotropy"])


@register("FIG15")
def fig15():
    title = "Full-kernel continuation bounds and retained unresolved status"
    fig, ax = make_figure(title)
    m6 = read_json(M6_CERT); m7 = read_json(M7_CERT)
    levels = np.array([6, 7])
    c2 = np.array([float(m6["tail_sharpening_relative_to_m6"]["m6_coordinate_C2_upper"]), float(m7["tail"]["C2_coordinate_trace"])])
    interval_lo = np.array([float(m6["m6_common_root_interval_retained"][0]), float(m7["common_root_necessary_interval"][0])])
    interval_hi = np.array([float(m6["m6_common_root_interval_retained"][1]), float(m7["common_root_necessary_interval"][1])])
    lambdas = np.array([0.125, 0.20, 0.25])
    margins = np.array([4.942858161, 1.942858161, 0.942858161])
    schur = np.array([1906.743, 493.071, 419.680])
    ax[0].semilogy(levels, c2, marker="o", color=WARM[2], lw=1.2)
    ax[1].errorbar(levels, (interval_lo + interval_hi)/2, yerr=(interval_hi-interval_lo)/2,
                   fmt="o", color=WARM[3], ecolor=WARM[5], capsize=4)
    ax[2].plot(lambdas, margins, marker="o", color=WARM[4], lw=1.2)
    ax[3].semilogy(lambdas, schur, marker="s", color=WARM[6], lw=1.2)
    ax[2].scatter([0.20], [margins[1]], s=55, facecolor="none", edgecolor=WARM[0], lw=1.0, label="primary unresolved case")
    panel(ax[0], "a", "Certified C2 tail sharpening", "exact shell level $m$", r"coordinate $C^2$ tail$/|w|$")
    panel(ax[1], "b", "Necessary root interval", "shell level $m$", r"$t/w$ interval")
    panel(ax[2], "c", "Schur convergence margin", r"$\lambda_\perp/a_B$", r"$a/\lambda_\perp-\kappa_Ba$")
    panel(ax[3], "d", "Coarse operator-norm majorant", r"$\lambda_\perp/a_B$", r"$M/|w|$")
    ax[2].legend()
    records = series_records("a", "C2 tail", levels, c2, "shell_level", "C2_tail_per_abs_w")
    records += series_records("c", "Schur margin", lambdas, margins, "lambda_perp_over_aB", "convergence_margin")
    records += series_records("d", "Schur majorant", lambdas, schur, "lambda_perp_over_aB", "M_over_abs_w")
    return finish("FIG15", fig, ax, title,
        ["M6-to-M7 reduction of the certified coordinate-$C^2$ tail.", "Necessary common-root interval remains broad.",
         "Positive Schur margins for the three frozen decay lengths, with $0.20$ marked as the retained primary unresolved case.",
         "Corresponding rigorous coarse row-sum bounds."],
        [M6_CERT, M7_CERT, INF_CERT], "FROZEN_CERTIFICATE_VALUES", "directed-rounding certificate values",
        "MAIN_TEXT_TIER_A", "shell level; lambda_perp/a_B", "tail bound; root interval; Schur margin",
        "lambda_perp/a_B={0.125,0.20,0.25}; no retuning",
        "M7 sharpens the tail by more than fivefold but does not certify a full-tensor root; the primary 0.20 case remains unresolved.", records,
        ["certificate extraction", "interval half-width", "log scaling"])


@register("FIG16")
def fig16():
    title = "Gap, bandwidth, velocity, and Hessian validation versus coupling"
    fig, ax = make_figure(title)
    obs = read_csv(OBS_CSV)
    u = np.array([as_float(r["w_over_w_star"]) for r in obs])
    bw = np.array([as_float(r["even_bandwidth_over_t"]) for r in obs])
    gap = np.array([as_float(r["signed_lower_isolation_gap_over_t"]) for r in obs])
    vel = np.array([as_float(r["maximum_generalized_velocity_t_over_hbar"]) for r in obs])
    hess = np.array([as_float(r["maximum_absolute_hessian_over_t"]) for r in obs])
    ax[0].plot(u, gap, marker="o", color=WARM[2], lw=1.2)
    ax[1].plot(u, bw, marker="s", color=WARM[3], lw=1.2)
    ax[2].plot(u, vel, marker="^", color=WARM[4], lw=1.2)
    ax[3].plot(u, hess, marker="D", color=WARM[5], lw=1.2)
    for a in ax: a.axvline(1, color=NEUTRAL, lw=0.7, ls="--")
    panel(ax[0], "a", "Signed lower isolation gap", r"$w/w_*$", r"$\Delta^L/t$")
    panel(ax[1], "b", "Target even-sector bandwidth", r"$w/w_*$", r"$W_+/t$")
    panel(ax[2], "c", "Maximum generalized velocity", r"$w/w_*$", r"$v_{\max}\hbar/t$")
    panel(ax[3], "d", "Maximum absolute Hessian", r"$w/w_*$", r"$\max|\lambda_i|/t$")
    records = series_records("a", "gap", u, gap, "w_over_w_star", "gap_over_t")
    records += series_records("b", "bandwidth", u, bw, "w_over_w_star", "bandwidth_over_t")
    records += series_records("c", "velocity", u, vel, "w_over_w_star", "velocity_t_over_hbar")
    records += series_records("d", "hessian", u, hess, "w_over_w_star", "max_abs_hessian_over_t")
    return finish("FIG16", fig, ax, title,
        ["Positive external isolation gap.", "Exact target bandwidth collapse.", "Velocity suppression.", "Hessian suppression."],
        [OBS_CSV, MAGIC_YES], "FROZEN_NUMERICAL_VALIDATION", "exact first-shell character-torus observables",
        "MAIN_TEXT_TIER_A", "w/w_*", "gap; bandwidth; velocity; Hessian", "five frozen coupling points",
        "bandwidth, velocity, and every Hessian scale vanish together at the isolated positive root while the external gap remains open.", records,
        ["direct column extraction", "normalization by t"])


def hodge_data():
    rows = read_csv(HODGE_CSV)
    u = np.array([as_float(r["w_over_w_star"]) for r in rows])
    vals = np.array([[as_float(r[f"lambda_{i}_over_t"]) for i in range(1, 5)] for r in rows])
    return rows, u, vals


@register("FIG17")
def fig17():
    title = "Hodge Hessian principal eigenvalues at the protected root"
    fig, ax = make_figure(title)
    rows, u, vals = hodge_data()
    for j in range(4):
        ax[0].plot(u, vals[:, j], marker=["o","s","^","D"][j], color=WARM[j+2], lw=1.1, label=rf"$\lambda_{j+1}$")
    trace = vals.sum(axis=1); maxabs = np.max(np.abs(vals), axis=1); split = vals.max(axis=1)-vals.min(axis=1)
    ax[1].plot(u, trace, marker="o", color=WARM[2], lw=1.2)
    ax[2].plot(u, maxabs, marker="s", color=WARM[4], lw=1.2)
    ax[3].semilogy(u, np.maximum(split, 1e-18), marker="D", color=WARM[6], lw=1.2)
    for a in ax: a.axvline(1, color=NEUTRAL, lw=0.7, ls="--")
    ax[0].axhline(0, color=NEUTRAL, lw=0.7, ls="-.")
    panel(ax[0], "a", "All four principal curvatures", r"$w/w_*$", r"$\lambda_i/t$")
    panel(ax[1], "b", "Hodge trace", r"$w/w_*$", r"$\mathrm{Tr}H/t$")
    panel(ax[2], "c", "Maximum curvature magnitude", r"$w/w_*$", r"$\max_i|\lambda_i|/t$")
    panel(ax[3], "d", "Eigenvalue splitting residual", r"$w/w_*$", r"$\lambda_{\max}-\lambda_{\min}$")
    ax[0].legend(ncol=2)
    records = []
    for j in range(4): records += series_records("a", f"lambda_{j+1}", u, vals[:,j], "w_over_w_star", "lambda_over_t")
    return finish("FIG17", fig, ax, title,
        ["All principal eigenvalues of the registered Hodge Hessian.", "Their trace.", "Spectral maximum norm.", "Numerical degeneracy residual."],
        [HODGE_CSV], "FROZEN_NUMERICAL_VALIDATION", "registered first-shell values",
        "MAIN_TEXT_TIER_A", "w/w_*", "Hodge eigenvalues", "G=I4 validation normalization",
        "all four principal curvatures cross zero together and remain degenerate within the frozen output precision.", records,
        ["direct column extraction", "trace", "spectral spread"])


@register("FIG18")
def fig18():
    title = "Independent Hodge tensor components versus coupling"
    fig, ax = make_figure(title)
    cert = read_json(COMMUTANT_CERT)
    cmat = np.array([[float(v) for v in row] for row in cert["physical_first_shell_tensor_C_S"]])
    u = np.linspace(0.7, 1.3, 500)
    tensors = 2 * (1-u[:,None,None]) * cmat[None,:,:]
    records=[]
    groups = [[(0,0),(0,1),(0,2)],[(0,3),(1,1),(1,2)],[(1,3),(2,2),(2,3)],[(3,3),(2,0),(3,0)]]
    for p, pairs in enumerate(groups):
        for k,(i,j) in enumerate(pairs):
            y=tensors[:,i,j]
            ax[p].plot(u,y,color=WARM[2+k+p],lw=1.0,label=rf"$H_{{{i+1}{j+1}}}$")
            records += series_records(chr(97+p), f"H_{i+1}{j+1}", u, y, "w_over_w_star", "tensor_component_over_t")
        panel(ax[p], chr(97+p), f"Tensor component group {p+1}", r"$w/w_*$", r"$H_{ij}/t$")
        ax[p].axvline(1,color=NEUTRAL,lw=.7,ls="--"); ax[p].axhline(0,color=NEUTRAL,lw=.7,ls="-."); ax[p].legend(ncol=2)
    return finish("FIG18", fig, ax, title,
        ["Components $(11,12,13)$.", "Components $(14,22,23)$.", "Components $(24,33,34)$.", "Remaining symmetry-related entries."],
        [COMMUTANT_CERT], "ANALYTIC_VISUALIZATION_EVALUATION + EXACT_TENSOR_CERTIFICATE", "exact first-shell tensor",
        "EXTENDED_DATA_TIER_B", "w/w_*", "Hodge tensor components", "H(u)=2(1-u)C_S",
        "every independent first-shell tensor component vanishes at the same coupling in the symmetric certified model.", records,
        ["exact tensor scaling evaluation"])


@register("FIG19")
def fig19():
    title = "Symmetry-breaking Hodge-Hessian splitting"
    fig, ax = make_figure(title)
    _, u, sym = hodge_data()
    ratios=np.array([1.10,0.90,1.05,0.95]); broken=2*(1-u[:,None]*ratios[None,:])
    for j in range(4): ax[0].plot(u,broken[:,j],marker=["o","s","^","D"][j],color=WARM[j+2],lw=1.0,label=rf"$\lambda_{j+1}$")
    spread=broken.max(axis=1)-broken.min(axis=1)
    centered=broken-broken.mean(axis=1,keepdims=True); anis=np.sqrt(np.sum(centered**2,axis=1))
    roots=1/ratios
    ax[1].plot(u,spread,marker="o",color=WARM[3],lw=1.2)
    ax[2].plot(u,anis,marker="s",color=WARM[5],lw=1.2)
    ax[3].stem(np.arange(4),roots-1,linefmt=WARM[2],markerfmt="o",basefmt=NEUTRAL)
    panel(ax[0],"a","Broken-control eigenvalues",r"$w/w_*$",r"$\lambda_i/t$")
    panel(ax[1],"b","Principal-value spread",r"$w/w_*$",r"$\lambda_{\max}-\lambda_{\min}$")
    panel(ax[2],"c","Traceless Frobenius norm",r"$w/w_*$",r"$\|H-\mathrm{Tr}H I/4\|_F/t$")
    panel(ax[3],"d","Directional root displacement","principal direction",r"$u_i^*-1$")
    ax[0].legend(ncol=2); ax[3].set_xticks(range(4),["1","2","3","4"])
    records=[]
    for j in range(4): records += series_records("a",f"lambda_{j+1}",u,broken[:,j],"w_over_w_star","lambda_over_t")
    return finish("FIG19",fig,ax,title,
        ["Four principal eigenvalues for the preregistered anisotropic control.","Spectral spread.","Basis-invariant anisotropy norm.","Four separated root shifts."],
        [HODGE_CSV,ROOT/"reproducibility/figures/p0_05_r7/make_r7.py"],"ANALYTIC_VISUALIZATION_EVALUATION + FROZEN_CONTROL","exact anisotropic control",
        "MAIN_TEXT_TIER_A","w/w_*; direction","Hessian eigenvalues; anisotropy; root shift","q_i/q_1=(1.10,0.90,1.05,0.95)",
        "trace cancellation survives at $u=1$, but the full Hessian does not vanish because symmetry breaking leaves a resolved traceless component.",records,
        ["exact anisotropic evaluation","spectral spread","Frobenius norm"])


@register("FIG20")
def fig20():
    title = "Derivative margins and finite-difference convergence"
    fig, ax = make_figure(title)
    rows=read_csv(DERIV_CSV); h=np.array([as_float(r["step"]) for r in rows])
    verr=np.array([as_float(r["velocity_abs_error"]) for r in rows]); herr=np.array([as_float(r["hessian_max_abs_error"]) for r in rows])
    ratios=np.array([1.10,0.90,1.05,0.95]); slopes=-2*ratios
    ax[0].loglog(h,verr,marker="o",color=WARM[2],lw=1.2,label="velocity error")
    ax[0].loglog(h,herr,marker="s",color=WARM[5],lw=1.2,label="Hessian error")
    ax[1].loglog(h,verr/h**2,marker="o",color=WARM[3],lw=1.2,label=r"$\epsilon_v/h^2$")
    ax[1].loglog(h,herr/h**2,marker="s",color=WARM[6],lw=1.2,label=r"$\epsilon_H/h^2$")
    ax[2].bar(np.arange(4),slopes,color=WARM[2:6]); ax[2].axhline(-2,color=NEUTRAL,lw=.7,ls="--")
    ax[3].bar(np.arange(4),slopes-slopes.mean(),color=WARM[3:7]); ax[3].axhline(0,color=NEUTRAL,lw=.7,ls="-.")
    panel(ax[0],"a","Finite-difference absolute errors","step $h$","absolute error")
    panel(ax[1],"b","Second-order scaled errors","step $h$",r"error$/h^2$")
    panel(ax[2],"c","Directional crossing slopes","principal direction",r"$d\lambda_i/du$")
    panel(ax[3],"d","Slope deviation from the mean","principal direction",r"$d\lambda_i/du-\overline{s}$")
    ax[0].legend();ax[1].legend();ax[2].set_xticks(range(4),["1","2","3","4"]);ax[3].set_xticks(range(4),["1","2","3","4"])
    records=series_records("a","velocity error",h,verr,"finite_difference_step","absolute_error")
    records+=series_records("a","Hessian error",h,herr,"finite_difference_step","absolute_error")
    records+=series_records("c","anisotropic slopes",np.arange(1,5),slopes,"principal_direction","eigenvalue_slope")
    return finish("FIG20",fig,ax,title,
        ["Registered velocity and Hessian finite-difference errors.","Errors divided by $h^2$.","Analytic principal crossing slopes.","Slope deviations quantifying anisotropic loss of a common derivative margin."],
        [DERIV_CSV,ROOT/"reproducibility/figures/p0_05_r7/make_r7.py"],"FROZEN_NUMERICAL_VALIDATION + ANALYTIC_CONTROL","finite-difference data and exact slopes",
        "EXTENDED_DATA_TIER_B","finite-difference step; direction","errors; crossing slopes","seven-eighths coupling audit",
        "the numerical derivatives converge at second order, while anisotropy creates a resolved spread in crossing slopes.",records,
        ["error normalization by h^2","exact slope extraction"])






