# Independent checks for "Grundy Domination of Graph Products and Minimum Rank".
# Julia 1.11, standard library only.  Run:  julia checks.jl
using LinearAlgebra
const FAIL = Ref(0); const PASS = Ref(0)
check(c, msg) = (c ? (PASS[] += 1) : (FAIL[] += 1; println("FAIL: ", msg)))

subsets(n, k) = k == 0 ? [Int[]] : [vcat(s, j) for s in subsets(n, k-1) for j in (isempty(s) ? 1 : last(s)+1):n]

# graphs as Vector{UInt128} of neighbourhood masks (closed or open)
function nbmasks(n, adj; closed=true)
    m = zeros(UInt128, n)
    for u in 1:n, v in 1:n
        if (closed && u == v) || (u != v && adj(u, v)); m[u] |= UInt128(1) << (v-1); end
    end
    m
end
function grundy(m::Vector{UInt128})
    memo = Dict{UInt128,Int}()
    f(D) = get!(memo, D) do
        b = 0
        for r in m
            (r & ~D) != 0 && (b = max(b, 1 + f(D | r)))
        end
        b
    end
    f(UInt128(0))
end
cyc(n) = (u, v) -> mod(u - v, n) in (1, n-1)
strong(n1, a1, n2, a2) = (u, v) -> begin
    g, h = divrem(u-1, n2); g2, h2 = divrem(v-1, n2)
    (g == g2 || a1(g+1, g2+1)) && (h == h2 || a2(h+1, h2+1))
end
direct(n1, a1, n2, a2) = (u, v) -> begin
    g, h = divrem(u-1, n2); g2, h2 = divrem(v-1, n2)
    g != g2 && h != h2 && a1(g+1, g2+1) && a2(h+1, h2+1)
end

# 1. tori
for k in 3:6, l in k:6
    check(grundy(nbmasks(k*l, strong(k, cyc(k), l, cyc(l)))) == (k-2)*(l-2), "torus $k $l")
end
# 2. Petersen and Petersen x C5
P = subsets(5, 2); padj = (u, v) -> isempty(intersect(P[u], P[v]))
check(grundy(nbmasks(10, padj)) == 5, "Petersen")
check(grundy(nbmasks(50, strong(10, padj, 5, cyc(5)))) == 15, "Petersen x C5")
# 3. H_N and the octahedron
hadj(u, v) = mod(abs(u - v), 3) == 1
oadj(u, v) = u != v && mod(u - v, 3) != 0
for N in 4:20
    check(grundy(nbmasks(N, hadj)) == div(N, 3) + 2, "H_$N")
end
for N in 4:12
    g = grundy(nbmasks(6N, strong(6, oadj, N, hadj)))
    check(g == max(N, 2*(div(N, 3) + 2)), "octahedron x H_$N = $g")
end
# 4. total: cycles and direct products
for n in 3:14
    check(grundy(nbmasks(n, cyc(n); closed=false)) == 2*div(n-1, 2), "total C_$n")
end
tc(n) = 2*div(n-1, 2)
for (a, b) in [(3,3), (3,5), (4,5), (5,5), (3,7), (6,5)]
    check(grundy(nbmasks(a*b, direct(a, cyc(a), b, cyc(b)); closed=false)) == tc(a)*tc(b), "direct C$a C$b")
end
# 5. ranks over F_p
function rankp(A::Matrix{Int}, p)
    M = mod.(A, p); r = 0; nr, nc = size(M)
    for c in 1:nc
        piv = findfirst(i -> M[i, c] != 0, r+1:nr); piv === nothing && continue
        piv += r; r += 1; M[[r, piv], :] = M[[piv, r], :]
        inv = invmod(M[r, c], p); M[r, :] = mod.(M[r, :] .* inv, p)
        for i in 1:nr
            (i != r && M[i, c] != 0) && (M[i, :] = mod.(M[i, :] .- M[i, c] .* M[r, :], p))
        end
    end
    r
end
kn(n) = (S = subsets(n, 2); [isempty(intersect(a, b)) ? 1 : 0 for a in S, b in S])
for n in 6:2:14
    check(rankp(kn(n) + I, 2) == n - 1, "Kneser F2 $n")
end
for (n, p) in [(7,3), (9,5), (10,3), (11,7), (13,3), (14,5)]
    check(rankp(kn(n) - I, p) == n - 1, "Kneser F$p $n")
end
for n in 6:12
    check(grundy(nbmasks(binomial(n,2), (u,v) -> kn(n)[u,v] == 1)) == n - 1, "gamma K($n,2)")
end
# 6. Theorem unbounded: the matrices UU^T over F2 and VV^T over F3
for m in 7:10
    S = subsets(m, 5)
    A = [length(intersect(a, b)) for a in S, b in S]
    check(all(mod(A[i,j], 2) == 1 ? (i == j || isodd(A[i,j])) : (i != j && iseven(A[i,j])) for i in axes(A,1), j in axes(A,2)), "A_m pattern $m")
    check(rankp(mod.(A, 2), 2) <= m, "rank A_$m")
    B = [binomial(A[i,j], 2) for i in axes(A,1), j in axes(A,2)]
    check(all((mod(B[i,j], 3) != 0) == (i == j || A[i,j] == 2) for i in axes(A,1), j in axes(A,2)), "B_m pattern $m")
    check(rankp(B, 3) <= binomial(m, 2), "rank B_$m")
end
# 7. projective planes over prime fields: p-rank and Grundy coverings
function pgp(p)
    pts = Tuple{Int,Int,Int}[]
    for a in 0:p-1, b in 0:p-1, c in 0:p-1
        v = (a, b, c); v == (0,0,0) && continue
        i = findfirst(!=(0), v); inv = invmod(v[i], p)
        w = mod.(v .* inv, p); w in pts || push!(pts, w)
    end
    [mod(sum(x .* l), p) == 0 ? 1 : 0 for x in pts, l in pts]
end
for (p, r, c) in [(2,4,4), (3,7,7), (5,16,15)]
    N = pgp(p)
    check(rankp(N, p) == r, "p-rank $p")
    rows = [sum(UInt128(N[i,j]) << (j-1) for j in axes(N,2)) for i in axes(N,1)]
    check(grundy(rows) == c, "c($p)")
end
check(rankp(pgp(7), 7) == 29, "7-rank")
# 8. Hermitian and signed cycle matrices
for n in 3:30
    A = zeros(ComplexF64, n, n)
    for t in 1:n-1; A[t,t+1] = A[t+1,t] = 1; end
    w = isodd(n) ? im : (mod(n, 4) == 0 ? 1.0 : -1.0)
    A[n,1] = w; A[1,n] = conj(w)
    ev = eigvals(Hermitian(A))
    check(count(x -> abs(x) > 1e-9, ev) == 2*div(n-1, 2), "Hermitian cycle $n")
end
for k in 3:30
    A = [mod(i - j, k) in (1, k-1) ? 1.0 : 0.0 for i in 1:k, j in 1:k] - 2cos(2pi/k) * I
    check(rank(Symmetric(A); atol=1e-9) == k - 2, "circulant C_$k")
end
println("passed $(PASS[]), failed $(FAIL[])")
exit(FAIL[] == 0 ? 0 : 1)
