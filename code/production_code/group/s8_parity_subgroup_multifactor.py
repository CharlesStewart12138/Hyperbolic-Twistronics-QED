"""All products of the eight compact degree-eight kernel orbits."""

from __future__ import annotations

from itertools import combinations
from typing import Iterable,Sequence

from production_code.group.s8_parity_subgroup_product_family import compact_maps,kernel_orbit_representatives
from production_code.group.s8_subgroup_c8_product_family import IDENTITY,compose


def generated_order(factors,cutoff:int=50000)->int:
    identity=(tuple(IDENTITY for _ in factors),0)
    moves=tuple((tuple(f.images[j] for f in factors),1) for j in range(4))
    seen={identity};frontier=[identity]
    while frontier:
        permutations,parity=frontier.pop()
        for move_permutations,move_parity in moves:
            value=(tuple(compose(x,y) for x,y in zip(permutations,move_permutations,strict=True)),parity^move_parity)
            if value not in seen:
                seen.add(value)
                if len(seen)>cutoff:return cutoff+1
                frontier.append(value)
    return len(seen)


def all_products(words:Iterable[Sequence[int]])->tuple[dict[str,object],...]:
    words=tuple(tuple(w) for w in words);reps=kernel_orbit_representatives(compact_maps())
    signatures={f.seed:tuple(f.image(w)[0] for w in words) for f in reps};results=[]
    for number in range(2,len(reps)+1):
        for indices in combinations(range(len(reps)),number):
            factors=tuple(reps[i] for i in indices)
            image_size=len({(tuple(signatures[f.seed][word_index] for f in factors),len(words[word_index])&1) for word_index in range(len(words))})
            order=generated_order(factors) if image_size==len(words) else 0
            results.append({"factor_indices":indices,"factor_seeds":[f.seed for f in factors],"factor_orders":[f.order for f in factors],"B3_image_size":image_size,"image_order":order,"B3_survivor_in_window":image_size==len(words) and 2338<=order<=50000})
    return tuple(results)

