# Proof review and scope

Revision reviewed 24 October 2026. This is a reproducible preparation audit, not an
independent referee report or a guarantee of editorial acceptance.

## Main unbounded-ratio theorem

The proof is complete as a written finite-dimensional argument, with no appeal to
an unproved theorem or unrefereed external proof.

1. A legal sequence has distinct vertices and distinct footprints. An exact
   closed-neighbourhood support matrix restricted to its selected rows and footprint
   columns is triangular with nonzero diagonal. Its rank bounds the sequence length.
2. For five-element sets, the element-incidence Gram matrix over F_2 has entries
   |S intersect T| mod 2. Its support is exactly the diagonal and intersection sizes
   1 and 3. Its rank is at most m.
3. The pair-incidence Gram matrix over F_3 has entries binom(|S intersect T|,2)
   mod 3. For intersection sizes 0,...,5 the residues are 0,0,1,0,0,1.
   Its support is exactly the diagonal and intersection size 2. Its rank is at most
   binom(m,2). In particular, the diagonal is nonzero in both matrices.
4. The distinct-set edge intersection sizes in the two graphs are disjoint.
   The diagonal set {(S,S)} is consequently independent in the strong product,
   giving a legal sequence of length binom(m,5).
5. The factor parameters are positive. Dividing the lower bound by the two
   upper bounds gives (m-2)(m-3)(m-4)/(60m), which tends to infinity.

Using different fields in steps 2 and 3 is legitimate: no common-field tensor
product bound is used. Merely giving a fitting matrix that vanishes on nonedges
would be insufficient for step 1; exact support is verified explicitly.

Alon's 1998 intersection-congruence construction is credited, with a reference to
Section 3. The present result is an application to legal domination sequences,
not a claim to have invented the finite-field method or to have refuted a Shannon
capacity theorem.

## Exact formula for H_N

The induced-subgraph observation preserves all footprints. It reduces the upper
bound to H_(3q+1) and the lower bound to H_(3q-1), with small base cases supplied.
Translation in H_(3q+1) places the first choice at 0. The remaining graph has
X_i adjacent to Y_j exactly when i >= j, and has a perfect matching X_i Y_i.

Until the first selected edge or third-class vertex, selected indices satisfy
i < j across the two classes. At the first edge, the displayed count bounds
selected vertices plus undominated vertices by q+1 after the initial choice.
At the first third-class vertex, the matching-neighbour map into W_k is
injective; collisions would require an index on both selected sides. At most
q+1-r-s vertices remain, giving the total upper bound q+3. If neither event
occurs, the perfect matching bounds the independent selections by q.

The lower construction has q-2 initial self-footprints and five specified final
footprints. The small q=2 and q=3 cases are separate. All selected vertices and
footprints are within H_(3q-1). Monotonicity gives the formula at each intermediate
N. The product footprints (x_(t+1),v_j) give the required length-N sequence with
the octahedron, and the arithmetic at N=19 and N>=21 is strict as claimed.

## Verification evidence

`verification/current/` records the actual current runs. Its summary states
whether that invocation also rebuilt Lean. The retained Lean sources are pinned
to Lean 4.34.1, have no Mathlib dependency, and concern N=21 only.

Fresh Python checks cover exact H_N values through N=30; lower witnesses through
q=300; the two upper-bound structural counts through q=10; and all ordered pairs
in the incidence matrices through m=10, including their ranks over F_2 and F_3.
Separate programs check the original counterexample and the masks and layer data
in the Lean files. Regenerating the layer source must agree after line-ending
normalization. None of these finite runs alone proves an all-parameter assertion.

The input archive's old C logs and old Lean audit remain provenance, distinct
from a current successful build. A fresh result is reported only after its
command finishes successfully. No native-decide trust claim is inferred solely
from a source-text search; the axiom printer is audited when Lean is rebuilt.

## Literature and editorial fit

Primary sources checked include the original conjecture (arXiv:1607.00248,
Conjecture 6.2 there; Conjecture 22 in the journal), Bell et al.'s forest result
(arXiv:2104.05665; published DOI 10.37236/9507), and the withdrawal notice for
arXiv:2212.04565v2. The withdrawn general proof is not cited as a valid theorem.
The current targeted searches did not locate an earlier independent unbounded-ratio
result. This is a bounded literature search, not exhaustive priority clearance.
The earlier local priority review is retained with its original date and scope.

Annals is the requested target. The strongest contribution here is a quantitative
disproof for a specialized invariant, with an elementary adaptation of classical
tools. Its significance threshold remains an editorial question. No sure
acceptance, independent referee endorsement, or resolution of unrelated conjectures
is claimed.

Primary links checked on 24 October 2026:

- https://arxiv.org/html/1607.00248v1
- https://arxiv.org/html/2104.05665v1
- https://arxiv.org/abs/2212.04565v2
- https://www.cs.tau.ac.il/~nogaa/PDFS/shann3.pdf
- https://doi.org/10.1007/PL00009824
- https://annals.math.princeton.edu/submission-guidelines
