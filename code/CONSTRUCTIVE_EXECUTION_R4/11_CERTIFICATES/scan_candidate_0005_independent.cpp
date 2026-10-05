#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace fs=std::filesystem;
namespace {
constexpr std::uint32_t p=3,kArith=6561,kRecordBytes=147,kMarker=std::numeric_limits<std::uint32_t>::max();
constexpr std::uint64_t kCommit=1'000'000;
struct K{std::uint8_t a=0,b=0;}; using A=std::array<K,4>;
int mod(int x){x%=3;return x<0?x+3:x;} K add(K x,K y){return K{(std::uint8_t)mod(x.a+y.a),(std::uint8_t)mod(x.b+y.b)};}
K neg(K x){return K{(std::uint8_t)mod(-x.a),(std::uint8_t)mod(-x.b)};} K mul(K x,K y){return K{(std::uint8_t)mod(x.a*y.a+2*x.b*y.b),(std::uint8_t)mod(x.a*y.b+x.b*y.a)};}
bool zero(K x){return x.a==0&&x.b==0;} void acc(A& o,int i,K x){o[i]=add(o[i],x);}
void bp(A& o,int l,int r,K x){const K c{2,2},d{1,2},c2=mul(c,c);if(l==0){acc(o,r,x);return;}if(r==0){acc(o,l,x);return;}
 if(l==1&&r==1){acc(o,0,mul(x,c));return;}if(l==1&&r==2){acc(o,3,x);return;}if(l==2&&r==1){acc(o,0,mul(x,d));acc(o,3,neg(x));return;}
 if(l==2&&r==2){acc(o,0,mul(x,c));return;}if(l==1&&r==3){acc(o,2,mul(x,c));return;}if(l==3&&r==1){acc(o,1,mul(x,d));acc(o,2,mul(x,neg(c)));return;}
 if(l==2&&r==3){acc(o,2,mul(x,d));acc(o,1,mul(x,neg(c)));return;}if(l==3&&r==2){acc(o,1,mul(x,c));return;}
 if(l==3&&r==3){acc(o,3,mul(x,d));acc(o,0,mul(x,neg(c2)));return;}throw std::runtime_error("missing algebra product");}
A amul(A l,A r){A o{};for(int i=0;i<4;++i)if(!zero(l[i]))for(int j=0;j<4;++j)if(!zero(r[j]))bp(o,i,j,mul(l[i],r[j]));return o;}
A agen(int i){static constexpr int uv[8][4]={{1,0,0,0},{0,0,1,0},{-1,0,0,1},{0,-1,1,0},{-1,0,0,0},{0,0,-1,0},{1,0,0,-1},{0,1,-1,0}};
 A x{};x[0]=K{1,1};x[1]=K{(std::uint8_t)mod(uv[i][0]),(std::uint8_t)mod(uv[i][1])};x[2]=K{(std::uint8_t)mod(uv[i][2]),(std::uint8_t)mod(uv[i][3])};return x;}
std::uint32_t encode(const A& x){std::uint32_t n=0,s=1;for(auto k:x)for(auto d:{k.a,k.b}){n+=s*d;s*=3;}return n;}
A decode(std::uint32_t n){A x{};for(auto& k:x){k.a=n%3;n/=3;k.b=n%3;n/=3;}return x;}
std::array<std::vector<std::uint32_t>,8> arith_trans(){std::array<std::vector<std::uint32_t>,8> t;for(auto& r:t)r.resize(kArith);
 for(std::uint32_t n=0;n<kArith;++n){A x=decode(n);for(int i=0;i<8;++i)t[i][n]=encode(amul(x,agen(i)));}return t;}
std::uint8_t qcoc(std::uint8_t l,std::uint8_t r){l&=15;r&=15;std::uint8_t z0=(((l&2)&&(r&2))^((l&4)&&(r&4)))&1;
 std::uint8_t z1=(((l&1)&&(r&1))^((l&8)&&(r&8)))&1;return z0|(z1<<1);}
std::uint8_t qmul(std::uint8_t l,std::uint8_t r){auto lv=l&15,rv=r&15,lz=(l>>4)&3,rz=(r>>4)&3;return (std::uint8_t)((lv^rv)|((lz^rz^qcoc(lv,rv))<<4));}
constexpr std::array<std::uint8_t,8> qgen{{1,18,55,27,33,2,23,11}};
struct Machine{std::vector<std::pair<std::uint32_t,std::uint8_t>> elements;std::vector<std::array<std::uint32_t,8>> next;};
Machine build_machine(){auto at=arith_trans();const std::uint32_t ai=encode(A{K{1,0},K{},K{},K{}});Machine m;std::queue<std::uint32_t> todo;
 std::unordered_map<std::uint64_t,std::uint32_t> id;auto key=[](std::uint32_t a,std::uint8_t q){return (std::uint64_t(a)<<6)|q;};
 m.elements.push_back({ai,0});m.next.push_back({});id[key(ai,0)]=0;todo.push(0);
 while(!todo.empty()){auto s=todo.front();todo.pop();auto [a,q]=m.elements[s];std::array<std::uint32_t,8> row{};
  for(int i=0;i<8;++i){auto na=at[i][a];auto nq=qmul(q,qgen[i]);auto k=key(na,nq);auto it=id.find(k);std::uint32_t target;
   if(it==id.end()){target=(std::uint32_t)m.elements.size();id[k]=target;m.elements.push_back({na,nq});m.next.push_back({});todo.push(target);}else target=it->second;row[i]=target;}
  m.next[s]=row;}
 if(m.elements.size()!=46080)throw std::runtime_error("independent actual image order is not 46080");return m;}
std::uint8_t digit(std::uint64_t hi,std::uint64_t lo,unsigned depth,unsigned i){unsigned sh=3*(depth-1-i);return sh<64?(lo>>sh)&7:(hi>>(sh-64))&7;}
std::uint32_t image(const Machine& m,std::uint64_t hi,std::uint64_t lo,unsigned depth){std::uint32_t s=0;for(unsigned i=0;i<depth;++i)s=m.next[s][digit(hi,lo,depth,i)];return s;}
std::uint32_t word(const Machine& m,const std::vector<unsigned>& w){std::uint32_t s=0;for(auto i:w)s=m.next[s][i];return s;}
void self_test(const Machine& m){for(unsigned i=0;i<8;++i)if(word(m,{i,(i+4)%8})!=0)throw std::runtime_error("inverse-shell self-test");
 if(word(m,{0,5,2,7,4,1,6,3})!=0)throw std::runtime_error("surface-relator self-test");
 std::unordered_set<std::uint32_t> all{0};std::vector<std::pair<std::uint32_t,int>> front{{0,-1}};
 for(int d=1;d<=3;++d){std::vector<std::pair<std::uint32_t,int>> next;for(auto [s,last]:front)for(int i=0;i<8;++i)if(last<0||i!=(last+4)%8){auto t=m.next[s][i];all.insert(t);next.push_back({t,i});}front=std::move(next);}
 if(all.size()!=457)throw std::runtime_error("complete B3 self-test");}
std::uint64_t u64(std::istream& in){std::uint64_t x=0;in.read((char*)&x,8);return x;}std::uint32_t u32(std::istream& in){std::uint32_t x=0;in.read((char*)&x,4);return x;}
struct State{std::uint64_t scanned=0;bool hit=false;};
State load(const fs::path& p){State s;if(!fs::exists(p))return s;std::ifstream h(p);std::string line;while(std::getline(h,line)){auto k=line.find('\t');if(k==std::string::npos)continue;auto a=line.substr(0,k),b=line.substr(k+1);if(a=="scanned_records")s.scanned=std::stoull(b);if(a=="hit")s.hit=b=="1";}return s;}
void save(const fs::path& p,State s,std::uint64_t total,double elapsed){auto tmp=fs::path(p.string()+".tmp");std::ofstream h(tmp);h<<"schema_version\t1.0\nalgorithm\tCAND-R4-0005-independent-joint-state\nactual_image_order\t46080\ntotal_records\t"<<total<<"\nscanned_records\t"<<s.scanned<<"\nhit\t"<<(s.hit?1:0)<<"\nelapsed_seconds\t"<<elapsed<<'\n';h.close();if(fs::exists(p))fs::remove(p);fs::rename(tmp,p);}
std::string ws(std::uint64_t hi,std::uint64_t lo,unsigned depth){std::ostringstream o;for(unsigned i=0;i<depth;++i){if(i)o<<' ';o<<'g'<<(unsigned)digit(hi,lo,depth,i);}return o.str();}
void witness(const fs::path& p,std::uint64_t rec,unsigned d,std::uint64_t hi,std::uint64_t lo){std::ofstream h(p);h<<"record_index\tdepth\tword\tword_high\tword_low\n"<<rec<<'\t'<<d<<'\t'<<ws(hi,lo,d)<<'\t'<<hi<<'\t'<<lo<<'\n';}
void scan(const fs::path& registry,const fs::path& cp,const fs::path& wit){Machine m=build_machine();self_test(m);std::ifstream in(registry,std::ios::binary);if(!in)throw std::runtime_error("registry open");
 static std::array<char,16*1024*1024> buffer{};in.rdbuf()->pubsetbuf(buffer.data(),buffer.size());char magic[8]{};in.read(magic,8);if(std::string(magic,8)!="BOLZGEO1")throw std::runtime_error("magic");
 auto total=u64(in);if(u32(in)!=kRecordBytes||u32(in)!=kMarker)throw std::runtime_error("header");if(fs::file_size(registry)!=24+total*kRecordBytes)throw std::runtime_error("file size contract");
 State s=load(cp);if(s.hit)return;in.seekg((std::streamoff)(24+s.scanned*kRecordBytes));std::array<char,kRecordBytes> raw{};auto start=std::chrono::steady_clock::now();auto commit=std::min(total,((s.scanned/kCommit)+1)*kCommit);
 while(s.scanned<total){in.read(raw.data(),raw.size());if(!in)throw std::runtime_error("short record");auto rec=s.scanned++;unsigned d=(std::uint8_t)raw[130];std::uint64_t hi=0,lo=0;std::memcpy(&hi,raw.data()+131,8);std::memcpy(&lo,raw.data()+139,8);
  if(d&&image(m,hi,lo,d)==0){s.hit=true;witness(wit,rec,d,hi,lo);double e=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();save(cp,s,total,e);std::cout<<"HIT "<<rec<<' '<<ws(hi,lo,d)<<'\n';return;}
  if(s.scanned==commit){double e=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();save(cp,s,total,e);if(!(s.scanned%25000000))std::cout<<"scanned="<<s.scanned<<'/'<<total<<'\n'<<std::flush;commit=std::min(total,commit+kCommit);}}
 double e=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();save(cp,s,total,e);std::cout<<"COMPLETE_NO_HIT\n";}
}
int main(int argc,char** argv){try{if(argc!=4)throw std::runtime_error("usage: REGISTRY CHECKPOINT WITNESS");scan(argv[1],argv[2],argv[3]);return 0;}catch(const std::exception& e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
