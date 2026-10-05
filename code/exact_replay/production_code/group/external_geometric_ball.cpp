#include <gmp.h>

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
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

// Reuse the accepted CM-GRP-EXT-001 exact Bolza field, PSU key, generator,
// multiplication, binary-key, hash, and peak-RSS implementation.  Renaming
// its command-line entry point keeps this translation unit mechanically tied
// to the frozen identity convention without creating a second algebra layer.
#define main cm_grp_ext_001_embedded_main
#include "external_group_ball.cpp"
#undef main

namespace {

constexpr std::uint32_t kGeoRecordBytes = 147;
constexpr std::uint32_t kGeoMaximumDepth = 42;
constexpr const char* kCheckpointName = "checkpoint.tsv";

struct GeoRecord {
  Matrix key;
  std::uint8_t depth = 0;
  std::uint64_t word_high = 0;
  std::uint64_t word_low = 0;
};

struct Checkpoint {
  int target_cutoff = 0;
  int flood_cutoff = 0;
  bool exact_q2_cutoff = false;
  std::int64_t exact_q2_p = 0;
  std::int64_t exact_q2_q = 0;
  std::string cutoff_label = "integral_multiple_of_a_B";
  int completed_depth = 0;
  std::uint64_t visited = 0;
  std::uint64_t frontier = 0;
  std::uint64_t candidate_emissions = 0;
  std::uint64_t duplicate_emissions = 0;
  std::uint64_t exact_boundary_fallbacks = 0;
  double elapsed_seconds = 0.0;
  std::uint64_t peak_rss_bytes = 0;
  bool complete = false;
  std::vector<std::uint64_t> shell_counts;
  std::vector<std::uint64_t> candidate_counts_by_depth;
  std::vector<std::uint64_t> duplicate_counts_by_depth;
};

std::vector<std::uint64_t> parse_u64_list(const std::string& text) {
  std::vector<std::uint64_t> values;
  if (text.empty()) return values;
  std::size_t start = 0;
  while (start <= text.size()) {
    const auto comma = text.find(',', start);
    values.push_back(std::stoull(text.substr(start, comma == std::string::npos ? comma : comma - start)));
    if (comma == std::string::npos) break;
    start = comma + 1;
  }
  return values;
}

std::string join_u64_list(const std::vector<std::uint64_t>& values) {
  std::ostringstream out;
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (i) out << ',';
    out << values[i];
  }
  return out.str();
}

std::string depth_name(int depth) {
  std::ostringstream out;
  out << "depth-" << std::setw(3) << std::setfill('0') << depth;
  return out.str();
}

fs::path state_path(const fs::path& root, int depth) {
  return root / "state" / depth_name(depth);
}

void geo_write_record(std::ostream& out, const GeoRecord& record) {
  write_key(out, record.key);
  out.put(static_cast<char>(record.depth));
  write_u64(out, record.word_high);
  write_u64(out, record.word_low);
}

GeoRecord geo_read_record(std::istream& in) {
  GeoRecord record;
  record.key = read_key(in);
  if (!in) return record;
  record.depth = static_cast<std::uint8_t>(in.get());
  record.word_high = read_u64(in);
  record.word_low = read_u64(in);
  return record;
}

bool geo_word_less(const GeoRecord& x, const GeoRecord& y) {
  if (x.depth != y.depth) return x.depth < y.depth;
  if (x.word_high != y.word_high) return x.word_high < y.word_high;
  return x.word_low < y.word_low;
}

bool geo_record_less(const GeoRecord& x, const GeoRecord& y) {
  const int key_comparison = compare_matrix(x.key, y.key);
  return key_comparison ? key_comparison < 0 : geo_word_less(x, y);
}

GeoRecord append_generator(const GeoRecord& parent, int generator_index) {
  if (parent.depth >= kGeoMaximumDepth) fail("transport word exceeds 126-bit capacity");
  GeoRecord child;
  child.key = projective_key(matrix_multiply(parent.key, generator(generator_index)));
  child.depth = static_cast<std::uint8_t>(parent.depth + 1);
  if ((parent.word_high >> 61U) != 0) fail("transport word shift overflow");
  child.word_high = (parent.word_high << 3U) | (parent.word_low >> 61U);
  child.word_low = (parent.word_low << 3U) | static_cast<std::uint64_t>(generator_index);
  return child;
}

long double geo_field_value_real(const Field& value) {
  const long double root2 = std::sqrt(2.0L);
  const long double beta = std::sqrt(2.0L + 2.0L * root2);
  const std::array<long double, 4> basis{1.0L, root2, beta, root2 * beta};
  long double result = 0;
  for (std::size_t i = 0; i < 4; ++i) result += value.c[i] * basis[i];
  return std::ldexp(result, -static_cast<int>(value.exp));
}

long double geo_field_value_imag(const Field& value) {
  const long double root2 = std::sqrt(2.0L);
  const long double beta = std::sqrt(2.0L + 2.0L * root2);
  const std::array<long double, 4> basis{1.0L, root2, beta, root2 * beta};
  long double result = 0;
  for (std::size_t i = 0; i < 4; ++i) result += value.c[i + 4] * basis[i];
  return std::ldexp(result, -static_cast<int>(value.exp));
}

Field geo_exact_cosh_displacement(const Matrix& value) {
  const Field norm = multiply(value.a, conjugate(value.a));
  return add(add(norm, norm), negate(one()));
}

void geo_mpz_set_i64_exact(mpz_t target, std::int64_t value) {
  const bool negative = value < 0;
  const std::uint64_t magnitude = negative
      ? static_cast<std::uint64_t>(-(value + 1)) + 1U
      : static_cast<std::uint64_t>(value);
  mpz_import(target, 1, -1, sizeof(magnitude), 0, 0, &magnitude);
  if (negative) mpz_neg(target, target);
}

int geo_sign_q2(const mpz_t p, const mpz_t q) {
  const int sp = mpz_sgn(p), sq = mpz_sgn(q);
  if (sq == 0) return sp;
  if (sp == 0) return sq;
  if (sp == sq) return sp;
  mpz_t p2, q2, delta;
  mpz_inits(p2, q2, delta, nullptr);
  mpz_mul(p2, p, p);
  mpz_mul(q2, q, q);
  mpz_mul_ui(q2, q2, 2);
  mpz_sub(delta, p2, q2);
  const int sd = mpz_sgn(delta);
  mpz_clears(p2, q2, delta, nullptr);
  if (sd == 0) fail("unexpected rational equality to sqrt(2)");
  return sp > 0 ? sd : -sd;
}

int geo_exact_real_field_sign(const Field& value) {
  for (std::size_t i = 4; i < 8; ++i) {
    if (value.c[i] != 0) fail("sign requested for non-real algebraic value");
  }
  mpz_t p, q, r, s;
  mpz_inits(p, q, r, s, nullptr);
  geo_mpz_set_i64_exact(p, value.c[0]);
  geo_mpz_set_i64_exact(q, value.c[1]);
  geo_mpz_set_i64_exact(r, value.c[2]);
  geo_mpz_set_i64_exact(s, value.c[3]);
  const int sa = geo_sign_q2(p, q), sb = geo_sign_q2(r, s);
  if (sb == 0 || sa == 0 || sa == sb) {
    const int answer = sb == 0 ? sa : (sa == 0 ? sb : sa);
    mpz_clears(p, q, r, s, nullptr);
    return answer;
  }

  mpz_t a0, a1, b0, b1, delta0, delta1, temporary;
  mpz_inits(a0, a1, b0, b1, delta0, delta1, temporary, nullptr);
  mpz_mul(a0, p, p);
  mpz_mul(temporary, q, q);
  mpz_mul_ui(temporary, temporary, 2);
  mpz_add(a0, a0, temporary);
  mpz_mul(a1, p, q);
  mpz_mul_ui(a1, a1, 2);
  mpz_mul(b0, r, r);
  mpz_mul(temporary, s, s);
  mpz_mul_ui(temporary, temporary, 2);
  mpz_add(b0, b0, temporary);
  mpz_mul(b1, r, s);
  mpz_mul_ui(b1, b1, 2);
  mpz_mul_ui(delta0, b0, 2);
  mpz_mul_ui(temporary, b1, 4);
  mpz_add(delta0, delta0, temporary);
  mpz_sub(delta0, a0, delta0);
  mpz_mul_ui(delta1, b0, 2);
  mpz_mul_ui(temporary, b1, 2);
  mpz_add(delta1, delta1, temporary);
  mpz_sub(delta1, a1, delta1);
  const int dominance = geo_sign_q2(delta0, delta1);
  mpz_clears(p, q, r, s, a0, a1, b0, b1, delta0, delta1, temporary, nullptr);
  if (dominance == 0) fail("unexpected beta-extension sign degeneracy");
  return dominance > 0 ? sa : sb;
}

Field geo_cutoff_cosh_exact(int cutoff_over_a) {
  if (cutoff_over_a < 0 || cutoff_over_a > 12) fail("unsupported integral cutoff");
  Q2 x{1, 1};
  Q2 t0{1, 0}, t1 = x;
  const int degree = 2 * cutoff_over_a;
  if (degree == 0) return one();
  for (int k = 2; k <= degree; ++k) {
    const auto product = q2_mul(x, t1);
    Q2 next{2 * product[0] - t0[0], 2 * product[1] - t0[1]};
    t0 = t1;
    t1 = next;
  }
  return field_from({checked_i64(t1[0]), checked_i64(t1[1]), 0, 0, 0, 0, 0, 0});
}

bool geo_inside_cutoff(const Matrix& value, const Field& exact_cutoff,
                       long double numeric_cutoff, std::uint64_t& exact_fallbacks) {
  const long double real = geo_field_value_real(value.a);
  const long double imag = geo_field_value_imag(value.a);
  const long double numeric = 2.0L * (real * real + imag * imag) - 1.0L;
  const long double scale = std::max({1.0L, std::fabs(numeric), std::fabs(numeric_cutoff)});
  const long double guard = 256.0L * std::numeric_limits<long double>::epsilon() * scale;
  if (numeric < numeric_cutoff - guard) return true;
  if (numeric > numeric_cutoff + guard) return false;
  ++exact_fallbacks;
  const Field delta = add(geo_exact_cosh_displacement(value), negate(exact_cutoff));
  return geo_exact_real_field_sign(delta) <= 0;
}

std::map<std::string, std::string> read_key_values(const fs::path& path) {
  std::ifstream in(path);
  if (!in) fail("cannot read checkpoint: " + path.string());
  std::map<std::string, std::string> values;
  std::string line;
  while (std::getline(in, line)) {
    const auto tab = line.find('\t');
    if (tab != std::string::npos) values[line.substr(0, tab)] = line.substr(tab + 1);
  }
  return values;
}

Checkpoint read_checkpoint(const fs::path& root) {
  const auto values = read_key_values(root / kCheckpointName);
  Checkpoint result;
  result.target_cutoff = std::stoi(values.at("target_cutoff_over_a_B"));
  result.flood_cutoff = std::stoi(values.at("flood_cutoff_over_a_B"));
  if (const auto it = values.find("cutoff_kind"); it != values.end()) {
    result.exact_q2_cutoff = it->second == "exact_Q_sqrt2_cosh";
  }
  if (const auto it = values.find("cutoff_q2_p"); it != values.end()) result.exact_q2_p = std::stoll(it->second);
  if (const auto it = values.find("cutoff_q2_q"); it != values.end()) result.exact_q2_q = std::stoll(it->second);
  if (const auto it = values.find("cutoff_label"); it != values.end()) result.cutoff_label = it->second;
  result.completed_depth = std::stoi(values.at("completed_depth"));
  result.visited = std::stoull(values.at("visited_elements"));
  result.frontier = std::stoull(values.at("frontier_elements"));
  result.candidate_emissions = std::stoull(values.at("candidate_emissions"));
  result.duplicate_emissions = std::stoull(values.at("duplicate_emissions"));
  result.exact_boundary_fallbacks = std::stoull(values.at("exact_boundary_fallbacks"));
  result.elapsed_seconds = std::stod(values.at("elapsed_seconds"));
  result.peak_rss_bytes = std::stoull(values.at("peak_rss_bytes"));
  result.complete = values.at("complete") == "1";
  result.shell_counts = parse_u64_list(values.at("shell_counts"));
  result.candidate_counts_by_depth = parse_u64_list(values.at("candidate_counts_by_depth"));
  result.duplicate_counts_by_depth = parse_u64_list(values.at("duplicate_counts_by_depth"));
  return result;
}

void write_checkpoint(const fs::path& root, const Checkpoint& value) {
  const fs::path final_path = root / kCheckpointName;
  const fs::path temporary = root / "checkpoint.tmp";
  std::ofstream out(temporary, std::ios::trunc);
  if (!out) fail("cannot write temporary checkpoint");
  out << "schema_version\t1.0\n"
      << "algorithm\texternal_exact_dirichlet_voronoi_center_flood\n"
      << "target_cutoff_over_a_B\t" << value.target_cutoff << '\n'
      << "flood_cutoff_over_a_B\t" << value.flood_cutoff << '\n'
      << "cutoff_kind\t" << (value.exact_q2_cutoff ? "exact_Q_sqrt2_cosh" : "integral_multiple_of_a_B") << '\n'
      << "cutoff_q2_p\t" << value.exact_q2_p << '\n'
      << "cutoff_q2_q\t" << value.exact_q2_q << '\n'
      << "cutoff_label\t" << value.cutoff_label << '\n'
      << "completed_depth\t" << value.completed_depth << '\n'
      << "visited_elements\t" << value.visited << '\n'
      << "frontier_elements\t" << value.frontier << '\n'
      << "candidate_emissions\t" << value.candidate_emissions << '\n'
      << "duplicate_emissions\t" << value.duplicate_emissions << '\n'
      << "exact_boundary_fallbacks\t" << value.exact_boundary_fallbacks << '\n'
      << "elapsed_seconds\t" << std::setprecision(17) << value.elapsed_seconds << '\n'
      << "peak_rss_bytes\t" << value.peak_rss_bytes << '\n'
      << "complete\t" << (value.complete ? 1 : 0) << '\n'
      << "shell_counts\t" << join_u64_list(value.shell_counts) << '\n'
      << "candidate_counts_by_depth\t" << join_u64_list(value.candidate_counts_by_depth) << '\n'
      << "duplicate_counts_by_depth\t" << join_u64_list(value.duplicate_counts_by_depth) << '\n';
  out.close();
  if (!out) fail("checkpoint write failed");
  if (fs::exists(final_path)) fs::remove(final_path);
  fs::rename(temporary, final_path);
}

std::uint64_t checked_record_count(const fs::path& path) {
  if (!fs::exists(path)) fail("missing record file: " + path.string());
  const auto bytes = fs::file_size(path);
  if (bytes % kGeoRecordBytes) fail("corrupt record byte count: " + path.string());
  return bytes / kGeoRecordBytes;
}

void create_empty_buckets(const fs::path& directory) {
  fs::create_directories(directory);
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    std::ofstream out(directory / bucket_name(bucket), std::ios::binary | std::ios::trunc);
    if (!out) fail("cannot create bucket");
  }
}

void initialize_mode(int target_cutoff, int flood_cutoff, const fs::path& root) {
  if (target_cutoff < 0 || flood_cutoff < target_cutoff || flood_cutoff > 12) fail("bad cutoffs");
  if (fs::exists(root / kCheckpointName)) fail("checkpoint already exists");
  fs::create_directories(root / "state");
  const fs::path state = state_path(root, 0);
  create_empty_buckets(state / "visited");
  create_empty_buckets(state / "frontier");
  const GeoRecord identity{projective_key(identity_matrix()), 0, 0, 0};
  const int bucket = static_cast<int>(hash_matrix(identity.key) & (kBuckets - 1));
  for (const auto& part : {"visited", "frontier"}) {
    std::ofstream out(state / part / bucket_name(bucket), std::ios::binary | std::ios::app);
    geo_write_record(out, identity);
  }
  std::ofstream manifest(state / "generation.tsv", std::ios::trunc);
  manifest << "depth\t0\nfrontier\t1\nvisited\t1\ncomplete\t1\n";
  Checkpoint checkpoint;
  checkpoint.target_cutoff = target_cutoff;
  checkpoint.flood_cutoff = flood_cutoff;
  checkpoint.completed_depth = 0;
  checkpoint.visited = 1;
  checkpoint.frontier = 1;
  checkpoint.peak_rss_bytes = peak_rss();
  checkpoint.shell_counts = {1};
  write_checkpoint(root, checkpoint);
}

void initialize_exact_q2_mode(std::int64_t cutoff_p, std::int64_t cutoff_q,
                              const std::string& label, const fs::path& root) {
  if (cutoff_p <= 1 || cutoff_q < 0) fail("bad exact Q(sqrt(2)) cutoff");
  if (label.empty() || label.find_first_of("\t\r\n") != std::string::npos) fail("bad cutoff label");
  if (fs::exists(root / kCheckpointName)) fail("checkpoint already exists");
  fs::create_directories(root / "state");
  const fs::path state = state_path(root, 0);
  create_empty_buckets(state / "visited");
  create_empty_buckets(state / "frontier");
  const GeoRecord identity{projective_key(identity_matrix()), 0, 0, 0};
  const int bucket = static_cast<int>(hash_matrix(identity.key) & (kBuckets - 1));
  for (const auto& part : {"visited", "frontier"}) {
    std::ofstream out(state / part / bucket_name(bucket), std::ios::binary | std::ios::app);
    geo_write_record(out, identity);
  }
  std::ofstream manifest(state / "generation.tsv", std::ios::trunc);
  manifest << "depth\t0\nfrontier\t1\nvisited\t1\ncomplete\t1\n";
  Checkpoint checkpoint;
  checkpoint.target_cutoff = -1;
  checkpoint.flood_cutoff = -1;
  checkpoint.exact_q2_cutoff = true;
  checkpoint.exact_q2_p = cutoff_p;
  checkpoint.exact_q2_q = cutoff_q;
  checkpoint.cutoff_label = label;
  checkpoint.completed_depth = 0;
  checkpoint.visited = 1;
  checkpoint.frontier = 1;
  checkpoint.peak_rss_bytes = peak_rss();
  checkpoint.shell_counts = {1};
  write_checkpoint(root, checkpoint);
}

struct ReductionCounts {
  std::uint64_t raw = 0;
  std::uint64_t candidate_unique = 0;
  std::uint64_t unseen = 0;
  std::uint64_t visited_output = 0;
};

ReductionCounts reduce_bucket(const fs::path& candidate_path,
                              const fs::path& visited_path,
                              const fs::path& next_frontier_path,
                              const fs::path& next_visited_path,
                              int expected_bucket) {
  ReductionCounts counts;
  counts.raw = checked_record_count(candidate_path);
  std::vector<GeoRecord> candidates(static_cast<std::size_t>(counts.raw));
  {
    std::ifstream input(candidate_path, std::ios::binary);
    for (auto& record : candidates) {
      record = geo_read_record(input);
      if (!input) fail("short candidate record");
      if (static_cast<int>(hash_matrix(record.key) & (kBuckets - 1)) != expected_bucket) fail("candidate bucket mismatch");
    }
  }
  std::sort(candidates.begin(), candidates.end(), geo_record_less);
  std::vector<GeoRecord> unique;
  unique.reserve(candidates.size());
  for (std::size_t i = 0; i < candidates.size();) {
    unique.push_back(candidates[i]);
    std::size_t j = i + 1;
    while (j < candidates.size() && candidates[j].key == candidates[i].key) ++j;
    i = j;
  }
  counts.candidate_unique = unique.size();
  candidates.clear();
  candidates.shrink_to_fit();

  std::ifstream visited(visited_path, std::ios::binary);
  if (!visited) fail("cannot open visited bucket");
  std::ofstream next_frontier(next_frontier_path, std::ios::binary | std::ios::trunc);
  std::ofstream next_visited(next_visited_path, std::ios::binary | std::ios::trunc);
  if (!next_frontier || !next_visited) fail("cannot open reduction outputs");

  const auto visited_count = checked_record_count(visited_path);
  std::uint64_t visited_index = 0;
  GeoRecord old;
  bool have_old = false;
  auto advance_old = [&]() {
    if (visited_index >= visited_count) { have_old = false; return; }
    old = geo_read_record(visited);
    if (!visited) fail("short visited record");
    ++visited_index;
    have_old = true;
  };
  advance_old();
  std::size_t candidate_index = 0;
  while (have_old || candidate_index < unique.size()) {
    if (!have_old) {
      const auto& value = unique[candidate_index++];
      geo_write_record(next_frontier, value);
      geo_write_record(next_visited, value);
      ++counts.unseen;
      ++counts.visited_output;
      continue;
    }
    if (candidate_index >= unique.size()) {
      geo_write_record(next_visited, old);
      ++counts.visited_output;
      advance_old();
      continue;
    }
    const int comparison = compare_matrix(old.key, unique[candidate_index].key);
    if (comparison < 0) {
      geo_write_record(next_visited, old);
      ++counts.visited_output;
      advance_old();
    } else if (comparison > 0) {
      const auto& value = unique[candidate_index++];
      geo_write_record(next_frontier, value);
      geo_write_record(next_visited, value);
      ++counts.unseen;
      ++counts.visited_output;
    } else {
      geo_write_record(next_visited, old);
      ++counts.visited_output;
      ++candidate_index;
      advance_old();
    }
  }
  return counts;
}

void step_mode(const fs::path& root) {
  Checkpoint checkpoint = read_checkpoint(root);
  if (checkpoint.complete) return;
  const auto started = std::chrono::steady_clock::now();
  const int next_depth = checkpoint.completed_depth + 1;
  const fs::path current = state_path(root, checkpoint.completed_depth);
  if (!fs::exists(current / "generation.tsv")) fail("current state is not committed");
  const fs::path candidates = root / "candidate.tmp";
  const fs::path next_temporary = root / "state.tmp";
  if (fs::exists(candidates)) fs::remove_all(candidates);
  if (fs::exists(next_temporary)) fs::remove_all(next_temporary);
  create_empty_buckets(candidates);
  fs::create_directories(next_temporary / "visited");
  fs::create_directories(next_temporary / "frontier");

  std::vector<std::ofstream> candidate_outputs;
  candidate_outputs.reserve(kBuckets);
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    candidate_outputs.emplace_back(candidates / bucket_name(bucket), std::ios::binary | std::ios::app);
    if (!candidate_outputs.back()) fail("cannot open candidate output");
  }
  const Field exact_cutoff = checkpoint.exact_q2_cutoff
      ? field_from({checkpoint.exact_q2_p, checkpoint.exact_q2_q, 0, 0, 0, 0, 0, 0})
      : geo_cutoff_cosh_exact(checkpoint.flood_cutoff);
  const long double root2 = std::sqrt(2.0L);
  const long double a_over_R = 2.0L * std::acosh(1.0L + root2);
  const long double numeric_cutoff = checkpoint.exact_q2_cutoff
      ? static_cast<long double>(checkpoint.exact_q2_p)
          + static_cast<long double>(checkpoint.exact_q2_q) * root2
      : std::cosh(checkpoint.flood_cutoff * a_over_R);
  std::uint64_t emitted_this_depth = 0;
  std::uint64_t fallbacks_this_depth = 0;
  for (int source_bucket = 0; source_bucket < kBuckets; ++source_bucket) {
    const fs::path path = current / "frontier" / bucket_name(source_bucket);
    const auto count = checked_record_count(path);
    std::ifstream input(path, std::ios::binary);
    for (std::uint64_t i = 0; i < count; ++i) {
      const GeoRecord parent = geo_read_record(input);
      if (!input) fail("short frontier record");
      for (int generator_index = 0; generator_index < kGenerators; ++generator_index) {
        GeoRecord child = append_generator(parent, generator_index);
        if (!geo_inside_cutoff(child.key, exact_cutoff, numeric_cutoff, fallbacks_this_depth)) continue;
        const int bucket = static_cast<int>(hash_matrix(child.key) & (kBuckets - 1));
        geo_write_record(candidate_outputs[bucket], child);
        ++emitted_this_depth;
      }
    }
  }
  for (auto& output : candidate_outputs) output.close();

  ReductionCounts total;
  std::ofstream bucket_manifest(next_temporary / "bucket_reduction.tsv", std::ios::trunc);
  bucket_manifest << "bucket\traw\tcandidate_unique\tunseen\tvisited_output\n";
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const auto counts = reduce_bucket(
        candidates / bucket_name(bucket),
        current / "visited" / bucket_name(bucket),
        next_temporary / "frontier" / bucket_name(bucket),
        next_temporary / "visited" / bucket_name(bucket), bucket);
    bucket_manifest << bucket << '\t' << counts.raw << '\t' << counts.candidate_unique
                    << '\t' << counts.unseen << '\t' << counts.visited_output << '\n';
    total.raw += counts.raw;
    total.candidate_unique += counts.candidate_unique;
    total.unseen += counts.unseen;
    total.visited_output += counts.visited_output;
  }
  if (total.raw != emitted_this_depth) fail("candidate emission/reduction count mismatch");
  if (total.visited_output != checkpoint.visited + total.unseen) fail("visited merge count mismatch");
  bucket_manifest << "TOTAL\t" << total.raw << '\t' << total.candidate_unique
                  << '\t' << total.unseen << '\t' << total.visited_output << '\n';
  bucket_manifest.close();

  std::ofstream generation(next_temporary / "generation.tsv", std::ios::trunc);
  generation << "depth\t" << next_depth << '\n'
             << "candidate_emissions\t" << total.raw << '\n'
             << "candidate_unique\t" << total.candidate_unique << '\n'
             << "new_frontier\t" << total.unseen << '\n'
             << "visited\t" << total.visited_output << '\n'
             << "exact_boundary_fallbacks\t" << fallbacks_this_depth << '\n'
             << "complete\t1\n";
  generation.close();

  const fs::path next_final = state_path(root, next_depth);
  if (fs::exists(next_final)) fail("next committed state already exists");
  fs::rename(next_temporary, next_final);
  const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
  checkpoint.completed_depth = next_depth;
  checkpoint.visited = total.visited_output;
  checkpoint.frontier = total.unseen;
  checkpoint.candidate_emissions += total.raw;
  checkpoint.duplicate_emissions += total.raw - total.unseen;
  checkpoint.exact_boundary_fallbacks += fallbacks_this_depth;
  checkpoint.elapsed_seconds += elapsed;
  checkpoint.peak_rss_bytes = std::max(checkpoint.peak_rss_bytes, peak_rss());
  checkpoint.complete = total.unseen == 0;
  checkpoint.shell_counts.push_back(total.unseen);
  checkpoint.candidate_counts_by_depth.push_back(total.raw);
  checkpoint.duplicate_counts_by_depth.push_back(total.raw - total.unseen);
  write_checkpoint(root, checkpoint);

  // A committed next-state plus atomic checkpoint is the deletion certificate
  // for the transient candidates and superseded previous state.
  fs::remove_all(candidates);
  if (current != next_final) fs::remove_all(current);
  std::cout << "completed_depth=" << next_depth << " new=" << total.unseen
            << " total=" << total.visited_output << " emitted=" << total.raw
            << " seconds=" << elapsed << '\n';
}

void finalize_mode(const fs::path& root, const fs::path& registry_path,
                   const fs::path& summary_path) {
  const Checkpoint checkpoint = read_checkpoint(root);
  if (!checkpoint.complete || checkpoint.frontier != 0) fail("cannot finalize incomplete flood");
  const fs::path state = state_path(root, checkpoint.completed_depth);
  if (registry_path.has_parent_path()) fs::create_directories(registry_path.parent_path());
  std::ofstream output(registry_path, std::ios::binary | std::ios::trunc);
  output.write("BOLZGEO1", 8);
  write_u64(output, checkpoint.visited);
  write_u32(output, kGeoRecordBytes);
  write_u32(output, checkpoint.exact_q2_cutoff
      ? std::numeric_limits<std::uint32_t>::max()
      : static_cast<std::uint32_t>(checkpoint.target_cutoff));
  std::uint64_t copied = 0;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path path = state / "visited" / bucket_name(bucket);
    const auto count = checked_record_count(path);
    std::ifstream input(path, std::ios::binary);
    std::vector<char> buffer(8U * 1024U * 1024U);
    while (input) {
      input.read(buffer.data(), static_cast<std::streamsize>(buffer.size()));
      const auto bytes = input.gcount();
      if (bytes > 0) output.write(buffer.data(), bytes);
    }
    copied += count;
  }
  if (copied != checkpoint.visited) fail("final registry count mismatch");
  output.close();
  std::ofstream summary(summary_path, std::ios::trunc);
  summary << "schema_version\t1.0\n"
          << "scope\texact_closed_geometric_ball\n"
          << "target_cutoff_over_a_B\t" << checkpoint.target_cutoff << '\n'
          << "flood_cutoff_over_a_B\t" << checkpoint.flood_cutoff << '\n'
          << "cutoff_kind\t" << (checkpoint.exact_q2_cutoff ? "exact_Q_sqrt2_cosh" : "integral_multiple_of_a_B") << '\n'
          << "cutoff_q2_p\t" << checkpoint.exact_q2_p << '\n'
          << "cutoff_q2_q\t" << checkpoint.exact_q2_q << '\n'
          << "cutoff_label\t" << checkpoint.cutoff_label << '\n'
          << "flood_generations\t" << checkpoint.completed_depth << '\n'
          << "candidate_emissions\t" << checkpoint.candidate_emissions << '\n'
          << "duplicate_emissions\t" << checkpoint.duplicate_emissions << '\n'
          << "target_unique_elements\t" << checkpoint.visited << '\n'
          << "frontier_exhausted\t1\n"
          << "exact_boundary_fallbacks\t" << checkpoint.exact_boundary_fallbacks << '\n'
          << "peak_rss_bytes\t" << checkpoint.peak_rss_bytes << '\n'
          << "runtime_seconds\t" << std::setprecision(17) << checkpoint.elapsed_seconds << '\n'
          << "registry_record_bytes\t" << kGeoRecordBytes << '\n'
          << "shell_counts\t" << join_u64_list(checkpoint.shell_counts) << '\n'
          << "candidate_counts_by_depth\t" << join_u64_list(checkpoint.candidate_counts_by_depth) << '\n'
          << "duplicate_counts_by_depth\t" << join_u64_list(checkpoint.duplicate_counts_by_depth) << '\n';
}

std::vector<std::string> parse_csv_line(const std::string& line) {
  std::vector<std::string> fields;
  std::string current;
  bool quoted = false;
  for (std::size_t i = 0; i < line.size(); ++i) {
    const char ch = line[i];
    if (quoted) {
      if (ch == '"' && i + 1 < line.size() && line[i + 1] == '"') {
        current.push_back('"');
        ++i;
      } else if (ch == '"') {
        quoted = false;
      } else {
        current.push_back(ch);
      }
    } else if (ch == '"') {
      quoted = true;
    } else if (ch == ',') {
      fields.push_back(current);
      current.clear();
    } else {
      current.push_back(ch);
    }
  }
  fields.push_back(current);
  if (quoted) fail("unterminated CSV quote");
  return fields;
}

Field parse_field_string(const std::string& text) {
  const auto semicolon = text.find(';');
  if (semicolon == std::string::npos) fail("bad exact field string");
  const int exponent = std::stoi(text.substr(0, semicolon));
  std::array<std::int64_t, 8> coefficients{};
  std::size_t start = semicolon + 1;
  for (std::size_t i = 0; i < coefficients.size(); ++i) {
    const auto comma = text.find(',', start);
    const std::string token = text.substr(start, comma == std::string::npos ? comma : comma - start);
    coefficients[i] = std::stoll(token);
    if (i + 1 < coefficients.size() && comma == std::string::npos) fail("short exact field tuple");
    start = comma == std::string::npos ? text.size() : comma + 1;
  }
  return field_from(coefficients, exponent);
}

void compare_old_csv_mode(const fs::path& root, const fs::path& csv_path,
                          const fs::path& report_path) {
  const Checkpoint checkpoint = read_checkpoint(root);
  if (!checkpoint.complete) fail("comparison requires completed new flood");
  const fs::path old_buckets = root / "old_csv_compare.tmp";
  if (fs::exists(old_buckets)) fs::remove_all(old_buckets);
  create_empty_buckets(old_buckets);
  std::vector<std::ofstream> outputs;
  outputs.reserve(kBuckets);
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    outputs.emplace_back(old_buckets / bucket_name(bucket), std::ios::binary | std::ios::app);
  }
  const GeoRecord identity{projective_key(identity_matrix()), 0, 0, 0};
  geo_write_record(outputs[hash_matrix(identity.key) & (kBuckets - 1)], identity);
  std::ifstream csv(csv_path);
  if (!csv) fail("cannot open frozen CSV");
  std::string line;
  if (!std::getline(csv, line)) fail("frozen CSV is empty");
  std::uint64_t rows = 0;
  while (std::getline(csv, line)) {
    const auto fields = parse_csv_line(line);
    if (fields.size() < 6) fail("short frozen CSV row");
    GeoRecord record;
    record.key = projective_key(Matrix{parse_field_string(fields[3]), parse_field_string(fields[4])});
    record.depth = static_cast<std::uint8_t>(std::stoi(fields[5]));
    const int bucket = static_cast<int>(hash_matrix(record.key) & (kBuckets - 1));
    geo_write_record(outputs[bucket], record);
    ++rows;
  }
  for (auto& output : outputs) output.close();

  const fs::path state = state_path(root, checkpoint.completed_depth);
  std::uint64_t old_raw = rows + 1, old_unique = 0, new_count = 0;
  std::uint64_t missing_from_new = 0, missing_from_old = 0;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path old_path = old_buckets / bucket_name(bucket);
    const auto old_count = checked_record_count(old_path);
    std::vector<GeoRecord> old(static_cast<std::size_t>(old_count));
    {
      std::ifstream input(old_path, std::ios::binary);
      for (auto& record : old) record = geo_read_record(input);
    }
    std::sort(old.begin(), old.end(), geo_record_less);
    std::vector<GeoRecord> unique;
    for (std::size_t i = 0; i < old.size();) {
      unique.push_back(old[i]);
      std::size_t j = i + 1;
      while (j < old.size() && old[j].key == old[i].key) ++j;
      i = j;
    }
    old_unique += unique.size();
    const fs::path new_path = state / "visited" / bucket_name(bucket);
    const auto current_count = checked_record_count(new_path);
    new_count += current_count;
    std::ifstream current(new_path, std::ios::binary);
    std::uint64_t current_index = 0;
    GeoRecord value;
    bool have_value = false;
    auto advance = [&]() {
      if (current_index >= current_count) { have_value = false; return; }
      value = geo_read_record(current);
      ++current_index;
      have_value = true;
    };
    advance();
    std::size_t old_index = 0;
    while (have_value || old_index < unique.size()) {
      if (!have_value) { missing_from_new += unique.size() - old_index; break; }
      if (old_index >= unique.size()) { missing_from_old += current_count - current_index + 1; break; }
      const int comparison = compare_matrix(value.key, unique[old_index].key);
      if (comparison < 0) { ++missing_from_old; advance(); }
      else if (comparison > 0) { ++missing_from_new; ++old_index; }
      else { advance(); ++old_index; }
    }
  }
  const bool equal = missing_from_new == 0 && missing_from_old == 0 && old_unique == new_count;
  std::ofstream report(report_path, std::ios::trunc);
  report << "schema_version\t1.0\n"
         << "frozen_csv_rows_nonidentity\t" << rows << '\n'
         << "old_raw_including_identity\t" << old_raw << '\n'
         << "old_unique_projective_keys\t" << old_unique << '\n'
         << "new_unique_projective_keys\t" << new_count << '\n'
         << "old_keys_missing_from_new\t" << missing_from_new << '\n'
         << "new_keys_missing_from_old\t" << missing_from_old << '\n'
         << "exact_key_set_equal\t" << (equal ? 1 : 0) << '\n';
  report.close();
  fs::remove_all(old_buckets);
  if (!equal) fail("frozen/new exact key set mismatch");
}

}  // namespace

#ifndef CM_GEO7_NO_MAIN
int main(int argc, char** argv) {
  try {
    if (argc < 2) fail("mode required");
    const std::string mode = argv[1];
    if (mode == "init" && argc == 5) {
      initialize_mode(std::stoi(argv[2]), std::stoi(argv[3]), argv[4]);
    } else if (mode == "init-exact-q2" && argc == 6) {
      initialize_exact_q2_mode(std::stoll(argv[2]), std::stoll(argv[3]), argv[4], argv[5]);
    } else if (mode == "step" && argc == 3) {
      step_mode(argv[2]);
    } else if (mode == "finalize" && argc == 5) {
      finalize_mode(argv[2], argv[3], argv[4]);
    } else if (mode == "compare-old-csv" && argc == 5) {
      compare_old_csv_mode(argv[2], argv[3], argv[4]);
    } else {
      fail("usage: init TARGET FLOOD ROOT | init-exact-q2 P Q LABEL ROOT | step ROOT | finalize ROOT REGISTRY SUMMARY | compare-old-csv ROOT CSV REPORT");
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 2;
  }
}
#endif
