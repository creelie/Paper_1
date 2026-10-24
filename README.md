# Unbounded strong-product ratios for the Grundy domination number

Deep Bhattacharjee. Annals of Mathematics submission preparation, 24 October 2026.

The main theorem gives explicit graphs A_m and B_m on the five-element subsets of [m]
with Grundy domination numbers at most m and binom(m,2), while their strong product
has a legal sequence of length binom(m,5). The resulting ratio grows without bound.
A second elementary argument proves gamma_gr(H_N) = floor((N+1)/3)+3 for every N >= 6.
Its product with the octahedron supplies a 114-vertex counterexample at N=19.

Both general theorems have complete written proofs. Their proofs use no unproved
external theorem or computer enumeration. The incidence method is credited to
Alon's classical work; its adaptation here requires exact neighbourhood support.

Complete ZIP: https://github.com/creelie/Paper_1/releases/download/v1.2.0/Paper_1_Annals_submission_v1.2.0.zip

## Submission files

- `Paper_1_Annals.pdf`: PDF for the editorial system.
- `manuscript/main.tex`, `references.bib`, `main.bbl`: complete manuscript sources.
- `manuscript/figures/`: vector PDF figures and their TikZ sources.
- `submission/COVER-LETTER.txt`: cover letter prepared for Annals.
- `submission/PORTAL-METADATA.md`: title, abstract, keywords and author details.
- `submission/SUBMISSION-NOTES.md`: current submission route and author declarations.
- `PROOF-REVIEW.md`: proof checks, scope and editorial assessment.
- `lean/`: the separate certificate for N=21, pinned to Lean 4.34.1.
- `verification/current/`: current verification outputs; other verification files came from the input archive.
- `provenance/INPUT.json`: input archive, hashes and earlier publication links.

This revision is published on Zenodo: https://doi.org/10.5281/zenodo.23607502 .
The complete submission ZIP is created only after that publication was confirmed.
The earlier DOI below identifies version 1.0.0.

The fresh Lean build and 25-declaration axiom audit passed. See `FORMAL-STATUS.md`.

## Reproduce

Python 3, TeX Live or MiKTeX with `aomart`, and Lean 4.34.1 suffice. No Python
third-party package or Mathlib dependency is needed for mathematical verification.

```text
python -X utf8 scripts/verify.py
python -X utf8 scripts/verify.py --lean
python -X utf8 scripts/build_manuscript.py
```

Use `--lake` and `--tex-bin` if the executables are outside PATH. A clean Lean
certificate build can be substantially slower than the Python checks. It verifies
N=21 only; neither general theorem has been formalized in this development.

## Publication history

Original preprint: https://hexagonmath.org/2610.00494v1

Original computational archive (v1.0.0): https://doi.org/10.5281/zenodo.23378021

Submission repository: https://github.com/creelie/Paper_1

The repository's existing MIT licence is preserved. AI assistance is disclosed
with specific proof locations in the manuscript. The package has not been
submitted to a journal. Editorial acceptance and an independent referee report
are not established by formatting or the checks in this repository.
