#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#define CM_GEO7_NO_MAIN
#include "external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {

Field post_zeta8() {
  return field_from({0, 1, 0, 0, 0, 1, 0, 0}, 1);
}

Matrix post_rotate_c8(Matrix value) {
  value.b = multiply(value.b, post_zeta8());
  return projective_key(value);
}

Matrix post_transform(const Matrix& value, const std::string& transform) {
  if (transform == "inverse") return projective_key(matrix_inverse(value));
  if (transform == "phi8") return post_rotate_c8(value);
  fail("unknown closure transform");
}

void post_stream_transform(const fs::path& input_buckets, const fs::path& temporary,
                           const std::string& transform, std::uint64_t expected_count) {
  if (fs::exists(temporary)) fs::remove_all(temporary);
  create_empty_buckets(temporary);
  std::vector<std::ofstream> outputs;
  outputs.reserve(kBuckets);
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    outputs.emplace_back(temporary / bucket_name(bucket), std::ios::binary | std::ios::app);
    if (!outputs.back()) fail("cannot open transform bucket");
  }
  std::uint64_t transformed = 0;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path path = input_buckets / bucket_name(bucket);
    const auto count = checked_record_count(path);
    std::ifstream input(path, std::ios::binary);
    for (std::uint64_t i = 0; i < count; ++i) {
      GeoRecord record = geo_read_record(input);
      if (!input) fail("short closure input record");
      record.key = post_transform(record.key, transform);
      const int destination = static_cast<int>(hash_matrix(record.key) & (kBuckets - 1));
      geo_write_record(outputs[destination], record);
      ++transformed;
    }
  }
  for (auto& output : outputs) output.close();
  if (transformed != expected_count) fail("closure transform count mismatch");
}

struct SetComparison {
  std::uint64_t transformed_raw = 0;
  std::uint64_t transformed_unique = 0;
  std::uint64_t input_count = 0;
  std::uint64_t input_missing_from_transform = 0;
  std::uint64_t transform_missing_from_input = 0;
};

SetComparison post_compare_transformed(const fs::path& input_buckets,
                                       const fs::path& transformed_buckets) {
  SetComparison result;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path transformed_path = transformed_buckets / bucket_name(bucket);
    const auto transformed_count = checked_record_count(transformed_path);
    result.transformed_raw += transformed_count;
    std::vector<GeoRecord> transformed(static_cast<std::size_t>(transformed_count));
    {
      std::ifstream input(transformed_path, std::ios::binary);
      for (auto& record : transformed) {
        record = geo_read_record(input);
        if (!input) fail("short transformed record");
      }
    }
    std::sort(transformed.begin(), transformed.end(), geo_record_less);
    std::vector<GeoRecord> unique;
    unique.reserve(transformed.size());
    for (std::size_t i = 0; i < transformed.size();) {
      unique.push_back(transformed[i]);
      std::size_t j = i + 1;
      while (j < transformed.size() && transformed[j].key == transformed[i].key) ++j;
      i = j;
    }
    result.transformed_unique += unique.size();

    const fs::path input_path = input_buckets / bucket_name(bucket);
    const auto input_count = checked_record_count(input_path);
    result.input_count += input_count;
    std::ifstream input(input_path, std::ios::binary);
    std::uint64_t input_index = 0;
    GeoRecord value;
    bool have_value = false;
    auto advance = [&]() {
      if (input_index >= input_count) { have_value = false; return; }
      value = geo_read_record(input);
      if (!input) fail("short closure reference record");
      ++input_index;
      have_value = true;
    };
    advance();
    std::size_t transformed_index = 0;
    while (have_value || transformed_index < unique.size()) {
      if (!have_value) {
        result.transform_missing_from_input += unique.size() - transformed_index;
        break;
      }
      if (transformed_index >= unique.size()) {
        result.input_missing_from_transform += input_count - input_index + 1;
        break;
      }
      const int comparison = compare_matrix(value.key, unique[transformed_index].key);
      if (comparison < 0) {
        ++result.input_missing_from_transform;
        advance();
      } else if (comparison > 0) {
        ++result.transform_missing_from_input;
        ++transformed_index;
      } else {
        advance();
        ++transformed_index;
      }
    }
  }
  return result;
}

void post_write_closure_report(const fs::path& path, const std::string& transform,
                               const SetComparison& result) {
  const bool equal = result.input_count == result.transformed_unique
      && result.input_missing_from_transform == 0
      && result.transform_missing_from_input == 0;
  std::ofstream report(path, std::ios::trunc);
  report << "schema_version\t1.0\n"
         << "transform\t" << transform << '\n'
         << "input_count\t" << result.input_count << '\n'
         << "transformed_raw\t" << result.transformed_raw << '\n'
         << "transformed_unique\t" << result.transformed_unique << '\n'
         << "input_missing_from_transform\t" << result.input_missing_from_transform << '\n'
         << "transform_missing_from_input\t" << result.transform_missing_from_input << '\n'
         << "exact_set_equal\t" << (equal ? 1 : 0) << '\n';
  report.close();
  if (!equal) fail("exact closure set comparison failed");
}

void closure_root_mode(const fs::path& root, const std::string& transform,
                       const fs::path& report) {
  const Checkpoint checkpoint = read_checkpoint(root);
  if (!checkpoint.complete) fail("closure requires completed flood");
  const fs::path input = state_path(root, checkpoint.completed_depth) / "visited";
  const fs::path temporary = root / ("closure_" + transform + ".tmp");
  post_stream_transform(input, temporary, transform, checkpoint.visited);
  const auto result = post_compare_transformed(input, temporary);
  post_write_closure_report(report, transform, result);
  fs::remove_all(temporary);
}

void closure_buckets_mode(const fs::path& buckets, std::uint64_t count,
                          const std::string& transform, const fs::path& report) {
  const fs::path temporary = buckets.parent_path() / ("closure_" + transform + ".tmp");
  post_stream_transform(buckets, temporary, transform, count);
  const auto result = post_compare_transformed(buckets, temporary);
  post_write_closure_report(report, transform, result);
  fs::remove_all(temporary);
}

void shell_mode(const fs::path& larger_root, const fs::path& smaller_root,
                const fs::path& output_buckets, const fs::path& registry_path,
                const fs::path& summary_path) {
  const Checkpoint larger = read_checkpoint(larger_root);
  const Checkpoint smaller = read_checkpoint(smaller_root);
  if (!larger.complete || !smaller.complete) fail("shell requires complete balls");
  if (larger.target_cutoff != smaller.target_cutoff + 1) fail("shell radii must be consecutive integers");
  if (fs::exists(output_buckets)) fs::remove_all(output_buckets);
  create_empty_buckets(output_buckets);
  const fs::path large_buckets = state_path(larger_root, larger.completed_depth) / "visited";
  const fs::path small_buckets = state_path(smaller_root, smaller.completed_depth) / "visited";
  std::uint64_t shell_count = 0, matched_smaller = 0;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path large_path = large_buckets / bucket_name(bucket);
    const fs::path small_path = small_buckets / bucket_name(bucket);
    const auto large_count = checked_record_count(large_path);
    const auto small_count = checked_record_count(small_path);
    std::ifstream large_input(large_path, std::ios::binary);
    std::ifstream small_input(small_path, std::ios::binary);
    std::ofstream output(output_buckets / bucket_name(bucket), std::ios::binary | std::ios::trunc);
    std::uint64_t large_index = 0, small_index = 0;
    GeoRecord large_value, small_value;
    bool have_large = false, have_small = false;
    auto advance_large = [&]() {
      if (large_index >= large_count) { have_large = false; return; }
      large_value = geo_read_record(large_input);
      if (!large_input) fail("short larger-ball record");
      ++large_index;
      have_large = true;
    };
    auto advance_small = [&]() {
      if (small_index >= small_count) { have_small = false; return; }
      small_value = geo_read_record(small_input);
      if (!small_input) fail("short smaller-ball record");
      ++small_index;
      have_small = true;
    };
    advance_large();
    advance_small();
    while (have_large) {
      if (!have_small) {
        geo_write_record(output, large_value);
        ++shell_count;
        advance_large();
        continue;
      }
      const int comparison = compare_matrix(large_value.key, small_value.key);
      if (comparison < 0) {
        geo_write_record(output, large_value);
        ++shell_count;
        advance_large();
      } else if (comparison > 0) {
        fail("smaller geometric ball is not an exact subset of larger ball");
      } else {
        ++matched_smaller;
        advance_large();
        advance_small();
      }
    }
    if (have_small) fail("smaller geometric ball has unmatched trailing keys");
  }
  if (matched_smaller != smaller.visited || shell_count + smaller.visited != larger.visited) {
    fail("exact shell cardinality identity failed");
  }
  if (registry_path.has_parent_path()) fs::create_directories(registry_path.parent_path());
  std::ofstream registry(registry_path, std::ios::binary | std::ios::trunc);
  registry.write("BOLZSH71", 8);
  write_u64(registry, shell_count);
  write_u32(registry, kGeoRecordBytes);
  write_u32(registry, static_cast<std::uint32_t>(smaller.target_cutoff));
  write_u32(registry, static_cast<std::uint32_t>(larger.target_cutoff));
  std::vector<char> buffer(8U * 1024U * 1024U);
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    std::ifstream input(output_buckets / bucket_name(bucket), std::ios::binary);
    while (input) {
      input.read(buffer.data(), static_cast<std::streamsize>(buffer.size()));
      if (const auto bytes = input.gcount(); bytes > 0) registry.write(buffer.data(), bytes);
    }
  }
  registry.close();
  std::ofstream summary(summary_path, std::ios::trunc);
  summary << "schema_version\t1.0\n"
          << "scope\texact_geometric_shell_(" << smaller.target_cutoff << ',' << larger.target_cutoff << "]\n"
          << "ball6_count\t" << smaller.visited << '\n'
          << "ball7_count\t" << larger.visited << '\n'
          << "shell_count\t" << shell_count << '\n'
          << "matched_ball6_keys\t" << matched_smaller << '\n'
          << "exact_difference_pass\t1\n"
          << "record_bytes\t" << kGeoRecordBytes << '\n';
}

}  // namespace

#ifndef CM_GEO7_POST_NO_MAIN
int main(int argc, char** argv) {
  try {
    if (argc < 2) fail("mode required");
    const std::string mode = argv[1];
    if (mode == "closure-root" && argc == 5) {
      closure_root_mode(argv[2], argv[3], argv[4]);
    } else if (mode == "closure-buckets" && argc == 6) {
      closure_buckets_mode(argv[2], std::stoull(argv[3]), argv[4], argv[5]);
    } else if (mode == "shell" && argc == 7) {
      shell_mode(argv[2], argv[3], argv[4], argv[5], argv[6]);
    } else {
      fail("usage: closure-root ROOT inverse|phi8 REPORT | closure-buckets BUCKETS COUNT inverse|phi8 REPORT | shell R7ROOT R6ROOT BUCKETS REGISTRY SUMMARY");
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 2;
  }
}
#endif
