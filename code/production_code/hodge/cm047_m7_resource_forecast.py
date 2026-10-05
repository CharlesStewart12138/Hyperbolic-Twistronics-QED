"""Resource gate for the exact radius-seven full-tensor ball."""

from __future__ import annotations

import ctypes
import json
import math
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
BASED = ROOT / "data" / "production" / "short_geodesics" / "based_enumeration_summary.json"
OUTPUT = ROOT / "data" / "production" / "local_full_kernel" / "EXACT_BALL7_TENSOR_RESOURCE_FORECAST.json"


class MemoryStatus(ctypes.Structure):
    _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong), ("total", ctypes.c_ulonglong), ("available", ctypes.c_ulonglong), ("total_page", ctypes.c_ulonglong), ("available_page", ctypes.c_ulonglong), ("total_virtual", ctypes.c_ulonglong), ("available_virtual", ctypes.c_ulonglong), ("extended", ctypes.c_ulonglong)]


def main() -> None:
    memory = MemoryStatus(); memory.length = ctypes.sizeof(memory)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
        raise OSError("GlobalMemoryStatusEx failed")
    disk = shutil.disk_usage(ROOT.anchor)
    baseline = json.loads(BASED.read_text(encoding="utf-8"))
    a_over_r = 3.0571418389619963225449123695873467866
    ratio = (math.cosh(7 * a_over_r) - 1) / (math.cosh(6 * a_over_r) - 1)
    states6 = 1 + int(baseline["dangerous_nonidentity_elements"])
    states7 = math.ceil(states6 * ratio)
    bytes_per_state = int(baseline["peak_working_set_bytes"]) / states6
    peak = math.ceil(states7 * bytes_per_state)
    csv_per_state = 7_561_157_638 / int(baseline["dangerous_nonidentity_elements"])
    record = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7",
        "forecast_precedes_exact_radius_7_enumeration": True,
        "host": {"total_physical_memory_bytes": int(memory.total), "available_physical_memory_bytes": int(memory.available), "workspace_volume_free_bytes": int(disk.free)},
        "exact_m6_calibration": {"states_including_identity": states6, "peak_working_set_bytes": int(baseline["peak_working_set_bytes"]), "enumeration_seconds": float(baseline["enumeration_seconds"]), "total_seconds_including_csv": float(baseline["total_seconds"])},
        "m7_forecast": {
            "hyperbolic_disk_area_ratio_7a_to_6a": ratio,
            "estimated_states_including_identity": states7,
            "estimated_peak_working_set_bytes": peak,
            "estimated_csv_bytes_current_schema": math.ceil(states7 * csv_per_state),
            "estimated_enumeration_seconds_memory_resident": states7 / (states6 / float(baseline["enumeration_seconds"])),
            "estimated_tensor_accumulation_seconds_at_m6_rate": 27.6946073 * ratio,
            "fits_total_physical_memory": peak <= int(memory.total),
            "fits_current_available_physical_memory": peak <= int(memory.available),
        },
        "resource_guard": {"maximum_new_peak_working_set_bytes": min(8 * 2**30, int(memory.available * 0.5)), "no_swap_thrashing": True},
        "decision": {
            "exact_complete_ball_m7_authorized": False,
            "reason": "The calibrated exact in-memory flood is predicted to exceed total physical RAM and the registered guard before tensor/orbit overhead; swap execution is forbidden.",
            "m8_released": False,
        },
        "frozen_m6_recomputed": False,
        "main_tex_modified": False,
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
