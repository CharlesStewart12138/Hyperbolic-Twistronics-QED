"""Exhaustively audit all C8-stable class-2 quotient branches of dimension <=2."""

from __future__ import annotations

import csv
import importlib
import json
from pathlib import Path


p2=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")
d0=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")
ROOT=Path(__file__).resolve().parents[2]; R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4"
LEDGER=R4/"09_CEGAR"/"WITNESS_LEDGER.tsv"; OUT=R4/"05_P_QUOTIENT"/"C8_D1_D2_BRANCH_AUDIT.json"
CURRENT_RAW=tuple("g3 g6 g0 g6 g3 g0 g3 g6 g3 g5 g0 g2 g5 g0".split())


def main():
    with LEDGER.open(encoding="utf-8",newline="") as handle: rows=list(csv.DictReader(handle,delimiter="\t"))
    words=[tuple(row["Canonical word"].split()) for row in rows if row["Type"]=="D_global(6a_B)"]
    words.append(d0.canonical_c8_inverse_word(CURRENT_RAW))
    images=[p2.word_full_geometric(word) for word in words]
    if any(v!=0 for v,z in images): raise RuntimeError(f"global witnesses should be central in class2: {images}")
    zvalues=[z for v,z in images]; columns=p2.phi_central_columns()
    d1=[]; d1_cover=[]
    for row in range(1,512):
        rs=(row,)
        if p2.stable(rs,columns):
            d1.append(rs)
            if all(p2.quotient_central(z,rs)!=0 for z in zvalues): d1_cover.append(rs)
    d2=[]; d2_cover=[]
    for rs in p2.canonical_row_spaces(2):
        if p2.stable(rs,columns):
            d2.append(rs)
            if all(p2.quotient_central(z,rs)!=0 for z in zvalues): d2_cover.append(rs)
    OUT.write_text(json.dumps({
        "schema_version":"1.0","scope":"all C8-stable dual row spaces of dimensions one and two in the certified nine-dimensional class-2 central layer",
        "global_witness_words":[list(word) for word in words],"global_witness_central_images":zvalues,
        "dimension_one":{"stable_count":len(d1),"stable_spaces":[list(x) for x in d1],"simultaneous_cover_count":len(d1_cover),"simultaneous_cover_spaces":[list(x) for x in d1_cover]},
        "dimension_two":{"stable_count":len(d2),"stable_spaces":[list(x) for x in d2],"simultaneous_cover_count":len(d2_cover),"simultaneous_cover_spaces":[list(x) for x in d2_cover]},
        "classification":"D2_BRANCH_AVAILABLE" if d2_cover else "NO_D1_OR_D2_SIMULTANEOUS_SEPARATOR",
        "scope_limit":"does not exclude higher p-class, other primes, nonnilpotent extensions, or unrelated finite quotients",
    },indent=2)+"\n",encoding="utf-8")


if __name__=="__main__": main()
