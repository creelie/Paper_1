"""Independent finite checks; the two universal arguments are written in the paper."""
from functools import lru_cache
from itertools import combinations
from math import comb
from fractions import Fraction
from pathlib import Path
import json


def neighbourhoods(n):
    return tuple(sum(1 << j for j in range(n) if i == j or abs(i-j) % 3 == 2) for i in range(n))


def exact_grundy(n):
    nb = neighbourhoods(n)
    @lru_cache(None)
    def longest(d):
        return max((1 + longest(d | v) for v in nb if d | v != d), default=0)
    return longest(0)


def lower_witness(n):
    if n < 6:
        raise ValueError('the formula requires n >= 6')
    q = (n+1)//3
    if q == 2:
        return (1,3,5,0,2), (1,5,0,2,4)
    if q == 3:
        return (0,7,2,4,5,1), (0,7,4,6,3,1)
    start = tuple(3*i for i in range(q-2))
    return start+(3*q-2,3*q-7,2,3*q-6,1), start+(3*q-2,3*q-5,3*q-8,3*q-6,3*q-3)


def legal_feet(n, seq, feet):
    cl = lambda u,v: u == v or abs(u-v) % 3 == 2
    return len(seq) == len(feet) and len(set(seq)) == len(seq) and all(
        0 <= v < n and 0 <= w < n and cl(v,w) and not any(cl(u,w) for u in seq[:i])
        for i,(v,w) in enumerate(zip(seq,feet)))


def independent_prefixes(q):
    for bits in range(1 << q):
        left = [i for i in range(q) if bits >> i & 1]
        start = max(left, default=-1)+1
        for tail in range(1 << (q-start)):
            yield left, [start+j for j in range(q-start) if tail >> j & 1]


def structural_counts(q):
    cuts = edges = 0
    for left,right in independent_prefixes(q):
        dominated = set()
        for i in left:
            dominated |= {i} | {q+j for j in range(i+1)}
        for j in right:
            dominated |= {q+j} | set(range(j,q))
        for k in range(q):
            w = set(range(k,q)) | {q+j for j in range(k+1)}
            images = [i if i >= k else q+i for i in left]
            images += [q+j if j <= k else j for j in right]
            assert len(set(images)) == len(left)+len(right)
            assert set(images) <= dominated & w
            assert len(left)+len(right)+len(w-dominated) <= q+1
            cuts += 1
        if right:
            for i in range(min(right),q):
                after = dominated | {i} | {q+j for j in range(i+1)}
                assert len(left)+len(right)+1+2*q-len(after) <= q+1
                edges += 1
        if left:
            for j in range(max(left)+1):
                after = dominated | {q+j} | set(range(j,q))
                assert len(left)+len(right)+1+2*q-len(after) <= q+1
                edges += 1
    return cuts,edges


def rank_mod(matrix,p):
    a = [row[:] for row in matrix]
    r = 0
    for c in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(r,len(a)) if a[i][c] % p),None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        inv = pow(a[r][c],-1,p)
        a[r] = [x*inv % p for x in a[r]]
        for i in range(r+1,len(a)):
            factor = a[i][c] % p
            if factor:
                a[i] = [(x-factor*y) % p for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def two_fields_audit():
    for t in range(6):
        assert bool(t % 2) == (t % 2 == 1)
        assert bool(comb(t,2) % 3) == (t % 3 == 2)
        assert bool(t % 2 and comb(t,2) % 3) == (t == 5)
    checks, cases = 0, []
    for m in range(5,11):
        sets = [frozenset(s) for s in combinations(range(m),5)]
        pairs = list(combinations(range(m),2))
        a,b = [],[]
        for s in sets:
            ar,br = [],[]
            for t in sets:
                x = sum(i in s and i in t for i in range(m)) % 2
                y = sum(i in s and j in s and i in t and j in t for i,j in pairs) % 3
                k = len(s & t)
                assert bool(x) == (s == t or k in (1,3))
                assert bool(y) == (s == t or k == 2)
                assert bool(x and y) == (s == t)
                ar.append(x);br.append(y);checks += 1
            a.append(ar);b.append(br)
        ra,rb = rank_mod(a,2),rank_mod(b,3)
        assert ra <= m and rb <= comb(m,2)
        cases.append({'m':m,'vertices':len(sets),'rank_F2':ra,'rank_F3':rb})
    ratios = {}
    for m in (5,12,13,20,100,1000):
        ratio = Fraction(comb(m,5),m*comb(m,2))
        assert ratio == Fraction((m-2)*(m-3)*(m-4),60*m)
        ratios[m] = str(ratio)
    return {'ordered_pairs':checks,'ranks':cases,'ratio_lower_bounds':ratios}


def audit():
    values = {n:exact_grundy(n) for n in range(1,31)}
    assert all(v == (n+1)//3+3 for n,v in values.items() if n >= 6)
    for q in range(2,301):
        for n in range(max(6,3*q-1),3*q+2):
            seq,feet = lower_witness(n)
            assert len(seq) == q+3 and legal_feet(n,seq,feet)
    counts = [structural_counts(q) for q in range(1,11)]
    assert values[5] == 3 and values[5] != (5+1)//3+3
    return {'exact_values':values,'witness_q_max':300,
            'cut_injections':sum(x for x,y in counts),'first_edges':sum(y for x,y in counts),
            'two_fields':two_fields_audit(),
            'scope':'Finite checks; universal claims rely on the written proofs, not enumeration.'}


if __name__ == '__main__':
    result = audit()
    print(json.dumps(result,indent=2))
    Path(__file__).with_name('revision_results.json').write_text(json.dumps(result,indent=2)+'\n')
