#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

namespace {
std::uint64_t factorial(unsigned n){std::uint64_t r=1;for(unsigned i=2;i<=n;++i)r*=i;return r;}
std::uint64_t ipow(std::uint64_t a,unsigned n){std::uint64_t r=1;while(n--!=0)r*=a;return r;}

// Number of square roots contributed by m cycles of a fixed length ell.
// An odd cycle may be rooted singly (uniquely); a paired pair of ell-cycles
// has exactly ell interlaced 2ell-cycle roots.  Even cycles must all be paired.
std::uint64_t root_factor(unsigned ell,unsigned m){
  std::uint64_t answer=0;
  unsigned first=(ell%2==0)?m/2:0, last=m/2;
  if(ell%2==0&&m%2!=0)return 0;
  for(unsigned pairs=first;pairs<=last;++pairs){
    if(ell%2==0&&2*pairs!=m)continue;
    auto ways=factorial(m)/(factorial(m-2*pairs)*ipow(2,pairs)*factorial(pairs));
    answer+=ways*ipow(ell,pairs);
  }
  return answer;
}
std::uint64_t roots_of_tau8(const std::vector<unsigned>&tau_cycles){
  std::vector<unsigned> mult(17);
  for(unsigned len:tau_cycles){unsigned d=std::gcd(len,8U);mult[len/d]+=d;}
  std::uint64_t r=1;for(unsigned ell=1;ell<=16;++ell)if(mult[ell])r*=root_factor(ell,mult[ell]);return r;
}
std::uint64_t centralizer(const std::vector<unsigned>&tau_cycles){
  std::vector<unsigned> mult(17);for(auto len:tau_cycles)++mult[len];
  std::uint64_t r=1;for(unsigned len=1;len<=16;++len)if(mult[len])r*=ipow(len,mult[len])*factorial(mult[len]);return r;
}
std::string name(const std::vector<unsigned>&parts){
  std::ostringstream out;out<<8;
  for(std::size_t i=0;i<parts.size();){std::size_t j=i+1;while(j<parts.size()&&parts[j]==parts[i])++j;out<<'+'<<parts[i];if(j-i>1)out<<'^'<<(j-i);i=j;}
  return out.str();
}
void partitions(unsigned remaining,unsigned maximum,std::vector<unsigned>&now,std::vector<std::vector<unsigned>>&out){
  if(!remaining){out.push_back(now);return;}
  for(unsigned x=std::min(remaining,maximum);x>=1;--x){now.push_back(x);partitions(remaining-x,x,now,out);now.pop_back();if(x==1)break;}
}
}
int main(){
  std::vector<std::vector<unsigned>> ps;std::vector<unsigned> now;partitions(8,8,now,ps);
  std::uint64_t total=0;std::cout<<"type\ttau8_cycle_type\tsquare_roots\tcentralizer\n";
  for(const auto&p:ps){std::vector<unsigned>tau{8};tau.insert(tau.end(),p.begin(),p.end());std::vector<unsigned>m(17);for(auto len:tau){auto d=std::gcd(len,8U);m[len/d]+=d;}std::ostringstream ct;bool first=true;for(int len=16;len>=1;--len)if(m[len]){if(!first)ct<<'+';ct<<len;if(m[len]>1)ct<<'^'<<m[len];first=false;}auto roots=roots_of_tau8(tau);total+=roots;std::cout<<name(p)<<'\t'<<ct.str()<<'\t'<<roots<<'\t'<<centralizer(tau)<<'\n';}
  std::vector<unsigned>tau16{16};auto roots16=roots_of_tau8(tau16);total+=roots16;
  std::cout<<"16\t2^8\t"<<roots16<<'\t'<<centralizer(tau16)<<'\n';
  std::cout<<"TOTAL_TYPES="<<(ps.size()+1)<<" TOTAL_ROOTS="<<total<<'\n';
}
