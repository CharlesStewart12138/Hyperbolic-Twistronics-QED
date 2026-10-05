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

// Proof-complete direct-orbit search for generated pair quotients inside
// S_d x C2, d=9 or 10.  Every exact-order-eight conjugator cycle type is
// enumerated.  A quotient element is (permutation, frozen word parity), so
// an internal sign character is automatically collapsed when appropriate.
namespace {
constexpr int MAXD=10;
struct Perm{std::array<std::uint8_t,MAXD>x{};bool operator==(const Perm&)const=default;bool operator<(const Perm&o)const{return x<o.x;}};
int degree=0;
Perm one(){Perm r;for(int i=0;i<degree;++i)r.x[i]=i;return r;}
Perm product(const Perm&a,const Perm&b){Perm r;for(int i=0;i<degree;++i)r.x[i]=a.x[b.x[i]];return r;}
Perm inverse(const Perm&a){Perm r;for(int i=0;i<degree;++i)r.x[a.x[i]]=i;return r;}
Perm action(const Perm&t,const Perm&x){return product(product(t,x),inverse(t));}
std::uint32_t rank_perm(const Perm&p){std::uint32_t r=0;for(int i=0;i<degree;++i){int less=0;for(int j=i+1;j<degree;++j)less+=p.x[j]<p.x[i];r=r*(degree-i)+less;}return r;}
std::uint64_t pair_key(const Perm&p,unsigned parity){return (std::uint64_t(rank_perm(p))<<1)|(parity&1U);}
std::size_t b3_size(const std::array<Perm,8>&im){std::unordered_set<std::uint64_t>s;s.reserve(1024);s.insert(pair_key(one(),0));for(int a=0;a<8;++a){s.insert(pair_key(im[a],1));for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=product(im[a],im[b]);s.insert(pair_key(ab,0));for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert(pair_key(product(ab,im[c]),1));}}return s.size();}
std::size_t generated_pair_order(const std::array<Perm,8>&im,std::size_t stop){struct E{Perm p;std::uint8_t parity;};std::unordered_set<std::uint64_t>s;s.reserve(stop*2+1);std::queue<E>q;auto id=one();s.insert(pair_key(id,0));q.push({id,0});while(!q.empty()){auto e=q.front();q.pop();for(auto&g:im){E y{product(e.p,g),std::uint8_t(e.parity^1)};if(s.insert(pair_key(y.p,y.parity)).second){if(s.size()>stop)return s.size();q.push(y);}}}return s.size();}
std::string show(const Perm&p){std::string s="(";for(int i=0;i<degree;++i){if(i)s+=',';s+=std::to_string(unsigned(p.x[i]));}return s+")";}
Perm cycle_type_tau(int kind){auto t=one();for(int i=0;i<7;++i)t.x[i]=i+1;t.x[7]=0;if(degree==10&&kind==1)std::swap(t.x[8],t.x[9]);return t;}
}
int main(int argc,char**argv){try{if(argc!=2)throw std::runtime_error("usage: enumerate_inner_c8_permutation_degree9_10_gpt56sol DEGREE");degree=std::stoi(argv[1]);if(degree!=9&&degree!=10)throw std::runtime_error("degree must be 9 or 10");int types=degree==9?1:2;for(int typ=0;typ<types;++typ){auto tau=cycle_type_tau(typ);std::array<std::uint64_t,8>hist{};std::uint64_t seeds=0,inv=0,rel=0,distinct=0,b3=0,window=0,over=0;std::vector<std::pair<Perm,std::size_t>>survivors;Perm seed=one();do{++seeds;std::array<Perm,8>im{};im[0]=seed;for(int i=1;i<8;++i)im[i]=action(tau,im[i-1]);if(!(im[4]==inverse(im[0])))continue;++inv;auto r=one();for(int i:std::array<int,8>{0,5,2,7,4,1,6,3})r=product(r,im[i]);if(!(r==one()))continue;++rel;if(std::set<Perm>(im.begin(),im.end()).size()!=8)continue;++distinct;auto bs=b3_size(im);if(bs!=457){++hist[bs&7U];continue;}++b3;auto n=generated_pair_order(im,50000);if(n>50000){++over;continue;}if(n>=2338){++window;survivors.push_back({seed,n});}
    }while(std::next_permutation(seed.x.begin(),seed.x.begin()+degree));std::cout<<"degree="<<degree<<" tau_type="<<(typ==0?"8+fixed":"8+2")<<" seeds="<<seeds<<" inverse="<<inv<<" relator="<<rel<<" distinct="<<distinct<<" b3="<<b3<<" over50000="<<over<<" window="<<window<<'\n';for(auto&[s,n]:survivors)std::cout<<"SURVIVOR order="<<n<<" seed="<<show(s)<<'\n';}
  return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
