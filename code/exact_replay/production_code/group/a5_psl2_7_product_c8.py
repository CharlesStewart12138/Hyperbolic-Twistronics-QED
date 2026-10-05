"""Exact C8 search in (A5 x PSL(2,7)) x C2, order 20,160."""

from __future__ import annotations

from itertools import permutations
from typing import Iterable,Sequence

from production_code.group.compact_pgl2_prime_search import PGL2


RELATOR=(0,5,2,7,4,1,6,3)


def compose(left:tuple[int,...],right:tuple[int,...])->tuple[int,...]:return tuple(left[right[i]] for i in range(len(left)))


def inverse(value:tuple[int,...])->tuple[int,...]:
    result=[0]*len(value)
    for i,j in enumerate(value):result[j]=i
    return tuple(result)


def power(value:tuple[int,...],n:int)->tuple[int,...]:
    result=tuple(range(len(value)));base=value
    while n:
        if n&1:result=compose(result,base)
        base=compose(base,base);n>>=1
    return result


def conjugate(by:tuple[int,...],value:tuple[int,...])->tuple[int,...]:return compose(by,compose(value,inverse(by)))


def parity(value:tuple[int,...])->int:return sum(value[i]>value[j] for i in range(len(value)) for j in range(i+1,len(value)))&1


def a5_elements()->tuple[tuple[int,...],...]:return tuple(x for x in permutations(range(5)) if parity(x)==0)


def s5_alpha_classes()->tuple[tuple[int,...],...]:
    group=tuple(permutations(range(5)));eligible={x for x in group if power(x,8)==tuple(range(5))};result=[]
    while eligible:
        rep=min(eligible);orbit={conjugate(g,rep) for g in group};result.append(rep);eligible-=orbit
    return tuple(result)


def factor_images_perm(alpha,seed):return tuple(conjugate(power(alpha,j),seed) for j in range(8))


def word_perm(images,word):
    result=tuple(range(len(images[0])))
    for digit in word:result=compose(result,images[digit])
    return result


def valid_perm_maps()->tuple[tuple[tuple[int,...],tuple[int,...],tuple[tuple[int,...],...]],...]:
    result=[]
    for alpha in s5_alpha_classes():
        for seed in a5_elements():
            images=factor_images_perm(alpha,seed)
            if all(images[j+4]==inverse(images[j]) for j in range(4)) and word_perm(images,RELATOR)==tuple(range(5)):
                result.append((alpha,seed,images))
    return tuple(result)


def psl7_alpha_classes(pgl:PGL2):
    group=pgl.elements();remaining={x for x in group if pgl.power(x,8)==pgl.identity and pgl.power(x,4)!=pgl.identity};result=[]
    while remaining:
        rep=min(remaining);orbit={pgl.conjugate(g,rep) for g in group};result.append(rep);remaining-=orbit
    return tuple(result)


def factor_images_psl(pgl,alpha,seed):return tuple(pgl.conjugate(pgl.power(alpha,j),seed) for j in range(8))


def word_psl(pgl,images,word):
    result=pgl.identity
    for digit in word:result=pgl.multiply(result,images[digit])
    return result


def valid_psl_maps():
    pgl=PGL2(7);psl=tuple(x for x in pgl.elements() if not pgl.odd(x));result=[]
    for alpha in psl7_alpha_classes(pgl):
        for seed in psl:
            images=factor_images_psl(pgl,alpha,seed)
            if all(images[j+4]==pgl.inverse(images[j]) for j in range(4)) and word_psl(pgl,images,RELATOR)==pgl.identity:
                result.append((alpha,seed,images))
    return pgl,tuple(result)


def generated_perm(images)->int:
    identity=tuple(range(len(images[0])));seen={identity};frontier=[identity]
    while frontier:
        current=frontier.pop()
        for move in images[:4]:
            value=compose(current,move)
            if value not in seen:seen.add(value);frontier.append(value)
    return len(seen)


def product_candidates(words:Iterable[Sequence[int]]):
    words=tuple(tuple(w) for w in words);left=valid_perm_maps();pgl,right=valid_psl_maps();result=[]
    for aalpha,aseed,aimages in left:
        if generated_perm(aimages)!=60:continue
        asig=tuple(word_perm(aimages,w) for w in words)
        for balpha,bseed,bimages in right:
            if pgl.generated_order(bimages)!=168:continue
            bsig=tuple(word_psl(pgl,bimages,w) for w in words)
            size=len(set(zip(asig,bsig,strict=True)))
            result.append({"a5_alpha":aalpha,"a5_seed":aseed,"psl_alpha":balpha,"psl_seed":bseed,"B3_image_size":size,"B3_survivor":size==len(words)})
    return tuple(result)

