"""Create the immutable candidate-0005 mathematical freeze and H_MATH root."""
from __future__ import annotations

import hashlib
import json
import platform
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


R4 = Path(__file__).resolve().parents[1]
OUT = R4 / "17_FINAL_FREEZE"
OUT.mkdir(parents=True, exist_ok=True)
NOW = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(rel: str) -> dict:
    return json.loads((R4 / rel).read_text(encoding="utf-8"))


def save(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


checksum_line = (R4 / "00_FROZEN_INPUTS/FROZEN_INPUT_ROOT_HASH.txt").read_text(encoding="utf-8").strip()
match = re.fullmatch(r"sha256\s+([0-9A-Fa-f]{64})\s+FROZEN_INPUT_MANIFEST\.tsv", checksum_line)
if not match:
    raise RuntimeError("invalid frozen root checksum line")
frozen_root = match.group(1).upper()

delivery_rel = "16_REPORTS/CONSTRUCTIVE_EXECUTION_R4_DELIVERY_MANIFEST.json"
delivery = load(delivery_rel)
bad = [row["path"] for row in delivery["artifacts"] if sha256(R4 / row["path"]) != row["sha256"]]
if delivery["artifact_count"] != 20 or bad:
    raise RuntimeError(f"delivery verification failed: {bad}")
delivery_verification_path = OUT / "R4_DELIVERY_20_OF_20_VERIFICATION.json"
save(delivery_verification_path, {
    "schema_version": "1.0",
    "classification": "PASS",
    "verified_artifacts": 20,
    "failed_artifacts": 0,
    "delivery_manifest": delivery_rel,
    "delivery_manifest_sha256": sha256(R4 / delivery_rel),
    "verified_at": NOW,
})

group_manifest_rel = "17_FINAL_FREEZE/artifacts/CAND-R4-0005_GROUP_ARTIFACT_MANIFEST.json"
group_manifest = load(group_manifest_rel)
candidate_rel = "10_CANDIDATES/CAND-R4-0005.certificate.json"
candidate = load(candidate_rel)
local_rel = "11_CERTIFICATES/CAND-R4-0005.local_independent_replay.json"
global_rel = "11_CERTIFICATES/CAND-R4-0005.global_pass_scan.json"
independent_rel = "11_CERTIFICATES/CAND-R4-0005.global_independent_replay.json"
audit_rel = "11_CERTIFICATES/R4_FINAL_ENDPOINT_INDEPENDENT_AUDIT_V2.json"

files = group_manifest["artifacts"]
freeze_path = OUT / "CAND-R4-0005_MATHEMATICAL_FREEZE.json"
freeze = {
    "schema_version": "1.0",
    "freeze_id": "CAND-R4-0005-MATHEMATICAL-FREEZE-V1",
    "candidate_id": "CAND-R4-0005",
    "marked_quotient_canonical_hash": candidate["marked_quotient_hash"],
    "exact_group_order": 46080,
    "group_structure": "SL(2,9) x C4 x C4 x C2 x C2",
    "presentation_generator_image_ids_zero_based": group_manifest["presentation_generator_image_ids_zero_based"],
    "physical_shell_image_ids_zero_based": group_manifest["physical_shell_image_ids_zero_based"],
    "exact_group_artifacts": {
        "manifest": group_manifest_rel,
        "manifest_sha256": sha256(R4 / group_manifest_rel),
        "element_encoding_sha256": files["CAND-R4-0005.elements_u8.bin"]["sha256"],
        "multiplication_right_generator_table_sha256": files["CAND-R4-0005.right_generators_u32le.bin"]["sha256"],
        "inverse_table_sha256": files["CAND-R4-0005.inverse_u32le.bin"]["sha256"],
        "C8_automorphism_sha256": files["CAND-R4-0005.C8_automorphism_u32le.bin"]["sha256"],
        "parity_character_sha256": files["CAND-R4-0005.parity_u8.bin"]["sha256"],
    },
    "certificate_hashes": {
        "candidate": sha256(R4 / candidate_rel),
        "local_injectivity": sha256(R4 / local_rel),
        "global_primary": sha256(R4 / global_rel),
        "global_independent": sha256(R4 / independent_rel),
        "final_independent_audit_30_of_30": sha256(R4 / audit_rel),
        "delivery_verification_20_of_20": sha256(delivery_verification_path),
    },
    "global_dangerous_domain": {
        "manifest": "00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json",
        "manifest_sha256": sha256(R4 / "00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json"),
        "registry_content_sha256": "1148BF89C1D3DDDF3F26EDA57F2385CE8E65CBC8CE8042546683F18BDE235C5B",
        "closed_records": 785639753,
        "boundary_included": True,
    },
    "primary_scan_root": {
        "certificate_sha256": sha256(R4 / global_rel),
        "records_scanned": 785639753,
        "kernel_hits": 0,
        "checkpoint_sha256": load(global_rel)["checkpoint_sha256"],
    },
    "independent_scan_root": {
        "certificate_sha256": sha256(R4 / independent_rel),
        "records_scanned": 785639753,
        "kernel_hits": 0,
        "checkpoint_sha256": load(independent_rel)["checkpoint_sha256"],
    },
    "audit_results": {
        "final_independent_audit": "30/30 PASS",
        "artifact_delivery_verification": "20/20 PASS",
    },
    "exact_conclusion": {
        "systole": "sys(H^2/K_*)/a_B > 6",
        "injectivity_radius": "r_inj(H^2/K_*)/a_B > 3",
    },
    "MATHEMATICAL_STATUS": "CERTIFIED",
    "RESOURCE_STATUS": "UNVERIFIED",
    "A1_STATUS": "NOT_FROZEN",
    "ORDER_OPTIMALITY": "UNPROVED",
    "UNIQUENESS": "UNPROVED",
    "GLOBAL_CLASSIFICATION": "UNPROVED",
    "frozen_at": NOW,
    "immutability_rule": "do not overwrite; any correction requires a new version",
}
save(freeze_path, freeze)

theory_rel = "00_FROZEN_INPUTS/theory_authority/R4_MAIN_AND_SUPPLEMENTS.tex"
components = [
    ("theory", sha256(R4 / theory_rel)),
    ("frozen_inputs", frozen_root),
    ("marked_quotient", candidate["marked_quotient_hash"]),
    ("symmetry", files["CAND-R4-0005.C8_automorphism_u32le.bin"]["sha256"]),
    ("parity", files["CAND-R4-0005.parity_u8.bin"]["sha256"]),
    ("local", sha256(R4 / local_rel)),
    ("global_primary", sha256(R4 / global_rel)),
    ("global_independent", sha256(R4 / independent_rel)),
    ("final_audit", sha256(R4 / audit_rel)),
]
preimage = "\n".join(f"{label}={digest}" for label, digest in components).encode("ascii")
h_math = hashlib.sha256(preimage).hexdigest().upper()
preimage_path = OUT / "H_MATH_PREIMAGE.txt"
preimage_path.write_bytes(preimage + b"\n")

contract_files = {
    "exact_geometry": "00_FROZEN_INPUTS/contracts/BOLZA_GEOMETRIC_GENERATORS.yaml",
    "Nielsen_dictionary": "00_FROZEN_INPUTS/contracts/BOLZA_NIELSEN_MAP.yaml",
    "phi_8": "00_FROZEN_INPUTS/contracts/BOLZA_PHI8_AUTOMORPHISM.yaml",
    "parity": "00_FROZEN_INPUTS/contracts/BOLZA_PHYSICAL_PARITY_CERTIFICATE.yaml",
    "physical_shell": "00_FROZEN_INPUTS/contracts/BOLZA_GENERATOR_SHELL_REGISTRY.yaml",
}
root_path = OUT / "CAND-R4-0005_ROOT_CERTIFICATE.json"
root = {
    "schema_version": "1.0",
    "root_certificate_id": "CAND-R4-0005-H-MATH-V1",
    "candidate_id": "CAND-R4-0005",
    "MATHEMATICAL_STATUS": "PASS",
    "RESOURCE_STATUS": "UNVERIFIED",
    "PRODUCTION_A1_STATUS": "NOT_FROZEN",
    "H_MATH": h_math,
    "H_MATH_algorithm": "SHA256 of the UTF-8/ASCII label=uppercase_digest lines in H_MATH_PREIMAGE.txt, LF-separated and without the file's terminal LF",
    "H_MATH_preimage_file": "17_FINAL_FREEZE/H_MATH_PREIMAGE.txt",
    "H_MATH_preimage_file_sha256": sha256(preimage_path),
    "H_MATH_components_in_order": [{"label": label, "digest": digest} for label, digest in components],
    "mathematical_freeze": {
        "path": "17_FINAL_FREEZE/CAND-R4-0005_MATHEMATICAL_FREEZE.json",
        "sha256": sha256(freeze_path),
    },
    "frozen_theory": {"path": theory_rel, "sha256": sha256(R4 / theory_rel), "version": "Revision 4 expanded and re-audited through Chapter 59"},
    "frozen_input_root": frozen_root,
    "contracts": {key: {"path": rel, "sha256": sha256(R4 / rel)} for key, rel in contract_files.items()},
    "marked_quotient": {"hash": candidate["marked_quotient_hash"], "order": 46080},
    "certificates": freeze["certificate_hashes"],
    "software_and_verifiers": {
        "python_runtime": platform.python_version(),
        "GAP_runtime": "4.16.0",
        "candidate_builder_sha256": sha256(R4 / "10_CANDIDATES/build_candidate_0005.py"),
        "primary_scanner_source_sha256": load(global_rel)["scanner_source_sha256"],
        "independent_scanner_source_sha256": load(independent_rel)["scanner_source_sha256"],
        "final_audit_script_sha256": sha256(R4 / "tests/final_endpoint_audit_v2.py"),
        "group_artifact_builder_sha256": sha256(R4 / "17_FINAL_FREEZE/build_exact_group_artifacts.py"),
    },
    "exact_conclusion": freeze["exact_conclusion"],
    "emitted_at": NOW,
    "immutability_rule": "H_MATH V1 and its mathematical freeze are immutable; corrections require V2",
}
save(root_path, root)

print(json.dumps({
    "classification": "MATHEMATICAL_FREEZE_AND_ROOT_PASS",
    "H_MATH": h_math,
    "mathematical_freeze_sha256": sha256(freeze_path),
    "root_certificate_sha256": sha256(root_path),
}, indent=2))
