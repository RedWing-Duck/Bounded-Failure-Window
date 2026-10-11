#!/usr/bin/env bash
# Reproduce every Task 13 result, figure and RESULTS_t13.md. Usage: ./run_t13.sh [code_commit_hash]
# Part D's comparison (compare_repro.py) needs a finished clean-checkout replay and is run separately (see reproduce_all.sh).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
python3 - > results/env.json <<'PY'
import json, platform, os, numpy, scipy, sympy, matplotlib, mpmath
print(json.dumps({"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
                  "sympy": sympy.__version__, "mpmath": mpmath.__version__, "matplotlib": matplotlib.__version__,
                  "platform": platform.platform(), "cpus": os.cpu_count()}, indent=1))
PY
: > results/runtime.tsv
for s in t13_partA_symbolic t13_partA_symbolic_diag t13_regression_symbolic t13_partA_numeric t13_partA_numeric_diag \
         t13_A3_attempt t13_A3_proof t13_A3_closed t13_A3_limits t13_audit_numbers t13_audit_refs t13_audit_classes t13_audit_classes_diag t13_audit_classes_diag2 \
         t13_figures_paper2; do
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log" 2>&1
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done
python3 make_results_t13.py "${1:-}"
echo "done: see RESULTS_t13.md"
