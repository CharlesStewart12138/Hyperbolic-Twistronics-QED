#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

#define CM_GEO7_POST_NO_MAIN
#include "geometric_ball_postprocess.cpp"
#undef CM_GEO7_POST_NO_MAIN

namespace {

std::string atomic_index(int index) {
  std::ostringstream stream;
  stream << std::setw(3) << std::setfill('0') << index;
  return stream.str();
}

std::map<std::string, std::string> atomic_read_tsv(const fs::path& path) {
  std::ifstream input(path);
  if (!input) fail("cannot open atomic manifest: " + path.string());
  std::map<std::string, std::string> values;
  std::string line;
  while (std::getline(input, line)) {
    const auto tab = line.find('\t');
    if (tab != std::string::npos) values[line.substr(0, tab)] = line.substr(tab + 1);
  }
  return values;
}

void atomic_write_text(const fs::path& path, const std::string& text) {
  fs::create_directories(path.parent_path());
  const fs::path temporary = path.string() + ".tmp";
  {
    std::ofstream output(temporary, std::ios::trunc);
    if (!output) fail("cannot write atomic manifest: " + temporary.string());
    output << text;
    output.flush();
    if (!output) fail("cannot flush atomic manifest: " + temporary.string());
  }
  if (fs::exists(path)) fs::remove(path);
  fs::rename(temporary, path);
}

std::uint64_t atomic_directory_count(const fs::path& directory) {
  std::uint64_t total = 0;
  for (int destination = 0; destination < kBuckets; ++destination) {
    const fs::path path = directory / bucket_name(destination);
    if (!fs::exists(path)) fail("atomic shard missing destination bucket");
    total += checked_record_count(path);
  }
  return total;
}

void atomic_transform_source(const fs::path& input_buckets, const fs::path& work,
                             const std::string& transform, int source) {
  if (source < 0 || source >= kBuckets) fail("source bucket index out of range");
  const std::string index = atomic_index(source);
  const fs::path shards = work / "transform_shards";
  const fs::path manifests = work / "transform_manifests";
  const fs::path complete = shards / ("source-" + index);
  const fs::path temporary = shards / ("source-" + index + ".tmp");
  const fs::path manifest = manifests / ("source-" + index + ".complete.tsv");
  const fs::path input_path = input_buckets / bucket_name(source);
  const std::uint64_t input_count = checked_record_count(input_path);

  if (fs::exists(manifest)) {
    const auto values = atomic_read_tsv(manifest);
    if (values.at("status") != "COMPLETE" || values.at("transform") != transform
        || std::stoull(values.at("source_bucket")) != static_cast<std::uint64_t>(source)
        || std::stoull(values.at("input_count")) != input_count
        || atomic_directory_count(complete) != input_count) {
      fail("completed transform shard failed validation");
    }
    std::cout << "already_complete source=" << source << " count=" << input_count << '\n';
    return;
  }

  if (fs::exists(complete)) {
    const std::uint64_t recovered_count = atomic_directory_count(complete);
    if (recovered_count != input_count) fail("unmanifested committed shard count mismatch");
  } else {
    if (fs::exists(temporary)) fs::remove_all(temporary);
    create_empty_buckets(temporary);
    std::vector<std::ofstream> outputs;
    outputs.reserve(kBuckets);
    for (int destination = 0; destination < kBuckets; ++destination) {
      outputs.emplace_back(temporary / bucket_name(destination), std::ios::binary | std::ios::app);
      if (!outputs.back()) fail("cannot open atomic transform destination");
    }
    std::ifstream input(input_path, std::ios::binary);
    for (std::uint64_t record_index = 0; record_index < input_count; ++record_index) {
      GeoRecord record = geo_read_record(input);
      if (!input) fail("short atomic transform source record");
      record.key = post_transform(record.key, transform);
      const int destination = static_cast<int>(hash_matrix(record.key) & (kBuckets - 1));
      geo_write_record(outputs[destination], record);
    }
    for (auto& output : outputs) output.close();
    if (atomic_directory_count(temporary) != input_count) fail("atomic transform shard count mismatch");
    fs::create_directories(shards);
    fs::rename(temporary, complete);
  }

  std::ostringstream body;
  body << "schema_version\t1.0\n"
       << "status\tCOMPLETE\n"
       << "transform\t" << transform << '\n'
       << "source_bucket\t" << source << '\n'
       << "input_count\t" << input_count << '\n'
       << "record_bytes\t" << kGeoRecordBytes << '\n';
  atomic_write_text(manifest, body.str());
  std::cout << "completed source=" << source << " count=" << input_count << '\n';
}

SetComparison atomic_compare_one(const fs::path& input_buckets, const fs::path& work,
                                 int destination) {
  if (destination < 0 || destination >= kBuckets) fail("destination bucket index out of range");
  std::uint64_t transformed_count = 0;
  for (int source = 0; source < kBuckets; ++source) {
    const fs::path manifest = work / "transform_manifests"
        / ("source-" + atomic_index(source) + ".complete.tsv");
    if (!fs::exists(manifest)) fail("transform source manifest missing");
    transformed_count += checked_record_count(work / "transform_shards"
        / ("source-" + atomic_index(source)) / bucket_name(destination));
  }

  std::vector<GeoRecord> transformed;
  transformed.reserve(static_cast<std::size_t>(transformed_count));
  for (int source = 0; source < kBuckets; ++source) {
    const fs::path path = work / "transform_shards" / ("source-" + atomic_index(source))
        / bucket_name(destination);
    const std::uint64_t count = checked_record_count(path);
    std::ifstream input(path, std::ios::binary);
    for (std::uint64_t i = 0; i < count; ++i) {
      transformed.push_back(geo_read_record(input));
      if (!input) fail("short atomic transformed record");
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

  SetComparison result;
  result.transformed_raw = transformed.size();
  result.transformed_unique = unique.size();
  const fs::path reference_path = input_buckets / bucket_name(destination);
  result.input_count = checked_record_count(reference_path);
  std::ifstream reference(reference_path, std::ios::binary);
  std::uint64_t reference_index = 0;
  std::size_t transformed_index = 0;
  GeoRecord value;
  bool have_value = false;
  auto advance = [&]() {
    if (reference_index >= result.input_count) { have_value = false; return; }
    value = geo_read_record(reference);
    if (!reference) fail("short atomic closure reference record");
    ++reference_index;
    have_value = true;
  };
  advance();
  while (have_value || transformed_index < unique.size()) {
    if (!have_value) {
      result.transform_missing_from_input += unique.size() - transformed_index;
      break;
    }
    if (transformed_index >= unique.size()) {
      result.input_missing_from_transform += result.input_count - reference_index + 1;
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
  return result;
}

void atomic_compare_destination(const fs::path& input_buckets, const fs::path& work,
                                int destination) {
  const std::string index = atomic_index(destination);
  const fs::path report = work / "comparison_manifests"
      / ("destination-" + index + ".complete.tsv");
  if (fs::exists(report)) {
    const auto values = atomic_read_tsv(report);
    if (values.at("status") != "COMPLETE"
        || std::stoull(values.at("destination_bucket")) != static_cast<std::uint64_t>(destination)) {
      fail("completed comparison manifest failed validation");
    }
    std::cout << "already_complete destination=" << destination << '\n';
    return;
  }
  const SetComparison result = atomic_compare_one(input_buckets, work, destination);
  std::ostringstream body;
  body << "schema_version\t1.0\n"
       << "status\tCOMPLETE\n"
       << "destination_bucket\t" << destination << '\n'
       << "transformed_raw\t" << result.transformed_raw << '\n'
       << "transformed_unique\t" << result.transformed_unique << '\n'
       << "input_count\t" << result.input_count << '\n'
       << "input_missing_from_transform\t" << result.input_missing_from_transform << '\n'
       << "transform_missing_from_input\t" << result.transform_missing_from_input << '\n';
  atomic_write_text(report, body.str());
  std::cout << "completed destination=" << destination
            << " input=" << result.input_count
            << " missing=" << (result.input_missing_from_transform
                + result.transform_missing_from_input) << '\n';
}

void atomic_finalize(const fs::path& work, const std::string& transform,
                     std::uint64_t expected_count, const fs::path& report) {
  SetComparison total;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path source_manifest = work / "transform_manifests"
        / ("source-" + atomic_index(bucket) + ".complete.tsv");
    const fs::path comparison_manifest = work / "comparison_manifests"
        / ("destination-" + atomic_index(bucket) + ".complete.tsv");
    if (!fs::exists(source_manifest) || !fs::exists(comparison_manifest)) {
      fail("atomic closure cannot finalize before 256/256 source and destination manifests");
    }
    const auto values = atomic_read_tsv(comparison_manifest);
    total.transformed_raw += std::stoull(values.at("transformed_raw"));
    total.transformed_unique += std::stoull(values.at("transformed_unique"));
    total.input_count += std::stoull(values.at("input_count"));
    total.input_missing_from_transform += std::stoull(values.at("input_missing_from_transform"));
    total.transform_missing_from_input += std::stoull(values.at("transform_missing_from_input"));
  }
  if (total.input_count != expected_count || total.transformed_raw != expected_count) {
    fail("atomic closure global count mismatch");
  }
  post_write_closure_report(report, transform, total);
  std::ostringstream body;
  body << "schema_version\t1.0\n"
       << "status\tCOMPLETE\n"
       << "transform\t" << transform << '\n'
       << "source_buckets_complete\t256\n"
       << "comparison_buckets_complete\t256\n"
       << "expected_count\t" << expected_count << '\n'
       << "input_missing_from_transform\t" << total.input_missing_from_transform << '\n'
       << "transform_missing_from_input\t" << total.transform_missing_from_input << '\n';
  atomic_write_text(work / "atomic_closure_complete.tsv", body.str());
  std::cout << "closure_complete count=" << expected_count << " missing=0\n";
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc < 2) fail("atomic closure mode required");
    const std::string mode = argv[1];
    if (mode == "transform-source" && argc == 6) {
      atomic_transform_source(argv[2], argv[3], argv[4], std::stoi(argv[5]));
    } else if (mode == "compare-destination" && argc == 5) {
      atomic_compare_destination(argv[2], argv[3], std::stoi(argv[4]));
    } else if (mode == "finalize" && argc == 6) {
      atomic_finalize(argv[2], argv[3], std::stoull(argv[4]), argv[5]);
    } else {
      fail("usage: transform-source INPUT_BUCKETS WORK TRANSFORM INDEX | compare-destination INPUT_BUCKETS WORK INDEX | finalize WORK TRANSFORM EXPECTED_COUNT REPORT");
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 2;
  }
}
