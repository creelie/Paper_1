#!/usr/bin/env bash
# run_all.sh: every check in this repository. Outputs go to build/.
#   C:      checks/c/grundy_bfs.c computes the Grundy domination number of H_N by breadth-first
#           search over dominated sets; it must give floor((N+1)/3)+3 for 6 <= N <= 27 and 2 for
#           the octahedron.
#   Python: checks/python/check_paper.py checks the finite statements of the paper from the
#           definitions: the incidence matrices and ranks of Section 2, the formula for H_N up
#           to N = 24 by a different search, the sequences of Lemma 5.2 and Proposition 4.1 up
#           to N = 64, and Example 5.3.
# Needs a C compiler and Python 3 (standard library only).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
B="$ROOT/build"
mkdir -p "$B"
cd "$ROOT"

echo "== C: Grundy domination numbers by breadth-first search"
cc -O2 -Wall -Wextra -Werror -o "$B/grundy_bfs" checks/c/grundy_bfs.c
: > "$B/grundy_bfs.txt"
"$B/grundy_bfs" oct | tee -a "$B/grundy_bfs.txt" | grep -q "Grundy domination number 2$"
for N in $(seq 6 27); do
  want=$(( (N + 1) / 3 + 3 ))
  "$B/grundy_bfs" "$N" | tee -a "$B/grundy_bfs.txt" | grep -q "Grundy domination number $want$"
done
echo "H_N: formula confirmed for N = 6, ..., 27"

echo "== Python: the finite statements of the paper"
python3 -I checks/python/check_paper.py | tee "$B/check_paper.txt"
grep -q '^failures 0$' "$B/check_paper.txt"
echo "all checks passed"
