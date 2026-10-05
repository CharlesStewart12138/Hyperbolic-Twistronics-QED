#include <algorithm>
#include <array>
#include <chrono>
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

// Proof-complete degree-15 ambient-conjugation C8 sweep.  For every cycle
// type tau=(8-cycle)*(partition of 7), alpha=Ad(tau), put y=x*tau^4.
// Then
//   alpha^4(x)=x^-1 and alpha^8(x)=x  <=>  y^2=tau^8,
// with inverse x=y*tau^-4.  The square roots are enumerated exactly by the
// cycle structure of tau^8.  After the frozen relator, eight-direction and
// B3 tests, survivors are reduced by the full centralizer C_S15(tau).
// Generated orders are exact through 50000; 50001 is the certified sentinel
// for a larger order.  Both internal sign parity and an external C2 parity
// augmentation are reported.  A 20-minute wall-clock guard is enforced.

namespace {
constexpr int D = 15;
constexpr std::uint64_t LIMIT = 50000;
using Clock = std::chrono::steady_clock;
Clock::time_point global_start;

struct P {
  std::array<std::uint8_t, D> x{};
  bool operator==(const P &) const = default;
  bool operator<(const P &o) const { return x < o.x; }
};

P identity() {
  P r;
  for (int i = 0; i < D; ++i) r.x[i] = static_cast<std::uint8_t>(i);
  return r;
}
P product(const P &a, const P &b) {
  P r;
  for (int i = 0; i < D; ++i) r.x[i] = a.x[b.x[i]];
  return r;
}
P inverse(const P &a) {
  P r;
  for (int i = 0; i < D; ++i) r.x[a.x[i]] = static_cast<std::uint8_t>(i);
  return r;
}
P power(P a, unsigned n) {
  auto r = identity();
  while (n) {
    if (n & 1U) r = product(r, a);
    a = product(a, a);
    n >>= 1U;
  }
  return r;
}
P conjugate(const P &t, const P &ti, const P &a) {
  return product(product(t, a), ti);
}
std::uint64_t packed(const P &p) {
  std::uint64_t r = 0;
  for (int i = 0; i < D; ++i) r |= std::uint64_t(p.x[i]) << (4 * i);
  return r;
}
std::uint64_t rank_perm(const P &p) {
  std::uint64_t r = 0;
  for (int i = 0; i < D; ++i) {
    unsigned less = 0;
    for (int j = i + 1; j < D; ++j) less += p.x[j] < p.x[i];
    r = r * (D - i) + less;
  }
  return r;
}
bool is_identity(const P &p) {
  for (int i = 0; i < D; ++i) if (p.x[i] != i) return false;
  return true;
}
bool is_odd(const P &p) {
  unsigned z = 0;
  for (int i = 0; i < D; ++i)
    for (int j = i + 1; j < D; ++j) z ^= unsigned(p.x[i] > p.x[j]);
  return (z & 1U) != 0;
}
void check_deadline() {
  if (Clock::now() - global_start > std::chrono::minutes(20))
    throw std::runtime_error("20-minute wall-clock guard reached");
}

// Orbit--stabilizer with Schreier generators.  If a known orbit-size product
// already exceeds cap, cap+1 is returned without constructing deeper levels.
std::uint64_t group_order_capped(std::vector<P> generators, std::uint64_t cap) {
  std::unordered_set<std::uint64_t> generator_keys;
  std::vector<P> sym;
  generator_keys.reserve(2 * generators.size() + 1);
  auto add = [&](const P &g) {
    if (!is_identity(g) && generator_keys.insert(packed(g)).second) sym.push_back(g);
  };
  for (const auto &g : generators) { add(g); add(inverse(g)); }
  if (sym.empty()) return 1;

  int base = -1;
  for (int b = 0; b < D && base < 0; ++b)
    for (const auto &g : sym) if (g.x[b] != b) { base = b; break; }
  if (base < 0) return 1;

  std::array<bool, D> reached{};
  std::array<P, D> transversal{};
  std::queue<int> todo;
  std::vector<int> orbit;
  reached[base] = true;
  transversal[base] = identity();
  todo.push(base);
  while (!todo.empty()) {
    int p = todo.front(); todo.pop();
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
  if (orbit.size() > cap) return cap + 1;

  std::unordered_set<std::uint64_t> stabilizer_keys;
  std::vector<P> stabilizer;
  stabilizer_keys.reserve(orbit.size() * sym.size() + 1);
  for (int p : orbit) for (const auto &s : sym) {
    int q = s.x[p];
    auto h = product(inverse(transversal[q]), product(s, transversal[p]));
    if (!is_identity(h) && stabilizer_keys.insert(packed(h)).second)
      stabilizer.push_back(h);
  }
  std::uint64_t residual_cap = cap / orbit.size();
  auto sub = group_order_capped(std::move(stabilizer), residual_cap);
  if (sub > residual_cap) return cap + 1;
  return std::uint64_t(orbit.size()) * sub;
}

std::uint64_t actual_order(const std::array<P, 8> &g) {
  return group_order_capped(std::vector<P>(g.begin(), g.end()), LIMIT);
}

// Used only if actual order <=50000 and sign is unavailable.  Projection to
// the permutation image has kernel at most C2, hence at most 100000 states.
std::uint64_t augmented_order(const std::array<P, 8> &g) {
  struct E { P p; std::uint8_t z; };
  auto key = [](const E &e) { return (packed(e.p) << 1U) | e.z; };
  std::unordered_set<std::uint64_t> seen;
  std::queue<E> todo;
  E one{identity(), 0};
  seen.reserve(100003);
  seen.insert(key(one));
  todo.push(one);
  while (!todo.empty()) {
    auto a = todo.front(); todo.pop();
    for (const auto &s : g) {
      E b{product(a.p, s), std::uint8_t(a.z ^ 1U)};
      if (seen.insert(key(b)).second) {
        if (seen.size() > LIMIT) return LIMIT + 1;
        todo.push(b);
      }
    }
  }
  return seen.size();
}

std::size_t b3_plain(const std::array<P, 8> &g) {
  std::unordered_set<std::uint64_t> s;
  s.reserve(1024);
  s.insert(packed(identity()));
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
  s.insert(key(identity(), 0));
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

P make_tau(const std::vector<int> &parts) {
  auto t = identity();
  int start = 0;
  auto cycle = [&](int len) {
    for (int i = 0; i < len; ++i) t.x[start + i] = start + ((i + 1) % len);
    start += len;
  };
  cycle(8);
  for (int len : parts) cycle(len);
  if (start != D) throw std::runtime_error("partition does not sum to 15");
  return t;
}
std::vector<std::vector<int>> cycles_of(const P &p) {
  std::array<bool, D> used{};
  std::vector<std::vector<int>> result;
  for (int i = 0; i < D; ++i) if (!used[i]) {
    std::vector<int> c;
    int j = i;
    do { used[j] = true; c.push_back(j); j = p.x[j]; } while (j != i);
    result.push_back(std::move(c));
  }
  return result;
}
std::uint64_t expected_centralizer_size(const P &t) {
  std::array<unsigned, D + 1> multiplicity{};
  for (const auto &c : cycles_of(t)) ++multiplicity[c.size()];
  std::uint64_t result = 1;
  for (int len = 1; len <= D; ++len) {
    for (unsigned i = 0; i < multiplicity[len]; ++i) result *= len;
    for (unsigned i = 2; i <= multiplicity[len]; ++i) result *= i;
  }
  return result;
}
std::vector<P> centralizer(const P &t) {
  auto cycles = cycles_of(t);
  std::vector<P> generators;
  for (const auto &c : cycles) if (c.size() > 1) {
    auto r = identity();
    for (std::size_t i = 0; i < c.size(); ++i) r.x[c[i]] = c[(i + 1) % c.size()];
    generators.push_back(r);
  }
  for (int len = 1; len <= D; ++len) {
    std::vector<const std::vector<int> *> same;
    for (const auto &c : cycles) if (int(c.size()) == len) same.push_back(&c);
    for (std::size_t k = 1; k < same.size(); ++k) {
      auto s = identity();
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
  auto one = identity();
  seen.insert(packed(one)); result.push_back(one); todo.push(one);
  while (!todo.empty()) {
    auto a = todo.front(); todo.pop();
    for (const auto &s : generators) {
      auto b = product(a, s);
      if (seen.insert(packed(b)).second) { result.push_back(b); todo.push(b); }
    }
  }
  if (result.size() != expected_centralizer_size(t))
    throw std::runtime_error("centralizer size mismatch");
  auto ti = inverse(t);
  for (const auto &z : result)
    if (!(conjugate(z, inverse(z), t) == t) || !(product(t, ti) == identity()))
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
    if (ii == fixed.size()) { emit(p); return; }
    int i = fixed[ii];
    used[ii] = true; p.x[i] = i; rec();
    for (std::size_t jj = ii + 1; jj < fixed.size(); ++jj) if (!used[jj]) {
      int j = fixed[jj];
      used[jj] = true; p.x[i] = j; p.x[j] = i; rec();
      p.x[j] = j; used[jj] = false;
    }
    p.x[i] = i; used[ii] = false;
  };
  rec();
}
template <class Emit> void square_roots(const P &c, Emit emit) {
  std::vector<int> fixed;
  std::vector<std::vector<int>> nontrivial;
  for (auto cyc : cycles_of(c)) {
    if (cyc.size() == 1) fixed.push_back(cyc[0]);
    else nontrivial.push_back(std::move(cyc));
  }
  std::vector<P> bases;
  if (nontrivial.empty()) {
    bases.push_back(identity());
  } else if (nontrivial.size() == 1 && nontrivial[0].size() == 3) {
    bases.push_back(power(c, 2));
  } else if (nontrivial.size() == 1 && nontrivial[0].size() == 5) {
    bases.push_back(power(c, 3));
  } else if (nontrivial.size() == 1 && nontrivial[0].size() == 7) {
    bases.push_back(power(c, 4));
  } else if (nontrivial.size() == 2 && nontrivial[0].size() == 3 &&
             nontrivial[1].size() == 3) {
    bases.push_back(power(c, 2));
    const auto &a = nontrivial[0];
    const auto &b = nontrivial[1];
    for (int shift = 0; shift < 3; ++shift) {
      auto y = identity();
      for (int i = 0; i < 3; ++i) {
        y.x[a[i]] = b[(i + shift) % 3];
        y.x[b[(i + shift) % 3]] = a[(i + 1) % 3];
      }
      bases.push_back(y);
    }
  } else throw std::runtime_error("unexpected tau^8 cycle structure");
  for (const auto &base : bases)
    involutions_on(fixed, base, [&](const P &y) {
      if (!(product(y, y) == c)) throw std::runtime_error("bad square root");
      emit(y);
    });
}

struct Counts {
  std::uint64_t roots = 0, relator = 0, distinct = 0;
  std::uint64_t b3_plain = 0, b3_augmented = 0;
};
struct Stats {
  std::uint64_t orbits = 0, seeds = 0, odd_orbits = 0, odd_seeds = 0;
};

void run_type(const std::string &name, const std::vector<int> &parts,
              std::uint64_t expected_roots) {
  auto t = make_tau(parts), ti = inverse(t), t4inv = power(ti, 4), c = power(t, 8);
  Counts count;
  std::vector<P> candidates;
  square_roots(c, [&](const P &y) {
    ++count.roots;
    if ((count.roots & ((1U << 20) - 1U)) == 0) check_deadline();
    auto seed = product(y, t4inv);
    std::array<P, 8> g{};
    g[0] = seed;
    for (int j = 1; j < 8; ++j) g[j] = conjugate(t, ti, g[j - 1]);
    if (!(conjugate(t, ti, g[7]) == g[0])) throw std::runtime_error("alpha^8 failure");
    if (!(g[4] == inverse(g[0]))) throw std::runtime_error("inverse-bijection failure");
    auto r = identity();
    for (int j : std::array<int, 8>{0, 5, 2, 7, 4, 1, 6, 3}) r = product(r, g[j]);
    if (!(r == identity())) return;
    ++count.relator;
    std::unordered_set<std::uint64_t> images;
    for (const auto &gj : g) images.insert(packed(gj));
    if (images.size() != 8) return;
    ++count.distinct;
    auto plain = b3_plain(g), augmented = b3_augmented(g);
    if (plain == 457) ++count.b3_plain;
    if (is_odd(seed) && plain != augmented)
      throw std::runtime_error("sign parity did not realize word parity");
    if (augmented == 457) { ++count.b3_augmented; candidates.push_back(seed); }
  });
  if (count.roots != expected_roots) throw std::runtime_error("square-root count mismatch");

  auto cent = centralizer(t);
  std::unordered_set<std::uint64_t> live;
  live.reserve(2 * candidates.size() + 1);
  for (const auto &seed : candidates) live.insert(packed(seed));
  std::map<std::uint64_t, Stats> actual_hist, augmented_hist;
  std::uint64_t orbit_count = 0, odd_orbits = 0, odd_seeds = 0;
  std::uint64_t actual_over_orbits = 0, actual_over_seeds = 0;
  std::uint64_t augmented_over_orbits = 0, augmented_over_seeds = 0;
  for (const auto &seed : candidates) {
    if (!live.erase(packed(seed))) continue;
    ++orbit_count;
    if ((orbit_count & 127U) == 0) check_deadline();
    std::uint64_t orbit_size = 1;
    for (const auto &z : cent)
      orbit_size += live.erase(packed(conjugate(z, inverse(z), seed)));
    bool odd = is_odd(seed);
    if (odd) { ++odd_orbits; odd_seeds += orbit_size; }
    std::array<P, 8> g{};
    g[0] = seed;
    for (int j = 1; j < 8; ++j) g[j] = conjugate(t, ti, g[j - 1]);
    auto actual = actual_order(g);
    auto augmented = actual > LIMIT ? LIMIT + 1 : (odd ? actual : augmented_order(g));
    auto update = [&](auto &hist, std::uint64_t order) {
      auto &s = hist[order];
      ++s.orbits; s.seeds += orbit_size;
      if (odd) { ++s.odd_orbits; s.odd_seeds += orbit_size; }
    };
    if (actual > LIMIT) { ++actual_over_orbits; actual_over_seeds += orbit_size; }
    else update(actual_hist, actual);
    if (augmented > LIMIT) { ++augmented_over_orbits; augmented_over_seeds += orbit_size; }
    else update(augmented_hist, augmented);
    if ((actual >= 2338 && actual <= LIMIT) ||
        (augmented >= 2338 && augmented <= LIMIT))
      std::cout << "REP type=" << name << " rank=" << rank_perm(seed)
                << " orbit_size=" << orbit_size << " odd_sign=" << unsigned(odd)
                << " actual_order=" << actual << " augmented_order=" << augmented << '\n';
  }
  if (!live.empty()) throw std::runtime_error("centralizer reduction incomplete");
  std::cout << "TYPE " << name << " roots=" << count.roots
            << " relator=" << count.relator << " distinct=" << count.distinct
            << " b3_plain=" << count.b3_plain << " b3_augmented=" << count.b3_augmented
            << " centralizer=" << cent.size() << " b3_orbits=" << orbit_count
            << " odd_sign_orbits=" << odd_orbits << " odd_sign_seeds=" << odd_seeds
            << " actual_over50000_orbits=" << actual_over_orbits
            << " actual_over50000_seeds=" << actual_over_seeds
            << " augmented_over50000_orbits=" << augmented_over_orbits
            << " augmented_over50000_seeds=" << augmented_over_seeds << '\n';
  for (const auto &[order, s] : actual_hist)
    std::cout << "ACTUAL_ORDER type=" << name << " order=" << order
              << " orbits=" << s.orbits << " seeds=" << s.seeds
              << " odd_sign_orbits=" << s.odd_orbits << " odd_sign_seeds=" << s.odd_seeds << '\n';
  for (const auto &[order, s] : augmented_hist)
    std::cout << "AUGMENTED_ORDER type=" << name << " order=" << order
              << " orbits=" << s.orbits << " seeds=" << s.seeds
              << " odd_sign_orbits=" << s.odd_orbits << " odd_sign_seeds=" << s.odd_seeds << '\n';
  std::cout.flush();
}
}  // namespace

int main() {
  try {
    global_start = Clock::now();
    run_type("8+1^7",       {1,1,1,1,1,1,1}, 10349536);
    run_type("8+2+1^5",     {2,1,1,1,1,1},   10349536);
    run_type("8+2^2+1^3",   {2,2,1,1,1},     10349536);
    run_type("8+2^3+1",     {2,2,2,1},       10349536);
    run_type("8+3+1^4",     {3,1,1,1,1},       140152);
    run_type("8+3+2+1^2",   {3,2,1,1},         140152);
    run_type("8+3+2^2",     {3,2,2},           140152);
    run_type("8+3^2+1",     {3,3,1},            10480);
    run_type("8+4+1^3",     {4,1,1,1},       10349536);
    run_type("8+4+2+1",     {4,2,1},         10349536);
    run_type("8+4+3",       {4,3},             140152);
    run_type("8+5+1^2",     {5,1,1},             9496);
    run_type("8+5+2",       {5,2},               9496);
    run_type("8+6+1",       {6,1},              10480);
    run_type("8+7",         {7},                  764);
    return 0;
  } catch (const std::exception &e) {
    std::cerr << "ERROR: " << e.what() << '\n';
    return 2;
  }
}
