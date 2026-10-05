"""Exact inner-C8 searches in the three PSL(3,4):2 internal-parity extensions."""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable,Sequence

from production_code.group.psl3_4_c8_family import IDENTITY as BASE_ID,PHYSICAL_RELATOR,elements as base_elements,matinv,matmul
from production_code.group.psl3_4_outer_c8_family import frobenius_matrix,graph_matrix


Element=tuple[tuple[int,...],int]
IDENTITY:Element=(BASE_ID,0)
OUTER_TYPES=("field","graph","field_graph")


def outer(m:Sequence[int],kind:str)->tuple[int,...]:
    if kind=="field":return frobenius_matrix(m)
    if kind=="graph":return graph_matrix(m)
    if kind=="field_graph":return frobenius_matrix(graph_matrix(m))
    raise ValueError(kind)


def multiply(left:Element,right:Element,kind:str)->Element:
    a,e=left;b,f=right
    return matmul(a,outer(b,kind) if e else b),e^f


def inverse(value:Element,kind:str)->Element:
    a,e=value
    return (outer(matinv(a),kind) if e else matinv(a),e)


def power(value:Element,n:int,kind:str)->Element:
    result=IDENTITY;base=value
    while n:
        if n&1:result=multiply(result,base,kind)
        base=multiply(base,base,kind);n>>=1
    return result


def conjugate(by:Element,value:Element,kind:str)->Element:return multiply(by,multiply(value,inverse(by,kind),kind),kind)


@lru_cache(maxsize=3)
def order_eight_classes(kind:str)->tuple[tuple[Element,tuple[Element,...]],...]:
    group=tuple((g,e) for g in base_elements() for e in (0,1));remaining={x for x in group if power(x,8,kind)==IDENTITY and power(x,4,kind)!=IDENTITY};classes=[]
    while remaining:
        rep=min(remaining);orbit={conjugate(g,rep,kind) for g in group};classes.append((rep,tuple(sorted(orbit&remaining))));remaining-=orbit
    return tuple(classes)


def physical_images(alpha:Element,seed:Element,kind:str)->tuple[Element,...]:return tuple(conjugate(power(alpha,j,kind),seed,kind) for j in range(8))


def word_image(images:Sequence[Element],word:Sequence[int],kind:str)->Element:
    result=IDENTITY
    for digit in word:result=multiply(result,images[digit],kind)
    return result


def relation_and_shell(alpha:Element,seed:Element,kind:str)->bool:
    images=physical_images(alpha,seed,kind)
    return len(set(images))==8 and all(images[j+4]==inverse(images[j],kind) for j in range(4)) and word_image(images,PHYSICAL_RELATOR,kind)==IDENTITY


def b3_image_size(alpha:Element,seed:Element,words:Iterable[Sequence[int]],kind:str)->int:
    images=physical_images(alpha,seed,kind);return len({word_image(images,w,kind) for w in words})


def generated_order(alpha:Element,seed:Element,kind:str,cutoff:int=40320)->int:
    moves=physical_images(alpha,seed,kind)[:4];seen={IDENTITY};frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for move in moves:
            value=multiply(current,move,kind)
            if value not in seen:
                seen.add(value)
                if len(seen)>cutoff:return cutoff+1
                frontier.append(value)
    return len(seen)


def candidate_seeds(words:Iterable[Sequence[int]],kind:str)->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words);result=[]
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes(kind)):
        for base in base_elements():
            seed=(base,1)
            if not relation_and_shell(alpha,seed,kind):continue
            size=b3_image_size(alpha,seed,words,kind);generated=generated_order(alpha,seed,kind) if size==len(words) else 0
            result.append({"outer_type":kind,"class_index":class_index,"alpha":alpha,"seed":seed,"B3_image_size":size,"generated_order":generated,"B3_survivor":size==len(words) and generated==40320})
    return tuple(result)

