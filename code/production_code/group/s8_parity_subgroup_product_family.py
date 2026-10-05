"""Products of all compact S8-orbit quotient images with frozen external parity."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Iterable, Sequence

from production_code.group.s8_subgroup_c8_product_family import (
    CYCLE, IDENTITY, RELATOR, compose, conjugate, inverse, physical_images,
    power, word_image,
)


Pair=tuple[tuple[int,...],int]
PAIR_ID=(IDENTITY,0)


def pair_mul(left:Pair,right:Pair)->Pair:return compose(left[0],right[0]),left[1]^right[1]


def generated_pair_group(images:Sequence[tuple[int,...]],cutoff:int|None=None)->frozenset[Pair]|int:
    moves=tuple((image,1) for image in images[:4]);seen={PAIR_ID};frontier=[PAIR_ID]
    while frontier:
        current=frontier.pop()
        for move in moves:
            value=pair_mul(current,move)
            if value not in seen:
                seen.add(value)
                if cutoff is not None and len(seen)>cutoff:return cutoff+1
                frontier.append(value)
    return frozenset(seen)


@dataclass(frozen=True)
class QuotientMap:
    seed:tuple[int,...]
    order:int

    @property
    def images(self)->tuple[tuple[int,...],...]:return physical_images(self.seed)

    def image(self,word:Sequence[int])->Pair:return word_image(self.images,word),len(word)&1


def compact_maps()->tuple[QuotientMap,...]:
    result=[]
    for seed in permutations(range(8)):
        images=physical_images(seed)
        if len(set(images))!=8:continue
        if not all(images[j+4]==inverse(images[j]) for j in range(4)):continue
        if word_image(images,RELATOR)!=IDENTITY:continue
        group=generated_pair_group(images);assert isinstance(group,frozenset);order=len(group)
        if order in (288,336):result.append(QuotientMap(seed,order))
    return tuple(result)


def kernel_orbit_representatives(maps:Iterable[QuotientMap])->tuple[QuotientMap,...]:
    by_seed={m.seed:m for m in maps};remaining=set(by_seed);result=[]
    while remaining:
        seed=min(remaining);orbit={conjugate(power(CYCLE,j),seed) for j in range(8)}
        result.append(by_seed[seed]);remaining-=orbit
    return tuple(result)


def paired_order(left:QuotientMap,right:QuotientMap,cutoff:int=50000)->int:
    identity=(IDENTITY,IDENTITY,0);moves=tuple((a,b,1) for a,b in zip(left.images[:4],right.images[:4],strict=True));seen={identity};frontier=[identity]
    while frontier:
        x,y,e=frontier.pop()
        for a,b,f in moves:
            value=(compose(x,a),compose(y,b),e^f)
            if value not in seen:
                seen.add(value)
                if len(seen)>cutoff:return cutoff+1
                frontier.append(value)
    return len(seen)


def product_candidates(words:Iterable[Sequence[int]])->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words);reps=kernel_orbit_representatives(compact_maps());signatures={m.seed:tuple(m.image(w) for w in words) for m in reps};result=[]
    for left,right in combinations(reps,2):
        size=len(set(zip(signatures[left.seed],signatures[right.seed],strict=True)));order=paired_order(left,right) if size==len(words) else 0
        result.append({"left_seed":left.seed,"right_seed":right.seed,"left_order":left.order,"right_order":right.order,"B3_image_size":size,"paired_order":order,"B3_survivor_in_window":size==len(words) and 2338<=order<=50000})
    return tuple(result)

