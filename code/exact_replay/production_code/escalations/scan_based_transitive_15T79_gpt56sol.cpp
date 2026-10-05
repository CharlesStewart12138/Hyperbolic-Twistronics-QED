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
#include <utility>
#include <vector>

namespace {

struct Meta {
  std::uint32_t parent;
  std::uint8_t generator;
  std::uint8_t depth;
  std::uint16_t reserved;
};
static_assert(sizeof(Meta) == 8);

using Perm = std::array<std::uint8_t,15>;

Perm identity() {
  Perm p{};
  for (int i=0;i<15;++i) p[i]=static_cast<std::uint8_t>(i);
  return p;
}

// GAP permutations act on the right: i^(a*b)=(i^a)^b.
Perm multiply(const Perm& a,const Perm& b) {
  Perm c{};
  for (int i=0;i<15;++i) c[i]=b[a[i]];
  return c;
}

Perm inverse(const Perm& a) {
  Perm b{};
  for (int i=0;i<15;++i) b[a[i]]=static_cast<std::uint8_t>(i);
  return b;
}

std::uint64_t key(const Perm& p) {
  std::uint64_t k=0;
  for (int i=0;i<15;++i) k|=static_cast<std::uint64_t>(p[i])<<(4*i);
  return k;
}

bool odd(const Perm& p) {
  int inv=0;
  for(int i=0;i<15;++i) for(int j=i+1;j<15;++j) inv+=(p[i]>p[j]);
  return (inv&1)!=0;
}

std::vector<Meta> load_tree(const std::string& path) {
  std::ifstream in(path,std::ios::binary);
  if(!in) throw std::runtime_error("cannot open based tree");
  char magic[8]{}; std::uint64_t count=0; std::uint32_t size=0;
  in.read(magic,8); in.read(reinterpret_cast<char*>(&count),8);
  in.read(reinterpret_cast<char*>(&size),4);
  if(std::string(magic,8)!="BOLZAT01" || count!=23'129'593ULL || size!=sizeof(Meta))
    throw std::runtime_error("based tree contract drift");
  std::vector<Meta> tree(static_cast<std::size_t>(count));
  in.read(reinterpret_cast<char*>(tree.data()),static_cast<std::streamsize>(tree.size()*sizeof(Meta)));
  if(!in) throw std::runtime_error("short based tree");
  return tree;
}

struct Candidate { int alpha_class=0,representative=0; std::array<Perm,8> images{}; };

std::vector<Candidate> load_candidates(const std::string& path) {
  std::ifstream in(path);
  if(!in) throw std::runtime_error("cannot open candidate data");
  std::string magic; int count=0,order=0;
  in>>magic>>count>>order;
  if(magic!="BOLZA15T79" || count!=10 || order!=38880) throw std::runtime_error("candidate header drift");
  std::vector<Candidate> out(static_cast<std::size_t>(count));
  for(auto& c:out) {
    in>>c.alpha_class>>c.representative;
    for(auto& p:c.images) for(auto& v:p) { int x=-1; in>>x; if(x<0||x>=15) throw std::runtime_error("bad permutation entry"); v=static_cast<std::uint8_t>(x); }
  }
  if(!in) throw std::runtime_error("short candidate data");
  return out;
}

std::size_t b3_cardinality(const std::array<Perm,8>& images) {
  std::set<std::uint64_t> seen;
  std::vector<std::pair<Perm,int>> frontier{{identity(),-1}};
  seen.insert(key(identity()));
  for(int depth=1;depth<=3;++depth) {
    std::vector<std::pair<Perm,int>> next;
    for(const auto& item:frontier) for(int g=0;g<8;++g) {
      if(item.second>=0 && g==(item.second+4)%8) continue;
      auto z=multiply(item.first,images[g]);
      seen.insert(key(z)); next.push_back({z,g});
    }
    frontier=std::move(next);
  }
  return seen.size();
}

} // namespace

int main(int argc,char** argv) {
  try {
    if(argc!=3) throw std::runtime_error("usage: CANDIDATES_DAT BASED_TREE_META_BIN");
    const auto candidates=load_candidates(argv[1]);
    const auto tree=load_tree(argv[2]);
    const Perm one=identity();
    for(const auto& c:candidates) {
      for(int i=0;i<4;++i) if(c.images[i+4]!=inverse(c.images[i])) throw std::runtime_error("inverse closure failure");
      for(const auto& p:c.images) if(!odd(p)) throw std::runtime_error("sign parity failure");
      Perm rel=one; const std::array<int,8> relator{0,5,2,7,4,1,6,3};
      for(int g:relator) rel=multiply(rel,c.images[g]);
      if(rel!=one) throw std::runtime_error("surface relator failure");
      if(b3_cardinality(c.images)!=457) throw std::runtime_error("B3 failure");

      std::vector<Perm> elements{one};
      std::unordered_map<std::uint64_t,std::uint16_t> index;
      index.reserve(50000); index.emplace(key(one),0);
      std::vector<std::array<std::uint16_t,8>> transition;
      for(std::size_t head=0;head<elements.size();++head) {
        std::array<std::uint16_t,8> row{};
        for(int g=0;g<8;++g) {
          const auto z=multiply(elements[head],c.images[g]); const auto kz=key(z);
          auto it=index.find(kz);
          if(it==index.end()) {
            if(elements.size()>=65536) throw std::runtime_error("group exceeds uint16 range");
            const auto id=static_cast<std::uint16_t>(elements.size());
            index.emplace(kz,id); elements.push_back(z); row[g]=id;
          } else row[g]=it->second;
        }
        transition.push_back(row);
      }
      if(elements.size()!=38880) throw std::runtime_error("generated order is not 38880");

      std::vector<std::uint16_t> state(tree.size()); state[0]=0;
      std::uint32_t witness=0;
      for(std::uint32_t id=1;id<tree.size();++id) {
        const auto edge=tree[id];
        if(edge.parent>=id || edge.generator>=8) throw std::runtime_error("bad tree edge");
        state[id]=transition[state[edge.parent]][edge.generator];
        if((edge.depth&1U)==0U && state[id]==0) { witness=id; break; }
      }
      std::cout<<"alpha="<<c.alpha_class<<" rep="<<c.representative<<" order="<<elements.size();
      if(!witness) { std::cout<<" BASED_PASS\n"; continue; }
      std::vector<unsigned> word;
      for(auto id=witness;id!=0;id=tree[id].parent) word.push_back(tree[id].generator);
      std::reverse(word.begin(),word.end());
      std::cout<<" based_witness_id="<<witness<<" depth="<<static_cast<unsigned>(tree[witness].depth)<<" word=";
      for(std::size_t i=0;i<word.size();++i) std::cout<<(i?" ":"")<<'g'<<word[i];
      std::cout<<'\n';
    }
    return 0;
  } catch(const std::exception& e) { std::cerr<<"ERROR: "<<e.what()<<'\n'; return 2; }
}
