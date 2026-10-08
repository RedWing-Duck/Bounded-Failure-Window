#!/usr/bin/env bash
# Reproduce every Task 11 result, figure and RESULTS_t11.md. Usage: ./run_t11.sh [code_commit_hash]
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
for s in t11_symbolic t11_garble t11_power t11_power_diag t11_delay t11_notnec t11_sampling t11_figures; do
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log" 2>&1
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done
python3 make_results_t11.py "${1:-}"
echo "done: see RESULTS_t11.md"
