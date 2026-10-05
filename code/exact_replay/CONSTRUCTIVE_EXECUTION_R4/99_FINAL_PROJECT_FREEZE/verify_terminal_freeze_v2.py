"""V2 build wrapper: exclude the current audit shell from project-job counts."""

from __future__ import annotations

import os
import runpy
from pathlib import Path

import psutil


BASE = Path(__file__).resolve().with_name("verify_terminal_freeze.py")
namespace = runpy.run_path(str(BASE), run_name="terminal_freeze_library")


def process_snapshot_v2() -> dict[str, int]:
    project = legacy = gap = 0
    for proc in psutil.process_iter(("pid", "name", "cmdline")):
        if proc.info["pid"] == os.getpid():
            continue
        name = (proc.info.get("name") or "").lower()
        command = " ".join(proc.info.get("cmdline") or []).lower()
        is_gap = name in {"gap.exe", "gap", "gapw95.exe"} or " gap.exe" in command
        is_legacy = "scan_candidate_0005" in command or "degree-24" in command or "degree24" in command
        is_project_job = (
            is_gap
            or is_legacy
            or (
                name.startswith("python")
                and "constructive_execution_r4" in command
                and "verify_terminal_freeze" not in command
            )
            or name.startswith("geometric_ball_")
            or name.startswith("scan_candidate_")
        )
        gap += int(is_gap)
        legacy += int(is_legacy)
        project += int(is_project_job)
    return {
        "running_project_processes": project,
        "running_legacy_enumeration_processes": legacy,
        "running_abandoned_GAP_processes": gap,
    }


namespace["process_snapshot"] = process_snapshot_v2
namespace["build"]()
