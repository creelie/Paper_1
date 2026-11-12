# Recomputes the finite statements of the paper with exact arithmetic.
# Usage: julia kneser_checks.jl <data-directory>
const DATA = length(ARGS) > 0 ? ARGS[1] : joinpath(@__DIR__, "..", "data")

ksubsets(n, r) = [m for m in 0:(1<<n)-1 if count_ones(m) == r]

# rank over F_p by Gaussian elimination on UInt8 entries
function rank_mod(A::Matrix{Int}, p::Int)
    M = UInt8.(mod.(A, p)); nr, nc = size(M); r = 0
    inv = zeros(Int, p); for a in 1:p-1, b in 1:p-1; (a*b) % p == 1 && (inv[a] = b); end
    for c in 1:nc
        piv = 0
        for i in r+1:nr; if M[i, c] != 0; piv = i; break; end; end
        piv == 0 && continue
        r += 1
        if piv != r; M[r, :], M[piv, :] = M[piv, :], M[r, :]; end
        s = inv[M[r, c]]
        @inbounds for j in c:nc; M[r, j] = UInt8((Int(M[r, j]) * s) % p); end
        @inbounds for i in r+1:nr
            f = Int(M[i, c]); f == 0 && continue
            for j in c:nc
                M[i, j] = UInt8(mod(Int(M[i, j]) - f * Int(M[r, j]), p))
            end
        end
    end
    return r
end

# I + c*D for the Kneser graph K(n,r)
function kneser_matrix(n, r, c)
    V = ksubsets(n, r); N = length(V); A = zeros(Int, N, N)
    for i in 1:N, j in 1:N
        A[i, j] = i == j ? 1 : ((V[i] & V[j]) == 0 ? c : 0)
    end
    return A
end

# matrix of Theorem 3.2: binom(|S cap T|-1, r-1) mod p, with binom(-1,k)=(-1)^k
gbin(t, k) = t >= 1 ? binomial(t - 1, k) : (-1)^k
function thm_matrix(n, r)
    V = ksubsets(n, r); N = length(V)
    [gbin(count_ones(V[i] & V[j]), r - 1) for i in 1:N, j in 1:N]
end

function legal(n, r, seq)
    V = ksubsets(n, r); dom = Set{Int}()
    length(unique(seq)) == length(seq) || return false
    for v in seq
        count_ones(v) == r || return false
        N = Set([w for w in V if w & v == 0]); push!(N, v)
        isempty(setdiff(N, dom)) && return false
        union!(dom, N)
    end
    return true
end

function readseq(f)
    t = split(read(f, String)); L = parse(Int, t[1]); parse.(Int, t[2:1+L])
end

println("== Theorem 3.2: rank of M_{n,r} over F_p equals binom(n-1,r-1)")
for (n, r, p) in [(9,3,3),(10,3,2),(11,3,5),(12,4,2),(13,4,5),(16,4,2),(15,5,5)]
    rk = rank_mod(thm_matrix(n, r), p); a = binomial(n - 1, r - 1)
    println("K($n,$r) p=$p rank=$rk alpha=$a ", rk == a ? "OK" : "FAIL")
    @assert rk == a
end

println("== Table 6.1: ranks of I + cD")
for (n, r, p, c, want) in [(7,3,3,1,20),(8,3,2,1,22),(9,4,3,2,77),(10,4,2,1,93),(11,4,3,2,121),
                           (11,5,3,1,296),(12,5,2,1,384),(13,5,3,1,507),(14,4,3,2,287),(14,5,2,1,716)]
    rk = rank_mod(kneser_matrix(n, r, c), p)
    println("K($n,$r) F_$p c=$c rank=$rk ", rk == want ? "OK" : "FAIL"); @assert rk == want
end

println("== Theorem 3.8: legal sequences")
for (n, r, f, L) in [(8,3,"seq_8_3.txt",22),(9,4,"seq_9_4.txt",77),(10,4,"seq_10_4.txt",93),
                     (11,4,"seq_11_4.txt",121),(11,5,"seq_11_5.txt",296)]
    s = readseq(joinpath(DATA, f)); ok = length(s) == L && legal(n, r, s)
    println("K($n,$r) length $(length(s)) legal=$ok"); @assert ok
end

println("== Example 4.6: G_2(m), G_3(m) on 5-subsets")
for m in 8:14
    V = ksubsets(m, 5); N = length(V)
    A2 = [count_ones(V[i] & V[j]) % 2 for i in 1:N, j in 1:N]
    A3 = [(count_ones(V[i] & V[j]) % 3 == 2) ? 1 : 0 for i in 1:N, j in 1:N]
    common = any(i != j && A2[i, j] != 0 && A3[i, j] != 0 for i in 1:N, j in 1:N)
    r2 = rank_mod(A2, 2); r3 = rank_mod(A3, 3)
    println("m=$m N=$N r2=$r2 r3=$r3 product=$(r2*r3) common_edge=$common")
    @assert !common && r2 == m && r3 == binomial(m, 2)
end
println("all checks passed")
