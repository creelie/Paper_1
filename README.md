# Grundy domination checks

Deep Bhattacharjee. Release v3.1.0.

Code that recomputes the finite statements of the paper "Grundy Domination of Kneser Graphs and
Graph Products": dominating sequences of strong and direct products, the graphs H_N and Kneser
graphs K(n,r), and ranks of closed-neighbourhood pattern matrices over finite fields. Every
statement is proved in the paper; the programs only re-check finite cases. The paper itself is not
part of this repository.

- `lean/GrundyCert.lean`: dominating sequences, Grundy coverings of PG(2,2) and PG(2,8), and
  rank factorizations over F_2, F_3, F_5 (Lean 4 core, v4.24.0, `decide`).
- `lean/KneserSequences.lean`: the five Kneser dominating sequences (`decide +kernel`).
- `julia/checks.jl` and `julia/kneser_checks.jl` (with `data/`): independent rank and sequence checks (Julia 1.11).
- `search/`: the exact C solver and the Python search scripts.
- `run_all.sh`: runs all Lean and Julia checks.

GitHub-related contact: egspl@proton.me (GitHub: creelie). Licence: MIT.
