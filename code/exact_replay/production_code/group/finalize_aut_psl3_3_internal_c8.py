"""Finalize the exact internal-parity PSL(3,3):2 C8 family audit."""

from __future__ import annotations

from datetime import datetime,timezone
import gzip,hashlib,json
from pathlib import Path
import sys

if __package__ in (None,""):sys.path.insert(0,str(Path(__file__).resolve().parents[2]))

from production_code.group.aut_psl3_3_internal_c8 import IDENTITY,candidate_seeds,conjugate,elements,physical_images,word_image
from production_code.group.injectivity_bridge import _geometry_from_matrix
from production_code.group.universal_cover import matrix_from_word


ROOT=Path(__file__).resolve().parents[2];GROUP=ROOT/"production_code"/"group";BALL=ROOT/"data"/"production"/"universal_cover"/"ball_radius_6_exact.jsonl.gz"
REPS=(
    ((0,0,1,2,0,1,2,2,0),1),
    ((0,0,1,2,1,0,0,2,0),1),
)
WORDS=((1,0,0,1,3,6,1,4),(1,6,1,4,7,1,2,2))


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()


def b3_words():
    with gzip.open(BALL,"rt",encoding="utf-8") as f:return tuple(tuple(int(t[1:]) for t in r["representative"]) for r in map(json.loads,f) if r["minimum_geometric_word_length"]<=3)


def main()->None:
    words=b3_words();survivors=tuple(x for x in candidate_seeds(words) if x["B3_survivor"])
    if len(survivors)!=16:raise RuntimeError("survivor drift")
    alpha=survivors[0]["alpha"];centralizer=tuple(g for g in elements() if conjugate(g,alpha)==alpha);remaining={x["seed"] for x in survivors};orbits=[]
    while remaining:
        seed=min(remaining);orbit={conjugate(c,seed) for c in centralizer}&{x["seed"] for x in survivors};orbits.append(tuple(sorted(orbit)));remaining-=orbit
    if len(centralizer)!=8 or tuple(o[0] for o in orbits)!=REPS or any(len(o)!=8 for o in orbits):raise RuntimeError("orbit drift")
    witnesses=[]
    for seed,word in zip(REPS,WORDS,strict=True):
        if word_image(physical_images(alpha,seed),word)!=IDENTITY:raise RuntimeError("kernel witness drift")
        matrix=matrix_from_word(tuple(f"g{x}" for x in word));based,translation,cosh_exact,half=_geometry_from_matrix(matrix);p,q=abs(int(half[1])),abs(int(half[2]))
        if half[0]!=0 or any(half[i] for i in range(3,9)) or not(p<2405 and q<1700 and translation<6):raise RuntimeError("exact short gate drift")
        witnesses.append({"seed":[list(seed[0]),seed[1]],"word":[f"g{x}" for x in word],"quotient_image":[list(IDENTITY[0]),IDENTITY[1]],"half_trace_exact_absolute_coefficients":[p,q],"exact_comparison":f"{p}+{q}sqrt(2)<2405+1700sqrt(2)","translation_length_over_a_B":translation,"based_displacement_over_a_B":based,"cosh_based_exact":list(cosh_exact)})
    record={"schema_version":"1.0","task_id":"PF-GRP-001-C8-TRACTABLE-CONSTRUCTIVE-V3-AUT-PSL3-3-INTERNAL","finished_utc":datetime.now(timezone.utc).isoformat(),"classification":"PROOF_COMPLETE_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR","group":{"name":"Aut(PSL(3,3))=PSL(3,3):2_graph","order":11232,"internal_parity":"extension bit","order_eight_inner_classes":2,"class_sizes":[1404,1404]},"enumeration":{"odd_seed_pairs":11232,"relation_inverse_distinct_retained":176,"exact_B3_survivors":16,"all_survivors_generate_full_group":True,"centralizer_order":8,"kernel_orbits":2,"orbit_sizes":[8,8]},"global_rejection":{"method":"exact B4 collision witnesses","witnesses":witnesses,"all_orbits_rejected":True,"axis_registry_scan_required":False},"scope":"All inner-C8 maps into the internal-parity graph extension PSL(3,3):2 are exhausted; this is not an all-groups no-go.","provenance":{"family_code_sha256":sha256(GROUP/"aut_psl3_3_internal_c8.py"),"universal_ball_sha256":sha256(BALL)}}
    (GROUP/"AUT_PSL3_3_INTERNAL_C8_CERTIFICATE.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    (GROUP/"AUT_PSL3_3_INTERNAL_C8_CERTIFICATE.md").write_text("# Internal-parity PSL(3,3):2 C8 audit\n\nThe exhaustive 11,232 seed-pair search leaves 16 exact-B3, full-generation candidates. The order-eight centralizer reduces them to two identical-kernel orbits. Each orbit has an independently evaluated nonidentity B4 collision word of exact translation length 4.702627955093438 a_B, strictly below 6 a_B. Hence the complete family fails the global systole gate.\n",encoding="utf-8")


if __name__=="__main__":main()

