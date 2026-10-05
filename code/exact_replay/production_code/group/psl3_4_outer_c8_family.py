"""Exact outer-automorphism C8 families in PSL(3,4) x C2."""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence

from production_code.group.psl3_4_c8_family import (
    IDENTITY, PHYSICAL_RELATOR, Q, add, canonical, determinant, elements,
    matinv, matmul, mul,
)


Auto = tuple[tuple[int,...],int,int]
AUTO_ID: Auto=(IDENTITY,0,0)


def frobenius_matrix(m:Sequence[int])->tuple[int,...]: return canonical(tuple(mul(x,x) for x in m))


def transpose(m:Sequence[int])->tuple[int,...]: return tuple(m[3*c+r] for r in range(3) for c in range(3))


def graph_matrix(m:Sequence[int])->tuple[int,...]: return canonical(transpose(matinv(m)))


def outer_on_conjugator(m:Sequence[int],field:int,graph:int)->tuple[int,...]:
    value=graph_matrix(m) if graph else canonical(m)
    return frobenius_matrix(value) if field else value


def auto_multiply(left:Auto,right:Auto)->Auto:
    a,e,f=left;b,g,h=right
    return (matmul(a,outer_on_conjugator(b,e,f)),e^g,f^h)


def auto_inverse(value:Auto)->Auto:
    a,e,f=value
    return (outer_on_conjugator(matinv(a),e,f),e,f)


def auto_power(value:Auto,n:int)->Auto:
    result=AUTO_ID;base=value
    while n:
        if n&1:result=auto_multiply(result,base)
        base=auto_multiply(base,base);n>>=1
    return result


def auto_conjugate(by:Auto,value:Auto)->Auto: return auto_multiply(by,auto_multiply(value,auto_inverse(by)))


def auto_apply(value:Auto,m:Sequence[int])->tuple[int,...]:
    a,e,f=value; x=graph_matrix(m) if f else canonical(m); x=frobenius_matrix(x) if e else x
    return matmul(a,matmul(x,matinv(a)))


@lru_cache(maxsize=1)
def pgl_elements()->tuple[tuple[int,...],...]:
    values={canonical(m) for m in product(range(Q),repeat=9) if determinant(m)!=0}
    if len(values)!=60480:raise RuntimeError(f"PGL(3,4) order drift: {len(values)}")
    return tuple(sorted(values))


@lru_cache(maxsize=1)
def order_eight_classes()->tuple[tuple[Auto,tuple[Auto,...]],...]:
    pgl=pgl_elements()
    remaining={(a,e,f) for a in pgl for e,f in ((0,1),(1,0),(1,1)) if auto_power((a,e,f),8)==AUTO_ID and auto_power((a,e,f),4)!=AUTO_ID}
    classes=[]; all_aut=tuple((a,e,f) for a in pgl for e in (0,1) for f in (0,1))
    while remaining:
        rep=min(remaining);orbit={auto_conjugate(beta,rep) for beta in all_aut};classes.append((rep,tuple(sorted(orbit&remaining))));remaining-=orbit
    return tuple(classes)


def physical_images(alpha:Auto,seed:Sequence[int])->tuple[tuple[int,...],...]:
    result=[];current=canonical(seed)
    for _ in range(8):result.append(current);current=auto_apply(alpha,current)
    return tuple(result)


def word_image(images:Sequence[Sequence[int]],word:Sequence[int])->tuple[int,...]:
    result=IDENTITY
    for digit in word:result=matmul(result,images[digit])
    return result


def relation_and_shell(alpha:Auto,seed:Sequence[int])->bool:
    images=physical_images(alpha,seed)
    return len(set(images))==8 and all(images[j+4]==matinv(images[j]) for j in range(4)) and word_image(images,PHYSICAL_RELATOR)==IDENTITY


def b3_image_size(alpha:Auto,seed:Sequence[int],words:Iterable[Sequence[int]])->int:
    images=physical_images(alpha,seed);return len({word_image(images,w) for w in words})


def generated_subgroup(alpha:Auto,seed:Sequence[int])->frozenset[tuple[int,...]]:
    generators=physical_images(alpha,seed)[:4];seen={IDENTITY};frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for generator in generators:
            value=matmul(current,generator)
            if value not in seen:seen.add(value);frontier.append(value)
    return frozenset(seen)


def candidate_seeds(words:Iterable[Sequence[int]])->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words);result=[]
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes()):
        for seed in elements():
            if not relation_and_shell(alpha,seed):continue
            size=b3_image_size(alpha,seed,words);generated=len(generated_subgroup(alpha,seed)) if size==len(words) else 0
            result.append({"class_index":class_index,"alpha":alpha,"seed":seed,"B3_image_size":size,"generated_order":generated,"B3_survivor":size==len(words) and generated==20160})
    return tuple(result)

