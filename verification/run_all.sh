#!/usr/bin/env bash
# Reproduce every result, figure and REPORT.md from scratch.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf results figures
mkdir -p results figures

python3 - > results/env.json <<'EOF'
import json, platform, os, numpy, scipy, sympy, matplotlib
print(json.dumps({"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
                  "sympy": sympy.__version__, "matplotlib": matplotlib.__version__,
                  "platform": platform.platform(), "cpus": os.cpu_count()}, indent=1))
EOF

: > results/runtime.tsv
for s in t1_symbolic t2_em t3_paired t4a_discrete t4b_colored t4c_drift t4d_gains t4e_fixed_gain; do
  echo "== $s"
  t0=$(date +%s.%N)
  python3 "$s.py" > "results/$s.log"
  t1=$(date +%s.%N)
  dt=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s\t%s\n' "$s" "$dt" >> results/runtime.tsv
  echo "   ${dt}s"
done

python3 make_report.py
echo "done: see REPORT.md"
