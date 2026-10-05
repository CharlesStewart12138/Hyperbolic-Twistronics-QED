"""Derive the p3 x D2-class2 scanner from the audited candidate-0003 v2 source."""

from pathlib import Path


HERE=Path(__file__).resolve().parent
source=(HERE/"scan_candidate_0003_axis6_v2.cpp").read_text(encoding="utf-8")
start=source.index("std::uint8_t class2_cocycle")
end=source.index("Field real_part",start)
block='''std::uint8_t class2_cocycle(std::uint8_t left,std::uint8_t right){
  const std::uint8_t lv=left&15U,rv=right&15U;
  std::uint8_t z0=0,z1=0;
  for(unsigned i=0;i<4;++i) z0^=((lv&(1U<<i))&&(rv&(1U<<i)));
  z1^=((lv&1U)&&(rv&1U));
  z1^=((lv&2U)&&(rv&2U));
  z1^=((lv&2U)&&(rv&1U));
  z1^=((lv&8U)&&(rv&4U));
  return static_cast<std::uint8_t>((z0&1U)|((z1&1U)<<1U));
}

std::uint8_t class2_multiply(std::uint8_t left,std::uint8_t right){
  const std::uint8_t lv=left&15U,rv=right&15U;
  const std::uint8_t lz=(left>>4U)&3U,rz=(right>>4U)&3U;
  return static_cast<std::uint8_t>((lv^rv)|((lz^rz^class2_cocycle(lv,rv))<<4U));
}

std::uint8_t class2_word(std::uint64_t high,std::uint64_t low,unsigned depth){
  static constexpr std::array<std::uint8_t,8> images{{1,50,7,27,49,2,55,43}};
  std::uint8_t result=0;
  for(unsigned index=0;index<depth;++index)
    result=class2_multiply(result,images[word_digit(high,low,depth,index)]);
  return result;
}

'''
source=source[:start]+block+source[end:]
source=source.replace("CAND-R4-0003-axis6-early-exit-v2","CAND-R4-0004-axis6-early-exit")
(HERE/"scan_candidate_0004_axis6.cpp").write_text(source,encoding="utf-8",newline="\n")
