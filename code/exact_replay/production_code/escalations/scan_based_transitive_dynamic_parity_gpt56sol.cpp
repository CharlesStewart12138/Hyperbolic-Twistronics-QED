#include <algorithm>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

// Independent verifier/scanner for generic-degree GAP CANDIDATE_NUMERIC
// records. It reconstructs the generated image, verifies eight distinct
// physical directions, inverse pairs, the frozen relator, exact B3=457,
// target order, and existence of the all-generators-odd C2 coloring. It then
// evaluates the complete certified 23,129,593-node based tree and returns the
// first (therefore shortest in tree order) even identity word.
namespace {
struct Meta {
  std::uint32_t parent;
  std::uint8_t generator, depth;
  std::uint16_t reserved;
};
static_assert(sizeof(Meta) == 8);

using Perm = std::vector<std::uint8_t>;
struct PermHash {
  std::size_t operator()(const Perm& p) const noexcept {
    std::uint64_t h = 1469598103934665603ULL;
    for (auto x : p) {
      h ^= x;
      h *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(h);
  }
};

struct Candidate {
  std::string group;
  int alpha = 0, rep = 0, order = 0, degree = 0;
  std::vector<Perm> images;
};

Perm one(int degree) {
  Perm p(static_cast<std::size_t>(degree));
  for (int i = 0; i < degree; ++i) p[i] = static_cast<std::uint8_t>(i);
  return p;
}

Perm mul(const Perm& a, const Perm& b) {
  if (a.size() != b.size()) throw std::runtime_error("degree mismatch");
  Perm c(a.size());
  for (std::size_t i = 0; i < a.size(); ++i) c[i] = b[a[i]];
  return c;
}

Perm inv(const Perm& a) {
  Perm b(a.size());
  for (std::size_t i = 0; i < a.size(); ++i) b[a[i]] = static_cast<std::uint8_t>(i);
  return b;
}

bool parse_int_token(const std::string& s, int& value) {
  const char* begin = s.data();
  const char* end = begin + s.size();
  auto result = std::from_chars(begin, end, value);
  return result.ec == std::errc{} && result.ptr == end;
}

int next_int(std::istream& in) {
  std::string token;
  int value;
  while (in >> token) {
    if (parse_int_token(token, value)) return value;
  }
  throw std::runtime_error("short numeric record");
}

std::vector<Candidate> load_candidates(int argc, char** argv) {
  std::vector<Candidate> out;
  std::set<std::tuple<std::string, int, int>> seen;
  for (int file_no = 1; file_no < argc - 1; ++file_no) {
    std::ifstream in(argv[file_no]);
    if (!in) throw std::runtime_error("cannot open candidate file");
    std::string token;
    while (in >> token) {
      if (token != "CANDIDATE_NUMERIC") continue;
      Candidate c;
      in >> c.group;
      c.alpha = next_int(in);
      c.rep = next_int(in);
      c.order = next_int(in);
      c.degree = next_int(in);
      if (c.degree < 1 || c.degree > 255) throw std::runtime_error("bad degree");
      c.images.assign(8, Perm(static_cast<std::size_t>(c.degree)));
      for (auto& p : c.images) {
        for (auto& x : p) {
          int z = next_int(in);
          if (z < 0 || z >= c.degree) throw std::runtime_error("bad permutation entry");
          x = static_cast<std::uint8_t>(z);
        }
      }
      if (!seen.emplace(c.group, c.alpha, c.rep).second)
        throw std::runtime_error("duplicate candidate identifier");
      out.push_back(std::move(c));
    }
  }
  return out;
}

std::vector<Meta> load_tree(const std::string& path) {
  std::ifstream in(path, std::ios::binary);
  if (!in) throw std::runtime_error("cannot open based tree");
  char magic[8]{};
  std::uint64_t count = 0;
  std::uint32_t record_size = 0;
  in.read(magic, 8);
  in.read(reinterpret_cast<char*>(&count), 8);
  in.read(reinterpret_cast<char*>(&record_size), 4);
  if (std::string(magic, 8) != "BOLZAT01" || count != 23'129'593ULL ||
      record_size != sizeof(Meta))
    throw std::runtime_error("tree contract drift");
  std::vector<Meta> tree(count);
  in.read(reinterpret_cast<char*>(tree.data()),
          static_cast<std::streamsize>(tree.size() * sizeof(Meta)));
  if (!in) throw std::runtime_error("short tree");
  return tree;
}

std::size_t b3(const std::vector<Perm>& images) {
  const auto identity = one(static_cast<int>(images[0].size()));
  std::set<Perm> values{identity};
  std::vector<std::pair<Perm, int>> frontier{{identity, -1}};
  for (int depth = 1; depth <= 3; ++depth) {
    std::vector<std::pair<Perm, int>> next;
    for (const auto& item : frontier) {
      for (int generator = 0; generator < 8; ++generator) {
        if (item.second >= 0 && generator == (item.second + 4) % 8) continue;
        auto z = mul(item.first, images[generator]);
        values.insert(z);
        next.push_back({std::move(z), generator});
      }
    }
    frontier = std::move(next);
  }
  return values.size();
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc < 3)
      throw std::runtime_error("usage: CERTIFICATE... BASED_TREE_META_BIN");
    const auto candidates = load_candidates(argc, argv);
    std::cout << "candidates=" << candidates.size() << '\n';
    if (candidates.empty()) return 0;
    const auto tree = load_tree(argv[argc - 1]);

    for (const auto& c : candidates) {
      const auto identity = one(c.degree);
      if (std::set<Perm>(c.images.begin(), c.images.end()).size() != 8)
        throw std::runtime_error("orbit distinctness failure");
      for (int i = 0; i < 4; ++i) {
        if (c.images[i + 4] != inv(c.images[i]))
          throw std::runtime_error("inverse failure");
      }
      Perm relator = identity;
      for (int generator : std::vector<int>{0, 5, 2, 7, 4, 1, 6, 3})
        relator = mul(relator, c.images[generator]);
      if (relator != identity) throw std::runtime_error("relator failure");
      const auto b3_count = b3(c.images);
      if (b3_count != 457) throw std::runtime_error("B3 failure");

      std::vector<Perm> elements{identity};
      std::unordered_map<Perm, std::uint16_t, PermHash> index;
      index.reserve(50000);
      index.emplace(identity, 0);
      std::vector<std::vector<std::uint16_t>> transition;
      transition.reserve(static_cast<std::size_t>(c.order));
      std::vector<std::uint8_t> parity{0};
      bool parity_consistent = true;
      for (std::size_t h = 0; h < elements.size(); ++h) {
        std::vector<std::uint16_t> row(8);
        for (int generator = 0; generator < 8; ++generator) {
          auto z = mul(elements[h], c.images[generator]);
          auto it = index.find(z);
          std::uint16_t j;
          if (it == index.end()) {
            if (elements.size() >= 65536)
              throw std::runtime_error("uint16 overflow");
            j = static_cast<std::uint16_t>(elements.size());
            index.emplace(z, j);
            elements.push_back(std::move(z));
            parity.push_back(static_cast<std::uint8_t>(parity[h] ^ 1U));
          } else {
            j = it->second;
            if (parity[j] != static_cast<std::uint8_t>(parity[h] ^ 1U))
              parity_consistent = false;
          }
          row[generator] = j;
        }
        transition.push_back(std::move(row));
      }
      if (static_cast<int>(elements.size()) != c.order)
        throw std::runtime_error("generated order failure");
      if (!parity_consistent)
        throw std::runtime_error("all-generators-odd parity coloring failure");

      std::vector<std::uint16_t> state(tree.size());
      std::uint32_t witness = 0;
      for (std::uint32_t i = 1; i < tree.size(); ++i) {
        const auto edge = tree[i];
        if (edge.parent >= i || edge.generator >= 8)
          throw std::runtime_error("bad tree edge");
        state[i] = transition[state[edge.parent]][edge.generator];
        if ((edge.depth & 1U) == 0U && state[i] == 0) {
          witness = i;
          break;
        }
      }

      std::cout << c.group << " alpha=" << c.alpha << " rep=" << c.rep
                << " degree=" << c.degree << " order=" << c.order
                << " distinct=8 inverse=1 relator=1 b3=" << b3_count
                << " generated=1 parity=1";
      if (!witness) {
        std::cout << " BASED_PASS\n";
        continue;
      }
      std::vector<unsigned> word;
      for (auto i = witness; i; i = tree[i].parent)
        word.push_back(tree[i].generator);
      std::reverse(word.begin(), word.end());
      std::cout << " BASED_FAIL witness_id=" << witness
                << " depth=" << static_cast<unsigned>(tree[witness].depth)
                << " word=";
      for (std::size_t i = 0; i < word.size(); ++i)
        std::cout << (i ? " " : "") << 'g' << word[i];
      std::cout << '\n';
    }
    return 0;
  } catch (const std::exception& e) {
    std::cerr << "ERROR: " << e.what() << '\n';
    return 2;
  }
}
