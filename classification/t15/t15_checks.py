"""Task 15 checks C1-C10 and C13 (PREREG_t15.md, commit aa0b914); C11/C12 are read from results/t15_partG.json.
Also records Part H.2 (manuscript PDF facts and errata page numbers). Usage: python3 t15_checks.py"""
import csv
import glob
import hashlib
import importlib
import json
import os
import pickle
import re
import subprocess
import sys
import time

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
RES = os.path.join(HERE, "results")
sys.path[:0] = [os.path.join(CLS, "register"), HERE]
import bibfmt  # noqa: E402
import fig_harness  # noqa: E402

THESIS_RENDERS = [os.path.join(CLS, f) for f in ("Stages_0_4_Thesis.md", "Roadmap_v3.md", "Appendix_A_Register.md",
                  "Appendix_B_Figures.md", "Appendix_C_References.md", "Appendix_D_Verification.md", "Appendix_E_Reproduction.md")] + \
    sorted(glob.glob(os.path.join(CLS, "figs_thesis", "*.txt"))) + [os.path.join(CLS, "figs_thesis", "README.md")] + \
    [os.path.join(REPO, "reference", "phase1", f) for f in ("README.md", "ERRATA.md")]
SOURCES = sorted(glob.glob(os.path.join(CLS, "source", "**", "*.*"), recursive=True)) + [os.path.join(CLS, "register", "matrix.csv")]
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_ch1-4.md")


def rel(p):
    return os.path.relpath(p, REPO)


def bib():
    return bibfmt.parse(os.path.join(CLS, "references.bib"))


def c1():
    B = bib()
    txt = open(os.path.join(CLS, "references.bib")).read()
    reg = yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))
    refs = yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))
    attached = {c for e in reg for c in e["citations"]}
    cited = set()
    for p in SOURCES:
        for m in re.finditer(r"\[(@[^\]]+)\]", open(p).read()):
            cited |= {k.strip().lstrip("@") for k in m.group(1).split(";")}
    planned = {r["key"] for r in refs if r["status"] == "planned"}
    used = attached | cited | planned
    out = {"entries": len(B), "doi": sum("doi" in f for f in B.values()), "verify": txt.count("VERIFY"),
           "dangling": sorted((attached | cited) - set(B)), "unused": sorted(set(B) - used),
           "attachments": {k: [e["key"] for e in reg if k in e["citations"]] for k in ("jazwinski1970", "simon2006")}}
    out["pass"] = out["entries"] == 53 and out["doi"] == 46 and out["verify"] == 0 and not out["dangling"] and not out["unused"]
    return out


FROZEN_TABLE = ["kalmanbucy1961", "ernstbanks2002", "friston2010", "heffes1966", "friedland1967", "nishimura1967", "griffin1968",
                "sangsukiam1990", "ge2016", "teunissen2021", "crouse2023", "singh2009", "boominathan2022", "hotzskelton1987",
                "xuskelton1992", "heeger1992", "carandiniheeger2012", "blackwell1951", "blackwell1953", "greenshtein1996",
                "yuksellinder2012", "yukselbasar2013", "yukselbasar2024", "hansentorgersen1974", "kalata1984", "sahomasugi2016",
                "brysonjohansen1965", "brysonhenrikson1968", "jazwinski1970", "edelsbrunnerharer2010", "cohensteiner2007", "carr2003",
                "milnor1963", "edelsbrunner2002", "oudot2015", "deyst1968", "kurt2025", "simon2006", "kalman1960", "andersonmoore1979",
                "hotzskelton1985", "collinsskelton1987", "yasuda1993", "skeltonikeda1989", "chang2014", "shmaliy2020", "ren2021",
                "martinezrey2017", "lecam1964", "torgersen1991", "hogeboomburr2021", "barshalom2002", "yoder2018"]


def c2():
    R = yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))
    nums = [r["number"] for r in R]
    keys = [r["key"] for r in R]
    out = {"n": len(R), "numbers_1_53": sorted(nums) == list(range(1, 54)), "unique_keys": len(set(keys)) == len(keys),
           "bijection_with_bib": set(keys) == set(bib()), "matches_frozen_table": [r["key"] for r in sorted(R, key=lambda r: r["number"])] == FROZEN_TABLE,
           "status_ok": all((r["status"] == "planned") == (r["number"] >= 46) for r in R)}
    out["pass"] = all(v for k, v in out.items() if k != "n") and out["n"] == 53
    return out


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"\\([^A-Za-z0-9\s])", r"\1", s.replace("&#91;", "["))).strip()


def c3():
    mine = [norm(l) for l in open(os.path.join(CLS, "Appendix_C_References.md")).read().split("\n") if re.match(r"^\[\d+\]", l)]
    d = open(DRAFT).read().split("**Appendix C")[1].split("**Appendix D")[0]
    theirs = [norm(l) for l in d.split("\n") if l.strip().startswith("&#91;")]
    diff = [(i + 1, a, b) for i, (a, b) in enumerate(zip(mine, theirs)) if a != b]
    return {"lines_render": len(mine), "lines_draft": len(theirs), "differences": diff[:10], "pass": len(mine) == len(theirs) == 53 and not diff}


AY = [re.compile(r"\b[A-Z][\w–'-]+ \((19|20)\d\d[a-z]?\)"), re.compile(r"\b[A-Z][a-z]+ (and|&) [A-Z][a-z]+\b[^.\n]{0,60}?\b(19|20)\d\d\b"),
      re.compile(r"et al\.")]


def c4():
    keys = set(bib())
    refs = {r["number"] for r in yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))}
    hits = {}
    for p in THESIS_RENDERS:
        if p.endswith("Appendix_C_References.md"):
            continue
        t = open(p).read()
        if p.endswith("Roadmap_v3.md"):   # rows 6-10 of section 7 quote search results as returned (excluded, disclosure 4)
            t = "\n".join(l for l in t.split("\n") if not re.match(r"^\| (6|7|8|9|10) \| ", l))
        h = []
        h += [("raw key", k) for k in keys if re.search(r"(?<![\w/.-])" + re.escape(k) + r"(?![\w-])", t)]
        for rx in AY:
            h += [("author-year", m.group(0)) for m in rx.finditer(t)]
        h += [("token", m.group(0)) for m in re.finditer(r"\[@", t)]
        for m in re.finditer(r"(?<![\w\]\\])\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\](?!\()", t):
            for part in m.group(1).split(", "):
                a, _, b = part.partition("–")
                for n in range(int(a), int(b or a) + 1):
                    if n not in refs:
                        h.append(("unresolved number", m.group(0)))
        if h:
            hits[rel(p)] = h
    return {"files": len(THESIS_RENDERS) - 1, "hits": hits, "pass": not hits}


NUMRX = re.compile(r"(Theorem|Proposition|Prop\.|Lemma|Corollary|Cor\.|Figure|Fig\.)\s*\d")


def load_caps():
    caps = {}
    for f in ("cap_new_t13.pkl", "cap_new_t8.pkl", "cap_B2.pkl"):
        caps.update(pickle.load(open(os.path.join(RES, f), "rb")))
    return caps


def c5():
    caps = load_caps()
    labels = {f"{e['label']}_{e['key']}" for e in yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))}
    hits = {k: [t for t in v["texts"] if NUMRX.search(t[1])] for k, v in caps.items() if k in labels}
    hits = {k: v for k, v in hits.items() if v}
    return {"figures_inspected": sorted(k for k in caps if k in labels), "n": sum(k in labels for k in caps),
            "text_elements": sum(len(v["texts"]) for k, v in caps.items() if k in labels), "hits": hits,
            "pass": not hits and sum(k in labels for k in caps) == 12}


def c6():
    import make_fig_B2 as B
    out = {"touch": {}, "r1": None, "ordering_violations": 0, "negative_q_drawn": 0}
    for r in (0.5,):
        nuR = B.nu_R(r)
        qm, qp = B.branches(np.array([nuR]), r)
        qs = B.q_star(nuR)
        out["touch"][str(r)] = {"nu_R": nuR, "q_minus": float(qm[0]), "q_plus": float(qp[0]), "q_star": float(qs),
                                "ok": max(abs(qm[0] - r), abs(qp[0] - r), abs(qs - r)) <= 1e-9}
    qm, qp = B.branches(np.logspace(-2, 3, 10000), 1.0)
    out["r1"] = bool(np.allclose(qm, 0, atol=1e-12) and np.allclose(qp, 2, atol=1e-12))
    nu = np.logspace(-2, 3, 10000)
    for r in B.RS:
        qm, qp = B.branches(nu, r)
        ok = np.isfinite(qm) & np.isfinite(qp)
        qs = B.q_star(nu[ok])
        out["ordering_violations"] += int(np.sum((qm[ok] > qs + 1e-12) | (qs > qp[ok] + 1e-12)))
    for k, (x, y) in B.curves().items():
        out["negative_q_drawn"] += int(np.sum(np.asarray(y) < 0))
    caps = pickle.load(open(os.path.join(RES, "cap_B2.pkl"), "rb"))["B.2_normal-form-plane"]
    out["negative_q_in_figure_lines"] = int(sum(np.sum(a[:, 1] < 0) for t, a in caps["arrays"] if t == "line" and a.ndim == 2))
    out["pass"] = all(v["ok"] for v in out["touch"].values()) and out["r1"] and out["ordering_violations"] == 0 and \
        out["negative_q_drawn"] == 0 and out["negative_q_in_figure_lines"] == 0
    return out


def eq_arrays(a, b):
    if a.shape != b.shape:
        return False
    a, b = np.asarray(a, float), np.asarray(b, float)
    nan = np.isnan(a) | np.isnan(b)
    if np.any(np.isnan(a) != np.isnan(b)):
        return False
    a, b = a[~nan], b[~nan]
    return bool(np.all(np.abs(a - b) <= 1e-12 * np.maximum(1, np.maximum(np.abs(a), np.abs(b)))))


def c7():
    """Run the original scripts unchanged (output redirected to a scratch directory) and compare arrays."""
    scratch = os.path.join(RES, "scratch_orig")
    os.makedirs(scratch, exist_ok=True)
    src = open(os.path.join(CLS, "t13", "t13_figures_paper2.py")).read()
    src = src.replace('OUT = os.path.join(CLS, "figs_paper2")', f'OUT = {scratch!r}')
    old13 = fig_harness.capture(os.path.join(CLS, "t13", "t13_figures_paper2.py"), os.path.join(RES, "cap_old_t13.pkl"), source=src,
                                cwd=os.path.join(CLS, "t13"))

    def setup():
        import t8_common
        importlib.reload(t8_common)
        t8_common.FIG = scratch
    old8 = fig_harness.capture(os.path.join(CLS, "t8_figures.py"), os.path.join(RES, "cap_old_t8.pkl"), setup=setup, cwd=CLS)
    old = {**old13, **old8}
    new = load_caps()
    F = yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))
    res = {}
    for e in F:
        if not e["source_file"]:
            continue
        o, n = old.get(os.path.basename(e["source_file"])), new.get(f"{e['label']}_{e['key']}")
        if o is None or n is None:
            res[e["label"]] = {"ok": False, "why": "missing capture"}
            continue
        same = len(o["arrays"]) == len(n["arrays"]) and all(ta == tb and eq_arrays(a, b) for (ta, a), (tb, b) in zip(o["arrays"], n["arrays"]))
        tdiff = [(a, b) for a, b in zip(o["texts"], n["texts"]) if a != b]
        res[e["label"]] = {"ok": same, "n_arrays": len(n["arrays"]), "text_changes": tdiff,
                           "text_count_old_new": [len(o["texts"]), len(n["texts"])]}
    return {"figures": res, "pass": all(v["ok"] for v in res.values()) and len(res) == 11}


def c8():
    s = open(os.path.join(CLS, "source", "Roadmap_v3_Source.md")).read()
    import make_sources_t15 as M
    exp = M.PART_D
    detok = lambda t: re.sub(r"\[(@[^\]]+)\]", lambda m: ", ".join(k.strip().lstrip("@") for k in m.group(1).split(";")), t)
    prompt = open(os.path.join(HERE, "input", "Task_15_Repo_Sync_Prompt.md")).read()
    ptab = [l for l in prompt.split("## Part D")[1].split("## Part E")[0].split("\n") if re.match(r"^\| (#|---|1[1-7]) ", l)]
    sec7 = s.split("## 7. Novelty")[1]
    srows = [detok(l) for l in sec7.split("\n") if re.match(r"^\| 1[1-7] \| ", l)]
    ok_rows = [l for l in ptab if l.startswith("| 1")] == [l for l in srows if l.startswith("| 1")]
    line = "Second-set priority combination searches: all four returned no prior work. 'No close prior found' describes these searches, not worldwide novelty."
    after = line in s and s.index(line) > s.index("| 17 | The framework")
    gone = not any("query text not supplied" in open(p).read() for p in SOURCES + THESIS_RENDERS)
    old = subprocess.run(["git", "-C", REPO, "show", "77a939c:classification/source/Roadmap_v3_Source.md"], capture_output=True, text=True).stdout
    same610 = [l for l in old.split("\n") if re.match(r"^\| (6|7|8|9|10) \| (steady|Kalman|mismatched|measurement)", l)] == \
              [l for l in s.split("\n") if re.match(r"^\| (6|7|8|9|10) \| (steady|Kalman|mismatched|measurement)", l)]
    return {"rows_11_17_equal": ok_rows, "n_prompt_rows": sum(l.startswith("| 1") for l in ptab), "line_after_table": after,
            "query_text_phrase_gone": gone, "rows_6_10_unchanged": same610, "pass": ok_rows and after and gone and same610}


def c9():
    hits = []
    for p in SOURCES + THESIS_RENDERS + [os.path.join(CLS, "Stages_0_4_Paper2.md")]:
        for i, l in enumerate(open(p).read().split("\n"), 1):
            for m in re.finditer(r"Appendix [BC]\b", l):
                old_sense = re.search(r"Appendix [BC]\b[^.]{0,40}(verification|reproduc)", l, re.I) or \
                            re.search(r"(verification|reproduc)\w*[^.]{0,20}\(?Appendix [BC]\b", l, re.I)
                manuscript = re.search(r"manuscript'?s? (own )?Appendix", l)
                hits.append({"file": rel(p), "line": i, "text": l.strip()[:160], "old_sense": bool(old_sense) and not manuscript})
    files = [os.path.exists(os.path.join(CLS, f)) for f in ("Appendix_A_Register.md", "Appendix_B_Figures.md", "Appendix_C_References.md",
                                                             "Appendix_D_Verification.md", "Appendix_E_Reproduction.md")]
    old = [h for h in hits if h["old_sense"]]
    return {"mentions": hits, "old_sense": old, "files_present": sum(files), "pass": not old and all(files)}


def c10():
    per = {}
    for p in THESIS_RENDERS:
        t = re.sub(r"\s+", " ", open(p).read())
        h = {"Paper 1": t.count("Paper 1"), "A-E": re.findall(r"\b[A-E]\.\d+\b", t)}
        if h["Paper 1"] or h["A-E"]:
            per[rel(p)] = h
    return {"files": len(THESIS_RENDERS), "hits": per, "pass": not per}


def c13():
    rs = open(os.path.join(CLS, "reproduce_all.sh")).read()
    run = re.findall(r'\[(\d+)\]="([^"]+)"', rs.split("declare -A RUN=")[1].split("\n")[0])
    outputs = re.compile(r"^(REPORT\.md|RESULTS_t\d+\.md)$|(^|/)(results|figs[\w]*|figures)/")
    checked, unresolved, how = 0, [], {}
    for t, path in run:
        p = os.path.join(CLS, path)
        checked += 1
        if not os.path.exists(p):
            unresolved.append(path)
            continue
        d = os.path.dirname(p)
        sh = open(p).read()
        names = set()
        for loop in re.findall(r"for s in (.*?); do", sh, re.S):
            names |= {n + ".py" for n in loop.replace("\\", " ").split()}
        names |= set(re.findall(r"python3 ([\w./-]+\.py)", sh))
        for n in sorted(names):
            q = os.path.join(d, n)
            checked += 1
            if not os.path.exists(q):
                unresolved.append(rel(q))
                continue
            src = open(q).read()
            for lit in sorted(set(re.findall(r"[\"']([\w./-]+\.(?:md|py|sh))[\"']", src))):
                if outputs.search(lit) or lit == os.path.basename(q):
                    continue
                if re.search(re.escape(lit) + r"[\"']\)?,\s*[\"']w[\"']", src) or re.search(r"open\([^)]*" + re.escape(lit) + r"[^)]*\),\s*\"w\"", src):
                    how[f"{rel(q)} -> {lit}"] = "written by the script"
                    continue
                checked += 1
                m = re.match(r"(t\d+)_", lit)
                cands = [os.path.join(d, lit), os.path.join(CLS, lit), os.path.join(REPO, lit)] + ([os.path.join(CLS, m.group(1), lit)] if m else [])
                hit = next((c for c in cands if os.path.exists(c)), None)
                if hit is None and re.search(r"^DOC = ", src, re.M):
                    sys.path.insert(0, d)
                    mod = importlib.import_module(os.path.basename(q)[:-3])
                    hit = mod.DOC if os.path.exists(mod.DOC) else None
                if hit is None and re.search(r'with open\(os\.path\.join\(OUT, "' + re.escape(lit) + r'"\), "w"\)', src):
                    how[f"{rel(q)} -> {lit}"] = "written by the script"
                    continue
                if hit is None:
                    unresolved.append(f"{rel(q)} -> {lit}")
                else:
                    how[f"{rel(q)} -> {lit}"] = rel(hit)
    return {"checked": checked, "unresolved": unresolved, "resolved_by": how, "pass": not unresolved}


def h2():
    P = os.path.join(REPO, "reference", "phase1", "Holder_2026_Bounded_Failure_Window_Final.pdf")
    info = subprocess.run(["pdfinfo", P], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    out = {"pages": pages, "bytes": os.path.getsize(P), "sha256": hashlib.sha256(open(P, "rb").read()).hexdigest(),
           "producer": re.search(r"Producer:\s+(.*)", info).group(1).strip(), "errata": {}}
    quotes = {"E1": (5, "produces at most a threshold, whatever the gain"), "E2": (5, "no tested gain produced more than one interval"),
              "E3": (8, "A gain with no initial over-weighting"), "E4": (12, "Every failure set was a single interval")}
    for e, (pg, q) in quotes.items():
        t = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-f", str(pg), "-l", str(pg), P, "-"], capture_output=True, text=True).stdout)
        out["errata"][e] = {"page": pg, "found_on_page": q in t}
    out["same_as_author_file"] = out["pages"] == 17 and out["bytes"] == 462929 and \
        out["sha256"] == "9f60625a98c1cdd23c96360e64eb511acba0ee45321dde95980ab6795070eedf"
    return out


CHECKS = {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "C6": c6, "C7": c7, "C8": c8, "C9": c9, "C10": c10, "C13": c13, "H2": h2}


def main():
    which = sys.argv[1:] or list(CHECKS)
    path = os.path.join(RES, "t15_checks.json")
    out = json.load(open(path)) if os.path.exists(path) else {}
    for c in which:
        t0 = time.time()
        r = CHECKS[c]()
        r["seconds"] = round(time.time() - t0, 2)
        out[c] = r
        short = {k: v for k, v in r.items() if k not in ("mentions", "resolved_by", "figures")}
        print(c, ("PASS" if r.get("pass") else "FAIL") if "pass" in r else "", json.dumps(short, default=str, ensure_ascii=False)[:700], flush=True)
        with open(path, "w") as fh:
            json.dump(out, fh, indent=1, default=str, ensure_ascii=False)


if __name__ == "__main__":
    main()
