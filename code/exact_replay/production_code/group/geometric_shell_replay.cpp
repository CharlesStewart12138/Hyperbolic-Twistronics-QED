#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

#define CM_GEO7_NO_MAIN
#include "external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {

bool same_record(const GeoRecord& left, const GeoRecord& right) {
  return left.key == right.key && left.depth == right.depth
      && left.word_high == right.word_high && left.word_low == right.word_low;
}

void write_report(const fs::path& path, std::uint64_t count,
                  std::uint64_t ball6, std::uint64_t ball7,
                  std::uint64_t bytes) {
  std::ofstream output(path, std::ios::trunc);
  if (!output) fail("cannot write shell replay report");
  output << "schema_version\t1.0\n"
         << "shell_count\t" << count << '\n'
         << "record_bytes\t" << kGeoRecordBytes << '\n'
         << "registry_bytes\t" << bytes << '\n'
         << "binary_layout_pass\t1\n"
         << "bucket_strict_order_pass\t1\n"
         << "duplicate_exact_keys\t0\n"
         << "bucket_membership_pass\t1\n"
         << "registry_bucket_replay_equal\t1\n"
         << "ball6_count\t" << ball6 << '\n'
         << "ball7_count\t" << ball7 << '\n'
         << "count_identity_pass\t" << ((ball6 + count == ball7) ? 1 : 0) << '\n';
  if (ball6 + count != ball7) fail("shell replay count identity failed");
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 7) {
      fail("usage: BUCKETS REGISTRY EXPECTED_COUNT BALL6_COUNT BALL7_COUNT REPORT");
    }
    const fs::path buckets = argv[1];
    const fs::path registry_path = argv[2];
    const std::uint64_t expected = std::stoull(argv[3]);
    const std::uint64_t ball6 = std::stoull(argv[4]);
    const std::uint64_t ball7 = std::stoull(argv[5]);
    const fs::path report = argv[6];

    std::ifstream registry(registry_path, std::ios::binary);
    if (!registry) fail("cannot open shell registry");
    std::array<char, 8> magic{};
    registry.read(magic.data(), magic.size());
    if (!registry || std::string(magic.data(), magic.size()) != "BOLZSH71") {
      fail("bad shell registry magic");
    }
    const std::uint64_t header_count = read_u64(registry);
    const std::uint32_t record_bytes = read_u32(registry);
    const std::uint32_t lower_radius = read_u32(registry);
    const std::uint32_t upper_radius = read_u32(registry);
    if (!registry || header_count != expected || record_bytes != kGeoRecordBytes
        || lower_radius != 6 || upper_radius != 7) {
      fail("shell registry header contract mismatch");
    }

    std::uint64_t total = 0;
    for (int bucket = 0; bucket < kBuckets; ++bucket) {
      const fs::path path = buckets / bucket_name(bucket);
      const std::uint64_t count = checked_record_count(path);
      std::ifstream input(path, std::ios::binary);
      GeoRecord previous;
      bool have_previous = false;
      for (std::uint64_t i = 0; i < count; ++i) {
        const GeoRecord record = geo_read_record(input);
        if (!input) fail("short shell bucket record");
        if (static_cast<int>(hash_matrix(record.key) & (kBuckets - 1)) != bucket) {
          fail("shell record in wrong exact-key bucket");
        }
        if (have_previous && compare_matrix(previous.key, record.key) >= 0) {
          fail("shell bucket is not strictly sorted or has duplicate exact key");
        }
        const GeoRecord replay = geo_read_record(registry);
        if (!registry || !same_record(record, replay)) {
          fail("shell registry differs from bucket replay");
        }
        previous = record;
        have_previous = true;
        ++total;
      }
    }
    char trailing = 0;
    registry.read(&trailing, 1);
    if (registry.gcount() != 0) fail("shell registry has trailing bytes");
    if (total != expected) fail("shell replay record count mismatch");
    const std::uint64_t expected_bytes = 28ULL + expected * kGeoRecordBytes;
    if (fs::file_size(registry_path) != expected_bytes) fail("shell registry byte length mismatch");
    write_report(report, total, ball6, ball7, expected_bytes);
    std::cout << "shell_replay_complete count=" << total << " duplicates=0\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 2;
  }
}
