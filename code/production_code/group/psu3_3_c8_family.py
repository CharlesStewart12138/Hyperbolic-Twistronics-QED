"""Proof-complete inner-C8 family in PSU(3,3) x C2.

Because gcd(3,3+1)=1, PSU(3,3)=SU(3,3).  F9 is encoded as
``a+b*u -> a+3*b`` with ``u^2=2`` and Frobenius ``x -> x^3``.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence


P = 3
Q = 9
IDENTITY = (1,0,0, 0,1,0, 0,0,1)
PHYSICAL_RELATOR = (0,5,2,7,4,1,6,3)


def add(x: int, y: int) -> int:
    return ((x%3+y%3)%3)+3*((x//3+y//3)%3)


def neg(x: int) -> int:
    return ((-x)%3)+3*((-(x//3))%3)


def sub(x: int, y: int) -> int:
    return add(x,neg(y))


def mul(x: int, y: int) -> int:
    a,b=x%3,x//3; c,d=y%3,y//3
    return ((a*c+2*b*d)%3)+3*((a*d+b*c)%3)


def power(x: int, exponent: int) -> int:
    result=1
    while exponent:
        if exponent&1: result=mul(result,x)
        x=mul(x,x); exponent>>=1
    return result


def inv(x: int) -> int:
    if x==0: raise ZeroDivisionError
    return power(x,Q-2)


def frobenius(x: int) -> int:
    return power(x,3)


def inner(v: Sequence[int], w: Sequence[int]) -> int:
    result=0
    for x,y in zip(v,w,strict=True): result=add(result,mul(frobenius(x),y))
    return result


def determinant(m: Sequence[int]) -> int:
    a,b,c,d,e,f,g,h,i=m
    return add(sub(mul(a,sub(mul(e,i),mul(f,h))),mul(b,sub(mul(d,i),mul(f,g)))),mul(c,sub(mul(d,h),mul(e,g))))


def matmul(x: Sequence[int], y: Sequence[int]) -> tuple[int,...]:
    result=[]
    for r in range(3):
        for c in range(3):
            value=0
            for k in range(3): value=add(value,mul(x[3*r+k],y[3*k+c]))
            result.append(value)
    return tuple(result)


def matinv(m: Sequence[int]) -> tuple[int,...]:
    # Unitary inverse is conjugate transpose.
    return tuple(frobenius(m[3*c+r]) for r in range(3) for c in range(3))


def matrix_power(x: Sequence[int], exponent: int) -> tuple[int,...]:
    result=IDENTITY; base=tuple(x)
    while exponent:
        if exponent&1: result=matmul(result,base)
        base=matmul(base,base); exponent>>=1
    return result


def conjugate(by: Sequence[int], value: Sequence[int]) -> tuple[int,...]:
    return matmul(by,matmul(value,matinv(by)))


@lru_cache(maxsize=1)
def norm_one_vectors() -> tuple[tuple[int,int,int],...]:
    return tuple(v for v in product(range(Q),repeat=3) if inner(v,v)==1)


@lru_cache(maxsize=1)
def elements() -> tuple[tuple[int,...],...]:
    vectors=norm_one_vectors(); result=[]
    for first in vectors:
        seconds=[v for v in vectors if inner(first,v)==0]
        for second in seconds:
            for third in vectors:
                if inner(first,third)==0 and inner(second,third)==0:
                    matrix=tuple(first[r] if c==0 else second[r] if c==1 else third[r] for r in range(3) for c in range(3))
                    if determinant(matrix)==1: result.append(matrix)
    unique=tuple(sorted(set(result)))
    if len(unique)!=6048: raise RuntimeError(f"PSU(3,3) order drift: {len(unique)}")
    return unique


@lru_cache(maxsize=1)
def order_eight_classes() -> tuple[tuple[tuple[int,...],tuple[tuple[int,...],...]],...]:
    group=elements()
    remaining={x for x in group if matrix_power(x,8)==IDENTITY and matrix_power(x,4)!=IDENTITY}
    classes=[]
    while remaining:
        representative=min(remaining)
        orbit={conjugate(g,representative) for g in group}
        classes.append((representative,tuple(sorted(orbit&remaining))))
        remaining-=orbit
    return tuple(classes)


def physical_images(alpha: Sequence[int],seed: Sequence[int]) -> tuple[tuple[int,...],...]:
    return tuple(conjugate(matrix_power(alpha,j),seed) for j in range(8))


def word_image(images: Sequence[Sequence[int]],word: Sequence[int]) -> tuple[int,...]:
    result=IDENTITY
    for digit in word: result=matmul(result,images[digit])
    return result


def relation_and_shell(alpha: Sequence[int],seed: Sequence[int]) -> bool:
    images=physical_images(alpha,seed)
    return len(set(images))==8 and all(images[j+4]==matinv(images[j]) for j in range(4)) and word_image(images,PHYSICAL_RELATOR)==IDENTITY


def b3_image_size(alpha: Sequence[int],seed: Sequence[int],words: Iterable[Sequence[int]]) -> int:
    images=physical_images(alpha,seed)
    return len({word_image(images,word) for word in words})


def generated_subgroup(alpha: Sequence[int],seed: Sequence[int]) -> frozenset[tuple[int,...]]:
    generators=physical_images(alpha,seed)[:4]; seen={IDENTITY}; frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for generator in generators:
            value=matmul(current,generator)
            if value not in seen: seen.add(value); frontier.append(value)
    return frozenset(seen)


def candidate_seeds(words: Iterable[Sequence[int]]) -> tuple[dict[str,object],...]:
    words=tuple(tuple(word) for word in words); result=[]
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes()):
        for seed in elements():
            if not relation_and_shell(alpha,seed): continue
            size=b3_image_size(alpha,seed,words); generated=len(generated_subgroup(alpha,seed))
            result.append({"class_index":class_index,"alpha":alpha,"seed":seed,"B3_image_size":size,"generated_order":generated,"B3_survivor":size==len(words) and generated==6048})
    return tuple(result)

