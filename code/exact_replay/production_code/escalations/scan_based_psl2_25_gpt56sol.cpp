#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

struct Meta {
  std::uint32_t parent;
  std::uint8_t generator;
  std::uint8_t depth;
  std::uint16_t reserved;
};
static_assert(sizeof(Meta) == 8);

using Matrix = std::array<std::uint8_t, 4>;

struct F25 {
  std::array<std::array<std::uint8_t, 25>, 25> add{}, mul{};
  std::array<std::uint8_t, 25> neg{}, inv{}, frob{};

  F25() {
    for (int x = 0; x < 25; ++x) {
      const int a = x % 5, b = x / 5;
      neg[x] = static_cast<std::uint8_t>((-a + 5) % 5 + 5 * ((-b + 5) % 5));
      for (int y = 0; y < 25; ++y) {
        const int c = y % 5, d = y / 5;
        add[x][y] = static_cast<std::uint8_t>((a + c) % 5 + 5 * ((b + d) % 5));
        mul[x][y] = static_cast<std::uint8_t>((a * c + 3 * b * d) % 5 + 5 * ((a * d + b * c) % 5));
      }
    }
    for (int x = 1; x < 25; ++x) {
      for (int y = 1; y < 25; ++y) if (mul[x][y] == 1) { inv[x] = static_cast<std::uint8_t>(y); break; }
      if (inv[x] == 0) throw std::runtime_error("F25 inverse failure");
    }
    for (int x = 0; x < 25; ++x) frob[x] = power(static_cast<std::uint8_t>(x), 5);
  }

  std::uint8_t power(std::uint8_t x, unsigned n) const {
    std::uint8_t r = 1;
    while (n) { if (n & 1U) r = mul[r][x]; x = mul[x][x]; n >>= 1U; }
    return r;
  }

  Matrix normalize(Matrix x) const {
    const auto it = std::find_if(x.begin(), x.end(), [](auto v) { return v != 0; });
    if (it == x.end()) throw std::runtime_error("zero projective matrix");
    const auto scale = inv[*it];
    for (auto& v : x) v = mul[v][scale];
    return x;
  }

  std::uint8_t determinant(const Matrix& x) const {
    return add[mul[x[0]][x[3]]][neg[mul[x[1]][x[2]]]];
  }

  Matrix multiply(const Matrix& x, const Matrix& y) const {
    return normalize({
      add[mul[x[0]][y[0]]][mul[x[1]][y[2]]],
      add[mul[x[0]][y[1]]][mul[x[1]][y[3]]],
      add[mul[x[2]][y[0]]][mul[x[3]][y[2]]],
      add[mul[x[2]][y[1]]][mul[x[3]][y[3]]]
    });
  }

  Matrix inverse(const Matrix& x) const { return normalize({x[3], neg[x[1]], neg[x[2]], x[0]}); }
  Matrix sigma(const Matrix& x) const { return {frob[x[0]], frob[x[1]], frob[x[2]], frob[x[3]]}; }
  Matrix semilinear_action(const Matrix& c, const Matrix& x) const {
    return multiply(multiply(c, sigma(x)), inverse(c));
  }
};

std::uint32_t pack(const Matrix& x) {
  return static_cast<std::uint32_t>(x[0]) | (static_cast<std::uint32_t>(x[1]) << 5U)
       | (static_cast<std::uint32_t>(x[2]) << 10U) | (static_cast<std::uint32_t>(x[3]) << 15U);
}

std::vector<Meta> load_tree(const std::string& path) {
  std::ifstream in(path, std::ios::binary);
  if (!in) throw std::runtime_error("cannot open based tree");
  char magic[8]{}; std::uint64_t count = 0; std::uint32_t size = 0;
  in.read(magic, 8); in.read(reinterpret_cast<char*>(&count), 8); in.read(reinterpret_cast<char*>(&size), 4);
  if (std::string(magic, 8) != "BOLZAT01" || count != 23'129'593ULL || size != sizeof(Meta))
    throw std::runtime_error("based tree contract drift");
  std::vector<Meta> result(static_cast<std::size_t>(count));
  in.read(reinterpret_cast<char*>(result.data()), static_cast<std::streamsize>(result.size() * sizeof(Meta)));
  if (!in) throw std::runtime_error("short based tree");
  return result;
}

} // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("usage: BASED_TREE_META_BIN");
    const F25 f;
    const Matrix identity{1,0,0,1};
    const Matrix alpha_conjugator{0,1,5,5};
    const std::array<Matrix, 6> seeds{{
      {{0,1,19,20}}, {{0,1,23,7}}, {{1,2,6,23}},
      {{1,2,20,22}}, {{1,4,10,22}}, {{1,8,21,9}}
    }};

    std::set<std::uint32_t> psl_keys;
    for (int a=0;a<25;++a) for(int b=0;b<25;++b) for(int c=0;c<25;++c) for(int d=0;d<25;++d) {
      Matrix x{static_cast<std::uint8_t>(a),static_cast<std::uint8_t>(b),static_cast<std::uint8_t>(c),static_cast<std::uint8_t>(d)};
      if (f.determinant(x) == 0) continue;
      x = f.normalize(x);
      if (f.power(f.determinant(x), 12) == 1) psl_keys.insert(pack(x));
    }
    if (psl_keys.size() != 7800) throw std::runtime_error("PSL(2,25) order drift");
    std::vector<Matrix> elements;
    std::unordered_map<std::uint32_t, std::uint16_t> index;
    for (auto key : psl_keys) {
      Matrix x{static_cast<std::uint8_t>(key & 31U), static_cast<std::uint8_t>((key >> 5U) & 31U),
               static_cast<std::uint8_t>((key >> 10U) & 31U), static_cast<std::uint8_t>((key >> 15U) & 31U)};
      index.emplace(key, static_cast<std::uint16_t>(elements.size())); elements.push_back(x);
    }
    const auto identity_index = index.at(pack(identity));
    const auto tree = load_tree(argv[1]);

    for (std::size_t candidate = 0; candidate < seeds.size(); ++candidate) {
      std::array<Matrix, 8> images{}; images[0] = seeds[candidate];
      for (int i=1;i<8;++i) images[i] = f.semilinear_action(alpha_conjugator, images[i-1]);
      for (int i=0;i<4;++i) if (images[i+4] != f.inverse(images[i])) throw std::runtime_error("inverse closure failure");
      if (std::set<Matrix>(images.begin(), images.end()).size() != 8) throw std::runtime_error("direction collision");
      const std::array<int,8> rel{0,5,2,7,4,1,6,3}; Matrix rel_image=identity;
      for (auto i:rel) rel_image=f.multiply(rel_image,images[i]);
      if (rel_image != identity) throw std::runtime_error("surface relation failure");

      std::array<std::vector<std::uint16_t>, 8> transition;
      for (int g=0;g<8;++g) { transition[g].resize(elements.size()); for(std::size_t i=0;i<elements.size();++i)
        transition[g][i] = index.at(pack(f.multiply(elements[i], images[g]))); }
      std::vector<std::uint8_t> visited(elements.size()); std::queue<std::uint16_t> queue;
      visited[identity_index]=1; queue.push(identity_index); std::size_t generated=1;
      while(!queue.empty()) { const auto x=queue.front();queue.pop();for(int g=0;g<8;++g){auto y=transition[g][x];if(!visited[y]){visited[y]=1;++generated;queue.push(y);}}}
      if (generated != 7800) throw std::runtime_error("seed does not generate PSL(2,25)");

      std::vector<std::uint16_t> state(tree.size()); state[0]=identity_index; std::uint32_t witness=0;
      for (std::uint32_t id=1;id<tree.size();++id) {
        const auto edge=tree[id]; if(edge.parent>=id || edge.generator>=8) throw std::runtime_error("bad tree edge");
        state[id]=transition[edge.generator][state[edge.parent]];
        if ((edge.depth & 1U)==0U && state[id]==identity_index) { witness=id; break; }
      }
      if (!witness) { std::cout << "candidate=" << candidate << " BASED_PASS\n"; continue; }
      std::vector<unsigned> reversed;
      for (auto id=witness;id!=0;id=tree[id].parent) reversed.push_back(tree[id].generator);
      std::reverse(reversed.begin(),reversed.end());
      std::cout << "candidate=" << candidate << " based_witness_id=" << witness
                << " depth=" << static_cast<unsigned>(tree[witness].depth) << " word=";
      for (std::size_t i=0;i<reversed.size();++i) std::cout << (i?" ":"") << 'g' << reversed[i];
      std::cout << '\n';
    }
    return 0;
  } catch (const std::exception& e) { std::cerr << "ERROR: " << e.what() << '\n'; return 2; }
}
