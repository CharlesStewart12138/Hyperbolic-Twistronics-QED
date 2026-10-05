#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>

#define CM_GEO7_NO_MAIN
#include "external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {

constexpr std::uint64_t kCommitRecords = 1'000'000;
constexpr std::uint32_t kExactCutoffMarker = std::numeric_limits<std::uint32_t>::max();
constexpr std::array<std::array<std::uint8_t, 16>, 8> kGeneratorImages{{
  {{0,17,19,1,0,22,11,1, 1,10,6,9,1,13,6,18}},
  {{1,0,17,19,1,0,22,11, 18,1,10,6,9,1,13,6}},
  {{11,1,0,17,19,1,0,22, 6,18,1,10,6,9,1,13}},
  {{22,11,1,0,17,19,1,0, 13,6,18,1,10,6,9,1}},
  {{0,22,11,1,0,17,19,1, 1,13,6,18,1,10,6,9}},
  {{1,0,22,11,1,0,17,19, 9,1,13,6,18,1,10,6}},
  {{19,1,0,22,11,1,0,17, 6,9,1,13,6,18,1,10}},
  {{17,19,1,0,22,11,1,0, 10,6,9,1,13,6,18,1}},
}};
constexpr std::array<int, 16> kComponentOrder{{0,8,1,9,2,10,3,11,4,12,5,13,6,14,7,15}};

using Perm = std::array<std::uint8_t, 4>;
using Mul = std::array<std::array<std::uint8_t, 24>, 24>;

struct ScanCheckpoint {
  std::uint64_t total_records = 0;
  std::uint64_t scanned_records = 0;
  std::uint64_t even_nonidentity_records = 0;
  std::uint64_t kernel_elements = 0;
  std::uint64_t dangerous_elements = 0;
  std::uint64_t component_evaluations = 0;
  std::uint64_t candidate_file_bytes = 0;
  std::uint64_t minimum_record_index = 0;
  std::uint8_t minimum_depth = 0;
  std::uint64_t minimum_word_high = 0;
  std::uint64_t minimum_word_low = 0;
  long double minimum_abs_trace_half = std::numeric_limits<long double>::infinity();
  double elapsed_seconds = 0.0;
  bool complete = false;
};

std::map<std::string, std::string> key_values(const fs::path& path) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot read scan checkpoint");
  std::map<std::string, std::string> result;
  std::string line;
  while (std::getline(in, line)) {
    const auto tab = line.find('\t');
    if (tab != std::string::npos) result[line.substr(0, tab)] = line.substr(tab + 1);
  }
  return result;
}

ScanCheckpoint read_scan_checkpoint(const fs::path& path) {
  const auto values = key_values(path);
  ScanCheckpoint c;
  c.total_records = std::stoull(values.at("total_records"));
  c.scanned_records = std::stoull(values.at("scanned_records"));
  c.even_nonidentity_records = std::stoull(values.at("even_nonidentity_records"));
  c.kernel_elements = std::stoull(values.at("kernel_elements"));
  c.dangerous_elements = std::stoull(values.at("dangerous_elements"));
  c.component_evaluations = std::stoull(values.at("component_evaluations"));
  c.candidate_file_bytes = std::stoull(values.at("candidate_file_bytes"));
  c.minimum_record_index = std::stoull(values.at("minimum_record_index"));
  c.minimum_depth = static_cast<std::uint8_t>(std::stoul(values.at("minimum_depth")));
  c.minimum_word_high = std::stoull(values.at("minimum_word_high"));
  c.minimum_word_low = std::stoull(values.at("minimum_word_low"));
  c.minimum_abs_trace_half = std::stold(values.at("minimum_abs_trace_half"));
  c.elapsed_seconds = std::stod(values.at("elapsed_seconds"));
  c.complete = values.at("complete") == "1";
  return c;
}

void write_scan_checkpoint(const fs::path& path, const ScanCheckpoint& c) {
  const auto temporary = path.string() + ".tmp";
  std::ofstream out(temporary, std::ios::trunc);
  if (!out) throw std::runtime_error("cannot write scan checkpoint temporary");
  out << "schema_version\t1.0\n"
      << "algorithm\tshort_circuit_exact_product_quotient_scan\n"
      << "quotient_id\tQ_BASED_S4CORE_PAIR_001\n"
      << "total_records\t" << c.total_records << '\n'
      << "scanned_records\t" << c.scanned_records << '\n'
      << "even_nonidentity_records\t" << c.even_nonidentity_records << '\n'
      << "kernel_elements\t" << c.kernel_elements << '\n'
      << "dangerous_elements\t" << c.dangerous_elements << '\n'
      << "component_evaluations\t" << c.component_evaluations << '\n'
      << "candidate_file_bytes\t" << c.candidate_file_bytes << '\n'
      << "minimum_record_index\t" << c.minimum_record_index << '\n'
      << "minimum_depth\t" << static_cast<unsigned>(c.minimum_depth) << '\n'
      << "minimum_word_high\t" << c.minimum_word_high << '\n'
      << "minimum_word_low\t" << c.minimum_word_low << '\n'
      << "minimum_abs_trace_half\t" << std::setprecision(25) << c.minimum_abs_trace_half << '\n'
      << "elapsed_seconds\t" << std::setprecision(17) << c.elapsed_seconds << '\n'
      << "complete\t" << (c.complete ? 1 : 0) << '\n';
  out.close();
  if (!out) throw std::runtime_error("scan checkpoint write failed");
  if (fs::exists(path)) fs::remove(path);
  fs::rename(temporary, path);
}

std::array<Perm, 24> permutations() {
  std::array<Perm, 24> result{};
  Perm value{{0,1,2,3}};
  std::size_t index = 0;
  do { result[index++] = value; } while (std::next_permutation(value.begin(), value.end()));
  if (index != 24) throw std::runtime_error("S4 enumeration failure");
  return result;
}

Mul multiplication_table(const std::array<Perm, 24>& elements) {
  Mul result{};
  for (std::size_t left = 0; left < 24; ++left) {
    for (std::size_t right = 0; right < 24; ++right) {
      Perm product{};
      for (std::size_t i = 0; i < 4; ++i) product[i] = elements[left][elements[right][i]];
      const auto it = std::find(elements.begin(), elements.end(), product);
      if (it == elements.end()) throw std::runtime_error("S4 product failure");
      result[left][right] = static_cast<std::uint8_t>(it - elements.begin());
    }
  }
  return result;
}

std::uint8_t word_digit(std::uint64_t high, std::uint64_t low, unsigned depth, unsigned index) {
  const unsigned shift = 3U * (depth - 1U - index);
  if (shift < 64U) return static_cast<std::uint8_t>((low >> shift) & 7U);
  return static_cast<std::uint8_t>((high >> (shift - 64U)) & 7U);
}

bool in_product_kernel(std::uint64_t high, std::uint64_t low, unsigned depth,
                       const Mul& multiply, std::uint64_t& evaluations) {
  for (const int component : kComponentOrder) {
    std::uint8_t image = 0;
    for (unsigned index = 0; index < depth; ++index) {
      const auto generator_index = word_digit(high, low, depth, index);
      image = multiply[image][kGeneratorImages[generator_index][component]];
    }
    ++evaluations;
    if (image != 0) return false;
  }
  return true;
}

std::string hex_u64(std::uint64_t value) {
  std::ostringstream out;
  out << std::hex << std::setw(16) << std::setfill('0') << value;
  return out.str();
}

void self_test(const Mul& multiply) {
  for (unsigned generator = 0; generator < 4; ++generator) {
    const std::uint64_t word = (static_cast<std::uint64_t>(generator) << 3U) | (generator + 4U);
    std::uint64_t evaluations = 0;
    if (!in_product_kernel(0, word, 2, multiply, evaluations) || evaluations != 16) {
      throw std::runtime_error("inverse-pair quotient self-test failed");
    }
  }
  for (unsigned generator = 0; generator < 8; ++generator) {
    std::uint64_t evaluations = 0;
    if (in_product_kernel(0, generator, 1, multiply, evaluations)) {
      throw std::runtime_error("single-generator quotient self-test failed");
    }
  }
}

Matrix matrix_from_raw(const std::array<char, kGeoRecordBytes>& raw) {
  std::string bytes(raw.data(), raw.size());
  std::istringstream in(bytes, std::ios::binary);
  return geo_read_record(in).key;
}

Field real_part(const Field& value) {
  Field result = value;
  for (std::size_t i = 4; i < 8; ++i) result.c[i] = 0;
  return result;
}

bool dangerous_trace(const Matrix& matrix) {
  const Field re = real_part(matrix.a);
  const Field cosh_3a = field_from({2405, 1700, 0, 0, 0, 0, 0, 0});
  const Field delta = add(multiply(re, re), negate(multiply(cosh_3a, cosh_3a)));
  return geo_exact_real_field_sign(delta) <= 0;
}

long double abs_trace_half(const Matrix& matrix) {
  return std::fabs(geo_field_value_real(matrix.a));
}

void scan(const fs::path& registry, const fs::path& checkpoint_path,
          const fs::path& candidate_path) {
  const auto elements = permutations();
  const auto multiply = multiplication_table(elements);
  self_test(multiply);

  std::ifstream input(registry, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open exact ball registry");
  static std::array<char, 16 * 1024 * 1024> input_buffer{};
  input.rdbuf()->pubsetbuf(input_buffer.data(), static_cast<std::streamsize>(input_buffer.size()));
  char magic[8]{};
  input.read(magic, 8);
  if (std::string(magic, 8) != "BOLZGEO1") throw std::runtime_error("bad registry magic");
  const std::uint64_t total = read_u64(input);
  if (read_u32(input) != kGeoRecordBytes) throw std::runtime_error("bad record size");
  if (read_u32(input) != kExactCutoffMarker) throw std::runtime_error("wrong cutoff marker");

  ScanCheckpoint state;
  if (fs::exists(checkpoint_path)) {
    state = read_scan_checkpoint(checkpoint_path);
    if (state.total_records != total) throw std::runtime_error("checkpoint registry count drift");
  } else {
    state.total_records = total;
    write_scan_checkpoint(checkpoint_path, state);
  }
  if (state.complete) return;

  if (!fs::exists(candidate_path)) {
    std::ofstream header(candidate_path, std::ios::trunc);
    header << "record_index\tdepth\tword_high_hex\tword_low_hex\tre_c0\tre_c1\tre_c2\tre_c3\texponent\tabs_trace_half\ttranslation_length_over_a_B\tdangerous_le_6a_B\n";
    header.close();
    state.candidate_file_bytes = fs::file_size(candidate_path);
    write_scan_checkpoint(checkpoint_path, state);
  }
  if (fs::file_size(candidate_path) < state.candidate_file_bytes) throw std::runtime_error("candidate file shorter than checkpoint");
  fs::resize_file(candidate_path, state.candidate_file_bytes);
  std::ofstream candidates(candidate_path, std::ios::app);
  candidates << std::setprecision(25);

  input.seekg(static_cast<std::streamoff>(24ULL + state.scanned_records * kGeoRecordBytes));
  std::array<char, kGeoRecordBytes> raw{};
  const long double root2 = std::sqrt(2.0L);
  const long double a_over_r = 2.0L * std::acosh(1.0L + root2);
  auto interval_started = std::chrono::steady_clock::now();
  std::uint64_t next_commit = std::min(total, ((state.scanned_records / kCommitRecords) + 1) * kCommitRecords);

  while (state.scanned_records < total) {
    input.read(raw.data(), raw.size());
    if (!input) throw std::runtime_error("short registry record");
    const std::uint64_t record_index = state.scanned_records;
    const auto depth = static_cast<std::uint8_t>(raw[130]);
    std::uint64_t high = 0, low = 0;
    std::memcpy(&high, raw.data() + 131, sizeof(high));
    std::memcpy(&low, raw.data() + 139, sizeof(low));
    ++state.scanned_records;
    if (depth != 0 && (depth & 1U) == 0U) {
      ++state.even_nonidentity_records;
      if (in_product_kernel(high, low, depth, multiply, state.component_evaluations)) {
        ++state.kernel_elements;
        const Matrix matrix = matrix_from_raw(raw);
        const Field re = real_part(matrix.a);
        const long double abs_re = abs_trace_half(matrix);
        const bool dangerous = dangerous_trace(matrix);
        if (dangerous) ++state.dangerous_elements;
        if (abs_re < state.minimum_abs_trace_half) {
          state.minimum_abs_trace_half = abs_re;
          state.minimum_record_index = record_index;
          state.minimum_depth = depth;
          state.minimum_word_high = high;
          state.minimum_word_low = low;
        }
        const long double length_over_a = 2.0L * std::acosh(abs_re) / a_over_r;
        candidates << record_index << '\t' << static_cast<unsigned>(depth) << '\t'
                   << hex_u64(high) << '\t' << hex_u64(low);
        for (std::size_t i = 0; i < 4; ++i) candidates << '\t' << re.c[i];
        candidates << '\t' << static_cast<unsigned>(re.exp) << '\t' << abs_re << '\t'
                   << length_over_a << '\t' << (dangerous ? 1 : 0) << '\n';
      }
    }
    if (state.scanned_records == next_commit || state.scanned_records == total) {
      candidates.flush();
      if (!candidates) throw std::runtime_error("candidate flush failed");
      state.candidate_file_bytes = fs::file_size(candidate_path);
      const auto now = std::chrono::steady_clock::now();
      state.elapsed_seconds += std::chrono::duration<double>(now - interval_started).count();
      interval_started = now;
      state.complete = state.scanned_records == total;
      write_scan_checkpoint(checkpoint_path, state);
      std::cout << "scanned=" << state.scanned_records << '/' << total
                << " kernel=" << state.kernel_elements
                << " dangerous=" << state.dangerous_elements
                << " components=" << state.component_evaluations << '\n' << std::flush;
      next_commit = std::min(total, next_commit + kCommitRecords);
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 4) throw std::runtime_error("usage: REGISTRY CHECKPOINT CANDIDATES");
    scan(argv[1], argv[2], argv[3]);
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 2;
  }
}
