#!/usr/bin/env bash
# Reproduce every Task 9 result, the figure and RESULTS_t9.md. Usage: ./run_t9.sh [code_commit_hash]
set -euo pipefail
cd "$(dirname "$0")"
rm -rf results && mkdir -p results
python3 - > results/env.json <<'PY'
import json, platform, os, numpy, scipy, sympy, matplotlib, mpmath
print(json.dumps({"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
                  "sympy": sympy.__version__, "mpmath": mpmath.__version__, "matplotlib": matplotlib.__version__,
                  "platform": platform.platform(), "cpus": os.cpu_count()}, indent=1))
PY
: > results/runtime.tsv
for s in t9_symbolic t9_filter t9_filter_diag t9_values t9_classify t9_order t9_order_diag t9_adversarial t9_figure; do
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log"
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done
python3 make_results_t9.py "${1:-}"
echo "done: see RESULTS_t9.md"
