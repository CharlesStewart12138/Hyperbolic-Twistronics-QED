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
#include <unordered_set>
#include <utility>
#include <vector>

// Independent verifier/scanner for GAP CANDIDATE_NUMERIC records in degree 20.
// It reconstructs the actual generated image, verifies inverse pairs, eight
// distinct physical directions, the frozen relator, exact B3 cardinality 457,
// target order, and existence of the all-generators-odd C2 coloring.  It then
// evaluates the complete certified 23,129,593-node based tree and returns the
// first (therefore shortest in tree order) even identity word.
namespace {
struct Meta { std::uint32_t parent; std::uint8_t generator,depth; std::uint16_t reserved; };
static_assert(sizeof(Meta)==8);
using Perm=std::array<std::uint8_t,20>;
struct Candidate { std::string group; int alpha=0,rep=0,order=0; std::array<Perm,8> images{}; };
struct Key { std::uint64_t lo=0,hi=0; bool operator==(const Key&)const=default; };
struct KeyHash { std::size_t operator()(const Key&k)const noexcept { auto x=k.lo^(k.hi+0x9e3779b97f4a7c15ULL+(k.lo<<6)+(k.lo>>2));x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;return std::size_t(x^(x>>31)); } };

Perm one(){Perm p{};for(int i=0;i<20;++i)p[i]=std::uint8_t(i);return p;}
Perm mul(const Perm&a,const Perm&b){Perm c{};for(int i=0;i<20;++i)c[i]=b[a[i]];return c;}
Perm inv(const Perm&a){Perm b{};for(int i=0;i<20;++i)b[a[i]]=std::uint8_t(i);return b;}
Key key(const Perm&p){Key k;for(int i=0;i<12;++i)k.lo|=std::uint64_t(p[i])<<(5*i);for(int i=12;i<20;++i)k.hi|=std::uint64_t(p[i])<<(5*(i-12));return k;}

bool parse_int_token(const std::string&s,int&v){const char*b=s.data(),*e=b+s.size();auto r=std::from_chars(b,e,v);return r.ec==std::errc{}&&r.ptr==e;}
int next_int(std::istream&in){std::string s;int v;while(in>>s)if(parse_int_token(s,v))return v;throw std::runtime_error("short numeric candidate record");}
std::vector<Candidate>load_candidates(int argc,char**argv){std::vector<Candidate>out;std::set<std::tuple<std::string,int,int>>seen;
 for(int f=1;f<argc-1;++f){std::ifstream in(argv[f]);if(!in)throw std::runtime_error("cannot open candidate certificate: "+std::string(argv[f]));std::string tok;
  while(in>>tok)if(tok=="CANDIDATE_NUMERIC"){Candidate c;in>>c.group;c.alpha=next_int(in);c.rep=next_int(in);c.order=next_int(in);
   for(auto&p:c.images)for(auto&x:p){int z=next_int(in);if(z<0||z>=20)throw std::runtime_error("bad permutation entry");x=std::uint8_t(z);}
   if(seen.emplace(c.group,c.alpha,c.rep).second)out.push_back(c);
  }
 }
 return out;
}
std::vector<Meta>load_tree(const std::string&path){std::ifstream in(path,std::ios::binary);if(!in)throw std::runtime_error("cannot open based tree");char magic[8]{};std::uint64_t count=0;std::uint32_t width=0;in.read(magic,8);in.read(reinterpret_cast<char*>(&count),8);in.read(reinterpret_cast<char*>(&width),4);if(!in||std::string(magic,8)!="BOLZAT01"||count!=23'129'593ULL||width!=sizeof(Meta))throw std::runtime_error("tree contract drift");std::vector<Meta>t(count);in.read(reinterpret_cast<char*>(t.data()),std::streamsize(t.size()*sizeof(Meta)));if(!in)throw std::runtime_error("short tree");return t;}
std::size_t b3(const std::array<Perm,8>&im){std::set<Perm>s{one()};std::vector<std::pair<Perm,int>>frontier{{one(),-1}};for(int depth=1;depth<=3;++depth){std::vector<std::pair<Perm,int>>next;for(const auto&item:frontier)for(int g=0;g<8;++g){if(item.second>=0&&g==(item.second+4)%8)continue;auto z=mul(item.first,im[g]);s.insert(z);next.push_back({z,g});}frontier=std::move(next);}return s.size();}
}

int main(int argc,char**argv){try{
 if(argc<3)throw std::runtime_error("usage: CERTIFICATE... BASED_TREE_META_BIN");
 const auto candidates=load_candidates(argc,argv);std::cout<<"candidates="<<candidates.size()<<"\n";if(candidates.empty())return 0;
 const auto tree=load_tree(argv[argc-1]);const auto identity=one();
 for(const auto&c:candidates){
  if(std::set<Perm>(c.images.begin(),c.images.end()).size()!=8)throw std::runtime_error("orbit distinctness failure");
  for(int i=0;i<4;++i)if(c.images[i+4]!=inv(c.images[i]))throw std::runtime_error("inverse failure");
  Perm rel=identity;for(int g:std::array<int,8>{0,5,2,7,4,1,6,3})rel=mul(rel,c.images[g]);if(rel!=identity)throw std::runtime_error("relator failure");
  const auto b=b3(c.images);if(b!=457)throw std::runtime_error("B3 failure");
  std::vector<Perm>elements{identity};std::unordered_map<Key,std::uint16_t,KeyHash>index;index.reserve(65536);index.emplace(key(identity),0);
  std::vector<std::array<std::uint16_t,8>>transition;transition.reserve(c.order);std::vector<std::uint8_t>color{0};bool parityConsistent=true;
  for(std::size_t h=0;h<elements.size();++h){std::array<std::uint16_t,8>row{};for(int g=0;g<8;++g){auto z=mul(elements[h],c.images[g]);auto kz=key(z);auto it=index.find(kz);std::uint16_t j;
    if(it==index.end()){if(elements.size()>=65536)throw std::runtime_error("uint16 overflow");j=std::uint16_t(elements.size());index.emplace(kz,j);elements.push_back(z);color.push_back(std::uint8_t(color[h]^1U));}
    else {j=it->second;if(color[j]!=(color[h]^1U))parityConsistent=false;}
    row[g]=j;
   }transition.push_back(row);
  }
  if(int(elements.size())!=c.order)throw std::runtime_error("generated order failure");if(!parityConsistent)throw std::runtime_error("all-generators-odd parity coloring failure");
  std::vector<std::uint16_t>state(tree.size());std::uint32_t witness=0;
  for(std::uint32_t i=1;i<tree.size();++i){const auto e=tree[i];if(e.parent>=i||e.generator>=8)throw std::runtime_error("bad tree edge");state[i]=transition[state[e.parent]][e.generator];if(!(e.depth&1U)&&state[i]==0){witness=i;break;}}
  std::cout<<c.group<<" alpha="<<c.alpha<<" rep="<<c.rep<<" order="<<c.order<<" b3="<<b<<" parity=1";
  if(!witness){std::cout<<" BASED_PASS\n";continue;}
  std::vector<unsigned>word;for(auto i=witness;i;i=tree[i].parent)word.push_back(tree[i].generator);std::reverse(word.begin(),word.end());
  std::cout<<" BASED_FAIL witness_id="<<witness<<" depth="<<unsigned(tree[witness].depth)<<" word=";for(std::size_t i=0;i<word.size();++i)std::cout<<(i?" ":"")<<"g"<<word[i];std::cout<<"\n";
 }
 return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<"\n";return 2;}}
