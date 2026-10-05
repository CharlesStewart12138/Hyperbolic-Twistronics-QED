"""Add the required exact translation-length filter to independent scanner v1."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=(HERE/"scan_candidate_0005_independent.cpp").read_text(encoding="utf-8")
needle="#include <vector>\n"
include='''#include <vector>

#define CM_GEO7_NO_MAIN
#include "../../production_code/group/external_geometric_ball.cpp"
#undef CM_GEO7_NO_MAIN
'''
if source.count(needle)!=1: raise RuntimeError("include insertion mismatch")
source=source.replace(needle,include)
source=source.replace("namespace fs=std::filesystem;\n","")
insert='''
Matrix independent_matrix_from_raw(const std::array<char,kRecordBytes>& raw){
 std::string bytes(raw.data(),raw.size());std::istringstream in(bytes,std::ios::binary);return geo_read_record(in).key;
}
Field independent_real_part(Field value){for(std::size_t i=4;i<8;++i)value.c[i]=0;return value;}
bool independent_dangerous_trace(const Matrix& matrix){
 const Field re=independent_real_part(matrix.a);const Field cutoff=field_from({2405,1700,0,0,0,0,0,0});
 const Field delta=add(multiply(re,re),negate(multiply(cutoff,cutoff)));return geo_exact_real_field_sign(delta)<=0;
}
'''
marker="struct State{std::uint64_t scanned=0;bool hit=false;};\n"
if source.count(marker)!=1: raise RuntimeError("geometry insertion mismatch")
source=source.replace(marker,insert+marker)
old="  if(d&&image(m,hi,lo,d)==0){"
new="  if(d&&image(m,hi,lo,d)==0&&independent_dangerous_trace(independent_matrix_from_raw(raw))){"
if source.count(old)!=1: raise RuntimeError("filter repair mismatch")
source=source.replace(old,new)
source=source.replace("CAND-R4-0005-independent-joint-state","CAND-R4-0005-independent-joint-state-v2")
(HERE/"scan_candidate_0005_independent_v2.cpp").write_text(source,encoding="utf-8",newline="\n")
