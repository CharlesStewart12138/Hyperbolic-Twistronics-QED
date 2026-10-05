"""Portable command-line entry point for the 5203 hyperbolic-bilayer source release."""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tokenize


ROOT = Path(__file__).resolve().parent
CODE = ROOT / "code"
PYTHON = sys.executable
REQUIRED_MODULES = (
    "numpy", "scipy", "h5py", "sympy", "matplotlib", "yaml",
    "openpyxl", "psutil", "PIL", "pypdf", "mpmath", "pytest",
)
REQUIRED_TOOLS = ("g++", "gap", "latexmk")


def environment() -> dict[str, str]:
    env = os.environ.copy()
    prior = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(CODE) + (os.pathsep + prior if prior else "")
    return env


def doctor() -> int:
    modules: dict[str, str] = {}
    for name in REQUIRED_MODULES:
        try:
            module = importlib.import_module(name)
            modules[name] = str(getattr(module, "__version__", "available"))
        except Exception as exc:
            modules[name] = f"MISSING_OR_BROKEN: {type(exc).__name__}: {exc}"
    tools = {name: shutil.which(name) for name in REQUIRED_TOOLS}
    payload = {
        "python": sys.version,
        "repository": str(ROOT),
        "code_root": str(CODE),
        "modules": modules,
        "tools": tools,
        "r4": (CODE / "CONSTRUCTIVE_EXECUTION_R4").is_dir(),
        "r5": (CODE / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT").is_dir(),
        "r6": (CODE / "r6_physics").is_dir(),
        "r7": (CODE / "r7_theory").is_dir(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if all(not value.startswith("MISSING_OR_BROKEN") for value in modules.values()) else 1


def audit() -> int:
    files = sorted(CODE.rglob("*.py")) + sorted((ROOT / "tools").rglob("*.py")) + [Path(__file__)]
    failures: list[dict[str, object]] = []
    for path in files:
        try:
            with tokenize.open(path) as handle:
                ast.parse(handle.read(), filename=str(path))
        except (OSError, SyntaxError, UnicodeError) as exc:
            failures.append({
                "path": str(path.relative_to(ROOT)),
                "type": type(exc).__name__,
                "line": getattr(exc, "lineno", None),
                "message": str(exc),
            })
    print(json.dumps({"files": len(files), "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


def run_tests(suite: str, extra: list[str]) -> int:
    targets = {
        "validation": CODE / "validation_code/tests",
        "production": CODE / "production_code/tests",
        "r6": CODE / "r6_physics/tests",
        "r7": CODE / "r7_theory/tests",
    }
    return subprocess.call([PYTHON, "-m", "pytest", str(targets[suite]), *extra], cwd=ROOT, env=environment())


def build_figures(figure: str | None) -> int:
    script = CODE / "FINAL_NUMERICAL_FIGURES/08_SCRIPTS/build_suite.py"
    command = [PYTHON, str(script)]
    if figure:
        command.extend(["--figure", figure])
    return subprocess.call(command, cwd=CODE, env=environment())


def run_r6_demo() -> int:
    script = CODE / "r6_physics/demo_reduced.py"
    return subprocess.call([PYTHON, str(script)], cwd=ROOT, env=environment())


def run_r7_certificate(output: str | None) -> int:
    script = CODE / "r7_theory/verify_magic_margin.py"
    command = [PYTHON, str(script)]
    if output:
        command.extend(["--output", output])
    return subprocess.call(command, cwd=ROOT, env=environment())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="check Python packages and external executables")
    subparsers.add_parser("audit", help="parse every packaged Python source file")
    tests = subparsers.add_parser("test", help="run a current test family")
    tests.add_argument("suite", choices=("validation", "production", "r6", "r7"))
    tests.add_argument("pytest_args", nargs=argparse.REMAINDER)
    figures = subparsers.add_parser("figures", help="build current numerical figures after data generation")
    figures.add_argument("--figure")
    subparsers.add_parser("r6-demo", help="run a source-only reduced R6 operator demonstration")
    r7 = subparsers.add_parser("r7-certificate", help="replay the exact R7 magic-margin certificate")
    r7.add_argument("--output")
    args = parser.parse_args()
    if args.command == "doctor":
        return doctor()
    if args.command == "audit":
        return audit()
    if args.command == "test":
        return run_tests(args.suite, args.pytest_args)
    if args.command == "figures":
        return build_figures(args.figure)
    if args.command == "r6-demo":
        return run_r6_demo()
    return run_r7_certificate(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
