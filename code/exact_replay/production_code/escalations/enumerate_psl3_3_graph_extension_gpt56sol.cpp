#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <unordered_set>
#include <vector>

// Exact direct-orbit search in the internal-parity almost-simple target
// PSL(3,3):2_graph = SL(3,3) semidirect <gamma>, gamma(A)=(A^-1)^T.
// PSL(3,3) has trivial center.  Elements are (A,e), e is the frozen parity.
namespace{
using M=std::array<std::uint8_t,9>;
struct E{M a;std::uint8_t e;bool operator==(const E&)const=default;bool operator<(const E&o)const{return e<o.e||(e==o.e&&a<o.a);}};
int mod3(int x){x%=3;return x<0?x+3:x;}
M idm(){return M{1,0,0,0,1,0,0,0,1};}
int det(const M&a){return mod3(a[0]*(a[4]*a[8]-a[5]*a[7])-a[1]*(a[3]*a[8]-a[5]*a[6])+a[2]*(a[3]*a[7]-a[4]*a[6]));}
M mul(const M&a,const M&b){M r{};for(int i=0;i<3;++i)for(int j=0;j<3;++j){int s=0;for(int k=0;k<3;++k)s+=a[3*i+k]*b[3*k+j];r[3*i+j]=mod3(s);}return r;}
M inv(const M&a){int d=det(a);if(!d)throw std::runtime_error("singular");int z=d==1?1:2;M r{(std::uint8_t)mod3(z*(a[4]*a[8]-a[5]*a[7])),(std::uint8_t)mod3(z*(a[2]*a[7]-a[1]*a[8])),(std::uint8_t)mod3(z*(a[1]*a[5]-a[2]*a[4])),(std::uint8_t)mod3(z*(a[5]*a[6]-a[3]*a[8])),(std::uint8_t)mod3(z*(a[0]*a[8]-a[2]*a[6])),(std::uint8_t)mod3(z*(a[2]*a[3]-a[0]*a[5])),(std::uint8_t)mod3(z*(a[3]*a[7]-a[4]*a[6])),(std::uint8_t)mod3(z*(a[1]*a[6]-a[0]*a[7])),(std::uint8_t)mod3(z*(a[0]*a[4]-a[1]*a[3]))};return r;}
M graph(const M&a){auto b=inv(a);return M{b[0],b[3],b[6],b[1],b[4],b[7],b[2],b[5],b[8]};}
E product(const E&x,const E&y){return E{mul(x.a,x.e?graph(y.a):y.a),std::uint8_t(x.e^y.e)};}
E inverse(const E&x){auto z=inv(x.a);return E{x.e?graph(z):z,x.e};}
E conjugate(const E&h,const E&x){return product(product(h,x),inverse(h));}
std::uint32_t mcode(const M&a){std::uint32_t r=0,p=1;for(auto x:a){r+=p*x;p*=3;}return r;}
std::uint32_t code(const E&x){return mcode(x.a)|(std::uint32_t(x.e)<<15);}
unsigned order(const E&x){E p{idm(),0};for(unsigned n=1;n<=128;++n){p=product(p,x);if(p==E{idm(),0})return n;}return 0;}
std::size_t b3(const std::array<E,8>&g){std::unordered_set<std::uint32_t>s;s.reserve(1024);s.insert(code(E{idm(),0}));for(int a=0;a<8;++a){s.insert(code(g[a]));for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=product(g[a],g[b]);s.insert(code(ab));for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert(code(product(ab,g[c])));}}return s.size();}
std::size_t generated(const std::array<E,8>&g){std::unordered_set<std::uint32_t>s;std::queue<E>q;E one{idm(),0};s.insert(code(one));q.push(one);while(!q.empty()){auto x=q.front();q.pop();for(auto&a:g){auto y=product(x,a);if(s.insert(code(y)).second)q.push(y);}}return s.size();}
}
int main(){try{std::vector<M>S;for(std::uint32_t c=0;c<19683;++c){auto z=c;M a{};for(auto&x:a){x=z%3;z/=3;}if(det(a)==1)S.push_back(a);}if(S.size()!=5616)throw std::runtime_error("SL3(3) order");std::vector<E>H;H.reserve(11232);for(int e=0;e<2;++e)for(auto&a:S)H.push_back(E{a,(std::uint8_t)e});std::vector<E>o8;for(auto&x:H)if(order(x)==8)o8.push_back(x);std::set<std::uint32_t>left;for(auto&x:o8)left.insert(code(x));std::vector<E>reps;std::vector<std::size_t>sizes;while(!left.empty()){auto target=*left.begin();auto it=std::find_if(o8.begin(),o8.end(),[&](auto&x){return code(x)==target;});auto r=*it;std::set<std::uint32_t>orb;for(auto&h:H)orb.insert(code(conjugate(h,r)));for(auto k:orb)left.erase(k);reps.push_back(r);sizes.push_back(orb.size());}
 std::cout<<"TARGET order=11232 order8="<<o8.size()<<" classes="<<reps.size()<<'\n';std::uint64_t total_class=0;for(auto n:sizes)total_class+=n;if(total_class!=o8.size())throw std::runtime_error("class coverage");
 for(std::size_t cls=0;cls<reps.size();++cls){auto h=reps[cls];std::uint64_t ni=0,nd=0,nr=0,nb=0,ng=0;std::size_t best=0;for(auto&a:S){E x{a,1};std::array<E,8>g{};g[0]=x;for(int i=1;i<8;++i)g[i]=conjugate(h,g[i-1]);if(!(g[4]==inverse(g[0])))continue;++ni;if(std::set<E>(g.begin(),g.end()).size()!=8)continue;++nd;auto r=E{idm(),0};for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=product(r,g[i]);if(!(r==E{idm(),0}))continue;++nr;auto bs=b3(g);best=std::max(best,bs);if(bs!=457)continue;++nb;if(generated(g)!=11232)continue;++ng;std::cout<<"SURVIVOR class="<<cls<<" seed_code="<<code(x)<<'\n';}std::cout<<"CLASS "<<cls<<" size="<<sizes[cls]<<" rep_code="<<code(h)<<" inverse="<<ni<<" distinct="<<nd<<" relator="<<nr<<" b3="<<nb<<" generates="<<ng<<" best_b3="<<best<<'\n';}
 return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
