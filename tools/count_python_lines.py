"""Count Python files and physical lines by release partition."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import tokenize


ROOT = Path(__file__).resolve().parents[1]


def read_source(path: Path) -> str:
    try:
        with tokenize.open(path) as handle:
            return handle.read()
    except (SyntaxError, UnicodeError):
        return path.read_text(encoding="utf-8", errors="replace")


def metrics(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    text = read_source(path)
    lines = text.splitlines()
    blank = sum(not line.strip() for line in lines)
    comment_only = sum(line.lstrip().startswith("#") for line in lines)
    return {
        "sha256": sha256(raw).hexdigest(),
        "physical_lines": len(lines),
        "blank_lines": blank,
        "comment_only_lines": comment_only,
        "nonblank_noncomment_lines": len(lines) - blank - comment_only,
    }


def summarize(paths: list[Path]) -> dict[str, int]:
    values = [metrics(path) for path in paths]
    return {
        "files": len(paths),
        "physical_lines": sum(int(value["physical_lines"]) for value in values),
        "blank_lines": sum(int(value["blank_lines"]) for value in values),
        "comment_only_lines": sum(int(value["comment_only_lines"]) for value in values),
        "nonblank_noncomment_lines": sum(int(value["nonblank_noncomment_lines"]) for value in values),
    }


def main() -> None:
    partitions = {
        "code": sorted((ROOT / "code").rglob("*.py")),
        "release_tools": sorted((ROOT / "tools").glob("*.py")) + [ROOT / "reproduce.py"],
    }
    all_paths = [path for paths in partitions.values() for path in paths]
    unique_by_hash: dict[str, Path] = {}
    for path in all_paths:
        unique_by_hash.setdefault(str(metrics(path)["sha256"]), path)
    payload = {
        "definition": "physical lines; comment_only means first non-whitespace character is #",
        "partitions": {name: summarize(paths) for name, paths in partitions.items()},
        "all_packaged_python": summarize(all_paths),
        "unique_file_content": summarize(sorted(unique_by_hash.values())),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
