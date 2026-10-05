"""Exact products of compact C8-equivariant proper subgroups of S8."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Iterable, Sequence


IDENTITY=tuple(range(8))
CYCLE=tuple((i+1)%8 for i in range(8))
RELATOR=(0,5,2,7,4,1,6,3)


def compose(left:tuple[int,...],right:tuple[int,...])->tuple[int,...]:return tuple(left[right[i]] for i in range(8))


def inverse(value:tuple[int,...])->tuple[int,...]:
    result=[0]*8
    for source,target in enumerate(value):result[target]=source
    return tuple(result)


def power(value:tuple[int,...],n:int)->tuple[int,...]:
    result=IDENTITY;base=value
    while n:
        if n&1:result=compose(result,base)
        base=compose(base,base);n>>=1
    return result


def conjugate(by:tuple[int,...],value:tuple[int,...])->tuple[int,...]:return compose(by,compose(value,inverse(by)))


def parity(value:tuple[int,...])->int:return sum(value[i]>value[j] for i in range(8) for j in range(i+1,8))&1


def physical_images(seed:tuple[int,...])->tuple[tuple[int,...],...]:return tuple(conjugate(power(CYCLE,j),seed) for j in range(8))


def word_image(images:Sequence[tuple[int,...]],word:Sequence[int])->tuple[int,...]:
    result=IDENTITY
    for digit in word:result=compose(result,images[digit])
    return result


def generated_group(images:Sequence[tuple[int,...]])->frozenset[tuple[int,...]]:
    moves=tuple(images[:4]);seen={IDENTITY};frontier=[IDENTITY]
    while frontier:
        current=frontier.pop()
        for move in moves:
            value=compose(current,move)
            if value not in seen:seen.add(value);frontier.append(value)
    return frozenset(seen)


@dataclass(frozen=True)
class CompactMap:
    seed:tuple[int,...]
    generated_order:int

    @property
    def images(self)->tuple[tuple[int,...],...]:return physical_images(self.seed)

    def image(self,word:Sequence[int])->tuple[int,...]:return word_image(self.images,word)


def compact_maps()->tuple[CompactMap,...]:
    result=[]
    for seed in permutations(range(8)):
        if not parity(seed):continue
        images=physical_images(seed)
        if len(set(images))!=8:continue
        if not all(images[j+4]==inverse(images[j]) for j in range(4)):continue
        if word_image(images,RELATOR)!=IDENTITY:continue
        order=len(generated_group(images))
        if order in (288,336):result.append(CompactMap(seed,order))
    return tuple(result)


def kernel_orbit_representatives(maps:Iterable[CompactMap])->tuple[CompactMap,...]:
    by_seed={m.seed:m for m in maps};remaining=set(by_seed);result=[]
    while remaining:
        seed=min(remaining);orbit={conjugate(power(CYCLE,j),seed) for j in range(8)}
        result.append(by_seed[seed]);remaining-=orbit
    return tuple(result)


def paired_generated_order(left:CompactMap,right:CompactMap,cutoff:int=50000)->int:
    identity=(IDENTITY,IDENTITY);moves=tuple(zip(left.images[:4],right.images[:4],strict=True));seen={identity};frontier=[identity]
    while frontier:
        current=frontier.pop()
        for move in moves:
            value=(compose(current[0],move[0]),compose(current[1],move[1]))
            if value not in seen:
                seen.add(value)
                if len(seen)>cutoff:return cutoff+1
                frontier.append(value)
    return len(seen)


def product_candidates(words:Iterable[Sequence[int]])->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words);reps=kernel_orbit_representatives(compact_maps());result=[]
    signatures={m.seed:tuple(m.image(w) for w in words) for m in reps}
    for left,right in combinations(reps,2):
        image_size=len(set(zip(signatures[left.seed],signatures[right.seed],strict=True)))
        order=paired_generated_order(left,right) if image_size==len(words) else 0
        result.append({"left_seed":left.seed,"right_seed":right.seed,"left_order":left.generated_order,"right_order":right.generated_order,"B3_image_size":image_size,"paired_order":order,"B3_survivor_in_window":image_size==len(words) and 2338<=order<=50000})
    return tuple(result)

