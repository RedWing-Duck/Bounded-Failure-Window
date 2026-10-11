"""Post-hoc diagnosis of the Part D failure for Task 10 (results/repro_task10_run1.log).
The replay ran every script listed in t10/run_t10.sh, then make_results_t10.py failed: it reads results/t10_2_diag.json,
which only t10_realize_diag.py writes, and run_t10.sh does not list that script. This script, in the replay's clean
checkout, runs the missing t10_realize_diag.py, re-runs make_results_t10.py with the original code hash, and compares the
regenerated RESULTS_t10.md with the committed one using the pre-registered comparison (compare_repro.compare).
Usage: python3 repro_t10_diag.py WORKDIR"""
import os
import subprocess
import sys
import time

from compare_repro import REPORTS, compare
from t13_common import CLS, save_json


def main():
    work = sys.argv[1]
    t10 = os.path.join(work, "classification", "t10")
    R = {"workdir": work, "cause": "t10/run_t10.sh omits t10_realize_diag.py; make_results_t10.py needs its t10_2_diag.json"}
    t0 = time.time()
    with open(os.path.join(t10, "results", "t10_realize_diag.log"), "w") as fh:
        R["realize_diag_rc"] = subprocess.run(["python3", "t10_realize_diag.py"], cwd=t10, stdout=fh, stderr=subprocess.STDOUT).returncode
    R["realize_diag_s"] = time.time() - t0
    mk = subprocess.run(["python3", "make_results_t10.py", "cbe96fe"], cwd=t10, capture_output=True, text=True)
    R["make_results_rc"], R["make_results_stderr"] = mk.returncode, mk.stderr[-2000:]
    if mk.returncode == 0:
        rel = REPORTS["10"]
        iss = compare(open(os.path.join(CLS, rel)).read(), open(os.path.join(work, "classification", rel)).read())
        R["issues"] = iss[:40]
        R["n_issues"] = len(iss)
        R["verdicts_identical"] = not any(i["kind"] == "verdicts" for i in iss)
        R["pass_after_fix"] = R["verdicts_identical"] and not iss
    R["text"] = (f"Task 10 (attribution: code, Task 10's run script). {R['cause']}. After running it in the clean checkout "
                 f"({R['realize_diag_s']:.0f} s), make_results_t10.py exit code {R['make_results_rc']}"
                 + (f"; comparison with the committed RESULTS_t10.md: {R['n_issues']} issues, verdicts identical "
                    f"{R['verdicts_identical']}." if mk.returncode == 0 else ".")
                 + (" The remaining difference is the provenance line's runtime list, which names t10_realize_diag in the "
                    "committed report (that script was run by hand in Task 10) and not in the replay; every verdict and result "
                    "number matches. RESULTS_t10.md's claim that run_t10.sh reproduces everything in one go is wrong."
                    if mk.returncode == 0 and R["n_issues"] == 1 and R["issues"][0]["line"] == 190 else ""))
    print(R["text"])
    for i in R.get("issues", [])[:8]:
        print("   ", str(i)[:400])
    save_json(R, "t13_repro_t10_diag.json")


if __name__ == "__main__":
    main()
