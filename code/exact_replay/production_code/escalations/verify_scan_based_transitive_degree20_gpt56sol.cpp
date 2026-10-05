#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {
struct Meta { std::uint32_t parent; std::uint8_t generator, depth; std::uint16_t reserved; };
static_assert(sizeof(Meta) == 8);
using Perm = std::array<std::uint8_t,20>;
struct PermHash {
  std::size_t operator()(const Perm& p) const noexcept {
    std::uint64_t h=1469598103934665603ULL;
    for (auto x:p) { h^=x; h*=1099511628211ULL; }
    return static_cast<std::size_t>(h);
  }
};
struct Candidate {
  std::string group;
  int alpha=0, rep=0, claimed_order=0;
  std::array<Perm,8> image{};
};
Perm identity() { Perm p{}; for(int i=0;i<20;++i)p[i]=static_cast<std::uint8_t>(i); return p; }
Perm multiply(const Perm&a,const Perm&b) {
  Perm c{}; for(int i=0;i<20;++i)c[i]=b[a[i]]; return c; // GAP right action
}
Perm inverse(const Perm&a) { Perm b{}; for(int i=0;i<20;++i)b[a[i]]=static_cast<std::uint8_t>(i); return b; }
bool parse_int(const std::string&s,int&v) {
  const char*b=s.data(),*e=b+s.size(); auto r=std::from_chars(b,e,v);
  return r.ec==std::errc{} && r.ptr==e;
}
std::string key(const Candidate&c) {
  std::string k=c.group+"/"+std::to_string(c.alpha)+"/"+std::to_string(c.rep)+"/"+std::to_string(c.claimed_order);
  for(const auto&p:c.image)for(auto x:p){k.push_back('/');k+=std::to_string(x);}
  return k;
}
std::vector<Candidate> load_candidates(const std::vector<std::string>&paths,std::size_t&partial) {
  std::vector<Candidate> out; std::unordered_set<std::string> seen; partial=0;
  for(const auto&path:paths) {
    std::ifstream in(path); if(!in)throw std::runtime_error("cannot open candidate file: "+path);
    std::string line;
    while(std::getline(in,line)) {
      if(line.rfind("CANDIDATE_NUMERIC\t",0)!=0)continue;
      std::istringstream ls(line); std::string tag; Candidate c; ls>>tag>>c.group>>c.alpha>>c.rep>>c.claimed_order;
      bool ok=bool(ls);
      for(auto&p:c.image)for(auto&x:p){int z=-1;if(!(ls>>z)||z<0||z>=20){ok=false;break;}x=static_cast<std::uint8_t>(z);}
      std::string extra; if(ls>>extra)ok=false;
      if(!ok){++partial;continue;}
      auto k=key(c); if(seen.insert(k).second)out.push_back(c);
    }
  }
  return out;
}
std::vector<Meta> load_tree(const std::string&path) {
  std::ifstream in(path,std::ios::binary); if(!in)throw std::runtime_error("cannot open based tree: "+path);
  char magic[8]{};std::uint64_t count=0;std::uint32_t sz=0;
  in.read(magic,8);in.read(reinterpret_cast<char*>(&count),8);in.read(reinterpret_cast<char*>(&sz),4);
  if(std::string(magic,8)!="BOLZAT01"||count!=23'129'593ULL||sz!=sizeof(Meta))
    throw std::runtime_error("based-tree header contract drift");
  std::vector<Meta> tree(count);in.read(reinterpret_cast<char*>(tree.data()),static_cast<std::streamsize>(tree.size()*sizeof(Meta)));
  if(!in)throw std::runtime_error("short based tree");
  if(tree[0].parent!=0||tree[0].depth!=0)throw std::runtime_error("bad based-tree root");
  std::uint8_t previous_depth=0;
  for(std::uint32_t i=1;i<tree.size();++i) {
    const auto&e=tree[i];
    if(e.parent>=i||e.generator>=8||e.depth!=static_cast<std::uint8_t>(tree[e.parent].depth+1)||e.depth<previous_depth)
      throw std::runtime_error("based tree is not a parent-valid breadth-first tree");
    previous_depth=e.depth;
  }
  return tree;
}
std::size_t b3(const std::array<Perm,8>&im) {
  std::set<Perm>s{identity()};std::vector<std::pair<Perm,int>>fr{{identity(),-1}};
  for(int d=1;d<=3;++d){std::vector<std::pair<Perm,int>>nx;for(const auto&v:fr)for(int g=0;g<8;++g){
    if(v.second>=0&&g==(v.second+4)%8)continue;auto z=multiply(v.first,im[g]);s.insert(z);nx.push_back({z,g});}
    fr=std::move(nx);}return s.size();
}
struct FiniteImage {
  std::vector<Perm> elements;
  std::vector<std::array<std::uint16_t,8>> transition;
  bool parity_consistent=true;
};
FiniteImage enumerate_image(const std::array<Perm,8>&im) {
  FiniteImage r; r.elements.push_back(identity());
  std::unordered_map<Perm,std::uint16_t,PermHash> index; index.reserve(50000); index.emplace(identity(),0);
  std::vector<std::int8_t> parity{0};
  for(std::size_t h=0;h<r.elements.size();++h){std::array<std::uint16_t,8>row{};
    for(int g=0;g<8;++g){auto z=multiply(r.elements[h],im[g]);auto it=index.find(z);std::uint16_t j;
      if(it==index.end()){if(r.elements.size()>=65536)throw std::runtime_error("image exceeds uint16 capacity");
        j=static_cast<std::uint16_t>(r.elements.size());index.emplace(z,j);r.elements.push_back(z);parity.push_back(parity[h]^1);
      }else{j=it->second;if(parity[j]!=(parity[h]^1))r.parity_consistent=false;}row[g]=j;}
    r.transition.push_back(row);
  }
  return r;
}
std::vector<unsigned> witness_word(std::uint32_t id,const std::vector<Meta>&tree) {
  std::vector<unsigned>w;while(id){w.push_back(tree[id].generator);id=tree[id].parent;}std::reverse(w.begin(),w.end());return w;
}
}

int main(int argc,char**argv)try {
  if(argc<4)throw std::runtime_error("usage: verifier OUTPUT BASED_TREE CANDIDATE_CERTIFICATE...");
  const std::string output=argv[1],treepath=argv[2];std::vector<std::string>inputs;
  for(int i=3;i<argc;++i)inputs.emplace_back(argv[i]);
  std::ofstream out(output);if(!out)throw std::runtime_error("cannot create output");
  std::size_t partial=0;auto candidates=load_candidates(inputs,partial);
  out<<"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE20-INDEPENDENT-VERIFY-BASED\n"
     <<"PERM_CONVENTION\tGAP right action: (a*b)[i]=b[a[i]]\n"
     <<"INPUT_FILES\t"<<inputs.size()<<"\nUNIQUE_CANDIDATES\t"<<candidates.size()<<"\nPARTIAL_RECORDS_IGNORED\t"<<partial<<"\n";
  if(candidates.empty()){out<<"RESULT\tNO_CURRENT_CANDIDATES\nDONE\n";return 0;}
  auto tree=load_tree(treepath);out<<"BASED_TREE_NODES\t"<<tree.size()<<"\nBASED_TREE_BREADTH_FIRST\ttrue\n";
  std::size_t pass=0;
  for(const auto&c:candidates){
    for(const auto&p:c.image){std::array<bool,20>seen{};for(auto x:p){if(seen[x])throw std::runtime_error("non-bijection in "+c.group);seen[x]=true;}}
    for(int i=0;i<4;++i)if(c.image[i+4]!=inverse(c.image[i]))throw std::runtime_error("inverse-pair failure in "+c.group);
    if(std::set<Perm>(c.image.begin(),c.image.end()).size()!=8)throw std::runtime_error("physical orbit is not distinct in "+c.group);
    Perm rel=identity();for(int g:std::array<int,8>{0,5,2,7,4,1,6,3})rel=multiply(rel,c.image[g]);
    if(rel!=identity())throw std::runtime_error("surface relator failure in "+c.group);
    const auto card=b3(c.image);if(card!=457)throw std::runtime_error("B3 failure in "+c.group);
    auto image=enumerate_image(c.image);const auto order=image.elements.size();
    if(order!=static_cast<std::size_t>(c.claimed_order)||order<2338||order>50000)throw std::runtime_error("target-order failure in "+c.group);
    if(!image.parity_consistent)throw std::runtime_error("frozen all-physical-odd parity is not well-defined in "+c.group);
    std::vector<std::uint16_t>state(tree.size());std::uint32_t witness=0;
    for(std::uint32_t i=1;i<tree.size();++i){const auto&e=tree[i];state[i]=image.transition[state[e.parent]][e.generator];
      if((e.depth&1U)==0U&&state[i]==0){witness=i;break;}}
    out<<"CANDIDATE\t"<<c.group<<"\tALPHA\t"<<c.alpha<<"\tREP\t"<<c.rep
       <<"\tORDER\t"<<order<<"\tBIJECTIONS\ttrue\tINVERSES\ttrue\tORBIT8\ttrue\tRELATOR\ttrue"
       <<"\tB3\t"<<card<<"\tGENERATE\ttrue\tPARITY_ALL_PHYSICAL_ODD\ttrue";
    if(!witness){++pass;out<<"\tBASED_PASS\ttrue\n";continue;}
    auto word=witness_word(witness,tree);Perm z=identity();for(auto g:word)z=multiply(z,c.image[g]);if(z!=identity())throw std::runtime_error("reported witness does not evaluate to identity");
    out<<"\tBASED_PASS\tfalse\tSHORTEST_EVEN_WITNESS_ID\t"<<witness<<"\tDEPTH\t"<<unsigned(tree[witness].depth)<<"\tWORD";
    for(auto g:word)out<<"\tg"<<g;out<<"\n";
  }
  out<<"TOTAL\tCANDIDATES\t"<<candidates.size()<<"\tBASED_PASS\t"<<pass<<"\tBASED_FAIL\t"<<(candidates.size()-pass)<<"\nRESULT\tPASS\nDONE\n";
  return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}
