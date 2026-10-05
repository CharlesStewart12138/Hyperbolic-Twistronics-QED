"""Write the mandatory pre-search resource forecast for global direct systole."""

from __future__ import annotations

import ctypes
import importlib.util
import json
import math
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
BASED = ROOT / "data" / "production" / "short_geodesics" / "based_enumeration_summary.json"
PILOT = ROOT / "data" / "production" / "global_direct" / "pilot_cyclic_phi8.json"
OUTPUT = GROUP / "GLOBAL_DIRECT_RESOURCE_FORECAST.json"


class MemoryStatus(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_ulong),
        ("memory_load", ctypes.c_ulong),
        ("total_physical", ctypes.c_ulonglong),
        ("available_physical", ctypes.c_ulonglong),
        ("total_page_file", ctypes.c_ulonglong),
        ("available_page_file", ctypes.c_ulonglong),
        ("total_virtual", ctypes.c_ulonglong),
        ("available_virtual", ctypes.c_ulonglong),
        ("available_extended_virtual", ctypes.c_ulonglong),
    ]


def memory_status() -> MemoryStatus:
    value = MemoryStatus()
    value.length = ctypes.sizeof(value)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(value)):
        raise OSError("GlobalMemoryStatusEx failed")
    return value


def main() -> None:
    based = json.loads(BASED.read_text(encoding="utf-8"))
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    memory = memory_status()
    disk = shutil.disk_usage(ROOT.anchor)

    a_over_r = 3.0571418389619963225449123695873467866
    r_out_over_r = 2.4484524476780757900053099136358691403
    required_radius_over_a = 6.0 + 2.0 * r_out_over_r / a_over_r
    exact_count_at_6 = 1 + int(based["dangerous_nonidentity_elements"])
    disk_area_ratio = (
        (math.cosh(required_radius_over_a * a_over_r) - 1.0)
        / (math.cosh(6.0 * a_over_r) - 1.0)
    )
    estimated_states = int(math.ceil(exact_count_at_6 * disk_area_ratio))
    measured_bytes_per_state = int(based["peak_working_set_bytes"]) / exact_count_at_6
    estimated_peak_memory = int(math.ceil(estimated_states * measured_bytes_per_state))
    measured_csv_bytes_per_nonidentity = 7_561_157_638 / int(based["dangerous_nonidentity_elements"])
    estimated_csv_bytes = int(math.ceil(estimated_states * measured_csv_bytes_per_nonidentity))
    enumeration_rate = exact_count_at_6 / float(based["enumeration_seconds"])
    estimated_enumeration_seconds = estimated_states / enumeration_rate
    pilot_rate = float(pilot["canonical_orbits_per_second"])
    log10_terminal_raw = 109 * math.log10(7)
    log10_terminal_dihedral_c8 = log10_terminal_raw - math.log10(220)
    log10_pilot_seconds = log10_terminal_dihedral_c8 - math.log10(pilot_rate)

    environment = {
        "gap_executable": shutil.which("gap"),
        "sage_executable": shutil.which("sage"),
        "libgap_python_module": importlib.util.find_spec("libgap") is not None,
    }
    result = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT",
        "quotient_id": "Q_BASED_S4CORE_PAIR_001",
        "forecast_precedes_any_large_new_enumeration": True,
        "host_at_forecast": {
            "total_physical_memory_bytes": int(memory.total_physical),
            "available_physical_memory_bytes": int(memory.available_physical),
            "workspace_volume_free_bytes": int(disk.free),
            "workspace_volume_total_bytes": int(disk.total),
        },
        "mathematical_complete_domains": {
            "raw_conjugacy_representative_bound": {
                "maximum_geometric_word_length": 110,
                "half_trace_cutoff_exact": "2405+1700*sqrt(2)",
                "terminal_freely_reduced_words_lower_scale": "8*7^109",
            },
            "axis_to_base_cell_reduction": {
                "theorem": "Conjugate an axis point into the base octagon K. If ell(g)<=6a_B and x lies on the conjugated axis in K, then d(o,g o)<=2 d(o,x)+ell(g)<=2 r_out+6a_B.",
                "required_based_displacement_radius_over_a_B": required_radius_over_a,
                "required_based_displacement_radius_over_R": required_radius_over_a * a_over_r,
                "completeness_condition": "Exact Dirichlet-Voronoi flood through the stated closed radius, followed by exact quotient-identity and trace-cutoff filters.",
            },
        },
        "existing_exact_calibration": {
            "radius_over_a_B": 6.0,
            "states_including_identity": exact_count_at_6,
            "candidate_edges_processed": int(based["candidate_edges_processed"]),
            "enumeration_seconds": float(based["enumeration_seconds"]),
            "total_seconds_including_csv": float(based["total_seconds"]),
            "peak_working_set_bytes": int(based["peak_working_set_bytes"]),
            "measured_states_per_second": enumeration_rate,
            "measured_peak_bytes_per_state": measured_bytes_per_state,
        },
        "quotient_specific_pilot": {
            "artifact": str(PILOT.relative_to(ROOT)).replace("\\", "/"),
            "maximum_primitive_geometric_word_length": int(pilot["maximum_primitive_geometric_word_length"]),
            "canonical_orbits": sum(int(v) for v in pilot["canonical_orbits_by_length"].values()),
            "runtime_seconds": float(pilot["runtime_seconds"]),
            "canonical_orbits_per_second": pilot_rate,
            "dangerous_kernel_witnesses": 0 if pilot["explicit_witness"] is None else 1,
            "proof_complete_for_global_cutoff": False,
        },
        "large_search_estimates": {
            "axis_to_base_cell_flood": {
                "model": "exact radius-6 state count scaled by the hyperbolic disk-area ratio",
                "disk_area_ratio_from_6a_B": disk_area_ratio,
                "estimated_candidate_states": estimated_states,
                "estimated_peak_memory_bytes_at_measured_layout": estimated_peak_memory,
                "estimated_count_only_enumeration_seconds_if_memory_resident": estimated_enumeration_seconds,
                "estimated_csv_bytes_if_current_row_schema_is_retained": estimated_csv_bytes,
                "uint32_state_capacity_exceeded": estimated_states >= 2**32,
                "memory_fit_against_total_physical": estimated_peak_memory <= int(memory.total_physical),
                "memory_fit_against_current_available_physical": estimated_peak_memory <= int(memory.available_physical),
            },
            "raw_length_110_cyclic_C8_pilot_scaling": {
                "log10_estimated_terminal_canonical_orbits": log10_terminal_dihedral_c8,
                "log10_estimated_terminal_runtime_seconds_at_pilot_rate": log10_pilot_seconds,
                "conclusion": "INFEASIBLE",
            },
        },
        "resource_guard": {
            "maximum_new_peak_working_set_bytes": min(int(0.50 * memory.available_physical), 8 * 2**30),
            "maximum_new_output_bytes": min(int(0.10 * disk.free), 100 * 2**30),
            "no_swap_thrashing": True,
            "no_full_bilayer_or_full_nearest_neighbor_csr": True,
        },
        "alternative_method_audit_in_required_order": {
            "G2-A_automatic_group_normal_form": {"available": bool(environment["gap_executable"] or environment["sage_executable"] or environment["libgap_python_module"]), "environment": environment, "blocking_object": "No proof-complete Bolza conjugacy normal-form/symbolic-dynamics emitter is registered in the current environment."},
            "G2-B_quotient_state_automaton": {"available": False, "blocking_object": "The finite quotient state is exact, but no certified lower bound on the translation length of every unfinished automaton branch is available; quotient reachability alone cannot prune trace cancellation."},
            "G2-C_Bolza_length_trace_spectrum": {"available": False, "blocking_object": "The audited 200,000-row table has multiplicities but no representative word and no proof-complete normal-form certificate."},
            "G2-D_finite_index_coset_graph": {"available": False, "blocking_object": "The quotient has 11,943,936 states; a finite coset graph does not by itself convert combinatorial loop length into a certified hyperbolic systole, and the required exact surface-cover geodesic engine is absent."},
            "G2-E_exact_algebraic_trace_search": {"available": False, "blocking_object": "Exact Q(sqrt(2),beta,i) arithmetic exists, but a completeness-preserving trace/word automaton over the 110-side-crossing domain is absent."},
        },
        "decision": {
            "large_axis_to_base_cell_flood_authorized": False,
            "raw_length_110_enumeration_authorized": False,
            "bounded_length_9_pilot_authorized": True,
            "reason": "Both proof-complete large routes violate the resource guard; a length-9 pilot remains bounded, non-certifying, and may still supply a GLOBAL-FAIL witness.",
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
