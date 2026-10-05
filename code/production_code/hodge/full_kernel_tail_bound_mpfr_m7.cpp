#include <array>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

#include <mpfr.h>

namespace {

constexpr mpfr_prec_t kPrecisionBits = 256;

[[noreturn]] void fail(const std::string& message) { throw std::runtime_error(message); }

std::string decimal(const mpfr_t value) {
    std::array<char, 160> buffer{};
    const int written = mpfr_snprintf(buffer.data(), buffer.size(), "%.60Re", value);
    if (written < 0 || static_cast<std::size_t>(written) >= buffer.size()) fail("MPFR formatting failed");
    return std::string(buffer.data());
}

void phi_integer(unsigned d, mpfr_t lower, mpfr_t upper) {
    mpfr_t x;
    mpfr_init2(x, kPrecisionBits);
    mpfr_set_ui(x, d, MPFR_RNDN);
    mpfr_sqr(x, x, MPFR_RNDN);
    mpfr_add_d(x, x, 0.25, MPFR_RNDN);
    mpfr_sqrt(lower, x, MPFR_RNDD);
    mpfr_sub_d(lower, lower, 0.5, MPFR_RNDD);
    mpfr_sqrt(upper, x, MPFR_RNDU);
    mpfr_sub_d(upper, upper, 0.5, MPFR_RNDU);
    mpfr_clear(x);
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            std::cerr << "usage: full_kernel_tail_bound_mpfr OUTPUT_JSON\n";
            return 2;
        }
        mpfr_t rlo, rhi, klo, khi, rinlo, rinhi, routlo, routhi, tubelo, tubehi;
        mpfr_t tmp, tmp2, denominator_lo, c_gamma_hi, p_hi, b_hi, pka_hi, branch_hi, base_hi, ca2_hi;
        mpfr_t phi6lo, phi6hi, phi7lo, phi7hi, secant_lo, q_hi, shell_hi;
        mpfr_t one_minus_q_lo, den2_lo, den3_lo, series0_hi, series1_hi, series_hi, term_hi, ca_hi, c0_hi, c1_hi, c2_hi;
        mpfr_inits2(kPrecisionBits,
                    rlo, rhi, klo, khi, rinlo, rinhi, routlo, routhi, tubelo, tubehi,
                    tmp, tmp2, denominator_lo, c_gamma_hi, p_hi, b_hi, pka_hi, branch_hi, base_hi, ca2_hi,
                    phi6lo, phi6hi, phi7lo, phi7hi, secant_lo, q_hi, shell_hi,
                    one_minus_q_lo, den2_lo, den3_lo, series0_hi, series1_hi, series_hi, term_hi, ca_hi, c0_hi, c1_hi, c2_hi,
                    static_cast<mpfr_ptr>(nullptr));

        mpfr_set_ui(tmp, 2, MPFR_RNDN);
        mpfr_sqrt(rlo, tmp, MPFR_RNDD);
        mpfr_sqrt(rhi, tmp, MPFR_RNDU);

        // kappa=2 acosh(1+sqrt(2)).
        mpfr_add_ui(tmp, rlo, 1, MPFR_RNDD);
        mpfr_acosh(klo, tmp, MPFR_RNDD);
        mpfr_mul_ui(klo, klo, 2, MPFR_RNDD);
        mpfr_add_ui(tmp, rhi, 1, MPFR_RNDU);
        mpfr_acosh(khi, tmp, MPFR_RNDU);
        mpfr_mul_ui(khi, khi, 2, MPFR_RNDU);
        mpfr_div_2ui(rinlo, klo, 1, MPFR_RNDD);
        mpfr_div_2ui(rinhi, khi, 1, MPFR_RNDU);

        // r_out=acosh((1+sqrt(2))^2), tube=r_in+r_out.
        mpfr_add_ui(tmp, rlo, 1, MPFR_RNDD);
        mpfr_sqr(tmp, tmp, MPFR_RNDD);
        mpfr_acosh(routlo, tmp, MPFR_RNDD);
        mpfr_add_ui(tmp, rhi, 1, MPFR_RNDU);
        mpfr_sqr(tmp, tmp, MPFR_RNDU);
        mpfr_acosh(routhi, tmp, MPFR_RNDU);
        mpfr_add(tubelo, rinlo, routlo, MPFR_RNDD);
        mpfr_add(tubehi, rinhi, routhi, MPFR_RNDU);

        // Lower denominator cosh(r_in)-1 used for all quotient upper bounds.
        mpfr_cosh(denominator_lo, rinlo, MPFR_RNDD);
        mpfr_sub_ui(denominator_lo, denominator_lo, 1, MPFR_RNDD);
        if (mpfr_sgn(denominator_lo) <= 0) fail("nonpositive inball denominator");

        // C_Gamma <= exp(3*kappa/2)/(2(cosh(r_in)-1)).
        mpfr_mul_ui(tmp, khi, 3, MPFR_RNDU);
        mpfr_div_2ui(tmp, tmp, 1, MPFR_RNDU);
        mpfr_exp(tmp, tmp, MPFR_RNDU);
        mpfr_mul_ui(tmp2, denominator_lo, 2, MPFR_RNDD);
        mpfr_div(c_gamma_hi, tmp, tmp2, MPFR_RNDU);

        // Bound both branches entering C_A=sqrt(3)*max(p*kappa,(p*kappa+b)/2).
        mpfr_sinh(tmp, tubehi, MPFR_RNDU);
        mpfr_const_pi(tmp2, MPFR_RNDD);
        mpfr_mul(tmp2, tmp2, denominator_lo, MPFR_RNDD);
        mpfr_div(p_hi, tmp, tmp2, MPFR_RNDU);
        mpfr_cosh(tmp, tubehi, MPFR_RNDU);
        mpfr_sub_ui(tmp, tmp, 1, MPFR_RNDU);
        mpfr_div(b_hi, tmp, denominator_lo, MPFR_RNDU);
        mpfr_mul(pka_hi, p_hi, khi, MPFR_RNDU);
        mpfr_add(branch_hi, pka_hi, b_hi, MPFR_RNDU);
        mpfr_div_2ui(branch_hi, branch_hi, 1, MPFR_RNDU);
        if (mpfr_cmp(pka_hi, branch_hi) >= 0) mpfr_set(base_hi, pka_hi, MPFR_RNDU);
        else mpfr_set(base_hi, branch_hi, MPFR_RNDU);
        mpfr_sqr(ca2_hi, base_hi, MPFR_RNDU);
        mpfr_mul_ui(ca2_hi, ca2_hi, 3, MPFR_RNDU);
        mpfr_sqrt(ca_hi, ca2_hi, MPFR_RNDU);

        phi_integer(7, phi6lo, phi6hi);
        phi_integer(8, phi7lo, phi7hi);
        mpfr_sub(secant_lo, phi7lo, phi6hi, MPFR_RNDD);
        if (mpfr_sgn(secant_lo) <= 0) fail("nonpositive secant lower bound");

        // q=exp(kappa-5*secant), upper endpoint.
        mpfr_mul_ui(tmp, secant_lo, 5, MPFR_RNDD);
        mpfr_sub(tmp, khi, tmp, MPFR_RNDU);
        mpfr_exp(q_hi, tmp, MPFR_RNDU);
        if (mpfr_cmp_ui(q_hi, 1) >= 0) fail("tail ratio does not contract");

        // First shell envelope C_Gamma exp(6*kappa-5*phi(6)), upper endpoint.
        mpfr_mul_ui(tmp, khi, 7, MPFR_RNDU);
        mpfr_mul_ui(tmp2, phi6lo, 5, MPFR_RNDD);
        mpfr_sub(tmp, tmp, tmp2, MPFR_RNDU);
        mpfr_exp(tmp, tmp, MPFR_RNDU);
        mpfr_mul(shell_hi, c_gamma_hi, tmp, MPFR_RNDU);

        // sum_{j>=0}(9+j)^2 q^j, evaluated monotonically at q_hi.
        mpfr_ui_sub(one_minus_q_lo, 1, q_hi, MPFR_RNDD);
        mpfr_sqr(den2_lo, one_minus_q_lo, MPFR_RNDD);
        mpfr_mul(den3_lo, den2_lo, one_minus_q_lo, MPFR_RNDD);
        mpfr_ui_div(series_hi, 81, one_minus_q_lo, MPFR_RNDU);
        mpfr_mul_ui(term_hi, q_hi, 18, MPFR_RNDU);
        mpfr_div(term_hi, term_hi, den2_lo, MPFR_RNDU);
        mpfr_add(series_hi, series_hi, term_hi, MPFR_RNDU);
        mpfr_add_ui(tmp, q_hi, 1, MPFR_RNDU);
        mpfr_mul(tmp, tmp, q_hi, MPFR_RNDU);
        mpfr_div(term_hi, tmp, den3_lo, MPFR_RNDU);
        mpfr_add(series_hi, series_hi, term_hi, MPFR_RNDU);

        // Directed C0 and C1 moment sums for first omitted shell m=7.
        mpfr_ui_div(series0_hi, 1, one_minus_q_lo, MPFR_RNDU);
        mpfr_ui_div(series1_hi, 9, one_minus_q_lo, MPFR_RNDU);
        mpfr_div(term_hi, q_hi, den2_lo, MPFR_RNDU);
        mpfr_add(series1_hi, series1_hi, term_hi, MPFR_RNDU);
        mpfr_mul(c0_hi, shell_hi, series0_hi, MPFR_RNDU);
        mpfr_mul(c1_hi, shell_hi, ca_hi, MPFR_RNDU);
        mpfr_mul(c1_hi, c1_hi, series1_hi, MPFR_RNDU);

        mpfr_mul(c2_hi, shell_hi, ca2_hi, MPFR_RNDU);
        mpfr_mul(c2_hi, c2_hi, series_hi, MPFR_RNDU);
        if (mpfr_cmp_d(c2_hi, 48.0) >= 0) fail("directed C2 result does not fit rational envelope 48");

        std::ofstream out(argv[1], std::ios::trunc);
        if (!out) fail("cannot open output JSON");
        out << "{\n"
            << "  \"schema_version\": \"1.0\",\n"
            << "  \"task_id\": \"CM-047-NP-M7\",\n"
            << "  \"first_omitted_shell\": 7,\n"
            << "  \"mpfr_precision_bits\": " << kPrecisionBits << ",\n"
            << "  \"shell_ratio_upper\": \"" << decimal(q_hi) << "\",\n"
            << "  \"C0_per_abs_w_upper_directed\": \"" << decimal(c0_hi) << "\",\n"
            << "  \"C1_coordinate_per_abs_w_upper_directed\": \"" << decimal(c1_hi) << "\",\n"
            << "  \"coordinate_trace_C2_upper_directed\": \"" << decimal(c2_hi) << "\",\n"
            << "  \"certified_rational_coordinate_trace_upper\": 48,\n"
            << "  \"bound\": \"Tr(T_tail)<48 for T_tail=sum_{d>7a_B}|w(d)| n n^T; conditional companion to a complete exact ball through 7a_B\",\n"
            << "  \"rounding_contract\": \"Every monotone endpoint evaluation uses MPFR directed rounding; the final decimal-independent envelope is the integer 48\"\n"
            << "}\n";
        if (!out) fail("output JSON write failed");
        std::cout << "C2_upper=" << decimal(c2_hi) << " certified_integer=48\n";

        mpfr_clears(rlo, rhi, klo, khi, rinlo, rinhi, routlo, routhi, tubelo, tubehi,
                    tmp, tmp2, denominator_lo, c_gamma_hi, p_hi, b_hi, pka_hi, branch_hi, base_hi, ca2_hi,
                    phi6lo, phi6hi, phi7lo, phi7hi, secant_lo, q_hi, shell_hi,
                    one_minus_q_lo, den2_lo, den3_lo, series0_hi, series1_hi, series_hi, term_hi, ca_hi, c0_hi, c1_hi, c2_hi,
                    static_cast<mpfr_ptr>(nullptr));
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
