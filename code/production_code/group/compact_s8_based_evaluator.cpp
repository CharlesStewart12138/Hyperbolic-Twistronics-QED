#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

struct Meta {
    std::uint32_t parent;
    std::uint8_t generator;
    std::uint8_t depth;
    std::uint16_t reserved;
};
static_assert(sizeof(Meta) == 8);
using Perm = std::array<std::uint8_t, 8>;

struct Candidate {
    std::string id;
    std::string representative;
    std::string members;
    std::array<Perm, 8> images;
};

[[noreturn]] static void fail(const std::string& message) { throw std::runtime_error(message); }

static std::vector<std::string> split(const std::string& line, char delimiter) {
    std::vector<std::string> fields;
    std::size_t begin = 0;
    while (true) {
        const auto end = line.find(delimiter, begin);
        fields.push_back(line.substr(begin, end == std::string::npos ? end : end - begin));
        if (end == std::string::npos) break;
        begin = end + 1;
    }
    return fields;
}

static Perm parse_perm(const std::string& text) {
    if (text.size() != 8) fail("bad S8 permutation width");
    Perm value{};
    std::array<bool, 8> seen{};
    for (int i = 0; i < 8; ++i) {
        if (text[i] < '0' || text[i] > '7') fail("bad S8 permutation digit");
        value[i] = static_cast<std::uint8_t>(text[i] - '0');
        if (seen[value[i]]) fail("repeated S8 permutation digit");
        seen[value[i]] = true;
    }
    return value;
}

static std::vector<Candidate> load_candidates(const fs::path& path) {
    std::ifstream input(path);
    if (!input) fail("cannot open S8 survivor manifest");
    std::string line;
    if (!std::getline(input, line)) fail("empty S8 survivor manifest");
    std::vector<Candidate> result;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        const auto fields = split(line, '\t');
        if (fields.size() != 11) fail("bad S8 survivor manifest row width");
        Candidate candidate;
        candidate.id = fields[0];
        candidate.representative = fields[1];
        candidate.members = fields[2];
        for (int i = 0; i < 8; ++i) candidate.images[i] = parse_perm(fields[3 + i]);
        result.push_back(candidate);
    }
    if (result.size() != 6) fail("expected six S8 kernel-orbit representatives");
    return result;
}

static std::vector<Meta> load_tree(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) fail("cannot open based tree");
    std::array<char, 8> magic{};
    std::uint64_t count = 0;
    std::uint32_t record_size = 0;
    input.read(magic.data(), magic.size());
    input.read(reinterpret_cast<char*>(&count), sizeof(count));
    input.read(reinterpret_cast<char*>(&record_size), sizeof(record_size));
    if (std::string(magic.data(), magic.size()) != "BOLZAT01" || record_size != sizeof(Meta)) fail("bad tree header");
    if (count != 23129593ULL) fail("tree count drift");
    std::vector<Meta> meta(static_cast<std::size_t>(count));
    input.read(reinterpret_cast<char*>(meta.data()), static_cast<std::streamsize>(meta.size() * sizeof(Meta)));
    if (!input) fail("short tree read");
    return meta;
}

static Perm compose(const Perm& left, const Perm& right) {
    Perm result{};
    for (int i = 0; i < 8; ++i) result[i] = left[right[i]];
    return result;
}

static bool identity(const Perm& value) {
    for (int i = 0; i < 8; ++i) if (value[i] != i) return false;
    return true;
}

static std::string reconstruct(std::uint32_t id, const std::vector<Meta>& meta) {
    std::vector<int> reverse;
    while (id) {
        reverse.push_back(meta[id].generator);
        id = meta[id].parent;
    }
    std::ostringstream out;
    for (auto it = reverse.rbegin(); it != reverse.rend(); ++it) {
        if (it != reverse.rbegin()) out << ' ';
        out << 'g' << *it;
    }
    return out.str();
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) fail("usage: evaluator tree.bin manifest.tsv result.tsv");
        const auto meta = load_tree(argv[1]);
        const auto candidates = load_candidates(argv[2]);
        std::ofstream output(argv[3], std::ios::trunc);
        if (!output) fail("cannot open based result output");
        output << "kernel_orbit_id\trepresentative_seed_index\tmember_seed_indices\tbased_pass\tfirst_kernel_element_id\tfirst_kernel_depth\tfirst_kernel_word\telements_evaluated\n";
        std::vector<Perm> states(meta.size());
        for (const auto& candidate : candidates) {
            states[0] = Perm{0,1,2,3,4,5,6,7};
            std::uint32_t witness = 0;
            std::uint64_t evaluated = 0;
            for (std::uint32_t id = 1; id < meta.size(); ++id) {
                const auto edge = meta[id];
                states[id] = compose(states[edge.parent], candidate.images[edge.generator]);
                evaluated = id;
                if (identity(states[id])) {
                    witness = id;
                    break;
                }
            }
            output << candidate.id << '\t' << candidate.representative << '\t' << candidate.members << '\t'
                   << (witness ? "FAIL" : "PASS") << '\t';
            if (witness) output << witness << '\t' << static_cast<int>(meta[witness].depth) << '\t' << reconstruct(witness, meta);
            else output << "\t\t";
            output << '\t' << evaluated << '\n';
            std::cerr << candidate.id << " based=" << (witness ? "FAIL" : "PASS") << " evaluated=" << evaluated << '\n';
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << '\n';
        return 1;
    }
}
