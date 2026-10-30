# Unbounded strong-product ratios for the Grundy domination number

Deep Bhattacharjee. Revision of 30 October 2026 (release v2.1.0).

A sequence of vertices of a graph is legal when every vertex in it dominates some vertex
that none of the earlier ones dominated, and the Grundy domination number of the graph is
the length of its longest legal sequence. Brešar, Bujtás, Gologranc, Klavžar, Košmrlj,
Patkós, Tuza and Vizer proved in 2016 that the Grundy domination number of a strong product
is at least the product of the Grundy domination numbers of the two factors, and conjectured
that equality always holds. The paper shows that the conjecture is false, and false by an
unbounded factor. The smallest counterexample it gives is the strong product of the
octahedron with the graph H^1_11 on {0, ..., 10} in which u and v are adjacent when
|u-v| = 1 (mod 3): 66 vertices, factors with Grundy domination numbers 2 and 5, and a legal
sequence of length 11 in the product. The paper computes the Grundy domination numbers of
H^1_N and H^2_N (adjacency |u-v| = 1 or 2 mod 3) for every N, namely floor(N/3)+2 and
floor((N+1)/3)+3. In the other direction it proves that the Grundy domination number of a
strong product is at most the product of the minimum ranks of the factors over any field,
so the conjecture holds whenever both factors attain their minimum rank over a common field.
Every statement is proved by hand; the programs here only recompute the small cases, and no
statement of the paper rests on them.

The counterexample was first made public on 14 October 2026 as release v1.0.0 of
[creelie/grundy-strong-product](https://github.com/creelie/grundy-strong-product), archived
on Zenodo as [10.5281/zenodo.23378021](https://doi.org/10.5281/zenodo.23378021). An earlier
and incomplete version of the paper appeared on Hexagon as
[hexagon:2610.00494](https://hexagonmath.org/2610.00494) on 23 October 2026; it gave one
counterexample and relied on a computer certificate for the Grundy domination number of
H_21. The releases v1.2.0, v1.3.0, v2.0.0 and v2.0.1 of this repository followed; v2.0.0
was posted on Hexagon as [hexagon:2610.00494v2](https://hexagonmath.org/2610.00494v2).
This revision (v2.1.0) adds the rank bound for strong products, the second family H^1_N
and the 66-vertex counterexample.

## Layout

- `paper/main.tex`, `paper/figures/`: the LaTeX source and the three figures; `paper/main.pdf` the compiled paper (9 pages, amsart, single column).
- `dist/`: the paper as `GrundyStrongProduct_final2.pdf`, its source zip and the arXiv tarball.
- `checks/c/grundy_bfs.c`: the Grundy domination number of H^r_N (N <= 63, r = 1, 2) and of the octahedron by breadth-first search over dominated sets.
- `checks/c/product_exact.c`: the Grundy domination number of the product of the octahedron with H^r_N (N <= 21) by a memoised search; it recomputes the values of Remark 6.6.
- `checks/python/check_paper.py`: the finite statements of the paper from the definitions: Lemma 2.1, Theorem 1.4 and Example 2.2 on small graphs, the incidence matrices and ranks of Section 3 for m <= 9, the formulas for H^1_N and H^2_N up to N = 27 by a different search, the hypotheses of Lemma 6.1, the sequences of Lemmas 6.3, 6.4 and Proposition 5.1 up to N = 64, and Example 6.5.
- `run_all.sh`: runs all three.

## Running the checks

    ./run_all.sh

Requirements: a C compiler with `unsigned __int128` (gcc or clang) and python3 (standard library only). About half a minute.

## Releases

Releases are published by the workflow `release.yml` from the Actions tab.
Each release carries the paper files of `dist/`.

| Release | DOI |
| --- | --- |
| v2.1.0 (this revision) | [10.5281/zenodo.23791279](https://doi.org/10.5281/zenodo.23791279) (concept [10.5281/zenodo.23607651](https://doi.org/10.5281/zenodo.23607651)) |
| v2.0.1 | assigned on publication |
| v2.0.0 | [10.5281/zenodo.23659882](https://doi.org/10.5281/zenodo.23659882) |
| v1.3.0 | [10.5281/zenodo.23629621](https://doi.org/10.5281/zenodo.23629621) |
| v1.2.0 | [10.5281/zenodo.23607502](https://doi.org/10.5281/zenodo.23607502) |

## Author

Deep Bhattacharjee, Formerly, Electro-Gravitational Space Propulsion Laboratory (EGSPL), Bhubaneswar, Odisha 751030, India; Formerly, University of Calcutta (Heramba Chandra College), 23/49 Gariahat Road, Golpark, Kolkata 700029, West Bengal, India.
Emails: d.bhattacharjee@erl-forschung.de, itsdeep@live.com, egspl@proton.me (GitHub-related contact; GitHub [creelie](https://github.com/creelie)).
ORCID: 0000-0003-0466-750X.

## Licence

MIT, see `LICENSE`.
