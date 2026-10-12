"""Task 16 register updates (Parts B and C; PREREG_t16.md). Run after t15/t15_register.py.
- results.yaml: every A-E-form legacy label prefixed "legacy " (C.1); result 5.6 verified_by in thesis numbering (C.3).
- crosswalk.md regenerated from results.yaml (same layout as t14/build_register.py); crosswalk_v1.yaml: "§A.3" -> "legacy §A.3".
- figures.yaml: the B.4 description's Pi_c set to the root recorded by Task 10 (t10/results/t10_2.json, mp.findroot at the
  figure's parameters), four significant figures (Part B). The script's 56.7 is its plotting-grid value.
Idempotent. Usage: python3 t16_register.py"""
import json
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REG = os.path.join(CLS, "register")
LABEL = re.compile(r"(?<!legacy )(?<![\w.§])([A-E]\.\d+)\b")


def prefix(s):
    return LABEL.sub(r"legacy \1", s)


def dump(path, data, width=200):
    head = "".join(l for l in open(path) if l.startswith("#"))
    with open(path, "w") as fh:
        fh.write(head)
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False, width=width, default_flow_style=None)


def main():
    p = os.path.join(REG, "results.yaml")
    res = yaml.safe_load(open(p))
    for e in res:
        e["legacy"] = [prefix(x) for x in e["legacy"]]
        if e["thesis_no"] == "5.6":
            e["verified_by"] = ["T8.1 (Corollary 3.3, excess identity)" if v == "T8.1 (Proposition 4)" else v
                                for v in e["verified_by"]]
    dump(p, res)
    cw = ["# Crosswalk: thesis numbers, keys, consolidated v1 numbers and legacy labels", "",
          "Legacy labels live only here (and, for the paper render of v1's change log, in `crosswalk_v1.yaml`). Thesis-facing "
          "documents use thesis numbers rendered from `results.yaml`. Every legacy label carries the prefix \"legacy\" (Task 16), "
          "so it cannot be read as a figure label B.n.", "", "| No. | Key | Cons. v1 | Legacy |", "|---|---|---|---|"]
    for e in res:
        cw.append(f"| {e['thesis_no']} | `{e['key']}` | {e['cons_v1'] or '—'} | {'; '.join(e['legacy'])} |")
    open(os.path.join(REG, "crosswalk.md"), "w").write("\n".join(cw) + "\n")
    p1 = os.path.join(REG, "crosswalk_v1.yaml")
    t = open(p1).read()
    t = re.sub(r"(?<!legacy )§A\.3 limits table", "legacy §A.3 limits table", t)
    open(p1, "w").write(t)
    pic = json.load(open(os.path.join(CLS, "t10", "results", "t10_2.json")))["a13_supp"][0]["Pi_c"]
    pf = os.path.join(REG, "figures.yaml")
    figs = yaml.safe_load(open(pf))
    for e in figs:
        if e["label"] == "B.4":
            e["description"] = re.sub(r"Pi_c = [\d.]+", f"Pi_c = {pic:#.4g}", e["description"])
    head = "".join(l for l in open(pf) if l.startswith("#"))
    with open(pf, "w") as fh:
        fh.write(head)
        yaml.safe_dump(figs, fh, allow_unicode=True, sort_keys=False, width=200)
    print(f"legacy labels prefixed; 5.6 verified_by rewritten; B.4 Pi_c = {pic:#.4g}")


if __name__ == "__main__":
    main()
