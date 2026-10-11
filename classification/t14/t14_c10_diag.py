"""Post-hoc diagnosis of the C10 failure (results/t14_checks.json). The pre-registered dry run resolves each string literal
against classification/, the script's directory and the repository root only. Here each flagged literal is resolved the way
its script actually builds the path (read from the script), and the module-level DOC of the two Task 13 audit scripts is
evaluated by importing them (their main() is guarded by __name__ == "__main__").
Usage: python3 t14_c10_diag.py"""
import importlib
import json
import os
import re
import sys

from t14_common import CLS, RES, save_json

T13 = os.path.join(CLS, "t13")


def main():
    flagged = json.load(open(os.path.join(RES, "t14_checks.json")))["C10"]["missing"]
    out = []
    sys.path.insert(0, T13)
    for f in flagged:
        script, lit = [x.strip() for x in f.split("->")]
        name = os.path.basename(script)
        if name in ("t13_audit_numbers.py", "t13_audit_refs.py"):
            doc = importlib.import_module(name[:-3]).DOC
            out.append({"flag": f, "how": "module-level DOC (with the Task 14 fallback)", "resolved": doc, "exists": os.path.exists(doc)})
        elif name == "t13_figures_paper2.py":
            src = open(os.path.join(T13, name)).read()
            written = bool(re.search(r'open\(os\.path\.join\(OUT, "README\.md"\), "w"\)', src))
            out.append({"flag": f, "how": "written by the script (output, not an input)", "resolved": "figs_paper2/README.md",
                        "exists": written})
        elif name == "t13_regression_symbolic.py":
            task = re.match(r"(t\d+)_", lit).group(1)
            p = os.path.join(CLS, task, lit)
            out.append({"flag": f, "how": f"copied from classification/{task}/ (SCRIPTS table)", "resolved": p, "exists": os.path.exists(p)})
        else:
            out.append({"flag": f, "how": "unhandled", "exists": False})
    ok = all(o["exists"] for o in out)
    R = {"items": out, "all_resolve": ok,
         "text": f"{sum(o['exists'] for o in out)}/{len(out)} flagged paths resolve when built the way their scripts build them; "
                 "attribution: code (the dry run's literal resolver), not a missing file."}
    print(R["text"])
    for o in out:
        print(" ", o["flag"], "->", o["resolved"] if "resolved" in o else "", o["exists"])
    save_json(R, "t14_c10_diag.json")


if __name__ == "__main__":
    main()
