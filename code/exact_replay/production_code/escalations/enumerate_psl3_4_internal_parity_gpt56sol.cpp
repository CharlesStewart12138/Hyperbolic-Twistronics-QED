#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

// Exhaustive internal-parity scans in PSL(3,4):2 for the field, graph,
// and field-graph outer involutions.  F4=F2[t]/(t^2+t+1), encoded by
// polynomial bits.  Matrices are row-major and canonical modulo the scalar
// centre {I,tI,(t+1)I}.  An extension element is (matrix,coset_bit).
namespace {
using Mat=std::array<std::uint8_t,9>;
struct Elt { Mat a; std::uint8_t e; };
bool operator==(const Elt&x,const Elt&y){return x.e==y.e&&x.a==y.a;}
bool operator<(const Elt&x,const Elt&y){return x.a<y.a||(x.a==y.a&&x.e<y.e);}

struct F4 {
 std::array<std::array<std::uint8_t,4>,4> m{};
 std::array<std::uint8_t,4> iv{};
 F4(){
  for(int x=0;x<4;++x)for(int y=0;y<4;++y){
   int a=x,b=y,r=0;
   while(b){if(b&1)r^=a;b>>=1;a<<=1;if(a&4)a^=7;}
   m[x][y]=std::uint8_t(r);
  }
  for(int x=1;x<4;++x)for(int y=1;y<4;++y)if(m[x][y]==1){iv[x]=std::uint8_t(y);break;}
 }
 std::uint8_t mul(std::uint8_t x,std::uint8_t y)const{return m[x][y];}
 Mat scalar(std::uint8_t s,Mat x)const{for(auto&z:x)z=mul(s,z);return x;}
 Mat canon(Mat x)const{return std::min(x,std::min(scalar(2,x),scalar(3,x)));}
 std::uint8_t det(const Mat&x)const{
  auto p=[&](int i,int j,int k){return mul(x[i],mul(x[j],x[k]));};
  return p(0,4,8)^p(0,5,7)^p(1,3,8)^p(1,5,6)^p(2,3,7)^p(2,4,6);
 }
 Mat product(const Mat&x,const Mat&y)const{
  Mat z{};
  for(int r=0;r<3;++r)for(int c=0;c<3;++c)
   z[3*r+c]=mul(x[3*r],y[c])^mul(x[3*r+1],y[3+c])^mul(x[3*r+2],y[6+c]);
  return canon(z);
 }
 Mat inverse(const Mat&x)const{
  Mat c{
   std::uint8_t(mul(x[4],x[8])^mul(x[5],x[7])),std::uint8_t(mul(x[3],x[8])^mul(x[5],x[6])),std::uint8_t(mul(x[3],x[7])^mul(x[4],x[6])),
   std::uint8_t(mul(x[1],x[8])^mul(x[2],x[7])),std::uint8_t(mul(x[0],x[8])^mul(x[2],x[6])),std::uint8_t(mul(x[0],x[7])^mul(x[1],x[6])),
   std::uint8_t(mul(x[1],x[5])^mul(x[2],x[4])),std::uint8_t(mul(x[0],x[5])^mul(x[2],x[3])),std::uint8_t(mul(x[0],x[4])^mul(x[1],x[3]))};
  Mat adj{};for(int r=0;r<3;++r)for(int col=0;col<3;++col)adj[3*r+col]=c[3*col+r];
  auto d=det(x);if(!d)throw std::runtime_error("singular inverse");return canon(scalar(iv[d],adj));
 }
 Mat field(Mat x)const{for(auto&z:x)z=mul(z,z);return canon(x);}
 Mat graph(const Mat&x)const{auto y=inverse(x);Mat z{};for(int r=0;r<3;++r)for(int c=0;c<3;++c)z[3*r+c]=y[3*c+r];return canon(z);}
};

std::uint32_t pack(const Mat&x){std::uint32_t k=0;for(int i=0;i<9;++i)k|=std::uint32_t(x[i])<<(2*i);return k;}
std::string show(const Mat&x){std::string s="(";for(int i=0;i<9;++i){if(i)s+=",";s+=std::to_string(unsigned(x[i]));}return s+")";}

struct Extension {
 const F4& f; int kind; // 0=field, 1=graph, 2=field-graph
 Mat psi(Mat x)const{if(kind==1)return f.graph(x);if(kind==0)return f.field(x);return f.field(f.graph(x));}
 Elt product(const Elt&x,const Elt&y)const{return{f.product(x.a,x.e?psi(y.a):y.a),std::uint8_t(x.e^y.e)};}
 Elt inverse(const Elt&x)const{return{x.e?psi(f.inverse(x.a)):f.inverse(x.a),x.e};}
 Elt power(Elt x,unsigned n)const{Elt r{{1,0,0,0,1,0,0,0,1},0};while(n){if(n&1)r=product(r,x);x=product(x,x);n>>=1;}return r;}
 Elt conjugate(const Elt&g,const Elt&x)const{return product(g,product(x,inverse(g)));}
};

std::uint32_t ekey(const Elt&x){return (pack(x.a)<<1)|x.e;}
unsigned order(const Extension&e,const Elt&x){Elt p{{1,0,0,0,1,0,0,0,1},0};for(unsigned n=1;n<=64;++n){p=e.product(p,x);if(p==Elt{{1,0,0,0,1,0,0,0,1},0})return n;}return 0;}

std::size_t b3(const Extension&e,const std::array<Elt,8>&g){
 std::unordered_set<std::uint32_t>s;s.reserve(600);Elt id{{1,0,0,0,1,0,0,0,1},0};s.insert(ekey(id));
 for(int a=0;a<8;++a){s.insert(ekey(g[a]));for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=e.product(g[a],g[b]);s.insert(ekey(ab));for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert(ekey(e.product(ab,g[c])));}}
 return s.size();
}

std::size_t generated(const Extension&e,const std::array<Elt,8>&g){
 std::unordered_set<std::uint32_t>s;s.reserve(45000);std::queue<Elt>q;Elt id{{1,0,0,0,1,0,0,0,1},0};s.insert(ekey(id));q.push(id);
 while(!q.empty()){auto x=q.front();q.pop();for(auto&a:g){auto y=e.product(x,a);if(s.insert(ekey(y)).second)q.push(y);}}return s.size();
}

struct Counts{std::uint64_t inverse=0,relator=0,distinct=0,b3pass=0,generates=0;};
void scan(const F4&f,const std::vector<Mat>&G,int kind){
 Extension e{f,kind};const char*name=kind==0?"field":kind==1?"graph":"fieldgraph";Elt id{{1,0,0,0,1,0,0,0,1},0};
 std::vector<Elt>H;H.reserve(40320);for(auto&a:G){H.push_back({a,0});H.push_back({a,1});}
 std::unordered_map<std::uint32_t,std::size_t>idx;idx.reserve(H.size()*2);for(std::size_t i=0;i<H.size();++i)idx.emplace(ekey(H[i]),i);
 std::vector<std::size_t>o8;for(std::size_t i=0;i<H.size();++i)if(order(e,H[i])==8)o8.push_back(i);
 std::unordered_set<std::uint32_t>remaining;remaining.reserve(o8.size()*2);for(auto i:o8)remaining.insert(ekey(H[i]));
 struct Class { Elt rep; std::size_t size,centralizer; };std::vector<Class>classes;
 while(!remaining.empty()){
  auto key=*std::min_element(remaining.begin(),remaining.end());auto rep=H[idx.at(key)];std::unordered_set<std::uint32_t>orb;orb.reserve(H.size());
  std::size_t cent=0;for(auto&z:H){if(e.product(z,rep)==e.product(rep,z))++cent;orb.insert(ekey(e.conjugate(z,rep)));}
  if(orb.size()*cent!=H.size())throw std::runtime_error("class-centralizer identity");
  for(auto k:orb)remaining.erase(k);classes.push_back({rep,orb.size(),cent});
 }
 std::sort(classes.begin(),classes.end(),[](const Class&a,const Class&b){return a.rep<b.rep;});
 std::uint64_t classsum=0;for(auto&c:classes)classsum+=c.size;if(classsum!=o8.size())throw std::runtime_error("class exhaustion");
 std::cout<<"TARGET "<<name<<" order=40320 order8="<<o8.size()<<" classes="<<classes.size()<<" class_sum="<<classsum<<'\n';
 for(std::size_t ci=0;ci<classes.size();++ci){
  auto alpha=classes[ci].rep;Counts c;std::vector<Mat>survivors;std::map<std::size_t,std::uint64_t>histogram;
  for(auto&base:G){
   std::array<Elt,8>g{};g[0]={base,1};for(int i=1;i<8;++i)g[i]=e.conjugate(alpha,g[i-1]);
   bool inv=true;for(int i=0;i<4;++i)inv&=(g[i+4]==e.inverse(g[i]));if(!inv)continue;++c.inverse;
   auto r=id;for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=e.product(r,g[i]);if(!(r==id))continue;++c.relator;
   std::set<Elt>distinct(g.begin(),g.end());if(distinct.size()!=8)continue;++c.distinct;
   const auto b3_size=b3(e,g);++histogram[b3_size];const bool b3_pass=b3_size==457;if(b3_pass)++c.b3pass;
   const bool generation_pass=generated(e,g)==40320;if(generation_pass)++c.generates;
   if(b3_pass&&generation_pass)survivors.push_back(base);
  }
  std::cout<<"CLASS target="<<name<<" index="<<ci<<" alpha="<<show(alpha.a)<<","<<unsigned(alpha.e)<<" class_size="<<classes[ci].size<<" centralizer="<<classes[ci].centralizer<<" seeds=20160 inverse="<<c.inverse<<" relator="<<c.relator<<" distinct="<<c.distinct<<" b3="<<c.b3pass<<" generates="<<c.generates<<'\n';
  for(auto [size,count]:histogram)std::cout<<"B3HIST target="<<name<<" class="<<ci<<" size="<<size<<" count="<<count<<'\n';
  for(auto&s:survivors)std::cout<<"SURVIVOR target="<<name<<" class="<<ci<<" seed="<<show(s)<<",1\n";
 }
}
}

int main(){try{
 F4 f;std::set<Mat>unique;
 for(std::uint32_t k=0;k<(1u<<18);++k){Mat x{};for(int i=0;i<9;++i)x[i]=std::uint8_t((k>>(2*i))&3);if(f.det(x)==1)unique.insert(f.canon(x));}
 std::vector<Mat>G(unique.begin(),unique.end());if(G.size()!=20160)throw std::runtime_error("PSL(3,4) order");
 for(int kind=0;kind<3;++kind)scan(f,G,kind);
 return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
