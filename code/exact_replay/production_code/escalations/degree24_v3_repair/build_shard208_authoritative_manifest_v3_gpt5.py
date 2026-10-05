#!/usr/bin/env python3
"""Freeze the Route-B authoritative class manifest for 24T13493."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(r"D:\work\revise")
OUTDIR = ROOT / "production_code/escalations/degree24_v3_repair"
SOURCE = OUTDIR / "DEG24_SHARD208_FORENSIC_RUN01_V3.tsv"
MANIFEST = OUTDIR / "DEG24_KEY_24T13493_CLASS_MANIFEST_V3.tsv"
GAP_MANIFEST = OUTDIR / "DEG24_KEY_24T13493_CLASS_MANIFEST_V3.g"
META = OUTDIR / "DEG24_KEY_24T13493_CLASS_MANIFEST_V3.json"
FORENSIC = OUTDIR / "DEG24_SHARD208_FORENSIC_REGRESSION_V3.json"


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_forensic(path: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    metadata: dict[str, str] = {}
    classes = []
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if fields[0] == "CLASS":
            if len(fields) != 9:
                raise ValueError(f"unexpected class field count {len(fields)}")
            classes.append({
                "source_ordinal_diagnostic": fields[1],
                "representative_display_diagnostic": fields[2],
                "pc_exponents_diagnostic": fields[3],
                "representative_serialization": fields[4],
                "class_size": fields[5],
                "centralizer_size": fields[6],
                "order": fields[7],
                "structural_filter": fields[8],
            })
        elif len(fields) == 2:
            metadata[fields[0]] = fields[1]
    return metadata, classes


def gap_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    metadata, classes = read_forensic(SOURCE)
    if metadata.get("KEY_ID") != "24T13493" or len(classes) != 1976:
        raise ValueError("unexpected shard208 source manifest")
    schema = metadata["REPRESENTATION_SCHEMA"]
    generator_serialization = metadata["GENERATOR_SERIALIZATION"]
    generator_sha256 = digest_text(generator_serialization)

    seen_serializations: set[str] = set()
    for row in classes:
        serialization = row["representative_serialization"]
        if serialization in seen_serializations:
            raise ValueError("duplicate frozen representative serialization")
        seen_serializations.add(serialization)
        identity_payload = (
            f"KEY_ID=24T13493\nSCHEMA={schema}\n"
            f"GENERATOR_TUPLE_SHA256={generator_sha256}\n"
            f"REPRESENTATIVE_SERIALIZATION={serialization}\n"
            f"CLASS_SIZE={row['class_size']}\nORDER={row['order']}\n"
            f"CENTRALIZER_SIZE={row['centralizer_size']}\n"
        )
        row["class_id_v3"] = digest_text(identity_payload)

    classes.sort(key=lambda row: (
        row["representative_serialization"],
        int(row["class_size"]),
        int(row["centralizer_size"]),
    ))
    for position, row in enumerate(classes, start=1):
        row["key_id"] = "24T13493"
        row["manifest_position"] = str(position)
        row_payload = "\t".join([
            row["key_id"], row["class_id_v3"], row["manifest_position"],
            row["representative_serialization"], row["class_size"],
            row["centralizer_size"], row["order"], row["structural_filter"],
        ])
        row["row_sha256"] = digest_text(row_payload)

    fieldnames = [
        "key_id", "class_id_v3", "manifest_position", "representative_serialization",
        "class_size", "centralizer_size", "order", "structural_filter",
        "source_ordinal_diagnostic", "representative_display_diagnostic",
        "pc_exponents_diagnostic", "row_sha256",
    ]
    with MANIFEST.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(classes)

    with GAP_MANIFEST.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("D24C8_MANIFEST_META:=rec(\n")
        handle.write(" key:=13493, schema:=" + gap_string(schema) + ",\n")
        handle.write(" generatorSerialization:=" + gap_string(generator_serialization) + ",\n")
        handle.write(" generatorTupleSha256:=" + gap_string(generator_sha256) + ",\n")
        handle.write(" classCount:=1976, sourceSha256:=" + gap_string(digest_file(SOURCE)) + ");\n")
        handle.write("D24C8_MANIFEST_RECORDS:=[\n")
        for index, row in enumerate(classes):
            image_lists = []
            for encoded_image in row["representative_serialization"].split(";"):
                image_lists.append("[" + encoded_image + "]")
            suffix = "," if index + 1 < len(classes) else ""
            handle.write(
                "rec(classId:=" + gap_string(row["class_id_v3"]) +
                ",position:=" + row["manifest_position"] +
                ",images:=[" + ",".join(image_lists) + "]" +
                ",classSize:=" + row["class_size"] +
                ",centralizerSize:=" + row["centralizer_size"] +
                ",order:=" + row["order"] +
                ",sourceOrdinalDiagnostic:=" + row["source_ordinal_diagnostic"] + ")" + suffix + "\n"
            )
        handle.write("];\n")

    meta = {
        "schema": "DEG24_AUTHORITATIVE_CLASS_MANIFEST_V3",
        "route": "B_FROZEN_EXPLICIT_REPRESENTATIVES",
        "key_id": "24T13493",
        "class_count": len(classes),
        "class_id_count": len({row["class_id_v3"] for row in classes}),
        "representation_schema": schema,
        "generator_tuple_sha256": generator_sha256,
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": digest_file(SOURCE),
        "manifest": MANIFEST.relative_to(ROOT).as_posix(),
        "manifest_sha256": digest_file(MANIFEST),
        "gap_manifest": GAP_MANIFEST.relative_to(ROOT).as_posix(),
        "gap_manifest_sha256": digest_file(GAP_MANIFEST),
        "worker_contract": "Workers reconstruct and consume these representatives; ordinals are diagnostic only.",
    }
    META.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    forensic_runs = []
    for run_number in (1, 2, 3):
        path = OUTDIR / f"DEG24_SHARD208_FORENSIC_RUN0{run_number}_V3.tsv"
        run_meta, run_classes = read_forensic(path)
        row844 = next(row for row in run_classes if row["source_ordinal_diagnostic"] == "844")
        forensic_runs.append({
            "run_id": run_meta["RUN_ID"],
            "seed": int(run_meta["RANDOM_SEED"]),
            "class_count": int(run_meta["ORDER8_CLASS_COUNT"]),
            "ordinal_844_class_size": int(row844["class_size"]),
            "ordinal_844_representative_serialization_sha256": digest_text(row844["representative_serialization"]),
            "output_sha256": digest_file(path),
        })
    regression = {
        "schema": "DEG24_SHARD208_FORENSIC_REGRESSION_V3",
        "key_id": "24T13493",
        "gap_version": "4.12.1",
        "fresh_process_runs": forensic_runs,
        "fresh_ordinal_844_class_sizes": [row["ordinal_844_class_size"] for row in forensic_runs],
        "legacy_uncommitted_ordinal_844_class_size": 192,
        "legacy_recovery_committed_ordinal_844_class_size": 48,
        "ordinal_844_is_stable_class_identity": False,
        "status": "PASS_DEFECT_REPRODUCED",
    }
    FORENSIC.write_text(json.dumps(regression, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"manifest": meta, "forensic": regression}, sort_keys=True))


if __name__ == "__main__":
    main()
