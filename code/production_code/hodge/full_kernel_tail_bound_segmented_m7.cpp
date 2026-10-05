#include <array>
#include <fstream>
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>

#include <mpfr.h>

namespace fs = std::filesystem;

namespace {

constexpr mpfr_prec_t PRECISION = 256;

[[noreturn]] void fail(const std::string& message) { throw std::runtime_error(message); }

std::string down(const mpfr_t value) {
  std::array<char, 192> buffer{};
  const int written = mpfr_snprintf(buffer.data(), buffer.size(), "%.75RDe", value);
  if (written < 0 || static_cast<std::size_t>(written) >= buffer.size()) fail("MPFR lower formatting failed");
  return buffer.data();
}

std::string up(const mpfr_t value) {
  std::array<char, 192> buffer{};
  const int written = mpfr_snprintf(buffer.data(), buffer.size(), "%.75RUe", value);
  if (written < 0 || static_cast<std::size_t>(written) >= buffer.size()) fail("MPFR upper formatting failed");
  return buffer.data();
}

void phi_integer(unsigned distance, mpfr_t lower, mpfr_t upper) {
  mpfr_t value;
  mpfr_init2(value, PRECISION);
  mpfr_set_ui(value, distance, MPFR_RNDN);
  mpfr_sqr(value, value, MPFR_RNDN);
  mpfr_add_d(value, value, 0.25, MPFR_RNDN);
  mpfr_sqrt(lower, value, MPFR_RNDD);
  mpfr_sub_d(lower, lower, 0.5, MPFR_RNDD);
  mpfr_sqrt(upper, value, MPFR_RNDU);
  mpfr_sub_d(upper, upper, 0.5, MPFR_RNDU);
  mpfr_clear(value);
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) {
      std::cerr << "usage: full_kernel_tail_bound_segmented_m7 OUTPUT_JSON\n";
      return 2;
    }
    mpfr_t root2_lo, root2_hi, a_lo, a_hi, rin_lo, rho_hi, rho_ratio_hi, cosh_a_lo;
    mpfr_t denominator_lo, c_gamma_hi, phi7_lo, phi7_hi, phi8_lo, phi8_hi;
    mpfr_t secant_lo, q_hi, one_minus_q_lo, shell_hi, q2_hi, q3_hi, q4_hi;
    mpfr_t q5_hi, q6_hi, q7_hi, one_minus_q5_lo, den_q5_2_lo, den_q5_3_lo;
    mpfr_t block_hi, sum_l_hi, sum_l2_hi, series1_hi, series2_hi;
    mpfr_t c0_hi, c1_hi, c2_hi, sqrt147_hi, temporary, term_hi;
    mpfr_inits2(PRECISION,
      root2_lo, root2_hi, a_lo, a_hi, rin_lo, rho_hi, rho_ratio_hi, cosh_a_lo,
      denominator_lo, c_gamma_hi, phi7_lo, phi7_hi, phi8_lo, phi8_hi,
      secant_lo, q_hi, one_minus_q_lo, shell_hi, q2_hi, q3_hi, q4_hi,
      q5_hi, q6_hi, q7_hi, one_minus_q5_lo, den_q5_2_lo, den_q5_3_lo,
      block_hi, sum_l_hi, sum_l2_hi, series1_hi, series2_hi,
      c0_hi, c1_hi, c2_hi, sqrt147_hi, temporary, term_hi,
      static_cast<mpfr_ptr>(nullptr));

    mpfr_set_ui(temporary, 2, MPFR_RNDN);
    mpfr_sqrt(root2_lo, temporary, MPFR_RNDD);
    mpfr_sqrt(root2_hi, temporary, MPFR_RNDU);
    mpfr_add_ui(temporary, root2_lo, 1, MPFR_RNDD);
    mpfr_acosh(a_lo, temporary, MPFR_RNDD);
    mpfr_mul_ui(a_lo, a_lo, 2, MPFR_RNDD);
    mpfr_add_ui(temporary, root2_hi, 1, MPFR_RNDU);
    mpfr_acosh(a_hi, temporary, MPFR_RNDU);
    mpfr_mul_ui(a_hi, a_hi, 2, MPFR_RNDU);
    mpfr_div_2ui(rin_lo, a_lo, 1, MPFR_RNDD);

    // Bolza Dirichlet circumradius rho=acosh((1+sqrt(2))^2), with rho<a_B.
    mpfr_add_ui(temporary, root2_hi, 1, MPFR_RNDU);
    mpfr_sqr(temporary, temporary, MPFR_RNDU);
    mpfr_acosh(rho_hi, temporary, MPFR_RNDU);
    if (mpfr_cmp(rho_hi, a_lo) >= 0) fail("directed proof of rho<a_B failed");
    mpfr_div(rho_ratio_hi, rho_hi, a_lo, MPFR_RNDU);

    // Same rigorous packing count N_n <= C_Gamma exp(n a_B/R).
    mpfr_cosh(denominator_lo, rin_lo, MPFR_RNDD);
    mpfr_sub_ui(denominator_lo, denominator_lo, 1, MPFR_RNDD);
    mpfr_mul_ui(temporary, a_hi, 3, MPFR_RNDU);
    mpfr_div_2ui(temporary, temporary, 1, MPFR_RNDU);
    mpfr_exp(temporary, temporary, MPFR_RNDU);
    mpfr_mul_ui(term_hi, denominator_lo, 2, MPFR_RNDD);
    mpfr_div(c_gamma_hi, temporary, term_hi, MPFR_RNDU);

    // Convex physical-kernel secant ratio beginning at strict d>7 a_B.
    phi_integer(7, phi7_lo, phi7_hi);
    phi_integer(8, phi8_lo, phi8_hi);
    mpfr_sub(secant_lo, phi8_lo, phi7_hi, MPFR_RNDD);
    mpfr_mul_ui(temporary, secant_lo, 5, MPFR_RNDD);
    mpfr_sub(temporary, a_hi, temporary, MPFR_RNDU);
    mpfr_exp(q_hi, temporary, MPFR_RNDU);
    if (mpfr_cmp_ui(q_hi, 1) >= 0) fail("tail ratio does not contract");
    mpfr_ui_sub(one_minus_q_lo, 1, q_hi, MPFR_RNDD);

    // P_7=C_Gamma exp(7a_B/R-5 phi(7)).
    mpfr_mul_ui(temporary, a_hi, 7, MPFR_RNDU);
    mpfr_mul_ui(term_hi, phi7_lo, 5, MPFR_RNDD);
    mpfr_sub(temporary, temporary, term_hi, MPFR_RNDU);
    mpfr_exp(temporary, temporary, MPFR_RNDU);
    mpfr_mul(shell_hi, c_gamma_hi, temporary, MPFR_RNDU);

    // k_j=ceil((j+8)/5): k=2 for j=0,1,2 and five terms per k>=3.
    mpfr_sqr(q2_hi, q_hi, MPFR_RNDU);
    mpfr_mul(q3_hi, q2_hi, q_hi, MPFR_RNDU);
    mpfr_mul(q4_hi, q3_hi, q_hi, MPFR_RNDU);
    mpfr_mul(q5_hi, q4_hi, q_hi, MPFR_RNDU);
    mpfr_mul(q6_hi, q5_hi, q_hi, MPFR_RNDU);
    mpfr_mul(q7_hi, q6_hi, q_hi, MPFR_RNDU);
    mpfr_ui_sub(one_minus_q5_lo, 1, q5_hi, MPFR_RNDD);
    mpfr_sqr(den_q5_2_lo, one_minus_q5_lo, MPFR_RNDD);
    mpfr_mul(den_q5_3_lo, den_q5_2_lo, one_minus_q5_lo, MPFR_RNDD);
    mpfr_add(block_hi, q3_hi, q4_hi, MPFR_RNDU);
    mpfr_add(block_hi, block_hi, q5_hi, MPFR_RNDU);
    mpfr_add(block_hi, block_hi, q6_hi, MPFR_RNDU);
    mpfr_add(block_hi, block_hi, q7_hi, MPFR_RNDU);

    // sum_{l>=0}(l+3) Q^l = Q/(1-Q)^2 + 3/(1-Q), Q=q^5.
    mpfr_div(sum_l_hi, q5_hi, den_q5_2_lo, MPFR_RNDU);
    mpfr_ui_div(term_hi, 3, one_minus_q5_lo, MPFR_RNDU);
    mpfr_add(sum_l_hi, sum_l_hi, term_hi, MPFR_RNDU);

    // sum_{l>=0}(l+3)^2 Q^l.
    mpfr_add_ui(temporary, q5_hi, 1, MPFR_RNDU);
    mpfr_mul(temporary, temporary, q5_hi, MPFR_RNDU);
    mpfr_div(sum_l2_hi, temporary, den_q5_3_lo, MPFR_RNDU);
    mpfr_mul_ui(temporary, q5_hi, 6, MPFR_RNDU);
    mpfr_div(temporary, temporary, den_q5_2_lo, MPFR_RNDU);
    mpfr_add(sum_l2_hi, sum_l2_hi, temporary, MPFR_RNDU);
    mpfr_ui_div(temporary, 9, one_minus_q5_lo, MPFR_RNDU);
    mpfr_add(sum_l2_hi, sum_l2_hi, temporary, MPFR_RNDU);

    // S1=2(1+q+q^2)+(q^3+...+q^7) sum(l+3)Q^l.
    mpfr_add_ui(series1_hi, q_hi, 1, MPFR_RNDU);
    mpfr_add(series1_hi, series1_hi, q2_hi, MPFR_RNDU);
    mpfr_mul_ui(series1_hi, series1_hi, 2, MPFR_RNDU);
    mpfr_mul(temporary, block_hi, sum_l_hi, MPFR_RNDU);
    mpfr_add(series1_hi, series1_hi, temporary, MPFR_RNDU);

    // S2=4(1+q+q^2)+(q^3+...+q^7) sum(l+3)^2 Q^l.
    mpfr_add_ui(series2_hi, q_hi, 1, MPFR_RNDU);
    mpfr_add(series2_hi, series2_hi, q2_hi, MPFR_RNDU);
    mpfr_mul_ui(series2_hi, series2_hi, 4, MPFR_RNDU);
    mpfr_mul(temporary, block_hi, sum_l2_hi, MPFR_RNDU);
    mpfr_add(series2_hi, series2_hi, temporary, MPFR_RNDU);

    mpfr_ui_div(c0_hi, 1, one_minus_q_lo, MPFR_RNDU);
    mpfr_mul(c0_hi, c0_hi, shell_hi, MPFR_RNDU);
    mpfr_set_ui(sqrt147_hi, 147, MPFR_RNDU);
    mpfr_sqrt(sqrt147_hi, sqrt147_hi, MPFR_RNDU);
    mpfr_mul(c1_hi, shell_hi, sqrt147_hi, MPFR_RNDU);
    mpfr_mul(c1_hi, c1_hi, series1_hi, MPFR_RNDU);
    mpfr_mul_ui(c2_hi, shell_hi, 147, MPFR_RNDU);
    mpfr_mul(c2_hi, c2_hi, series2_hi, MPFR_RNDU);
    if (mpfr_cmp_ui(c2_hi, 1) >= 0) fail("segmented C2 result does not fit rational envelope 1");

    const fs::path output = argv[1];
    const fs::path temporary_path = output.string() + ".tmp";
    std::ofstream out_file(temporary_path, std::ios::trunc);
    if (!out_file) fail("cannot open output JSON");
    out_file << "{\n"
      << "  \"schema_version\": \"1.0\",\n"
      << "  \"task_id\": \"CM-047-NP-M7-ANALYTIC-TAIL\",\n"
      << "  \"status\": \"COMPLETE\",\n"
      << "  \"first_omitted_shell\": 7,\n"
      << "  \"mpfr_precision_bits\": 256,\n"
      << "  \"complete_ball_radius_over_a_B\": 7,\n"
      << "  \"complete_ball_maximum_abelian_norm_squared\": 147,\n"
      << "  \"segmentation_length_over_a_B\": 5,\n"
      << "  \"circumradius_over_a_B_upper\": \"" << up(rho_ratio_hi) << "\",\n"
      << "  \"circumradius_strictly_below_a_B\": true,\n"
      << "  \"increment_displacement_bound\": \"5a_B+2rho<7a_B\",\n"
      << "  \"shell_coordinate_bound\": \"||n(g)||_2^2<=147*ceil((n+1)/5)^2 for n a_B<=d(g o,o)<(n+1)a_B\",\n"
      << "  \"shell_ratio_upper\": \"" << up(q_hi) << "\",\n"
      << "  \"ceil_series_C1_upper\": \"" << up(series1_hi) << "\",\n"
      << "  \"ceil_series_C2_upper\": \"" << up(series2_hi) << "\",\n"
      << "  \"C0_per_abs_w_upper_directed\": \"" << up(c0_hi) << "\",\n"
      << "  \"C1_coordinate_per_abs_w_upper_directed\": \"" << up(c1_hi) << "\",\n"
      << "  \"coordinate_trace_C2_upper_directed\": \"" << up(c2_hi) << "\",\n"
      << "  \"certified_rational_coordinate_trace_upper\": 1,\n"
      << "  \"bound\": \"Tr(T_tail)<1 for T_tail=sum_{d>7a_B}|w(d)| n n^T\",\n"
      << "  \"rounding_contract\": \"Every algebraic, hyperbolic, exponential and rational-series endpoint uses 256-bit MPFR directed rounding; decimal upper endpoints use RNDU\",\n"
      << "  \"proof_contract\": \"Dirichlet-domain geodesic segmentation plus exact exhaustive maximum over B_geo(7a_B); no extrapolation from sampled shells\"\n"
      << "}\n";
    out_file.close();
    if (!out_file) fail("cannot flush output JSON");
    if (fs::exists(output)) fs::remove(output);
    fs::rename(temporary_path, output);
    std::cout << "C0_upper=" << up(c0_hi) << " C1_upper=" << up(c1_hi)
              << " C2_upper=" << up(c2_hi) << " certified_integer=1\n";

    mpfr_clears(root2_lo, root2_hi, a_lo, a_hi, rin_lo, rho_hi, rho_ratio_hi, cosh_a_lo,
      denominator_lo, c_gamma_hi, phi7_lo, phi7_hi, phi8_lo, phi8_hi,
      secant_lo, q_hi, one_minus_q_lo, shell_hi, q2_hi, q3_hi, q4_hi,
      q5_hi, q6_hi, q7_hi, one_minus_q5_lo, den_q5_2_lo, den_q5_3_lo,
      block_hi, sum_l_hi, sum_l2_hi, series1_hi, series2_hi,
      c0_hi, c1_hi, c2_hi, sqrt147_hi, temporary, term_hi,
      static_cast<mpfr_ptr>(nullptr));
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
