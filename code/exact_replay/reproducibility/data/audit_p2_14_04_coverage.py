"""Audit whether every R1-R15 figure result has complete structured raw data."""

from __future__ import annotations

import json
from pathlib import Path

from validate_dataset import validate_dataset_package


DATA_ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = DATA_ROOT / "figure_data_manifest.json"
OUTPUT_PATH = DATA_ROOT / "p2_14_04_figure_data_coverage_audit.json"
RESULT_IDS = [f"R{index}" for index in range(1, 16)]


def main() -> int:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry_rows = {str(row["result_id"]): row for row in registry["results"]}
    packages: list[dict[str, object]] = []
    coverage = {result_id: [] for result_id in RESULT_IDS}

    for manifest_path in sorted(DATA_ROOT.glob("*/dataset.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validation = validate_dataset_package(manifest_path.parent)
        plotting = manifest.get("plotting", {})
        uncertainty = manifest.get("uncertainty", {})
        record = {
            "package": manifest_path.parent.name,
            "dataset_id": manifest.get("dataset_id"),
            "created_by_task": manifest.get("created_by_task"),
            "status": manifest.get("status"),
            "result_ids": manifest.get("result_ids", []),
            "schema_and_hash_validation": validation["status"],
            "validation_errors": validation["errors"],
            "uncertainty_status": uncertainty.get("status"),
            "plot_scripts": plotting.get("plot_scripts", []),
        }
        record["figure_ready"] = bool(
            record["status"] == "COMPLETE"
            and record["schema_and_hash_validation"] == "PASS"
            and record["uncertainty_status"] in {"AVAILABLE", "NOT_APPLICABLE"}
            and record["plot_scripts"]
        )
        packages.append(record)
        for result_id in record["result_ids"]:
            if result_id in coverage:
                coverage[result_id].append(record["package"])

    result_rows = []
    for result_id in RESULT_IDS:
        linked_packages = [record for record in packages if record["package"] in coverage[result_id]]
        figure_ready_packages = [record["package"] for record in linked_packages if record["figure_ready"]]
        result_rows.append({
            "result_id": result_id,
            "registry_status": registry_rows.get(result_id, {}).get("status", "MISSING"),
            "registry_dataset_manifest": registry_rows.get(result_id, {}).get("dataset_manifest"),
            "discovered_packages": coverage[result_id],
            "figure_ready_packages": figure_ready_packages,
            "figure_ready": bool(figure_ready_packages),
        })

    fully_covered = [row["result_id"] for row in result_rows if row["figure_ready"]]
    partially_covered = [
        row["result_id"] for row in result_rows if row["discovered_packages"] and not row["figure_ready"]
    ]
    uncovered = [row["result_id"] for row in result_rows if not row["discovered_packages"]]
    checks = {
        "registry_contains_exactly_R1_R15": set(registry_rows) == set(RESULT_IDS),
        "registry_status_complete": registry.get("registry_status") == "COMPLETE",
        "every_result_has_figure_ready_package": len(fully_covered) == len(RESULT_IDS),
        "every_registry_row_links_dataset": all(
            registry_rows.get(result_id, {}).get("dataset_manifest") for result_id in RESULT_IDS
        ),
    }
    summary = {
        "task_id": "P2-14-04",
        "status": "PASS" if all(checks.values()) else "BLOCKED",
        "checks": checks,
        "fully_covered_result_ids": fully_covered,
        "partially_covered_result_ids": partially_covered,
        "uncovered_result_ids": uncovered,
        "result_count": len(RESULT_IDS),
        "dataset_package_count": len(packages),
        "blocking_reason": (
            None if all(checks.values()) else
            "No R1-R15 result currently has a COMPLETE, validator-passing package with resolved "
            "uncertainty and a registered plot script; R10-R15 have no discovered dataset package."
        ),
        "required_to_unblock": [
            "Freeze the retained formal figure/result set and its mapping to R1-R15.",
            "Supply missing production geometry, Hamiltonian, target, parameter, response, and uncertainty inputs.",
            "Generate COMPLETE validator-passing dataset packages and registered plot scripts for every retained result.",
            "Update figure_data_manifest.json to point every retained result to its validated dataset manifest.",
        ],
        "packages": packages,
        "results": result_rows,
    }
    OUTPUT_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
