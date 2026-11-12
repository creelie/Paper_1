#!/usr/bin/env bash
# Runs the Lean certificate and the Julia checks. Needs `lean` (v4.24.0) and `julia` (1.11) on PATH.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
echo "== Lean"
lean lean/GrundyCert.lean
echo "== Julia"
julia julia/checks.jl
echo "all checks passed"
