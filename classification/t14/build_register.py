"""Task 14 §2: build register/results.yaml, register/tasks.yaml and register/crosswalk.md.
Input: t14/input/register_table.csv (the prompt's 82-row table, verbatim), §12 of archive/Stages_0_4_Consolidated_v1.md
(verified_by for consolidated results) and the starting study's verification/REPORT.md (Tasks 1-7; mapping below).
Usage: python3 build_register.py"""
import csv
import os
import re

import yaml

from t14_common import CLS, REPO

V1 = os.path.join(CLS, "archive", "Stages_0_4_Consolidated_v1.md")
if not os.path.exists(V1):
    V1 = os.path.join(CLS, "Stages_0_4_Consolidated.md")
REG = os.path.join(CLS, "register")

# Tasks 1-7 checks per starting-study result, read from verification/REPORT.md:
# T1.1/T1.1b + T2 (stationary variance), T1.8 (excess identity), T1.4-T1.7 + T3 + T4d (window), T1.6 + T7.2a (optimal gain,
# envelope), T1.3-T1.5 + T1.9 + T3 + T7.2b-d (Bayesian weight), T4b + T6 C1/C3 (coloured relay variance), T4a + T7.1e
# (discrete excess), T4e (precision-blind), T4d + T7.2e (Hill).
PHASE1 = {"stationary-variance": ["T1", "T2"], "excess-identity": ["T1"], "window-theorem": ["T1", "T3", "T4"],
          "optimal-envelope": ["T1", "T7"], "bayesian-weight": ["T1", "T3", "T7"], "tau-relay-variance": ["T4", "T6"],
          "discrete-excess": ["T4", "T7"], "precision-blind": ["T4"], "hill-turning-points": ["T4", "T7"]}
EXTRA = {"no-mixed-decreasing-ratio": ["T13 C2 (row-8 diagnosis, t13_audit_classes_diag2.py)"]}
CIT = [(["stationary-variance", "excess-identity"], "heffes1966, friedland1967, nishimura1967, griffin1968, sangsukiam1990, ge2016, deyst1968, kurt2025"),
       (["optimal-envelope", "single-minimum-gain"], "kalmanbucy1961, kalman1960, andersonmoore1979"),
       (["normal-form"], "kalata1984"), (["bayesian-weight"], "ernstbanks2002, friston2010"), (["discrete-excess"], "sahomasugi2016"),
       (["tau-relay-variance", "tau-optimal-error"], "brysonjohansen1965, brysonhenrikson1968, chang2014"),
       (["matched-variance-optimal", "power-family-sharpness"], "shmaliy2020, ren2021"),
       (["critical-tolerance", "signature"], "edelsbrunnerharer2010, carr2003, milnor1963, edelsbrunner2002, oudot2015"),
       (["structural-stability"], "cohensteiner2007"),
       (["realizability"], "hotzskelton1987, hotzskelton1985, collinsskelton1987, xuskelton1992, yasuda1993, skeltonikeda1989"),
       (["hill-turning-points", "hill-classification"], "heeger1992, carandiniheeger2012"),
       (["causal-monotonicity", "causal-garbling"], "blackwell1951, blackwell1953, greenshtein1996, yuksellinder2012, yukselbasar2013, yukselbasar2024, lecam1964, torgersen1991"),
       (["spectral-dominance", "gaussian-orderings-coincide"], "hansentorgersen1974, torgersen1991, hogeboomburr2021"),
       (["latency", "pathwise-not-enough"], "barshalom2002, yoder2018"), (["dt-optimal-mp", "mp-not-ordered"], "martinezrey2017"),
       (["window-theorem"], "singh2009, boominathan2022, teunissen2021, crouse2023")]
THESIS_ONLY = {"2.3", "2.8", "2.9", "3.2", "6.5"}


def split_top(s, seps=(";", ",")):  # split at top-level separators
    out, depth, cur = [], 0, ""
    for ch in s:
        depth += ch == "("
        depth -= ch == ")"
        if ch in seps and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    merged = []
    for x in out:   # a piece not naming a task continues the previous item (e.g. "T13 A1, A2 (b)")
        if merged and not re.match(r"^(T\d|Paper 1)", x):
            merged[-1] += ", " + x
        else:
            merged.append(x)
    return [x for x in merged if x and x != "—"]


def section12():
    txt = open(V1).read().split("## 12. Verification appendix")[1].split("**Route notes.**")[0]
    rows = {}
    for ln in txt.split("\n"):
        m = re.match(r"^\| (\d+) \| [^|]+ \| [^|]+ \| (.+) \|$", ln)
        if m:
            rows[int(m.group(1))] = m.group(2).strip()
    return rows


def lead_int(s):
    m = re.match(r"^(\d+)(\s|$)", s)
    return int(m.group(1)) if m else None


def main():
    tab = list(csv.DictReader(open(os.path.join(CLS, "t14", "input", "register_table.csv"))))
    v12 = section12()
    cites = {}
    for keys, s in CIT:
        for k in keys:
            cites.setdefault(k, []).extend(x.strip() for x in s.split(","))
    out = []
    for r in tab:
        k, no, typ = r["key"], r["thesis_no"], r["type"]
        cv = None if r["cons_v1"] == "—" else r["cons_v1"]
        n = lead_int(cv) if cv else None
        vb = list(PHASE1.get(k, []))
        if n is not None and k != "no-mixed-decreasing-ratio":
            vb += [x for x in split_top(v12[n]) if x != "Paper 1"]
        vb += EXTRA.get(k, [])
        if no in THESIS_ONLY:
            vb = []
        status = ("definition" if typ == "Definition" else "to-verify" if no in THESIS_ONLY else
                  {"Numerical result": "numerical", "Conjecture": "conjecture"}.get(typ, "proved"))
        out.append({"key": k, "thesis_no": no, "type": typ, "title": r["title"], "chapter": int(no.split(".")[0]),
                    "cons_v1": cv, "legacy": [x.strip() for x in r["legacy"].split(" / ")],
                    "verified_by": vb, "status": status, "citations": cites.get(k, [])})
    os.makedirs(REG, exist_ok=True)
    with open(os.path.join(REG, "results.yaml"), "w") as fh:
        fh.write("# Register of results (single source of truth for numbering). Freeze v1, Task 14.\n"
                 "# thesis_no: chapter.counter, one counter per chapter shared by all types. Keys are permanent.\n"
                 "# cons_v1: number in archive/Stages_0_4_Consolidated_v1.md (or a note); legacy: earlier labels (crosswalk only).\n")
        yaml.safe_dump(out, fh, allow_unicode=True, sort_keys=False, width=200, default_flow_style=None)
    tasks = []
    T17 = {"pre": "d21f193", "res": "70ebb55", "file": "verification/PREREG.md", "rep": "verification/REPORT.md"}
    for t in range(1, 6):
        tasks.append({"task": f"T{t}", "prereg_file": T17["file"], "prereg_commit": T17["pre"], "results_commit": T17["res"],
                      "report": T17["rep"]})
    tasks.append({"task": "T6", "prereg_file": "verification/PREREG_t6.md", "prereg_commit": "824ca06", "results_commit": "0944b81",
                  "report": "verification/REPORT.md (Task 6 section)", "note": "results commit read from the git log (not in Appendix B)"})
    tasks.append({"task": "T7", "prereg_file": "verification/PREREG_t7.md", "prereg_commit": "a0d2be2", "results_commit": "2f9da71",
                  "report": "verification/REPORT.md (Task 7 section)"})
    for t, pre, res, rep in [(8, "d8fa786", "83b9455", "classification/REPORT.md"), (9, "2555442", "238c15f", "classification/t9/RESULTS_t9.md"),
                             (10, "da3d826", "cbe96fe", "classification/t10/RESULTS_t10.md"), (11, "5337c2e", "e4ce89c", "classification/t11/RESULTS_t11.md"),
                             (12, "6e09e88", "82edc1b", "classification/t12/RESULTS_t12.md"), (13, "296a797", "d683915", "classification/t13/RESULTS_t13.md")]:
        tasks.append({"task": f"T{t}", "prereg_file": f"classification/PREREG_t{t}.md", "prereg_commit": pre, "results_commit": res, "report": rep})
    with open(os.path.join(REG, "tasks.yaml"), "w") as fh:
        fh.write("# Verification tasks T1-T13. Tasks 1-5 share one pre-registration and one results commit (starting study, Appendix B).\n")
        yaml.safe_dump(tasks, fh, allow_unicode=True, sort_keys=False, width=200)
    cw = ["# Crosswalk: thesis numbers, keys, consolidated v1 numbers and legacy labels", "",
          "Legacy labels live only here (and, for the paper render of v1's change log, in `crosswalk_v1.yaml`). Thesis-facing "
          "documents use thesis numbers rendered from `results.yaml`.", "", "| No. | Key | Cons. v1 | Legacy |", "|---|---|---|---|"]
    for e in out:
        cw.append(f"| {e['thesis_no']} | `{e['key']}` | {e['cons_v1'] or '—'} | {'; '.join(e['legacy'])} |")
    open(os.path.join(REG, "crosswalk.md"), "w").write("\n".join(cw) + "\n")
    print(len(out), "results;", len(tasks), "tasks")


if __name__ == "__main__":
    main()
