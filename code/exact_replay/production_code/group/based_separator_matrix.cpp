#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <mutex>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

namespace fs = std::filesystem;

struct Meta {
    std::uint32_t parent;
    std::uint8_t generator;
    std::uint8_t depth;
    std::uint16_t reserved;
};
static_assert(sizeof(Meta) == 8);

struct Candidate {
    std::uint32_t column = 0;
    std::string id;
    std::string family;
    int degree = 0;
    std::uint16_t identity = 0;
    std::array<std::uint16_t, 8> images{};
    int parent_left = -1;
    int parent_right = -1;
};

struct GroupData {
    int degree = 0;
    std::uint16_t order = 0;
    std::vector<std::uint16_t> table;
};

struct OrbitData {
    std::vector<std::uint32_t> element_to_row;
    std::vector<std::uint32_t> representatives;
    std::vector<std::uint32_t> weights;
};

[[noreturn]] static void fail(const std::string& message) {
    throw std::runtime_error(message);
}

static std::vector<std::string> split_tab(const std::string& line) {
    std::vector<std::string> fields;
    std::size_t start = 0;
    while (true) {
        const auto end = line.find('\t', start);
        fields.push_back(line.substr(start, end == std::string::npos ? end : end - start));
        if (end == std::string::npos) break;
        start = end + 1;
    }
    return fields;
}

static std::vector<Candidate> load_manifest(const fs::path& path) {
    std::ifstream input(path);
    if (!input) fail("cannot open candidate manifest: " + path.string());
    std::string line;
    if (!std::getline(input, line)) fail("empty candidate manifest");
    const auto header = split_tab(line);
    if (header.size() != 15 || header[0] != "column_index" || header[5] != "g0") {
        fail("unexpected candidate manifest header");
    }
    std::vector<Candidate> candidates;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        const auto fields = split_tab(line);
        if (fields.size() != 15) fail("candidate manifest row has wrong width");
        Candidate candidate;
        candidate.column = static_cast<std::uint32_t>(std::stoul(fields[0]));
        candidate.id = fields[1];
        candidate.family = fields[2];
        candidate.degree = std::stoi(fields[3]);
        candidate.identity = static_cast<std::uint16_t>(std::stoi(fields[4]));
        for (int i = 0; i < 8; ++i) candidate.images[i] = static_cast<std::uint16_t>(std::stoi(fields[5 + i]));
        candidate.parent_left = std::stoi(fields[13]);
        candidate.parent_right = std::stoi(fields[14]);
        if (candidate.column != candidates.size()) fail("candidate columns are not contiguous");
        candidates.push_back(std::move(candidate));
    }
    if (candidates.size() != 1182) fail("expected 1182 registered candidate columns");
    return candidates;
}

static std::vector<Meta> load_tree(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) fail("cannot open tree binary: " + path.string());
    std::array<char, 8> magic{};
    std::uint64_t count = 0;
    std::uint32_t record_size = 0;
    input.read(magic.data(), magic.size());
    input.read(reinterpret_cast<char*>(&count), sizeof(count));
    input.read(reinterpret_cast<char*>(&record_size), sizeof(record_size));
    if (std::string(magic.data(), magic.size()) != "BOLZAT01" || record_size != sizeof(Meta)) {
        fail("bad tree binary header");
    }
    if (count != 23129593ULL) fail("tree count differs from exact based certificate");
    std::vector<Meta> meta(static_cast<std::size_t>(count));
    input.read(reinterpret_cast<char*>(meta.data()), static_cast<std::streamsize>(meta.size() * sizeof(Meta)));
    if (!input) fail("short tree binary read");
    if (meta[0].parent != 0 || meta[0].generator != 255 || meta[0].depth != 0) fail("bad tree identity record");
    for (std::size_t id = 1; id < meta.size(); ++id) {
        if (meta[id].parent >= id || meta[id].generator >= 8 || meta[id].depth == 0) fail("invalid tree edge");
        if (meta[id].depth != static_cast<std::uint8_t>(meta[meta[id].parent].depth + 1)) fail("tree depth mismatch");
    }
    return meta;
}

static std::uint32_t parse_prefixed_id(const char* begin, const char* end, char prefix) {
    if (begin == end || *begin != prefix) fail("bad prefixed ID in based CSV");
    std::uint32_t value = 0;
    for (const char* p = begin + 1; p != end; ++p) {
        if (*p < '0' || *p > '9') fail("nondigit in based CSV ID");
        value = value * 10U + static_cast<std::uint32_t>(*p - '0');
    }
    return value;
}

static std::uint32_t parse_uint(const char* begin, const char* end) {
    if (begin == end) fail("empty unsigned integer field");
    std::uint32_t value = 0;
    for (const char* p = begin; p != end; ++p) {
        if (*p < '0' || *p > '9') fail("nondigit in unsigned field");
        value = value * 10U + static_cast<std::uint32_t>(*p - '0');
    }
    return value;
}

struct CsvNeeded {
    std::uint32_t canonical = 0;
    std::uint32_t depth = 0;
    std::uint32_t inverse = 0;
    std::uint32_t c8_orbit = 0;
};

static CsvNeeded parse_needed_csv_fields(const std::string& line) {
    std::array<std::pair<const char*, const char*>, 4> slices{};
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
            else if (field == 10) slot = 2;
            else if (field == 11) slot = 3;
            if (slot >= 0) {
                slices[slot] = {start, data + i};
                ++captured;
            }
            ++field;
            start = data + i + 1;
            if (field > 11 && captured == 4) break;
        }
    }
    if (captured != 4) fail("could not parse needed based CSV fields");
    return CsvNeeded{
        parse_prefixed_id(slices[0].first, slices[0].second, 'B'),
        parse_uint(slices[1].first, slices[1].second),
        parse_prefixed_id(slices[2].first, slices[2].second, 'B'),
        parse_prefixed_id(slices[3].first, slices[3].second, 'O'),
    };
}

static OrbitData build_orbits(const fs::path& csv_path, const std::vector<Meta>& meta) {
    const std::size_t count = meta.size();
    std::vector<std::uint32_t> inverse(count, 0), c8(count, 0);
    std::ifstream input(csv_path);
    if (!input) fail("cannot open based CSV: " + csv_path.string());
    std::vector<char> buffer(16U << 20U);
    input.rdbuf()->pubsetbuf(buffer.data(), static_cast<std::streamsize>(buffer.size()));
    std::string line;
    if (!std::getline(input, line) || line.rfind("canonical_id,", 0) != 0) fail("bad based CSV header");
    std::uint32_t expected = 1;
    while (std::getline(input, line)) {
        const auto fields = parse_needed_csv_fields(line);
        if (fields.canonical != expected) fail("based CSV IDs are not contiguous");
        if (fields.depth != meta[expected].depth) fail("CSV/tree depth mismatch");
        if (fields.inverse >= count || fields.c8_orbit >= count) fail("based CSV link outside exact set");
        inverse[expected] = fields.inverse;
        c8[expected] = fields.c8_orbit;
        if (expected % 1000000U == 0) std::cerr << "orbit_csv_rows=" << expected << '/' << (count - 1) << '\n';
        ++expected;
    }
    if (expected != count) fail("based CSV row count mismatch");

    std::vector<std::uint32_t> row_by_rep(count, std::numeric_limits<std::uint32_t>::max());
    OrbitData result;
    result.element_to_row.resize(count, std::numeric_limits<std::uint32_t>::max());
    result.representatives.reserve((count - 1) / 12);
    result.weights.reserve((count - 1) / 12);
    for (std::uint32_t id = 1; id < count; ++id) {
        const std::uint32_t inv = inverse[id];
        if (inverse[inv] != id) fail("inverse links are not involutive");
        const std::uint32_t representative = std::min(c8[id], c8[inv]);
        auto& row = row_by_rep[representative];
        if (row == std::numeric_limits<std::uint32_t>::max()) {
            row = static_cast<std::uint32_t>(result.representatives.size());
            result.representatives.push_back(representative);
            result.weights.push_back(0);
        }
        result.element_to_row[id] = row;
        ++result.weights[row];
    }
    for (const auto weight : result.weights) {
        if (weight == 0 || weight > 16) fail("unexpected inversion/C8 orbit weight");
    }
    return result;
}

static std::uint16_t permutation_rank(const std::array<std::uint8_t, 6>& permutation, int degree) {
    static constexpr std::array<int, 7> factorial{1, 1, 2, 6, 24, 120, 720};
    int rank = 0;
    for (int i = 0; i < degree; ++i) {
        int smaller = 0;
        for (int j = i + 1; j < degree; ++j) smaller += permutation[j] < permutation[i];
        rank += smaller * factorial[degree - 1 - i];
    }
    return static_cast<std::uint16_t>(rank);
}

static GroupData make_symmetric_group(int degree) {
    if (degree < 4 || degree > 6) fail("unsupported symmetric-group degree");
    std::array<std::uint8_t, 6> current{};
    std::iota(current.begin(), current.end(), static_cast<std::uint8_t>(0));
    std::vector<std::array<std::uint8_t, 6>> permutations;
    do {
        permutations.push_back(current);
    } while (std::next_permutation(current.begin(), current.begin() + degree));
    GroupData group;
    group.degree = degree;
    group.order = static_cast<std::uint16_t>(permutations.size());
    group.table.resize(static_cast<std::size_t>(group.order) * group.order);
    for (std::uint16_t left = 0; left < group.order; ++left) {
        for (std::uint16_t right = 0; right < group.order; ++right) {
            std::array<std::uint8_t, 6> composed{};
            for (int i = 0; i < degree; ++i) composed[i] = permutations[left][permutations[right][i]];
            for (int i = degree; i < 6; ++i) composed[i] = static_cast<std::uint8_t>(i);
            group.table[static_cast<std::size_t>(left) * group.order + right] = permutation_rank(composed, degree);
        }
    }
    return group;
}

static const GroupData& group_for_degree(const std::array<GroupData, 3>& groups, int degree) {
    return groups.at(static_cast<std::size_t>(degree - 4));
}

static std::vector<std::uint32_t> evaluate_single(
    const Candidate& candidate,
    const GroupData& group,
    const std::vector<Meta>& meta,
    const OrbitData& orbits
) {
    if (candidate.identity >= group.order) fail("candidate identity outside base group");
    for (const auto image : candidate.images) if (image >= group.order) fail("candidate image outside base group");
    std::vector<std::uint16_t> state(meta.size());
    std::vector<std::uint8_t> base_kernel_counts(orbits.weights.size(), 0);
    state[0] = candidate.identity;
    for (std::uint32_t id = 1; id < meta.size(); ++id) {
        const auto edge = meta[id];
        const std::uint16_t value = group.table[
            static_cast<std::size_t>(state[edge.parent]) * group.order + candidate.images[edge.generator]
        ];
        state[id] = value;
        if (value == candidate.identity && (edge.depth & 1U) == 0) {
            auto& count = base_kernel_counts[orbits.element_to_row[id]];
            if (count == std::numeric_limits<std::uint8_t>::max()) fail("orbit count overflow");
            ++count;
        }
    }
    std::vector<std::uint32_t> zeros;
    zeros.reserve(orbits.weights.size() / std::max<int>(2, group.order));
    for (std::uint32_t row = 0; row < orbits.weights.size(); ++row) {
        if (base_kernel_counts[row] == orbits.weights[row]) zeros.push_back(row);
    }
    return zeros;
}

static std::vector<std::uint32_t> intersect_sorted(
    const std::vector<std::uint32_t>& left,
    const std::vector<std::uint32_t>& right
) {
    std::vector<std::uint32_t> out;
    out.reserve(std::min(left.size(), right.size()));
    std::set_intersection(left.begin(), left.end(), right.begin(), right.end(), std::back_inserter(out));
    return out;
}

static bool disjoint_sorted(const std::vector<std::uint32_t>& left,
                            const std::vector<std::uint32_t>& right) {
    std::size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] == right[j]) return false;
        if (left[i] < right[j]) ++i;
        else ++j;
    }
    return true;
}

static std::uint64_t weighted_count(const std::vector<std::uint32_t>& rows,
                                    const std::vector<std::uint32_t>& weights) {
    std::uint64_t result = 0;
    for (const auto row : rows) result += weights[row];
    return result;
}

static void write_orbit_binary(const fs::path& path, const OrbitData& orbits) {
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out) fail("cannot write orbit binary");
    const std::array<char, 8> magic{'B','O','L','Z','A','O','0','1'};
    const std::uint64_t elements = orbits.element_to_row.size();
    const std::uint64_t rows = orbits.weights.size();
    out.write(magic.data(), magic.size());
    out.write(reinterpret_cast<const char*>(&elements), sizeof(elements));
    out.write(reinterpret_cast<const char*>(&rows), sizeof(rows));
    out.write(reinterpret_cast<const char*>(orbits.element_to_row.data()),
              static_cast<std::streamsize>(orbits.element_to_row.size() * sizeof(std::uint32_t)));
    out.write(reinterpret_cast<const char*>(orbits.representatives.data()),
              static_cast<std::streamsize>(orbits.representatives.size() * sizeof(std::uint32_t)));
    out.write(reinterpret_cast<const char*>(orbits.weights.data()),
              static_cast<std::streamsize>(orbits.weights.size() * sizeof(std::uint32_t)));
    if (!out) fail("orbit binary write failed");
}

static void write_kernel_csc(
    const fs::path& path,
    std::uint64_t rows,
    const std::vector<std::vector<std::uint32_t>>& zeros
) {
    std::vector<std::uint64_t> indptr(zeros.size() + 1, 0);
    for (std::size_t i = 0; i < zeros.size(); ++i) indptr[i + 1] = indptr[i] + zeros[i].size();
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out) fail("cannot write kernel CSC binary");
    const std::array<char, 8> magic{'B','O','L','Z','A','K','0','1'};
    const std::uint64_t columns = zeros.size();
    const std::uint64_t nnz = indptr.back();
    out.write(magic.data(), magic.size());
    out.write(reinterpret_cast<const char*>(&rows), sizeof(rows));
    out.write(reinterpret_cast<const char*>(&columns), sizeof(columns));
    out.write(reinterpret_cast<const char*>(&nnz), sizeof(nnz));
    out.write(reinterpret_cast<const char*>(indptr.data()),
              static_cast<std::streamsize>(indptr.size() * sizeof(std::uint64_t)));
    for (const auto& column : zeros) {
        out.write(reinterpret_cast<const char*>(column.data()),
                  static_cast<std::streamsize>(column.size() * sizeof(std::uint32_t)));
    }
    if (!out) fail("kernel CSC binary write failed");
}

static std::string json_escape(const std::string& value) {
    std::ostringstream out;
    for (const unsigned char ch : value) {
        if (ch == '"' || ch == '\\') out << '\\' << ch;
        else if (ch >= 0x20) out << ch;
    }
    return out.str();
}

int main(int argc, char** argv) {
    try {
        fs::path root = "D:/work/revise";
        unsigned threads = std::min(8U, std::max(1U, std::thread::hardware_concurrency()));
        for (int i = 1; i < argc; ++i) {
            const std::string arg = argv[i];
            if (arg == "--root" && i + 1 < argc) root = argv[++i];
            else if (arg == "--threads" && i + 1 < argc) threads = static_cast<unsigned>(std::stoul(argv[++i]));
            else fail("usage: based_separator_matrix [--root PATH] [--threads N]");
        }
        if (threads == 0 || threads > 16) fail("thread count must be 1..16");
        const fs::path output = root / "data/production/quotient_separator";
        fs::create_directories(output);
        const auto candidates = load_manifest(output / "candidate_manifest.tsv");
        const auto meta = load_tree(output / "based_tree_meta.bin");
        std::cerr << "tree_loaded=" << meta.size() << '\n';
        const auto orbits = build_orbits(root / "data/production/short_geodesics/dangerous_based.csv", meta);
        std::cerr << "symmetry_orbits=" << orbits.weights.size() << '\n';
        write_orbit_binary(output / "based_orbit_map.bin", orbits);

        const std::array<GroupData, 3> groups{
            make_symmetric_group(4), make_symmetric_group(5), make_symmetric_group(6)
        };
        for (const auto& group : groups) std::cerr << "S" << group.degree << "_order=" << group.order << '\n';

        std::size_t singles = 0;
        while (singles < candidates.size() && candidates[singles].degree > 0) ++singles;
        if (singles != 1158) fail("unexpected single-map count/order");
        std::vector<std::vector<std::uint32_t>> zeros(candidates.size());
        std::atomic<std::size_t> next{0};
        std::atomic<std::size_t> complete{0};
        std::mutex io_mutex;
        auto worker = [&]() {
            while (true) {
                const std::size_t index = next.fetch_add(1);
                if (index >= singles) return;
                const auto& candidate = candidates[index];
                zeros[index] = evaluate_single(candidate, group_for_degree(groups, candidate.degree), meta, orbits);
                const std::size_t done = complete.fetch_add(1) + 1;
                if (done % 10 == 0 || done == singles) {
                    std::lock_guard<std::mutex> lock(io_mutex);
                    std::cerr << "candidate_columns=" << done << '/' << singles << '\n';
                }
            }
        };
        std::vector<std::thread> pool;
        for (unsigned i = 0; i < threads; ++i) pool.emplace_back(worker);
        for (auto& thread : pool) thread.join();

        for (std::size_t index = singles; index < candidates.size(); ++index) {
            const auto& candidate = candidates[index];
            if (candidate.parent_left < 0 || candidate.parent_right < 0 ||
                candidate.parent_left >= static_cast<int>(index) || candidate.parent_right >= static_cast<int>(index)) {
                fail("bad composite parent indices");
            }
            zeros[index] = intersect_sorted(zeros[candidate.parent_left], zeros[candidate.parent_right]);
        }

        std::vector<std::uint32_t> uncovered = zeros.front();
        for (std::size_t index = 1; index < zeros.size() && !uncovered.empty(); ++index) {
            uncovered = intersect_sorted(uncovered, zeros[index]);
        }

        std::vector<std::size_t> selected;
        std::string solution_status;
        auto empty_single = std::find_if(zeros.begin(), zeros.end(), [](const auto& value) { return value.empty(); });
        if (empty_single != zeros.end()) {
            selected.push_back(static_cast<std::size_t>(std::distance(zeros.begin(), empty_single)));
            solution_status = "OPTIMAL";
        } else {
            bool pair_found = false;
            std::vector<std::size_t> order(zeros.size());
            std::iota(order.begin(), order.end(), 0);
            std::sort(order.begin(), order.end(), [&](auto a, auto b) { return zeros[a].size() < zeros[b].size(); });
            for (std::size_t oi = 0; oi < order.size() && !pair_found; ++oi) {
                for (std::size_t oj = oi + 1; oj < order.size(); ++oj) {
                    if (disjoint_sorted(zeros[order[oi]], zeros[order[oj]])) {
                        selected = {order[oi], order[oj]};
                        pair_found = true;
                        break;
                    }
                }
            }
            if (pair_found) {
                solution_status = "OPTIMAL";
            } else {
                selected.push_back(order.front());
                std::vector<std::uint32_t> remaining = zeros[order.front()];
                while (!remaining.empty()) {
                    std::size_t best = zeros.size();
                    std::vector<std::uint32_t> best_intersection = remaining;
                    for (std::size_t index = 0; index < zeros.size(); ++index) {
                        if (std::find(selected.begin(), selected.end(), index) != selected.end()) continue;
                        auto trial = intersect_sorted(remaining, zeros[index]);
                        if (trial.size() < best_intersection.size()) {
                            best = index;
                            best_intersection.swap(trial);
                            if (best_intersection.empty()) break;
                        }
                    }
                    if (best == zeros.size()) break;
                    selected.push_back(best);
                    remaining.swap(best_intersection);
                }
                solution_status = remaining.empty() ? "CERTIFIED COMPLETE BUT NOT PROVEN MINIMAL" : "NO COMPLETE COVER";
            }
        }

        write_kernel_csc(output / "separator_kernel_exceptions.cscbin", orbits.weights.size(), zeros);
        std::ofstream counts(output / "candidate_kernel_counts.csv", std::ios::trunc);
        counts << "column_index,candidate_id,family,base_degree,kernel_orbit_rows,kernel_elements,separated_elements\n";
        for (std::size_t index = 0; index < candidates.size(); ++index) {
            const auto kernel_elements = weighted_count(zeros[index], orbits.weights);
            counts << index << ',' << candidates[index].id << ',' << candidates[index].family << ','
                   << candidates[index].degree << ',' << zeros[index].size() << ',' << kernel_elements << ','
                   << (meta.size() - 1 - kernel_elements) << '\n';
        }

        const std::uint64_t uncovered_elements = weighted_count(uncovered, orbits.weights);
        const std::uint64_t total_exceptions = std::accumulate(
            zeros.begin(), zeros.end(), std::uint64_t{0},
            [](std::uint64_t sum, const auto& column) { return sum + column.size(); }
        );
        std::ofstream solution(output / "based_separator_solution.json", std::ios::trunc);
        solution << "{\n"
                 << "  \"schema_version\": \"1.0\",\n"
                 << "  \"task_id\": \"PF-GRP-001-Q-GEO-SEP-BASED\",\n"
                 << "  \"scope\": \"exact based obstruction set only\",\n"
                 << "  \"dangerous_elements\": " << (meta.size() - 1) << ",\n"
                 << "  \"symmetry_orbit_rows\": " << orbits.weights.size() << ",\n"
                 << "  \"candidate_columns\": " << candidates.size() << ",\n"
                 << "  \"single_base_maps_evaluated\": " << singles << ",\n"
                 << "  \"composite_columns_derived_exactly\": " << (candidates.size() - singles) << ",\n"
                 << "  \"matrix_encoding\": \"default-one separator matrix with CSC zero/kernel exceptions and exact element-to-orbit expansion\",\n"
                 << "  \"kernel_exception_orbit_entries\": " << total_exceptions << ",\n"
                 << "  \"all_candidates_uncovered_orbit_rows\": " << uncovered.size() << ",\n"
                 << "  \"all_candidates_uncovered_elements\": " << uncovered_elements << ",\n"
                 << "  \"solution_status\": \"" << solution_status << "\",\n"
                 << "  \"selected_columns\": [";
        for (std::size_t i = 0; i < selected.size(); ++i) {
            if (i) solution << ',';
            solution << selected[i];
        }
        solution << "],\n  \"selected_candidate_ids\": [";
        for (std::size_t i = 0; i < selected.size(); ++i) {
            if (i) solution << ',';
            solution << '"' << json_escape(candidates[selected[i]].id) << '"';
        }
        solution << "],\n"
                 << "  \"global_scope_evaluated\": false,\n"
                 << "  \"main_tex_modified\": false\n"
                 << "}\n";

        std::cout << "dangerous_elements=" << (meta.size() - 1)
                  << " symmetry_orbits=" << orbits.weights.size()
                  << " candidates=" << candidates.size()
                  << " exception_entries=" << total_exceptions
                  << " uncovered_elements=" << uncovered_elements
                  << " solution=" << solution_status
                  << " selected=" << selected.size() << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }
}
