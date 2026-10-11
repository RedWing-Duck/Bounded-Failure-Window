"""Part D: one manifest for the whole replay (results/repro_manifest.json).
The Tasks 8-12 replay ran in three invocations in one worktree (Task 8; Tasks 9-12, stopped by the Task 10 failure; Tasks
11-12) and Task 13 in a second worktree on the final commit, so only the last invocation of each wrote its own manifest.
This script collects the per-task runtimes from every runtime_*.tsv (Task 10: sum of its logged script runtimes, since the
replay stopped before recording it) and hashes every output file with the same file map as reproduce_all.sh.
Note: Task 10's outputs include t10_2_diag.json and the RESULTS_t10.md written by repro_t10_diag.py after the failure.
Usage: python3 merge_manifests.py WORKDIR_8_12 [WORKDIR_13]"""
import hashlib
import json
import os
import platform
import subprocess
import sys

import matplotlib
import mpmath
import numpy
import scipy
import sympy

from t13_common import RES, save_json

DIRS = {"8": ["results", "figures", "REPORT.md"], "9": ["t9/results", "t9/RESULTS_t9.md", "t9/fig_t9_tau.png"],
        "10": ["t10/results", "t10/figs", "t10/RESULTS_t10.md"], "11": ["t11/results", "t11/figs", "t11/RESULTS_t11.md"],
        "12": ["t12/results", "t12/figs", "t12/RESULTS_t12.md"], "13": ["t13/results", "t13/RESULTS_t13.md"]}


def runtimes(work):
    rt = {}
    for fn in sorted(os.listdir(work)):
        if fn.startswith("runtime_") and fn.endswith(".tsv"):
            for ln in open(os.path.join(work, fn)).read().splitlines():
                if ln.strip():
                    t, s = ln.split("\t")
                    rt[t] = float(s)
    return rt


def hashes(work, tasks):
    cls, out = os.path.join(work, "classification"), {}
    for t in tasks:
        for d in DIRS[t]:
            p = os.path.join(cls, d)
            if not os.path.exists(p):
                continue
            files = [p] if os.path.isfile(p) else [os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs]
            for f in sorted(files):
                out[os.path.relpath(f, cls)] = hashlib.sha256(open(f, "rb").read()).hexdigest()
    return out


def main():
    works = sys.argv[1:]
    M = {"invocations": [], "runtime_s": {}, "sha256": {}, "python": platform.python_version(), "numpy": numpy.__version__,
         "scipy": scipy.__version__, "sympy": sympy.__version__, "mpmath": mpmath.__version__,
         "matplotlib": matplotlib.__version__, "platform": platform.platform(), "cpus": os.cpu_count()}
    for w in works:
        rt = runtimes(w)
        commit = subprocess.run(["git", "-C", w, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        t10 = os.path.join(w, "classification", "t10", "results", "runtime.tsv")
        if "10" not in rt and os.path.exists(os.path.join(w, "task10.log")) and os.path.exists(t10):
            rt["10"] = sum(float(l.split("\t")[1]) for l in open(t10).read().splitlines()
                           if l.strip() and l.split("\t")[0] != "t10_realize_diag")
            M["task10_note"] = "replay failed in make_results_t10.py; runtime = sum of the scripts it ran"
        tasks = [t for t in DIRS if t in rt]
        M["invocations"].append({"workdir": w, "commit": commit, "tasks": tasks})
        M["runtime_s"].update({t: rt[t] for t in tasks})
        M["sha256"].update({f"{t}:{k}": v for t in tasks for k, v in hashes(w, [t]).items()})
    M["runtime_s"] = dict(sorted(M["runtime_s"].items(), key=lambda kv: int(kv[0])))
    print({k: v for k, v in M.items() if k != "sha256"}, "files:", len(M["sha256"]))
    save_json(M, "repro_manifest.json")


if __name__ == "__main__":
    main()
