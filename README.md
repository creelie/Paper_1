# Grundy Domination of Graph Products and Minimum Rank

Deep Bhattacharjee. Release v3.0.0.

The paper [`paper/GrundyPaper.pdf`](paper/GrundyPaper.pdf) proves that the Grundy domination
number of a strong product is at most the product of the minimum ranks of the factors over any
field. From this it determines the Grundy domination number of strong products of cycles
(the torus value (k-2)(l-2)), paths, complete bipartite graphs and Kneser graphs K(n,2), and
the Grundy total domination number of direct products of cycles, forests and complete graphs.
It shows that the strong-product conjecture of Brešar et al. (2016) and the direct-product
conjecture of Brešar et al. (2021) are false with unbounded ratios, and that incidence graphs
of projective planes give a negative answer to Question 1 of Brešar, Henning and Rall (2016).

Every statement is proved in the paper. The programs recompute the finite cases.

- `lean/GrundyCert.lean`: Lean 4 (core library, v4.24.0) certificates checked by `decide`:
  dominating sequences, Grundy coverings of PG(2,2) and PG(2,8), and rank factorizations over
  F_2, F_3, F_5. Run `lean lean/GrundyCert.lean`.
- `julia/checks.jl`: 153 independent checks (Julia 1.11, standard library). Run `julia julia/checks.jl`.
- `search/`: the exact C solver `gr.c` and the Python scripts for the search of Section 8.
- `run_all.sh`: runs the Lean and Julia checks.

Concept DOI: [10.5281/zenodo.23607651](https://doi.org/10.5281/zenodo.23607651).
