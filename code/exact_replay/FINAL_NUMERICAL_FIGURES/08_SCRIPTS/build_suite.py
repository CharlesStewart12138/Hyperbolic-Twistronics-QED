from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from figures_geometry_magic import REGISTRY as GEOMETRY_MAGIC
from figures_cert_group import REGISTRY as CERT_GROUP
from figures_operator_spectral import REGISTRY as OPERATOR_SPECTRAL
from suite_core import FIGURE_IDS, OUT, SCRIPT_DIR, WORKING, configure_matplotlib, ensure_dirs, finalize_manifest


REGISTRY = {}
REGISTRY.update(GEOMETRY_MAGIC)
REGISTRY.update(CERT_GROUP)
REGISTRY.update(OPERATOR_SPECTRAL)


def generate_wrappers() -> None:
    for fig_id in FIGURE_IDS:
        path = SCRIPT_DIR / f"plot_{fig_id.lower()}.py"
        path.write_text(
            "from build_suite import build_one\n\n"
            f"if __name__ == '__main__':\n    build_one('{fig_id}')\n",
            encoding="utf-8",
        )


def build_one(fig_id: str):
    ensure_dirs()
    configure_matplotlib()
    if fig_id not in REGISTRY:
        raise KeyError(f"Unknown or intentionally omitted figure ID: {fig_id}")
    entry = REGISTRY[fig_id]()
    print(json.dumps({"built": fig_id, "title": entry["Title"]}, ensure_ascii=False))
    return entry


def build_all() -> list[dict[str, str]]:
    ensure_dirs()
    font_path = configure_matplotlib()
    generate_wrappers()
    missing = [fig_id for fig_id in FIGURE_IDS if fig_id not in REGISTRY]
    if missing:
        raise RuntimeError(f"Missing figure builders: {missing}")
    entries = []
    for fig_id in FIGURE_IDS:
        print(f"BUILDING {fig_id}", flush=True)
        entries.append(REGISTRY[fig_id]())
    finalize_manifest(entries, font_path)
    headers = list(entries[0].keys())
    with (WORKING / "NUMERICAL_FIGURE_CATALOG_SOURCE.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(entries)
    print(json.dumps({"built_count": len(entries), "figure_ids": [e["Figure ID"] for e in entries]}, ensure_ascii=False))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", choices=FIGURE_IDS)
    args = parser.parse_args()
    if args.figure:
        build_one(args.figure)
    else:
        build_all()


if __name__ == "__main__":
    main()
