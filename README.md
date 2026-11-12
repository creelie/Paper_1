# Grundy Domination of Kneser Graphs and Graph Products

Deep Bhattacharjee. Release v3.0.0.

The paper [`paper/GrundyPaper.pdf`](paper/GrundyPaper.pdf) bounds the Grundy domination number
of a graph by the minimum rank of its closed-neighbourhood pattern over any field. For Kneser
graphs it proves that the Grundy domination number of K(n,r) equals binom(n-1,r-1) whenever a
prime power at least r divides n-2r, which settles the conjecture of Campêlo and Severín for all
but finitely many n for each r, and it determines K(8,3), K(9,4), K(10,4), K(11,4) and K(11,5)
exactly. For products it determines strong tori (the value (k-2)(l-2)) and many further strong
and direct products, shows that both product conjectures of Brešar et al. are false with largest
ratio n^(1/2+o(1)), and answers Question 1 of Brešar, Henning and Rall negatively with
projective planes.

Every statement is proved in the paper. The programs recompute the finite cases.

- `lean/GrundyCert.lean`: dominating sequences, Grundy coverings of PG(2,2) and PG(2,8), and
  rank factorizations over F_2, F_3, F_5 (Lean 4 core, v4.24.0, `decide`).
- `lean/KneserSequences.lean`: the five Kneser dominating sequences of the paper (`decide +kernel`).
- `julia/checks.jl` and `julia/kneser_checks.jl` (with `data/`): independent rank and sequence checks (Julia 1.11).
- `search/`: the exact C solver and the Python search scripts.
- `run_all.sh`: runs all Lean and Julia checks.

Concept DOI: [10.5281/zenodo.23607651](https://doi.org/10.5281/zenodo.23607651).
