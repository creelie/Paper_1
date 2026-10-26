"""check_paper.py: the finite statements of the paper, from the definitions.

  1. Lemma 2.1 and Theorem 2.2 for 5 <= m <= 9: the nonzero entries of U U^T over F_2 and of
     V V^T over F_3 are exactly the closed neighbourhoods of A_m and B_m, the ranks are at most m
     and binom(m,2), the diagonal D_m is independent in A_m x B_m (strong product), and for m <= 7
     the exact Grundy domination numbers of A_m and B_m are at most the bounds.
  2. gamma_gr(K_{2,2,2}) = 2, by trying every sequence of distinct vertices.
  3. Theorem 1.3: gamma_gr(H_N) = floor((N+1)/3) + 3 for 6 <= N <= 24, by a memoised depth-first
     search over dominated sets.
  4. Lemma 5.2: the sequences (5.3) and the two small ones are legal in H_N with the stated
     footprints, for 6 <= N <= 64.
  5. Proposition 4.1: the sequence ((j mod 3), j) is legal in K_{2,2,2} x H_N with the stated
     footprints, for 1 <= N <= 64.
  6. Example 5.3 and the numbers 1287 and 1014 quoted after Theorem 2.2.

Usage: python3 -I check_paper.py
"""
import itertools
import sys
from functools import lru_cache
from itertools import combinations
from math import comb

failures = 0


def check(cond, what):
    global failures
    if cond:
        print("ok   ", what)
    else:
        failures += 1
        print("FAIL ", what)


# ---- graphs as closed-neighbourhood bitmasks ---------------------------------------------

def closed_nbhd(n, adj):
    return [sum(1 << u for u in range(n) if u == v or adj(u, v)) for v in range(n)]


def exact_grundy(nb):
    @lru_cache(None)
    def longest(d):
        return max((1 + longest(d | v) for v in nb if d | v != d), default=0)
    return longest(0)


def legal_with_feet(nb, seq, feet):
    """seq is legal and seq[i] footprints feet[i]."""
    if len(seq) != len(feet) or len(set(seq)) != len(seq):
        return False
    dom = 0
    for v, w in zip(seq, feet):
        if not (nb[v] >> w) & 1 or (dom >> w) & 1:
            return False
        dom |= nb[v]
    return True


def h_adj(u, v):
    return abs(u - v) % 3 == 2


def H(n):
    return closed_nbhd(n, h_adj)


def oct_adj(u, v):
    return abs(u - v) != 3


OCT = closed_nbhd(6, oct_adj)


def strong_nbhd(nb1, n1, nb2, n2):
    """closed neighbourhoods of the strong product, vertex (a,b) -> a*n2+b."""
    out = []
    for a in range(n1):
        for b in range(n2):
            m = 0
            for a2 in range(n1):
                if (nb1[a] >> a2) & 1:
                    for b2 in range(n2):
                        if (nb2[b] >> b2) & 1:
                            m |= 1 << (a2 * n2 + b2)
            out.append(m)
    return out


# ---- 1. the incidence matrices ---------------------------------------------------------------

def rank_mod(rows, p):
    rows = [r[:] for r in rows]
    rank = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = next((i for i in range(rank, len(rows)) if rows[i][c] % p), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = pow(rows[rank][c], -1, p)
        rows[rank] = [(x * inv) % p for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


for m in range(5, 10):
    sets = list(combinations(range(1, m + 1), 5))
    n = len(sets)
    inter = [[len(set(S) & set(T)) for T in sets] for S in sets]
    a_nb = closed_nbhd(n, lambda u, v: inter[u][v] % 2 == 1)
    b_nb = closed_nbhd(n, lambda u, v: inter[u][v] % 3 == 2)
    U = [[1 if j in S else 0 for j in range(1, m + 1)] for S in sets]
    V = [[1 if set(P) <= set(S) else 0 for P in combinations(range(1, m + 1), 2)] for S in sets]
    UUt = [[sum(U[s][k] * U[t][k] for k in range(m)) % 2 for t in range(n)] for s in range(n)]
    VVt = [[sum(V[s][k] * V[t][k] for k in range(comb(m, 2))) % 3 for t in range(n)] for s in range(n)]
    check(all(((a_nb[s] >> t) & 1) == (UUt[s][t] != 0) for s in range(n) for t in range(n)),
          f"m={m}: support of U U^T mod 2 is the closed neighbourhoods of A_m")
    check(all(((b_nb[s] >> t) & 1) == (VVt[s][t] != 0) for s in range(n) for t in range(n)),
          f"m={m}: support of V V^T mod 3 is the closed neighbourhoods of B_m")
    ra, rb = rank_mod(UUt, 2), rank_mod(VVt, 3)
    check(ra <= m and rb <= comb(m, 2), f"m={m}: ranks {ra} <= {m} and {rb} <= {comb(m, 2)}")
    # D_m independent in the strong product: S != T adjacent in both factors is impossible
    check(all(not (((a_nb[s] >> t) & 1) and ((b_nb[s] >> t) & 1)) for s in range(n) for t in range(n) if s != t),
          f"m={m}: the diagonal D_m is independent in A_m x B_m, so gamma_gr(A_m x B_m) >= {n}")
    if m <= 7:
        ga, gb = exact_grundy(a_nb), exact_grundy(b_nb)
        check(ga <= m and gb <= comb(m, 2), f"m={m}: exact gamma_gr(A_m) = {ga}, gamma_gr(B_m) = {gb}")

check(comb(13, 5) == 1287 and 13 * comb(13, 2) == 1014, "m=13: binom(13,5) = 1287 > 13 binom(13,2) = 1014")
check(all(comb(m, 5) * 60 * m == m * comb(m, 2) * (m - 2) * (m - 3) * (m - 4) for m in range(5, 60)),
      "the ratio binom(m,5) / (m binom(m,2)) equals (m-2)(m-3)(m-4)/(60m)")

# ---- 2. the octahedron -----------------------------------------------------------------------

best = 0
for k in range(1, 7):
    for seq in itertools.permutations(range(6), k):
        dom, ok = 0, True
        for v in seq:
            if OCT[v] & ~dom == 0:
                ok = False
                break
            dom |= OCT[v]
        if ok:
            best = max(best, k)
check(best == 2, "gamma_gr(K_{2,2,2}) = 2")

# ---- 3. the formula for H_N ------------------------------------------------------------------

for N in range(6, 25):
    g = exact_grundy(H(N))
    check(g == (N + 1) // 3 + 3, f"gamma_gr(H_{N}) = {g} = floor((N+1)/3) + 3")

# ---- 4. the sequences of Lemma 5.2 -----------------------------------------------------------

def lower_sequence(q):
    a = lambda i: 3 * i
    b = lambda i: 3 * i + 1
    c = lambda i: 3 * i + 2
    if q == 2:
        return (1, 3, 5, 0, 2), (1, 5, 0, 2, 4)
    if q == 3:
        return (0, 7, 2, 4, 5, 1), (0, 7, 4, 6, 3, 1)
    seq = tuple(a(i) for i in range(q - 2)) + (b(q - 1), c(q - 3), c(0), a(q - 2), b(0))
    feet = tuple(a(i) for i in range(q - 2)) + (b(q - 1), b(q - 2), b(q - 3), a(q - 2), a(q - 1))
    return seq, feet


for N in range(6, 65):
    q = (N + 1) // 3
    seq, feet = lower_sequence(q)
    check(len(seq) == q + 3 and max(seq) < N and legal_with_feet(H(N), seq, feet),
          f"H_{N}: the sequence of Lemma 5.2 (q={q}) is legal, length {q + 3}, with the stated footprints")

# ---- 5. the product sequence of Proposition 4.1 -----------------------------------------------

for N in range(1, 65):
    nb = strong_nbhd(OCT, 6, H(N), N)
    seq = [(j % 3) * N + j for j in range(N)]            # (g_{j mod 3}, v_j), g_i = i
    feet = [(((j + 1) % 3) + 3) * N + j for j in range(N)]  # (x_{j mod 3 + 1}, v_j), x_i = i + 3
    check(legal_with_feet(nb, seq, feet), f"K_{{2,2,2}} x H_{N}: the sequence of Proposition 4.1 is legal, length {N}")

# ---- 6. Example 5.3 --------------------------------------------------------------------------

check(lower_sequence(6)[0] == (0, 3, 6, 9, 16, 11, 2, 12, 1) and exact_grundy(H(19)) == 9 and 6 * 19 == 114,
      "N=19: the sequence (0,3,6,9,16,11,2,12,1), gamma_gr(H_19) = 9 < 19/2, 114 vertices")
check(lower_sequence(7)[0] == (0, 3, 6, 9, 12, 19, 14, 2, 15, 1) and exact_grundy(H(21)) == 10 and 6 * 21 == 126,
      "N=21: the sequence (0,3,6,9,12,19,14,2,15,1), gamma_gr(H_21) = 10 < 21/2, 126 vertices")
check(exact_grundy(H(20)) == 10, "N=20: gamma_gr(H_20) = 10 = 20/2, undecided")

print(f"failures {failures}")
sys.exit(1 if failures else 0)
