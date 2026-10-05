#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>

#define CM_GEO7_NO_MAIN
#include "external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {
constexpr std::uint64_t kCommitRecords = 1'000'000;
constexpr std::uint32_t kExactCutoffMarker = std::numeric_limits<std::uint32_t>::max();
constexpr std::array<long double, 4> kCutoffs{{2.5L, 3.0L, 3.5L, 4.0L}};
constexpr long double kHeight = 0.5L;

struct State {
  std::uint64_t total = 0, scanned = 0;
  std::array<std::uint64_t, 4> counts{};
  std::array<long double, 4> minimum_abs_cosh_gap{{
      std::numeric_limits<long double>::infinity(), std::numeric_limits<long double>::infinity(),
      std::numeric_limits<long double>::infinity(), std::numeric_limits<long double>::infinity()}};
  double elapsed_seconds = 0.0;
  bool complete = false;
};

std::map<std::string, std::string> read_values(const std::filesystem::path& path) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot read checkpoint");
  std::map<std::string, std::string> values;
  std::string line;
  while (std::getline(in, line)) {
    const auto tab = line.find('\t');
    if (tab != std::string::npos) values[line.substr(0, tab)] = line.substr(tab + 1);
  }
  return values;
}

State read_state(const std::filesystem::path& path) {
  const auto v = read_values(path);
  State s;
  s.total = std::stoull(v.at("total_records"));
  s.scanned = std::stoull(v.at("scanned_records"));
  for (std::size_t i = 0; i < kCutoffs.size(); ++i) {
    const auto tag = std::to_string(static_cast<int>(2 * kCutoffs[i]));
    s.counts[i] = std::stoull(v.at("count_Dc_half_units_" + tag));
    s.minimum_abs_cosh_gap[i] = std::stold(v.at("minimum_abs_cosh_gap_Dc_half_units_" + tag));
  }
  s.elapsed_seconds = std::stod(v.at("elapsed_seconds"));
  s.complete = v.at("complete") == "1";
  return s;
}

void write_state(const std::filesystem::path& path, const State& s,
                 const std::array<long double, 4>& planar,
                 const std::array<long double, 4>& cosh_cutoff) {
  const auto temporary = path.string() + ".tmp";
  std::ofstream out(temporary, std::ios::trunc);
  if (!out) throw std::runtime_error("cannot write checkpoint temporary");
  out << std::setprecision(25) << "schema_version\t1.0\n"
      << "algorithm\tfull_exact_registry_numeric_cutoff_count\n"
      << "height_over_a_B\t" << kHeight << '\n'
      << "total_records\t" << s.total << '\n'
      << "scanned_records\t" << s.scanned << '\n';
  for (std::size_t i = 0; i < kCutoffs.size(); ++i) {
    const auto tag = std::to_string(static_cast<int>(2 * kCutoffs[i]));
    out << "Dc_over_a_B_half_units_" << tag << '\t' << kCutoffs[i] << '\n'
        << "planar_radius_over_a_B_half_units_" << tag << '\t' << planar[i] << '\n'
        << "cosh_cutoff_half_units_" << tag << '\t' << cosh_cutoff[i] << '\n'
        << "count_Dc_half_units_" << tag << '\t' << s.counts[i] << '\n'
        << "minimum_abs_cosh_gap_Dc_half_units_" << tag << '\t' << s.minimum_abs_cosh_gap[i] << '\n';
  }
  out << "elapsed_seconds\t" << std::setprecision(17) << s.elapsed_seconds << '\n'
      << "complete\t" << (s.complete ? 1 : 0) << '\n';
  out.close();
  if (!out) throw std::runtime_error("checkpoint write failed");
  if (std::filesystem::exists(path)) std::filesystem::remove(path);
  std::filesystem::rename(temporary, path);
}

void scan(const std::filesystem::path& registry, const std::filesystem::path& checkpoint) {
  std::ifstream input(registry, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open exact ball registry");
  static std::array<char, 16 * 1024 * 1024> buffer{};
  input.rdbuf()->pubsetbuf(buffer.data(), static_cast<std::streamsize>(buffer.size()));
  char magic[8]{};
  input.read(magic, 8);
  if (std::string(magic, 8) != "BOLZGEO1") throw std::runtime_error("bad registry magic");
  const std::uint64_t total = read_u64(input);
  if (read_u32(input) != kGeoRecordBytes) throw std::runtime_error("bad record size");
  if (read_u32(input) != kExactCutoffMarker) throw std::runtime_error("wrong cutoff marker");
  const long double root2 = std::sqrt(2.0L);
  const long double a_over_R = 2.0L * std::acosh(1.0L + root2);
  std::array<long double, 4> planar{}, cosh_cutoff{};
  for (std::size_t i = 0; i < kCutoffs.size(); ++i) {
    planar[i] = std::sqrt(kCutoffs[i] * kCutoffs[i] - kHeight * kHeight);
    cosh_cutoff[i] = std::cosh(planar[i] * a_over_R);
  }
  State state;
  if (std::filesystem::exists(checkpoint)) {
    state = read_state(checkpoint);
    if (state.total != total) throw std::runtime_error("checkpoint registry count drift");
  } else {
    state.total = total;
    write_state(checkpoint, state, planar, cosh_cutoff);
  }
  if (state.complete) return;
  input.seekg(static_cast<std::streamoff>(24ULL + state.scanned * kGeoRecordBytes));
  auto interval_started = std::chrono::steady_clock::now();
  std::uint64_t next_commit = std::min(total, ((state.scanned / kCommitRecords) + 1) * kCommitRecords);
  while (state.scanned < total) {
    const GeoRecord record = geo_read_record(input);
    if (!input) throw std::runtime_error("short registry record");
    ++state.scanned;
    const long double real = geo_field_value_real(record.key.a);
    const long double imag = geo_field_value_imag(record.key.a);
    const long double displacement_cosh = 2.0L * (real * real + imag * imag) - 1.0L;
    for (std::size_t i = 0; i < kCutoffs.size(); ++i) {
      state.minimum_abs_cosh_gap[i] = std::min(
          state.minimum_abs_cosh_gap[i], std::fabs(displacement_cosh - cosh_cutoff[i]));
      if (displacement_cosh <= cosh_cutoff[i]) ++state.counts[i];
    }
    if (state.scanned == next_commit || state.scanned == total) {
      const auto now = std::chrono::steady_clock::now();
      state.elapsed_seconds += std::chrono::duration<double>(now - interval_started).count();
      interval_started = now;
      state.complete = state.scanned == total;
      write_state(checkpoint, state, planar, cosh_cutoff);
      std::cout << "scanned=" << state.scanned << '/' << total << " counts="
                << state.counts[0] << ',' << state.counts[1] << ','
                << state.counts[2] << ',' << state.counts[3] << '\n' << std::flush;
      next_commit = std::min(total, next_commit + kCommitRecords);
    }
  }
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 3) throw std::runtime_error("usage: REGISTRY CHECKPOINT");
    scan(argv[1], argv[2]);
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 2;
  }
}
