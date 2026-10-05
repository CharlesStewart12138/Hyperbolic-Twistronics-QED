"""Audit the source-only release without generating per-file manifests."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "RELEASE_AUDIT.json"
EXCLUDED_PARTS = {".git", ".venv", ".pytest_cache", "__pycache__", "outputs", "htmlcov"}
FORBIDDEN_SUFFIXES = {
    ".bin", ".npz", ".npy", ".csv", ".jsonl", ".gz", ".pdf",
    ".png", ".jpg", ".jpeg", ".svg", ".xlsx", ".xls", ".parquet",
    ".h5", ".hdf5", ".mp4", ".avi", ".mov", ".exe", ".dll",
}
NODE_SUFFIXES = {".js", ".mjs", ".cjs", ".ts", ".tsx"}
NODE_FILENAMES = {"package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"}
REMOVED_MANIFESTS = {"ENTRYPOINTS.tsv", "SOURCE_MANIFEST.tsv", "PACKAGE_MANIFEST.tsv"}
NATIVE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".cu"}


def included(path: Path) -> bool:
    return (
        path.is_file()
        and path != REPORT
        and not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def main() -> int:
    files = sorted(path for path in ROOT.rglob("*") if included(path))
    forbidden = [path.relative_to(ROOT).as_posix() for path in files if path.suffix.lower() in FORBIDDEN_SUFFIXES]
    node_files = [
        path.relative_to(ROOT).as_posix()
        for path in files
        if path.suffix.lower() in NODE_SUFFIXES or path.name.lower() in NODE_FILENAMES
    ]
    removed_manifest_residue = [
        path.relative_to(ROOT).as_posix() for path in files if path.name in REMOVED_MANIFESTS
    ]
    suffixes: Counter[str] = Counter(path.suffix.lower() or "[none]" for path in files)
    sections: Counter[str] = Counter(
        path.relative_to(ROOT).parts[0] if len(path.relative_to(ROOT).parts) > 1 else "release_root"
        for path in files
    )
    total_bytes = sum(path.stat().st_size for path in files)
    exact_root = ROOT / "code" / "exact_replay"
    exact_files = [path for path in exact_root.rglob("*") if path.is_file()] if exact_root.is_dir() else []
    source_counts = {
        "python": sum(path.suffix.lower() == ".py" for path in files),
        "gap": sum(path.suffix.lower() in {".g", ".gap"} for path in files),
        "shell_sh": sum(path.suffix.lower() == ".sh" for path in files),
        "powershell": sum(path.suffix.lower() == ".ps1" for path in files),
        "native_c_cpp_headers": sum(path.suffix.lower() in NATIVE_SUFFIXES for path in files),
        "exact_replay_files": len(exact_files),
    }
    passed = not forbidden and not node_files and not removed_manifest_residue
    report = {
        "status": "pass" if passed else "fail",
        "file_count": len(files),
        "total_bytes": total_bytes,
        "sections": dict(sorted(sections.items())),
        "extensions": dict(sorted(suffixes.items())),
        "source_counts": source_counts,
        "forbidden_result_or_binary_files": forbidden,
        "node_source_or_lockfiles": node_files,
        "removed_manifest_residue": removed_manifest_residue,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
