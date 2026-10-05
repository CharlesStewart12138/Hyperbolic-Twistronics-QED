#include <algorithm>
#include <array>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

// Exact degree-14 ambient-permutation search for an inner implementation of
// the frozen C8 action.  The ambient permutation tau has an 8-cycle and one
// of the eleven partitions of the remaining six points.  Put alpha=Ad(tau).
// The substitution
//
//                    y = x tau^4
//
// is a bijection between alpha^4(x)=x^{-1}, alpha^8(x)=x and the square
// roots y^2=tau^8; x is recovered as y tau^{-4}.  Square roots of tau^8 are
// enumerated exhaustively from its cycle structure.  B3 survivors are then
// quotient by the exact centralizer C_{S14}(tau), and the actual generated
// permutation group order is computed by a deterministic Schreier recursion.
// The external parity augmentation <(g_j,1)> is also measured.  Internal
// parity is feasible precisely when the seed permutation is odd.

namespace {

template <int N> struct Perm {
  std::array<std::uint8_t, N> x{};
  bool operator==(const Perm &) const = default;
  bool operator<(const Perm &o) const { return x < o.x; }
};

template <int N> Perm<N> identity() {
  Perm<N> r;
  for (int i = 0; i < N; ++i) r.x[i] = static_cast<std::uint8_t>(i);
  return r;
}

template <int N> Perm<N> product(const Perm<N> &a, const Perm<N> &b) {
  Perm<N> r;
  for (int i = 0; i < N; ++i) r.x[i] = a.x[b.x[i]];
  return r;
}

template <int N> Perm<N> inverse(const Perm<N> &a) {
  Perm<N> r;
  for (int i = 0; i < N; ++i) r.x[a.x[i]] = static_cast<std::uint8_t>(i);
  return r;
}

template <int N> Perm<N> power(Perm<N> a, unsigned n) {
  auto r = identity<N>();
  while (n) {
    if (n & 1U) r = product(r, a);
    a = product(a, a);
    n >>= 1U;
  }
  return r;
}

template <int N>
Perm<N> conjugate(const Perm<N> &t, const Perm<N> &ti, const Perm<N> &a) {
  return product(product(t, a), ti);
}

template <int N> std::uint64_t packed(const Perm<N> &p) {
  static_assert(N <= 16);
  std::uint64_t r = 0;
  for (int i = 0; i < N; ++i) r |= std::uint64_t(p.x[i]) << (4 * i);
  return r;
}

template <int N> std::uint64_t rank_perm(const Perm<N> &p) {
  std::uint64_t r = 0;
  for (int i = 0; i < N; ++i) {
    unsigned less = 0;
    for (int j = i + 1; j < N; ++j) less += p.x[j] < p.x[i];
    r = r * (N - i) + less;
  }
  return r;
}

template <int N> bool is_odd(const Perm<N> &p) {
  unsigned inv = 0;
  for (int i = 0; i < N; ++i)
    for (int j = i + 1; j < N; ++j) inv ^= unsigned(p.x[i] > p.x[j]);
  return (inv & 1U) != 0;
}

template <int N> bool is_identity(const Perm<N> &p) {
  for (int i = 0; i < N; ++i)
    if (p.x[i] != i) return false;
  return true;
}

// Exact order by orbit--stabilizer and Schreier generators.  Every recursive
// generating set is symmetrized and deduplicated; degree at most 16 keeps the
// computation small, even when the answer itself is greater than 50000.
template <int N> std::uint64_t group_order_rec(std::vector<Perm<N>> generators) {
  std::unordered_set<std::uint64_t> seen_generators;
  std::vector<Perm<N>> sym;
  seen_generators.reserve(2 * generators.size() + 1);
  auto add_generator = [&](const Perm<N> &g) {
    if (!is_identity(g) && seen_generators.insert(packed(g)).second) sym.push_back(g);
  };
  for (const auto &g : generators) {
    add_generator(g);
    add_generator(inverse(g));
  }
  if (sym.empty()) return 1;

  int base = -1;
  for (int b = 0; b < N && base < 0; ++b)
    for (const auto &g : sym)
      if (g.x[b] != b) {
        base = b;
        break;
      }
  if (base < 0) return 1;

  std::array<bool, N> reached{};
  std::array<Perm<N>, N> transversal{};
  std::queue<int> todo;
  reached[base] = true;
  transversal[base] = identity<N>();
  todo.push(base);
  std::vector<int> orbit;
  while (!todo.empty()) {
    int p = todo.front();
    todo.pop();
    orbit.push_back(p);
    for (const auto &s : sym) {
      int q = s.x[p];
      if (!reached[q]) {
        reached[q] = true;
        transversal[q] = product(s, transversal[p]);
        todo.push(q);
      }
    }
  }

  std::unordered_set<std::uint64_t> seen_stabilizer;
  std::vector<Perm<N>> stabilizer;
  seen_stabilizer.reserve(orbit.size() * sym.size() + 1);
  for (int p : orbit) {
    for (const auto &s : sym) {
      int q = s.x[p];
      auto h = product(inverse(transversal[q]), product(s, transversal[p]));
      if (!is_identity(h) && seen_stabilizer.insert(packed(h)).second)
        stabilizer.push_back(h);
    }
  }
  return std::uint64_t(orbit.size()) * group_order_rec<N>(std::move(stabilizer));
}

template <int N, std::size_t K>
std::uint64_t group_order(const std::array<Perm<N>, K> &g) {
  return group_order_rec<N>(std::vector<Perm<N>>(g.begin(), g.end()));
}

constexpr int D = 14;
using P = Perm<D>;

std::size_t b3_plain(const std::array<P, 8> &g) {
  std::unordered_set<std::uint64_t> s;
  s.reserve(1024);
  s.insert(packed(identity<D>()));
  for (int a = 0; a < 8; ++a) {
    s.insert(packed(g[a]));
    for (int b = 0; b < 8; ++b) if (b != (a + 4) % 8) {
      auto ab = product(g[a], g[b]);
      s.insert(packed(ab));
      for (int c = 0; c < 8; ++c) if (c != (b + 4) % 8)
        s.insert(packed(product(ab, g[c])));
    }
  }
  return s.size();
}

std::size_t b3_augmented(const std::array<P, 8> &g) {
  std::unordered_set<std::uint64_t> s;
  s.reserve(1024);
  auto key = [](const P &p, unsigned z) { return (packed(p) << 1U) | z; };
  s.insert(key(identity<D>(), 0));
  for (int a = 0; a < 8; ++a) {
    s.insert(key(g[a], 1));
    for (int b = 0; b < 8; ++b) if (b != (a + 4) % 8) {
      auto ab = product(g[a], g[b]);
      s.insert(key(ab, 0));
      for (int c = 0; c < 8; ++c) if (c != (b + 4) % 8)
        s.insert(key(product(ab, g[c]), 1));
    }
  }
  return s.size();
}

std::uint64_t augmented_order(const std::array<P, 8> &g) {
  using Q = Perm<D + 2>;
  std::array<Q, 8> q{};
  for (int j = 0; j < 8; ++j) {
    q[j] = identity<D + 2>();
    for (int i = 0; i < D; ++i) q[j].x[i] = g[j].x[i];
    q[j].x[D] = D + 1;
    q[j].x[D + 1] = D;
  }
  return group_order(q);
}

P make_tau(const std::vector<int> &residual_parts) {
  auto t = identity<D>();
  int start = 0;
  auto add_cycle = [&](int len) {
    for (int i = 0; i < len; ++i) t.x[start + i] = start + ((i + 1) % len);
    start += len;
  };
  add_cycle(8);
  for (int len : residual_parts) add_cycle(len);
  if (start != D) throw std::runtime_error("partition does not sum to 14");
  return t;
}

std::vector<std::vector<int>> cycles_of(const P &p) {
  std::array<bool, D> used{};
  std::vector<std::vector<int>> cycles;
  for (int i = 0; i < D; ++i) if (!used[i]) {
    std::vector<int> c;
    int j = i;
    do {
      used[j] = true;
      c.push_back(j);
      j = p.x[j];
    } while (j != i);
    cycles.push_back(std::move(c));
  }
  return cycles;
}

std::uint64_t expected_centralizer_size(const P &t) {
  std::array<unsigned, D + 1> counts{};
  for (const auto &c : cycles_of(t)) ++counts[c.size()];
  std::uint64_t answer = 1;
  for (int len = 1; len <= D; ++len) {
    for (unsigned i = 0; i < counts[len]; ++i) answer *= len;
    for (unsigned i = 2; i <= counts[len]; ++i) answer *= i;
  }
  return answer;
}

std::vector<P> centralizer(const P &t) {
  auto cycles = cycles_of(t);
  std::vector<P> generators;
  for (const auto &c : cycles) if (c.size() > 1) {
    auto r = identity<D>();
    for (std::size_t i = 0; i < c.size(); ++i) r.x[c[i]] = c[(i + 1) % c.size()];
    generators.push_back(r);
  }
  for (int len = 1; len <= D; ++len) {
    std::vector<const std::vector<int> *> same;
    for (const auto &c : cycles) if (int(c.size()) == len) same.push_back(&c);
    for (std::size_t k = 1; k < same.size(); ++k) {
      auto s = identity<D>();
      for (int i = 0; i < len; ++i) {
        s.x[(*same[k - 1])[i]] = (*same[k])[i];
        s.x[(*same[k])[i]] = (*same[k - 1])[i];
      }
      generators.push_back(s);
    }
  }
  std::unordered_set<std::uint64_t> seen;
  std::vector<P> result;
  std::queue<P> todo;
  auto one = identity<D>();
  seen.insert(packed(one));
  result.push_back(one);
  todo.push(one);
  while (!todo.empty()) {
    auto a = todo.front();
    todo.pop();
    for (const auto &s : generators) {
      auto b = product(a, s);
      if (seen.insert(packed(b)).second) {
        result.push_back(b);
        todo.push(b);
      }
    }
  }
  if (result.size() != expected_centralizer_size(t))
    throw std::runtime_error("centralizer size mismatch");
  auto ti = inverse(t);
  for (const auto &c : result)
    if (!(conjugate(c, inverse(c), t) == t) || !(product(t, ti) == identity<D>()))
      throw std::runtime_error("centralizer construction error");
  return result;
}

template <class Emit>
void involutions_on(const std::vector<int> &fixed, const P &base, Emit emit) {
  P p = base;
  std::vector<bool> used(fixed.size());
  std::function<void()> rec = [&] {
    std::size_t ii = 0;
    while (ii < fixed.size() && used[ii]) ++ii;
    if (ii == fixed.size()) {
      emit(p);
      return;
    }
    int i = fixed[ii];
    used[ii] = true;
    p.x[i] = i;
    rec();
    for (std::size_t jj = ii + 1; jj < fixed.size(); ++jj) if (!used[jj]) {
      int j = fixed[jj];
      used[jj] = true;
      p.x[i] = j;
      p.x[j] = i;
      rec();
      p.x[j] = j;
      used[jj] = false;
    }
    p.x[i] = i;
    used[ii] = false;
  };
  rec();
}

template <class Emit> void square_roots(const P &c, Emit emit) {
  auto cycles = cycles_of(c);
  std::vector<int> fixed;
  std::vector<std::vector<int>> nontrivial;
  for (auto &cyc : cycles) {
    if (cyc.size() == 1) fixed.push_back(cyc[0]);
    else nontrivial.push_back(cyc);
  }
  std::vector<P> bases;
  if (nontrivial.empty()) {
    bases.push_back(identity<D>());
  } else if (nontrivial.size() == 1 && nontrivial[0].size() == 3) {
    bases.push_back(power(c, 2));
  } else if (nontrivial.size() == 1 && nontrivial[0].size() == 5) {
    bases.push_back(power(c, 3));
  } else if (nontrivial.size() == 2 && nontrivial[0].size() == 3 &&
             nontrivial[1].size() == 3) {
    bases.push_back(power(c, 2));
    const auto &a = nontrivial[0];
    const auto &b = nontrivial[1];
    for (int shift = 0; shift < 3; ++shift) {
      auto y = identity<D>();
      for (int i = 0; i < 3; ++i) {
        y.x[a[i]] = b[(i + shift) % 3];
        y.x[b[(i + shift) % 3]] = a[(i + 1) % 3];
      }
      bases.push_back(y);
    }
  } else {
    throw std::runtime_error("unexpected tau^8 cycle structure");
  }
  for (const auto &base : bases)
    involutions_on(fixed, base, [&](const P &y) {
      if (!(product(y, y) == c)) throw std::runtime_error("bad square root");
      emit(y);
    });
}

struct Counts {
  std::uint64_t roots = 0;
  std::uint64_t relator = 0;
  std::uint64_t distinct = 0;
  std::uint64_t b3_plain = 0;
  std::uint64_t b3_augmented = 0;
};

struct OrderStats {
  std::uint64_t orbit_count = 0;
  std::uint64_t seed_count = 0;
  std::uint64_t sign_orbit_count = 0;
  std::uint64_t sign_seed_count = 0;
};

void run_type(const std::string &name, const std::vector<int> &parts,
              std::uint64_t expected_roots) {
  const auto t = make_tau(parts);
  const auto ti = inverse(t);
  const auto t4inv = power(ti, 4);
  const auto c = power(t, 8);
  Counts counts;
  std::vector<P> candidates;

  square_roots(c, [&](const P &y) {
    ++counts.roots;
    auto seed = product(y, t4inv);
    std::array<P, 8> g{};
    g[0] = seed;
    for (int j = 1; j < 8; ++j) g[j] = conjugate(t, ti, g[j - 1]);
    if (!(conjugate(t, ti, g[7]) == g[0])) throw std::runtime_error("alpha^8 failure");
    if (!(g[4] == inverse(g[0]))) throw std::runtime_error("inverse-bijection failure");
    auto r = identity<D>();
    for (int j : std::array<int, 8>{0, 5, 2, 7, 4, 1, 6, 3}) r = product(r, g[j]);
    if (!(r == identity<D>())) return;
    ++counts.relator;
    std::unordered_set<std::uint64_t> orbit_images;
    for (const auto &gj : g) orbit_images.insert(packed(gj));
    if (orbit_images.size() != 8) return;
    ++counts.distinct;
    auto bp = b3_plain(g);
    auto ba = b3_augmented(g);
    if (bp == 457) ++counts.b3_plain;
    if (ba == 457) {
      ++counts.b3_augmented;
      candidates.push_back(seed);
    }
  });
  if (counts.roots != expected_roots) throw std::runtime_error("square-root count mismatch");

  auto cent = centralizer(t);
  std::unordered_set<std::uint64_t> live;
  live.reserve(2 * candidates.size() + 1);
  for (const auto &p : candidates) live.insert(packed(p));

  std::map<std::uint64_t, OrderStats> actual_hist;
  std::map<std::uint64_t, OrderStats> augmented_hist;
  std::uint64_t centralizer_orbits = 0;
  std::uint64_t sign_orbits = 0, sign_seeds = 0;
  std::uint64_t actual_over_orbits = 0, actual_over_seeds = 0;
  std::uint64_t augmented_over_orbits = 0, augmented_over_seeds = 0;

  for (const auto &seed : candidates) {
    if (!live.erase(packed(seed))) continue;
    ++centralizer_orbits;
    std::uint64_t orbit_size = 1;
    for (const auto &z : cent) {
      auto q = conjugate(z, inverse(z), seed);
      orbit_size += live.erase(packed(q));
    }
    bool sign = is_odd(seed);
    if (sign) {
      ++sign_orbits;
      sign_seeds += orbit_size;
    }
    std::array<P, 8> g{};
    g[0] = seed;
    for (int j = 1; j < 8; ++j) g[j] = conjugate(t, ti, g[j - 1]);
    auto actual = group_order(g);
    auto augmented = augmented_order(g);
    if (sign && actual != augmented)
      throw std::runtime_error("odd-sign augmentation is not the graph of sign");
    auto update = [&](auto &hist, std::uint64_t order) {
      auto &s = hist[order];
      ++s.orbit_count;
      s.seed_count += orbit_size;
      if (sign) {
        ++s.sign_orbit_count;
        s.sign_seed_count += orbit_size;
      }
    };
    if (actual > 50000) {
      ++actual_over_orbits;
      actual_over_seeds += orbit_size;
    } else update(actual_hist, actual);
    if (augmented > 50000) {
      ++augmented_over_orbits;
      augmented_over_seeds += orbit_size;
    } else update(augmented_hist, augmented);

    if ((actual >= 2338 && actual <= 50000) ||
        (augmented >= 2338 && augmented <= 50000)) {
      std::cout << "REP type=" << name << " rank=" << rank_perm(seed)
                << " orbit_size=" << orbit_size << " odd_sign=" << unsigned(sign)
                << " actual_order=" << actual << " augmented_order=" << augmented
                << '\n';
    }
  }
  if (!live.empty()) throw std::runtime_error("centralizer orbit reduction incomplete");

  std::cout << "TYPE " << name
            << " roots=" << counts.roots
            << " relator=" << counts.relator
            << " distinct=" << counts.distinct
            << " b3_plain=" << counts.b3_plain
            << " b3_augmented=" << counts.b3_augmented
            << " centralizer=" << cent.size()
            << " b3_orbits=" << centralizer_orbits
            << " odd_sign_orbits=" << sign_orbits
            << " odd_sign_seeds=" << sign_seeds
            << " actual_over50000_orbits=" << actual_over_orbits
            << " actual_over50000_seeds=" << actual_over_seeds
            << " augmented_over50000_orbits=" << augmented_over_orbits
            << " augmented_over50000_seeds=" << augmented_over_seeds
            << '\n';
  for (const auto &[order, s] : actual_hist)
    std::cout << "ACTUAL_ORDER type=" << name << " order=" << order
              << " orbits=" << s.orbit_count << " seeds=" << s.seed_count
              << " odd_sign_orbits=" << s.sign_orbit_count
              << " odd_sign_seeds=" << s.sign_seed_count << '\n';
  for (const auto &[order, s] : augmented_hist)
    std::cout << "AUGMENTED_ORDER type=" << name << " order=" << order
              << " orbits=" << s.orbit_count << " seeds=" << s.seed_count
              << " odd_sign_orbits=" << s.sign_orbit_count
              << " odd_sign_seeds=" << s.sign_seed_count << '\n';
  std::cout.flush();
}

}  // namespace

int main() {
  try {
    run_type("8+1^6",       {1, 1, 1, 1, 1, 1}, 2390480);
    run_type("8+2+1^4",     {2, 1, 1, 1, 1},    2390480);
    run_type("8+2^2+1^2",   {2, 2, 1, 1},       2390480);
    run_type("8+2^3",       {2, 2, 2},          2390480);
    run_type("8+3+1^3",     {3, 1, 1, 1},         35696);
    run_type("8+3+2+1",     {3, 2, 1},            35696);
    run_type("8+3^2",       {3, 3},                3056);
    run_type("8+4+1^2",     {4, 1, 1},          2390480);
    run_type("8+4+2",       {4, 2},             2390480);
    run_type("8+5+1",       {5, 1},                2620);
    run_type("8+6",         {6},                   3056);
    return 0;
  } catch (const std::exception &e) {
    std::cerr << "ERROR: " << e.what() << '\n';
    return 2;
  }
}
