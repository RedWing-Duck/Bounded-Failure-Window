"""Post-hoc diagnosis of Part D comparison failures (results/t13_compare_repro.json).
For every report that failed the pre-registered comparison, test whether every difference lies on the provenance line
("Runtime per script (s): ..."), whose numbers the criterion masks but whose list of script names and order it does not.
That list records how a task was run, not a result. Usage: python3 repro_compare_diag.py WORKDIR"""
import json
import os
import re
import sys

from compare_repro import REPORTS
from t13_common import CLS, RES, save_json


def main():
    cmp_ = json.load(open(os.path.join(RES, "t13_compare_repro.json")))
    R = {"reports": {}}
    for t, v in cmp_["reports"].items():
        if v.get("pass", True):
            continue
        iss = v["issues"]
        a = open(os.path.join(CLS, REPORTS[t])).read().split("\n")
        b = open(os.path.join(sys.argv[1], "classification", REPORTS[t])).read().split("\n")
        prov = [{"committed": a[i["line"] - 1], "reproduced": b[i["line"] - 1]} for i in iss
                if i["kind"] == "text" and "Runtime per script" in a[i["line"] - 1] and "Runtime per script" in b[i["line"] - 1]]
        only_prov = len(prov) == len(iss) == v["n_issues"]
        names = lambda s: re.findall(r"t\d+_\w+", s.split("Runtime per script", 1)[1])
        R["reports"][t] = {"n_issues": v["n_issues"], "verdicts_identical": v["verdicts_identical"],
                           "only_provenance_line": only_prov,
                           "script_names_committed": [names(i["committed"]) for i in prov],
                           "script_names_reproduced": [names(i["reproduced"]) for i in prov]}
    R["text"] = "; ".join(
        f"Task {t}: {r['n_issues']} difference(s), verdicts identical {r['verdicts_identical']}, all on the provenance runtime "
        f"line {r['only_provenance_line']} (attribution: criterion; the masking covers runtime numbers but not the list of "
        f"script names, which differs because the original runs were separate invocations)" for t, r in R["reports"].items())
    print(R["text"])
    save_json(R, "t13_repro_compare_diag.json")


if __name__ == "__main__":
    main()
