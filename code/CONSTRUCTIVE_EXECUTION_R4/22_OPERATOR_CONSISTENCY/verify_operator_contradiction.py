"""Independent fail-closed replay of the A1 operator-scope contradiction."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "OPERATOR_CONTRADICTION_REPLAY.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


paths = {
    "manuscript": ROOT / "source_current_195/main.tex",
    "model_contract": ROOT / "production_code/MODEL_CONTRACT.md",
    "benchmark": ROOT / "production_code/config/theory_production_benchmark.yaml",
    "model": ROOT / "production_code/config/model.yaml",
    "math_freeze": ROOT / "CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json",
    "math_root": ROOT / "CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/CAND-R4-0005_ROOT_CERTIFICATE.json",
}

texts = {name: path.read_text(encoding="utf-8") for name, path in paths.items()}

checks = {
    "frozen_interval_is_continuous": "interval: [0, pi/8]" in texts["benchmark"],
    "frozen_initial_grid_has_91_points": "initial_uniform_points: 91" in texts["benchmark"],
    "fixed_full_2N_model_required": "hamiltonian: full_2N_bilayer_block_matrix" in texts["model"],
    "paired_cover_all_pairs_required": "interlayer: paired_cover_full_radial_all_pairs" in texts["model"],
    "manuscript_states_infinite_coincidence_index": "eq:fc-incommensurate-infinite-index" in texts["manuscript"],
    "manuscript_states_no_common_periodic_quotient": "No finite common periodic bilayer quotient exists" in texts["manuscript"],
    "manuscript_limits_paired_cover_to_local_observables": "This construction supports local Hamiltonian and local spectral" in texts["manuscript"],
    "manuscript_denies_complete_global_periodic_spectrum": "or a complete global periodic spectrum" in texts["manuscript"],
    "contract_requires_full_fixed_matrix": "| MC-001 | Use the complete one-particle Hamiltonian" in texts["model_contract"],
    "contract_requires_lift_minimum": "| MC-002 | Use the exact Poincar" in texts["model_contract"] and "subgroup-lift minimization" in texts["model_contract"],
    "contract_requires_fixed_fibre_derivatives": "| MC-006 | Differentiate geometry, Hamiltonian and target projectors on one fixed Hilbert-space fiber" in texts["model_contract"],
    "contract_requires_global_observables": "| MC-010 | Evaluate physical flatness" in texts["model_contract"] and "bandwidth, isolation gap, maximum velocity" in texts["model_contract"],
    "contract_requires_exact_finite_DOS": "| MC-017 | Compute exact finite DOS together with independent KPM and SLQ estimates" in texts["model_contract"],
    "mathematical_root_preserved": "AEEE9C3AB53239DDD6231A870AEAA88C61881DF4B6D187F4CAA5B0F550549618" in texts["math_root"],
}

all_checks_pass = all(checks.values())
classification = (
    "FAIL_MATHEMATICAL_CONTRADICTION_REPRODUCED"
    if all_checks_pass
    else "REPLAY_INPUT_OR_EXPECTATION_MISMATCH"
)

payload = {
    "schema_version": "1.0",
    "classification": classification,
    "candidate_id": "CAND-R4-0005",
    "mathematical_root": "AEEE9C3AB53239DDD6231A870AEAA88C61881DF4B6D187F4CAA5B0F550549618",
    "contradiction": {
        "local_theorem": "generic incommensurate paired covers support local Hamiltonians/local spectral observables only and do not create a complete global periodic spectrum",
        "mandatory_contract": "one fixed 92160-dimensional full quotient Hamiltonian over the generic-twist grid with global band, derivative, and complete DOS observables",
        "resource_independence": "the conflict is unchanged by precision, solver, Krylov, KPM, probe, memory, wall-time, or HPC settings",
    },
    "checks": checks,
    "all_checks_pass": all_checks_pass,
    "input_hashes_sha256": {name: sha256(path) for name, path in paths.items()},
    "replayed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}

temporary = OUT.with_suffix(".json.tmp")
temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
temporary.replace(OUT)
print(json.dumps({"classification": classification, "checks": f"{sum(checks.values())}/{len(checks)}"}, indent=2))

if not all_checks_pass:
    raise SystemExit(1)
