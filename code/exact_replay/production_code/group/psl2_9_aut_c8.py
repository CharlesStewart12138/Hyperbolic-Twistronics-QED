"""Exact order-eight Aut(A6)=PΓL(2,9) action on A6=PSL(2,9)."""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from typing import Iterable,Sequence

from production_code.group.psu3_3_c8_family import Q,add,frobenius,inv,mul,neg,sub


IDENTITY=(1,0,0,1)
RELATOR=(0,5,2,7,4,1,6,3)
Auto=tuple[tuple[int,int,int,int],int]
AUTO_ID:Auto=(IDENTITY,0)


def determinant(m:Sequence[int])->int:
    a,b,c,d=m;return sub(mul(a,d),mul(b,c))


def canonical(m:Sequence[int])->tuple[int,int,int,int]:
    values=tuple(m);pivot=next(x for x in values if x);scale=inv(pivot)
    return tuple(mul(scale,x) for x in values)  # type: ignore[return-value]


def matmul(x:Sequence[int],y:Sequence[int])->tuple[int,int,int,int]:
    a,b,c,d=x;e,f,g,h=y
    return canonical((add(mul(a,e),mul(b,g)),add(mul(a,f),mul(b,h)),add(mul(c,e),mul(d,g)),add(mul(c,f),mul(d,h))))


def matinv(m:Sequence[int])->tuple[int,int,int,int]:
    a,b,c,d=m;return canonical((d,neg(b),neg(c),a))


def matrix_frobenius(m:Sequence[int])->tuple[int,int,int,int]:return canonical(tuple(frobenius(x) for x in m))


def pow_field(x:int,n:int)->int:
    result=1
    while n:
        if n&1:result=mul(result,x)
        x=mul(x,x);n>>=1
    return result


def is_square(x:int)->bool:return x!=0 and pow_field(x,4)==1


@lru_cache(maxsize=1)
def pgl_elements()->tuple[tuple[int,int,int,int],...]:
    values={canonical(m) for m in product(range(Q),repeat=4) if determinant(m)!=0}
    if len(values)!=720:raise RuntimeError("PGL2(9) order drift")
    return tuple(sorted(values))


@lru_cache(maxsize=1)
def psl_elements()->tuple[tuple[int,int,int,int],...]:
    values=tuple(x for x in pgl_elements() if is_square(determinant(x)))
    if len(values)!=360:raise RuntimeError("PSL2(9) order drift")
    return values


def auto_mul(left:Auto,right:Auto)->Auto:
    a,e=left;b,f=right
    return matmul(a,matrix_frobenius(b) if e else b),e^f


def auto_inv(value:Auto)->Auto:
    a,e=value;return (matrix_frobenius(matinv(a)) if e else matinv(a),e)


def auto_power(value:Auto,n:int)->Auto:
    result=AUTO_ID;base=value
    while n:
        if n&1:result=auto_mul(result,base)
        base=auto_mul(base,base);n>>=1
    return result


def auto_conjugate(by:Auto,value:Auto)->Auto:return auto_mul(by,auto_mul(value,auto_inv(by)))


def auto_apply(value:Auto,m:Sequence[int])->tuple[int,int,int,int]:
    a,e=value;x=matrix_frobenius(m) if e else canonical(m);return matmul(a,matmul(x,matinv(a)))


@lru_cache(maxsize=1)
def order_eight_classes()->tuple[tuple[Auto,tuple[Auto,...]],...]:
    group=tuple((a,e) for a in pgl_elements() for e in (0,1));remaining={x for x in group if auto_power(x,8)==AUTO_ID and auto_power(x,4)!=AUTO_ID};classes=[]
    while remaining:
        rep=min(remaining);orbit={auto_conjugate(g,rep) for g in group};classes.append((rep,tuple(sorted(orbit&remaining))));remaining-=orbit
    return tuple(classes)


def physical_images(alpha:Auto,seed:Sequence[int])->tuple[tuple[int,int,int,int],...]:
    result=[];current=canonical(seed)
    for _ in range(8):result.append(current);current=auto_apply(alpha,current)
    return tuple(result)


def word_image(images,word):
    result=IDENTITY
    for digit in word:result=matmul(result,images[digit])
    return result


def valid_maps(words:Iterable[Sequence[int]]):
    words=tuple(tuple(w) for w in words);result=[]
    for class_index,(alpha,_orbit) in enumerate(order_eight_classes()):
        for seed in psl_elements():
            images=physical_images(alpha,seed)
            if len(set(images))!=8 or not all(images[j+4]==matinv(images[j]) for j in range(4)) or word_image(images,RELATOR)!=IDENTITY:continue
            size=len({word_image(images,w) for w in words});result.append({"class_index":class_index,"alpha":alpha,"seed":seed,"images":images,"B3_image_size":size})
    return tuple(result)


def generated_order(images)->int:
    seen={IDENTITY};frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for move in images[:4]:
            value=matmul(current,move)
            if value not in seen:seen.add(value);frontier.append(value)
    return len(seen)

