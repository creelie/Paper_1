# Unbounded strong-product ratios for the Grundy domination number

Deep Bhattacharjee. Final revision, 26 October 2026.

A sequence of vertices of a graph is legal when every vertex in it dominates some vertex
that none of the earlier ones dominated, and the Grundy domination number of the graph is
the length of its longest legal sequence. Brešar, Bujtás, Gologranc, Klavžar, Košmrlj,
Patkós, Tuza and Vizer proved in 2016 that the Grundy domination number of a strong product
is at least the product of the Grundy domination numbers of the two factors, and conjectured
that equality always holds. The paper shows that the conjecture is false, and false by an
unbounded factor: for every number C there are graphs whose strong product has Grundy
domination number more than C times the product of the two factors. The graphs are built on
the five-element subsets of an m-element set, with adjacency decided by the size of the
intersection; incidence matrices over the fields with two and three elements bound the two
factors by m and binom(m,2), while the diagonal of the product is an independent set of
size binom(m,5). The paper also computes the Grundy domination number of the graph H_N on
{0, ..., N-1} in which u and v are adjacent when |u-v| = 2 (mod 3): it is floor((N+1)/3)+3
for every N >= 6. Its strong product with the octahedron has a legal sequence of length N,
so the conjecture already fails for N = 19, on a graph with 114 vertices, and for every
N >= 21. Every statement is proved by hand; the programs here only recompute the small
cases, and no statement of the paper rests on them.

The counterexample was first made public on 14 October 2026 as release v1.0.0 of
[creelie/grundy-strong-product](https://github.com/creelie/grundy-strong-product), archived
on Zenodo as [10.5281/zenodo.23378021](https://doi.org/10.5281/zenodo.23378021). An earlier
and incomplete version of the paper appeared on Hexagon as
[hexagon:2610.00494](https://hexagonmath.org/2610.00494) on 23 October 2026; it gave one
counterexample and relied on a computer certificate for the Grundy domination number of
H_21. The revisions that followed are the releases v1.2.0 and v1.3.0 of this repository,
archived as [10.5281/zenodo.23607502](https://doi.org/10.5281/zenodo.23607502) and
[10.5281/zenodo.23629621](https://doi.org/10.5281/zenodo.23629621). This revision replaces
them: the Grundy domination number of H_N is computed by hand for every N >= 6, the ratio is
shown to be unbounded, and nothing rests on a computer.

## Layout

- `paper/main.tex`, `paper/figures/`: the LaTeX source and the three figures; `paper/main.pdf` the compiled paper (9 pages, single column).
- `dist/`: the paper as `GrundyStrongProduct_final2.pdf`, its source zip and the arXiv tarball.
- `checks/c/grundy_bfs.c`: the Grundy domination number of H_N (N <= 63) and of the octahedron by breadth-first search over dominated sets.
- `checks/python/check_paper.py`: the finite statements of the paper from the definitions: the incidence matrices and ranks of Section 2 for m <= 9, the formula for H_N up to N = 24 by a different search, the sequences of Lemma 5.2 and Proposition 4.1 up to N = 64, and Example 5.3.
- `run_all.sh`: runs both.

## Running the checks

    ./run_all.sh

Requirements: a C compiler and python3 (standard library only). About half a minute.

## Releases

Releases are published by the workflow `release.yml` from the Actions tab.
Each release carries the paper files of `dist/`.

| Release | DOI |
| --- | --- |
| v2.0.0 (this revision) | to be recorded |
| v1.3.0 | [10.5281/zenodo.23629621](https://doi.org/10.5281/zenodo.23629621) |
| v1.2.0 | [10.5281/zenodo.23607502](https://doi.org/10.5281/zenodo.23607502) |

## Author

Deep Bhattacharjee, Formerly, Electro-Gravitational Space Propulsion Laboratory (EGSPL), Bhubaneswar, Odisha 751030, India; Formerly, University of Calcutta, Senate House, 87/1 College Street, Kolkata 700073, West Bengal, India.
Emails: d.bhattacharjee@erl-forschung.de, itsdeep@live.com, egspl@proton.me (for questions about this repository).
ORCID: 0000-0003-0466-750X.

## Licence

MIT, see `LICENSE`.
