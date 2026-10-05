"""All C8 image groups from A5 and A6 factors with frozen parity."""

from __future__ import annotations

from typing import Iterable,Sequence

from production_code.group.a5_psl2_7_product_c8 import compose,valid_perm_maps,word_perm
from production_code.group.psl2_9_aut_c8 import IDENTITY as A6_ID,matmul,valid_maps,word_image


def actual_order(left_images,right_images)->int:
    identity=(tuple(range(5)),A6_ID,0);moves=tuple((a,b,1) for a,b in zip(left_images[:4],right_images[:4],strict=True));seen={identity};frontier=[identity]
    while frontier:
        x,y,e=frontier.pop()
        for a,b,f in moves:
            value=(compose(x,a),matmul(y,b),e^f)
            if value not in seen:seen.add(value);frontier.append(value)
    return len(seen)


def candidates(words:Iterable[Sequence[int]]):
    words=tuple(tuple(w) for w in words);left=valid_perm_maps();right=valid_maps(words);result=[]
    for aalpha,aseed,aimages in left:
        asig=tuple(word_perm(aimages,w) for w in words)
        for item in right:
            bimages=item["images"];bsig=tuple(word_image(bimages,w) for w in words);size=len({(asig[i],bsig[i],len(words[i])&1) for i in range(len(words))});order=actual_order(aimages,bimages) if size==len(words) else 0
            result.append({"a5_alpha":aalpha,"a5_seed":aseed,"a6_class":item["class_index"],"a6_seed":item["seed"],"B3_image_size":size,"actual_order":order,"survivor_in_window":size==len(words) and 2338<=order<=50000})
    return tuple(result)

