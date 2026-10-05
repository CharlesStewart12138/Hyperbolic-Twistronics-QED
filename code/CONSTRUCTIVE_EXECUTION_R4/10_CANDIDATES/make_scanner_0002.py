"""Derive the p=3 plus H1(F2) early-exit scanner from audited scanner v2."""

from pathlib import Path


HERE = Path(__file__).resolve().parent
source = (HERE / "scan_candidate_0001_axis6_v2.cpp").read_text(encoding="utf-8")
source = source.replace("constexpr int p = 5;", "constexpr int p = 3;")
source = source.replace(
    "constexpr std::uint32_t kRingSize = 390625;  // 5^8 algebra coordinate tuples.",
    "constexpr std::uint32_t kRingSize = 6561;  // 3^8 algebra coordinate tuples.",
)
source = source.replace("code%5;code/=5", "code%p;code/=p")
needle = "Field real_part(Field value){"
homology = """std::uint8_t homology_word(std::uint64_t high,std::uint64_t low,unsigned depth){
  static constexpr std::array<std::uint8_t,8> images{{1,2,7,11,1,2,7,11}};
  std::uint8_t result=0;
  for(unsigned index=0;index<depth;++index)result^=images[word_digit(high,low,depth,index)];
  return result;
}

"""
if needle not in source:
    raise RuntimeError("scanner insertion point missing")
source = source.replace(needle, homology + needle, 1)
source = source.replace(
    "if(depth&&!(depth&1U)&&word_image(high,low,depth,next)==identity){",
    "if(depth&&homology_word(high,low,depth)==0U&&word_image(high,low,depth,next)==identity){",
)
source = source.replace("CAND-R4-0001-axis6-early-exit", "CAND-R4-0002-axis6-early-exit")
(HERE / "scan_candidate_0002_axis6.cpp").write_text(source, encoding="utf-8", newline="\n")
