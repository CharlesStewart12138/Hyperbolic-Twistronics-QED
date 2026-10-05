"""Search [weight-2,weight-2] commutators for an exact short gamma_4 witness."""
from itertools import product
from production_code.group.injectivity_bridge import _geometry_from_matrix
from production_code.group.universal_cover import matrix_from_word

def iw(w): return tuple((x+4)%8 for x in reversed(w))
def red(w):
    s=[]
    for x in w:
        if s and s[-1]==(x+4)%8: s.pop()
        else: s.append(x)
    return tuple(s)
def co(x,y): return red(x+y+iw(x)+iw(y))
def main():
    hits=[]
    for i,j,k,l in product(range(8),repeat=4):
        w=co(co((i,),(j,)),co((k,),(l,)))
        if not w: continue
        mat=matrix_from_word(tuple(f"g{x}" for x in w))
        based,tr,_,ht=_geometry_from_matrix(mat)
        if tr<6:hits.append((tr,based,w,tuple(ht)))
    hits.sort(key=lambda x:(x[0],len(x[2]),x[2]))
    print(f"hits={len(hits)}")
    for tr,b,w,ht in hits[:40]:print(f"ell={tr:.15f} based={b:.15f} depth={len(w)} word={' '.join(f'g{x}' for x in w)} half_trace={ht}")
if __name__=='__main__':main()
