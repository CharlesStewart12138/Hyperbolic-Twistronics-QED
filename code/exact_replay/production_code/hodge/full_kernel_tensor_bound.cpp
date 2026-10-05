#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include <mpfr.h>

namespace fs = std::filesystem;

namespace {

constexpr std::uint64_t kElements = 23129593ULL;
constexpr std::size_t kSymmetricEntries = 10;
constexpr mpfr_prec_t kPrecisionBits = 192;

struct Meta {
    std::uint32_t parent;
    std::uint8_t generator;
    std::uint8_t depth;
    std::uint16_t reserved;
};
static_assert(sizeof(Meta) == 8);

struct AbelianVector {
    std::int8_t value[4]{};
};
static_assert(sizeof(AbelianVector) == 4);

using SymmetricIntegerMatrix = std::array<std::int32_t, kSymmetricEntries>;

constexpr std::array<std::array<int, 4>, 8> kGeneratorAbelianization{{
    {{ 1,  0,  0,  0}},
    {{ 0, -1,  0,  0}},
    {{-1, -1,  1,  0}},
    {{-1, -1,  0, -1}},
    {{-1,  0,  0,  0}},
    {{ 0,  1,  0,  0}},
    {{ 1,  1, -1,  0}},
    {{ 1,  1,  0,  1}},
}};

constexpr std::array<std::array<int, 4>, 4> kTangentC8{{
    {{ 1, 1,  0,  1}},
    {{-1, 0,  0,  0}},
    {{ 0, 0,  0,  1}},
    {{ 1, 0, -1, -1}},
}};

[[noreturn]] void fail(const std::string& message) {
    throw std::runtime_error(message);
}

std::size_t packed_index(int i, int j) {
    if (i > j) std::swap(i, j);
    static constexpr std::size_t start[4]{0, 4, 7, 9};
    return start[i] + static_cast<std::size_t>(j - i);
}

std::array<std::array<std::int64_t, 4>, 4> unpack(const SymmetricIntegerMatrix& packed) {
    std::array<std::array<std::int64_t, 4>, 4> matrix{};
    for (int i = 0; i < 4; ++i) {
        for (int j = i; j < 4; ++j) {
            matrix[i][j] = matrix[j][i] = packed[packed_index(i, j)];
        }
    }
    return matrix;
}

bool is_c8_invariant(const SymmetricIntegerMatrix& packed) {
    const auto matrix = unpack(packed);
    std::array<std::array<std::int64_t, 4>, 4> transformed{};
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            std::int64_t value = 0;
            for (int a = 0; a < 4; ++a) {
                for (int b = 0; b < 4; ++b) {
                    value += static_cast<std::int64_t>(kTangentC8[a][i]) * matrix[a][b]
                           * static_cast<std::int64_t>(kTangentC8[b][j]);
                }
            }
            transformed[i][j] = value;
            if (value != matrix[i][j]) return false;
        }
    }
    return true;
}

struct OrbitMap {
    std::vector<std::uint32_t> element_to_row;
    std::vector<std::uint32_t> representatives;
    std::vector<std::uint32_t> weights;
};

OrbitMap load_orbit_map(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) fail("cannot open orbit map: " + path.string());
    std::array<char, 8> magic{};
    std::uint64_t elements = 0, rows = 0;
    input.read(magic.data(), static_cast<std::streamsize>(magic.size()));
    input.read(reinterpret_cast<char*>(&elements), sizeof(elements));
    input.read(reinterpret_cast<char*>(&rows), sizeof(rows));
    if (std::string(magic.data(), magic.size()) != "BOLZAO01") fail("bad orbit-map magic");
    if (elements != kElements || rows == 0) fail("orbit-map dimensions disagree with exact certificate");
    OrbitMap result;
    result.element_to_row.resize(static_cast<std::size_t>(elements));
    result.representatives.resize(static_cast<std::size_t>(rows));
    result.weights.resize(static_cast<std::size_t>(rows));
    input.read(reinterpret_cast<char*>(result.element_to_row.data()),
               static_cast<std::streamsize>(result.element_to_row.size() * sizeof(std::uint32_t)));
    input.read(reinterpret_cast<char*>(result.representatives.data()),
               static_cast<std::streamsize>(result.representatives.size() * sizeof(std::uint32_t)));
    input.read(reinterpret_cast<char*>(result.weights.data()),
               static_cast<std::streamsize>(result.weights.size() * sizeof(std::uint32_t)));
    if (!input) fail("short orbit-map read");
    return result;
}

std::vector<SymmetricIntegerMatrix> build_orbit_moments(
    const fs::path& tree_path,
    const OrbitMap& orbits,
    std::uint64_t& total_trace,
    std::uint64_t& invariant_orbits
) {
    std::ifstream input(tree_path, std::ios::binary);
    if (!input) fail("cannot open tree binary: " + tree_path.string());
    std::array<char, 8> magic{};
    std::uint64_t count = 0;
    std::uint32_t record_size = 0;
    input.read(magic.data(), static_cast<std::streamsize>(magic.size()));
    input.read(reinterpret_cast<char*>(&count), sizeof(count));
    input.read(reinterpret_cast<char*>(&record_size), sizeof(record_size));
    if (std::string(magic.data(), magic.size()) != "BOLZAT01" || count != kElements || record_size != sizeof(Meta)) {
        fail("tree binary disagrees with the exact based-ball certificate");
    }

    std::vector<AbelianVector> vectors(static_cast<std::size_t>(count));
    std::vector<SymmetricIntegerMatrix> moments(orbits.representatives.size());
    Meta meta{};
    for (std::uint32_t id = 0; id < count; ++id) {
        input.read(reinterpret_cast<char*>(&meta), sizeof(meta));
        if (!input) fail("short tree record read");
        if (id == 0) {
            if (meta.parent != 0 || meta.generator != 255 || meta.depth != 0) fail("bad identity tree record");
            continue;
        }
        if (meta.parent >= id || meta.generator >= 8 || meta.depth == 0) fail("bad tree edge");
        const auto& parent = vectors[meta.parent];
        AbelianVector current{};
        for (int i = 0; i < 4; ++i) {
            const int value = static_cast<int>(parent.value[i]) + kGeneratorAbelianization[meta.generator][i];
            if (value < -127 || value > 127) fail("abelianization exceeds int8 contract");
            current.value[i] = static_cast<std::int8_t>(value);
        }
        vectors[id] = current;
        const auto row = orbits.element_to_row[id];
        if (row >= moments.size()) fail("tree element maps outside orbit table");
        auto& matrix = moments[row];
        for (int i = 0; i < 4; ++i) {
            for (int j = i; j < 4; ++j) {
                const int product = static_cast<int>(current.value[i]) * static_cast<int>(current.value[j]);
                auto& entry = matrix[packed_index(i, j)];
                if ((product > 0 && entry > std::numeric_limits<std::int32_t>::max() - product) ||
                    (product < 0 && entry < std::numeric_limits<std::int32_t>::min() - product)) {
                    fail("orbit integer moment overflow");
                }
                entry += product;
            }
        }
        if (id % 2000000U == 0) std::cerr << "tree_moments=" << id << '/' << (count - 1) << '\n';
    }

    total_trace = 0;
    invariant_orbits = 0;
    std::uint64_t orbit_weight_sum = 0;
    for (std::size_t row = 0; row < moments.size(); ++row) {
        orbit_weight_sum += orbits.weights[row];
        const auto matrix = unpack(moments[row]);
        const std::int64_t trace = matrix[0][0] + matrix[1][1] + matrix[2][2] + matrix[3][3];
        if (trace < 0) fail("negative exact orbit trace");
        total_trace += static_cast<std::uint64_t>(trace);
        if (!is_c8_invariant(moments[row])) fail("an inversion/C8 orbit moment is not exactly invariant");
        ++invariant_orbits;
    }
    if (orbit_weight_sum != count - 1) fail("orbit weights do not cover the exact nonidentity ball");
    return moments;
}

std::uint32_t parse_prefixed_id(const char* begin, const char* end, char prefix) {
    if (begin == end || *begin != prefix) fail("bad prefixed CSV id");
    std::uint32_t value = 0;
    for (const char* p = begin + 1; p != end; ++p) {
        if (*p < '0' || *p > '9') fail("nondigit in CSV id");
        value = value * 10U + static_cast<std::uint32_t>(*p - '0');
    }
    return value;
}

std::uint32_t parse_uint(const char* begin, const char* end) {
    if (begin == end) fail("empty CSV integer");
    std::uint32_t value = 0;
    for (const char* p = begin; p != end; ++p) {
        if (*p < '0' || *p > '9') fail("nondigit in CSV integer");
        value = value * 10U + static_cast<std::uint32_t>(*p - '0');
    }
    return value;
}

struct CsvFields {
    std::uint32_t id = 0;
    std::uint32_t depth = 0;
    const char* interval_begin = nullptr;
    const char* interval_end = nullptr;
};

CsvFields parse_csv_fields(const std::string& line) {
    const char* starts[3]{};
    const char* ends[3]{};
    int captured = 0;
    int field = 0;
    bool quoted = false;
    const char* start = line.data();
    const char* data = line.data();
    const std::size_t size = line.size();
    for (std::size_t i = 0; i <= size; ++i) {
        const bool at_end = i == size;
        const char ch = at_end ? '\0' : data[i];
        if (!at_end && ch == '"') {
            if (quoted && i + 1 < size && data[i + 1] == '"') {
                ++i;
                continue;
            }
            quoted = !quoted;
        }
        if (at_end || (ch == ',' && !quoted)) {
            int slot = -1;
            if (field == 0) slot = 0;
            else if (field == 5) slot = 1;
            else if (field == 13) slot = 2;
            if (slot >= 0) {
                starts[slot] = start;
                ends[slot] = data + i;
                ++captured;
            }
            ++field;
            start = data + i + 1;
        }
    }
    if (captured != 3 || quoted) fail("could not parse required CSV fields");
    return CsvFields{parse_prefixed_id(starts[0], ends[0], 'B'), parse_uint(starts[1], ends[1]), starts[2], ends[2]};
}

std::pair<std::string, std::string> parse_interval(const char* begin, const char* end) {
    while (begin != end && (*begin == '"' || *begin == '[')) ++begin;
    while (end != begin && (end[-1] == '"' || end[-1] == ']')) --end;
    const char* comma = begin;
    while (comma != end && *comma != ',') ++comma;
    if (comma == begin || comma == end || comma + 1 == end) fail("bad numerical interval");
    return {std::string(begin, comma), std::string(comma + 1, end)};
}

void physical_weight_interval(const std::string& distance_lower,
                              const std::string& distance_upper,
                              mpfr_t weight_lower,
                              mpfr_t weight_upper) {
    mpfr_t d, x, half;
    mpfr_inits2(kPrecisionBits, d, x, half, static_cast<mpfr_ptr>(nullptr));
    mpfr_set_ui(half, 1, MPFR_RNDN);
    mpfr_div_2ui(half, half, 1, MPFR_RNDN);

    // Lower weight: use an upper enclosure for d and every increasing stage.
    if (mpfr_set_str(d, distance_upper.c_str(), 10, MPFR_RNDU) != 0) fail("cannot parse upper distance");
    mpfr_sqr(x, d, MPFR_RNDU);
    mpfr_add_d(x, x, 0.25, MPFR_RNDU);
    mpfr_sqrt(x, x, MPFR_RNDU);
    mpfr_sub(x, x, half, MPFR_RNDU);
    mpfr_mul_ui(x, x, 5, MPFR_RNDU);
    mpfr_neg(x, x, MPFR_RNDN);
    mpfr_exp(weight_lower, x, MPFR_RNDD);

    // Upper weight: use a lower enclosure for d and every increasing stage.
    if (mpfr_set_str(d, distance_lower.c_str(), 10, MPFR_RNDD) != 0) fail("cannot parse lower distance");
    mpfr_sqr(x, d, MPFR_RNDD);
    mpfr_add_d(x, x, 0.25, MPFR_RNDD);
    mpfr_sqrt(x, x, MPFR_RNDD);
    mpfr_sub(x, x, half, MPFR_RNDD);
    mpfr_mul_ui(x, x, 5, MPFR_RNDD);
    mpfr_neg(x, x, MPFR_RNDN);
    mpfr_exp(weight_upper, x, MPFR_RNDU);
    if (mpfr_cmp(weight_lower, weight_upper) > 0) fail("reversed physical-weight interval");
    mpfr_clears(d, x, half, static_cast<mpfr_ptr>(nullptr));
}

std::string decimal(const mpfr_t value) {
    std::array<char, 128> buffer{};
    const int written = mpfr_snprintf(buffer.data(), buffer.size(), "%.45Re", value);
    if (written < 0 || static_cast<std::size_t>(written) >= buffer.size()) fail("MPFR formatting failed");
    return std::string(buffer.data());
}

std::array<std::array<std::string, 4>, 4> unpack_decimal(const std::array<mpfr_t, kSymmetricEntries>& packed) {
    std::array<std::array<std::string, 4>, 4> matrix{};
    for (int i = 0; i < 4; ++i) {
        for (int j = i; j < 4; ++j) {
            const auto value = decimal(packed[packed_index(i, j)]);
            matrix[i][j] = matrix[j][i] = value;
        }
    }
    return matrix;
}

void print_json_matrix(std::ostream& out, const std::array<std::array<std::string, 4>, 4>& matrix, int indent) {
    const std::string pad(static_cast<std::size_t>(indent), ' ');
    out << "[\n";
    for (int i = 0; i < 4; ++i) {
        out << pad << "  [";
        for (int j = 0; j < 4; ++j) {
            if (j) out << ", ";
            out << '"' << matrix[i][j] << '"';
        }
        out << ']' << (i == 3 ? "\n" : ",\n");
    }
    out << pad << ']';
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 5) {
            std::cerr << "usage: full_kernel_tensor_bound BASED_CSV TREE_BIN ORBIT_BIN OUTPUT_JSON\n";
            return 2;
        }
        const fs::path csv_path = argv[1], tree_path = argv[2], orbit_path = argv[3], output_path = argv[4];
        const auto started = std::chrono::steady_clock::now();
        const auto orbits = load_orbit_map(orbit_path);
        std::uint64_t unweighted_trace = 0, invariant_orbits = 0;
        const auto moments = build_orbit_moments(tree_path, orbits, unweighted_trace, invariant_orbits);
        std::cerr << "exact_orbit_moments=" << moments.size() << " invariant=" << invariant_orbits << '\n';

        std::array<mpfr_t, kSymmetricEntries> lower{}, upper{};
        for (std::size_t k = 0; k < kSymmetricEntries; ++k) {
            mpfr_init2(lower[k], kPrecisionBits);
            mpfr_init2(upper[k], kPrecisionBits);
            mpfr_set_zero(lower[k], 0);
            mpfr_set_zero(upper[k], 0);
        }
        mpfr_t weight_lower, weight_upper, term;
        mpfr_inits2(kPrecisionBits, weight_lower, weight_upper, term, static_cast<mpfr_ptr>(nullptr));

        std::ifstream csv(csv_path);
        if (!csv) fail("cannot open based CSV: " + csv_path.string());
        std::vector<char> buffer(32U << 20U);
        csv.rdbuf()->pubsetbuf(buffer.data(), static_cast<std::streamsize>(buffer.size()));
        std::string line;
        if (!std::getline(csv, line) || line.rfind("canonical_id,", 0) != 0) fail("bad based CSV header");
        std::uint32_t expected = 1;
        std::uint64_t representative_rows = 0;
        while (std::getline(csv, line)) {
            const auto fields = parse_csv_fields(line);
            if (fields.id != expected) fail("based CSV ids are not contiguous");
            const auto row = orbits.element_to_row[expected];
            if (row >= moments.size()) fail("CSV element maps outside orbit table");
            if (orbits.representatives[row] == expected) {
                const auto interval = parse_interval(fields.interval_begin, fields.interval_end);
                physical_weight_interval(interval.first, interval.second, weight_lower, weight_upper);
                for (std::size_t k = 0; k < kSymmetricEntries; ++k) {
                    const long coefficient = moments[row][k];
                    if (coefficient >= 0) {
                        mpfr_mul_si(term, weight_lower, coefficient, MPFR_RNDD);
                        mpfr_add(lower[k], lower[k], term, MPFR_RNDD);
                        mpfr_mul_si(term, weight_upper, coefficient, MPFR_RNDU);
                        mpfr_add(upper[k], upper[k], term, MPFR_RNDU);
                    } else {
                        mpfr_mul_si(term, weight_upper, coefficient, MPFR_RNDD);
                        mpfr_add(lower[k], lower[k], term, MPFR_RNDD);
                        mpfr_mul_si(term, weight_lower, coefficient, MPFR_RNDU);
                        mpfr_add(upper[k], upper[k], term, MPFR_RNDU);
                    }
                }
                ++representative_rows;
                if (representative_rows % 200000U == 0) {
                    std::cerr << "directed_weight_orbits=" << representative_rows << '/' << moments.size() << '\n';
                }
            }
            ++expected;
        }
        if (expected != kElements) fail("based CSV row count mismatch");
        if (representative_rows != moments.size()) fail("not every inversion/C8 orbit received a weight");

        const auto lower_matrix = unpack_decimal(lower);
        const auto upper_matrix = unpack_decimal(upper);
        const double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
        if (output_path.has_parent_path()) fs::create_directories(output_path.parent_path());
        std::ofstream out(output_path, std::ios::trunc);
        if (!out) fail("cannot write output JSON");
        out << "{\n"
            << "  \"schema_version\": \"1.0\",\n"
            << "  \"task_id\": \"CM-047-NP-TENSOR-BOUND\",\n"
            << "  \"scope\": \"LOCAL centered Bolza exact based geometric ball d<=6a_B\",\n"
            << "  \"h_over_a_B\": 0.5,\n"
            << "  \"lambda_perp_over_a_B\": 0.2,\n"
            << "  \"dangerous_nonidentity_elements\": " << (kElements - 1) << ",\n"
            << "  \"inversion_C8_orbits\": " << moments.size() << ",\n"
            << "  \"exact_C8_invariant_orbit_moments\": " << invariant_orbits << ",\n"
            << "  \"unweighted_integer_trace_sum\": " << unweighted_trace << ",\n"
            << "  \"mpfr_precision_bits\": " << kPrecisionBits << ",\n"
            << "  \"weight_formula\": \"exp(-5*(sqrt(1/4+d^2)-1/2))\",\n"
            << "  \"partial_tensor_entrywise_lower\": ";
        print_json_matrix(out, lower_matrix, 2);
        out << ",\n  \"partial_tensor_entrywise_upper\": ";
        print_json_matrix(out, upper_matrix, 2);
        out << ",\n"
            << "  \"directed_rounding_contract\": \"CSV distance endpoints are parsed outward; sqrt, multiplication, subtraction, exp, coefficient products, and sums use MPFR directed rounding\",\n"
            << "  \"symmetry_contract\": \"Each exact inversion/C8 orbit integer second moment passes U^T M U=M before any floating evaluation\",\n"
            << "  \"elapsed_seconds\": " << std::setprecision(17) << seconds << "\n"
            << "}\n";
        if (!out) fail("output JSON write failed");

        for (std::size_t k = 0; k < kSymmetricEntries; ++k) {
            mpfr_clear(lower[k]);
            mpfr_clear(upper[k]);
        }
        mpfr_clears(weight_lower, weight_upper, term, static_cast<mpfr_ptr>(nullptr));
        std::cout << "rows=" << (kElements - 1) << " orbits=" << representative_rows
                  << " seconds=" << std::setprecision(8) << seconds << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
