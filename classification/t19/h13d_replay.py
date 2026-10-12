"""Task 19, H-13.D: the Task 13 Part D reproduction of Tasks 10 and 12, corrected per the Task 13 diagnosis (PREREG_t19.md).
A clean git worktree of the commit the Task 13 replay used (7195070) is created in the scratch directory, and in it:
  Task 10: bash t10/run_t10.sh cbe96fe (its last step, make_results_t10.py, fails as diagnosed), then the omitted
           python3 t10_realize_diag.py, then python3 make_results_t10.py cbe96fe;
  Task 12: bash t12/run_t12.sh 82edc1b.
The regenerated RESULTS_t10.md and RESULTS_t12.md are compared with the committed ones by t13/compare_repro.compare (unchanged),
after one added masking: the provenance line "Runtime per script (s): ..." is replaced by a placeholder in both texts (it records
how a task was invoked, which the Task 13 diagnosis found differs between separate invocations and one chain).
Pass: for both reports, every verdict identical and 0 remaining issues.
Usage: python3 h13d_replay.py [--dry]   (--dry: worktree and comparison of the committed reports with themselves only)"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
DRY = "--dry" in sys.argv
RES = os.path.join(HERE, "results", "dry" if DRY else "", "h")
SCR = os.environ.get("T19_SCRATCH", "/tmp/claude-0/t19")
COMMIT = "7195070"
sys.path.insert(0, os.path.join(CLS, "t13"))
from compare_repro import REPORTS, compare  # noqa: E402

PROV = re.compile(r"^.*Runtime per script \(s\):.*$", re.M)


def run(cmd, cwd, log):
    t0 = time.time()
    with open(log, "w") as fh:
        rc = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    return rc, round(time.time() - t0, 1)


def main():
    os.makedirs(RES, exist_ok=True)
    wt = os.path.join(SCR, "repro19")
    if os.path.exists(wt):
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO, capture_output=True)
        shutil.rmtree(wt, ignore_errors=True)
    os.makedirs(SCR, exist_ok=True)
    subprocess.run(["git", "worktree", "add", "--detach", wt, COMMIT], cwd=REPO, check=True, capture_output=True)
    wcls = os.path.join(wt, "classification")
    R = {"commit": COMMIT, "workdir": wt, "steps": {}}
    logs = os.path.join(RES, "h13d_logs")
    os.makedirs(logs, exist_ok=True)
    if not DRY:
        R["steps"]["t10_run_script"] = run(["bash", "t10/run_t10.sh", "cbe96fe"], wcls, os.path.join(logs, "t10_run.log"))
        R["steps"]["t10_realize_diag"] = run(["python3", "t10_realize_diag.py"], os.path.join(wcls, "t10"), os.path.join(logs, "t10_realize_diag.log"))
        R["steps"]["t10_make_results"] = run(["python3", "make_results_t10.py", "cbe96fe"], os.path.join(wcls, "t10"), os.path.join(logs, "t10_make.log"))
        R["steps"]["t12_run_script"] = run(["bash", "t12/run_t12.sh", "82edc1b"], wcls, os.path.join(logs, "t12_run.log"))
    R["reports"] = {}
    for t in ("10", "12"):
        rel = REPORTS[t]
        a = open(os.path.join(CLS, rel)).read()
        b = open(os.path.join(wcls if not DRY else CLS, rel)).read() if os.path.exists(os.path.join(wcls, rel)) else None
        if b is None:
            R["reports"][t] = {"status": "not regenerated", "pass": False}
            continue
        raw = compare(a, b)
        iss = compare(PROV.sub("<provenance runtime list>", a), PROV.sub("<provenance runtime list>", b))
        verd = not any(i["kind"] == "verdicts" for i in iss)
        R["reports"][t] = {"file": rel, "issues_unmasked_provenance": len(raw), "n_issues": len(iss), "issues": iss[:40],
                           "verdicts_identical": verd, "pass": verd and not iss}
    R["pass"] = all(v.get("pass") for v in R["reports"].values())
    json.dump(R, open(os.path.join(RES, "H-13.D.json"), "w"), indent=1, default=str)
    print(json.dumps({"id": "H-13.D", "pass": R["pass"], "steps": R["steps"]}))
    for t in ("10", "12"):     # keep the regenerated reports and runtime tables next to the logs
        for f in (REPORTS[t], f"t{t}/results/runtime.tsv"):
            p = os.path.join(wcls, f)
            if os.path.exists(p) and not DRY:
                shutil.copy(p, os.path.join(logs, f.replace("/", "__")))
    subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO, capture_output=True)


if __name__ == "__main__":
    main()
