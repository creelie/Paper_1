#!/usr/bin/env bash
# run_all.sh: every check in this repository. Outputs go to build/.
#   C:      checks/c/grundy_bfs.c computes the Grundy domination number of H^r_N by breadth-first
#           search over dominated sets; it must give floor(N/3)+2 for r = 1, 4 <= N <= 30, and
#           floor((N+1)/3)+3 for r = 2, 6 <= N <= 27, and 2 for the octahedron.
#           checks/c/product_exact.c computes the Grundy domination number of K_{2,2,2} x H^r_N
#           by a memoised search; it must give the values of Remark 6.6.
#   Python: checks/python/check_paper.py checks the finite statements of the paper from the
#           definitions: Lemma 2.1, Theorem 1.4 and Example 2.2 on small graphs, the incidence
#           matrices of Section 3, the formulas for H^1_N and H^2_N by a different search, the
#           hypotheses of Lemma 6.1, the sequences of Lemmas 6.3, 6.4 and Proposition 5.1 up to
#           N = 64, and Example 6.5.
# Needs a C compiler with unsigned __int128 (gcc or clang) and Python 3 (standard library only).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
B="$ROOT/build"
mkdir -p "$B"
cd "$ROOT"

echo "== C: Grundy domination numbers by breadth-first search"
cc -O2 -Wall -Wextra -Werror -o "$B/grundy_bfs" checks/c/grundy_bfs.c
: > "$B/grundy_bfs.txt"
"$B/grundy_bfs" oct | tee -a "$B/grundy_bfs.txt" | grep -q "Grundy domination number 2$"
for N in $(seq 4 30); do
  want=$(( N / 3 + 2 ))
  "$B/grundy_bfs" "$N" 1 | tee -a "$B/grundy_bfs.txt" | grep -q "Grundy domination number $want$"
done
echo "H^1_N: formula confirmed for N = 4, ..., 30"
for N in $(seq 6 27); do
  want=$(( (N + 1) / 3 + 3 ))
  "$B/grundy_bfs" "$N" 2 | tee -a "$B/grundy_bfs.txt" | grep -q "Grundy domination number $want$"
done
echo "H^2_N: formula confirmed for N = 6, ..., 27"

echo "== C: the products K_{2,2,2} x H^r_N (Remark 6.6)"
cc -O2 -Wall -Wextra -Werror -o "$B/product_exact" checks/c/product_exact.c
: > "$B/product_exact.txt"
set -- 6 6 8 8 8 10 10 11 12 13
for N in $(seq 4 13); do
  "$B/product_exact" "$N" 1 | tee -a "$B/product_exact.txt" | grep -q "Grundy domination number $1$"
  shift
done
for N in $(seq 6 12); do
  want=$(( 2 * ((N + 1) / 3 + 3) ))
  "$B/product_exact" "$N" 2 | tee -a "$B/product_exact.txt" | grep -q "Grundy domination number $want$"
done
echo "products: the values of Remark 6.6 confirmed"

echo "== Python: the finite statements of the paper"
python3 -I checks/python/check_paper.py | tee "$B/check_paper.txt"
grep -q '^failures 0$' "$B/check_paper.txt"
echo "all checks passed"
