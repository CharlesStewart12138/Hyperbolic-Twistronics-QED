"""Exact inner-C8 search in Aut(PSL(3,3))=PSL(3,3):2 with internal parity."""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable,Sequence

from production_code.group.psl3_3_c8_family import IDENTITY as BASE_ID,PHYSICAL_RELATOR,elements as base_elements,matinv,matmul


Element=tuple[tuple[int,...],int]
IDENTITY:Element=(BASE_ID,0)


def transpose(m:Sequence[int])->tuple[int,...]:return tuple(m[3*c+r] for r in range(3) for c in range(3))


def outer(m:Sequence[int])->tuple[int,...]:return transpose(matinv(m))


def multiply(left:Element,right:Element)->Element:
    a,e=left;b,f=right
    return matmul(a,outer(b) if e else b),e^f


def inverse(value:Element)->Element:
    a,e=value
    return (outer(matinv(a)) if e else matinv(a),e)


def power(value:Element,n:int)->Element:
    result=IDENTITY;base=value
    while n:
        if n&1:result=multiply(result,base)
        base=multiply(base,base);n>>=1
    return result


def conjugate(by:Element,value:Element)->Element:return multiply(by,multiply(value,inverse(by)))


@lru_cache(maxsize=1)
def elements()->tuple[Element,...]:return tuple((g,e) for g in base_elements() for e in (0,1))


@lru_cache(maxsize=1)
def order_eight_classes()->tuple[tuple[Element,tuple[Element,...]],...]:
    group=elements();remaining={x for x in group if power(x,8)==IDENTITY and power(x,4)!=IDENTITY};classes=[]
    while remaining:
        rep=min(remaining);orbit={conjugate(g,rep) for g in group};classes.append((rep,tuple(sorted(orbit&remaining))));remaining-=orbit
    return tuple(classes)


def physical_images(alpha:Element,seed:Element)->tuple[Element,...]:return tuple(conjugate(power(alpha,j),seed) for j in range(8))


def word_image(images:Sequence[Element],word:Sequence[int])->Element:
    result=IDENTITY
    for digit in word:result=multiply(result,images[digit])
    return result


def relation_and_shell(alpha:Element,seed:Element)->bool:
    images=physical_images(alpha,seed)
    return len(set(images))==8 and all(images[j+4]==inverse(images[j]) for j in range(4)) and word_image(images,PHYSICAL_RELATOR)==IDENTITY


def b3_image_size(alpha:Element,seed:Element,words:Iterable[Sequence[int]])->int:
    images=physical_images(alpha,seed);return len({word_image(images,w) for w in words})


def generated_order(alpha:Element,seed:Element,cutoff:int=11232)->int:
    moves=physical_images(alpha,seed)[:4];seen={IDENTITY};frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for move in moves:
            value=multiply(current,move)
            if value not in seen:
                seen.add(value)
                if len(seen)>cutoff:return cutoff+1
                frontier.append(value)
    return len(seen)


def candidate_seeds(words:Iterable[Sequence[int]])->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words);result=[]
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes()):
        for base in base_elements():
            seed=(base,1)
            if not relation_and_shell(alpha,seed):continue
            size=b3_image_size(alpha,seed,words);generated=generated_order(alpha,seed) if size==len(words) else 0
            result.append({"class_index":class_index,"alpha":alpha,"seed":seed,"B3_image_size":size,"generated_order":generated,"B3_survivor":size==len(words) and generated==11232})
    return tuple(result)

