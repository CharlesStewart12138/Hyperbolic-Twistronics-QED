#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {
constexpr int D=15;
struct P{std::array<std::uint8_t,D>x{};bool operator==(const P&)const=default;};
P id(){P r;for(int i=0;i<D;++i)r.x[i]=i;return r;}
P mul(const P&a,const P&b){P r;for(int i=0;i<D;++i)r.x[i]=a.x[b.x[i]];return r;}
P inv(const P&a){P r;for(int i=0;i<D;++i)r.x[a.x[i]]=i;return r;}
P conj(const P&t,const P&ti,const P&a){return mul(mul(t,a),ti);}
std::uint64_t pack(const P&p){std::uint64_t r=0;for(int i=0;i<D;++i)r|=std::uint64_t(p.x[i])<<(4*i);return r;}
std::uint64_t rank_perm(const P&p){std::uint64_t r=0;for(int i=0;i<D;++i){unsigned d=0;for(int j=i+1;j<D;++j)d+=p.x[j]<p.x[i];r=r*(D-i)+d;}return r;}
P unrank_perm(std::uint64_t r){
  std::array<unsigned,D> digit{};
  for(int i=D-1;i>=0;--i){unsigned base=D-i;digit[i]=unsigned(r%base);r/=base;}
  if(r)throw std::runtime_error("rank out of range");
  std::vector<unsigned> available;for(int i=0;i<D;++i)available.push_back(i);
  P p;for(int i=0;i<D;++i){if(digit[i]>=available.size())throw std::runtime_error("bad Lehmer digit");p.x[i]=available[digit[i]];available.erase(available.begin()+digit[i]);}
  return p;
}
P tau(){auto t=id();for(int i=0;i<7;++i)t.x[i]=i+1;t.x[7]=0;for(int i=8;i<11;++i)t.x[i]=i+1;t.x[11]=8;return t;}
void print_perm(const P&p){std::cout<<'[';for(int i=0;i<D;++i)std::cout<<(i?",":"")<<unsigned(p.x[i]);std::cout<<']';}

struct Meta{std::uint32_t parent;std::uint8_t generator;std::uint8_t depth;std::uint16_t reserved;};
static_assert(sizeof(Meta)==8);
std::vector<Meta> load_tree(const std::string&path){
  std::ifstream in(path,std::ios::binary);if(!in)throw std::runtime_error("cannot open based tree");
  char magic[8]{};std::uint64_t count=0;std::uint32_t size=0;
  in.read(magic,8);in.read(reinterpret_cast<char*>(&count),8);in.read(reinterpret_cast<char*>(&size),4);
  if(std::string(magic,8)!="BOLZAT01"||count!=23'129'593ULL||size!=sizeof(Meta))throw std::runtime_error("based tree contract drift");
  std::vector<Meta> tree(static_cast<std::size_t>(count));
  in.read(reinterpret_cast<char*>(tree.data()),static_cast<std::streamsize>(tree.size()*sizeof(Meta)));
  if(!in)throw std::runtime_error("short based tree");return tree;
}

struct Group{
  std::vector<P> elements;
  std::unordered_map<std::uint64_t,std::uint16_t> index;
  std::array<std::vector<std::uint16_t>,8> transition;
};
Group build_group(const std::array<P,8>&g){
  Group q;q.elements.reserve(38880);q.index.reserve(80000);
  q.elements.push_back(id());q.index.emplace(pack(id()),0);
  for(std::size_t head=0;head<q.elements.size();++head)for(int j=0;j<8;++j){
    auto y=mul(q.elements[head],g[j]);auto [it,fresh]=q.index.emplace(pack(y),static_cast<std::uint16_t>(q.elements.size()));
    if(fresh){q.elements.push_back(y);if(q.elements.size()>38880)throw std::runtime_error("generated order exceeds certified 38880");}
  }
  if(q.elements.size()!=38880)throw std::runtime_error("generated order is not 38880");
  for(int j=0;j<8;++j){q.transition[j].resize(q.elements.size());for(std::size_t i=0;i<q.elements.size();++i)q.transition[j][i]=q.index.at(pack(mul(q.elements[i],g[j])));}
  return q;
}
}

int main(int argc,char**argv){try{
  if(argc!=2)throw std::runtime_error("usage: BASED_TREE_META_BIN");
  const std::array<std::uint64_t,8> ranks{{757701091722ULL,710759741466ULL,911941300008ULL,777302836524ULL,773670498474ULL,862924518342ULL,761057489982ULL,765089238222ULL}};
  auto t=tau(),ti=inv(t);std::cout<<"tau=";print_perm(t);std::cout<<'\n';
  std::array<std::array<P,8>,8> all{};
  for(std::size_t k=0;k<ranks.size();++k){
    auto seed=unrank_perm(ranks[k]);if(rank_perm(seed)!=ranks[k])throw std::runtime_error("unrank roundtrip failure");
    all[k][0]=seed;for(int j=1;j<8;++j)all[k][j]=conj(t,ti,all[k][j-1]);
    for(int j=0;j<4;++j)if(!(all[k][j+4]==inv(all[k][j])))throw std::runtime_error("inverse closure failure");
    auto rel=id();for(int j:std::array<int,8>{0,5,2,7,4,1,6,3})rel=mul(rel,all[k][j]);if(!(rel==id()))throw std::runtime_error("relator failure");
    std::cout<<"candidate="<<k<<" rank="<<ranks[k]<<" seed=";print_perm(seed);std::cout<<'\n';
    for(int j=0;j<8;++j){std::cout<<"candidate="<<k<<" g"<<j<<'=';print_perm(all[k][j]);std::cout<<'\n';}
  }
  std::cout.flush();
  auto tree=load_tree(argv[1]);
  for(std::size_t k=0;k<ranks.size();++k){
    auto group=build_group(all[k]);
    std::vector<std::uint16_t> state(tree.size());std::uint32_t witness=0;
    for(std::uint32_t n=1;n<tree.size();++n){auto e=tree[n];if(e.parent>=n||e.generator>=8)throw std::runtime_error("bad tree edge");state[n]=group.transition[e.generator][state[e.parent]];if((e.depth&1U)==0U&&state[n]==0){witness=n;break;}}
    if(!witness){std::cout<<"candidate="<<k<<" rank="<<ranks[k]<<" BASED_PASS\n";continue;}
    std::vector<unsigned> word;for(auto n=witness;n;n=tree[n].parent)word.push_back(tree[n].generator);std::reverse(word.begin(),word.end());
    std::cout<<"candidate="<<k<<" rank="<<ranks[k]<<" based_witness_id="<<witness<<" depth="<<unsigned(tree[witness].depth)<<" word=";
    for(std::size_t i=0;i<word.size();++i)std::cout<<(i?" ":"")<<'g'<<word[i];std::cout<<'\n';std::cout.flush();
  }
  return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
