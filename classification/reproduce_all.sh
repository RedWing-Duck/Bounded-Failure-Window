#!/usr/bin/env bash
# Reproduce Tasks 8-13 from a clean checkout and write a manifest.
# Usage: ./reproduce_all.sh WORKDIR [TASK ...]      (default tasks: 8 9 10 11 12 13)
#   WORKDIR  scratch directory for the clean checkout (a git worktree of the current HEAD is created there if absent;
#            an existing worktree is reused as is, so a later invocation can run further tasks in the same checkout).
# Writes WORKDIR/manifest_<tasks>.json: commit, package versions, CPUs, per-task runtime, SHA-256 of every output file.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(git -C "$here" rev-parse --show-toplevel)"
work="${1:?usage: reproduce_all.sh WORKDIR [TASK ...]}"; shift || true
tasks=("$@"); [ ${#tasks[@]} -gt 0 ] || tasks=(8 9 10 11 12 13)
if [ ! -d "$work/classification" ]; then
  git -C "$repo" worktree add --detach "$work" HEAD
fi
cls="$work/classification"
commit="$(git -C "$work" rev-parse --short HEAD)"
tag="$(IFS=_; echo "${tasks[*]}")"
times="$work/runtime_${tag}.tsv"; : > "$times"
# code commits cited by the original reports (passed through so the regenerated reports print the same hash)
declare -A CODE=([8]=83b9455 [9]=238c15f [10]=cbe96fe [11]=e4ce89c [12]=82edc1b [13]="")
declare -A RUN=([8]="run_all.sh" [9]="t9/run_t9.sh" [10]="t10/run_t10.sh" [11]="t11/run_t11.sh" [12]="t12/run_t12.sh" [13]="t13/run_t13.sh")
for t in "${tasks[@]}"; do
  echo "== Task $t ($(date -u +%FT%TZ))"
  t0=$(date +%s.%N)
  ( cd "$cls" && bash "${RUN[$t]}" "${CODE[$t]}" ) > "$work/task${t}.log" 2>&1
  t1=$(date +%s.%N)
  printf '%s\t%s\n' "$t" "$(python3 -c "print(f'{$t1-$t0:.1f}')")" >> "$times"
  echo "   done in $(tail -1 "$times" | cut -f2) s"
done
python3 - "$work" "$commit" "$times" "$tag" <<'PY'
import hashlib, json, os, platform, sys
work, commit, times, tag = sys.argv[1:5]
import numpy, scipy, sympy, matplotlib, mpmath
dirs = {"8": ["results", "figures", "REPORT.md"], "9": ["t9/results", "t9/RESULTS_t9.md", "t9/fig_t9_tau.png"],
        "10": ["t10/results", "t10/figs", "t10/RESULTS_t10.md"], "11": ["t11/results", "t11/figs", "t11/RESULTS_t11.md"],
        "12": ["t12/results", "t12/figs", "t12/RESULTS_t12.md"], "13": ["t13/results", "t13/RESULTS_t13.md"]}
rt = dict(l.split("\t") for l in open(times).read().splitlines() if l.strip())
out = {"commit": commit, "tasks": list(rt), "runtime_s": {k: float(v) for k, v in rt.items()},
       "python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__,
       "sympy": sympy.__version__, "mpmath": mpmath.__version__, "matplotlib": matplotlib.__version__,
       "platform": platform.platform(), "cpus": os.cpu_count(), "sha256": {}}
cls = os.path.join(work, "classification")
for t in rt:
    for d in dirs[t]:
        p = os.path.join(cls, d)
        files = [p] if os.path.isfile(p) else [os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs]
        for f in sorted(files):
            out["sha256"][os.path.relpath(f, cls)] = hashlib.sha256(open(f, "rb").read()).hexdigest()
json.dump(out, open(os.path.join(work, f"manifest_{tag}.json"), "w"), indent=1)
print("manifest:", os.path.join(work, f"manifest_{tag}.json"), "files:", len(out["sha256"]))
PY
