#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {
struct Meta { std::uint32_t parent; std::uint8_t generator, depth; std::uint16_t reserved; };
static_assert(sizeof(Meta) == 8);
using Perm = std::array<std::uint8_t, 20>;
struct PermHash {
  std::size_t operator()(const Perm& p) const noexcept {
    std::uint64_t h = 1469598103934665603ULL;
    for (auto x : p) { h ^= x; h *= 1099511628211ULL; }
    return static_cast<std::size_t>(h);
  }
};
struct Candidate { std::string group; int alpha=0, rep=0, order=0; std::array<Perm,8> images{}; };

Perm one() { Perm p{}; for (int i=0;i<20;++i) p[i]=static_cast<std::uint8_t>(i); return p; }
Perm mul(const Perm& a,const Perm& b) { Perm c{}; for (int i=0;i<20;++i) c[i]=b[a[i]]; return c; }
Perm inv(const Perm& a) { Perm b{}; for (int i=0;i<20;++i) b[a[i]]=static_cast<std::uint8_t>(i); return b; }

bool parse_int_token(const std::string& s,int& v) {
  const char* b=s.data(); const char* e=b+s.size(); auto r=std::from_chars(b,e,v);
  return r.ec==std::errc{} && r.ptr==e;
}
int next_int(std::istream& in) {
  std::string s; int v=0;
  while (in>>s) if (parse_int_token(s,v)) return v;
  throw std::runtime_error("short numeric candidate record");
}
std::vector<Candidate> load_candidates(int argc,char** argv) {
  std::vector<Candidate> out;
  for (int f=1;f<argc-1;++f) {
    std::ifstream in(argv[f]); if (!in) throw std::runtime_error("cannot open candidate certificate");
    std::string tok;
    while (in>>tok) if (tok=="CANDIDATE_NUMERIC") {
      Candidate c; in>>c.group; c.alpha=next_int(in); c.rep=next_int(in); c.order=next_int(in);
      for (auto& p:c.images) for (auto& x:p) {
        const int z=next_int(in); if (z<0 || z>=20) throw std::runtime_error("bad permutation entry");
        x=static_cast<std::uint8_t>(z);
      }
      out.push_back(c);
    }
  }
  return out;
}
std::vector<Meta> load_tree(const std::string& path) {
  std::ifstream in(path,std::ios::binary); if (!in) throw std::runtime_error("cannot open based tree");
  char magic[8]{}; std::uint64_t count=0; std::uint32_t size=0;
  in.read(magic,8); in.read(reinterpret_cast<char*>(&count),8); in.read(reinterpret_cast<char*>(&size),4);
  if (std::string(magic,8)!="BOLZAT01" || count!=23'129'593ULL || size!=sizeof(Meta)) throw std::runtime_error("based tree contract drift");
  std::vector<Meta> tree(static_cast<std::size_t>(count));
  in.read(reinterpret_cast<char*>(tree.data()),static_cast<std::streamsize>(tree.size()*sizeof(Meta)));
  if (!in) throw std::runtime_error("short based tree");
  return tree;
}
std::size_t b3(const std::array<Perm,8>& im) {
  std::set<Perm> seen{one()}; std::vector<std::pair<Perm,int>> frontier{{one(),-1}};
  for (int depth=1;depth<=3;++depth) {
    std::vector<std::pair<Perm,int>> next;
    for (const auto& item:frontier) for (int g=0;g<8;++g) {
      if (item.second>=0 && g==(item.second+4)%8) continue;
      auto z=mul(item.first,im[g]); seen.insert(z); next.push_back({z,g});
    }
    frontier=std::move(next);
  }
  return seen.size();
}
}

int main(int argc,char** argv) {
  try {
    if (argc<3) throw std::runtime_error("usage: CERTIFICATE... BASED_TREE_META_BIN");
    const auto candidates=load_candidates(argc,argv);
    std::cout<<"candidates="<<candidates.size()<<'\n';
    if (candidates.empty()) return 0;
    const auto tree=load_tree(argv[argc-1]); const auto id=one();
    for (const auto& c:candidates) {
      for (int i=0;i<4;++i) if (c.images[i+4]!=inv(c.images[i])) throw std::runtime_error("inverse failure");
      Perm rel=id; for (int g:std::array<int,8>{0,5,2,7,4,1,6,3}) rel=mul(rel,c.images[g]);
      if (rel!=id) throw std::runtime_error("relator failure");
      if (b3(c.images)!=457) throw std::runtime_error("B3 failure");

      std::vector<Perm> elements{id};
      std::unordered_map<Perm,std::uint16_t,PermHash> index; index.reserve(50000); index.emplace(id,0);
      std::vector<std::array<std::uint16_t,8>> transition;
      for (std::size_t head=0;head<elements.size();++head) {
        std::array<std::uint16_t,8> row{};
        for (int g=0;g<8;++g) {
          auto z=mul(elements[head],c.images[g]); auto it=index.find(z);
          if (it==index.end()) {
            if (elements.size()>=65536) throw std::runtime_error("uint16 overflow");
            auto j=static_cast<std::uint16_t>(elements.size()); index.emplace(z,j); elements.push_back(z); row[g]=j;
          } else row[g]=it->second;
        }
        transition.push_back(row);
      }
      if (static_cast<int>(elements.size())!=c.order) throw std::runtime_error("generated order failure");

      std::vector<std::uint16_t> state(tree.size()); std::uint32_t witness=0;
      for (std::uint32_t i=1;i<tree.size();++i) {
        const auto e=tree[i]; if (e.parent>=i || e.generator>=8) throw std::runtime_error("bad tree edge");
        state[i]=transition[state[e.parent]][e.generator];
        if ((e.depth&1U)==0U && state[i]==0) { witness=i; break; }
      }
      std::cout<<c.group<<" alpha="<<c.alpha<<" rep="<<c.rep<<" order="<<elements.size();
      if (!witness) { std::cout<<" BASED_PASS\n"; continue; }
      std::vector<unsigned> word;
      for (auto i=witness;i;i=tree[i].parent) word.push_back(tree[i].generator);
      std::reverse(word.begin(),word.end());
      std::cout<<" witness_id="<<witness<<" depth="<<static_cast<unsigned>(tree[witness].depth)<<" word=";
      for (std::size_t i=0;i<word.size();++i) std::cout<<(i?" ":"")<<'g'<<word[i];
      std::cout<<'\n';
    }
    return 0;
  } catch (const std::exception& e) { std::cerr<<"ERROR: "<<e.what()<<'\n'; return 2; }
}
