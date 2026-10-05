#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#define CM_GEO7_NO_MAIN
#include "../../production_code/group/external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN

namespace {

constexpr std::uint32_t kCutoffMarker = std::numeric_limits<std::uint32_t>::max();
constexpr std::uint64_t kCommitRecords = 1'000'000;
constexpr int p = 3;
constexpr std::uint32_t kRingSize = 6561;  // 3^8 algebra coordinate tuples.

struct K { std::uint8_t a = 0, b = 0; };
using A = std::array<K,4>;  // I,X,Y,Z over F5[s]/(s^2-2).

int mod(int x) { x %= p; return x < 0 ? x + p : x; }
K add(K x,K y){return K{static_cast<std::uint8_t>(mod(x.a+y.a)),static_cast<std::uint8_t>(mod(x.b+y.b))};}
K neg(K x){return K{static_cast<std::uint8_t>(mod(-x.a)),static_cast<std::uint8_t>(mod(-x.b))};}
K mul(K x,K y){return K{static_cast<std::uint8_t>(mod(x.a*y.a+2*x.b*y.b)),static_cast<std::uint8_t>(mod(x.a*y.b+x.b*y.a))};}
bool zero(K x){return x.a==0&&x.b==0;}

void accumulate(A& out,int target,K value){out[target]=add(out[target],value);}

void basis_product(A& out,int left,int right,K coefficient){
  const K one{1,0}, c0{2,2}, d0{4,2}, c02=mul(c0,c0);
  if(left==0){accumulate(out,right,coefficient);return;}
  if(right==0){accumulate(out,left,coefficient);return;}
  if(left==1&&right==1){accumulate(out,0,mul(coefficient,c0));return;}
  if(left==1&&right==2){accumulate(out,3,coefficient);return;}
  if(left==2&&right==1){accumulate(out,0,mul(coefficient,d0));accumulate(out,3,neg(coefficient));return;}
  if(left==2&&right==2){accumulate(out,0,mul(coefficient,c0));return;}
  if(left==1&&right==3){accumulate(out,2,mul(coefficient,c0));return;}
  if(left==3&&right==1){accumulate(out,1,mul(coefficient,d0));accumulate(out,2,mul(coefficient,neg(c0)));return;}
  if(left==2&&right==3){accumulate(out,2,mul(coefficient,d0));accumulate(out,1,mul(coefficient,neg(c0)));return;}
  if(left==3&&right==2){accumulate(out,1,mul(coefficient,c0));return;}
  if(left==3&&right==3){accumulate(out,3,mul(coefficient,d0));accumulate(out,0,mul(coefficient,neg(c02)));return;}
  throw std::runtime_error("missing algebra product");
}

A amultiply(A left,A right){
  A out{};
  for(int i=0;i<4;++i)if(!zero(left[i]))for(int j=0;j<4;++j)if(!zero(right[j]))
    basis_product(out,i,j,mul(left[i],right[j]));
  return out;
}

A agenerator(int index){
  static constexpr int uv[8][4]={{1,0,0,0},{0,0,1,0},{-1,0,0,1},{0,-1,1,0},{-1,0,0,0},{0,0,-1,0},{1,0,0,-1},{0,1,-1,0}};
  A result{}; result[0]=K{1,1};
  result[1]=K{static_cast<std::uint8_t>(mod(uv[index][0])),static_cast<std::uint8_t>(mod(uv[index][1]))};
  result[2]=K{static_cast<std::uint8_t>(mod(uv[index][2])),static_cast<std::uint8_t>(mod(uv[index][3]))};
  return result;
}

std::uint32_t encode(const A& value){
  std::uint32_t code=0,scale=1;
  for(const auto& x:value)for(const auto digit:{x.a,x.b}){code+=scale*digit;scale*=p;}
  return code;
}

A decode(std::uint32_t code){
  A value{};
  for(auto& x:value){x.a=code%p;code/=p;x.b=code%p;code/=p;}
  return value;
}

std::array<std::vector<std::uint32_t>,8> transitions(){
  std::array<std::vector<std::uint32_t>,8> result;
  for(auto& row:result)row.resize(kRingSize);
  for(std::uint32_t code=0;code<kRingSize;++code){
    const A value=decode(code);
    for(int index=0;index<8;++index)result[index][code]=encode(amultiply(value,agenerator(index)));
  }
  return result;
}

std::uint8_t word_digit(std::uint64_t high,std::uint64_t low,unsigned depth,unsigned index){
  const unsigned shift=3U*(depth-1U-index);
  return shift<64U?static_cast<std::uint8_t>((low>>shift)&7U):static_cast<std::uint8_t>((high>>(shift-64U))&7U);
}

std::uint32_t word_image(std::uint64_t high,std::uint64_t low,unsigned depth,const std::array<std::vector<std::uint32_t>,8>& next){
  std::uint32_t state=encode(A{K{1,0},K{},K{},K{}});
  for(unsigned index=0;index<depth;++index)state=next[word_digit(high,low,depth,index)][state];
  return state;
}

Matrix matrix_from_raw(const std::array<char,kGeoRecordBytes>& raw){
  std::string bytes(raw.data(),raw.size());
  std::istringstream in(bytes,std::ios::binary);
  return geo_read_record(in).key;
}

std::uint8_t class2_cocycle(std::uint8_t left,std::uint8_t right){
  // Projection row 19 selects a1^2, b1^2, and [b1,a1].
  std::uint8_t z=0;
  z^=((left&1U)&&(right&1U));
  z^=((left&2U)&&(right&2U));
  z^=((left&2U)&&(right&1U));
  z^=((left&8U)&&(right&4U));  // [b2,a2]=[b1,a1]
  return z&1U;
}

std::uint8_t class2_multiply(std::uint8_t left,std::uint8_t right){
  const std::uint8_t lv=left&15U,rv=right&15U;
  const std::uint8_t lz=(left>>4U)&1U,rz=(right>>4U)&1U;
  return static_cast<std::uint8_t>((lv^rv)|((lz^rz^class2_cocycle(lv,rv))<<4U));
}

std::uint8_t class2_word(std::uint64_t high,std::uint64_t low,unsigned depth){
  static constexpr std::array<std::uint8_t,8> images{{1,18,7,11,17,2,23,27}};
  std::uint8_t result=0;
  for(unsigned index=0;index<depth;++index)
    result=class2_multiply(result,images[word_digit(high,low,depth,index)]);
  return result;
}

Field real_part(Field value){for(std::size_t i=4;i<8;++i)value.c[i]=0;return value;}
bool dangerous_trace(const Matrix& matrix){
  const Field re=real_part(matrix.a);
  const Field cutoff=field_from({2405,1700,0,0,0,0,0,0});
  const Field delta=add(multiply(re,re),negate(multiply(cutoff,cutoff)));
  return geo_exact_real_field_sign(delta)<=0;
}

struct State{std::uint64_t scanned=0;bool hit=false;};

State load_state(const fs::path& path){
  State state; if(!fs::exists(path))return state;
  std::ifstream in(path);std::string line;
  while(std::getline(in,line)){const auto tab=line.find('\t');if(tab==std::string::npos)continue;
    const auto key=line.substr(0,tab),value=line.substr(tab+1);
    if(key=="scanned_records")state.scanned=std::stoull(value);
    if(key=="hit")state.hit=value=="1";
  }
  return state;
}

void save_state(const fs::path& path,const State& state,std::uint64_t total,double elapsed){
  const fs::path temporary=path.string()+".tmp";
  std::ofstream out(temporary,std::ios::trunc);
  out<<"schema_version\t1.0\nalgorithm\tCAND-R4-0003-axis6-early-exit-v2\n"
     <<"total_records\t"<<total<<"\nscanned_records\t"<<state.scanned
     <<"\nhit\t"<<(state.hit?1:0)<<"\nelapsed_seconds\t"<<elapsed<<'\n';
  out.close();if(!out)throw std::runtime_error("checkpoint write failed");
  if(fs::exists(path))fs::remove(path);fs::rename(temporary,path);
}

std::string word_string(std::uint64_t high,std::uint64_t low,unsigned depth){
  std::ostringstream out;
  for(unsigned i=0;i<depth;++i){if(i)out<<' ';out<<'g'<<static_cast<unsigned>(word_digit(high,low,depth,i));}
  return out.str();
}

void save_witness(const fs::path& path,std::uint64_t record,unsigned depth,std::uint64_t high,std::uint64_t low,const Matrix& matrix){
  const fs::path temporary=path.string()+".tmp";
  const Field re=real_part(matrix.a);
  std::ofstream out(temporary,std::ios::trunc);
  out<<"record_index\tdepth\tword\tword_high\tword_low\texponent\tre_c0\tre_c1\tre_c2\tre_c3\n";
  out<<record<<'\t'<<depth<<'\t'<<word_string(high,low,depth)<<'\t'<<high<<'\t'<<low<<'\t'
     <<static_cast<unsigned>(re.exp);
  for(int i=0;i<4;++i)out<<'\t'<<re.c[i];
  out<<'\n';out.close();if(!out)throw std::runtime_error("witness write failed");
  if(fs::exists(path))fs::remove(path);fs::rename(temporary,path);
}

void scan(const fs::path& registry,const fs::path& checkpoint,const fs::path& witness){
  const auto next=transitions();
  // Exact finite-image self-tests before touching the 115 GB registry.
  const auto identity=encode(A{K{1,0},K{},K{},K{}});
  for(unsigned j=0;j<8;++j){
    const std::uint64_t code=(static_cast<std::uint64_t>(j)<<3U)|((j+4U)%8U);
    if(word_image(0,code,2,next)!=identity)throw std::runtime_error("inverse-shell self-test failed");
  }
  const std::array<unsigned,8> rel{{0,5,2,7,4,1,6,3}};
  std::uint64_t relcode=0;for(auto digit:rel)relcode=(relcode<<3U)|digit;
  if(word_image(0,relcode,8,next)!=identity)throw std::runtime_error("surface-relator self-test failed");
  if(class2_word(0,relcode,8)!=0U)throw std::runtime_error("class2 surface-relator self-test failed");
  for(unsigned j=0;j<8;++j){
    const std::uint64_t qcode=(static_cast<std::uint64_t>(j)<<3U)|((j+4U)%8U);
    if(class2_word(0,qcode,2)!=0U)throw std::runtime_error("class2 inverse-shell self-test failed");
  }

  std::ifstream input(registry,std::ios::binary);if(!input)throw std::runtime_error("cannot open registry");
  static std::array<char,16*1024*1024> buffer{};input.rdbuf()->pubsetbuf(buffer.data(),buffer.size());
  char magic[8]{};input.read(magic,8);if(std::string(magic,8)!="BOLZGEO1")throw std::runtime_error("bad magic");
  const auto total=read_u64(input);if(read_u32(input)!=kGeoRecordBytes||read_u32(input)!=kCutoffMarker)throw std::runtime_error("bad registry contract");
  State state=load_state(checkpoint);if(state.hit)return;
  input.seekg(static_cast<std::streamoff>(24ULL+state.scanned*kGeoRecordBytes));
  std::array<char,kGeoRecordBytes> raw{};
  auto start=std::chrono::steady_clock::now();
  std::uint64_t next_commit=std::min(total,((state.scanned/kCommitRecords)+1)*kCommitRecords);
  while(state.scanned<total){
    input.read(raw.data(),raw.size());if(!input)throw std::runtime_error("short registry record");
    const std::uint64_t record=state.scanned++;
    const auto depth=static_cast<std::uint8_t>(raw[130]);
    std::uint64_t high=0,low=0;std::memcpy(&high,raw.data()+131,8);std::memcpy(&low,raw.data()+139,8);
    if(depth&&class2_word(high,low,depth)==0U&&word_image(high,low,depth,next)==identity){
      const Matrix matrix=matrix_from_raw(raw);
      if(dangerous_trace(matrix)){
        state.hit=true;save_witness(witness,record,depth,high,low,matrix);
        const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        save_state(checkpoint,state,total,elapsed);
        std::cout<<"HIT record="<<record<<" depth="<<static_cast<unsigned>(depth)<<" word="<<word_string(high,low,depth)<<'\n';
        return;
      }
    }
    if(state.scanned==next_commit){
      const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
      save_state(checkpoint,state,total,elapsed);
      std::cout<<"scanned="<<state.scanned<<'/'<<total<<'\n'<<std::flush;
      next_commit=std::min(total,next_commit+kCommitRecords);
    }
  }
  const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  save_state(checkpoint,state,total,elapsed);
  std::cout<<"COMPLETE_NO_HIT\n";
}

} // namespace

int main(int argc,char** argv){
  try{
    if(argc!=4)throw std::runtime_error("usage: REGISTRY CHECKPOINT WITNESS");
    scan(argv[1],argv[2],argv[3]);return 0;
  }catch(const std::exception& error){std::cerr<<"ERROR: "<<error.what()<<'\n';return 2;}
}
