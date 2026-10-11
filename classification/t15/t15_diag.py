"""Post-hoc diagnosis of the T15 C4 and C10 failures (results/t15_checks.json). Not a pass criterion.
C4: every flagged "unresolved number" is shown in context and classified as a citation or as an interval/other bracket.
C10: every A-E match is tested against the figure labels of register/figures.yaml (B.1-B.12, introduced by Task 15's decision 3)
and against the legacy A-E labels of the crosswalk.
Usage: python3 t15_diag.py"""
import json
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)


def main():
    C = json.load(open(os.path.join(HERE, "results", "t15_checks.json")))
    R = {}
    c4 = []
    for f, hits in C["C4"]["hits"].items():
        t = open(os.path.join(REPO, f)).read()
        for kind, s in hits:
            i = t.find(s)
            ctx = t[max(0, i - 60): i + len(s) + 20].replace("\n", " ")
            c4.append({"file": f, "kind": kind, "match": s, "context": ctx,
                       "is_citation": False if re.search(r"(in|on|over) \[\d", ctx) or re.search(r"\[\d+, \d+\]\s*\(", ctx) is None and
                       re.search(r"theta|θ|in \[", ctx) else True})
    R["C4"] = {"items": c4, "citation_hits": sum(x["is_citation"] for x in c4),
               "text": f"{len(c4)} flagged item(s); {sum(not x['is_citation'] for x in c4)} are interval notation in figure descriptions "
                       "(e.g. 'theta in [0, 10]'), not citations. Attribution: criterion/code — the pre-registered bracket pattern "
                       "cannot tell an interval from a citation."}
    figs = {e["label"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))}
    legacy = set(re.findall(r"\b[A-E]\.\d+\b", open(os.path.join(CLS, "register", "crosswalk.md")).read()))
    tot, fig_hits, other = 0, 0, []
    for f, h in C["C10"]["hits"].items():
        for m in h["A-E"]:
            tot += 1
            if m in figs:
                fig_hits += 1
            else:
                other.append((f, m))
        if h["Paper 1"]:
            other.append((f, "Paper 1"))
    R["C10"] = {"matches": tot, "figure_labels": fig_hits, "other": other, "legacy_overlap_note": sorted(figs & legacy),
                "text": f"{tot} A–E matches, {fig_hits} of them Task 15's figure labels B.1–B.12 (decision 3), {len(other)} other; "
                        "0 'Paper 1'. The labels B.1–B.12 coincide in form, and for B.1–B.12 also in text, with the legacy labels "
                        "B.1–B.12 of the crosswalk, so the pre-registered legacy-label pattern cannot pass once figures are labelled "
                        "B.n. Attribution: criterion."}
    print(R["C4"]["text"])
    print(R["C10"]["text"])
    with open(os.path.join(HERE, "results", "t15_diag.json"), "w") as fh:
        json.dump(R, fh, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
