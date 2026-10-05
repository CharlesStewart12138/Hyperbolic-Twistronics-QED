"""Exact direct inner-C8 family in PSL(3,4) x C2 (order 40,320)."""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence


Q=4
IDENTITY=(1,0,0, 0,1,0, 0,0,1)
PHYSICAL_RELATOR=(0,5,2,7,4,1,6,3)
SCALARS=(1,2,3)


def add(x:int,y:int)->int: return x^y


def mul(x:int,y:int)->int:
    a,b=x&1,x>>1; c,d=y&1,y>>1
    return (a*c ^ b*d) | ((a*d ^ b*c ^ b*d)<<1)


def power(x:int,n:int)->int:
    r=1
    while n:
        if n&1:r=mul(r,x)
        x=mul(x,x); n>>=1
    return r


def inv(x:int)->int:
    if not x: raise ZeroDivisionError
    return power(x,2)


def determinant(m:Sequence[int])->int:
    a,b,c,d,e,f,g,h,i=m
    # Characteristic two turns all determinant signs positive.
    return add(add(mul(a,add(mul(e,i),mul(f,h))),mul(b,add(mul(d,i),mul(f,g)))),mul(c,add(mul(d,h),mul(e,g))))


def scalar_mul(s:int,m:Sequence[int])->tuple[int,...]: return tuple(mul(s,x) for x in m)


def canonical(m:Sequence[int])->tuple[int,...]: return min(scalar_mul(s,m) for s in SCALARS)


def matmul(x:Sequence[int],y:Sequence[int])->tuple[int,...]:
    values=[]
    for r in range(3):
        for c in range(3):
            value=0
            for k in range(3): value=add(value,mul(x[3*r+k],y[3*k+c]))
            values.append(value)
    return canonical(values)


def matinv(m:Sequence[int])->tuple[int,...]:
    a,b,c,d,e,f,g,h,i=m
    cof=(
        add(mul(e,i),mul(f,h)), add(mul(d,i),mul(f,g)), add(mul(d,h),mul(e,g)),
        add(mul(b,i),mul(c,h)), add(mul(a,i),mul(c,g)), add(mul(a,h),mul(b,g)),
        add(mul(b,f),mul(c,e)), add(mul(a,f),mul(c,d)), add(mul(a,e),mul(b,d)),
    )
    det_inverse=inv(determinant(m))
    return canonical(tuple(mul(det_inverse,cof[3*c+r]) for r in range(3) for c in range(3)))


def matrix_power(x:Sequence[int],n:int)->tuple[int,...]:
    r=IDENTITY; b=tuple(x)
    while n:
        if n&1:r=matmul(r,b)
        b=matmul(b,b);n>>=1
    return r


def conjugate(by:Sequence[int],x:Sequence[int])->tuple[int,...]: return matmul(by,matmul(x,matinv(by)))


@lru_cache(maxsize=1)
def elements()->tuple[tuple[int,...],...]:
    result={canonical(m) for m in product(range(Q),repeat=9) if determinant(m)==1}
    if len(result)!=20160: raise RuntimeError(f"PSL(3,4) order drift: {len(result)}")
    return tuple(sorted(result))


@lru_cache(maxsize=1)
def order_eight_classes()->tuple[tuple[tuple[int,...],tuple[tuple[int,...],...]],...]:
    group=elements(); remaining={x for x in group if matrix_power(x,8)==IDENTITY and matrix_power(x,4)!=IDENTITY}; classes=[]
    while remaining:
        rep=min(remaining); orbit={conjugate(g,rep) for g in group}; classes.append((rep,tuple(sorted(orbit&remaining)))); remaining-=orbit
    return tuple(classes)


def physical_images(alpha:Sequence[int],seed:Sequence[int])->tuple[tuple[int,...],...]: return tuple(conjugate(matrix_power(alpha,j),seed) for j in range(8))


def word_image(images:Sequence[Sequence[int]],word:Sequence[int])->tuple[int,...]:
    result=IDENTITY
    for digit in word:result=matmul(result,images[digit])
    return result


def relation_and_shell(alpha:Sequence[int],seed:Sequence[int])->bool:
    images=physical_images(alpha,seed)
    return len(set(images))==8 and all(images[j+4]==matinv(images[j]) for j in range(4)) and word_image(images,PHYSICAL_RELATOR)==IDENTITY


def b3_image_size(alpha:Sequence[int],seed:Sequence[int],words:Iterable[Sequence[int]])->int:
    images=physical_images(alpha,seed);return len({word_image(images,w) for w in words})


def generated_subgroup(alpha:Sequence[int],seed:Sequence[int])->frozenset[tuple[int,...]]:
    generators=physical_images(alpha,seed)[:4];seen={IDENTITY};frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for generator in generators:
            value=matmul(current,generator)
            if value not in seen:seen.add(value);frontier.append(value)
    return frozenset(seen)


def candidate_seeds(words:Iterable[Sequence[int]])->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words); result=[]
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes()):
        for seed in elements():
            if not relation_and_shell(alpha,seed):continue
            size=b3_image_size(alpha,seed,words); generated=len(generated_subgroup(alpha,seed)) if size==len(words) else 0
            result.append({"class_index":class_index,"alpha":alpha,"seed":seed,"B3_image_size":size,"generated_order":generated,"B3_survivor":size==len(words) and generated==20160})
    return tuple(result)

