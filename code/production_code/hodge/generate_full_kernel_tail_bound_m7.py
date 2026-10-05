"""Generate the immutable MPFR-directed m=7 tail evaluator from the m=6 source."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "production_code" / "hodge" / "full_kernel_tail_bound_mpfr.cpp"
OUTPUT = ROOT / "production_code" / "hodge" / "full_kernel_tail_bound_mpfr_m7.cpp"


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"expected one occurrence of {old!r}, found {text.count(old)}")
    return text.replace(old, new)


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    replacements = (
        ("mpfr_t one_minus_q_lo, den2_lo, den3_lo, series_hi, term_hi, c2_hi;", "mpfr_t one_minus_q_lo, den2_lo, den3_lo, series0_hi, series1_hi, series_hi, term_hi, ca_hi, c0_hi, c1_hi, c2_hi;"),
        ("one_minus_q_lo, den2_lo, den3_lo, series_hi, term_hi, c2_hi,", "one_minus_q_lo, den2_lo, den3_lo, series0_hi, series1_hi, series_hi, term_hi, ca_hi, c0_hi, c1_hi, c2_hi,"),
        ("phi_integer(6, phi6lo, phi6hi);", "phi_integer(7, phi6lo, phi6hi);"),
        ("phi_integer(7, phi7lo, phi7hi);", "phi_integer(8, phi7lo, phi7hi);"),
        ("mpfr_mul_ui(tmp, khi, 6, MPFR_RNDU);", "mpfr_mul_ui(tmp, khi, 7, MPFR_RNDU);"),
        ("// sum_{j>=0}(8+j)^2 q^j, evaluated monotonically at q_hi.", "// sum_{j>=0}(9+j)^2 q^j, evaluated monotonically at q_hi."),
        ("mpfr_ui_div(series_hi, 64, one_minus_q_lo, MPFR_RNDU);", "mpfr_ui_div(series_hi, 81, one_minus_q_lo, MPFR_RNDU);"),
        ("mpfr_mul_ui(term_hi, q_hi, 16, MPFR_RNDU);", "mpfr_mul_ui(term_hi, q_hi, 18, MPFR_RNDU);"),
        ("if (mpfr_cmp_d(c2_hi, 261.0) >= 0) fail(\"directed C2 result does not fit rational envelope 261\");", "if (mpfr_cmp_d(c2_hi, 48.0) >= 0) fail(\"directed C2 result does not fit rational envelope 48\");"),
        ("\\\"task_id\\\": \\\"CM-047-NP-TENSOR-BOUND\\\"", "\\\"task_id\\\": \\\"CM-047-NP-M7\\\""),
        ("\\\"first_omitted_shell\\\": 6", "\\\"first_omitted_shell\\\": 7"),
        ("\\\"certified_rational_coordinate_trace_upper\\\": 261", "\\\"certified_rational_coordinate_trace_upper\\\": 48"),
        ("Tr(T_tail)<=261 for T_tail=sum_{d>6a_B}|w(d)| n n^T", "Tr(T_tail)<48 for T_tail=sum_{d>7a_B}|w(d)| n n^T; conditional companion to a complete exact ball through 7a_B"),
        ("certified_integer=261", "certified_integer=48"),
        ("final decimal-independent envelope is the integer 261", "final decimal-independent envelope is the integer 48"),
    )
    repeated = "one_minus_q_lo, den2_lo, den3_lo, series_hi, term_hi, c2_hi,"
    for old, new in replacements:
        expected = 2 if old == repeated else 1
        if text.count(old) != expected:
            raise AssertionError(f"expected {expected} occurrences of {old!r}, found {text.count(old)}")
        text = text.replace(old, new)
    text = replace_once(
        text,
        "        mpfr_sqr(ca2_hi, base_hi, MPFR_RNDU);\n        mpfr_mul_ui(ca2_hi, ca2_hi, 3, MPFR_RNDU);",
        "        mpfr_sqr(ca2_hi, base_hi, MPFR_RNDU);\n        mpfr_mul_ui(ca2_hi, ca2_hi, 3, MPFR_RNDU);\n        mpfr_sqrt(ca_hi, ca2_hi, MPFR_RNDU);",
    )
    text = replace_once(
        text,
        "        mpfr_mul(c2_hi, shell_hi, ca2_hi, MPFR_RNDU);",
        "        // Directed C0 and C1 moment sums for first omitted shell m=7.\n"
        "        mpfr_ui_div(series0_hi, 1, one_minus_q_lo, MPFR_RNDU);\n"
        "        mpfr_ui_div(series1_hi, 9, one_minus_q_lo, MPFR_RNDU);\n"
        "        mpfr_div(term_hi, q_hi, den2_lo, MPFR_RNDU);\n"
        "        mpfr_add(series1_hi, series1_hi, term_hi, MPFR_RNDU);\n"
        "        mpfr_mul(c0_hi, shell_hi, series0_hi, MPFR_RNDU);\n"
        "        mpfr_mul(c1_hi, shell_hi, ca_hi, MPFR_RNDU);\n"
        "        mpfr_mul(c1_hi, c1_hi, series1_hi, MPFR_RNDU);\n\n"
        "        mpfr_mul(c2_hi, shell_hi, ca2_hi, MPFR_RNDU);",
    )
    text = replace_once(
        text,
        "            << \"  \\\"shell_ratio_upper\\\": \\\"\" << decimal(q_hi) << \"\\\",\\n\"",
        "            << \"  \\\"shell_ratio_upper\\\": \\\"\" << decimal(q_hi) << \"\\\",\\n\"\n"
        "            << \"  \\\"C0_per_abs_w_upper_directed\\\": \\\"\" << decimal(c0_hi) << \"\\\",\\n\"\n"
        "            << \"  \\\"C1_coordinate_per_abs_w_upper_directed\\\": \\\"\" << decimal(c1_hi) << \"\\\",\\n\"",
    )
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
