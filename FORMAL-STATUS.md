# Formal verification, 24 October 2026

A fresh build from the supplied Lean sources completed successfully with Lean
4.34.1 (commit 5045d0056413266e57c625dcd7c365b10e377c52). The initial build
completed seven jobs; the `GrundyStrong.Counterexample` module took 858 seconds.
The sources were copied from the input archive, without mathematical changes.
There is no Mathlib or other external Lean-library dependency.

The subsequent `lake env lean Check.lean` run printed the axioms of 25 declarations.
`scripts/audit_axioms.py` passed: all 25 use only the permitted standard axioms,
and five depend on no axioms at all. The audit excludes `sorryAx`,
`native_decide`/`ofReduceBool` trust and any additional axioms. Raw current output
is in `verification/current/lean-axioms.txt` and `axiom-audit.txt`.

This certificate proves the original finite N=21 counterexample, including the
upper bound gamma_gr(H_21) <= 10 and the legal sequence of length 21 in its
strong product with the octahedron. It does not formalize the unbounded-ratio
theorem or the exact formula for every N. Those are the written proofs in
Sections 2 and 5 of the manuscript, corroborated by the specified finite checks.

Reproduce with:

```text
python -X utf8 scripts/verify.py --lean
```

Allow time for kernel evaluation on a clean build. The original archive's
`verification/axioms.txt` is retained separately from the fresh output.
