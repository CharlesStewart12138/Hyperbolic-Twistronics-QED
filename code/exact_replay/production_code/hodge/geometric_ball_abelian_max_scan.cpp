#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#define CM_TENSOR_NO_MAIN
#include "geometric_ball_tensor_stream.cpp"
#undef CM_TENSOR_NO_MAIN

namespace {

void replace_file(const fs::path& temporary, const fs::path& final_path) {
  if (fs::exists(final_path)) fs::remove(final_path);
  fs::rename(temporary, final_path);
}

std::string bucket_name(int bucket, const std::string& suffix) {
  std::ostringstream value;
  value << "bucket-" << std::setw(3) << std::setfill('0') << bucket << suffix;
  return value.str();
}

bool complete_summary(const fs::path& path, int bucket, std::uint64_t count) {
  if (!fs::exists(path)) return false;
  std::ifstream input(path);
  std::ostringstream text;
  text << input.rdbuf();
  const std::string value = text.str();
  return value.find("\"status\": \"COMPLETE\"") != std::string::npos
      && value.find("\"bucket\": " + std::to_string(bucket)) != std::string::npos
      && value.find("\"elements_consumed\": " + std::to_string(count)) != std::string::npos;
}

void scan_bucket(const fs::path& source, int bucket, const std::string& family,
                 const fs::path& output) {
  const std::uint64_t count = checked_record_count(source);
  if (complete_summary(output, bucket, count)) {
    std::cout << "already_complete family=" << family << " bucket=" << bucket << '\n';
    return;
  }
  const auto started = std::chrono::steady_clock::now();
  std::ifstream input(source, std::ios::binary);
  if (!input) fail("cannot open exact geometric bucket");
  std::vector<char> buffer(16U * 1024U * 1024U);
  input.rdbuf()->pubsetbuf(buffer.data(), static_cast<std::streamsize>(buffer.size()));
  std::uint64_t maximum_norm_squared = 0;
  std::uint64_t maximum_l1 = 0;
  std::uint64_t maximum_abs_coordinate = 0;
  std::uint8_t maximum_depth = 0;
  std::array<int, 4> maximizing_vector{};
  std::uint8_t maximizing_depth = 0;
  for (std::uint64_t row = 0; row < count; ++row) {
    const GeoRecord record = geo_read_record(input);
    if (!input) fail("short exact geometric bucket record");
    const auto vector = record_abelianization(record);
    std::uint64_t norm_squared = 0;
    std::uint64_t l1 = 0;
    std::uint64_t linf = 0;
    for (int coordinate : vector) {
      const auto magnitude = static_cast<std::uint64_t>(coordinate < 0 ? -coordinate : coordinate);
      norm_squared += magnitude * magnitude;
      l1 += magnitude;
      linf = std::max(linf, magnitude);
    }
    if (norm_squared > maximum_norm_squared ||
        (norm_squared == maximum_norm_squared && vector < maximizing_vector)) {
      maximum_norm_squared = norm_squared;
      maximizing_vector = vector;
      maximizing_depth = record.depth;
    }
    maximum_l1 = std::max(maximum_l1, l1);
    maximum_abs_coordinate = std::max(maximum_abs_coordinate, linf);
    maximum_depth = std::max(maximum_depth, record.depth);
  }
  char trailing = 0;
  input.read(&trailing, 1);
  if (input.gcount() != 0) fail("trailing partial exact record");
  const double elapsed = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - started).count();
  fs::create_directories(output.parent_path());
  const fs::path temporary = output.string() + ".tmp";
  std::ofstream out(temporary, std::ios::trunc);
  if (!out) fail("cannot create abelian maximum summary");
  out << "{\n"
      << "  \"schema_version\": \"1.0\",\n"
      << "  \"task_id\": \"CM-047-NP-M7-ANALYTIC-TAIL\",\n"
      << "  \"status\": \"COMPLETE\",\n"
      << "  \"family\": \"" << family << "\",\n"
      << "  \"bucket\": " << bucket << ",\n"
      << "  \"elements_consumed\": " << count << ",\n"
      << "  \"maximum_norm_squared\": " << maximum_norm_squared << ",\n"
      << "  \"maximum_l1\": " << maximum_l1 << ",\n"
      << "  \"maximum_abs_coordinate\": " << maximum_abs_coordinate << ",\n"
      << "  \"maximum_transport_word_depth\": " << static_cast<int>(maximum_depth) << ",\n"
      << "  \"maximizing_vector\": [" << maximizing_vector[0] << ", "
      << maximizing_vector[1] << ", " << maximizing_vector[2] << ", "
      << maximizing_vector[3] << "],\n"
      << "  \"maximizing_vector_word_depth\": " << static_cast<int>(maximizing_depth) << ",\n"
      << "  \"peak_rss_bytes\": " << peak_rss() << ",\n"
      << "  \"elapsed_seconds\": " << std::setprecision(17) << elapsed << "\n"
      << "}\n";
  out.close();
  if (!out) fail("cannot flush abelian maximum summary");
  replace_file(temporary, output);
  std::cout << "family=" << family << " bucket=" << bucket << " elements=" << count
            << " max_norm_squared=" << maximum_norm_squared << " seconds=" << elapsed << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 6) {
      std::cerr << "usage: geometric_ball_abelian_max_scan INPUT_DIR FAMILY OUTPUT_DIR START STOP\n";
      return 2;
    }
    const fs::path input_dir = argv[1];
    const std::string family = argv[2];
    const fs::path output_dir = argv[3];
    const int start = std::stoi(argv[4]);
    const int stop = std::stoi(argv[5]);
    if (start < 0 || stop >= 256 || start > stop) fail("invalid bucket range");
    for (int bucket = start; bucket <= stop; ++bucket) {
      scan_bucket(input_dir / bucket_name(bucket, ".bin"), bucket, family,
                  output_dir / family / bucket_name(bucket, ".json"));
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
