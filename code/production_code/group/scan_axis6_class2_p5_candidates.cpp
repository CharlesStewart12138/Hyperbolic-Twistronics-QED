#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>

#define CM_GEO7_NO_MAIN
#include "external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {
constexpr std::uint64_t kCommitRecords = 1'000'000;
constexpr std::uint32_t kExactCutoffMarker = std::numeric_limits<std::uint32_t>::max();
constexpr int kP = 5, kHalf = 3;
using Row = std::array<std::uint8_t, 6>;
struct Candidate { Row first, second; };
constexpr std::array<Candidate, 16> kCandidates{{
  {{{1,0,0,0,2,1}},{{0,1,3,3,0,0}}},
  {{{1,0,2,2,1,1}},{{0,1,2,2,3,0}}},
  {{{1,0,2,3,0,4}},{{0,1,0,0,4,0}}},
  {{{1,0,2,3,0,4}},{{0,1,1,3,4,1}}},
  {{{1,0,2,3,0,4}},{{0,1,2,1,4,2}}},
  {{{1,0,2,3,0,4}},{{0,1,2,4,1,1}}},
  {{{1,0,2,3,0,4}},{{0,1,3,4,4,3}}},
  {{{1,0,2,3,0,4}},{{0,1,4,2,4,4}}},
  {{{1,0,3,2,0,4}},{{0,1,0,0,4,0}}},
  {{{1,0,3,2,0,4}},{{0,1,1,2,4,2}}},
  {{{1,0,3,2,0,4}},{{0,1,2,4,4,4}}},
  {{{1,0,3,2,0,4}},{{0,1,3,1,4,1}}},
  {{{1,0,3,2,0,4}},{{0,1,4,2,1,1}}},
  {{{1,0,3,2,0,4}},{{0,1,4,3,4,3}}},
  {{{1,0,3,3,3,1}},{{0,1,4,4,2,0}}},
  {{{1,2,0,0,0,1}},{{0,0,1,1,2,0}}},
}};

struct State {
  std::uint64_t total = 0, scanned = 0, abelian_hits = 0;
  std::array<std::uint64_t, 16> kernel_hits{}, dangerous_hits{};
  std::array<std::uint64_t, 16> witness_index{};
  std::array<std::uint8_t, 16> witness_depth{};
  std::array<std::uint64_t, 16> witness_high{}, witness_low{};
  std::array<long double, 16> minimum_abs_trace_half{};
  double elapsed_seconds = 0.0;
  bool complete = false;
  State() { minimum_abs_trace_half.fill(std::numeric_limits<long double>::infinity()); }
};

std::uint8_t digit(std::uint64_t high, std::uint64_t low, unsigned depth, unsigned index) {
  const unsigned shift = 3U * (depth - 1U - index);
  return static_cast<std::uint8_t>(shift < 64 ? (low >> shift) & 7U : (high >> (shift - 64U)) & 7U);
}
int mod5(int value) { value %= 5; return value < 0 ? value + 5 : value; }

void wedge(const std::array<int,4>& a, const std::array<int,4>& b, std::array<int,6>& out) {
  constexpr std::array<std::array<int,2>,6> pairs{{{{0,1}},{{0,2}},{{0,3}},{{1,2}},{{1,3}},{{2,3}}}};
  for (std::size_t k=0;k<6;++k) out[k]=mod5(a[pairs[k][0]]*b[pairs[k][1]]-a[pairs[k][1]]*b[pairs[k][0]]);
}

void word_image(std::uint64_t high, std::uint64_t low, unsigned depth,
                std::array<int,4>& v, std::array<int,6>& c) {
  v.fill(0); c.fill(0);
  for (unsigned i=0;i<depth;++i) {
    const auto d=digit(high,low,depth,i);
    std::array<int,4> w{};
    w[d&3U] = d<4 ? 1 : 4;
    std::array<int,6> cross{}; wedge(v,w,cross);
    for (std::size_t k=0;k<6;++k) c[k]=mod5(c[k]+kHalf*cross[k]);
    for (std::size_t k=0;k<4;++k) v[k]=mod5(v[k]+w[k]);
  }
}

bool central_zero(const Candidate& candidate, const std::array<int,6>& c) {
  int a=0,b=0;
  for (std::size_t k=0;k<6;++k) { a+=candidate.first[k]*c[k]; b+=candidate.second[k]*c[k]; }
  return mod5(a)==0 && mod5(b)==0;
}

Field real_part(const Field& value) { Field r=value; for(std::size_t i=4;i<8;++i) r.c[i]=0; return r; }
bool dangerous_trace(const Matrix& matrix) {
  const Field re=real_part(matrix.a);
  const Field cosh_3a=field_from({2405,1700,0,0,0,0,0,0});
  return geo_exact_real_field_sign(add(multiply(re,re),negate(multiply(cosh_3a,cosh_3a))))<=0;
}
long double abs_trace_half(const Matrix& matrix) { return std::fabs(geo_field_value_real(matrix.a)); }

void write_state(const std::filesystem::path& path,const State& s) {
  const auto tmp=path.string()+".tmp"; std::ofstream out(tmp,std::ios::trunc);
  if(!out) throw std::runtime_error("cannot write checkpoint");
  out<<std::setprecision(25)<<"schema_version\t1.0\nalgorithm\tclass2_p5_c8_candidate_full_kernel_scan\n"
     <<"candidate_order\t31250\ntotal_records\t"<<s.total<<"\nscanned_records\t"<<s.scanned
     <<"\nabelian_parity_hits\t"<<s.abelian_hits<<'\n';
  for(std::size_t i=0;i<16;++i) out<<"candidate_"<<i<<"_kernel_hits\t"<<s.kernel_hits[i]<<'\n'
    <<"candidate_"<<i<<"_dangerous_hits\t"<<s.dangerous_hits[i]<<'\n'
    <<"candidate_"<<i<<"_witness_index\t"<<s.witness_index[i]<<'\n'
    <<"candidate_"<<i<<"_witness_depth\t"<<static_cast<unsigned>(s.witness_depth[i])<<'\n'
    <<"candidate_"<<i<<"_witness_high\t"<<s.witness_high[i]<<'\n'
    <<"candidate_"<<i<<"_witness_low\t"<<s.witness_low[i]<<'\n'
    <<"candidate_"<<i<<"_minimum_abs_trace_half\t"<<s.minimum_abs_trace_half[i]<<'\n';
  out<<"elapsed_seconds\t"<<std::setprecision(17)<<s.elapsed_seconds<<"\ncomplete\t"<<(s.complete?1:0)<<'\n';
  out.close(); if(!out) throw std::runtime_error("checkpoint flush failed");
  if(std::filesystem::exists(path)) std::filesystem::remove(path); std::filesystem::rename(tmp,path);
}

State read_state(const std::filesystem::path& path) {
  std::ifstream in(path); if(!in) throw std::runtime_error("cannot read checkpoint");
  std::map<std::string,std::string> m; std::string line;
  while(std::getline(in,line)){auto t=line.find('\t');if(t!=std::string::npos)m[line.substr(0,t)]=line.substr(t+1);}
  State s; s.total=std::stoull(m.at("total_records"));s.scanned=std::stoull(m.at("scanned_records"));s.abelian_hits=std::stoull(m.at("abelian_parity_hits"));
  for(std::size_t i=0;i<16;++i){const auto p="candidate_"+std::to_string(i)+"_";s.kernel_hits[i]=std::stoull(m.at(p+"kernel_hits"));s.dangerous_hits[i]=std::stoull(m.at(p+"dangerous_hits"));s.witness_index[i]=std::stoull(m.at(p+"witness_index"));s.witness_depth[i]=static_cast<std::uint8_t>(std::stoul(m.at(p+"witness_depth")));s.witness_high[i]=std::stoull(m.at(p+"witness_high"));s.witness_low[i]=std::stoull(m.at(p+"witness_low"));s.minimum_abs_trace_half[i]=std::stold(m.at(p+"minimum_abs_trace_half"));}
  s.elapsed_seconds=std::stod(m.at("elapsed_seconds"));s.complete=m.at("complete")=="1";return s;
}

void scan(const std::filesystem::path& registry,const std::filesystem::path& checkpoint) {
  std::ifstream input(registry,std::ios::binary);if(!input)throw std::runtime_error("cannot open registry");
  static std::array<char,16*1024*1024> buffer{};input.rdbuf()->pubsetbuf(buffer.data(),buffer.size());
  char magic[8]{};input.read(magic,8);if(std::string(magic,8)!="BOLZGEO1")throw std::runtime_error("bad magic");
  const auto total=read_u64(input);if(read_u32(input)!=kGeoRecordBytes||read_u32(input)!=kExactCutoffMarker)throw std::runtime_error("bad registry contract");
  State s;if(std::filesystem::exists(checkpoint)){s=read_state(checkpoint);if(s.total!=total)throw std::runtime_error("total drift");}else{s.total=total;write_state(checkpoint,s);}if(s.complete)return;
  input.seekg(static_cast<std::streamoff>(24ULL+s.scanned*kGeoRecordBytes));
  auto started=std::chrono::steady_clock::now();auto next=std::min(total,((s.scanned/kCommitRecords)+1)*kCommitRecords);
  std::array<char,kGeoRecordBytes> raw{};
  while(s.scanned<total){input.read(raw.data(),raw.size());if(!input)throw std::runtime_error("short record");const auto index=s.scanned++;
    const auto depth=static_cast<std::uint8_t>(raw[130]);if(depth!=0&&(depth&1U)==0U){std::uint64_t high=0,low=0;std::memcpy(&high,raw.data()+131,8);std::memcpy(&low,raw.data()+139,8);std::array<int,4> v{};std::array<int,6> c{};word_image(high,low,depth,v,c);if(v==std::array<int,4>{}){++s.abelian_hits;bool any=false;std::array<bool,16> hit{};for(std::size_t i=0;i<16;++i)if(central_zero(kCandidates[i],c)){hit[i]=true;any=true;++s.kernel_hits[i];}if(any){std::string bytes(raw.data(),raw.size());std::istringstream stream(bytes,std::ios::binary);const auto matrix=geo_read_record(stream).key;const bool dangerous=dangerous_trace(matrix);const auto trace=abs_trace_half(matrix);for(std::size_t i=0;i<16;++i)if(hit[i]){s.minimum_abs_trace_half[i]=std::min(s.minimum_abs_trace_half[i],trace);if(dangerous){++s.dangerous_hits[i];if(s.witness_depth[i]==0){s.witness_index[i]=index;s.witness_depth[i]=depth;s.witness_high[i]=high;s.witness_low[i]=low;}}}}}}
    if(s.scanned==next||s.scanned==total){auto now=std::chrono::steady_clock::now();s.elapsed_seconds+=std::chrono::duration<double>(now-started).count();started=now;s.complete=s.scanned==total;write_state(checkpoint,s);std::cout<<"scanned="<<s.scanned<<'/'<<total<<" dangerous=";for(auto x:s.dangerous_hits)std::cout<<x<<',';std::cout<<'\n'<<std::flush;next=std::min(total,next+kCommitRecords);}}
}
}
int main(int argc,char**argv){try{if(argc!=3)throw std::runtime_error("usage: REGISTRY CHECKPOINT");scan(argv[1],argv[2]);return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}}
