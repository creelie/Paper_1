# Validation of revision 1.1.0

23 October 2026

Section 5 gives a complete elementary hand proof of the H_N formula for all N>=6.
Section 6 gives a complete elementary hand proof that strong-product ratios are unbounded.
These arguments have been checked in this session. Neither has been independently refereed
or formalized in Lean. The construction credits classical intersection-congruence methods;
limited literature searches do not establish global priority.

## Checks

- Original scripts/run_all.sh: PASS. C breadth-first search for N=6,...,45, original Python
  graph checks, neighbourhood masks and reproduction of the Lean layer data.
- verification/python/verify_revision.py: PASS. Exact Grundy values N=1,...,30; explicit lower
  footprints through q=300 in all three residue classes; 103,423 cut injections and 94,206
  first-edge cases; domain refuter N=5; all six possible intersection types for five-subsets;
  82,994 ordered set pairs; exact finite-field ranks through m=10; exact rational checks of
  the lower-bound formula. Finite checks support the universal arguments rather than replace them.
- The original Lean source and 25-declaration audit from version 1.0.0 are retained. They concern
  N=21. A fresh Lean build was not repeated after recovery of this workspace. The new general
  theorems are not described as Lean-verified.
- The local Anaxia patch adds both constructions, typed proof nodes, controls, task records and
  failure-loop replays. Formal, literature and human-review gates remain open. It is an update
  candidate, without an engine release or autonomous-discovery claim. Eight focused tests pass;
  a full run of all 309 engine tests is not claimed. The patch is against eBLLM commit
  9edc00135ecc31b933b5fb10d4a86a84b8a2ace1 and is supplied without committing that repository.
- All three PDFs compile. Their mathematical text and general_proofs.tex input agree, apart
  from the flat figure paths in the JCTB version. PDFs were rendered for visual review.
- ZIP integrity, source-package layout and metadata syntax were checked. Publisher style files
  are unchanged. Project whitespace checks exclude those unmodified vendor files.

## Publication state

The GitHub commit, push, release and Zenodo archive are separate from proof verification.
No external release or new DOI is asserted in these files. The old DOI 10.5281/zenodo.23378021
identifies version 1.0.0. A new DOI must be confirmed before it is added to the metadata.
