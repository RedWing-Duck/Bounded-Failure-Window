#!/usr/bin/env bash
# Reproduce every Task 12 result, figure and RESULTS_t12.md. Usage: ./run_t12.sh [code_commit_hash]
# Order matters: t12_blind reads the A8 census classes (results/t12_a8.json); t12_figures reads the A2/A3 points from it.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf results figs && mkdir -p results figs
python3 - > results/env.json <<'PY'
import json, platform, os, numpy, scipy, sympy, matplotlib, mpmath
print(json.dumps({"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
                  "sympy": sympy.__version__, "mpmath": mpmath.__version__, "matplotlib": matplotlib.__version__,
                  "platform": platform.platform(), "cpus": os.cpu_count()}, indent=1))
PY
: > results/runtime.tsv
for s in t12_symbolic t12_symbolic_diag t12_a8 t12_dt t12_mi t12_sigma t12_blind t12_diag t12_figures; do
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log" 2>&1
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done
python3 make_results_t12.py "${1:-}"
echo "done: see RESULTS_t12.md"
