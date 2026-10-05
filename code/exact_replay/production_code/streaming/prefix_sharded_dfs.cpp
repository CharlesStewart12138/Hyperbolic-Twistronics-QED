#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif

namespace {

constexpr int kAlphabet = 8;
constexpr int kMaxLength = 63;

struct Counts {
  std::uint64_t recursion_nodes = 0;
  std::uint64_t inverse_prunes = 0;
  std::uint64_t cyclic_rejects = 0;
  std::uint64_t raw_leaves = 0;
  std::uint64_t accepted = 0;
  std::uint64_t noncanonical = 0;
  std::map<int, std::uint64_t> orbit_histogram;
};

struct Options {
  std::vector<std::uint8_t> prefix;
  int minimum_length = 1;
  int maximum_length = 9;
  std::string accepted_output;
  std::string summary_output;
};

int inverse_of(int generator) { return (generator + 4) % kAlphabet; }

std::vector<std::uint8_t> parse_prefix(const std::string &text) {
  std::vector<std::uint8_t> result;
  std::stringstream stream(text);
  std::string token;
  while (std::getline(stream, token, ',')) {
    if (token.empty()) continue;
    const int value = std::stoi(token);
    if (value < 0 || value >= kAlphabet) throw std::runtime_error("prefix token outside 0..7");
    result.push_back(static_cast<std::uint8_t>(value));
  }
  if (result.empty() || result.front() != 0) {
    throw std::runtime_error("C8-normalized prefix must begin with generator 0");
  }
  for (std::size_t index = 1; index < result.size(); ++index) {
    if (result[index] == inverse_of(result[index - 1])) {
      throw std::runtime_error("prefix is not freely reduced");
    }
  }
  return result;
}

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string key(argv[index]);
    if (index + 1 >= argc) throw std::runtime_error("missing value after " + key);
    const std::string value(argv[++index]);
    if (key == "--prefix") options.prefix = parse_prefix(value);
    else if (key == "--min-length") options.minimum_length = std::stoi(value);
    else if (key == "--max-length") options.maximum_length = std::stoi(value);
    else if (key == "--accepted-output") options.accepted_output = value;
    else if (key == "--summary-output") options.summary_output = value;
    else throw std::runtime_error("unknown option: " + key);
  }
  if (options.prefix.empty()) throw std::runtime_error("--prefix is required");
  if (options.minimum_length < 1 || options.maximum_length < options.minimum_length ||
      options.maximum_length > kMaxLength) {
    throw std::runtime_error("invalid length interval");
  }
  if (static_cast<int>(options.prefix.size()) > options.maximum_length) {
    throw std::runtime_error("prefix is longer than the maximum length");
  }
  if (options.accepted_output.empty() || options.summary_output.empty()) {
    throw std::runtime_error("both output paths are required");
  }
  return options;
}

int transformed_token(const std::array<std::uint8_t, kMaxLength> &word, int length,
                      bool inverted, int rotation, int position) {
  const int source_index = (rotation + position) % length;
  if (!inverted) return word[source_index];
  const int reversed_index = length - 1 - source_index;
  return inverse_of(word[reversed_index]);
}

int normalized_token(const std::array<std::uint8_t, kMaxLength> &word, int length,
                     bool inverted, int rotation, int position) {
  const int offset = transformed_token(word, length, inverted, rotation, 0);
  return (transformed_token(word, length, inverted, rotation, position) - offset + kAlphabet) % kAlphabet;
}

bool transformation_is_smaller(const std::array<std::uint8_t, kMaxLength> &word,
                               int length, bool inverted, int rotation) {
  for (int position = 0; position < length; ++position) {
    const int candidate = normalized_token(word, length, inverted, rotation, position);
    if (candidate < word[position]) return true;
    if (candidate > word[position]) return false;
  }
  return false;
}

bool transformations_equal(const std::array<std::uint8_t, kMaxLength> &word,
                           int length, bool left_inverted, int left_rotation,
                           bool right_inverted, int right_rotation) {
  for (int position = 0; position < length; ++position) {
    if (normalized_token(word, length, left_inverted, left_rotation, position) !=
        normalized_token(word, length, right_inverted, right_rotation, position)) return false;
  }
  return true;
}

bool canonical_and_orbit_size(const std::array<std::uint8_t, kMaxLength> &word,
                              int length, int &orbit_size) {
  for (int inverted = 0; inverted <= 1; ++inverted) {
    for (int rotation = 0; rotation < length; ++rotation) {
      if (transformation_is_smaller(word, length, inverted != 0, rotation)) return false;
    }
  }
  orbit_size = 0;
  for (int inverted = 0; inverted <= 1; ++inverted) {
    for (int rotation = 0; rotation < length; ++rotation) {
      bool seen = false;
      for (int prior_inverted = 0; prior_inverted <= inverted && !seen; ++prior_inverted) {
        const int prior_limit = prior_inverted < inverted ? length : rotation;
        for (int prior_rotation = 0; prior_rotation < prior_limit; ++prior_rotation) {
          if (transformations_equal(word, length, inverted != 0, rotation,
                                    prior_inverted != 0, prior_rotation)) {
            seen = true;
            break;
          }
        }
      }
      if (!seen) ++orbit_size;
    }
  }
  return true;
}

std::uint64_t peak_rss_bytes() {
#ifdef _WIN32
  PROCESS_MEMORY_COUNTERS counters{};
  if (GetProcessMemoryInfo(GetCurrentProcess(), &counters, sizeof(counters))) {
    return static_cast<std::uint64_t>(counters.PeakWorkingSetSize);
  }
#endif
  return 0;
}

class Enumerator {
 public:
  Enumerator(const Options &options, std::ofstream &accepted)
      : options_(options), accepted_(accepted) {
    std::copy(options.prefix.begin(), options.prefix.end(), word_.begin());
  }

  void run() {
    const int prefix_length = static_cast<int>(options_.prefix.size());
    for (int target = options_.minimum_length; target <= options_.maximum_length; ++target) {
      if (target < prefix_length) continue;
      visit(prefix_length, target, by_length_[target]);
    }
  }

  const std::map<int, Counts> &by_length() const { return by_length_; }

 private:
  void visit(int length, int target, Counts &counts) {
    ++counts.recursion_nodes;
    if (length == target) {
      if (inverse_of(word_[length - 1]) == word_[0]) {
        ++counts.cyclic_rejects;
        return;
      }
      ++counts.raw_leaves;
      int orbit_size = 0;
      if (!canonical_and_orbit_size(word_, length, orbit_size)) {
        ++counts.noncanonical;
        return;
      }
      ++counts.accepted;
      ++counts.orbit_histogram[orbit_size];
      accepted_.put(static_cast<char>(length));
      accepted_.write(reinterpret_cast<const char *>(word_.data()), length);
      return;
    }
    for (int generator = 0; generator < kAlphabet; ++generator) {
      if (generator == inverse_of(word_[length - 1])) {
        ++counts.inverse_prunes;
        continue;
      }
      word_[length] = static_cast<std::uint8_t>(generator);
      visit(length + 1, target, counts);
    }
  }

  const Options &options_;
  std::ofstream &accepted_;
  std::array<std::uint8_t, kMaxLength> word_{};
  std::map<int, Counts> by_length_;
};

void write_summary(const Options &options, const std::map<int, Counts> &by_length,
                   double elapsed_seconds, std::uint64_t rss_bytes) {
  std::ofstream output(options.summary_output, std::ios::binary | std::ios::trunc);
  if (!output) throw std::runtime_error("cannot open summary output");
  output << "schema_version\t1.0\n";
  output << "engine\tprefix_sharded_dfs_cpp20\n";
  output << "contract\tfree_reduction+cyclic_reduction+C8_shift+rotation+inversion\n";
  output << "prefix\t";
  for (std::size_t i = 0; i < options.prefix.size(); ++i) {
    if (i) output << ',';
    output << static_cast<int>(options.prefix[i]);
  }
  output << "\nminimum_length\t" << options.minimum_length << "\n";
  output << "maximum_length\t" << options.maximum_length << "\n";
  output << "elapsed_seconds\t" << elapsed_seconds << "\n";
  output << "peak_rss_bytes\t" << rss_bytes << "\n";
  output << "length\trecursion_nodes\tinverse_prunes\tcyclic_rejects\traw_leaves\taccepted\tnoncanonical\torbit_histogram\n";
  for (const auto &[length, counts] : by_length) {
    output << length << '\t' << counts.recursion_nodes << '\t' << counts.inverse_prunes << '\t'
           << counts.cyclic_rejects << '\t' << counts.raw_leaves << '\t' << counts.accepted << '\t'
           << counts.noncanonical << '\t';
    bool first = true;
    for (const auto &[orbit_size, count] : counts.orbit_histogram) {
      if (!first) output << ',';
      first = false;
      output << orbit_size << ':' << count;
    }
    output << '\n';
  }
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    std::ofstream accepted(options.accepted_output, std::ios::binary | std::ios::trunc);
    if (!accepted) throw std::runtime_error("cannot open accepted-word output");
    const auto started = std::chrono::steady_clock::now();
    Enumerator enumerator(options, accepted);
    enumerator.run();
    accepted.flush();
    if (!accepted) throw std::runtime_error("failed while writing accepted-word output");
    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    write_summary(options, enumerator.by_length(), elapsed, peak_rss_bytes());
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "FAILED: " << error.what() << '\n';
    return 2;
  }
}
