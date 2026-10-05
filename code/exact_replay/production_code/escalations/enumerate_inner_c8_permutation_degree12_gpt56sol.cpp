#include <algorithm>
#include <array>
#include <cstdint>
#include <functional>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <unordered_set>

// Proof-complete degree-12 direct inner-C8 permutation search.  For the
// four order-eight conjugator types, alpha^4(x)=x^-1 is parameterized
// bijectively by involutions y=x*tau^4 (only 140,152 cases per type).
// For 8+3+1, alpha^8(x)=x is parameterized by C_S12(tau^8)=C3 x S9.
namespace{
constexpr int D=12;struct P{std::array<std::uint8_t,D>x{};bool operator==(const P&)const=default;bool operator<(const P&o)const{return x<o.x;}};P id(){P r;for(int i=0;i<D;++i)r.x[i]=i;return r;}P product(const P&a,const P&b){P r;for(int i=0;i<D;++i)r.x[i]=a.x[b.x[i]];return r;}P inverse(const P&a){P r;for(int i=0;i<D;++i)r.x[a.x[i]]=i;return r;}P power(P a,unsigned n){P r=id();while(n){if(n&1)r=product(r,a);a=product(a,a);n>>=1;}return r;}P conjugate(const P&t,const P&ti,const P&a){P r;for(int i=0;i<D;++i)r.x[i]=t.x[a.x[ti.x[i]]];return r;}std::uint32_t rank(const P&p){std::uint32_t r=0;for(int i=0;i<D;++i){unsigned less=0;for(int j=i+1;j<D;++j)less+=p.x[j]<p.x[i];r=r*(D-i)+less;}return r;}std::uint64_t key(const P&p,unsigned z){return(std::uint64_t(rank(p))<<1)|(z&1U);}std::size_t b3(const std::array<P,8>&g){std::unordered_set<std::uint64_t>s;s.reserve(1024);s.insert(key(id(),0));for(int a=0;a<8;++a){s.insert(key(g[a],1));for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=product(g[a],g[b]);s.insert(key(ab,0));for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert(key(product(ab,g[c]),1));}}return s.size();}std::size_t generated(const std::array<P,8>&g){struct E{P p;std::uint8_t z;};std::unordered_set<std::uint64_t>s;s.reserve(100003);std::queue<E>q;s.insert(key(id(),0));q.push({id(),0});while(!q.empty()){auto a=q.front();q.pop();for(auto&x:g){E y{product(a.p,x),std::uint8_t(a.z^1)};if(s.insert(key(y.p,y.z)).second){if(s.size()>50000)return s.size();q.push(y);}}}return s.size();}P tau(int type){auto r=id();for(int i=0;i<7;++i)r.x[i]=i+1;r.x[7]=0;if(type==1)std::swap(r.x[8],r.x[9]);if(type==2){std::swap(r.x[8],r.x[9]);std::swap(r.x[10],r.x[11]);}if(type==3){r.x[8]=9;r.x[9]=10;r.x[10]=8;}if(type==4){r.x[8]=9;r.x[9]=10;r.x[10]=11;r.x[11]=8;}return r;}
struct Counts{std::uint64_t parameter=0,inv=0,rel=0,distinct=0,b3n=0,over=0,window=0;};
void test(const P&seed,const P&t,const P&ti,Counts&c){++c.parameter;std::array<P,8>g{};g[0]=seed;for(int i=1;i<8;++i)g[i]=conjugate(t,ti,g[i-1]);if(!(conjugate(t,ti,g[7])==g[0]))throw std::runtime_error("alpha8 parameterization");if(!(g[4]==inverse(g[0])))return;++c.inv;auto r=id();for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=product(r,g[i]);if(!(r==id()))return;++c.rel;if(std::set<P>(g.begin(),g.end()).size()!=8)return;++c.distinct;if(b3(g)!=457)return;++c.b3n;auto n=generated(g);if(n>50000){++c.over;return;}if(n>=2338){++c.window;std::cout<<"SURVIVOR order="<<n<<" seed_rank="<<rank(seed)<<'\n';}}
void involutions(const std::function<void(const P&)>&emit){P p=id();std::array<bool,D>used{};std::function<void()>rec=[&]{int i=0;while(i<D&&used[i])++i;if(i==D){emit(p);return;}used[i]=true;p.x[i]=i;rec();for(int j=i+1;j<D;++j)if(!used[j]){used[j]=true;p.x[i]=j;p.x[j]=i;rec();p.x[j]=j;used[j]=false;}p.x[i]=i;used[i]=false;};rec();}
}
int main(){try{const char*names[5]={"8+1+1+1+1","8+2+1+1","8+2+2","8+3+1","8+4"};for(int type=0;type<5;++type){auto t=tau(type),ti=inverse(t);Counts c;if(type!=3){auto t4=power(t,4);involutions([&](const P&y){test(product(y,t4),t,ti,c);});if(c.parameter!=140152||c.inv!=c.parameter)throw std::runtime_error("involution bijection");}else{std::array<std::uint8_t,9>dom{{0,1,2,3,4,5,6,7,11}},img=dom;do{for(int k=0;k<3;++k){P x=id();for(int i=0;i<9;++i)x.x[dom[i]]=img[i];for(int i=0;i<3;++i)x.x[8+i]=8+((i+k)%3);test(x,t,ti,c);}}while(std::next_permutation(img.begin(),img.end()));if(c.parameter!=1088640)throw std::runtime_error("C(tau8) count");}std::cout<<"type="<<names[type]<<" parameter_seeds="<<c.parameter<<" inverse="<<c.inv<<" relator="<<c.rel<<" distinct="<<c.distinct<<" b3="<<c.b3n<<" over50000="<<c.over<<" window="<<c.window<<'\n';}return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
