"""check_paper.py: the finite statements of the paper, from the definitions.

  1. Lemma 2.1 and Theorem 1.4 on small graphs: for every graph on at most 5 vertices, gamma_gr is
     at most the rank of a matrix over F_5 with the closed neighbourhoods as its support, and the
     Kronecker product of two such matrices has the support of the strong product; Example 2.2 over
     F_p with p = 1 (mod a) in place of C.
  2. Theorem 3.1 for 5 <= m <= 9: the nonzero entries of U U^T over F_2 and of V V^T over F_3 are
     exactly the closed neighbourhoods of A_m and B_m, the ranks are at most m and binom(m,2), the
     diagonal D_m is independent in A_m x B_m (strong product), and for m <= 7 the exact Grundy
     domination numbers of A_m and B_m are at most the bounds.
  3. gamma_gr(K_{2,2,2}) = 2, by trying every sequence of distinct vertices.
  4. Theorem 1.3: gamma_gr(H^1_N) = floor(N/3) + 2 for 4 <= N <= 27 and gamma_gr(H^2_N) =
     floor((N+1)/3) + 3 for 6 <= N <= 27, by a memoised depth-first search over dominated sets;
     the hypotheses (6.1) and (6.2) of Lemma 6.1 in H^1_{3q+2} and H^2_{3q+1} for q <= 20.
  5. Lemmas 6.3 and 6.4: the sequences are legal in H^r_N with the stated footprints, N <= 64.
  6. Proposition 5.1: the sequence (g_{t(j)}, j) is legal in K_{2,2,2} x H^r_N with the stated
     footprints, for 1 <= N <= 64 and r = 1, 2.
  7. Example 6.5 and the numbers 1287 and 1014 quoted after Theorem 3.1.

Usage: python3 -I check_paper.py
"""
import itertools
import random
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


def H(n, r=2):
    return closed_nbhd(n, lambda u, v: abs(u - v) % 3 == r)


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


# ---- 1. Lemma 2.1, Theorem 1.4 and Example 2.2 ------------------------------------------------

rng = random.Random(1)


def support_matrix(nb, n, p):
    return [[rng.randrange(1, p) if (nb[u] >> v) & 1 else 0 for v in range(n)] for u in range(n)]


P5 = 5
small = []
for n in range(1, 6):
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        E = {pairs[i] for i in range(len(pairs)) if mask >> i & 1}
        small.append((n, closed_nbhd(n, lambda u, v: (min(u, v), max(u, v)) in E)))
ok = True
for n, nb in small:
    g = exact_grundy(nb)
    for _ in range(3):
        if g > rank_mod(support_matrix(nb, n, P5), P5):
            ok = False
check(ok, f"Lemma 2.1: gamma_gr <= rank for all {len(small)} labelled graphs on <= 5 vertices, random F_5 matrices")
ok = True
for _ in range(200):
    (n1, nb1), (n2, nb2) = rng.choice(small), rng.choice(small)
    M1, M2 = support_matrix(nb1, n1, P5), support_matrix(nb2, n2, P5)
    nbp = strong_nbhd(nb1, n1, nb2, n2)
    K = [[M1[a][a2] * M2[b][b2] % P5 for a2 in range(n1) for b2 in range(n2)] for a in range(n1) for b in range(n2)]
    if any(((nbp[i] >> j) & 1) != (K[i][j] != 0) for i in range(n1 * n2) for j in range(n1 * n2)):
        ok = False
    if rank_mod(K, P5) != rank_mod(M1, P5) * rank_mod(M2, P5):
        ok = False
check(ok, "Theorem 1.4: the Kronecker product has the support of the strong product and multiplicative rank (200 pairs)")
ok = True
for a in range(1, 7):
    p = next(p for p in range(a + 1, 1000) if p % a == 1 % a and all(p % d for d in range(2, p)))
    zeta = next(z for z in range(1, p) if pow(z, a, p) == 1 and all(pow(z, e, p) != 1 for e in range(1, a)))
    for b in range(1, a + 1):
        Z = [[pow(zeta, k * j, p) for j in range(b)] for k in range(a)]
        Zs = [[pow(zeta, (p - 2) * k * j, p) for k in range(a)] for j in range(b)]   # zeta^{-kj}
        M = [[a % p if i == k else 0 for k in range(a)] + Z[i] for i in range(a)] + \
            [Zs[j] + [1 if j == l else 0 for l in range(b)] for j in range(b)]
        nb = closed_nbhd(a + b, lambda u, v: (u < a) != (v < a))
        if any(((nb[i] >> j) & 1) != (M[i][j] != 0) for i in range(a + b) for j in range(a + b)):
            ok = False
        if rank_mod(M, p) != a or exact_grundy(nb) != a:
            ok = False
check(ok, "Example 2.2: for 1 <= b <= a <= 6 the matrix has the support of K_{a,b} and rank a = gamma_gr(K_{a,b}) (over F_p, p = 1 mod a)")

# ---- 2. the incidence matrices ---------------------------------------------------------------

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

# ---- 3. the octahedron -----------------------------------------------------------------------

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

# ---- 4. the formulas for H^1_N and H^2_N ---------------------------------------------------

for N in range(4, 28):
    g = exact_grundy(H(N, 1))
    check(g == N // 3 + 2, f"gamma_gr(H^1_{N}) = {g} = floor(N/3) + 2")
for N in range(6, 28):
    g = exact_grundy(H(N, 2))
    check(g == (N + 1) // 3 + 3, f"gamma_gr(H^2_{N}) = {g} = floor((N+1)/3) + 3")


def half_graph_hypotheses(n, r, q, eps):
    """Lemma 6.1 for z = 0 in H^r_n: the non-neighbours are X_i = 3(i+1), Y_j, and (6.1), (6.2) hold."""
    nb = H(n, r)
    X = [3 * (i + 1) for i in range(q)]
    Y = [3 * j + (2 if r == 1 else 1) for j in range(q)]
    if sorted(X + Y) != [v for v in range(n) if not (nb[0] >> v) & 1]:
        return False
    if any(nb[X[i]] >> X[k] & 1 or nb[Y[i]] >> Y[k] & 1 for i in range(q) for k in range(q) if i != k):
        return False
    if any(bool(nb[X[i]] >> Y[j] & 1) != (i >= j) for i in range(q) for j in range(q)):
        return False
    for w in range(1, n):
        if (nb[0] >> w) & 1:
            ks = [k for k in range(q + 1)
                  if all(bool(nb[w] >> X[i] & 1) == (i < k) for i in range(q))
                  and all(bool(nb[w] >> Y[j] & 1) == (j >= k + eps) for j in range(q))]
            if not ks:
                return False
    # translation modulo n is an automorphism
    return all(((nb[u] >> v) & 1) == ((nb[(u + 1) % n] >> ((v + 1) % n)) & 1) for u in range(n) for v in range(n))


for q in range(1, 21):
    check(half_graph_hypotheses(3 * q + 2, 1, q, 0) and half_graph_hypotheses(3 * q + 1, 2, q, 1),
          f"q={q}: Lemma 6.1 applies to H^1_{3 * q + 2} (eps = 0) and H^2_{3 * q + 1} (eps = 1), circulant")

# ---- 5. the sequences of Lemmas 6.3 and 6.4 ---------------------------------------------------

def lower_sequence_1(q):
    a = lambda i: 3 * i
    b = lambda i: 3 * i + 1
    c = lambda i: 3 * i + 2
    if q == 1:
        return (0, 1, 2), (0, 2, 3), 4
    if q == 2:
        return (0, 5, 1, 2), (0, 5, 2, 3), 6
    seq = (a(0), a(1)) + tuple(c(m) for m in range(q - 1)) + (b(0),)
    feet = (a(0), c(0), a(2)) + tuple(c(m) for m in range(1, q - 1)) + (c(q - 1),)
    return seq, feet, 3 * q


for N in range(4, 65):
    q = N // 3
    seq, feet, host = lower_sequence_1(q)
    check(len(seq) == q + 2 and host <= N and max(seq + feet) < host and legal_with_feet(H(host, 1), seq, feet)
          and legal_with_feet(H(N, 1), seq, feet),
          f"H^1_{N}: the sequence of Lemma 6.3 (q={q}) is legal, length {q + 2}, with the stated footprints")


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
    check(len(seq) == q + 3 and max(seq + feet) < N and legal_with_feet(H(N, 2), seq, feet),
          f"H^2_{N}: the sequence of Lemma 6.4 (q={q}) is legal, length {q + 3}, with the stated footprints")

# ---- 6. the product sequence of Proposition 5.1 -----------------------------------------------

for r in (1, 2):
    for N in range(1, 65):
        nb = strong_nbhd(OCT, 6, H(N, r), N)
        t = [(-j) % 3 if r == 1 else j % 3 for j in range(N)]
        seq = [t[j] * N + j for j in range(N)]                    # (g_{t(j)}, j), g_i = i
        feet = [(((t[j] + 1) % 3) + 3) * N + j for j in range(N)]  # (x_{t(j)+1}, j), x_i = i + 3
        check(legal_with_feet(nb, seq, feet),
              f"K_{{2,2,2}} x H^{r}_{N}: the sequence of Proposition 5.1 is legal, length {N}")

# ---- 7. Example 6.5 --------------------------------------------------------------------------

check(lower_sequence_1(3)[0] == (0, 3, 2, 5, 1) and exact_grundy(H(11, 1)) == 5 and 6 * 11 == 66,
      "N=11, r=1: the sequence (0,3,2,5,1), gamma_gr(H^1_11) = 5 < 11/2, 66 vertices")
check(lower_sequence(6)[0] == (0, 3, 6, 9, 16, 11, 2, 12, 1) and exact_grundy(H(19)) == 9 and 6 * 19 == 114,
      "N=19, r=2: the sequence (0,3,6,9,16,11,2,12,1), gamma_gr(H^2_19) = 9 < 19/2, 114 vertices")
check(exact_grundy(H(12, 1)) == 6 and exact_grundy(H(20)) == 10, "N=12, r=1 and N=20, r=2: ratio exactly 2, undecided")
fails1 = [N for N in range(4, 200) if N > 2 * (N // 3 + 2)]
fails2 = [N for N in range(6, 200) if N > 2 * ((N + 1) // 3 + 3)]
check(fails1 == [11, 13, 14] + list(range(15, 200)) and fails2 == [19] + list(range(21, 200)),
      "Theorem 1.3: N > 2 gamma_gr(H^r_N) exactly for N = 11, 13, 14, >= 15 (r=1) and N = 19, >= 21 (r=2)")

print(f"failures {failures}")
sys.exit(1 if failures else 0)
