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
struct Meta { std::uint32_t parent; std::uint8_t generator; std::uint8_t depth; std::uint16_t reserved; };
static_assert(sizeof(Meta) == 8);
using Matrix = std::array<std::uint8_t, 4>;
struct Candidate { std::string id; int prime = 0; std::array<Matrix, 8> images{}; };
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
static Matrix parse_matrix(const std::string& text, int prime) {
    const auto fields = split(text, ':');
    if (fields.size() != 4) fail("bad PGL matrix width");
    Matrix value{};
    for (int i = 0; i < 4; ++i) {
        const int parsed = std::stoi(fields[i]);
        if (parsed < 0 || parsed >= prime) fail("PGL matrix entry outside field");
        value[i] = static_cast<std::uint8_t>(parsed);
    }
    return value;
}
static std::vector<Candidate> load_candidates(const fs::path& path) {
    std::ifstream input(path);
    if (!input) fail("cannot open PGL survivor manifest");
    std::string line;
    if (!std::getline(input, line)) fail("empty PGL survivor manifest");
    std::vector<Candidate> result;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        const auto fields = split(line, '\t');
        if (fields.size() != 14) fail("bad PGL survivor row width");
        Candidate candidate;
        candidate.id = fields[0];
        candidate.prime = std::stoi(fields[1]);
        for (int i = 0; i < 8; ++i) candidate.images[i] = parse_matrix(fields[6 + i], candidate.prime);
        result.push_back(candidate);
    }
    return result;
}
static std::vector<Meta> load_tree(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) fail("cannot open based tree");
    std::array<char, 8> magic{}; std::uint64_t count = 0; std::uint32_t record_size = 0;
    input.read(magic.data(), magic.size()); input.read(reinterpret_cast<char*>(&count), sizeof(count)); input.read(reinterpret_cast<char*>(&record_size), sizeof(record_size));
    if (std::string(magic.data(), magic.size()) != "BOLZAT01" || record_size != sizeof(Meta) || count != 23129593ULL) fail("bad based tree header");
    std::vector<Meta> meta(static_cast<std::size_t>(count));
    input.read(reinterpret_cast<char*>(meta.data()), static_cast<std::streamsize>(meta.size() * sizeof(Meta)));
    if (!input) fail("short based tree read");
    return meta;
}
static Matrix multiply(const Matrix& left, const Matrix& right, int p, const std::array<int, 64>& inverses) {
    const int a = (left[0] * right[0] + left[1] * right[2]) % p;
    const int b = (left[0] * right[1] + left[1] * right[3]) % p;
    const int c = (left[2] * right[0] + left[3] * right[2]) % p;
    const int d = (left[2] * right[1] + left[3] * right[3]) % p;
    const std::array<int, 4> raw{a,b,c,d};
    int pivot = 0;
    for (const int value : raw) if (value) { pivot = value; break; }
    if (!pivot) fail("singular zero product");
    const int scale = inverses[pivot];
    return Matrix{static_cast<std::uint8_t>(a * scale % p), static_cast<std::uint8_t>(b * scale % p), static_cast<std::uint8_t>(c * scale % p), static_cast<std::uint8_t>(d * scale % p)};
}
static bool identity(const Matrix& value) { return value == Matrix{1,0,0,1}; }
static std::string reconstruct(std::uint32_t id, const std::vector<Meta>& meta) {
    std::vector<int> reverse;
    while (id) { reverse.push_back(meta[id].generator); id = meta[id].parent; }
    std::ostringstream out;
    for (auto it = reverse.rbegin(); it != reverse.rend(); ++it) { if (it != reverse.rbegin()) out << ' '; out << 'g' << *it; }
    return out.str();
}
int main(int argc, char** argv) {
    try {
        if (argc != 4) fail("usage: evaluator tree.bin manifest.tsv output.tsv");
        const auto meta = load_tree(argv[1]); const auto candidates = load_candidates(argv[2]);
        std::ofstream output(argv[3], std::ios::trunc); if (!output) fail("cannot open output TSV");
        output << "candidate_id\tprime\tbased_pass\tfirst_kernel_element_id\tfirst_kernel_depth\tfirst_kernel_word\telements_evaluated\n";
        std::vector<Matrix> states(meta.size());
        for (const auto& candidate : candidates) {
            std::array<int, 64> inverses{};
            for (int value = 1; value < candidate.prime; ++value) for (int possible = 1; possible < candidate.prime; ++possible) if (value * possible % candidate.prime == 1) { inverses[value] = possible; break; }
            states[0] = Matrix{1,0,0,1}; std::uint32_t witness = 0; std::uint64_t evaluated = 0;
            for (std::uint32_t id = 1; id < meta.size(); ++id) {
                const auto edge = meta[id];
                states[id] = multiply(states[edge.parent], candidate.images[edge.generator], candidate.prime, inverses);
                evaluated = id;
                if (identity(states[id])) { witness = id; break; }
            }
            output << candidate.id << '\t' << candidate.prime << '\t' << (witness ? "FAIL" : "PASS") << '\t';
            if (witness) output << witness << '\t' << static_cast<int>(meta[witness].depth) << '\t' << reconstruct(witness, meta);
            else output << "\t\t";
            output << '\t' << evaluated << '\n';
            std::cerr << candidate.id << " based=" << (witness ? "FAIL" : "PASS") << " evaluated=" << evaluated << '\n';
        }
        return 0;
    } catch (const std::exception& error) { std::cerr << "error: " << error.what() << '\n'; return 1; }
}
