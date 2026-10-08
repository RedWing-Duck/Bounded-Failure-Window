#!/usr/bin/env bash
# Reproduce every Task 8 result, the figure and REPORT.md from scratch.
# Usage: ./run_all.sh [final_commit_hash]
set -euo pipefail
cd "$(dirname "$0")"
rm -rf results figures
mkdir -p results figures

python3 - > results/env.json <<'PY'
import json, platform, os, numpy, scipy, sympy, matplotlib
print(json.dumps({"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
                  "sympy": sympy.__version__, "matplotlib": matplotlib.__version__,
                  "platform": platform.platform(), "cpus": os.cpu_count()}, indent=1))
PY

: > results/runtime.tsv
for s in t8_symbolic t8_values t8_classify t8_no_window t8_realize t8_figures; do
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log"
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done

python3 t8_report.py "${1:-}" > /dev/null
echo "done: see REPORT.md and results/t8.txt"
