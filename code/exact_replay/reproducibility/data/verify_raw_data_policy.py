"""Self-test the raw-data contract without creating scientific results."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

from validate_dataset import sha256_file, validate_dataset_package


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> dict[str, object]:
    checks: dict[str, bool] = {}
    figure_registry = json.loads((HERE / "figure_data_manifest.json").read_text(encoding="utf-8"))
    schema = json.loads((HERE / "dataset_schema.json").read_text(encoding="utf-8"))
    figures = figure_registry.get("figures", [])
    required_fields = {
        "manuscript_order",
        "task_id",
        "run_id",
        "latex_label",
        "scientific_scope",
        "figure_pdf",
        "figure_pdf_sha256",
        "source_data",
        "source_data_sha256",
        "generator",
        "generator_sha256",
        "plot_config",
        "plot_config_sha256",
        "run_record",
    }
    checks["schema_json_parses"] = schema.get("title") == "Clean-room scientific dataset manifest"
    checks["current_registry_schema_v2"] = (
        figure_registry.get("schema_version") == 2
        and figure_registry.get("registry_status") == "COMPLETE_CURRENT_MANUSCRIPT"
    )
    checks["eight_current_figures_registered"] = (
        len(figures) == 8 == figure_registry.get("main_figure_count")
        and [item.get("manuscript_order") for item in figures] == list(range(1, 9))
    )
    checks["required_mapping_fields_complete"] = all(
        required_fields.issubset(item)
        and all(item.get(field) not in (None, "") for field in required_fields)
        and all(len(item.get(field, "")) == 64 for field in (
            "figure_pdf_sha256", "source_data_sha256", "generator_sha256", "plot_config_sha256"
        ))
        for item in figures
    )
    checks["unique_figure_labels_and_paths"] = (
        len({item.get("latex_label") for item in figures}) == len(figures)
        and len({item.get("figure_pdf") for item in figures}) == len(figures)
    )
    manuscript = (PROJECT_ROOT / figure_registry["manuscript"]).read_text(encoding="utf-8")
    included = {
        (PROJECT_ROOT / "source_current_195" / match).resolve().relative_to(PROJECT_ROOT).as_posix()
        for match in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", manuscript)
    }
    mapped = {item["figure_pdf"] for item in figures}
    hash_pairs = (
        ("figure_pdf", "figure_pdf_sha256"),
        ("source_data", "source_data_sha256"),
        ("generator", "generator_sha256"),
        ("plot_config", "plot_config_sha256"),
    )
    registered_files_exist = True
    registered_hashes_match = True
    run_records_exist = True
    for item in figures:
        for path_key, hash_key in hash_pairs:
            path = PROJECT_ROOT / item[path_key]
            exists = path.is_file()
            registered_files_exist = registered_files_exist and exists
            registered_hashes_match = registered_hashes_match and (
                exists and _sha256(path) == item[hash_key]
            )
        run_records_exist = run_records_exist and (
            PROJECT_ROOT / item["run_record"]
        ).is_file()
    checks["registered_files_exist"] = registered_files_exist
    checks["registered_hashes_match"] = registered_hashes_match
    checks["run_records_exist"] = run_records_exist

    checks["manuscript_mapping_is_closed_set"] = included == mapped
    checks["no_unplotted_production_target_promoted"] = bool(
        figure_registry.get("planning_scope_note")
    ) and "results" not in figure_registry
    checks["legacy_not_data"] = figure_registry.get("legacy_policy") == "LEGACY_RENDERED_REFERENCE_NOT_DATA"

    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    seed_config = PROJECT_ROOT / "reproducibility" / "random" / "seeds.json"
    with tempfile.TemporaryDirectory(prefix="p2_14_04_policy_") as temp_name:
        package = Path(temp_name) / "synthetic-validator-fixture"
        package.mkdir()
        data_path = package / "data.csv"
        uncertainty_path = package / "uncertainty.csv"
        data_path.write_text("x,value\n0,1.0\n1,2.0\n", encoding="utf-8")
        uncertainty_path.write_text("x,sigma\n0,0.1\n1,0.2\n", encoding="utf-8")
        manifest = {
            "schema_version": 1,
            "dataset_id": "synthetic-validator-fixture",
            "status": "COMPLETE",
            "created_by_task": "P2-14-04-SELF-TEST",
            "result_ids": ["R1"],
            "observable": {"name": "synthetic value", "definition": "Validator fixture only", "units": "dimensionless"},
            "theory_sources": [{"file": "SELF_TEST", "section_or_equation": "NOT_SCIENTIFIC_DATA"}],
            "parameter_registry_sha256": "0" * 64,
            "geometry": {"status": "NOT_APPLICABLE"},
            "representation": {"status": "NOT_APPLICABLE"},
            "finite_cover": {"status": "NOT_APPLICABLE"},
            "algorithm": {"name": "fixture writer", "implementation": "verify_raw_data_policy.py", "settings": {}},
            "environment": {"lock_file": "reproducibility/environment/environment-lock.json", "lock_sha256": _sha256(environment_lock)},
            "stochastic": {"status": "USED", "reason": "Exercise seed provenance fields", "seed_config_sha256": _sha256(seed_config), "streams": [{"namespace": "numpy.general", "first_index": 0, "count": 1}]},
            "files": [
                {"relative_path": "data.csv", "role": "raw", "media_type": "text/csv", "bytes": data_path.stat().st_size, "sha256": sha256_file(data_path)},
                {"relative_path": "uncertainty.csv", "role": "uncertainty", "media_type": "text/csv", "bytes": uncertainty_path.stat().st_size, "sha256": sha256_file(uncertainty_path)}
            ],
            "uncertainty": {"status": "AVAILABLE", "method": "synthetic fixture values", "files": ["uncertainty.csv"], "justification": "Exercises required uncertainty-file validation."},
            "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": ["SELF_TEST_ONLY"]}
        }
        (package / "dataset.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        valid_report = validate_dataset_package(package)
        checks["valid_fixture_passes"] = valid_report["status"] == "PASS"
        data_path.write_text("x,value\n0,999.0\n", encoding="utf-8")
        tampered_report = validate_dataset_package(package)
        checks["tampered_file_fails"] = tampered_report["status"] == "FAIL" and any(
            "mismatch" in message for message in tampered_report["errors"]
        )

    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "status": "PASS" if not failed else "FAIL",
        "policy_scope": "schema-v2 closed manuscript/figure mapping, live registered-file hashes, and dataset tamper rejection",
        "checks": checks,
        "failed_checks": failed,
        "figure_registry_status": figure_registry.get("registry_status"),
        "figure_count": len(figures),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    report = verify()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
