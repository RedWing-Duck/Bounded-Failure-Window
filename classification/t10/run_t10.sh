#!/usr/bin/env bash
# Reproduce every Task 10 result, figure and RESULTS_t10.md. Usage: ./run_t10.sh [code_commit_hash]
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
for s in t10_symbolic t10_symbolic_diag t10_realize t10_census t10_mixed t10_degenerate t10_degenerate_diag t10_tau t10_tau_diag t10_blind t10_figures; do
  [ -f "$s.py" ] || continue
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log" 2>&1
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done
python3 make_results_t10.py "${1:-}"
echo "done: see RESULTS_t10.md"
