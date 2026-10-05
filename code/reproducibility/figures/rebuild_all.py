"""Rebuild and audit every figure currently loaded by the manuscript.

Run from any directory with ``python reproducibility/figures/rebuild_all.py``.
Eight registered generators remain the sole producers of plotted values; this
driver invokes them and verifies the complete manuscript/provenance closed set.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
FIG_ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "source_current_195/main.tex"
AUDIT_PATH = FIG_ROOT / "P0-05-COMMON_audit.json"
CENTRAL_MANIFEST = ROOT / "reproducibility/data/figure_data_manifest.json"

RUN_ID = "P0-05-COMMON-reexec-20260903T112800+0800"

JOBS = (
    ("P0-05-R1", "p0_05_r1", "make_r1.py", "P0-05-R1_platform_hamiltonian"),
    ("P0-05-R2", "p0_05_r2", "make_r2.py", "P0-05-R2_euclidean_commensurate_benchmark"),
    ("P0-05-R4", "p0_05_r4", "make_r4.py", "P0-05-R4_diffraction_fourier_reconstruction"),
    ("P0-05-R5", "p0_05_r5", "make_r5.py", "P0-05-R5_magic_no_magic_dichotomy"),
    ("P0-05-R7", "p0_05_r7", "make_r7.py", "P0-05-R7_hodge_mechanism"),
    ("P0-05-R9", "p0_05_r9", "make_r9.py", "P0-05-R9_finite_cover_convergence"),
    ("P0-05-R12", "p0_05_r12", "make_r12.py", "P0-05-R12_ldos_projector_tomography"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def manuscript_figure_paths() -> set[str]:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    refs = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    selected = set()
    for ref in refs:
        normalized = (MANUSCRIPT.parent / ref).resolve()
        try:
            relative = normalized.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise RuntimeError(f"figure outside repository: {ref}") from exc
        selected.add(relative)
    return selected


def verify_job(task_id: str, folder: str, script_name: str, stem: str) -> dict:
    directory = FIG_ROOT / folder
    required = {
        "script": directory / script_name,
        "csv": directory / f"{task_id}_source_data.csv",
        "config": directory / f"{task_id}_plot_config.json",
        "record": directory / f"{task_id}_run_record.json",
        "pdf": directory / f"{stem}.pdf",
        "svg": directory / f"{stem}.svg",
        "png": directory / f"{stem}.png",
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    if missing:
        raise RuntimeError(f"{task_id}: missing required files {missing}")

    record = json.loads(required["record"].read_text(encoding="utf-8"))
    if record.get("task_id") != task_id or not record.get("run_id"):
        raise RuntimeError(f"{task_id}: invalid task/run identity")
    if not record.get("negative_control"):
        raise RuntimeError(f"{task_id}: missing preregistered negative control")
    if not record.get("terminal_scientific_status"):
        raise RuntimeError(f"{task_id}: missing terminal scientific status")

    hash_checks = []
    for item in record.get("files", []):
        path = ROOT / item["path"]
        actual = sha256(path)
        passed = path.stat().st_size == item["bytes"] and actual == item["sha256"]
        hash_checks.append({"path": item["path"], "pass": passed})
    if not hash_checks or not all(item["pass"] for item in hash_checks):
        raise RuntimeError(f"{task_id}: at least one run-record hash is stale")

    with Image.open(required["png"]) as image:
        dpi = image.info.get("dpi", (0.0, 0.0))
        if min(dpi) < 599.0:
            raise RuntimeError(f"{task_id}: PNG is not 600 dpi (reported {dpi})")

    return {
        "task_id": task_id,
        "run_id": record["run_id"],
        "terminal_scientific_status": record["terminal_scientific_status"],
        "negative_control": record["negative_control"],
        "hashes_verified": len(hash_checks),
        "png_dpi": [round(float(dpi[0]), 3), round(float(dpi[1]), 3)],
        "figure_pdf": required["pdf"].relative_to(ROOT).as_posix(),
    }


def verify_q5() -> dict:
    directory = FIG_ROOT / "p1_09_q5"
    script = ROOT / "theory_tasks" / "generate_P1-09-Q5_w0_figure.py"
    record_path = directory / "manifest.json"
    required = {
        "script": script,
        "record": record_path,
        "pdf": directory / "P1-09-Q5_w0_folded_band_controls.pdf",
        "png": directory / "P1-09-Q5_w0_folded_band_controls.png",
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    if missing:
        raise RuntimeError(f"P1-09-Q5: missing required files {missing}")

    record = json.loads(record_path.read_text(encoding="utf-8"))
    source = ROOT / record["source"]
    checks = {
        "source": source.is_file() and sha256(source) == record["source_sha256"],
        "script": sha256(script) == record["generator"]["sha256"],
        "pdf": sha256(required["pdf"]) == record["pdf"]["sha256"],
        "png": sha256(required["png"]) == record["png"]["sha256"],
    }
    if not all(checks.values()):
        raise RuntimeError(f"P1-09-Q5: stale provenance hash {checks}")
    if record.get("status") != "EXACT_W0_FOLDING_CONTROL_ONLY":
        raise RuntimeError("P1-09-Q5: incorrect scientific scope")

    with Image.open(required["png"]) as image:
        dpi = image.info.get("dpi", (0.0, 0.0))
        if min(dpi) < 599.0:
            raise RuntimeError(f"P1-09-Q5: PNG is not 600 dpi (reported {dpi})")

    return {
        "task_id": "P1-09-Q5",
        "run_id": record["run_id"],
        "terminal_scientific_status": record["status"],
        "negative_control": record["negative_control"],
        "hashes_verified": len(checks),
        "png_dpi": [round(float(dpi[0]), 3), round(float(dpi[1]), 3)],
        "figure_pdf": required["pdf"].relative_to(ROOT).as_posix(),
    }


def refresh_central_manifest(records: list[dict], expected: set[str]) -> int:
    """Refresh and validate the manuscript-order figure/data hash registry."""
    registry = json.loads(CENTRAL_MANIFEST.read_text(encoding="utf-8"))
    figures = registry.get("figures", [])
    mapped = {item.get("figure_pdf") for item in figures}
    if mapped != expected or len(figures) != len(expected):
        raise RuntimeError(
            "central figure manifest mismatch: "
            f"unregistered={sorted(expected - mapped)}, unloaded={sorted(mapped - expected)}"
        )
    records_by_task = {item["task_id"]: item for item in records}
    hash_pairs = (
        ("figure_pdf", "figure_pdf_sha256"),
        ("source_data", "source_data_sha256"),
        ("generator", "generator_sha256"),
        ("plot_config", "plot_config_sha256"),
    )
    refreshed = 0
    for item in figures:
        task_id = item.get("task_id")
        if task_id not in records_by_task:
            raise RuntimeError(f"central manifest has unknown task: {task_id}")
        item["run_id"] = records_by_task[task_id]["run_id"]
        for path_key, hash_key in hash_pairs:
            path = ROOT / item[path_key]
            if not path.is_file():
                raise RuntimeError(f"central manifest path missing: {path}")
            item[hash_key] = sha256(path)
            refreshed += 1
    registry["last_verified_run_id"] = RUN_ID
    registry["last_verified_hash_count"] = refreshed
    CENTRAL_MANIFEST.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    return refreshed

def main() -> None:
    for task_id, folder, script_name, _ in JOBS:
        script = FIG_ROOT / folder / script_name
        print(f"rebuilding {task_id}: {script.relative_to(ROOT)}", flush=True)
        subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)

    q5_script = ROOT / "theory_tasks" / "generate_P1-09-Q5_w0_figure.py"
    print(f"rebuilding P1-09-Q5: {q5_script.relative_to(ROOT)}", flush=True)
    subprocess.run([sys.executable, str(q5_script)], cwd=ROOT, check=True)

    records = [verify_job(*job) for job in JOBS]
    records.append(verify_q5())
    expected = {item["figure_pdf"] for item in records}
    loaded = manuscript_figure_paths()
    if loaded != expected:
        raise RuntimeError(
            "manuscript/manifest mismatch: "
            f"unregistered={sorted(loaded - expected)}, unloaded={sorted(expected - loaded)}"
        )

    central_hashes = refresh_central_manifest(records, expected)

    audit = {
        "task_id": "P0-05-COMMON",
        "run_id": RUN_ID,
        "terminal_scientific_status": "DONE_ALL_CURRENT_MAIN_FIGURES_REBUILT_AND_HASH_VERIFIED",
        "command": f"{Path(sys.executable).name} reproducibility/figures/rebuild_all.py",
        "manuscript": MANUSCRIPT.relative_to(ROOT).as_posix(),
        "main_figure_count": len(loaded),
        "all_manuscript_figures_registered": True,
        "manual_data_entry": False,
        "central_manifest_hashes_refreshed": central_hashes,

        "records": records,
    }
    AUDIT_PATH.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"PASS: rebuilt and verified {len(records)} manuscript figures")
    print(AUDIT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()

