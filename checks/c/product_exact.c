/* product_exact.c: exact Grundy domination number of the strong product K_{2,2,2} x H^r_N.
 *
 *   product_exact N r     N between 1 and 21, r in {1, 2}
 *
 * H^r_N is the graph on 0, ..., N-1 with u ~ v when |u-v| = r (mod 3); the octahedron K_{2,2,2}
 * has the vertices 0, ..., 5 with i and i+3 the only non-adjacent pairs. The product vertex (g, v)
 * is g*N + v. A memoised depth-first search computes, for every dominated set D reached by a legal
 * sequence, the length of a longest legal continuation; the Grundy domination number is its value
 * at the empty set. Dominated sets are 128-bit masks, so 6N <= 128.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int n;
static u128 nb[128], full;
static u128 *keys;
static signed char *vals;
static uint64_t cap;
static long stored;

static uint64_t hash(u128 x) {
  uint64_t a = (uint64_t)x, b = (uint64_t)(x >> 64);
  a ^= b * 0x9E3779B97F4A7C15ULL;
  a ^= a >> 29;
  a *= 0xBF58476D1CE4E5B9ULL;
  a ^= a >> 32;
  return a & (cap - 1);
}

static int longest(u128 d) {
  if (d == full) return 0;
  uint64_t h = hash(d);
  while (vals[h] >= 0) {
    if (keys[h] == d) return vals[h];
    h = (h + 1) & (cap - 1);
  }
  int best = 0;
  for (int v = 0; v < n; v++)
    if (nb[v] & ~d) {
      int x = 1 + longest(d | nb[v]);
      if (x > best) best = x;
    }
  if (2 * (uint64_t)++stored > cap) { fprintf(stderr, "hash table too small\n"); exit(1); }
  h = hash(d);
  while (vals[h] >= 0) h = (h + 1) & (cap - 1);
  keys[h] = d;
  vals[h] = (signed char)best;
  return best;
}

int main(int argc, char **argv) {
  if (argc != 3) { fprintf(stderr, "usage: product_exact N r\n"); return 2; }
  int N = atoi(argv[1]), r = atoi(argv[2]);
  if (N < 1 || 6 * N > 128 || (r != 1 && r != 2)) { fprintf(stderr, "need 1 <= N <= 21 and r in {1,2}\n"); return 2; }
  n = 6 * N;
  for (int g = 0; g < 6; g++)
    for (int v = 0; v < N; v++) {
      u128 m = 0;
      for (int g2 = 0; g2 < 6; g2++) {
        if (g2 != g && (g2 - g == 3 || g - g2 == 3)) continue;
        for (int v2 = 0; v2 < N; v2++) {
          int d = v2 > v ? v2 - v : v - v2;
          if (v2 == v || d % 3 == r) m |= (u128)1 << (g2 * N + v2);
        }
      }
      nb[g * N + v] = m;
    }
  full = n == 128 ? ~(u128)0 : (((u128)1 << n) - 1);
  cap = 1ULL << 23;
  keys = malloc(cap * sizeof *keys);
  vals = malloc(cap);
  if (!keys || !vals) { fprintf(stderr, "out of memory\n"); return 1; }
  memset(vals, -1, cap);
  int g = longest(0);
  printf("K_{2,2,2} x H^%d_%d: %ld dominated sets; Grundy domination number %d\n", r, N, stored, g);
  return 0;
}
