#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>

namespace {
constexpr int BASE=8192,GENS=8,B3WORDS=457,DIM=25;
using Bits=std::uint32_t;
struct Transition{std::uint16_t next=0;Bits delta=0;};
struct Meta{std::uint32_t parent;std::uint8_t generator,depth;std::uint16_t reserved;};
static_assert(sizeof(Meta)==8);
struct B3State{int parent=-1,generator=-1;std::uint16_t base=0;Bits layer=0;};
struct Tables{std::array<std::array<Transition,GENS>,BASE>trans{};std::array<B3State,B3WORDS>b3{};};
struct Candidate{Bits f1=0,f2=0;std::string type;std::uint32_t witness=0;};
Bits parse_bits(const std::string&s){if(s.size()!=DIM)throw std::runtime_error("bad 25-bit mask");Bits v=0;for(int i=0;i<DIM;++i){if(s[i]=='1')v|=Bits{1}<<i;else if(s[i]!='0')throw std::runtime_error("non-bit mask");}return v;}
std::string bits(Bits v){std::string s(DIM,'0');for(int i=0;i<DIM;++i)if(v&(Bits{1}<<i))s[i]='1';return s;}
int dot(Bits a,Bits b){return std::popcount(a&b)&1;}
Tables load_tables(const std::string&path){std::ifstream in(path);if(!in)throw std::runtime_error("cannot open transition export");Tables t;std::array<std::array<bool,GENS>,BASE>seen{};std::array<bool,B3WORDS>bseen{};std::string line;int nt=0,nb=0;
 while(std::getline(in,line)){std::istringstream ls(line);std::string tag;ls>>tag;if(tag=="TRANS"){int u,g,v;std::string d;ls>>u>>g>>v>>d;if(u<0||u>=BASE||g<0||g>=GENS||v<0||v>=BASE||seen[u][g])throw std::runtime_error("bad/duplicate transition");seen[u][g]=true;t.trans[u][g]={static_cast<std::uint16_t>(v),parse_bits(d)};++nt;}
  else if(tag=="B3STATE"){int i,p,g,u;std::string d;ls>>i>>p>>g>>u>>d;if(i<0||i>=B3WORDS||u<0||u>=BASE||bseen[i])throw std::runtime_error("bad/duplicate B3 state");bseen[i]=true;t.b3[i]={p,g,static_cast<std::uint16_t>(u),parse_bits(d)};++nb;}}
 if(nt!=BASE*GENS||nb!=B3WORDS)throw std::runtime_error("incomplete transition export");
 if(t.b3[0].parent!=-1||t.b3[0].generator!=-1||t.b3[0].base!=0||t.b3[0].layer!=0)throw std::runtime_error("bad B3 root");
 for(int i=1;i<B3WORDS;++i){auto&r=t.b3[i];if(r.parent<0||r.parent>=i||r.generator<0||r.generator>=GENS)throw std::runtime_error("bad B3 parent");auto q=t.trans[t.b3[r.parent].base][r.generator];if(q.next!=r.base||(t.b3[r.parent].layer^q.delta)!=r.layer)throw std::runtime_error("all-457 GAP/direct transition cross-check failed");}
 return t;}
std::vector<Candidate>load_candidates(const std::string&path){std::ifstream in(path);if(!in)throw std::runtime_error("cannot open classifier output");std::vector<Candidate>c;std::string line;while(std::getline(in,line))if(line.rfind("B3_SURVIVOR\t",0)==0){std::istringstream ls(line);std::string tag,k,type,f1,f2,tmp;int dim,order;ls>>tag>>k>>dim>>k>>type>>k>>order>>k>>f1>>k>>f2;if(dim!=2||order!=32768)throw std::runtime_error("unexpected B3 survivor");c.push_back({parse_bits(f1),parse_bits(f2),type,0});}
 if(c.size()!=512)throw std::runtime_error("classifier does not contain exactly 512 survivors");std::set<std::array<Bits,3>>uniq;for(auto&q:c){std::array<Bits,3>a{q.f1,q.f2,Bits(q.f1^q.f2)};std::sort(a.begin(),a.end());uniq.insert(a);}if(uniq.size()!=c.size())throw std::runtime_error("duplicate quotient planes");return c;}
std::vector<Meta>load_tree(const std::string&path){std::ifstream in(path,std::ios::binary);if(!in)throw std::runtime_error("cannot open based tree");char magic[8]{};std::uint64_t count=0;std::uint32_t size=0;in.read(magic,8);in.read(reinterpret_cast<char*>(&count),8);in.read(reinterpret_cast<char*>(&size),4);if(std::string(magic,8)!="BOLZAT01"||count!=23'129'593ULL||size!=sizeof(Meta))throw std::runtime_error("based tree header drift");std::vector<Meta>tree(count);in.read(reinterpret_cast<char*>(tree.data()),static_cast<std::streamsize>(tree.size()*sizeof(Meta)));if(!in)throw std::runtime_error("short based tree");if(tree[0].parent||tree[0].depth)throw std::runtime_error("bad tree root");std::uint8_t prev=0;for(std::uint32_t i=1;i<tree.size();++i){auto&e=tree[i];if(e.parent>=i||e.generator>=8||e.depth!=tree[e.parent].depth+1||e.depth<prev)throw std::runtime_error("tree is not parent-valid breadth-first order");prev=e.depth;}return tree;}
std::vector<unsigned>word(std::uint32_t i,const std::vector<Meta>&tree){std::vector<unsigned>w;while(i){w.push_back(tree[i].generator);i=tree[i].parent;}std::reverse(w.begin(),w.end());return w;}
}
int main(int argc,char**argv)try{
 if(argc!=5)throw std::runtime_error("usage: scanner TRANSITIONS CLASSIFIER BASED_TREE OUTPUT");auto tab=load_tables(argv[1]);auto cand=load_candidates(argv[2]);
 // Independent B3 reconstruction from the 457 directly certified U3 states.
 for(const auto&c:cand){std::set<std::tuple<std::uint16_t,int,int>>keys;for(const auto&s:tab.b3)keys.emplace(s.base,dot(s.layer,c.f1),dot(s.layer,c.f2));if(keys.size()!=457)throw std::runtime_error("candidate fails independent B3 reconstruction");}
 auto tree=load_tree(argv[3]);std::vector<std::uint16_t>base(tree.size());std::vector<Bits>layer(tree.size());std::size_t unresolved=cand.size();std::uint32_t lastScanned=0;
 for(std::uint32_t i=1;i<tree.size();++i){auto&e=tree[i];auto tr=tab.trans[base[e.parent]][e.generator];base[i]=tr.next;layer[i]=layer[e.parent]^tr.delta;lastScanned=i;
  if((e.depth&1U)==0U&&base[i]==0){for(auto&c:cand)if(!c.witness&&!dot(layer[i],c.f1)&&!dot(layer[i],c.f2)){c.witness=i;--unresolved;}}
  if(!unresolved)break;
 }
 std::ofstream out(argv[4]);if(!out)throw std::runtime_error("cannot create output");out<<"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-MODULE-BASED-SCAN\n"
  <<"SCOPE\tall 512 B3 survivors among full-U2-skeleton central quotients U3/W with dim(L3/W)=2\n"
  <<"METHOD\tone exact frozen-tree pass using (13-bit U2 state,25-bit central state); candidate identity iff U2 state=0 and both dual functionals vanish\n"
  <<"TRANSITION_ROWS\t65536\nB3_DIRECT_CROSSCHECK_ROWS\t457\nB3_CANDIDATES_RECHECKED\t"<<cand.size()<<"\nBASED_TREE_NODES\t"<<tree.size()<<"\nTREE_BREADTH_FIRST\ttrue\nLAST_SCANNED_NODE\t"<<lastScanned<<"\n";
 std::size_t pass=0;for(std::size_t n=0;n<cand.size();++n){auto&c=cand[n];out<<"CANDIDATE\t"<<n+1<<"\tTYPE\t"<<c.type<<"\tORDER\t32768\tF1\t"<<bits(c.f1)<<"\tF2\t"<<bits(c.f2);
  if(!c.witness){++pass;out<<"\tBASED_PASS\ttrue\n";continue;}auto w=word(c.witness,tree);std::uint16_t u=0;Bits d=0;for(auto g:w){auto tr=tab.trans[u][g];u=tr.next;d^=tr.delta;}if(u||dot(d,c.f1)||dot(d,c.f2))throw std::runtime_error("witness replay failure");
  out<<"\tBASED_PASS\tfalse\tSHORTEST_EVEN_WITNESS_ID\t"<<c.witness<<"\tDEPTH\t"<<unsigned(tree[c.witness].depth)<<"\tLAYER_MASK\t"<<bits(d)<<"\tWORD";for(auto g:w)out<<"\tg"<<g;out<<"\n";}
 out<<"TOTAL\tCANDIDATES\t"<<cand.size()<<"\tBASED_PASS\t"<<pass<<"\tBASED_FAIL\t"<<cand.size()-pass<<"\nRESULT\tPASS\nDONE\n";return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}
