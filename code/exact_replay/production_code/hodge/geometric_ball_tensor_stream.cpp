#include <mpfr.h>

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

#define CM_GEO7_NO_MAIN
#include "../group/external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {

constexpr mpfr_prec_t kTensorPrecision = 192;
constexpr std::size_t kTensorEntries = 10;

constexpr std::array<std::array<int, 4>, 8> kGeoGeneratorAbelianization{{
    {{ 1,  0,  0,  0}},
    {{ 0, -1,  0,  0}},
    {{-1, -1,  1,  0}},
    {{-1, -1,  0, -1}},
    {{-1,  0,  0,  0}},
    {{ 0,  1,  0,  0}},
    {{ 1,  1, -1,  0}},
    {{ 1,  1,  0,  1}},
}};

std::size_t tensor_index(int i, int j) {
  if (i > j) std::swap(i, j);
  static constexpr std::size_t start[4]{0, 4, 7, 9};
  return start[i] + static_cast<std::size_t>(j - i);
}

std::array<int, 4> record_abelianization(const GeoRecord& record) {
  std::array<int, 4> result{};
  std::uint64_t high = record.word_high, low = record.word_low;
  for (std::uint8_t i = 0; i < record.depth; ++i) {
    const int token = static_cast<int>(low & 7U);
    for (int coordinate = 0; coordinate < 4; ++coordinate) {
      result[coordinate] += kGeoGeneratorAbelianization[token][coordinate];
    }
    low = (low >> 3U) | (high << 61U);
    high >>= 3U;
  }
  if (high != 0 || low != 0) fail("transport word has bits above declared depth");
  return result;
}

void set_i64(mpfr_t target, std::int64_t value, mpfr_rnd_t rounding) {
  mpz_t exact;
  mpz_init(exact);
  geo_mpz_set_i64_exact(exact, value);
  const int inexact = mpfr_set_z(target, exact, rounding);
  mpz_clear(exact);
  if (inexact != 0) {
    // 192 bits exactly contains every signed 64-bit coefficient.
    fail("int64 coefficient was not represented exactly by MPFR");
  }
}

struct IntervalBasis {
  std::array<mpfr_t, 4> lower{};
  std::array<mpfr_t, 4> upper{};
  mpfr_t a_B_lower;
  mpfr_t a_B_upper;

  IntervalBasis() {
    for (int i = 0; i < 4; ++i) {
      mpfr_init2(lower[i], kTensorPrecision);
      mpfr_init2(upper[i], kTensorPrecision);
    }
    mpfr_init2(a_B_lower, kTensorPrecision);
    mpfr_init2(a_B_upper, kTensorPrecision);
    mpfr_set_ui(lower[0], 1, MPFR_RNDD);
    mpfr_set_ui(upper[0], 1, MPFR_RNDU);
    mpfr_set_ui(lower[1], 2, MPFR_RNDD);
    mpfr_sqrt(lower[1], lower[1], MPFR_RNDD);
    mpfr_set_ui(upper[1], 2, MPFR_RNDU);
    mpfr_sqrt(upper[1], upper[1], MPFR_RNDU);

    mpfr_t temporary;
    mpfr_init2(temporary, kTensorPrecision);
    mpfr_mul_ui(temporary, lower[1], 2, MPFR_RNDD);
    mpfr_add_ui(temporary, temporary, 2, MPFR_RNDD);
    mpfr_sqrt(lower[2], temporary, MPFR_RNDD);
    mpfr_mul_ui(temporary, upper[1], 2, MPFR_RNDU);
    mpfr_add_ui(temporary, temporary, 2, MPFR_RNDU);
    mpfr_sqrt(upper[2], temporary, MPFR_RNDU);
    mpfr_mul(lower[3], lower[1], lower[2], MPFR_RNDD);
    mpfr_mul(upper[3], upper[1], upper[2], MPFR_RNDU);

    mpfr_add_ui(temporary, lower[1], 1, MPFR_RNDD);
    mpfr_acosh(a_B_lower, temporary, MPFR_RNDD);
    mpfr_mul_ui(a_B_lower, a_B_lower, 2, MPFR_RNDD);
    mpfr_add_ui(temporary, upper[1], 1, MPFR_RNDU);
    mpfr_acosh(a_B_upper, temporary, MPFR_RNDU);
    mpfr_mul_ui(a_B_upper, a_B_upper, 2, MPFR_RNDU);
    mpfr_clear(temporary);
  }

  ~IntervalBasis() {
    for (int i = 0; i < 4; ++i) {
      mpfr_clear(lower[i]);
      mpfr_clear(upper[i]);
    }
    mpfr_clear(a_B_lower);
    mpfr_clear(a_B_upper);
  }
};

void field_component_interval(const Field& field, int offset,
                              const IntervalBasis& basis,
                              mpfr_t lower, mpfr_t upper) {
  mpfr_set_zero(lower, 0);
  mpfr_set_zero(upper, 0);
  mpfr_t coefficient, term;
  mpfr_inits2(kTensorPrecision, coefficient, term, static_cast<mpfr_ptr>(nullptr));
  for (int i = 0; i < 4; ++i) {
    const auto value = field.c[static_cast<std::size_t>(offset + i)];
    if (value == 0) continue;
    set_i64(coefficient, value, MPFR_RNDN);
    if (value > 0) {
      mpfr_mul(term, coefficient, basis.lower[i], MPFR_RNDD);
      mpfr_add(lower, lower, term, MPFR_RNDD);
      mpfr_mul(term, coefficient, basis.upper[i], MPFR_RNDU);
      mpfr_add(upper, upper, term, MPFR_RNDU);
    } else {
      mpfr_mul(term, coefficient, basis.upper[i], MPFR_RNDD);
      mpfr_add(lower, lower, term, MPFR_RNDD);
      mpfr_mul(term, coefficient, basis.lower[i], MPFR_RNDU);
      mpfr_add(upper, upper, term, MPFR_RNDU);
    }
  }
  mpfr_div_2ui(lower, lower, field.exp, MPFR_RNDD);
  mpfr_div_2ui(upper, upper, field.exp, MPFR_RNDU);
  mpfr_clears(coefficient, term, static_cast<mpfr_ptr>(nullptr));
}

void square_interval(const mpfr_t lower, const mpfr_t upper,
                     mpfr_t square_lower, mpfr_t square_upper) {
  mpfr_t left_square_lower, right_square_lower, left_square_upper, right_square_upper;
  mpfr_inits2(kTensorPrecision, left_square_lower, right_square_lower,
              left_square_upper, right_square_upper, static_cast<mpfr_ptr>(nullptr));
  if (mpfr_sgn(lower) <= 0 && mpfr_sgn(upper) >= 0) {
    mpfr_set_zero(square_lower, 0);
  } else {
    mpfr_sqr(left_square_lower, lower, MPFR_RNDD);
    mpfr_sqr(right_square_lower, upper, MPFR_RNDD);
    mpfr_min(square_lower, left_square_lower, right_square_lower, MPFR_RNDD);
  }
  mpfr_sqr(left_square_upper, lower, MPFR_RNDU);
  mpfr_sqr(right_square_upper, upper, MPFR_RNDU);
  mpfr_max(square_upper, left_square_upper, right_square_upper, MPFR_RNDU);
  mpfr_clears(left_square_lower, right_square_lower, left_square_upper,
              right_square_upper, static_cast<mpfr_ptr>(nullptr));
}

void distance_interval_over_a_B(const Matrix& matrix, const IntervalBasis& basis,
                                mpfr_t distance_lower, mpfr_t distance_upper) {
  mpfr_t real_lower, real_upper, imag_lower, imag_upper;
  mpfr_t real2_lower, real2_upper, imag2_lower, imag2_upper;
  mpfr_t cosh_lower, cosh_upper;
  mpfr_inits2(kTensorPrecision, real_lower, real_upper, imag_lower, imag_upper,
              real2_lower, real2_upper, imag2_lower, imag2_upper,
              cosh_lower, cosh_upper, static_cast<mpfr_ptr>(nullptr));
  field_component_interval(matrix.a, 0, basis, real_lower, real_upper);
  field_component_interval(matrix.a, 4, basis, imag_lower, imag_upper);
  square_interval(real_lower, real_upper, real2_lower, real2_upper);
  square_interval(imag_lower, imag_upper, imag2_lower, imag2_upper);
  mpfr_add(cosh_lower, real2_lower, imag2_lower, MPFR_RNDD);
  mpfr_mul_ui(cosh_lower, cosh_lower, 2, MPFR_RNDD);
  mpfr_sub_ui(cosh_lower, cosh_lower, 1, MPFR_RNDD);
  mpfr_add(cosh_upper, real2_upper, imag2_upper, MPFR_RNDU);
  mpfr_mul_ui(cosh_upper, cosh_upper, 2, MPFR_RNDU);
  mpfr_sub_ui(cosh_upper, cosh_upper, 1, MPFR_RNDU);
  if (mpfr_cmp_ui(cosh_lower, 1) < 0) mpfr_set_ui(cosh_lower, 1, MPFR_RNDD);
  if (mpfr_cmp_ui(cosh_upper, 1) < 0) fail("upper cosh displacement below one");
  mpfr_acosh(distance_lower, cosh_lower, MPFR_RNDD);
  mpfr_acosh(distance_upper, cosh_upper, MPFR_RNDU);
  mpfr_div(distance_lower, distance_lower, basis.a_B_upper, MPFR_RNDD);
  mpfr_div(distance_upper, distance_upper, basis.a_B_lower, MPFR_RNDU);
  mpfr_clears(real_lower, real_upper, imag_lower, imag_upper,
              real2_lower, real2_upper, imag2_lower, imag2_upper,
              cosh_lower, cosh_upper, static_cast<mpfr_ptr>(nullptr));
}

void physical_weight_interval(const mpfr_t distance_lower, const mpfr_t distance_upper,
                              mpfr_t weight_lower, mpfr_t weight_upper) {
  mpfr_t value, half;
  mpfr_inits2(kTensorPrecision, value, half, static_cast<mpfr_ptr>(nullptr));
  mpfr_set_ui(half, 1, MPFR_RNDN);
  mpfr_div_2ui(half, half, 1, MPFR_RNDN);
  mpfr_sqr(value, distance_upper, MPFR_RNDU);
  mpfr_add_d(value, value, 0.25, MPFR_RNDU);
  mpfr_sqrt(value, value, MPFR_RNDU);
  mpfr_sub(value, value, half, MPFR_RNDU);
  mpfr_mul_ui(value, value, 5, MPFR_RNDU);
  mpfr_neg(value, value, MPFR_RNDN);
  mpfr_exp(weight_lower, value, MPFR_RNDD);
  mpfr_sqr(value, distance_lower, MPFR_RNDD);
  mpfr_add_d(value, value, 0.25, MPFR_RNDD);
  mpfr_sqrt(value, value, MPFR_RNDD);
  mpfr_sub(value, value, half, MPFR_RNDD);
  mpfr_mul_ui(value, value, 5, MPFR_RNDD);
  mpfr_neg(value, value, MPFR_RNDN);
  mpfr_exp(weight_upper, value, MPFR_RNDU);
  if (mpfr_cmp(weight_lower, weight_upper) > 0) fail("reversed weight interval");
  mpfr_clears(value, half, static_cast<mpfr_ptr>(nullptr));
}

std::string tensor_decimal(const mpfr_t value, bool lower_endpoint) {
  std::array<char, 192> buffer{};
  const char* format = lower_endpoint ? "%.70RDe" : "%.70RUe";
  const int written = mpfr_snprintf(buffer.data(), buffer.size(), format, value);
  if (written < 0 || static_cast<std::size_t>(written) >= buffer.size()) fail("MPFR output overflow");
  return std::string(buffer.data());
}

void print_tensor(std::ostream& out, const std::array<mpfr_t, kTensorEntries>& packed,
                  int indentation, bool lower_endpoint) {
  const std::string pad(static_cast<std::size_t>(indentation), ' ');
  out << "[\n";
  for (int i = 0; i < 4; ++i) {
    out << pad << "  [";
    for (int j = 0; j < 4; ++j) {
      if (j) out << ", ";
      out << '"' << tensor_decimal(packed[tensor_index(i, j)], lower_endpoint) << '"';
    }
    out << ']' << (i == 3 ? "\n" : ",\n");
  }
  out << pad << ']';
}

struct RegistryHeader {
  std::string magic;
  std::uint64_t count = 0;
  std::uint32_t record_bytes = 0;
  std::uint32_t header_bytes = 0;
  std::string scope;
};

RegistryHeader read_registry_header(std::istream& input) {
  std::array<char, 8> magic{};
  input.read(magic.data(), 8);
  RegistryHeader result;
  result.magic.assign(magic.data(), magic.size());
  result.count = read_u64(input);
  result.record_bytes = read_u32(input);
  if (result.magic == "BOLZGEO1") {
    const auto radius = read_u32(input);
    result.header_bytes = 24;
    result.scope = "closed geometric ball d<=" + std::to_string(radius) + "a_B";
  } else if (result.magic == "BOLZSH71") {
    const auto lower = read_u32(input), upper = read_u32(input);
    result.header_bytes = 28;
    result.scope = "exact geometric shell " + std::to_string(lower) + "a_B<d<=" + std::to_string(upper) + "a_B";
  } else {
    fail("unsupported geometric registry magic");
  }
  if (result.record_bytes != kGeoRecordBytes) fail("geometric registry record-size mismatch");
  return result;
}

void tensor_mode(const fs::path& registry_path, const fs::path& output_path) {
  const auto started = std::chrono::steady_clock::now();
  std::ifstream input(registry_path, std::ios::binary);
  if (!input) fail("cannot open geometric registry");
  std::vector<char> input_buffer(32U * 1024U * 1024U);
  input.rdbuf()->pubsetbuf(input_buffer.data(), static_cast<std::streamsize>(input_buffer.size()));
  const RegistryHeader header = read_registry_header(input);
  if (fs::file_size(registry_path) != header.header_bytes + header.count * header.record_bytes) {
    fail("geometric registry byte count mismatch");
  }

  IntervalBasis basis;
  std::array<mpfr_t, kTensorEntries> lower{}, upper{};
  for (std::size_t k = 0; k < kTensorEntries; ++k) {
    mpfr_init2(lower[k], kTensorPrecision);
    mpfr_init2(upper[k], kTensorPrecision);
    mpfr_set_zero(lower[k], 0);
    mpfr_set_zero(upper[k], 0);
  }
  mpfr_t distance_lower, distance_upper, weight_lower, weight_upper, term;
  mpfr_inits2(kTensorPrecision, distance_lower, distance_upper, weight_lower,
              weight_upper, term, static_cast<mpfr_ptr>(nullptr));
  std::uint64_t unweighted_trace = 0;
  std::uint8_t maximum_depth = 0;
  for (std::uint64_t row = 0; row < header.count; ++row) {
    const GeoRecord record = geo_read_record(input);
    if (!input) fail("short geometric registry record");
    maximum_depth = std::max(maximum_depth, record.depth);
    const auto vector = record_abelianization(record);
    std::uint64_t trace = 0;
    for (const int value : vector) trace += static_cast<std::uint64_t>(value * value);
    unweighted_trace += trace;
    if (trace != 0) {
      distance_interval_over_a_B(record.key, basis, distance_lower, distance_upper);
      physical_weight_interval(distance_lower, distance_upper, weight_lower, weight_upper);
      for (int i = 0; i < 4; ++i) {
        for (int j = i; j < 4; ++j) {
          const long coefficient = static_cast<long>(vector[i] * vector[j]);
          const auto index = tensor_index(i, j);
          if (coefficient >= 0) {
            mpfr_mul_si(term, weight_lower, coefficient, MPFR_RNDD);
            mpfr_add(lower[index], lower[index], term, MPFR_RNDD);
            mpfr_mul_si(term, weight_upper, coefficient, MPFR_RNDU);
            mpfr_add(upper[index], upper[index], term, MPFR_RNDU);
          } else {
            mpfr_mul_si(term, weight_upper, coefficient, MPFR_RNDD);
            mpfr_add(lower[index], lower[index], term, MPFR_RNDD);
            mpfr_mul_si(term, weight_lower, coefficient, MPFR_RNDU);
            mpfr_add(upper[index], upper[index], term, MPFR_RNDU);
          }
        }
      }
    }
    if ((row + 1) % 2000000U == 0) {
      std::cerr << "tensor_rows=" << (row + 1) << '/' << header.count << '\n';
    }
  }
  const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
  if (output_path.has_parent_path()) fs::create_directories(output_path.parent_path());
  std::ofstream output(output_path, std::ios::trunc);
  output << "{\n"
         << "  \"schema_version\": \"1.0\",\n"
         << "  \"task_id\": \"CM-047-NP-GEOMETRIC-STREAM\",\n"
         << "  \"scope\": \"" << header.scope << "\",\n"
         << "  \"registry_magic\": \"" << header.magic << "\",\n"
         << "  \"elements_consumed\": " << header.count << ",\n"
         << "  \"maximum_transport_word_depth\": " << static_cast<int>(maximum_depth) << ",\n"
         << "  \"unweighted_integer_trace_sum\": " << unweighted_trace << ",\n"
         << "  \"mpfr_precision_bits\": " << kTensorPrecision << ",\n"
         << "  \"weight_formula\": \"exp(-5*(sqrt(1/4+d^2)-1/2))\",\n"
         << "  \"partial_tensor_entrywise_lower\": ";
  print_tensor(output, lower, 2, true);
  output << ",\n  \"partial_tensor_entrywise_upper\": ";
  print_tensor(output, upper, 2, false);
  output << ",\n"
         << "  \"directed_rounding_contract\": \"exact algebraic matrix coefficients are evaluated outward at 192 bits; acosh, normalization by a_B, weight, products, and sums use directed MPFR rounding\",\n"
         << "  \"transport_word_contract\": \"the 4-vector is the exact abelianization homomorphism evaluated on the stored deterministic transport word\",\n"
         << "  \"peak_rss_bytes\": " << peak_rss() << ",\n"
         << "  \"elapsed_seconds\": " << std::setprecision(17) << elapsed << "\n"
         << "}\n";

  for (std::size_t k = 0; k < kTensorEntries; ++k) {
    mpfr_clear(lower[k]);
    mpfr_clear(upper[k]);
  }
  mpfr_clears(distance_lower, distance_upper, weight_lower, weight_upper,
              term, static_cast<mpfr_ptr>(nullptr));
  std::cout << "elements=" << header.count << " trace=" << unweighted_trace
            << " seconds=" << elapsed << '\n';
}

}  // namespace

#ifndef CM_TENSOR_NO_MAIN
int main(int argc, char** argv) {
  try {
    if (argc != 3) {
      std::cerr << "usage: geometric_ball_tensor_stream REGISTRY OUTPUT_JSON\n";
      return 2;
    }
    tensor_mode(argv[1], argv[2]);
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
#endif
