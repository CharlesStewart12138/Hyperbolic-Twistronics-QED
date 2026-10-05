"""Second-opinion audit of the generic-twist A1 blocker.

This replay uses the 471-page companion theory and implementation sources that
were not part of the first 14-condition replay.
"""

from __future__ import annotations

import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "SECOND_OPINION_REPLAY.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


paths = {
    "companion": ROOT / "source_companion_471/main.tex",
    "code_log": ROOT / "CODE_WORK_LOG.md",
    "mc002": ROOT / "production_code/contract_rules/mc_002.py",
    "mc006": ROOT / "production_code/contract_rules/mc_006.py",
    "mc002_tests": ROOT / "production_code/tests/test_model_contract_mc002.py",
    "kernel_config": ROOT / "production_code/config/kernel.yaml",
    "model_config": ROOT / "production_code/config/model.yaml",
    "benchmark": ROOT / "production_code/config/theory_production_benchmark.yaml",
    "matrix_free": ROOT / "production_code/group/matrix_free_bilayer.py",
    "prior_status_audit": ROOT / "P0-03-02_CHAPTER_STATUS_AUDIT.md",
}
texts = {name: path.read_text(encoding="utf-8") for name, path in paths.items()}
kernel = yaml.safe_load(texts["kernel_config"])

tree = ast.parse(texts["matrix_free"])
matrix_free_definitions = {
    node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))
}
generic_builder_names = {
    "build_paired_cover_hamiltonian",
    "construct_generic_twist_interlayer",
    "enumerate_paired_cover_support",
    "paired_cover_distance",
}

checks = {
    "companion_denies_single_periodic_quotient": "generic incommensurate bilayer $\\not\\equiv$ single periodic finite quotient" in texts["companion"],
    "companion_defines_local_pattern": "eq:IFEL_local_pattern_definition" in texts["companion"],
    "companion_calls_paired_cover_nonperiodic": "It is not an exact periodic bilayer" in texts["companion"],
    "companion_forbids_global_artificial_interpretation": "Global quantities derived from an artificial identification of the two" in texts["companion"] and "should not be interpreted as exact bulk observables" in texts["companion"],
    "companion_defines_Hloc": "H_{N}^{\\mathrm{loc}}" in texts["companion"] and "local spectral observables without imposing an artificial common periodic supercell" in texts["companion"],
    "companion_separates_commensurate_and_incommensurate_hierarchies": "For an exact commensurate configuration" in texts["companion"] and "For an incommensurate target twist, the numerical hierarchy is fundamentally different" in texts["companion"],
    "prior_audit_keeps_global_bulk_open": "OP for global bulk; RA/MV for local construction" in texts["prior_status_audit"],
    "code_log_says_lift_search_set_missing": "Parameters still missing: production quotient, certified lift search set, injectivity radius and cutoff" in texts["code_log"],
    "mc002_accepts_asserted_boolean": 'contract_value(config, "geometry.lift_invariance_verified", RULE_ID) is True' in texts["mc002"] and 'contract_value(config, "geometry.local_uniqueness_certified", RULE_ID) is True' in texts["mc002"],
    "mc002_test_supplies_asserted_boolean": '"lift_invariance_verified": True' in texts["mc002_tests"] and '"local_uniqueness_certified": True' in texts["mc002_tests"],
    "mc006_accepts_asserted_fixed_fiber": '== "fixed_fiber"' in texts["mc006"] and '"twist.dimension_constant"' in texts["mc006"],
    "kernel_cutoff_and_tail_unfrozen": kernel.get("cutoff") is None and kernel.get("tail_budget") is None,
    "matrix_free_requires_caller_supplied_pairs": "The caller supplies" in texts["matrix_free"] and "complete supported pair list" in texts["matrix_free"],
    "no_generic_builder_in_matrix_free_module": not (matrix_free_definitions & generic_builder_names),
    "frozen_grid_not_commensurate_only": "interval: [0, pi/8]" in texts["benchmark"] and "initial_uniform_points: 91" in texts["benchmark"],
    "fixed_full_space_model_required": "hamiltonian: full_2N_bilayer_block_matrix" in texts["model_config"] and "paired_cover_full_radial_all_pairs" in texts["model_config"],
}

all_pass = all(checks.values())
payload = {
    "schema_version": "1.0",
    "classification": "SECOND_OPINION_CONFIRMS_MATHEMATICAL_CONTRADICTION" if all_pass else "SECOND_OPINION_INCONCLUSIVE",
    "independent_scope": "471-page companion theory plus implementation/test semantics; excludes first replay source set where possible",
    "logical_core": {
        "theory": "generic incommensurate production is local H_N^loc and is not a single global periodic finite quotient",
        "contract": "fixed 92160-dimensional full quotient operator and global observables over a non-commensurate-only continuous grid",
        "implementation": "schema validators accept asserted booleans; no complete generic paired-cover support constructor or terminating lift-search certificate exists",
    },
    "checks": checks,
    "all_checks_pass": all_pass,
    "matrix_free_definitions": sorted(matrix_free_definitions),
    "missing_generic_builder_names": sorted(generic_builder_names - matrix_free_definitions),
    "input_hashes_sha256": {name: sha256(path) for name, path in paths.items()},
    "verified_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}

temporary = OUT.with_suffix(".json.tmp")
temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
temporary.replace(OUT)
print(json.dumps({"classification": payload["classification"], "checks": f"{sum(checks.values())}/{len(checks)}"}, indent=2))
if not all_pass:
    raise SystemExit(1)
