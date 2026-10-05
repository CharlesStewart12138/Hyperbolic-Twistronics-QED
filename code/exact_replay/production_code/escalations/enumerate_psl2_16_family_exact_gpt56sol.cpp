#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

// Exhaustive PSL(2,16) x C2 direct-orbit family enumerator.
// F16=F2[t]/(t^4+t+1), encoded by four polynomial bits.  Quotient keys
// include the frozen external word-parity bit.
namespace {
using Mat=std::array<std::uint8_t,4>;
struct F16{std::array<std::array<std::uint8_t,16>,16>mul{};std::array<std::uint8_t,16>inv{};F16(){for(int x=0;x<16;++x)for(int y=0;y<16;++y){int a=x,b=y,r=0;while(b){if(b&1)r^=a;b>>=1;a<<=1;if(a&16)a^=0x13;}mul[x][y]=r;}for(int x=1;x<16;++x)for(int y=1;y<16;++y)if(mul[x][y]==1){inv[x]=y;break;}}Mat norm(Mat x)const{auto it=std::find_if(x.begin(),x.end(),[](auto z){return z;});if(it==x.end())throw std::runtime_error("zero matrix");auto s=inv[*it];for(auto&z:x)z=mul[z][s];return x;}std::uint8_t det(const Mat&x)const{return mul[x[0]][x[3]]^mul[x[1]][x[2]];}Mat product(const Mat&a,const Mat&b)const{return norm({std::uint8_t(mul[a[0]][b[0]]^mul[a[1]][b[2]]),std::uint8_t(mul[a[0]][b[1]]^mul[a[1]][b[3]]),std::uint8_t(mul[a[2]][b[0]]^mul[a[3]][b[2]]),std::uint8_t(mul[a[2]][b[1]]^mul[a[3]][b[3]])});}Mat inverse(const Mat&x)const{return norm({x[3],x[1],x[2],x[0]});}Mat frob(Mat x,int k)const{while(k--)for(auto&z:x)z=mul[z][z];return x;}};
std::uint32_t pack(const Mat&x){return x[0]|(std::uint32_t(x[1])<<4)|(std::uint32_t(x[2])<<8)|(std::uint32_t(x[3])<<12);}
struct Semi{Mat c;std::uint8_t k;};bool operator==(const Semi&a,const Semi&b){return a.k==b.k&&a.c==b.c;}Semi compose(const F16&f,const Semi&a,const Semi&b){return{f.product(a.c,f.frob(b.c,a.k)),std::uint8_t((a.k+b.k)&3)};}Mat act(const F16&f,const Semi&a,const Mat&x){return f.product(f.product(a.c,f.frob(x,a.k)),f.inverse(a.c));}unsigned order(const F16&f,const Semi&a){Semi p{{1,0,0,1},0};for(unsigned n=1;n<=64;++n){p=compose(f,a,p);if(p==Semi{{1,0,0,1},0})return n;}return 0;}
std::size_t b3(const F16&f,const std::array<Mat,8>&g){std::set<std::uint64_t>s;s.insert(std::uint64_t(pack(Mat{1,0,0,1}))<<1);for(int a=0;a<8;++a){s.insert((std::uint64_t(pack(g[a]))<<1)|1U);for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=f.product(g[a],g[b]);s.insert(std::uint64_t(pack(ab))<<1);for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert((std::uint64_t(pack(f.product(ab,g[c])))<<1)|1U);}}return s.size();}
std::size_t generated(const F16&f,const std::array<Mat,8>&g){std::unordered_set<std::uint32_t>s;std::queue<Mat>q;Mat id{1,0,0,1};s.insert(pack(id));q.push(id);while(!q.empty()){auto x=q.front();q.pop();for(auto&a:g){auto y=f.product(x,a);if(s.insert(pack(y)).second)q.push(y);}}return s.size();}
std::string show(const Mat&x){return"("+std::to_string(x[0])+","+std::to_string(x[1])+","+std::to_string(x[2])+","+std::to_string(x[3])+")";}
}
int main(){try{F16 f;Mat id{1,0,0,1};std::set<std::uint32_t>keys;std::vector<Mat>G;for(int a=0;a<16;++a)for(int b=0;b<16;++b)for(int c=0;c<16;++c)for(int d=0;d<16;++d){Mat x{(std::uint8_t)a,(std::uint8_t)b,(std::uint8_t)c,(std::uint8_t)d};if(f.det(x))keys.insert(pack(f.norm(x)));}for(auto k:keys)G.push_back(Mat{std::uint8_t(k&15),std::uint8_t((k>>4)&15),std::uint8_t((k>>8)&15),std::uint8_t((k>>12)&15)});if(G.size()!=4080)throw std::runtime_error("group order");const std::array<Semi,2>A{{{{0,1,1,2},1},{{0,1,1,2},3}}};std::uint64_t order8=0;for(int k=0;k<4;++k)for(auto c:G)order8+=(order(f,Semi{c,(std::uint8_t)k})==8);if(order8!=4080)throw std::runtime_error("order-eight automorphism count");std::uint64_t class_sum=0;
 for(int cls=0;cls<2;++cls){auto alpha=A[cls];std::vector<Semi>C;for(int k=0;k<4;++k)for(auto c:G){Semi z{c,(std::uint8_t)k};if(compose(f,alpha,z)==compose(f,z,alpha))C.push_back(z);}class_sum+=16320/C.size();std::uint64_t ni=0,nr=0,nd=0,nb=0,ng=0;std::vector<Mat>surv;for(auto x:G){std::array<Mat,8>g{};g[0]=x;for(int i=1;i<8;++i)g[i]=act(f,alpha,g[i-1]);bool ok=true;for(int i=0;i<4;++i)ok&=(g[i+4]==f.inverse(g[i]));if(!ok)continue;++ni;auto r=id;for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=f.product(r,g[i]);if(r!=id)continue;++nr;if(std::set<Mat>(g.begin(),g.end()).size()!=8)continue;++nd;if(b3(f,g)!=457)continue;++nb;if(generated(f,g)!=4080)continue;++ng;surv.push_back(x);}std::cout<<"CLASS "<<cls<<" alpha="<<show(alpha.c)<<","<<unsigned(alpha.k)<<" centralizer="<<C.size()<<" class_size="<<16320/C.size()<<" seeds=4080 inverse="<<ni<<" relator="<<nr<<" distinct="<<nd<<" b3="<<nb<<" generates="<<ng<<'\n';std::set<Mat>left(surv.begin(),surv.end());unsigned oi=0;while(!left.empty()){auto rep=*left.begin();std::set<Mat>orb;for(auto&z:C)orb.insert(act(f,z,rep));for(auto&y:orb)left.erase(y);std::cout<<"ORBIT "<<oi++<<" size="<<orb.size()<<" rep="<<show(rep)<<'\n';}for(auto&x:surv)std::cout<<"SURVIVOR "<<cls<<','<<unsigned(x[0])<<','<<unsigned(x[1])<<','<<unsigned(x[2])<<','<<unsigned(x[3])<<'\n';}
 if(class_sum!=order8)throw std::runtime_error("order-eight classes do not exhaust");std::cout<<"AUT order=16320 order8="<<order8<<" class_sum="<<class_sum<<'\n';return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
