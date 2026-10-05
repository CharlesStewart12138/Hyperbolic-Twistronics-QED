"""Deterministically produce scanner v2 from the preserved failed v1 source."""

from pathlib import Path


HERE = Path(__file__).resolve().parent
source = (HERE / "scan_candidate_0001_axis6.cpp").read_text(encoding="utf-8")
source = source.replace("A multiply(A left,A right){", "A amultiply(A left,A right){")
source = source.replace("A generator(int index){", "A agenerator(int index){")
source = source.replace(
    "result[index][code]=encode(multiply(value,generator(index)))",
    "result[index][code]=encode(amultiply(value,agenerator(index)))",
)
needle = "Field real_part(Field value){"
helper = """Matrix matrix_from_raw(const std::array<char,kGeoRecordBytes>& raw){
  std::string bytes(raw.data(),raw.size());
  std::istringstream in(bytes,std::ios::binary);
  return geo_read_record(in).key;
}

"""
if needle not in source:
    raise RuntimeError("scanner repair insertion point missing")
source = source.replace(needle, helper + needle, 1)
(HERE / "scan_candidate_0001_axis6_v2.cpp").write_text(source, encoding="utf-8", newline="\n")
