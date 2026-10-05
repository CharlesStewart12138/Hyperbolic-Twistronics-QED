#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {
constexpr int DIM=25, WORDS=457;
using Bits=std::uint32_t;
struct Edge{std::uint16_t a,b;Bits difference;};
struct Input{std::array<Bits,DIM> actionRows{};Bits g0power4=0;std::vector<Edge> edges;};
Bits parse_bits(const std::string&s){if(s.size()!=DIM)throw std::runtime_error("bit string is not length 25");Bits v=0;for(int i=0;i<DIM;++i){if(s[i]=='1')v|=Bits{1}<<i;else if(s[i]!='0')throw std::runtime_error("non-bit character");}return v;}
std::string bits(Bits v){std::string s(DIM,'0');for(int i=0;i<DIM;++i)if(v&(Bits{1}<<i))s[i]='1';return s;}
Input load(const std::string&path){std::ifstream in(path);if(!in)throw std::runtime_error("cannot open GAP module export");Input x;std::string line;int rows=0,declaredWords=0,edgeTotal=-1,zeroTotal=-1;
 while(std::getline(in,line)){std::istringstream ls(line);std::string tag;ls>>tag;if(tag=="ROW"){int i;std::string s;ls>>i>>s;if(i<1||i>DIM)throw std::runtime_error("bad row index");x.actionRows[i-1]=parse_bits(s);++rows;}
  else if(tag=="G0POWER4"){std::string s;ls>>s;x.g0power4=parse_bits(s);}else if(tag=="WORDS")ls>>declaredWords;
  else if(tag=="EDGE"){int a,b;std::string s;ls>>a>>b>>s;if(a<0||a>=WORDS||b<=a||b>=WORDS)throw std::runtime_error("bad edge");x.edges.push_back({static_cast<std::uint16_t>(a),static_cast<std::uint16_t>(b),parse_bits(s)});}
  else if(tag=="EDGE_TOTAL")ls>>edgeTotal;else if(tag=="ZERO_EDGE_TOTAL")ls>>zeroTotal;}
 if(rows!=DIM||declaredWords!=WORDS||edgeTotal!=static_cast<int>(x.edges.size())||zeroTotal!=0||x.g0power4==0)throw std::runtime_error("GAP export contract failure");return x;}
int dot(Bits a,Bits b){return std::popcount(a&b)&1;}
Bits apply_rows(const std::array<Bits,DIM>&rows,Bits v){Bits o=0;for(int i=0;i<DIM;++i)if(dot(rows[i],v))o|=Bits{1}<<i;return o;}
std::array<Bits,DIM> compose_rows(const std::array<Bits,DIM>&a,const std::array<Bits,DIM>&b){ // a(b(v))
 std::array<Bits,DIM>o{};for(int i=0;i<DIM;++i){Bits r=0,m=a[i];while(m){int j=std::countr_zero(m);r^=b[j];m&=m-1;}o[i]=r;}return o;}
std::vector<Bits> kernel_basis(std::array<Bits,DIM> eq){int rank=0;std::array<int,DIM>pivot{};pivot.fill(-1);
 for(int col=0;col<DIM;++col){int sel=-1;for(int r=rank;r<DIM;++r)if((eq[r]>>col)&1U){sel=r;break;}if(sel<0)continue;std::swap(eq[rank],eq[sel]);
  for(int r=0;r<DIM;++r)if(r!=rank&&((eq[r]>>col)&1U))eq[r]^=eq[rank];pivot[col]=rank++;}
 std::vector<Bits>basis;for(int freecol=0;freecol<DIM;++freecol)if(pivot[freecol]<0){Bits v=Bits{1}<<freecol;
  for(int col=0;col<DIM;++col)if(pivot[col]>=0&&((eq[pivot[col]]>>freecol)&1U))v|=Bits{1}<<col;basis.push_back(v);}return basis;}
std::vector<Bits> span(const std::vector<Bits>&basis){std::vector<Bits>v{0};for(Bits b:basis){auto n=v.size();for(std::size_t i=0;i<n;++i)v.push_back(v[i]^b);}std::sort(v.begin(),v.end());return v;}
struct DSU{std::array<std::uint16_t,WORDS>p{};DSU(){for(int i=0;i<WORDS;++i)p[i]=i;}int find(int x){while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;}void join(int a,int b){a=find(a);b=find(b);if(a!=b)p[b]=a;}int count(){int n=0;for(int i=0;i<WORDS;++i)if(find(i)==i)++n;return n;}};
int b3(Bits f1,Bits f2,const std::vector<Edge>&edges){DSU d;for(const auto&e:edges)if(!dot(e.difference,f1)&&!dot(e.difference,f2))d.join(e.a,e.b);return d.count();}
struct Quotient{Bits f1=0,f2=0;int dim=0;std::string type;};
}
int main(int argc,char**argv)try{
 if(argc!=3)throw std::runtime_error("usage: classifier GAP_EXPORT OUTPUT");Input in=load(argv[1]);std::ofstream out(argv[2]);if(!out)throw std::runtime_error("cannot create output");
 std::array<Bits,DIM>id{},nilRows{};for(int i=0;i<DIM;++i){id[i]=Bits{1}<<i;nilRows[i]=in.actionRows[i]^id[i];}
 auto action2=compose_rows(in.actionRows,in.actionRows),action4=compose_rows(action2,action2),action8=compose_rows(action4,action4);
 if(action8!=id)throw std::runtime_error("T^8 is not identity");auto nil2=compose_rows(nilRows,nilRows); auto nil3=compose_rows(nil2,nilRows),nil4=compose_rows(nil2,nil2);for(Bits r:nil4)if(r)throw std::runtime_error("(T-I)^4 is not zero");
 auto k1basis=kernel_basis(nilRows),k2basis=kernel_basis(nil2),k3basis=kernel_basis(nil3);if(k1basis.size()!=7||k2basis.size()!=13||k3basis.size()!=19)throw std::runtime_error("kernel dimensions differ from GAP v3");
 auto k1=span(k1basis),k2=span(k2basis);std::vector<Quotient>q;q.push_back({0,0,0,"ZERO"});
 for(Bits f:k1)if(f)q.push_back({f,0,1,"J1"});
 std::set<std::array<Bits,3>>trivial,jordan;
 for(std::size_t i=1;i<k1.size();++i)for(std::size_t j=i+1;j<k1.size();++j){std::array<Bits,3>a{k1[i],k1[j],Bits(k1[i]^k1[j])};std::sort(a.begin(),a.end());trivial.insert(a);}
 for(Bits f:k2){Bits n=apply_rows(nilRows,f);if(n){std::array<Bits,3>a{f,n,Bits(f^n)};std::sort(a.begin(),a.end());jordan.insert(a);}}
 if(trivial.size()!=2667||jordan.size()!=4032)throw std::runtime_error("invariant-plane counts are not 2667+4032");
 for(const auto&a:trivial)q.push_back({a[0],a[1],2,"J1+J1"});for(const auto&a:jordan)q.push_back({a[0],a[1],2,"J2"});
 if(q.size()!=6827)throw std::runtime_error("total quotient count is not 6827");
 out<<"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-FULL-U2-SKELETON-DIMLE2\n"
    <<"SCOPE\tall phi8-stable quotients U3/W with W contained in L3 and dim(L3/W)<=2; equivalently all p-class<=3 quotients retaining the full U2 skeleton in the order window\n"
    <<"NONCLAIM\tnot all p-class3 2-group quotients: kernels not contained in L3 are outside this certificate\n"
    <<"METHOD\tdual invariant subspaces S=W_perp; radius-3 equality iff both functionals annihilate the exact L3 difference mask\n"
    <<"DUAL_JORDAN_TYPE\tJ4^6+J1\nKERNEL_DIM_TMINUSI\t"<<k1basis.size()<<"\nKERNEL_DIM_TMINUSI_SQUARED\t"<<k2basis.size()<<"\nKERNEL_DIM_TMINUSI_CUBED\t"<<k3basis.size()<<"\n"
    <<"DIM0_QUOTIENTS\t1\nDIM1_J1_QUOTIENTS\t127\nDIM2_TRIVIAL_QUOTIENTS\t"<<trivial.size()<<"\nDIM2_J2_QUOTIENTS\t"<<jordan.size()<<"\nTOTAL_QUOTIENTS\t"<<q.size()<<"\n"
    <<"GAP_COLLISION_EDGES\t"<<in.edges.size()<<"\nG0_POWER4_MASK\t"<<bits(in.g0power4)<<"\n";
 std::map<std::tuple<int,std::string,int>,std::uint64_t>dist;std::array<std::uint64_t,3>sep{},surv{};std::array<int,3>maxb{};
 for(const auto&x:q){
  Bits tf1=apply_rows(in.actionRows,x.f1),tf2=apply_rows(in.actionRows,x.f2);
  auto member=[&](Bits z){return z==0||z==x.f1||z==x.f2||z==(x.f1^x.f2);};if(!member(tf1)||!member(tf2))throw std::runtime_error("enumerated plane is not T-invariant");
  bool separates=dot(in.g0power4,x.f1)||dot(in.g0power4,x.f2);if(separates)++sep[x.dim];int card=b3(x.f1,x.f2,in.edges);++dist[{x.dim,x.type,card}];maxb[x.dim]=std::max(maxb[x.dim],card);
  if(card==457){++surv[x.dim];out<<"B3_SURVIVOR\tDIM\t"<<x.dim<<"\tTYPE\t"<<x.type<<"\tORDER\t"<<(std::uint64_t{1}<<(13+x.dim))<<"\tF1\t"<<bits(x.f1)<<"\tF2\t"<<bits(x.f2)<<"\tSEPARATES_G0POWER4\t"<<separates<<"\n";}
 }
 if(b3(0,0,in.edges)!=325)throw std::runtime_error("dim0 quotient does not reproduce certified U2 B3=325");
 for(int d=0;d<=2;++d)out<<"DIM_SUMMARY\tDIM\t"<<d<<"\tORDER\t"<<(std::uint64_t{1}<<(13+d))<<"\tG0POWER4_SEPARATED\t"<<sep[d]<<"\tMAX_B3\t"<<maxb[d]<<"\tB3_EQ_457\t"<<surv[d]<<"\n";
 for(const auto&[k,n]:dist){auto[d,t,c]=k;out<<"B3_DISTRIBUTION\tDIM\t"<<d<<"\tTYPE\t"<<t<<"\tCARDINALITY\t"<<c<<"\tCOUNT\t"<<n<<"\n";}
 auto totalSurv=surv[0]+surv[1]+surv[2];out<<"TOTAL\tQUOTIENTS\t"<<q.size()<<"\tB3_SURVIVORS\t"<<totalSurv<<"\nRESULT\tPASS\nDONE\n";return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}
