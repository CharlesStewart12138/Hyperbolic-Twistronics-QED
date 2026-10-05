"""Parse every Python source file below a directory without creating bytecode."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import tokenize


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    files = sorted(args.root.resolve().rglob("*.py"))
    failures: list[dict[str, object]] = []
    for path in files:
        try:
            with tokenize.open(path) as handle:
                ast.parse(handle.read(), filename=str(path))
        except (OSError, SyntaxError, UnicodeError) as exc:
            failures.append(
                {
                    "path": str(path),
                    "type": type(exc).__name__,
                    "line": getattr(exc, "lineno", None),
                    "message": str(exc),
                }
            )

    print(
        json.dumps(
            {"root": str(args.root.resolve()), "files": len(files), "failures": failures},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
