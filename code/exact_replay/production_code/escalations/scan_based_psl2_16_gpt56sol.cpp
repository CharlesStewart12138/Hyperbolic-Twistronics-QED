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
#include <vector>
namespace {
struct Meta{std::uint32_t parent;std::uint8_t generator,depth;std::uint16_t reserved;};static_assert(sizeof(Meta)==8);
using Mat=std::array<std::uint8_t,4>;
struct F16{std::array<std::array<std::uint8_t,16>,16>m{};std::array<std::uint8_t,16>iv{};F16(){for(int x=0;x<16;++x)for(int y=0;y<16;++y){int a=x,b=y,r=0;while(b){if(b&1)r^=a;b>>=1;a<<=1;if(a&16)a^=0x13;}m[x][y]=r;}for(int x=1;x<16;++x)for(int y=1;y<16;++y)if(m[x][y]==1){iv[x]=y;break;}}
 Mat norm(Mat x)const{auto p=*std::find_if(x.begin(),x.end(),[](auto z){return z;});auto s=iv[p];for(auto&z:x)z=m[z][s];return x;}std::uint8_t det(const Mat&x)const{return m[x[0]][x[3]]^m[x[1]][x[2]];}Mat mul(const Mat&x,const Mat&y)const{return norm({std::uint8_t(m[x[0]][y[0]]^m[x[1]][y[2]]),std::uint8_t(m[x[0]][y[1]]^m[x[1]][y[3]]),std::uint8_t(m[x[2]][y[0]]^m[x[3]][y[2]]),std::uint8_t(m[x[2]][y[1]]^m[x[3]][y[3]])});}Mat inverse(const Mat&x)const{return norm({x[3],x[1],x[2],x[0]});}Mat frob(Mat x,int k)const{while(k--)for(auto&z:x)z=m[z][z];return x;}Mat act(const Mat&c,int k,const Mat&x)const{return mul(mul(c,frob(x,k)),inverse(c));}};
std::uint32_t pack(const Mat&x){return x[0]|(std::uint32_t(x[1])<<4)|(std::uint32_t(x[2])<<8)|(std::uint32_t(x[3])<<12);}std::vector<Meta>load(const char*p){std::ifstream in(p,std::ios::binary);char mg[8]{};std::uint64_t n=0;std::uint32_t z=0;in.read(mg,8);in.read((char*)&n,8);in.read((char*)&z,4);if(!in||std::string(mg,8)!="BOLZAT01"||n!=23129593||z!=8)throw std::runtime_error("tree contract");std::vector<Meta>v(n);in.read((char*)v.data(),n*8);if(!in)throw std::runtime_error("short tree");return v;}
}
int main(int ac,char**av){try{if(ac!=2)throw std::runtime_error("usage TREE");F16 f;const Mat one{1,0,0,1},c{0,1,1,2};const std::array<std::pair<int,Mat>,8>cases{{{1,{0,1,1,8}},{1,{1,1,7,14}},{1,{1,2,9,13}},{1,{1,3,12,14}},{3,{0,1,1,12}},{3,{1,1,6,9}},{3,{1,1,9,10}},{3,{1,2,7,11}}}};
 std::set<std::uint32_t>keys;for(int a=0;a<16;++a)for(int b=0;b<16;++b)for(int cc=0;cc<16;++cc)for(int d=0;d<16;++d){Mat x{(std::uint8_t)a,(std::uint8_t)b,(std::uint8_t)cc,(std::uint8_t)d};if(f.det(x))keys.insert(pack(f.norm(x)));}if(keys.size()!=4080)throw std::runtime_error("order");std::vector<Mat>el;std::unordered_map<std::uint32_t,std::uint16_t>idx;for(auto k:keys){Mat x{std::uint8_t(k&15),std::uint8_t((k>>4)&15),std::uint8_t((k>>8)&15),std::uint8_t((k>>12)&15)};idx[k]=el.size();el.push_back(x);}auto id=idx.at(pack(one));auto tree=load(av[1]);
 for(std::size_t q=0;q<cases.size();++q){auto [fk,seed]=cases[q];std::array<Mat,8>im{};im[0]=seed;for(int i=1;i<8;++i)im[i]=f.act(c,fk,im[i-1]);for(int i=0;i<4;++i)if(im[i+4]!=f.inverse(im[i]))throw std::runtime_error("inverse");Mat r=one;for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=f.mul(r,im[i]);if(r!=one)throw std::runtime_error("rel");std::array<std::vector<std::uint16_t>,8>tr;for(int g=0;g<8;++g){tr[g].resize(el.size());for(std::size_t x=0;x<el.size();++x)tr[g][x]=idx.at(pack(f.mul(el[x],im[g])));}std::vector<std::uint8_t>seen(el.size());std::queue<std::uint16_t>qq;seen[id]=1;qq.push(id);std::size_t n=1;while(!qq.empty()){auto x=qq.front();qq.pop();for(int g=0;g<8;++g){auto y=tr[g][x];if(!seen[y]){seen[y]=1;++n;qq.push(y);}}}if(n!=4080)throw std::runtime_error("generate");std::vector<std::uint16_t>st(tree.size());st[0]=id;std::uint32_t w=0;for(std::uint32_t x=1;x<tree.size();++x){auto e=tree[x];st[x]=tr[e.generator][st[e.parent]];if(!(e.depth&1)&&st[x]==id){w=x;break;}}if(!w){std::cout<<"candidate="<<q<<" BASED_PASS\n";continue;}std::vector<unsigned>word;for(auto x=w;x;x=tree[x].parent)word.push_back(tree[x].generator);std::reverse(word.begin(),word.end());std::cout<<"candidate="<<q<<" witness_id="<<w<<" depth="<<unsigned(tree[w].depth)<<" word=";for(std::size_t i=0;i<word.size();++i)std::cout<<(i?" ":"")<<'g'<<word[i];std::cout<<'\n';}
 return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
