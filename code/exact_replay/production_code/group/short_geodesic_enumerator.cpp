#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
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

#include <gmp.h>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif

// Exact geometry-driven enumeration for the regular-octagon Bolza group.
//
// A field element is represented in the basis
//   1,sqrt(2),beta,sqrt(2)beta,i,i sqrt(2),i beta,i sqrt(2)beta,
// beta^2=2+2sqrt(2), with a dyadic denominator.  This matches
// universal_cover.py exactly.  Matrix identities and cutoff decisions are
// exact; long-double values are reporting/fast-rejection aids only.

namespace fs = std::filesystem;
using i128 = __int128_t;

struct Field {
    std::array<std::int64_t, 8> c{};
    std::uint8_t exp = 0;
};

struct Matrix {
    Field a;
    Field b;
};

struct Meta {
    std::uint32_t parent = 0;
    std::uint8_t generator = 255;
    std::uint8_t depth = 0;
    std::uint16_t reserved = 0;
};

static_assert(sizeof(Field) <= 72, "Field layout unexpectedly large");
static_assert(sizeof(Matrix) <= 144, "Matrix layout unexpectedly large");
static_assert(sizeof(Meta) == 8, "Meta must remain compact");

[[noreturn]] static void fail(const std::string& message) {
    throw std::runtime_error(message);
}

static int trailing_zeros_abs(i128 value) {
    if (value < 0) value = -value;
    if (value == 0) return 127;
    int result = 0;
    while ((value & 1) == 0) {
        value >>= 1;
        ++result;
    }
    return result;
}

static std::int64_t checked_i64(i128 value) {
    if (value < std::numeric_limits<std::int64_t>::min() ||
        value > std::numeric_limits<std::int64_t>::max()) {
        fail("exact coefficient overflowed int64 storage");
    }
    return static_cast<std::int64_t>(value);
}

static Field normalize(const std::array<i128, 8>& values, int exponent) {
    bool nonzero = false;
    int shift = exponent;
    for (const auto value : values) {
        if (value != 0) {
            nonzero = true;
            shift = std::min(shift, trailing_zeros_abs(value));
        }
    }
    Field result;
    if (!nonzero) return result;
    if (exponent < 0 || exponent > 255) fail("invalid dyadic exponent");
    result.exp = static_cast<std::uint8_t>(exponent - shift);
    for (std::size_t index = 0; index < 8; ++index) {
        result.c[index] = checked_i64(values[index] >> shift);
    }
    return result;
}

static Field field_from(std::array<std::int64_t, 8> values, int exponent = 0) {
    std::array<i128, 8> wide{};
    for (std::size_t i = 0; i < 8; ++i) wide[i] = values[i];
    return normalize(wide, exponent);
}

static Field negate(Field value) {
    for (auto& coefficient : value.c) coefficient = -coefficient;
    return value;
}

static Field conjugate(Field value) {
    for (std::size_t i = 4; i < 8; ++i) value.c[i] = -value.c[i];
    return value;
}

static Field add(const Field& left, const Field& right) {
    const int exponent = std::max<int>(left.exp, right.exp);
    const int left_shift = exponent - left.exp;
    const int right_shift = exponent - right.exp;
    std::array<i128, 8> result{};
    for (std::size_t i = 0; i < 8; ++i) {
        result[i] = (static_cast<i128>(left.c[i]) << left_shift) +
                    (static_cast<i128>(right.c[i]) << right_shift);
    }
    return normalize(result, exponent);
}

using Q2 = std::array<i128, 2>;
using R4 = std::array<i128, 4>;

static Q2 q2_mul(const Q2& x, const Q2& y) {
    return {x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]};
}

static R4 real4_mul(const R4& x, const R4& y) {
    const Q2 p{x[0], x[1]}, q{x[2], x[3]};
    const Q2 s{y[0], y[1]}, t{y[2], y[3]};
    const Q2 ps = q2_mul(p, s);
    const Q2 qt = q2_mul(q, t);
    const Q2 beta2 = q2_mul(qt, Q2{2, 2});
    const Q2 pt = q2_mul(p, t);
    const Q2 qs = q2_mul(q, s);
    return {ps[0] + beta2[0], ps[1] + beta2[1], pt[0] + qs[0], pt[1] + qs[1]};
}

static Field multiply(const Field& left, const Field& right) {
    R4 lr{}, li{}, rr{}, ri{};
    for (std::size_t i = 0; i < 4; ++i) {
        lr[i] = left.c[i];
        li[i] = left.c[i + 4];
        rr[i] = right.c[i];
        ri[i] = right.c[i + 4];
    }
    const R4 rr_part = real4_mul(lr, rr);
    const R4 ii_part = real4_mul(li, ri);
    const R4 ri_part = real4_mul(lr, ri);
    const R4 ir_part = real4_mul(li, rr);
    std::array<i128, 8> result{};
    for (std::size_t i = 0; i < 4; ++i) {
        result[i] = rr_part[i] - ii_part[i];
        result[i + 4] = ri_part[i] + ir_part[i];
    }
    return normalize(result, static_cast<int>(left.exp) + right.exp);
}

static bool operator==(const Field& x, const Field& y) {
    return x.exp == y.exp && x.c == y.c;
}

static bool operator==(const Matrix& x, const Matrix& y) {
    return x.a == y.a && x.b == y.b;
}

static Field one() {
    return field_from({1, 0, 0, 0, 0, 0, 0, 0});
}

static Field zero() {
    return Field{};
}

static Matrix identity_matrix() {
    return Matrix{one(), zero()};
}

static const std::array<Field, 8>& phased_beta() {
    static const std::array<Field, 8> values = {
        field_from({0, 0, 1, 0, 0, 0, 0, 0}),
        field_from({0, 0, 0, 1, 0, 0, 0, 1}, 1),
        field_from({0, 0, 0, 0, 0, 0, 1, 0}),
        field_from({0, 0, 0, -1, 0, 0, 0, 1}, 1),
        field_from({0, 0, -1, 0, 0, 0, 0, 0}),
        field_from({0, 0, 0, -1, 0, 0, 0, -1}, 1),
        field_from({0, 0, 0, 0, 0, 0, -1, 0}),
        field_from({0, 0, 0, 1, 0, 0, 0, -1}, 1),
    };
    return values;
}

static Matrix generator(int index) {
    static const Field alpha = field_from({1, 1, 0, 0, 0, 0, 0, 0});
    return Matrix{alpha, phased_beta().at(static_cast<std::size_t>(index))};
}

static Matrix matrix_multiply(const Matrix& left, const Matrix& right) {
    return Matrix{
        add(multiply(left.a, right.a), multiply(left.b, conjugate(right.b))),
        add(multiply(left.a, right.b), multiply(left.b, conjugate(right.a))),
    };
}

static Matrix matrix_inverse(const Matrix& value) {
    return Matrix{conjugate(value.a), negate(value.b)};
}

static std::uint64_t mix64(std::uint64_t x) {
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

static std::uint64_t hash_matrix(const Matrix& value) {
    std::uint64_t h = 0x9e3779b97f4a7c15ULL;
    const Field* fields[2] = {&value.a, &value.b};
    for (const Field* field : fields) {
        h = mix64(h ^ field->exp);
        for (const auto coefficient : field->c) {
            h = mix64(h ^ static_cast<std::uint64_t>(coefficient));
        }
    }
    return h;
}

class ExactIndex {
public:
    explicit ExactIndex(std::uint64_t maximum_elements) {
        std::uint64_t needed = maximum_elements + maximum_elements / 2 + 1024;
        capacity_ = 1;
        while (capacity_ < needed) capacity_ <<= 1;
        if (capacity_ > (1ULL << 34)) fail("requested hash table is too large");
        slots_.assign(static_cast<std::size_t>(capacity_), 0);
        mask_ = capacity_ - 1;
    }

    std::pair<std::uint32_t, bool> insert(const Matrix& key, std::vector<Matrix>& matrices) {
        std::uint64_t pos = hash_matrix(key) & mask_;
        while (true) {
            const std::uint32_t stored = slots_[static_cast<std::size_t>(pos)];
            if (stored == 0) {
                if (matrices.size() >= std::numeric_limits<std::uint32_t>::max()) {
                    fail("element count exceeds uint32 index capacity");
                }
                matrices.push_back(key);
                const auto id = static_cast<std::uint32_t>(matrices.size() - 1);
                slots_[static_cast<std::size_t>(pos)] = id + 1;
                return {id, true};
            }
            const std::uint32_t id = stored - 1;
            if (matrices[id] == key) return {id, false};
            pos = (pos + 1) & mask_;
        }
    }

    std::uint32_t find(const Matrix& key, const std::vector<Matrix>& matrices) const {
        std::uint64_t pos = hash_matrix(key) & mask_;
        while (true) {
            const std::uint32_t stored = slots_[static_cast<std::size_t>(pos)];
            if (stored == 0) fail("exact matrix lookup failed");
            const std::uint32_t id = stored - 1;
            if (matrices[id] == key) return id;
            pos = (pos + 1) & mask_;
        }
    }

    std::uint64_t capacity() const { return capacity_; }

private:
    std::vector<std::uint32_t> slots_;
    std::uint64_t capacity_ = 0;
    std::uint64_t mask_ = 0;
};

static long double field_value_real(const Field& value) {
    const long double root2 = std::sqrt(2.0L);
    const long double beta = std::sqrt(2.0L + 2.0L * root2);
    const std::array<long double, 4> basis{1.0L, root2, beta, root2 * beta};
    long double result = 0;
    for (std::size_t i = 0; i < 4; ++i) result += value.c[i] * basis[i];
    return std::ldexp(result, -static_cast<int>(value.exp));
}

static long double field_value_imag(const Field& value) {
    const long double root2 = std::sqrt(2.0L);
    const long double beta = std::sqrt(2.0L + 2.0L * root2);
    const std::array<long double, 4> basis{1.0L, root2, beta, root2 * beta};
    long double result = 0;
    for (std::size_t i = 0; i < 4; ++i) result += value.c[i + 4] * basis[i];
    return std::ldexp(result, -static_cast<int>(value.exp));
}

static Field exact_cosh_displacement(const Matrix& value) {
    const Field norm = multiply(value.a, conjugate(value.a));
    return add(add(norm, norm), negate(one()));
}

static void mpz_set_i64_exact(mpz_t target, std::int64_t value) {
    const bool negative = value < 0;
    const std::uint64_t magnitude = negative
        ? static_cast<std::uint64_t>(-(value + 1)) + 1U
        : static_cast<std::uint64_t>(value);
    mpz_import(target, 1, -1, sizeof(magnitude), 0, 0, &magnitude);
    if (negative) mpz_neg(target, target);
}

static int sign_q2(const mpz_t p, const mpz_t q) {
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

static int exact_real_field_sign(const Field& value) {
    for (std::size_t i = 4; i < 8; ++i) {
        if (value.c[i] != 0) fail("sign requested for non-real algebraic value");
    }
    mpz_t p, q, r, s;
    mpz_inits(p, q, r, s, nullptr);
    mpz_set_i64_exact(p, value.c[0]);
    mpz_set_i64_exact(q, value.c[1]);
    mpz_set_i64_exact(r, value.c[2]);
    mpz_set_i64_exact(s, value.c[3]);
    const int sa = sign_q2(p, q), sb = sign_q2(r, s);
    if (sb == 0 || sa == 0 || sa == sb) {
        const int answer = sb == 0 ? sa : (sa == 0 ? sb : sa);
        mpz_clears(p, q, r, s, nullptr);
        return answer;
    }

    mpz_t a0, a1, b0, b1, delta0, delta1, tmp;
    mpz_inits(a0, a1, b0, b1, delta0, delta1, tmp, nullptr);
    mpz_mul(a0, p, p);
    mpz_mul(tmp, q, q);
    mpz_mul_ui(tmp, tmp, 2);
    mpz_add(a0, a0, tmp);
    mpz_mul(a1, p, q);
    mpz_mul_ui(a1, a1, 2);
    mpz_mul(b0, r, r);
    mpz_mul(tmp, s, s);
    mpz_mul_ui(tmp, tmp, 2);
    mpz_add(b0, b0, tmp);
    mpz_mul(b1, r, s);
    mpz_mul_ui(b1, b1, 2);

    // (b0+b1 sqrt2)*(2+2sqrt2)=(2b0+4b1)+(2b0+2b1)sqrt2.
    mpz_mul_ui(delta0, b0, 2);
    mpz_mul_ui(tmp, b1, 4);
    mpz_add(delta0, delta0, tmp);
    mpz_sub(delta0, a0, delta0);
    mpz_mul_ui(delta1, b0, 2);
    mpz_mul_ui(tmp, b1, 2);
    mpz_add(delta1, delta1, tmp);
    mpz_sub(delta1, a1, delta1);
    const int dominance = sign_q2(delta0, delta1);
    mpz_clears(p, q, r, s, a0, a1, b0, b1, delta0, delta1, tmp, nullptr);
    if (dominance == 0) fail("unexpected beta-extension sign degeneracy");
    return dominance > 0 ? sa : sb;
}

static Field cutoff_cosh_exact(int cutoff_over_a) {
    // a_B/R=2u, cosh(u)=1+sqrt(2); hence cosh(n a_B/R)=T_{2n}(1+sqrt(2)).
    if (cutoff_over_a < 0 || cutoff_over_a > 12) fail("unsupported integral cutoff");
    Q2 x{1, 1};
    Q2 t0{1, 0}, t1 = x;
    const int degree = 2 * cutoff_over_a;
    if (degree == 0) return one();
    for (int k = 2; k <= degree; ++k) {
        const auto xt = q2_mul(x, t1);
        Q2 next{2 * xt[0] - t0[0], 2 * xt[1] - t0[1]};
        t0 = t1;
        t1 = next;
    }
    if (t1[0] < std::numeric_limits<std::int64_t>::min() ||
        t1[0] > std::numeric_limits<std::int64_t>::max() ||
        t1[1] < std::numeric_limits<std::int64_t>::min() ||
        t1[1] > std::numeric_limits<std::int64_t>::max()) {
        fail("cutoff algebraic value exceeds int64");
    }
    return field_from({checked_i64(t1[0]), checked_i64(t1[1]), 0, 0, 0, 0, 0, 0});
}

static bool inside_cutoff(const Matrix& value, const Field& exact_cutoff,
                          long double numeric_cutoff, std::uint64_t& exact_fallbacks) {
    const long double re = field_value_real(value.a);
    const long double im = field_value_imag(value.a);
    const long double numeric = 2.0L * (re * re + im * im) - 1.0L;
    const long double scale = std::max({1.0L, std::fabs(numeric), std::fabs(numeric_cutoff)});
    const long double guard = 256.0L * std::numeric_limits<long double>::epsilon() * scale;
    if (numeric < numeric_cutoff - guard) return true;
    if (numeric > numeric_cutoff + guard) return false;
    ++exact_fallbacks;
    const Field delta = add(exact_cosh_displacement(value), negate(exact_cutoff));
    return exact_real_field_sign(delta) <= 0;
}

static std::string field_string(const Field& value) {
    std::ostringstream out;
    out << static_cast<int>(value.exp) << ';';
    for (std::size_t i = 0; i < value.c.size(); ++i) {
        if (i) out << ',';
        out << value.c[i];
    }
    return out.str();
}

static std::string csv_escape(const std::string& value) {
    if (value.find_first_of(",\"\n\r") == std::string::npos) return value;
    std::string result = "\"";
    for (const char ch : value) result += ch == '\"' ? "\"\"" : std::string(1, ch);
    result += '\"';
    return result;
}

static std::vector<std::uint8_t> reconstruct_word(std::uint32_t id,
                                                   const std::vector<Meta>& meta) {
    std::vector<std::uint8_t> reverse;
    while (id != 0) {
        reverse.push_back(meta[id].generator);
        id = meta[id].parent;
    }
    return std::vector<std::uint8_t>(reverse.rbegin(), reverse.rend());
}

static std::string geometric_word_string(const std::vector<std::uint8_t>& word) {
    if (word.empty()) return "e";
    std::ostringstream out;
    for (std::size_t i = 0; i < word.size(); ++i) {
        if (i) out << ' ';
        out << 'g' << static_cast<int>(word[i]);
    }
    return out.str();
}

static std::vector<std::uint8_t> presentation_word(const std::vector<std::uint8_t>& word) {
    static const std::array<std::vector<std::uint8_t>, 8> map = {
        std::vector<std::uint8_t>{0},
        std::vector<std::uint8_t>{3},
        std::vector<std::uint8_t>{1, 3, 4},
        std::vector<std::uint8_t>{1, 3, 7},
        std::vector<std::uint8_t>{1},
        std::vector<std::uint8_t>{2},
        std::vector<std::uint8_t>{5, 2, 0},
        std::vector<std::uint8_t>{6, 2, 0},
    };
    std::vector<std::uint8_t> stack;
    for (const auto g : word) {
        for (const auto token : map[g]) {
            if (!stack.empty() && (stack.back() ^ 1U) == token) stack.pop_back();
            else stack.push_back(token);
        }
    }
    return stack;
}

static std::string presentation_word_string(const std::vector<std::uint8_t>& word) {
    static const std::array<const char*, 8> names{
        "a1", "a1_inv", "b1", "b1_inv", "a2", "a2_inv", "b2", "b2_inv"};
    if (word.empty()) return "e";
    std::ostringstream out;
    for (std::size_t i = 0; i < word.size(); ++i) {
        if (i) out << ' ';
        out << names[word[i]];
    }
    return out.str();
}

static Field zeta8() {
    return field_from({0, 1, 0, 0, 0, 1, 0, 0}, 1);
}

static Matrix rotate_c8(Matrix value) {
    value.b = multiply(value.b, zeta8());
    return value;
}

static std::uint64_t peak_working_set_bytes() {
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS_EX counters{};
    counters.cb = sizeof(counters);
    if (GetProcessMemoryInfo(GetCurrentProcess(),
            reinterpret_cast<PROCESS_MEMORY_COUNTERS*>(&counters), sizeof(counters))) {
        return static_cast<std::uint64_t>(counters.PeakWorkingSetSize);
    }
#endif
    return 0;
}

static void write_checkpoint(const fs::path& path, int cutoff, int depth,
                             std::size_t count, std::size_t frontier,
                             std::uint64_t processed, std::uint64_t fallbacks,
                             double seconds, std::uint64_t peak_bytes,
                             bool complete) {
    const fs::path temporary = path.string() + ".tmp";
    std::ofstream out(temporary, std::ios::trunc);
    out << "{\n"
        << "  \"schema_version\": \"1.0\",\n"
        << "  \"cutoff_displacement_over_a_B\": " << cutoff << ",\n"
        << "  \"completed_word_depth\": " << depth << ",\n"
        << "  \"enumerated_elements_in_closed_ball_including_identity\": " << count << ",\n"
        << "  \"current_frontier\": " << frontier << ",\n"
        << "  \"candidate_edges_processed\": " << processed << ",\n"
        << "  \"exact_boundary_fallbacks\": " << fallbacks << ",\n"
        << "  \"elapsed_seconds\": " << std::setprecision(17) << seconds << ",\n"
        << "  \"peak_working_set_bytes\": " << peak_bytes << ",\n"
        << "  \"complete\": " << (complete ? "true" : "false") << "\n"
        << "}\n";
    out.close();
    fs::rename(temporary, path);
}

struct Options {
    fs::path output_dir = "data/production/short_geodesics";
    int cutoff_over_a = 6;
    std::uint64_t maximum_elements = 40000000;
    std::uint64_t reserve_elements = 25000000;
    bool write_csv = true;
    fs::path tree_binary;
};

static Options parse_options(int argc, char** argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        auto require_value = [&]() -> std::string {
            if (++i >= argc) fail("missing value after " + arg);
            return argv[i];
        };
        if (arg == "--output-dir") options.output_dir = require_value();
        else if (arg == "--cutoff-over-a") options.cutoff_over_a = std::stoi(require_value());
        else if (arg == "--maximum-elements") options.maximum_elements = std::stoull(require_value());
        else if (arg == "--reserve-elements") options.reserve_elements = std::stoull(require_value());
        else if (arg == "--count-only") options.write_csv = false;
        else if (arg == "--tree-binary") options.tree_binary = require_value();
        else fail("unknown argument: " + arg);
    }
    if (options.maximum_elements < 1024) fail("maximum-elements is too small");
    options.reserve_elements = std::min(options.reserve_elements, options.maximum_elements);
    return options;
}

int main(int argc, char** argv) {
    try {
        const Options options = parse_options(argc, argv);
        fs::create_directories(options.output_dir);
        const fs::path checkpoint = options.output_dir / "based_enumeration_checkpoint.json";
        const Field exact_cutoff = cutoff_cosh_exact(options.cutoff_over_a);
        const long double root2 = std::sqrt(2.0L);
        const long double a_over_R = 2.0L * std::acosh(1.0L + root2);
        const long double displacement_cutoff = options.cutoff_over_a * a_over_R;
        const long double numeric_cosh_cutoff = std::cosh(displacement_cutoff);

        std::vector<Matrix> matrices;
        std::vector<Meta> meta;
        matrices.reserve(static_cast<std::size_t>(options.reserve_elements));
        meta.reserve(static_cast<std::size_t>(options.reserve_elements));
        ExactIndex index(options.maximum_elements);
        const auto inserted_identity = index.insert(identity_matrix(), matrices);
        if (!inserted_identity.second || inserted_identity.first != 0) fail("identity initialization failed");
        meta.push_back(Meta{});
        std::vector<std::uint32_t> frontier{0}, next;
        std::vector<std::uint64_t> shell_counts{1};
        std::uint64_t processed = 0;
        std::uint64_t exact_fallbacks = 0;
        const auto started = std::chrono::steady_clock::now();
        int depth = 0;

        while (!frontier.empty()) {
            ++depth;
            next.clear();
            next.reserve(frontier.size() * 4);
            for (std::size_t position = 0; position < frontier.size(); ++position) {
                const std::uint32_t parent = frontier[position];
                const std::uint8_t last = meta[parent].generator;
                for (std::uint8_t g = 0; g < 8; ++g) {
                    if (last != 255 && ((g + 4) & 7U) == last) continue;
                    ++processed;
                    const Matrix candidate = matrix_multiply(matrices[parent], generator(g));
                    if (!inside_cutoff(candidate, exact_cutoff, numeric_cosh_cutoff, exact_fallbacks)) continue;
                    const auto inserted = index.insert(candidate, matrices);
                    if (!inserted.second) continue;
                    if (matrices.size() > options.maximum_elements) fail("maximum-elements boundary reached");
                    if (depth > 255) fail("word depth exceeds metadata capacity");
                    meta.push_back(Meta{parent, g, static_cast<std::uint8_t>(depth), 0});
                    next.push_back(inserted.first);
                }
                if ((position + 1) % 1000000 == 0) {
                    const double seconds = std::chrono::duration<double>(
                        std::chrono::steady_clock::now() - started).count();
                    write_checkpoint(checkpoint, options.cutoff_over_a, depth - 1,
                        matrices.size(), next.size(), processed, exact_fallbacks,
                        seconds, peak_working_set_bytes(), false);
                    std::cerr << "depth=" << depth << " processed=" << (position + 1)
                              << '/' << frontier.size() << " elements=" << matrices.size() << '\n';
                }
            }
            shell_counts.push_back(next.size());
            frontier.swap(next);
            const double seconds = std::chrono::duration<double>(
                std::chrono::steady_clock::now() - started).count();
            write_checkpoint(checkpoint, options.cutoff_over_a, depth,
                matrices.size(), frontier.size(), processed, exact_fallbacks,
                seconds, peak_working_set_bytes(), frontier.empty());
            std::cerr << "completed_depth=" << depth << " new=" << frontier.size()
                      << " total=" << matrices.size() << " seconds=" << seconds << '\n';
        }

        const double enumeration_seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();

        if (!options.tree_binary.empty()) {
            if (options.tree_binary.has_parent_path()) {
                fs::create_directories(options.tree_binary.parent_path());
            }
            std::ofstream tree(options.tree_binary, std::ios::binary | std::ios::trunc);
            if (!tree) fail("cannot open tree binary output");
            const std::array<char, 8> magic{'B','O','L','Z','A','T','0','1'};
            const std::uint64_t count = meta.size();
            const std::uint32_t record_size = sizeof(Meta);
            tree.write(magic.data(), static_cast<std::streamsize>(magic.size()));
            tree.write(reinterpret_cast<const char*>(&count), sizeof(count));
            tree.write(reinterpret_cast<const char*>(&record_size), sizeof(record_size));
            tree.write(reinterpret_cast<const char*>(meta.data()),
                       static_cast<std::streamsize>(meta.size() * sizeof(Meta)));
            if (!tree) fail("tree binary write failed");
        }

        if (options.write_csv) {
            const fs::path csv_path = options.output_dir / "dangerous_based.csv";
            std::ofstream csv(csv_path, std::ios::trunc);
            csv << "canonical_id,s8_geometric_reduced_word,s8_presentation_transported_word,"
                   "matrix_a_exact,matrix_b_exact,geometric_word_length,presentation_word_length,"
                   "displacement_over_a_B,translation_length_over_a_B,trace_exact,inverse_id,"
                   "c8_orbit_id,conjugacy_class_id,numerical_error_interval\n";
            csv << std::setprecision(21);
            for (std::uint32_t id = 1; id < matrices.size(); ++id) {
                const auto word = reconstruct_word(id, meta);
                const auto pword = presentation_word(word);
                const Matrix& matrix = matrices[id];
                const long double ar = field_value_real(matrix.a);
                const long double ai = field_value_imag(matrix.a);
                const long double cosh_d = std::max(1.0L, 2.0L * (ar * ar + ai * ai) - 1.0L);
                const long double displacement = std::acosh(cosh_d) / a_over_R;
                const long double half_trace = std::fabs(ar);
                const long double translation = 2.0L * std::acosh(std::max(1.0L, half_trace)) / a_over_R;
                const Field trace = add(matrix.a, conjugate(matrix.a));
                const std::uint32_t inverse_id = index.find(matrix_inverse(matrix), matrices);
                Matrix rotated = matrix;
                std::uint32_t orbit_id = id;
                for (int j = 1; j < 8; ++j) {
                    rotated = rotate_c8(rotated);
                    orbit_id = std::min(orbit_id, index.find(rotated, matrices));
                }
                const long double lower = std::nextafter(displacement,
                    -std::numeric_limits<long double>::infinity());
                const long double upper = std::nextafter(displacement,
                    std::numeric_limits<long double>::infinity());
                std::ostringstream interval;
                interval << std::setprecision(21) << '[' << lower << ',' << upper << ']';
                std::ostringstream cid, iid, oid;
                cid << 'B' << std::setw(8) << std::setfill('0') << id;
                iid << 'B' << std::setw(8) << std::setfill('0') << inverse_id;
                oid << 'O' << std::setw(8) << std::setfill('0') << orbit_id;
                csv << cid.str() << ','
                    << csv_escape(geometric_word_string(word)) << ','
                    << csv_escape(presentation_word_string(pword)) << ','
                    << csv_escape(field_string(matrix.a)) << ','
                    << csv_escape(field_string(matrix.b)) << ','
                    << static_cast<int>(meta[id].depth) << ',' << pword.size() << ','
                    << displacement << ',' << translation << ','
                    << csv_escape(field_string(trace)) << ',' << iid.str() << ','
                    << oid.str() << ",," << csv_escape(interval.str()) << '\n';
                if (id % 1000000 == 0) {
                    std::cerr << "csv_rows=" << id << '/' << (matrices.size() - 1) << '\n';
                }
            }
        }

        const double total_seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        const fs::path summary_path = options.output_dir / "based_enumeration_summary.json";
        std::ofstream summary(summary_path, std::ios::trunc);
        summary << "{\n"
                << "  \"schema_version\": \"1.0\",\n"
                << "  \"scope\": \"exact based obstruction set\",\n"
                << "  \"cutoff_displacement_over_a_B\": " << options.cutoff_over_a << ",\n"
                << "  \"identity_included_in_internal_ball\": true,\n"
                << "  \"dangerous_nonidentity_elements\": " << (matrices.size() - 1) << ",\n"
                << "  \"largest_minimum_geometric_word_length\": " << (depth - 1) << ",\n"
                << "  \"terminal_empty_shell_depth\": " << depth << ",\n"
                << "  \"shell_counts_including_identity_at_depth_zero\": [";
        for (std::size_t i = 0; i < shell_counts.size(); ++i) {
            if (i) summary << ',';
            summary << shell_counts[i];
        }
        summary << "],\n"
                << "  \"candidate_edges_processed\": " << processed << ",\n"
                << "  \"exact_boundary_fallbacks\": " << exact_fallbacks << ",\n"
                << "  \"hash_table_capacity\": " << index.capacity() << ",\n"
                << "  \"enumeration_seconds\": " << std::setprecision(17) << enumeration_seconds << ",\n"
                << "  \"total_seconds\": " << total_seconds << ",\n"
                << "  \"peak_working_set_bytes\": " << peak_working_set_bytes() << ",\n"
                << "  \"complete\": true,\n"
                << "  \"completeness_argument\": \"The regular Bolza octagons are the Dirichlet-Voronoi cells of the orbit of o. For any orbit point p in the closed metric ball B(o,D), the geodesic [o,p] crosses a side-adjacent chain of Voronoi cells. If q is the center of a crossed cell at x, nearest-site inequalities give d(q,x)<=d(p,x), hence d(o,q)<=d(o,x)+d(x,p)=d(o,p)<=D. Thus the induced side-adjacency subgraph on orbit centers in B(o,D) is connected. Exact flood fill from o therefore reaches every such center. The first empty new shell proves termination and completeness.\"\n"
                << "}\n";

        std::cout << "dangerous_nonidentity_elements=" << (matrices.size() - 1)
                  << " largest_word_length=" << (depth - 1)
                  << " enumeration_seconds=" << enumeration_seconds
                  << " total_seconds=" << total_seconds << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }
}
