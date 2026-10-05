#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif

namespace fs = std::filesystem;
using i128 = __int128_t;

namespace {

constexpr int kGenerators = 8;
constexpr int kBuckets = 256;
constexpr int kMaximumRadius = 7;
constexpr std::uint32_t kKeyBytes = 130;
constexpr std::uint32_t kRawBytes = 136;
constexpr std::uint32_t kUniqueBytes = 135;
constexpr std::uint32_t kRegistryBytes = 147;

struct Field {
  std::array<std::int64_t, 8> c{};
  std::uint8_t exp = 0;
};

struct Matrix { Field a; Field b; };

struct RawRecord {
  Matrix key;
  std::uint8_t length = 0;
  std::uint32_t word = 0;
  std::uint8_t shard = 0;
};

struct UniqueRecord {
  Matrix key;
  std::uint8_t length = 0;
  std::uint32_t word = 0;
};

struct RegistryRecord {
  UniqueRecord canonical;
  std::uint32_t inverse_id = 0;
  std::uint32_t phi8_id = 0;
  std::uint8_t c8_orbit_size = 0;
  std::uint8_t combined_orbit_size = 0;
  std::uint8_t c8_stabilizer_order = 0;
  std::uint8_t combined_stabilizer_order = 0;
};

[[noreturn]] void fail(const std::string& message) { throw std::runtime_error(message); }

int inverse_of(int generator) { return (generator + 4) % kGenerators; }

int trailing_zeros_abs(i128 value) {
  if (value < 0) value = -value;
  if (value == 0) return 127;
  int result = 0;
  while ((value & 1) == 0) { value >>= 1; ++result; }
  return result;
}

std::int64_t checked_i64(i128 value) {
  if (value < std::numeric_limits<std::int64_t>::min() ||
      value > std::numeric_limits<std::int64_t>::max()) fail("exact coefficient overflow");
  return static_cast<std::int64_t>(value);
}

Field normalize(const std::array<i128, 8>& values, int exponent) {
  bool nonzero = false;
  int shift = exponent;
  for (const auto value : values) if (value != 0) {
    nonzero = true;
    shift = std::min(shift, trailing_zeros_abs(value));
  }
  Field result;
  if (!nonzero) return result;
  if (exponent < 0 || exponent > 255) fail("invalid dyadic exponent");
  result.exp = static_cast<std::uint8_t>(exponent - shift);
  for (std::size_t i = 0; i < 8; ++i) result.c[i] = checked_i64(values[i] >> shift);
  return result;
}

Field field_from(std::array<std::int64_t, 8> values, int exponent = 0) {
  std::array<i128, 8> wide{};
  for (std::size_t i = 0; i < 8; ++i) wide[i] = values[i];
  return normalize(wide, exponent);
}

Field negate(Field value) {
  for (auto& coefficient : value.c) {
    if (coefficient == std::numeric_limits<std::int64_t>::min()) fail("negation overflow");
    coefficient = -coefficient;
  }
  return value;
}

Field conjugate(Field value) {
  for (std::size_t i = 4; i < 8; ++i) value.c[i] = -value.c[i];
  return value;
}

Field add(const Field& left, const Field& right) {
  const int exponent = std::max<int>(left.exp, right.exp);
  const int ls = exponent - left.exp, rs = exponent - right.exp;
  std::array<i128, 8> result{};
  for (std::size_t i = 0; i < 8; ++i) {
    result[i] = (static_cast<i128>(left.c[i]) << ls) + (static_cast<i128>(right.c[i]) << rs);
  }
  return normalize(result, exponent);
}

using Q2 = std::array<i128, 2>;
using R4 = std::array<i128, 4>;

Q2 q2_mul(const Q2& x, const Q2& y) {
  return {x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]};
}

R4 real4_mul(const R4& x, const R4& y) {
  const Q2 p{x[0], x[1]}, q{x[2], x[3]}, s{y[0], y[1]}, t{y[2], y[3]};
  const Q2 ps = q2_mul(p, s), qt = q2_mul(q, t), beta2 = q2_mul(qt, Q2{2, 2});
  const Q2 pt = q2_mul(p, t), qs = q2_mul(q, s);
  return {ps[0] + beta2[0], ps[1] + beta2[1], pt[0] + qs[0], pt[1] + qs[1]};
}

Field multiply(const Field& left, const Field& right) {
  R4 lr{}, li{}, rr{}, ri{};
  for (std::size_t i = 0; i < 4; ++i) {
    lr[i] = left.c[i]; li[i] = left.c[i + 4];
    rr[i] = right.c[i]; ri[i] = right.c[i + 4];
  }
  const R4 rr_part = real4_mul(lr, rr), ii_part = real4_mul(li, ri);
  const R4 ri_part = real4_mul(lr, ri), ir_part = real4_mul(li, rr);
  std::array<i128, 8> result{};
  for (std::size_t i = 0; i < 4; ++i) {
    result[i] = rr_part[i] - ii_part[i];
    result[i + 4] = ri_part[i] + ir_part[i];
  }
  return normalize(result, static_cast<int>(left.exp) + right.exp);
}

bool operator==(const Field& x, const Field& y) { return x.exp == y.exp && x.c == y.c; }
bool operator==(const Matrix& x, const Matrix& y) { return x.a == y.a && x.b == y.b; }

Field one() { return field_from({1, 0, 0, 0, 0, 0, 0, 0}); }
Field zero() { return Field{}; }
Matrix identity_matrix() { return Matrix{one(), zero()}; }

const std::array<Field, 8>& phased_beta() {
  static const std::array<Field, 8> values = {
    field_from({0,0,1,0,0,0,0,0}), field_from({0,0,0,1,0,0,0,1},1),
    field_from({0,0,0,0,0,0,1,0}), field_from({0,0,0,-1,0,0,0,1},1),
    field_from({0,0,-1,0,0,0,0,0}), field_from({0,0,0,-1,0,0,0,-1},1),
    field_from({0,0,0,0,0,0,-1,0}), field_from({0,0,0,1,0,0,0,-1},1),
  };
  return values;
}

Matrix generator(int index) {
  static const Field alpha = field_from({1,1,0,0,0,0,0,0});
  return Matrix{alpha, phased_beta().at(static_cast<std::size_t>(index))};
}

Matrix matrix_multiply(const Matrix& left, const Matrix& right) {
  return Matrix{
    add(multiply(left.a, right.a), multiply(left.b, conjugate(right.b))),
    add(multiply(left.a, right.b), multiply(left.b, conjugate(right.a)))
  };
}

Matrix matrix_inverse(const Matrix& value) { return Matrix{conjugate(value.a), negate(value.b)}; }

int compare_field(const Field& x, const Field& y) {
  if (x.exp != y.exp) return x.exp < y.exp ? -1 : 1;
  if (x.c < y.c) return -1;
  if (y.c < x.c) return 1;
  return 0;
}

int compare_matrix(const Matrix& x, const Matrix& y) {
  const int a = compare_field(x.a, y.a);
  return a ? a : compare_field(x.b, y.b);
}

Matrix projective_key(Matrix matrix) {
  const Matrix negative{negate(matrix.a), negate(matrix.b)};
  return compare_matrix(negative, matrix) < 0 ? negative : matrix;
}

std::uint64_t mix64(std::uint64_t x) {
  x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
  x ^= x >> 27; x *= 0x94d049bb133111ebULL;
  x ^= x >> 31; return x;
}

std::uint64_t hash_matrix(const Matrix& value) {
  std::uint64_t h = 0x9e3779b97f4a7c15ULL;
  for (const Field* field : {&value.a, &value.b}) {
    h = mix64(h ^ field->exp);
    for (const auto coefficient : field->c) h = mix64(h ^ static_cast<std::uint64_t>(coefficient));
  }
  return h;
}

struct MatrixHash { std::size_t operator()(const Matrix& value) const { return hash_matrix(value); } };

void write_u32(std::ostream& out, std::uint32_t value) { out.write(reinterpret_cast<const char*>(&value), 4); }
void write_u64(std::ostream& out, std::uint64_t value) { out.write(reinterpret_cast<const char*>(&value), 8); }
std::uint32_t read_u32(std::istream& in) { std::uint32_t v; in.read(reinterpret_cast<char*>(&v),4); return v; }
std::uint64_t read_u64(std::istream& in) { std::uint64_t v; in.read(reinterpret_cast<char*>(&v),8); return v; }

void write_key(std::ostream& out, const Matrix& key) {
  for (const Field* field : {&key.a, &key.b}) {
    out.put(static_cast<char>(field->exp));
    out.write(reinterpret_cast<const char*>(field->c.data()), 8 * sizeof(std::int64_t));
  }
}

Matrix read_key(std::istream& in) {
  Matrix key;
  for (Field* field : {&key.a, &key.b}) {
    const int exponent = in.get();
    if (exponent == EOF) return Matrix{};
    field->exp = static_cast<std::uint8_t>(exponent);
    in.read(reinterpret_cast<char*>(field->c.data()), 8 * sizeof(std::int64_t));
  }
  return key;
}

void write_raw(std::ostream& out, const RawRecord& record) {
  write_key(out, record.key); out.put(static_cast<char>(record.length));
  write_u32(out, record.word); out.put(static_cast<char>(record.shard));
}

RawRecord read_raw(std::istream& in) {
  RawRecord record; record.key = read_key(in);
  if (!in) return record;
  record.length = static_cast<std::uint8_t>(in.get()); record.word = read_u32(in);
  record.shard = static_cast<std::uint8_t>(in.get()); return record;
}

void write_unique(std::ostream& out, const UniqueRecord& record) {
  write_key(out, record.key); out.put(static_cast<char>(record.length)); write_u32(out, record.word);
}

UniqueRecord read_unique(std::istream& in) {
  UniqueRecord record; record.key = read_key(in);
  if (!in) return record;
  record.length = static_cast<std::uint8_t>(in.get()); record.word = read_u32(in); return record;
}

std::string bucket_name(int bucket) {
  std::ostringstream out; out << "bucket-" << std::setw(3) << std::setfill('0') << bucket << ".bin";
  return out.str();
}

std::string shard_name(int shard) {
  std::ostringstream out; out << "shard-" << std::setw(2) << std::setfill('0') << shard;
  return out.str();
}

std::uint64_t peak_rss() {
#ifdef _WIN32
  PROCESS_MEMORY_COUNTERS counters{};
  if (GetProcessMemoryInfo(GetCurrentProcess(), &counters, sizeof(counters))) return counters.PeakWorkingSetSize;
#endif
  return 0;
}

class Generator {
 public:
  Generator(int maximum, int shard, const fs::path& root) : maximum_(maximum), shard_(shard) {
    const fs::path directory = root / "generation" / shard_name(shard);
    fs::create_directories(directory);
    streams_.reserve(kBuckets);
    for (int bucket = 0; bucket < kBuckets; ++bucket) {
      streams_.emplace_back(directory / bucket_name(bucket), std::ios::binary | std::ios::trunc);
      if (!streams_.back()) fail("cannot open generation bucket");
    }
  }

  void run() {
    if (shard_ == 8) { emit(identity_matrix(), 0, 0); return; }
    word_[0] = shard_;
    visit(generator(shard_), 1, static_cast<std::uint32_t>(shard_));
  }

  const std::array<std::uint64_t, kMaximumRadius + 1>& by_length() const { return by_length_; }

 private:
  void emit(const Matrix& matrix, int length, std::uint32_t code) {
    RawRecord record{projective_key(matrix), static_cast<std::uint8_t>(length), code, static_cast<std::uint8_t>(shard_)};
    const int bucket = static_cast<int>(hash_matrix(record.key) & (kBuckets - 1));
    write_raw(streams_[bucket], record); ++by_length_[length];
  }
  void visit(const Matrix& matrix, int length, std::uint32_t code) {
    emit(matrix, length, code);
    if (length == maximum_) return;
    for (int next = 0; next < kGenerators; ++next) {
      if (next == inverse_of(word_[length - 1])) continue;
      word_[length] = next;
      visit(matrix_multiply(matrix, generator(next)), length + 1, (code << 3) | static_cast<std::uint32_t>(next));
    }
  }
  int maximum_, shard_;
  std::array<int, kMaximumRadius> word_{};
  std::array<std::uint64_t, kMaximumRadius + 1> by_length_{};
  std::vector<std::ofstream> streams_;
};

bool record_less(const RawRecord& x, const RawRecord& y) {
  const int key = compare_matrix(x.key, y.key);
  if (key) return key < 0;
  if (x.length != y.length) return x.length < y.length;
  if (x.word != y.word) return x.word < y.word;
  return x.shard < y.shard;
}

void generate_mode(int maximum, int shard, const fs::path& root, const fs::path& summary) {
  if (maximum < 0 || maximum > kMaximumRadius || shard < 0 || shard > 8) fail("bad generation arguments");
  const auto started = std::chrono::steady_clock::now();
  Generator generator_job(maximum, shard, root); generator_job.run();
  std::ofstream out(summary, std::ios::trunc);
  out << "status\tCOMPLETE\nshard\t" << shard << "\nmaximum\t" << maximum << "\nrecord_bytes\t" << kRawBytes << "\n";
  std::uint64_t total = 0;
  for (int length = 0; length <= maximum; ++length) { const auto count = generator_job.by_length()[length]; total += count; out << "length_" << length << '\t' << count << '\n'; }
  out << "total\t" << total << "\npeak_rss_bytes\t" << peak_rss() << "\nelapsed_seconds\t"
      << std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count() << '\n';
}

void reduce_mode(int maximum, const fs::path& root, const fs::path& summary) {
  const auto started = std::chrono::steady_clock::now();
  const fs::path reduced = root / "reduced"; fs::create_directories(reduced);
  std::ofstream report(summary, std::ios::trunc);
  report << "bucket\traw\tunique\tduplicates\n";
  std::uint64_t total_raw = 0, total_unique = 0;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    std::vector<RawRecord> records;
    for (int shard = 0; shard <= 8; ++shard) {
      const fs::path path = root / "generation" / shard_name(shard) / bucket_name(bucket);
      std::ifstream input(path, std::ios::binary);
      if (!input) fail("missing shard bucket: " + path.string());
      const auto bytes = fs::file_size(path);
      if (bytes % kRawBytes) fail("corrupt raw bucket size");
      const std::size_t prior = records.size(); records.resize(prior + bytes / kRawBytes);
      for (std::size_t i = prior; i < records.size(); ++i) {
        records[i] = read_raw(input);
        if (!input || (hash_matrix(records[i].key) & (kBuckets - 1)) != static_cast<std::uint64_t>(bucket)) fail("raw bucket key mismatch");
      }
    }
    std::sort(records.begin(), records.end(), record_less);
    const fs::path output_path = reduced / bucket_name(bucket);
    std::ofstream output(output_path, std::ios::binary | std::ios::trunc);
    std::uint64_t unique = 0;
    for (std::size_t i = 0; i < records.size();) {
      const RawRecord& chosen = records[i]; write_unique(output, UniqueRecord{chosen.key, chosen.length, chosen.word}); ++unique;
      std::size_t j = i + 1; while (j < records.size() && records[j].key == chosen.key) ++j; i = j;
    }
    report << bucket << '\t' << records.size() << '\t' << unique << '\t' << (records.size() - unique) << '\n';
    total_raw += records.size(); total_unique += unique;
  }
  report << "TOTAL\t" << total_raw << '\t' << total_unique << '\t' << (total_raw - total_unique) << "\n";
  report << "maximum\t" << maximum << "\npeak_rss_bytes\t" << peak_rss() << "\nelapsed_seconds\t"
         << std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count() << '\n';
}

std::vector<int> decode_word(std::uint8_t length, std::uint32_t code) {
  std::vector<int> result(length);
  for (int index = length - 1; index >= 0; --index) { result[index] = code & 7U; code >>= 3; }
  return result;
}

Matrix matrix_from_tokens(const std::vector<int>& word) {
  Matrix result = identity_matrix();
  for (int token : word) result = matrix_multiply(result, generator(token));
  return projective_key(result);
}

Matrix inverse_key(const UniqueRecord& record) { return projective_key(matrix_inverse(record.key)); }

Matrix phi_key(const UniqueRecord& record) {
  auto word = decode_word(record.length, record.word);
  for (auto& token : word) token = (token + 1) & 7;
  return matrix_from_tokens(word);
}

void finalize_mode(int maximum, const fs::path& root, const fs::path& registry_path, const fs::path& summary_path) {
  const auto started = std::chrono::steady_clock::now();
  std::vector<UniqueRecord> unique;
  for (int bucket = 0; bucket < kBuckets; ++bucket) {
    const fs::path path = root / "reduced" / bucket_name(bucket);
    std::ifstream input(path, std::ios::binary);
    if (!input) fail("missing reduced bucket");
    const auto bytes = fs::file_size(path);
    if (bytes % kUniqueBytes) fail("corrupt reduced bucket size");
    const std::size_t prior = unique.size(); unique.resize(prior + bytes / kUniqueBytes);
    for (std::size_t i = prior; i < unique.size(); ++i) { unique[i] = read_unique(input); if (!input) fail("short reduced record"); }
  }
  std::unordered_map<Matrix, std::uint32_t, MatrixHash> lookup;
  lookup.reserve(unique.size() + unique.size() / 3);
  for (std::uint32_t id = 0; id < unique.size(); ++id) if (!lookup.emplace(unique[id].key, id).second) fail("cross-bucket duplicate exact key");
  std::vector<RegistryRecord> registry(unique.size());
  std::array<std::uint64_t, kMaximumRadius + 1> shells{};
  for (std::uint32_t id = 0; id < unique.size(); ++id) {
    auto& output = registry[id]; output.canonical = unique[id];
    ++shells.at(output.canonical.length);
    const auto inverse_it = lookup.find(inverse_key(unique[id]));
    const auto phi_it = lookup.find(phi_key(unique[id]));
    if (inverse_it == lookup.end() || phi_it == lookup.end()) fail("symmetry partner absent from registry");
    output.inverse_id = inverse_it->second; output.phi8_id = phi_it->second;
  }
  for (std::uint32_t id = 0; id < registry.size(); ++id) {
    std::array<std::uint32_t, 16> members{}; int member_count = 0;
    std::uint32_t cursor = id; int c8 = 0;
    do { if (++c8 > 8) fail("phi8 orbit exceeds order eight"); cursor = registry[cursor].phi8_id; } while (cursor != id);
    if (8 % c8) fail("invalid C8 orbit size");
    for (int inv = 0; inv < 2; ++inv) {
      cursor = inv ? registry[id].inverse_id : id;
      for (int power = 0; power < 8; ++power) {
        if (std::find(members.begin(), members.begin() + member_count, cursor) == members.begin() + member_count) members[member_count++] = cursor;
        cursor = registry[cursor].phi8_id;
      }
    }
    if (16 % member_count) fail("invalid dihedral orbit size");
    registry[id].c8_orbit_size = static_cast<std::uint8_t>(c8);
    registry[id].combined_orbit_size = static_cast<std::uint8_t>(member_count);
    registry[id].c8_stabilizer_order = static_cast<std::uint8_t>(8 / c8);
    registry[id].combined_stabilizer_order = static_cast<std::uint8_t>(16 / member_count);
  }
  for (std::uint32_t id = 0; id < registry.size(); ++id) {
    if (registry[registry[id].inverse_id].inverse_id != id) fail("inverse map is not an involution");
    std::uint32_t cursor = id;
    for (int power = 0; power < 8; ++power) cursor = registry[cursor].phi8_id;
    if (cursor != id) fail("phi8^8 closure failed");
  }
  if (registry_path.has_parent_path()) fs::create_directories(registry_path.parent_path());
  std::ofstream out(registry_path, std::ios::binary | std::ios::trunc);
  out.write("BOLZAG07", 8); write_u64(out, registry.size()); write_u32(out, kRegistryBytes);
  for (const auto& record : registry) {
    write_unique(out, record.canonical); write_u32(out, record.inverse_id); write_u32(out, record.phi8_id);
    out.put(static_cast<char>(record.c8_orbit_size)); out.put(static_cast<char>(record.combined_orbit_size));
    out.put(static_cast<char>(record.c8_stabilizer_order)); out.put(static_cast<char>(record.combined_stabilizer_order));
  }
  std::ofstream summary(summary_path, std::ios::trunc);
  summary << "radius,shell_count,ball_count\n"; std::uint64_t ball = 0;
  for (int length = 0; length <= maximum; ++length) { ball += shells[length]; summary << length << ',' << shells[length] << ',' << ball << '\n'; }
  summary << "#inverse_closure,1\n#phi8_closure,1\n#minimum_shortlex_rule,1\n";
  summary << "#peak_rss_bytes," << peak_rss() << "\n#elapsed_seconds,"
          << std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count() << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc < 2) fail("mode required");
    const std::string mode = argv[1];
    if (mode == "generate" && argc == 6) generate_mode(std::stoi(argv[2]), std::stoi(argv[3]), argv[4], argv[5]);
    else if (mode == "reduce" && argc == 5) reduce_mode(std::stoi(argv[2]), argv[3], argv[4]);
    else if (mode == "finalize" && argc == 6) finalize_mode(std::stoi(argv[2]), argv[3], argv[4], argv[5]);
    else fail("usage: generate MAX SHARD ROOT SUMMARY | reduce MAX ROOT SUMMARY | finalize MAX ROOT REGISTRY SUMMARY");
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAILED: " << error.what() << '\n'; return 2;
  }
}
