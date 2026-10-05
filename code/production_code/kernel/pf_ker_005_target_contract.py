"""Build the noncircular PF-KER-005 target-contract audit certificate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FREEZE = ROOT / "production_code" / "config" / "freeze_records"
OUT_JSON = ROOT / "production_code" / "kernel" / "PF_KER_005_TARGET_CONTRACT.json"
OUT_MD = ROOT / "production_code" / "kernel" / "PF_KER_005_TARGET_CONTRACT.md"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_contract() -> dict[str, Any]:
    target = {
        key: _load_json(FREEZE / f"{key}.json")
        for key in ("PF-TGT-001", "PF-TGT-002", "PF-TGT-003", "PF-TGT-004", "PF-TGT-005")
    }
    rep4 = _load_json(FREEZE / "PF-REP-004.json")
    cutoff = _load_json(FREEZE / "PF-KER-002.json")
    dos = _load_json(FREEZE / "PF-DOS-001.json")
    tails = _load_json(ROOT / "production_code" / "kernel" / "PF_KER_005_CANONICAL_TAILS.json")

    # A frozen target may not be synthesized by filling null authority records.
    for key in ("PF-TGT-001", "PF-TGT-002", "PF-TGT-003", "PF-TGT-004"):
        if target[key]["frozen_value"] is not None or target[key]["status"] != "Blocked":
            raise RuntimeError(f"authoritative target input changed: {key}")
    if rep4["frozen_value"] is not None or rep4["status"] != "Blocked":
        raise RuntimeError("authoritative target representation input changed: PF-REP-004")
    if cutoff["status"] != "Fixed" or cutoff["frozen_value"]["cutoff_over_a"]["primary"] != 3:
        raise RuntimeError("registered hopping cutoff changed")

    m6 = next(row for row in tails["selected_tail_rows_per_abs_w"] if row["first_omitted_shell"] == 6)
    fields: dict[str, Any] = {
        "target_ancestry": {
            "value": None,
            "status": "MISSING",
            "authority": ["PF-TGT-001", "PF-TGT-004"],
            "required_object": "an ex-ante reference projector/anchor and fixed rank-energy-layer-parity-point-group-translation-window-orbital signature",
        },
        "target_contour_C": {
            "value": None,
            "status": "MISSING",
            "authority": ["PF-TGT-002"],
            "required_object": "a preregistered common Riesz contour or adaptive contour rule with a certified same-scope spectral-distance margin",
        },
        "target_rank": {
            "value": None,
            "status": "MISSING",
            "authority": ["PF-TGT-003"],
            "required_object": "the reference-projector rank and a certified rank-change policy",
        },
        "minimum_isolation_gap_Delta_C": {
            "value": None,
            "status": "MISSING",
            "authority": ["main.tex:eq:M5-isolation-gap"],
            "required_object": "a positive uniform lower bound over the same target, representation, cover, and parameter domain",
        },
        "M1": {
            "value": None,
            "status": "MISSING",
            "authority": ["main.tex:eq:release-velocity-tail-bound", "main.tex:eq:release-D01-band-derivative-bridge"],
            "required_object": "a uniform same-scope bound on first operator derivatives",
        },
        "M2": {
            "value": None,
            "status": "MISSING",
            "authority": ["main.tex:eq:release-band-Hessian-tail-bound", "main.tex:eq:release-D01-band-derivative-bridge"],
            "required_object": "a uniform same-scope bound on second operator derivatives",
        },
        "C0_acceptance_tolerance": {
            "value": None,
            "status": "MISSING",
            "required_object": "separate numerical tolerances for energy, bandwidth, isolation gap, and Riesz-projector error",
        },
        "C1_acceptance_tolerance": {
            "value": None,
            "status": "MISSING",
            "required_object": "separate numerical tolerances for generalized velocity and first spectral derivatives",
        },
        "C2_acceptance_tolerance": {
            "value": None,
            "status": "MISSING",
            "required_object": "separate numerical tolerances for Hessian, principal curvature, and Hodge comparison",
        },
        "parameter_domain": {
            "value": None,
            "status": "PARTIAL_NOT_TARGET_SPECIFIC",
            "available": {
                "hyperbolic_twist_irreducible_interval": ["0", "pi/8"],
                "frozen_kernel_point": tails["frozen_point"],
            },
            "missing": ["target-specific coupled parameter domain", "registered w/t domain", "production grid and solver tolerances"],
        },
        "representation_scope": {
            "value": None,
            "status": "MISSING",
            "authority": ["PF-REP-004", "main.tex:eq:release-common-contour-target-restriction"],
            "required_object": "target support on a complete registered finite-group irrep inventory cut by one common contour",
        },
        "cover_scope": {
            "value": None,
            "status": "MISSING",
            "required_object": "a fully globally admissible finite quotient or an explicitly LOCAL operator scope with matching target data",
        },
        "hopping_cutoff": {
            "value": cutoff["frozen_value"],
            "status": "FROZEN_INDEPENDENT_CONSTRAINT",
            "authority": ["PF-KER-002"],
        },
        "normalization": {
            "value": None,
            "status": "PARTIAL_NOT_TARGET_COMPLETE",
            "available": {
                "energy_coordinate": dos["frozen_value"]["energy_coordinate"],
                "global_DOS_mass": dos["frozen_value"]["global_mass_normalization"],
                "target_DOS_rule": dos["frozen_value"]["target_normalization"],
            },
            "missing": "the declared target rank needed to instantiate the target normalization",
        },
    }

    missing = [name for name, item in fields.items() if item["status"] in {"MISSING", "PARTIAL_NOT_TARGET_SPECIFIC", "PARTIAL_NOT_TARGET_COMPLETE"}]
    return {
        "schema_version": 1,
        "task_id": "PF-KER-005-TARGET-CONTRACT",
        "authority": "2026-09-05 highest-priority directive Sections 22-24",
        "scope": "TARGET_REGISTRY_AUDIT; no finite-quotient or bulk promotion",
        "classification": "TARGET-CONTRACT-BLOCKED",
        "status": "Blocked",
        "circularity_rule": {
            "target_selection_may_read_final_flatness_result": False,
            "allowed_selection_bases": ["ancestry", "independently registered continuation anchor", "symmetry/representation identity", "preregistered spectral-island rule"],
            "audit_result": "FAIL_CLOSED_NO_NONCIRCULAR_TARGET",
        },
        "source_equations": [
            "main.tex:eq:M4-reference-rank",
            "main.tex:eq:M4-reference-target-signature",
            "main.tex:eq:M5-isolation-gap",
            "main.tex:eq:release-common-contour-target-restriction",
            "main.tex:eq:release-C1-projector-rotation",
            "main.tex:eq:release-velocity-tail-bound",
            "main.tex:eq:release-Hessian-contour-hypotheses",
            "main.tex:eq:release-band-Hessian-tail-bound",
        ],
        "R_target": fields,
        "missing_or_partial_fields": missing,
        "available_m6_tail_per_abs_w": {
            "first_omitted_shell": 6,
            "C0": m6["c0_per_abs_w"],
            "C1_Hodge": m6["c1_hodge_per_abs_w"],
            "C2_Hodge": m6["c2_hodge_per_abs_w"],
        },
        "derivative_order_acceptance": {
            "C0": "UNRESOLVED",
            "C1": "UNRESOLVED",
            "C2": "UNRESOLVED",
            "reason": "Per-|w| tail norms cannot be normalized against absent same-scope target margins and tolerances.",
        },
        "downstream_gates": {
            "PF_KER_005_derivative_order_closure_released": False,
            "PF_HOD_004_full_tensor_root_released": False,
            "physical_optimizer_may_read_Hodge_outputs": False,
        },
        "primary_blocker": "No independently registered ex-ante target anchor/projector and ancestry signature exist; therefore the target contour, rank, gap and derivative norms cannot be instantiated without circular target selection.",
        "exact_resume_object": {
            "reference_operator": "H_ref on a declared LOCAL or accepted finite-cover scope",
            "reference_parameter_point": "p_0 fixed before inspecting the desired flatness result",
            "reference_projector": "P_C^0 selected by a preregistered spectral-island rule",
            "signature": "(rank, reference energy, layer parity, point-group irrep, translation-sector content, energy window, orbital ancestry)",
            "isolation": "one common contour C with positive uniform distance/gap over the declared parameter domain",
            "derivative_and_acceptance_registry": "same-scope M1, M2 and separate C0/C1/C2 observable tolerances",
        },
        "main_tex_modified": False,
        "new_manuscript_pdf_generated": False,
    }


def render_markdown(c: dict[str, Any]) -> str:
    f = c["R_target"]
    rows = []
    for key, item in f.items():
        value = "null" if item["value"] is None else "frozen; see JSON"
        rows.append(f"| `{key}` | {item['status']} | {value} |")
    rows_text = "\n".join(rows)
    template = r"""# PF-KER-005 target contract

## Decision

`PF-KER-005-TARGET-CONTRACT` is **Blocked** and classified
`TARGET-CONTRACT-BLOCKED`.  This is a fail-closed scientific result: the
repository contains no independently registered ex-ante target anchor or
ancestry signature.  Selecting a band or contour now by inspecting which one
flattens best would violate the noncircularity rule.

The frozen `main.tex` was not modified and no manuscript PDF was generated.

## Coherent registry audit

| Required field | Status | Contract value |
|---|---|---|
{ROWS}

The independent constraints that remain usable are the hyperbolic irreducible
twist interval `[0,pi/8]`, the frozen kernel point `h/a_B=0.50`,
`lambda_perp/a_B=0.20`, the hard-cutoff policy with primary `D_c/a_B=3`, the
energy coordinate `E/t`, and the projector-step target `0.20` with hard limit
strictly below one.  They do not identify a spectral island.

## Mathematical acceptance chain

For one independently fixed target, the manuscript requires the common Riesz
projector

\[
P_{C,\rho}=\frac{1}{2\pi i}\oint_{\mathscr C}
(z-H_N[\rho])^{-1}\,dz
\]

with the same ancestry in every sector.  At first omitted shell `m=6`, the
available canonical bounds per `|w|` are

\[
(T_0,T_1,T_2)_G\le
(0.003856544343098889,\ 1.5561304907547204,\ 629.7779064951307).
\]

They have no PASS/FAIL meaning until a same-scope registry supplies `|w|/t`,
`Delta_C`, `M1`, `M2`, and the three independent tolerance families.  In
particular, the velocity bound needs

\[
T_1+\frac{2M_1T_0}{\Delta_C-T_0},\qquad T_0<\Delta_C/2,
\]

while Hessian transport additionally needs the fixed contour length/distance,
`M2`, and the differentiated-projector terms.  A small `C0` tail cannot certify
`C1` or `C2`.

## Exact stop and resume object

The primary blocker is: **no ex-ante reference projector/anchor and target
ancestry signature exist**.  The exact resume object is a record fixed before
examining the desired flatness result containing `H_ref`, a reference point
`p_0`, a preregistered spectral-island projector `P_C^0`, its complete
signature and rank, a common contour with positive uniform isolation, and the
same-scope `M1`, `M2`, and observable tolerances.

Consequently PF-KER-005 derivative-order closure and PF-HOD-004 full-tensor
root/transversality are not released.
"""
    return template.replace("{ROWS}", rows_text)


def main() -> None:
    contract = build_contract()
    OUT_JSON.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(contract), encoding="utf-8")


if __name__ == "__main__":
    main()
