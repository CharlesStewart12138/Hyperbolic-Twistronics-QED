"""Certified R5 common-cover metadata; never synthesizes missing physics."""

from __future__ import annotations

from dataclasses import dataclass

from group_inputs import load_r5_certificate


@dataclass(frozen=True)
class CommonCoverRecord:
    theta: float
    index: int
    qstar_order: int
    bilayer_dimension: int
    certificate_status: str
    physical_interlayer_matrix_available: bool


def certified_theta_c_record() -> CommonCoverRecord:
    cert = load_r5_certificate()
    run = cert["r5_comm_run"]
    return CommonCoverRecord(
        theta=float(cert["construction"]["theta_c_radians"]),
        index=int(run["common_cover_index"]),
        qstar_order=46_080,
        bilayer_dimension=int(run["hilbert_dimension"]),
        certificate_status=str(cert["status"]),
        physical_interlayer_matrix_available=bool(run["physical_coefficient_matrix_materialized"]),
    )


def require_physical_common_cover_operator() -> None:
    record = certified_theta_c_record()
    if not record.physical_interlayer_matrix_available:
        raise RuntimeError(
            "R5 certifies the index-234 cover and its group action, but the frozen "
            "inputs do not materialize the theta_c physical interlayer coefficient map."
        )

