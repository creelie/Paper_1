Deep Bhattacharjee, *Unbounded strong-product ratios for the Grundy domination number*. Revision of 30 October 2026, single column (amsart), 9 pages.

The paper disproves the conjecture of Brešar, Bujtás, Gologranc, Klavžar, Košmrlj, Patkós, Tuza
and Vizer (2016) that the Grundy domination number of a strong product equals the product of
the Grundy domination numbers of its factors, and shows that the ratio is unbounded. This
revision adds three results, all proved by hand:

- the Grundy domination number of a strong product is at most the product of the minimum
  ranks of the factors over any field (matrices whose nonzero entries are exactly the closed
  neighbourhoods), so the conjecture holds whenever both factors attain their minimum rank
  over a common field, for example for products of complete, edgeless and complete bipartite
  graphs;
- the Grundy domination number of the graph H^1_N (u and v adjacent when |u-v| = 1 mod 3) is
  floor(N/3)+2 for N >= 4, by the same half-graph count as for H^2_N, whose value
  floor((N+1)/3)+3 is kept;
- the strong product of the octahedron with H^1_N is a counterexample for N = 11, 13, 14 and
  every N >= 15; the smallest has 66 vertices.

Programs in C and Python recompute the small cases, including the exact Grundy domination
numbers of the products for N <= 13; this release runs them before publishing. No statement
of the paper rests on them.

This revision replaces v2.0.1 and its Hexagon version hexagon:2610.00494v2; the
counterexample was first made public on 14 October 2026 as release v1.0.0 of
creelie/grundy-strong-product.

Files: the paper (`GrundyStrongProduct_final2.pdf`), its LaTeX source with the figures
(`GrundyStrongProduct_final2-tex.zip`) and the arXiv tarball
(`GrundyStrongProduct_final2-arxiv.tar.gz`).

Contact: d.bhattacharjee@erl-forschung.de, itsdeep@live.com; GitHub-related contact egspl@proton.me (GitHub creelie).
