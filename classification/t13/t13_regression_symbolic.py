"""A-reg (PREREG_t13): re-run every symbolic check of Tasks 8-12 in one pass, with the documented fallback routes for the
three items that needed them (Task 10: two sqrt(square) items via t10_symbolic_diag; Task 12: the D2 O(1/dt) coefficient via
the series route of t12_symbolic_diag). Runs in a scratch copy so the committed results of Tasks 8-12 are not touched."""
import json
import os
import shutil
import subprocess
import tempfile
import time

from t13_common import CLS, save_json

SCRIPTS = [("t8", ".", "t8_symbolic.py", "results/t8_1.json"), ("t9", "t9", "t9_symbolic.py", "t9/results/t9_1.json"),
           ("t10", "t10", "t10_symbolic.py", "t10/results/t10_1.json"), ("t11", "t11", "t11_symbolic.py", "t11/results/t11_1.json"),
           ("t12", "t12", "t12_symbolic.py", "t12/results/t12_symbolic.json")]
DIAGS = [("t10", "t10", "t10_symbolic_diag.py", "t10/results/t10_1_diag.json"),
         ("t12", "t12", "t12_symbolic_diag.py", "t12/results/t12_symbolic_diag.json")]


def items(d):
    for k, v in d.items():
        if isinstance(v, list):
            for i, it in enumerate(v):
                if isinstance(it, dict) and "pass" in it:
                    yield k, i, it


def main():
    t0 = time.time()
    tmp = tempfile.mkdtemp(prefix="t13reg_")
    work = os.path.join(tmp, "classification")
    shutil.copytree(CLS, work, ignore=shutil.ignore_patterns("results", "figs", "figures", "__pycache__", "t13", "*.png", "*.pdf"))
    for _, d, _, _ in SCRIPTS:
        os.makedirs(os.path.join(work, d, "results"), exist_ok=True)
    R = {"by_task": {}, "fallbacks": []}
    for tag, d, s, out in SCRIPTS + DIAGS:
        t1 = time.time()
        p = subprocess.run(["python3", s], cwd=os.path.join(work, d), capture_output=True, text=True, timeout=7200)
        R.setdefault("runs", []).append({"script": f"{d}/{s}", "returncode": p.returncode, "seconds": time.time() - t1,
                                         "tail": p.stdout[-400:] + p.stderr[-400:]})
    data = {tag: json.load(open(os.path.join(work, out))) for tag, _, _, out in SCRIPTS}
    d10 = json.load(open(os.path.join(work, "t10/results/t10_1_diag.json")))
    d12 = json.load(open(os.path.join(work, "t12/results/t12_symbolic_diag.json")))
    total = passed = 0
    for tag, d in data.items():
        n_ok = n_all = 0
        fails = []
        for k, i, it in items(d):
            ok = bool(it["pass"])
            route = it.get("route")
            if not ok and tag == "t10" and k in ("c", "g"):
                ok = bool(d10[k].get("reduces") or d10[k].get("reduces_under_R2_lt_F"))
                route = "documented fallback: factor radicand (t10_symbolic_diag)"
                R["fallbacks"].append({"task": tag, "item": it["desc"], "ok": ok, "route": route})
            if not ok and tag == "t12" and "D2 post at dt->oo" in it["desc"]:
                ok = bool(d12.get("series_route_pass"))
                route = "documented fallback: series route (t12_symbolic_diag)"
                R["fallbacks"].append({"task": tag, "item": it["desc"], "ok": ok, "route": route})
            n_all += 1
            n_ok += ok
            if not ok:
                fails.append({"key": k, "desc": it["desc"], "route": route})
        R["by_task"][tag] = {"n": n_all, "n_pass": n_ok, "fails": fails, "script_pass_flag": d.get("pass")}
        total += n_all
        passed += n_ok
        print(tag, n_ok, "/", n_all, fails, flush=True)
    R["n"], R["n_pass"], R["pass"] = total, passed, total == passed
    R["seconds"] = time.time() - t0
    shutil.rmtree(tmp, ignore_errors=True)
    print("A-reg", "PASS" if R["pass"] else "FAIL", passed, "/", total)
    save_json(R, "t13_regression_symbolic.json")


if __name__ == "__main__":
    main()
