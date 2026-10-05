#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#define CM_TENSOR_NO_MAIN
#include "geometric_ball_tensor_stream.cpp"
#undef CM_TENSOR_NO_MAIN

namespace {

void atomic_replace_file(const fs::path& temporary, const fs::path& final_path) {
  if (fs::exists(final_path)) fs::remove(final_path);
  fs::rename(temporary, final_path);
}

void tensor_bucket_mode(const fs::path& bucket_path, int bucket,
                        const fs::path& output_json, const fs::path& output_accumulator) {
  if (bucket < 0 || bucket >= kBuckets) fail("tensor bucket index out of range");
  const auto started = std::chrono::steady_clock::now();
  const std::uint64_t count = checked_record_count(bucket_path);
  std::ifstream input(bucket_path, std::ios::binary);
  if (!input) fail("cannot open exact shell bucket");
  std::vector<char> input_buffer(16U * 1024U * 1024U);
  input.rdbuf()->pubsetbuf(input_buffer.data(), static_cast<std::streamsize>(input_buffer.size()));

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
  for (std::uint64_t row = 0; row < count; ++row) {
    const GeoRecord record = geo_read_record(input);
    if (!input) fail("short exact shell bucket record");
    maximum_depth = std::max(maximum_depth, record.depth);
    const auto vector = record_abelianization(record);
    std::uint64_t trace = 0;
    for (const int value : vector) trace += static_cast<std::uint64_t>(value * value);
    unweighted_trace += trace;
    if (trace == 0) continue;
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
  char trailing = 0;
  input.read(&trailing, 1);
  if (input.gcount() != 0) fail("exact shell bucket has trailing partial data");
  const double elapsed = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - started).count();
  const std::uint64_t rss = peak_rss();

  fs::create_directories(output_json.parent_path());
  fs::create_directories(output_accumulator.parent_path());
  const fs::path json_temporary = output_json.string() + ".tmp";
  const fs::path accumulator_temporary = output_accumulator.string() + ".tmp";
  {
    std::ofstream output(json_temporary, std::ios::trunc);
    if (!output) fail("cannot write tensor bucket JSON");
    output << "{\n"
           << "  \"schema_version\": \"1.0\",\n"
           << "  \"task_id\": \"CM-047-NP-M7-STREAM\",\n"
           << "  \"scope\": \"exact geometric shell 6a_B<d<=7a_B; exact-key bucket " << bucket << "\",\n"
           << "  \"bucket\": " << bucket << ",\n"
           << "  \"status\": \"COMPLETE\",\n"
           << "  \"elements_consumed\": " << count << ",\n"
           << "  \"maximum_transport_word_depth\": " << static_cast<int>(maximum_depth) << ",\n"
           << "  \"unweighted_integer_trace_sum\": " << unweighted_trace << ",\n"
           << "  \"mpfr_precision_bits\": " << kTensorPrecision << ",\n"
           << "  \"weight_formula\": \"exp(-5*(sqrt(1/4+d^2)-1/2))\",\n"
           << "  \"partial_tensor_entrywise_lower\": ";
    print_tensor(output, lower, 2, true);
    output << ",\n  \"partial_tensor_entrywise_upper\": ";
    print_tensor(output, upper, 2, false);
    output << ",\n"
           << "  \"directed_rounding_contract\": \"RNDD lower and RNDU upper at 192-bit MPFR precision for algebraic evaluation, distance, weight, products, and sequential within-bucket sums\",\n"
           << "  \"transport_word_contract\": \"tensor contribution is a function of exact group element; the stored word is used only to evaluate the certified abelianization homomorphism\",\n"
           << "  \"peak_rss_bytes\": " << rss << ",\n"
           << "  \"elapsed_seconds\": " << std::setprecision(17) << elapsed << "\n"
           << "}\n";
    output.flush();
    if (!output) fail("cannot flush tensor bucket JSON");
  }
  {
    std::ofstream output(accumulator_temporary, std::ios::trunc);
    if (!output) fail("cannot write tensor bucket accumulator");
    output << "schema_version\t1.0\n"
           << "status\tCOMPLETE\n"
           << "bucket\t" << bucket << '\n'
           << "elements_consumed\t" << count << '\n'
           << "unweighted_integer_trace_sum\t" << unweighted_trace << '\n'
           << "maximum_transport_word_depth\t" << static_cast<int>(maximum_depth) << '\n'
           << "peak_rss_bytes\t" << rss << '\n'
           << "elapsed_seconds\t" << std::setprecision(17) << elapsed << '\n';
    for (std::size_t k = 0; k < kTensorEntries; ++k) {
      output << "lower_" << k << '\t' << tensor_decimal(lower[k], true) << '\n'
             << "upper_" << k << '\t' << tensor_decimal(upper[k], false) << '\n';
    }
    output.flush();
    if (!output) fail("cannot flush tensor bucket accumulator");
  }
  atomic_replace_file(json_temporary, output_json);
  atomic_replace_file(accumulator_temporary, output_accumulator);

  for (std::size_t k = 0; k < kTensorEntries; ++k) {
    mpfr_clear(lower[k]);
    mpfr_clear(upper[k]);
  }
  mpfr_clears(distance_lower, distance_upper, weight_lower, weight_upper,
              term, static_cast<mpfr_ptr>(nullptr));
  std::cout << "bucket=" << bucket << " elements=" << count << " trace="
            << unweighted_trace << " seconds=" << elapsed << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 5) {
      std::cerr << "usage: geometric_ball_tensor_bucket BUCKET_BIN BUCKET_INDEX OUTPUT_JSON OUTPUT_ACC\n";
      return 2;
    }
    tensor_bucket_mode(argv[1], std::stoi(argv[2]), argv[3], argv[4]);
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
