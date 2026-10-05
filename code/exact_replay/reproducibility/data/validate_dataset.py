"""Validate one clean-room structured dataset package and its file hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DATASET_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
RESULT_ID_RE = re.compile(r"^R([1-9]|1[0-5])$")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp"}
ALLOWED_STATUS = {"COMPLETE", "PARTIAL", "FAILED_RUN"}
ALLOWED_FILE_ROLES = {"raw", "derived", "coordinate", "parameter", "diagnostic", "uncertainty"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_dataset_package(package_dir: str | Path) -> dict[str, Any]:
    package = Path(package_dir).resolve()
    manifest_path = package / "dataset.json"
    errors: list[str] = []
    checked_files: list[dict[str, Any]] = []

    if not manifest_path.is_file():
        return {"status": "FAIL", "package": str(package), "errors": ["dataset.json is missing"], "checked_files": []}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "package": str(package), "errors": [f"dataset.json cannot be parsed: {exc}"], "checked_files": []}

    required = {
        "schema_version", "dataset_id", "status", "created_by_task", "result_ids", "observable",
        "theory_sources", "parameter_registry_sha256", "geometry", "representation", "finite_cover",
        "algorithm", "environment", "stochastic", "files", "uncertainty", "plotting",
    }
    missing = sorted(required.difference(manifest))
    if missing:
        errors.append(f"Missing required manifest fields: {missing}")

    if manifest.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if not isinstance(manifest.get("dataset_id"), str) or not DATASET_ID_RE.fullmatch(manifest["dataset_id"]):
        errors.append("dataset_id has an invalid format")
    if manifest.get("status") not in ALLOWED_STATUS:
        errors.append("status must be COMPLETE, PARTIAL, or FAILED_RUN")
    if not _nonempty_string(manifest.get("created_by_task")):
        errors.append("created_by_task must be a non-empty string")

    result_ids = manifest.get("result_ids")
    if not isinstance(result_ids, list) or not result_ids or len(result_ids) != len(set(result_ids)):
        errors.append("result_ids must be a non-empty unique list")
    elif not all(isinstance(item, str) and RESULT_ID_RE.fullmatch(item) for item in result_ids):
        errors.append("result_ids may contain only R1 through R15")

    observable = manifest.get("observable")
    if not isinstance(observable, dict) or not all(
        _nonempty_string(observable.get(key)) for key in ("name", "definition", "units")
    ):
        errors.append("observable must define non-empty name, definition, and units")

    theory_sources = manifest.get("theory_sources")
    if not isinstance(theory_sources, list) or not theory_sources:
        errors.append("theory_sources must be a non-empty list")
    elif not all(
        isinstance(item, dict)
        and _nonempty_string(item.get("file"))
        and _nonempty_string(item.get("section_or_equation"))
        for item in theory_sources
    ):
        errors.append("every theory source must identify a file and section or equation")

    for field in ("parameter_registry_sha256",):
        if not isinstance(manifest.get(field), str) or not SHA256_RE.fullmatch(manifest[field]):
            errors.append(f"{field} must be a lowercase SHA-256 hex string")

    for field in ("geometry", "representation", "finite_cover"):
        if not isinstance(manifest.get(field), dict):
            errors.append(f"{field} must be an object")

    algorithm = manifest.get("algorithm")
    if not isinstance(algorithm, dict) or not _nonempty_string(algorithm.get("name")) or not _nonempty_string(algorithm.get("implementation")) or not isinstance(algorithm.get("settings"), dict):
        errors.append("algorithm must contain name, implementation, and settings")

    environment = manifest.get("environment")
    if not isinstance(environment, dict) or not _nonempty_string(environment.get("lock_file")) or not isinstance(environment.get("lock_sha256"), str) or not SHA256_RE.fullmatch(environment["lock_sha256"]):
        errors.append("environment must contain lock_file and lock_sha256")

    stochastic = manifest.get("stochastic")
    if not isinstance(stochastic, dict) or stochastic.get("status") not in {"USED", "NOT_APPLICABLE"} or not _nonempty_string(stochastic.get("reason")) or not isinstance(stochastic.get("streams"), list):
        errors.append("stochastic must contain status, reason, and streams")
    elif stochastic["status"] == "USED":
        seed_hash = stochastic.get("seed_config_sha256")
        if not isinstance(seed_hash, str) or not SHA256_RE.fullmatch(seed_hash):
            errors.append("stochastic USED requires seed_config_sha256")
        if not stochastic["streams"]:
            errors.append("stochastic USED requires at least one stream record")
        for stream in stochastic["streams"]:
            if not isinstance(stream, dict) or not _nonempty_string(stream.get("namespace")) or not isinstance(stream.get("first_index"), int) or stream.get("first_index", -1) < 0 or not isinstance(stream.get("count"), int) or stream.get("count", 0) < 1:
                errors.append("every stochastic stream needs namespace, non-negative first_index, and positive count")
    elif stochastic.get("seed_config_sha256") is not None or stochastic.get("streams") != []:
        errors.append("stochastic NOT_APPLICABLE requires null seed_config_sha256 and an empty streams list")

    files = manifest.get("files")
    observed_paths: set[str] = set()
    observed_roles: dict[str, str] = {}
    if not isinstance(files, list) or not files:
        errors.append("files must be a non-empty list")
    else:
        for entry in files:
            if not isinstance(entry, dict):
                errors.append("each files entry must be an object")
                continue
            relative_text = entry.get("relative_path")
            if not _nonempty_string(relative_text):
                errors.append("each file requires relative_path")
                continue
            relative = Path(relative_text)
            if relative.is_absolute() or ".." in relative.parts:
                errors.append(f"file path must remain inside the dataset package: {relative_text}")
                continue
            normalized = relative.as_posix()
            if normalized in observed_paths:
                errors.append(f"duplicate file path: {normalized}")
                continue
            observed_paths.add(normalized)
            if relative.suffix.lower() in IMAGE_SUFFIXES:
                errors.append(f"rendered image is forbidden as structured data: {normalized}")
            role = entry.get("role")
            if role not in ALLOWED_FILE_ROLES:
                errors.append(f"invalid file role for {normalized}: {role!r}")
            else:
                observed_roles[normalized] = role
            full_path = (package / relative).resolve()
            try:
                full_path.relative_to(package)
            except ValueError:
                errors.append(f"resolved file path escapes package: {normalized}")
                continue
            if not full_path.is_file():
                errors.append(f"declared file is missing: {normalized}")
                continue
            actual_bytes = full_path.stat().st_size
            actual_hash = sha256_file(full_path)
            expected_bytes = entry.get("bytes")
            expected_hash = entry.get("sha256")
            if expected_bytes != actual_bytes:
                errors.append(f"byte count mismatch for {normalized}: expected {expected_bytes}, found {actual_bytes}")
            if expected_hash != actual_hash:
                errors.append(f"SHA-256 mismatch for {normalized}")
            if not _nonempty_string(entry.get("media_type")):
                errors.append(f"media_type is missing for {normalized}")
            checked_files.append({"relative_path": normalized, "bytes": actual_bytes, "sha256": actual_hash})

    uncertainty = manifest.get("uncertainty")
    if not isinstance(uncertainty, dict) or uncertainty.get("status") not in {"AVAILABLE", "NOT_APPLICABLE", "MISSING"} or not isinstance(uncertainty.get("files"), list) or not _nonempty_string(uncertainty.get("justification")):
        errors.append("uncertainty must contain status, files, and justification")
    else:
        uncertainty_files = uncertainty["files"]
        if uncertainty["status"] == "AVAILABLE":
            if not _nonempty_string(uncertainty.get("method")) or not uncertainty_files:
                errors.append("AVAILABLE uncertainty requires a method and at least one file")
            for relative_text in uncertainty_files:
                if observed_roles.get(relative_text) != "uncertainty":
                    errors.append(f"uncertainty file is not declared with role uncertainty: {relative_text}")
        elif uncertainty["status"] == "NOT_APPLICABLE":
            if uncertainty.get("method") is not None or uncertainty_files:
                errors.append("NOT_APPLICABLE uncertainty requires null method and an empty files list")
        elif manifest.get("status") == "COMPLETE":
            errors.append("a COMPLETE dataset cannot declare uncertainty MISSING")

    plotting = manifest.get("plotting")
    if not isinstance(plotting, dict) or plotting.get("compute_plot_separated") is not True or plotting.get("raw_data_is_source") is not True or not isinstance(plotting.get("plot_scripts"), list):
        errors.append("plotting must enforce compute/plot separation and structured data as source")

    return {
        "status": "PASS" if not errors else "FAIL",
        "package": str(package),
        "dataset_id": manifest.get("dataset_id"),
        "checked_files": checked_files,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="Dataset directory containing dataset.json")
    parser.add_argument("--output", type=Path, default=None, help="Optional validation-report JSON path")
    args = parser.parse_args()
    report = validate_dataset_package(args.package)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
