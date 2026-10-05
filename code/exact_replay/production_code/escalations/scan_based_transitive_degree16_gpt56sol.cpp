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
struct Meta { std::uint32_t parent; std::uint8_t generator,depth; std::uint16_t reserved; };
static_assert(sizeof(Meta)==8);
using Perm=std::array<std::uint8_t,16>;
struct Candidate { std::string group; int alpha=0,rep=0,order=0; std::array<Perm,8> images{}; };

Perm one(){Perm p{};for(int i=0;i<16;++i)p[i]=static_cast<std::uint8_t>(i);return p;}
Perm mul(const Perm&a,const Perm&b){Perm c{};for(int i=0;i<16;++i)c[i]=b[a[i]];return c;}
Perm inv(const Perm&a){Perm b{};for(int i=0;i<16;++i)b[a[i]]=static_cast<std::uint8_t>(i);return b;}
std::uint64_t key(const Perm&p){std::uint64_t k=0;for(int i=0;i<16;++i)k|=static_cast<std::uint64_t>(p[i])<<(4*i);return k;}

bool parse_int_token(const std::string&s,int&v){const char*b=s.data(),*e=b+s.size();auto r=std::from_chars(b,e,v);return r.ec==std::errc{}&&r.ptr==e;}
int next_int(std::istream&in){std::string s;int v;while(in>>s)if(parse_int_token(s,v))return v;throw std::runtime_error("short numeric candidate record");}
std::vector<Candidate> load_candidates(int argc,char**argv){std::vector<Candidate> out;
 for(int f=1;f<argc-1;++f){std::ifstream in(argv[f]);if(!in)throw std::runtime_error("cannot open candidate certificate");std::string tok;
  while(in>>tok)if(tok=="CANDIDATE_NUMERIC"){Candidate c;in>>c.group;c.alpha=next_int(in);c.rep=next_int(in);c.order=next_int(in);
   for(auto&p:c.images)for(auto&x:p){int z=next_int(in);if(z<0||z>=16)throw std::runtime_error("bad permutation entry");x=static_cast<std::uint8_t>(z);}out.push_back(c);}
 }return out;}
std::vector<Meta> load_tree(const std::string&path){std::ifstream in(path,std::ios::binary);if(!in)throw std::runtime_error("cannot open based tree");char magic[8]{};std::uint64_t count=0;std::uint32_t sz=0;in.read(magic,8);in.read(reinterpret_cast<char*>(&count),8);in.read(reinterpret_cast<char*>(&sz),4);if(std::string(magic,8)!="BOLZAT01"||count!=23'129'593ULL||sz!=sizeof(Meta))throw std::runtime_error("tree contract drift");std::vector<Meta>t(count);in.read(reinterpret_cast<char*>(t.data()),static_cast<std::streamsize>(t.size()*sizeof(Meta)));if(!in)throw std::runtime_error("short tree");return t;}
std::size_t b3(const std::array<Perm,8>&im){std::set<std::uint64_t>s{key(one())};std::vector<std::pair<Perm,int>>fr{{one(),-1}};for(int d=1;d<=3;++d){std::vector<std::pair<Perm,int>>nx;for(const auto&a:fr)for(int g=0;g<8;++g){if(a.second>=0&&g==(a.second+4)%8)continue;auto z=mul(a.first,im[g]);s.insert(key(z));nx.push_back({z,g});}fr=std::move(nx);}return s.size();}
}
int main(int argc,char**argv){try{if(argc<3)throw std::runtime_error("usage: CERTIFICATE... BASED_TREE_META_BIN");const auto cs=load_candidates(argc,argv);std::cout<<"candidates="<<cs.size()<<'\n';if(cs.empty())return 0;const auto tree=load_tree(argv[argc-1]);const auto id=one();
 for(const auto&c:cs){for(int i=0;i<4;++i)if(c.images[i+4]!=inv(c.images[i]))throw std::runtime_error("inverse failure");Perm r=id;for(int g:std::array<int,8>{0,5,2,7,4,1,6,3})r=mul(r,c.images[g]);if(r!=id)throw std::runtime_error("relator failure");if(b3(c.images)!=457)throw std::runtime_error("B3 failure");
  std::vector<Perm>els{id};std::unordered_map<std::uint64_t,std::uint16_t>idx;idx.reserve(50000);idx.emplace(key(id),0);std::vector<std::array<std::uint16_t,8>>tr;
  for(std::size_t h=0;h<els.size();++h){std::array<std::uint16_t,8>row{};for(int g=0;g<8;++g){auto z=mul(els[h],c.images[g]);auto kz=key(z);auto it=idx.find(kz);if(it==idx.end()){if(els.size()>=65536)throw std::runtime_error("uint16 overflow");auto j=static_cast<std::uint16_t>(els.size());idx.emplace(kz,j);els.push_back(z);row[g]=j;}else row[g]=it->second;}tr.push_back(row);}if(static_cast<int>(els.size())!=c.order)throw std::runtime_error("order failure");
  std::vector<std::uint16_t>state(tree.size());std::uint32_t witness=0;for(std::uint32_t i=1;i<tree.size();++i){auto e=tree[i];if(e.parent>=i||e.generator>=8)throw std::runtime_error("bad tree edge");state[i]=tr[state[e.parent]][e.generator];if((e.depth&1U)==0U&&state[i]==0){witness=i;break;}}
  std::cout<<c.group<<" alpha="<<c.alpha<<" rep="<<c.rep<<" order="<<c.order;if(!witness){std::cout<<" BASED_PASS\n";continue;}std::vector<unsigned>w;for(auto i=witness;i;i=tree[i].parent)w.push_back(tree[i].generator);std::reverse(w.begin(),w.end());std::cout<<" witness_id="<<witness<<" depth="<<static_cast<unsigned>(tree[witness].depth)<<" word=";for(std::size_t i=0;i<w.size();++i)std::cout<<(i?" ":"")<<'g'<<w[i];std::cout<<'\n';
 }return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
