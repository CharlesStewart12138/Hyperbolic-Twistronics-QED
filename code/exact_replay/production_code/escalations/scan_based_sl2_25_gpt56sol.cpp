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
struct Meta { std::uint32_t parent; std::uint8_t generator, depth; std::uint16_t reserved; };
static_assert(sizeof(Meta)==8);
using Mat=std::array<std::uint8_t,4>;
struct Field {
  std::array<std::array<std::uint8_t,25>,25> a{},m{}; std::array<std::uint8_t,25> n{},iv{},fr{};
  Field(){for(int x=0;x<25;++x){int x0=x%5,x1=x/5;n[x]=(-x0+5)%5+5*((-x1+5)%5);for(int y=0;y<25;++y){int y0=y%5,y1=y/5;a[x][y]=(x0+y0)%5+5*((x1+y1)%5);m[x][y]=(x0*y0+3*x1*y1)%5+5*((x0*y1+x1*y0)%5);}}
    for(int x=1;x<25;++x)for(int y=1;y<25;++y)if(m[x][y]==1){iv[x]=y;break;}for(int x=0;x<25;++x)fr[x]=power(x,5);}
  std::uint8_t power(std::uint8_t x,unsigned e)const{std::uint8_t r=1;while(e){if(e&1)r=m[r][x];x=m[x][x];e>>=1;}return r;}
  std::uint8_t det(const Mat&x)const{return a[m[x[0]][x[3]]][n[m[x[1]][x[2]]]];}
  Mat mul(const Mat&x,const Mat&y)const{return{a[m[x[0]][y[0]]][m[x[1]][y[2]]],a[m[x[0]][y[1]]][m[x[1]][y[3]]],a[m[x[2]][y[0]]][m[x[3]][y[2]]],a[m[x[2]][y[1]]][m[x[3]][y[3]]]};}
  Mat inverse(const Mat&x)const{auto s=iv[det(x)];return{m[x[3]][s],m[n[x[1]]][s],m[n[x[2]]][s],m[x[0]][s]};}
  Mat sigma(const Mat&x)const{return{fr[x[0]],fr[x[1]],fr[x[2]],fr[x[3]]};}
  Mat act(const Mat&c,const Mat&x)const{return mul(mul(c,sigma(x)),inverse(c));}
};
std::uint32_t pack(const Mat&x){return x[0]|(std::uint32_t(x[1])<<5)|(std::uint32_t(x[2])<<10)|(std::uint32_t(x[3])<<15);}
std::vector<Meta> load(const char*path){std::ifstream in(path,std::ios::binary);char magic[8]{};std::uint64_t count=0;std::uint32_t size=0;in.read(magic,8);in.read(reinterpret_cast<char*>(&count),8);in.read(reinterpret_cast<char*>(&size),4);if(!in||std::string(magic,8)!="BOLZAT01"||count!=23129593ULL||size!=8)throw std::runtime_error("tree contract");std::vector<Meta>v(count);in.read(reinterpret_cast<char*>(v.data()),v.size()*8ULL);if(!in)throw std::runtime_error("short tree");return v;}
}
int main(int argc,char**argv){try{if(argc!=2)throw std::runtime_error("usage: TREE");Field f;const Mat one{1,0,0,1},c{0,1,5,5};const std::array<Mat,16> seeds{{
  {{0,6,13,22}},{{0,7,8,22}},{{0,23,22,8}},{{0,24,17,8}},{{1,7,9,7}},{{1,10,14,18}},{{1,16,13,7}},{{1,17,1,18}},
  {{1,18,12,10}},{{1,22,19,10}},{{2,6,6,5}},{{2,9,9,20}},{{6,6,1,18}},{{6,10,8,18}},{{8,10,11,18}},{{8,12,1,18}} }};
  std::vector<Mat> el;std::unordered_map<std::uint32_t,std::uint16_t> idx;for(int a=0;a<25;++a)for(int b=0;b<25;++b)for(int cc=0;cc<25;++cc)for(int d=0;d<25;++d){Mat x{(std::uint8_t)a,(std::uint8_t)b,(std::uint8_t)cc,(std::uint8_t)d};if(f.det(x)==1){idx.emplace(pack(x),el.size());el.push_back(x);}}if(el.size()!=15600)throw std::runtime_error("SL order");auto id=idx.at(pack(one));auto tree=load(argv[1]);
  for(std::size_t k=0;k<seeds.size();++k){std::array<Mat,8> im{};im[0]=seeds[k];for(int i=1;i<8;++i)im[i]=f.act(c,im[i-1]);for(int i=0;i<4;++i)if(im[i+4]!=f.inverse(im[i]))throw std::runtime_error("inverse closure");Mat r=one;for(int j:std::array<int,8>{0,5,2,7,4,1,6,3})r=f.mul(r,im[j]);if(r!=one)throw std::runtime_error("relator");
    std::array<std::vector<std::uint16_t>,8> tr;for(int g=0;g<8;++g){tr[g].resize(el.size());for(std::size_t x=0;x<el.size();++x)tr[g][x]=idx.at(pack(f.mul(el[x],im[g])));}std::vector<std::uint8_t> seen(el.size());std::queue<std::uint16_t>q;seen[id]=1;q.push(id);std::size_t generated=1;while(!q.empty()){auto x=q.front();q.pop();for(int g=0;g<8;++g){auto y=tr[g][x];if(!seen[y]){seen[y]=1;++generated;q.push(y);}}}if(generated!=15600)throw std::runtime_error("generation");
    std::vector<std::uint16_t> state(tree.size());state[0]=id;std::uint32_t w=0;for(std::uint32_t x=1;x<tree.size();++x){auto e=tree[x];state[x]=tr[e.generator][state[e.parent]];if(!(e.depth&1)&&state[x]==id){w=x;break;}}if(!w){std::cout<<"candidate="<<k<<" BASED_PASS\n";continue;}std::vector<unsigned>word;for(auto x=w;x;x=tree[x].parent)word.push_back(tree[x].generator);std::reverse(word.begin(),word.end());std::cout<<"candidate="<<k<<" witness_id="<<w<<" depth="<<unsigned(tree[w].depth)<<" word=";for(std::size_t i=0;i<word.size();++i)std::cout<<(i?" ":"")<<'g'<<word[i];std::cout<<'\n';}
  return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
