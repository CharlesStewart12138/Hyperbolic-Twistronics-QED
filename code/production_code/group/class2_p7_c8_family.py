"""Proof-complete class-two exponent-seven C8 quotient family of order 33,614."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator, Sequence

import numpy as np
from numpy.typing import NDArray


P=7
HALF=4
EXTERIOR_PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
PHYSICAL_RELATOR=(0,5,2,7,4,1,6,3)


def rotation_matrix(p:int=P)->NDArray[np.int64]:
    result=np.zeros((4,4),dtype=np.int64)
    for i in range(3):result[i+1,i]=1
    result[0,3]=-1
    return result%p


def exterior_vector(left:Sequence[int],right:Sequence[int],p:int=P)->NDArray[np.int64]:
    return np.array([(left[i]*right[j]-left[j]*right[i])%p for i,j in EXTERIOR_PAIRS],dtype=np.int64)


def exterior_rotation(p:int=P)->NDArray[np.int64]:
    rotation=rotation_matrix(p);result=np.zeros((6,6),dtype=np.int64)
    for column,(i,j) in enumerate(EXTERIOR_PAIRS):result[:,column]=exterior_vector(rotation[:,i],rotation[:,j],p)
    return result


def physical_vectors(p:int=P)->tuple[NDArray[np.int64],...]:
    rotation=rotation_matrix(p);v=np.array((1,0,0,0),dtype=np.int64);result=[]
    for _ in range(8):result.append(v);v=rotation@v%p
    return tuple(result)


def relator_exterior_vector(p:int=P)->NDArray[np.int64]:
    vectors=physical_vectors(p);result=np.zeros(6,dtype=np.int64)
    for i in range(len(PHYSICAL_RELATOR)):
        for j in range(i+1,len(PHYSICAL_RELATOR)):
            result+=exterior_vector(vectors[PHYSICAL_RELATOR[i]],vectors[PHYSICAL_RELATOR[j]],p)
    return result%p


def projective_rows(dimension:int=6,p:int=P)->Iterator[tuple[int,...]]:
    for pivot in range(dimension):
        for tail in product(range(p),repeat=dimension-pivot-1):
            yield (0,)*pivot+(1,)+tuple(tail)


@dataclass(frozen=True)
class Candidate:
    ordinal:int
    row:tuple[int,...]
    central_eigenvalue:int

    @property
    def order(self)->int:return 2*P**5

    def image(self,word:Sequence[int])->tuple[int,...]:
        vectors=physical_vectors();homology=np.zeros(4,dtype=np.int64);central=np.zeros(6,dtype=np.int64);parity=0
        for digit in word:
            vector=vectors[digit];central=(central+HALF*exterior_vector(homology,vector))%P;homology=(homology+vector)%P;parity^=1
        projected=int(np.dot(np.asarray(self.row,dtype=np.int64),central)%P)
        return (parity,*map(int,homology),projected)


def invariant_relator_quotients()->tuple[Candidate,...]:
    action=exterior_rotation();relator=relator_exterior_vector();result=[]
    for row_tuple in projective_rows():
        row=np.asarray(row_tuple,dtype=np.int64)
        if int(row@relator%P):continue
        transformed=row@action%P;pivot=int(np.flatnonzero(row)[0]);eigenvalue=int(transformed[pivot])
        if eigenvalue and np.array_equal(transformed,eigenvalue*row%P):result.append(Candidate(len(result),row_tuple,eigenvalue))
    return tuple(result)


def b3_survivors(words:Iterable[Sequence[int]])->tuple[Candidate,...]:
    words=tuple(tuple(word) for word in words);return tuple(c for c in invariant_relator_quotients() if len({c.image(w) for w in words})==len(words))

