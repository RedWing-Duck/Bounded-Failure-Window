"""T7.5: time the full run_all.sh (Task 7 included) in a temporary copy of verification/, so the committed
results and earlier REPORT.md sections are not touched. Not part of run_all.sh (it would recurse)."""
import filecmp
import json
import os
import shutil
import subprocess
import tempfile
import time

from common import HERE, RES, dump


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in ("runtime_s", "lines")}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


with tempfile.TemporaryDirectory(prefix="t7_runall_") as tmp:
    dst = os.path.join(tmp, "verification")
    shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("__pycache__"))
    t0 = time.time()
    proc = subprocess.run(["bash", "run_all.sh"], cwd=dst, capture_output=True, text=True)
    wall = time.time() - t0
    per = []
    tsv = os.path.join(dst, "results", "runtime.tsv")
    if os.path.exists(tsv):
        per = [ln.split("\t") for ln in open(tsv).read().splitlines() if ln.strip()]
    same, differ, missing = [], [], []
    for fn in sorted(os.listdir(RES)):
        if not fn.endswith(".json") or fn in ("t7_runtime.json", "env.json"):
            continue
        new = os.path.join(dst, "results", fn)
        if not os.path.exists(new):
            missing.append(fn)
            continue
        a, b = strip(json.load(open(os.path.join(RES, fn)))), strip(json.load(open(new)))
        (same if a == b else differ).append(fn)
    figdir = os.path.join(HERE, "figures")
    figs_same = [f for f in sorted(os.listdir(figdir))
                 if os.path.exists(os.path.join(dst, "figures", f))
                 and filecmp.cmp(os.path.join(figdir, f), os.path.join(dst, "figures", f), shallow=False)]
    n_figs = len(os.listdir(figdir))

res = {"exit_code": proc.returncode, "pass": proc.returncode == 0, "wall_s": wall,
       "per_script": [{"script": s, "seconds": float(t)} for s, t in per],
       "sum_scripts_s": sum(float(t) for _, t in per),
       "json_identical": same, "json_differ": differ, "json_missing": missing,
       "figures_identical": len(figs_same), "figures_total": n_figs,
       "stderr_tail": proc.stderr[-2000:]}
print(json.dumps({k: v for k, v in res.items() if k != "stderr_tail"}, indent=1))
dump("t7_runtime.json", res)
