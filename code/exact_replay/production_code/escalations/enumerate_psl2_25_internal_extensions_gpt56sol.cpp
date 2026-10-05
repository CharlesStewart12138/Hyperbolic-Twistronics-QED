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
#include <unordered_set>
#include <vector>

// Exact scan of the three index-two extensions of PSL(2,25) inside
// P Gamma L(2,25): diagonal (PGL), field (P Sigma L), and diagonal-field.
// Each target has order 15,600 and its nontrivial outer coset is the frozen
// physical parity class.  Aut(target) is induced faithfully by P Gamma L:
// the characteristic socle PSL(2,25) is centerless and self-centralizing,
// while all three index-two subgroups are normal in the abelian outer V4.
// Thus the two P Gamma L conjugacy classes below exhaust exact-order-eight
// automorphisms.  Every odd-coset seed is tested exactly.

namespace {
using Mat=std::array<std::uint8_t,4>;
struct Meta { std::uint32_t parent; std::uint8_t generator,depth; std::uint16_t reserved; };
static_assert(sizeof(Meta)==8);

struct F25 {
 std::array<std::array<std::uint8_t,25>,25> add{},mul{};
 std::array<std::uint8_t,25> neg{},inv{},fr{};
 F25(){
  for(int x=0;x<25;++x){int a=x%5,b=x/5;neg[x]=(-a+5)%5+5*((-b+5)%5);
   for(int y=0;y<25;++y){int c=y%5,d=y/5;
    add[x][y]=(a+c)%5+5*((b+d)%5);
    mul[x][y]=(a*c+3*b*d)%5+5*((a*d+b*c)%5);
   }
  }
  for(int x=1;x<25;++x){for(int y=1;y<25;++y)if(mul[x][y]==1){inv[x]=y;break;}
   if(!inv[x])throw std::runtime_error("field inverse");
  }
  for(int x=0;x<25;++x)fr[x]=power(x,5);
 }
 std::uint8_t power(std::uint8_t x,unsigned n)const{std::uint8_t r=1;while(n){if(n&1)r=mul[r][x];x=mul[x][x];n>>=1;}return r;}
 Mat sigma(Mat x)const{for(auto&z:x)z=fr[z];return x;}
 Mat norm(Mat x)const{auto it=std::find_if(x.begin(),x.end(),[](auto z){return z;});if(it==x.end())throw std::runtime_error("zero matrix");auto s=inv[*it];for(auto&z:x)z=mul[z][s];return x;}
 std::uint8_t det(const Mat&x)const{return add[mul[x[0]][x[3]]][neg[mul[x[1]][x[2]]]];}
 Mat product(const Mat&x,const Mat&y)const{return norm({
  add[mul[x[0]][y[0]]][mul[x[1]][y[2]]],add[mul[x[0]][y[1]]][mul[x[1]][y[3]]],
  add[mul[x[2]][y[0]]][mul[x[3]][y[2]]],add[mul[x[2]][y[1]]][mul[x[3]][y[3]]]});}
 Mat inverse(const Mat&x)const{return norm({x[3],neg[x[1]],neg[x[2]],x[0]});}
 bool nonsquare_det(const Mat&x)const{return power(det(x),12)!=1;}
};

std::uint32_t pack_mat(const Mat&x){return x[0]|(std::uint32_t(x[1])<<5)|(std::uint32_t(x[2])<<10)|(std::uint32_t(x[3])<<15);}
struct Semi { Mat c; std::uint8_t k; };
bool operator==(const Semi&a,const Semi&b){return a.k==b.k&&a.c==b.c;}
bool operator<(const Semi&a,const Semi&b){return a.k<b.k||(a.k==b.k&&a.c<b.c);}
std::uint32_t pack(const Semi&x){return pack_mat(x.c)|(std::uint32_t(x.k)<<20);}
Semi compose(const F25&f,const Semi&a,const Semi&b){return{f.product(a.c,a.k?f.sigma(b.c):b.c),std::uint8_t((a.k+b.k)&1)};}
Semi inverse(const F25&f,const Semi&a){return{a.k?f.sigma(f.inverse(a.c)):f.inverse(a.c),a.k};}
Semi conjugate(const F25&f,const Semi&a,const Semi&x){return compose(f,compose(f,a,x),inverse(f,a));}
unsigned order(const F25&f,const Semi&a){Semi p{{1,0,0,1},0},id=p;for(unsigned n=1;n<=64;++n){p=compose(f,p,a);if(p==id)return n;}return 0;}
unsigned outer_label(const F25&f,const Semi&x){return unsigned(f.nonsquare_det(x.c))|(unsigned(x.k)<<1);}

std::size_t b3(const F25&f,const std::array<Semi,8>&g){
 std::set<std::uint32_t>s; const Semi id{{1,0,0,1},0}; s.insert(pack(id));
 for(int a=0;a<8;++a){s.insert(pack(g[a]));for(int b=0;b<8;++b)if(b!=(a+4)%8){auto ab=compose(f,g[a],g[b]);s.insert(pack(ab));for(int c=0;c<8;++c)if(c!=(b+4)%8)s.insert(pack(compose(f,ab,g[c])));}}
 return s.size();
}
std::size_t generated(const F25&f,const std::array<Semi,8>&g){
 std::unordered_set<std::uint32_t>s;std::queue<Semi>q;Semi id{{1,0,0,1},0};s.insert(pack(id));q.push(id);
 while(!q.empty()){auto x=q.front();q.pop();for(const auto&a:g){auto y=compose(f,x,a);if(s.insert(pack(y)).second)q.push(y);}}
 return s.size();
}
std::vector<Meta> load_tree(const char*path){
 std::ifstream in(path,std::ios::binary);char magic[8]{};std::uint64_t n=0;std::uint32_t width=0;
 in.read(magic,8);in.read(reinterpret_cast<char*>(&n),8);in.read(reinterpret_cast<char*>(&width),4);
 if(!in||std::string(magic,8)!="BOLZAT01"||n!=23129593||width!=8)throw std::runtime_error("based-tree contract");
 std::vector<Meta>v(n);in.read(reinterpret_cast<char*>(v.data()),std::streamsize(n*sizeof(Meta)));if(!in)throw std::runtime_error("short based tree");return v;
}
std::string show(const Semi&x){return"("+std::to_string(x.c[0])+","+std::to_string(x.c[1])+","+std::to_string(x.c[2])+","+std::to_string(x.c[3])+";"+std::to_string(unsigned(x.k))+")";}
struct Candidate { unsigned target,cls,orbit; Semi seed; std::array<Semi,8> images; };
}

int main(int argc,char**argv){try{
 if(argc!=2)throw std::runtime_error("usage: enumerator BASED_TREE_META_BIN");
 F25 f;const Semi id{{1,0,0,1},0};
 std::set<std::uint32_t>mkeys;std::vector<Mat>pgl;
 for(int a=0;a<25;++a)for(int b=0;b<25;++b)for(int c=0;c<25;++c)for(int d=0;d<25;++d){
  Mat x{std::uint8_t(a),std::uint8_t(b),std::uint8_t(c),std::uint8_t(d)};if(!f.det(x))continue;mkeys.insert(pack_mat(f.norm(x)));
 }
 for(auto z:mkeys)pgl.push_back(Mat{std::uint8_t(z&31),std::uint8_t((z>>5)&31),std::uint8_t((z>>10)&31),std::uint8_t((z>>15)&31)});
 if(pgl.size()!=15600)throw std::runtime_error("PGL order");
 std::vector<Semi>ambient;ambient.reserve(31200);for(int k=0;k<2;++k)for(const auto&m:pgl)ambient.push_back({m,std::uint8_t(k)});
 const std::array<Semi,2>alphas{{{{0,1,5,9},0},{{0,1,5,5},1}}};
 std::uint64_t order8=0;for(const auto&z:ambient)order8+=(order(f,z)==8);if(order8!=5200)throw std::runtime_error("order-eight ambient count");
 std::uint64_t classSum=0;std::vector<Candidate>candidates;
 // Target labels are the two-element outer subgroups {0,h}; h=1,2,3.
 // Their odd physical cosets have label h.
 for(unsigned h=1;h<=3;++h){
  std::vector<Semi>target,seeds;target.reserve(15600);seeds.reserve(7800);
  for(const auto&z:ambient){auto o=outer_label(f,z);if(o==0||o==h)target.push_back(z);if(o==h)seeds.push_back(z);}
  if(target.size()!=15600||seeds.size()!=7800)throw std::runtime_error("target/coset size");
  std::cout<<"TARGET h="<<h<<" name="<<(h==1?"PGL_diagonal":h==2?"PSigmaL_field":"diagonal_field")<<" order=15600 odd_seeds=7800\n";
  for(unsigned cls=0;cls<alphas.size();++cls){const auto alpha=alphas[cls];std::vector<Semi>C;
   for(const auto&z:ambient)if(compose(f,alpha,z)==compose(f,z,alpha))C.push_back(z);
   if(h==1)classSum+=31200/C.size();
   std::uint64_t ni=0,nr=0,nd=0,nb=0,ng=0;std::vector<Semi>surv;
   for(const auto&x:seeds){std::array<Semi,8>g{};g[0]=x;for(int j=1;j<8;++j)g[j]=conjugate(f,alpha,g[j-1]);
    bool ok=true;for(int j=0;j<4;++j)ok&=(g[j+4]==inverse(f,g[j]));if(!ok)continue;++ni;
    auto r=id;for(int j:std::array<int,8>{0,5,2,7,4,1,6,3})r=compose(f,r,g[j]);if(!(r==id))continue;++nr;
    if(std::set<Semi>(g.begin(),g.end()).size()!=8)continue;++nd;
    if(b3(f,g)!=457)continue;++nb;if(generated(f,g)!=15600)continue;++ng;surv.push_back(x);
   }
   std::set<Semi>left(surv.begin(),surv.end());unsigned oi=0;
   while(!left.empty()){auto rep=*left.begin();std::set<Semi>orb;for(const auto&z:C)orb.insert(conjugate(f,z,rep));for(const auto&y:orb)left.erase(y);
    std::array<Semi,8>g{};g[0]=rep;for(int j=1;j<8;++j)g[j]=conjugate(f,alpha,g[j-1]);candidates.push_back({h,cls,oi,rep,g});
    std::cout<<"ORBIT h="<<h<<" class="<<cls<<" orbit="<<oi++<<" size="<<orb.size()<<" rep="<<show(rep)<<"\n";
   }
   std::cout<<"CLASS h="<<h<<" class="<<cls<<" alpha="<<show(alpha)<<" centralizer="<<C.size()<<" class_size="<<31200/C.size()
    <<" seeds=7800 inverse="<<ni<<" relator="<<nr<<" distinct="<<nd<<" b3="<<nb<<" generates="<<ng<<" centralizer_orbits="<<oi<<"\n";
  }
 }
 if(classSum!=order8)throw std::runtime_error("two alpha classes do not exhaust exact-order-eight automorphisms");
 std::cout<<"AUT order=31200 order8="<<order8<<" class_sum="<<classSum<<" candidates="<<candidates.size()<<"\n";
 if(candidates.empty())return 0;
 auto tree=load_tree(argv[1]);
 for(const auto&cand:candidates){
  std::vector<Semi>elts;elts.reserve(15600);std::unordered_map<std::uint32_t,std::uint16_t>idx;
  for(const auto&z:ambient){auto o=outer_label(f,z);if(o==0||o==cand.target){idx.emplace(pack(z),std::uint16_t(elts.size()));elts.push_back(z);}}
  const auto idIndex=idx.at(pack(id));std::array<std::vector<std::uint16_t>,8>tr;
  for(int j=0;j<8;++j){tr[j].resize(elts.size());for(std::size_t i=0;i<elts.size();++i)tr[j][i]=idx.at(pack(compose(f,elts[i],cand.images[j])));}
  std::vector<std::uint16_t>state(tree.size());state[0]=idIndex;std::uint32_t witness=0;
  for(std::uint32_t i=1;i<tree.size();++i){const auto e=tree[i];state[i]=tr[e.generator][state[e.parent]];if(!(e.depth&1)&&state[i]==idIndex){witness=i;break;}}
  std::cout<<"BASED h="<<cand.target<<" class="<<cand.cls<<" orbit="<<cand.orbit;
  if(!witness){std::cout<<" PASS\n";continue;}
  std::vector<unsigned>word;for(auto i=witness;i;i=tree[i].parent)word.push_back(tree[i].generator);std::reverse(word.begin(),word.end());
  std::cout<<" FAIL witness_id="<<witness<<" depth="<<unsigned(tree[witness].depth)<<" word=";for(std::size_t i=0;i<word.size();++i)std::cout<<(i?" ":"")<<"g"<<word[i];std::cout<<"\n";
 }
 return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<"\n";return 2;}}
