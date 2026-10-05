"""Derive the p3 x 32-element class-2 early-exit scanner from candidate 0002."""

from pathlib import Path


HERE = Path(__file__).resolve().parent
source = (HERE / "scan_candidate_0002_axis6_v2.cpp").read_text(encoding="utf-8")

old = '''std::uint8_t homology_word(std::uint64_t high,std::uint64_t low,unsigned depth){
  static constexpr std::array<std::uint8_t,8> images{{1,2,7,11,1,2,7,11}};
  std::uint8_t result=0;
  for(unsigned index=0;index<depth;++index)result^=images[word_digit(high,low,depth,index)];
  return result;
}
'''
new = '''std::uint8_t class2_cocycle(std::uint8_t left,std::uint8_t right){
  // Projection row 19 selects a1^2, b1^2, and [b1,a1].
  std::uint8_t z=0;
  z^=((left&1U)&&(right&1U));
  z^=((left&2U)&&(right&2U));
  z^=((left&2U)&&(right&1U));
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
'''
if source.count(old) != 1:
    raise RuntimeError("candidate-0002 homology block did not match")
source = source.replace(old, new)
source = source.replace(
    "if(depth&&homology_word(high,low,depth)==0U&&word_image(high,low,depth,next)==identity){",
    "if(depth&&class2_word(high,low,depth)==0U&&word_image(high,low,depth,next)==identity){",
)
source = source.replace("CAND-R4-0002-axis6-early-exit", "CAND-R4-0003-axis6-early-exit")

needle = '  if(word_image(0,relcode,8,next)!=identity)throw std::runtime_error("surface-relator self-test failed");\n'
extra = '''  if(class2_word(0,relcode,8)!=0U)throw std::runtime_error("class2 surface-relator self-test failed");
  for(unsigned j=0;j<8;++j){
    const std::uint64_t qcode=(static_cast<std::uint64_t>(j)<<3U)|((j+4U)%8U);
    if(class2_word(0,qcode,2)!=0U)throw std::runtime_error("class2 inverse-shell self-test failed");
  }
'''
if source.count(needle) != 1:
    raise RuntimeError("candidate-0002 self-test insertion point did not match")
source = source.replace(needle, needle + extra)
(HERE / "scan_candidate_0003_axis6.cpp").write_text(source, encoding="utf-8", newline="\n")
