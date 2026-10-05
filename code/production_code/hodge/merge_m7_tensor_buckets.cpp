#include <mpfr.h>

#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace fs = std::filesystem;

constexpr mpfr_prec_t PRECISION = 192;
constexpr int ENTRIES = 16;
constexpr int BUCKETS = 256;

struct Node {
    std::array<mpfr_t, ENTRIES> lo;
    std::array<mpfr_t, ENTRIES> hi;
    std::int64_t elements = 0;
    std::int64_t trace = 0;
    int first_bucket = -1;
    int last_bucket = -1;

    Node() {
        for (int i = 0; i < ENTRIES; ++i) {
            mpfr_init2(lo[i], PRECISION);
            mpfr_init2(hi[i], PRECISION);
            mpfr_set_zero(lo[i], 0);
            mpfr_set_zero(hi[i], 0);
        }
    }
    ~Node() {
        for (int i = 0; i < ENTRIES; ++i) {
            mpfr_clear(lo[i]);
            mpfr_clear(hi[i]);
        }
    }
    Node(const Node&) = delete;
    Node& operator=(const Node&) = delete;
};

std::unordered_map<std::string, std::string> read_tsv(const fs::path& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open " + path.string());
    std::unordered_map<std::string, std::string> result;
    std::string line;
    while (std::getline(input, line)) {
        const auto tab = line.find('\t');
        if (tab != std::string::npos) result.emplace(line.substr(0, tab), line.substr(tab + 1));
    }
    return result;
}

std::string read_all(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) throw std::runtime_error("cannot open " + path.string());
    std::ostringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

std::int64_t json_integer(const std::string& text, const std::string& key) {
    const std::string needle = "\"" + key + "\"";
    auto pos = text.find(needle);
    if (pos == std::string::npos) throw std::runtime_error("missing JSON integer " + key);
    pos = text.find(':', pos + needle.size());
    if (pos == std::string::npos) throw std::runtime_error("missing JSON colon " + key);
    ++pos;
    while (pos < text.size() && std::isspace(static_cast<unsigned char>(text[pos]))) ++pos;
    std::size_t used = 0;
    auto value = std::stoll(text.substr(pos), &used);
    if (used == 0) throw std::runtime_error("invalid JSON integer " + key);
    return value;
}

std::array<std::string, ENTRIES> json_matrix(const std::string& text, const std::string& key) {
    std::array<std::string, ENTRIES> result;
    const std::string needle = "\"" + key + "\"";
    auto pos = text.find(needle);
    if (pos == std::string::npos) throw std::runtime_error("missing JSON matrix " + key);
    pos = text.find('[', pos + needle.size());
    for (int i = 0; i < ENTRIES; ++i) {
        pos = text.find('"', pos);
        if (pos == std::string::npos) throw std::runtime_error("short JSON matrix " + key);
        const auto end = text.find('"', pos + 1);
        if (end == std::string::npos) throw std::runtime_error("unterminated JSON matrix " + key);
        result[i] = text.substr(pos + 1, end - pos - 1);
        pos = end + 1;
    }
    return result;
}

std::string format_mpfr(const mpfr_t value, mpfr_rnd_t rounding) {
    char buffer[192];
    const char* format = rounding == MPFR_RNDD ? "%.75RDe" : "%.75RUe";
    const int count = mpfr_snprintf(buffer, sizeof(buffer), format, value);
    if (count < 0 || static_cast<std::size_t>(count) >= sizeof(buffer)) {
        throw std::runtime_error("MPFR serialization overflow");
    }
    return buffer;
}

void load_bucket(Node& node, const fs::path& path, int bucket) {
    const auto values = read_tsv(path);
    if (values.at("status") != "COMPLETE" || std::stoi(values.at("bucket")) != bucket) {
        throw std::runtime_error("invalid bucket metadata " + std::to_string(bucket));
    }
    node.elements = std::stoll(values.at("elements_consumed"));
    node.trace = std::stoll(values.at("unweighted_integer_trace_sum"));
    node.first_bucket = bucket;
    node.last_bucket = bucket;
    constexpr std::array<int, ENTRIES> symmetric_slot = {
        0, 1, 2, 3,
        1, 4, 5, 6,
        2, 5, 7, 8,
        3, 6, 8, 9,
    };
    for (int i = 0; i < ENTRIES; ++i) {
        const int slot = symmetric_slot[i];
        if (mpfr_set_str(node.lo[i], values.at("lower_" + std::to_string(slot)).c_str(), 10, MPFR_RNDD) != 0 ||
            mpfr_set_str(node.hi[i], values.at("upper_" + std::to_string(slot)).c_str(), 10, MPFR_RNDU) != 0) {
            throw std::runtime_error("invalid MPFR endpoint in bucket " + std::to_string(bucket));
        }
        if (mpfr_greater_p(node.lo[i], node.hi[i])) {
            throw std::runtime_error("reversed interval in bucket " + std::to_string(bucket));
        }
    }
}

std::unique_ptr<Node> merge_nodes(const Node& left, const Node& right) {
    auto result = std::make_unique<Node>();
    result->elements = left.elements + right.elements;
    result->trace = left.trace + right.trace;
    result->first_bucket = left.first_bucket;
    result->last_bucket = right.last_bucket;
    for (int i = 0; i < ENTRIES; ++i) {
        mpfr_add(result->lo[i], left.lo[i], right.lo[i], MPFR_RNDD);
        mpfr_add(result->hi[i], left.hi[i], right.hi[i], MPFR_RNDU);
    }
    return result;
}

void add_frozen_m6(Node& full, const Node& shell, const fs::path& m6_path) {
    const auto text = read_all(m6_path);
    const auto lower = json_matrix(text, "partial_tensor_entrywise_lower");
    const auto upper = json_matrix(text, "partial_tensor_entrywise_upper");
    full.elements = shell.elements + json_integer(text, "dangerous_nonidentity_elements") + 1;
    full.trace = shell.trace + json_integer(text, "unweighted_integer_trace_sum");
    full.first_bucket = 0;
    full.last_bucket = 255;
    mpfr_t endpoint;
    mpfr_init2(endpoint, PRECISION);
    for (int i = 0; i < ENTRIES; ++i) {
        if (mpfr_set_str(endpoint, lower[i].c_str(), 10, MPFR_RNDD) != 0) {
            throw std::runtime_error("invalid frozen m6 lower endpoint");
        }
        mpfr_add(full.lo[i], endpoint, shell.lo[i], MPFR_RNDD);
        if (mpfr_set_str(endpoint, upper[i].c_str(), 10, MPFR_RNDU) != 0) {
            throw std::runtime_error("invalid frozen m6 upper endpoint");
        }
        mpfr_add(full.hi[i], endpoint, shell.hi[i], MPFR_RNDU);
    }
    mpfr_clear(endpoint);
}

void write_matrix(std::ostream& out, const std::array<mpfr_t, ENTRIES>& values, mpfr_rnd_t rounding) {
    out << "[\n";
    for (int row = 0; row < 4; ++row) {
        out << "    [";
        for (int col = 0; col < 4; ++col) {
            if (col) out << ", ";
            out << '"' << format_mpfr(values[row * 4 + col], rounding) << '"';
        }
        out << "]" << (row == 3 ? "\n" : ",\n");
    }
    out << "  ]";
}

void write_tensor(const fs::path& path, const Node& node, const std::string& scope,
                  std::int64_t shell_elements, bool full_ball) {
    const fs::path temporary = path.string() + ".tmp";
    std::ofstream out(temporary, std::ios::binary);
    if (!out) throw std::runtime_error("cannot create " + temporary.string());
    out << "{\n"
        << "  \"schema_version\": \"1.0\",\n"
        << "  \"task_id\": \"CM-047-NP-M7-STREAM\",\n"
        << "  \"status\": \"COMPLETE\",\n"
        << "  \"scope\": \"" << scope << "\",\n"
        << "  \"elements_consumed\": " << node.elements << ",\n"
        << "  \"shell_elements_consumed\": " << shell_elements << ",\n"
        << "  \"identity_included\": " << (full_ball ? "true" : "false") << ",\n"
        << "  \"unweighted_integer_trace_sum\": " << node.trace << ",\n"
        << "  \"maximum_transport_word_depth\": 20,\n"
        << "  \"mpfr_precision_bits\": 192,\n"
        << "  \"weight_formula\": \"exp(-5*(sqrt(1/4+d^2)-1/2))\",\n"
        << "  \"merge_order\": \"bucket index 000..255, then fixed adjacent binary tree; frozen m6 added once with directed rounding\",\n"
        << "  \"partial_tensor_entrywise_lower\": ";
    write_matrix(out, node.lo, MPFR_RNDD);
    out << ",\n  \"partial_tensor_entrywise_upper\": ";
    write_matrix(out, node.hi, MPFR_RNDU);
    out << ",\n"
        << "  \"directed_rounding_contract\": \"bucket endpoints parsed outward; every fixed-tree lower addition uses RNDD and every upper addition uses RNDU at 192-bit MPFR precision\",\n"
        << "  \"deterministic_merge_contract\": \"completion and file-enumeration order are discarded; leaf positions are exact bucket indices\"\n"
        << "}\n";
    out.close();
    if (!out) throw std::runtime_error("failed writing " + temporary.string());
    fs::rename(temporary, path);
}

void write_trace_row(std::ostream& out, int level, int node_index, const Node& node) {
    out << level << '\t' << node_index << '\t' << node.first_bucket << '\t' << node.last_bucket
        << '\t' << node.elements << '\t' << node.trace;
    for (int i = 0; i < ENTRIES; ++i) out << '\t' << format_mpfr(node.lo[i], MPFR_RNDD);
    for (int i = 0; i < ENTRIES; ++i) out << '\t' << format_mpfr(node.hi[i], MPFR_RNDU);
    out << '\n';
}

int main(int argc, char** argv) {
    if (argc < 6 || argc > 7) {
        std::cerr << "usage: merge_m7_tensor_buckets BUCKET_DIR M6_JSON SHELL_JSON FULL_JSON TRACE_TSV [reverse-load]\n";
        return 2;
    }
    try {
        const fs::path bucket_dir = argv[1];
        const fs::path m6_path = argv[2];
        const fs::path shell_output = argv[3];
        const fs::path full_output = argv[4];
        const fs::path trace_output = argv[5];
        const bool reverse_load = argc == 7 && std::string(argv[6]) == "reverse-load";
        std::vector<std::unique_ptr<Node>> layer(BUCKETS);
        for (int step = 0; step < BUCKETS; ++step) {
            const int index = reverse_load ? BUCKETS - 1 - step : step;
            layer[index] = std::make_unique<Node>();
            std::ostringstream name;
            name << "bucket-" << std::setw(3) << std::setfill('0') << index << ".acc.tsv";
            load_bucket(*layer[index], bucket_dir / name.str(), index);
        }
        const fs::path trace_temp = trace_output.string() + ".tmp";
        std::ofstream trace(trace_temp, std::ios::binary);
        trace << "level\tnode\tfirst_bucket\tlast_bucket\telements\tinteger_trace";
        for (int i = 0; i < ENTRIES; ++i) trace << "\tlower_" << i;
        for (int i = 0; i < ENTRIES; ++i) trace << "\tupper_" << i;
        trace << '\n';
        int level_number = 0;
        while (layer.size() > 1) {
            if (layer.size() % 2) throw std::runtime_error("non-binary merge layer");
            std::vector<std::unique_ptr<Node>> next;
            next.reserve(layer.size() / 2);
            ++level_number;
            for (std::size_t i = 0; i < layer.size(); i += 2) {
                auto merged = merge_nodes(*layer[i], *layer[i + 1]);
                write_trace_row(trace, level_number, static_cast<int>(i / 2), *merged);
                next.push_back(std::move(merged));
            }
            layer = std::move(next);
        }
        trace.close();
        if (!trace) throw std::runtime_error("failed writing merge trace");
        fs::rename(trace_temp, trace_output);
        Node full;
        add_frozen_m6(full, *layer[0], m6_path);
        write_tensor(shell_output, *layer[0], "exact geometric shell 6a_B<d<=7a_B full 4D tensor",
                     layer[0]->elements, false);
        write_tensor(full_output, full, "LOCAL centered Bolza exact geometric ball d<=7a_B full 4D tensor",
                     layer[0]->elements, true);
        std::cout << "buckets=256 shell_elements=" << layer[0]->elements
                  << " shell_trace=" << layer[0]->trace
                  << " full_elements=" << full.elements
                  << " full_trace=" << full.trace
                  << " levels=" << level_number << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
