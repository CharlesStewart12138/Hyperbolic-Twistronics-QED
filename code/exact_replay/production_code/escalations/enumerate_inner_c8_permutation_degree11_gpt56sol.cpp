#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>

// Exhaustive degree-11 extension of the direct inner-C8 permutation search.
// The three conjugator cycle types containing an 8-cycle are 8+1+1+1,
// 8+2+1, and 8+3.  In the last case the ambient conjugator has order 24,
// so alpha^8(seed)=seed is tested explicitly.  Quotient states are the
// actual generated pairs (permutation,frozen parity), never the ambient S11.
namespace{
constexpr int D=11;
struct P{std::array<std::uint8_t,D>x{};bool operator==(const P&)const=default;bool operator<(const P&o)const{return x<o.x;}};
P id(){P r;for(int i=0;i<D;++i)r.x[i]=i;return r;}
P product(const P&a,const P&b){P r;for(int i=0;i<D;++i)r.x[i]=a.x[b.x[i]];return r;}
P inverse(const P&a){P r;for(int i=0;i<D;++i)r.x[a.x[i]]=i;return r;}
P conjugate(const P&t,const P&ti,const P&a){P r;for(int i=0;i<D;++i)r.x[i]=t.x[a.x[ti.x[i]]];return r;}
std::uint32_t rank(const P&p){std::uint32_t r=0;for(int i=0;i<D;++i){unsigned less=0;for(int j=i+1;j<D;++j)less+=p.x[j]<p.x[i];r=r*(D-i)+less;}return r;}
std::uint64_t key(const P&p,unsigned parity){return(std::uint64_t(rank(p))<<1)|(parity&1U);}
std::size_t b3(const std::array<P,8>&g){std::unordered_set<std::uint64_t>s;s.reserve(1024);s.insert(key(id(),0));for(int a=0;a<8;++a){s.insert(key(g[a],1));for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=product(g[a],g[b]);s.insert(key(ab,0));for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert(key(product(ab,g[c]),1));}}return s.size();}
std::size_t generated(const std::array<P,8>&g){struct E{P p;std::uint8_t z;};std::unordered_set<std::uint64_t>s;s.reserve(100003);std::queue<E>q;s.insert(key(id(),0));q.push({id(),0});while(!q.empty()){auto a=q.front();q.pop();for(auto&x:g){E y{product(a.p,x),std::uint8_t(a.z^1)};if(s.insert(key(y.p,y.z)).second){if(s.size()>50000)return s.size();q.push(y);}}}return s.size();}
P tau(int type){auto r=id();for(int i=0;i<7;++i)r.x[i]=i+1;r.x[7]=0;if(type==1)std::swap(r.x[8],r.x[9]);if(type==2){r.x[8]=9;r.x[9]=10;r.x[10]=8;}return r;}
}
int main(){try{for(int type=0;type<3;++type){auto t=tau(type),ti=inverse(t);std::uint64_t all=0,a8=0,inv=0,rel=0,distinct=0,b3n=0,over=0,window=0;P seed=id();do{++all;std::array<P,8>g{};g[0]=seed;for(int i=1;i<8;++i)g[i]=conjugate(t,ti,g[i-1]);if(!(conjugate(t,ti,g[7])==g[0]))continue;++a8;if(!(g[4]==inverse(g[0])))continue;++inv;auto r=id();for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=product(r,g[i]);if(!(r==id()))continue;++rel;if(std::set<P>(g.begin(),g.end()).size()!=8)continue;++distinct;if(b3(g)!=457)continue;++b3n;auto n=generated(g);if(n>50000){++over;continue;}if(n>=2338){++window;std::cout<<"SURVIVOR type="<<type<<" order="<<n<<" seed_rank="<<rank(seed)<<'\n';}}while(std::next_permutation(seed.x.begin(),seed.x.end()));const char*name=type==0?"8+1+1+1":type==1?"8+2+1":"8+3";std::cout<<"type="<<name<<" seeds="<<all<<" alpha8="<<a8<<" inverse="<<inv<<" relator="<<rel<<" distinct="<<distinct<<" b3="<<b3n<<" over50000="<<over<<" window="<<window<<'\n';}return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
