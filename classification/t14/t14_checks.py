"""Task 14 checks C1-C10 (PREREG_t14.md, commit e5edebf). Read-only except results/t14_checks.json and the scratch renders.
Usage: python3 t14_checks.py [C1 C2 ...]   (default: all)"""
import csv
import difflib
import glob
import os
import re
import subprocess
import sys
import time

import mpmath as mp
import yaml

from t14_common import AE, CLS, LEGACY, REPO, RES, save_json

sys.path.insert(0, os.path.join(CLS, "register"))
import render as R  # noqa: E402

REG = os.path.join(CLS, "register")
SOURCES = [os.path.join(CLS, "source", "Stages_0_4_Source.md"), os.path.join(CLS, "source", "Roadmap_v3_Source.md")] + \
    sorted(glob.glob(os.path.join(CLS, "source", "figs", "*"))) + [os.path.join(REG, "matrix.csv")]
EXTRA_SOURCES = sorted(glob.glob(os.path.join(CLS, "source", "phase1", "*")))   # reported, not part of the verdicts
TOKEN = re.compile(r"\[\[([^\]|]+)(\|[nta])?\]\]")
THESIS_ONLY = {"2.3", "2.8", "2.9", "3.2", "6.5"}
V1 = os.path.join(CLS, "archive", "Stages_0_4_Consolidated_v1.md")
TMP = os.path.join(RES, "scratch")


def rel(p):
    return os.path.relpath(p, REPO)


def reg():
    return yaml.safe_load(open(os.path.join(REG, "results.yaml")))


def strip_code(t):
    return re.sub(r"^```.*?^```", "", t, flags=re.S | re.M)


def c1():
    E = reg()
    keys = [e["key"] for e in E]
    nos = [e["thesis_no"] for e in E]
    chap = {}
    for n in nos:
        c, i = n.split(".")
        chap.setdefault(int(c), []).append(int(i))
    contig = {c: sorted(v) == list(range(1, len(v) + 1)) for c, v in chap.items()}
    mapped = set()
    for e in E:
        m = re.match(r"^(\d+)(\s|$)", e["cons_v1"] or "")
        if m:
            mapped.add(int(m.group(1)))
    table = list(csv.DictReader(open(os.path.join(CLS, "t14", "input", "register_table.csv"))))
    labels_table = {l for r in table for l in re.findall(r"\b[A-E]\.\d+\b", r["legacy"])}
    labels_reg = {l for e in E for x in e["legacy"] for l in re.findall(r"\b[A-E]\.\d+\b", x)}
    out = {"n_entries": len(E), "keys_unique": len(set(keys)) == len(keys),
           "keys_pattern": all(re.fullmatch(r"[a-z0-9-]+", k) for k in keys), "thesis_no_unique": len(set(nos)) == len(nos),
           "chapters_contiguous": contig, "v1_unmapped": sorted(set(range(1, 74)) - mapped),
           "legacy_labels_in_table": len(labels_table), "legacy_labels_unmapped": sorted(labels_table - labels_reg)}
    out["pass"] = (out["n_entries"] == 82 and out["keys_unique"] and out["keys_pattern"] and out["thesis_no_unique"]
                   and all(contig.values()) and not out["v1_unmapped"] and not out["legacy_labels_unmapped"])
    return out


def c2():
    E = {e["key"]: e for e in reg()}
    used, unres = {}, []
    for p in SOURCES:
        for m in TOKEN.finditer(open(p).read()):
            used[m.group(1)] = used.get(m.group(1), 0) + 1
            if m.group(1) not in E:
                unres.append((rel(p), m.group(0)))
    unref = [k for k, e in E.items() if k not in used and e["thesis_no"] not in THESIS_ONLY]
    src = open(SOURCES[0]).read()
    heads = set(R.HEADED.findall(src))
    paper_vis = R.strip_cond(src, "paper")
    headless_paper = sorted({m.group(1) for m in TOKEN.finditer(paper_vis) if m.group(2) != "|t" and m.group(1) not in heads})
    thesis_vis = "".join(R.strip_cond(open(p).read(), "thesis") for p in SOURCES)
    headless_thesis = sorted({m.group(1) for m in TOKEN.finditer(thesis_vis) if m.group(1) not in heads})
    extra_unres = [(rel(p), m.group(0)) for p in EXTRA_SOURCES for m in TOKEN.finditer(open(p).read()) if m.group(1) not in E]
    return {"tokens": sum(used.values()), "keys_referenced": len(used), "unresolved": unres, "unreferenced": unref,
            "headless_in_paper_render": headless_paper, "headless_in_thesis_render (cited by thesis number)": headless_thesis,
            "phase1_sources_unresolved": extra_unres, "pass": not unres and not unref}


def c3():
    per = {}
    for p in SOURCES + EXTRA_SOURCES:
        t = strip_code(open(p).read())
        hits = [m.group(0) for m in LEGACY.finditer(t)] + AE.findall(t) + ["Paper 1"] * t.count("Paper 1")
        per[rel(p)] = hits
    main = sum(len(per[rel(p)]) for p in SOURCES)
    return {"matches_in_sources": main, "per_file": {k: v for k, v in per.items() if v},
            "phase1_sources_matches": sum(len(per[rel(p)]) for p in EXTRA_SOURCES), "pass": main == 0}


def c4():
    E = {e["key"]: e for e in reg()}
    paper = R.numbering("paper", E)
    bad = []
    for k, n in paper.items():
        m = re.match(r"^(\d+)(?: \(main part\))?$", E[k]["cons_v1"] or "")
        exp = (int(m.group(1)) if int(m.group(1)) < 7 else int(m.group(1)) + 1) if m else 7
        if k == "no-mixed-decreasing-ratio":
            exp = 7
        if int(n) != exp:
            bad.append((k, n, exp))
    os.makedirs(TMP, exist_ok=True)
    rr = R.Renderer("v1check")
    v1c = rr.render(open(SOURCES[0]).read())
    open(os.path.join(TMP, "v1check.md"), "w").write(v1c)
    a, b = open(V1).read().split("\n"), v1c.split("\n")
    hunks = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        old, new = a[i1:i2], b[j1:j2]
        txt = "\n".join(old + new)
        if re.search(r"^\| 2[56] \| \$\\Delta t\$", txt, re.M) and all(re.match(r"^\| 2[56] \|", l) for l in old + new):
            cat = "c (rows 25-26)"
        elif "6+" in txt or "addendum" in txt or (170 <= i1 + 1 <= 186):
            cat = "b (split)"
        else:
            cat = "other"
        hunks.append({"v1_lines": f"{i1 + 1}-{i2}", "category": cat, "old": old[:4], "new": new[:4]})
    other = [h for h in hunks if h["category"] == "other"]
    paper_doc = open(os.path.join(CLS, "Stages_0_4_Paper2.md")).read().split("\n")
    raw = sum(1 for l in difflib.unified_diff(a, paper_doc, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---")))
    return {"numbering_mismatches": bad, "hunks": len(hunks), "by_category": {c: sum(h["category"] == c for h in hunks)
            for c in ("b (split)", "c (rows 25-26)", "other")}, "other_hunks": other, "all_hunks": hunks,
            "raw_paper_vs_v1_changed_lines": raw, "pass": not bad and not other}


def c5():
    files = [os.path.join(CLS, "Stages_0_4_Thesis.md"), os.path.join(CLS, "Roadmap_v3.md"), os.path.join(CLS, "Appendix_A_Register.md")] + \
        sorted(glob.glob(os.path.join(CLS, "figs_thesis", "*")))
    per = {}
    for p in files:
        t = open(p).read()
        per[rel(p)] = {"Paper 1": t.count("Paper 1"), "A-E": AE.findall(t)}
    tot = sum(v["Paper 1"] + len(v["A-E"]) for v in per.values())
    return {"files": len(files), "hits": {k: v for k, v in per.items() if v["Paper 1"] or v["A-E"]}, "total": tot, "pass": tot == 0}


def table(path):
    L = open(path).read().split("\n")
    i = next(i for i, l in enumerate(L) if l.startswith("| # | Sweep |"))
    j = i
    while j < len(L) and L[j].startswith("|"):
        j += 1
    return "\n".join(L[i:j])


def c6():
    t1, t2 = table(os.path.join(CLS, "Stages_0_4_Thesis.md")), table(os.path.join(CLS, "Roadmap_v3.md"))
    rows = {}
    for l in t1.split("\n"):
        c = [x.strip() for x in l.strip().strip("|").split(" | ")]
        if c[0] in ("25", "26"):
            rows[c[0]] = c[9]
    norm = lambda s: s.replace("$", "").replace("\\Pi", "Π").replace("\\le", "≤")
    exp = {"25": "2R if G > 2FΠ (Proposition 6.20)",
           "26": "2R if G > 2FΠ (Proposition 6.20); also seen for G ≤ 2FΠ (Numerical result 6.21)"}
    ok = {k: norm(rows[k]) == v for k, v in exp.items()}
    return {"byte_identical": t1.encode() == t2.encode(), "rows": rows, "normalised": {k: norm(v) for k, v in rows.items()},
            "rows_exact": ok, "n_lines": len(t1.split("\n")), "pass": t1.encode() == t2.encode() and all(ok.values())}


def c7():
    mp.mp.dps = 60
    lam, c, Sig, P0 = mp.mpf(1), mp.mpf(1), mp.mpf("0.01"), mp.mpf(5)

    def sig2(P):
        G = c * P**2 / (P**2 + P0**2)
        return (Sig + G**2 / (2 * P)) / (lam + G)

    def d(x):   # analytic derivative in log10(Pi): Lemma 51 form, N with elasticity eps = 2/(1 + T)
        P = mp.power(10, x)
        G = c * P**2 / (P**2 + P0**2)
        eps = 2 * P0**2 / (P**2 + P0**2)
        return G * (eps * (G**2 + 2 * lam * G - 2 * Sig * P) - G * (lam + G))   # sign of dsigma^2/dPi
    xs = [mp.mpf(k) / 50 for k in range(-200, 301)]
    sgn = [mp.sign(d(x)) for x in xs]
    k = next(i for i in range(len(xs) - 1) if sgn[i] < 0 and sgn[i + 1] > 0)   # first minimum (- to +)
    lo, hi = xs[k], xs[k + 1]
    while hi - lo > mp.mpf("1e-40"):
        mid = (lo + hi) / 2
        if mp.sign(d(mid)) < 0:
            lo = mid
        else:
            hi = mid
    Pm = mp.power(10, (lo + hi) / 2)
    m = sig2(Pm)
    nturn = sum(1 for i in range(len(sgn) - 1) if sgn[i] != sgn[i + 1])
    r5 = mp.nstr(m, 5)
    return {"m_8sf": mp.nstr(m, 8), "m_30sf": mp.nstr(m, 30), "Pi_at_min": mp.nstr(Pm, 12), "turning_points_on_grid": nturn,
            "m_5sf": r5, "pass": r5 == "0.0099852"}


def c8():
    T = yaml.safe_load(open(os.path.join(REG, "tasks.yaml")))
    hs = sorted({h for t in T if int(t["task"][1:]) <= 7 for h in (t["prereg_commit"], t["results_commit"])})
    res = {h: subprocess.run(["git", "-C", REPO, "cat-file", "-e", h + "^{commit}"]).returncode == 0 for h in hs}
    return {"hashes": res, "missing": [h for h, ok in res.items() if not ok], "pass": all(res.values())}


def bib_entries():
    txt = open(os.path.join(CLS, "references.bib")).read()
    ents = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", txt, re.S):
        body = m.group(3)
        doi = re.search(r"\bdoi\s*=\s*\{([^}]*)\}", body)
        note = re.search(r"\bnote\s*=\s*\{(.*?)\}\s*,?\s*$", body, re.S | re.M)
        ents[m.group(2).strip()] = {"type": m.group(1), "doi": doi.group(1) if doi else None,
                                     "verify": "VERIFY" in body}
    return ents


def c9():
    ents = bib_entries()
    used = {c for e in reg() for c in e["citations"]}
    cited = set()
    for p in SOURCES + EXTRA_SOURCES:
        cited |= set(re.findall(r"\[([a-z][a-z-]*\d{4}[a-z]?)\]", open(p).read()))
    dangling = sorted(used - set(ents))
    unused = sorted(set(ents) - used - cited)
    res = {}
    for k, e in ents.items():
        if not e["doi"]:
            continue
        try:
            p = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20",
                                f"https://doi.org/{e['doi']}"], capture_output=True, text=True, timeout=30)
            code, err = p.stdout.strip(), p.stderr.strip()[:160]
        except Exception as ex:  # noqa: BLE001
            code, err = "000", str(ex)[:160]
        resolved = code.startswith("3") or code == "200"
        res[k] = {"doi": e["doi"], "http": code, "error": err, "resolved": resolved, "marked_verify": e["verify"]}
    bad = [k for k, v in res.items() if not v["resolved"] and not v["marked_verify"]]
    return {"entries": len(ents), "dangling": dangling, "unused": unused, "doi_entries": len(res),
            "doi_resolved": sum(v["resolved"] for v in res.values()), "doi_unresolved_unmarked": bad, "doi": res,
            "pass": not dangling and not unused and not bad}


def c10():
    rs = open(os.path.join(CLS, "reproduce_all.sh")).read()
    run = re.findall(r'\[(\d+)\]="([^"]+)"', rs.split("declare -A RUN=")[1].split("\n")[0])
    missing, checked, fallback = [], [], []
    outputs = re.compile(r"^(REPORT\.md|RESULTS_t\d+\.md)$|(^|/)(results|figs[\w]*|figures)/")
    for t, path in run:
        p = os.path.join(CLS, path)
        checked.append(rel(p))
        if not os.path.exists(p):
            missing.append(rel(p))
            continue
        d = os.path.dirname(p)
        sh = open(p).read()
        names = set()
        for loop in re.findall(r"for s in (.*?); do", sh, re.S):
            names |= {n + ".py" for n in loop.replace("\\", " ").split()}
        names |= set(re.findall(r"python3 ([\w./-]+\.py)", sh))
        for n in sorted(names):
            q = os.path.join(d, n)
            checked.append(rel(q))
            if not os.path.exists(q):
                missing.append(rel(q))
                continue
            src = open(q).read()
            for lit in sorted(set(re.findall(r"[\"']([\w./-]+\.(?:md|py|sh))[\"']", src))):
                if outputs.search(lit) or lit == os.path.basename(q):
                    continue
                cands = [os.path.join(CLS, lit), os.path.join(d, lit), os.path.join(REPO, lit)]
                checked.append(f"{rel(q)} -> {lit}")
                if any(os.path.exists(c) for c in cands):
                    continue
                if re.search(re.escape(lit) + r"[\"']\)\nif not os\.path\.exists\(DOC\):", src) and \
                        os.path.exists(os.path.join(CLS, "archive", "Stages_0_4_Consolidated_v1.md")):
                    fallback.append(f"{rel(q)}: {lit} -> archive/Stages_0_4_Consolidated_v1.md")
                    continue
                missing.append(f"{rel(q)} -> {lit}")
    return {"checked": len(checked), "missing": missing, "resolved_by_fallback": fallback, "pass": not missing}


CHECKS = {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "C6": c6, "C7": c7, "C8": c8, "C9": c9, "C10": c10}


def main():
    which = sys.argv[1:] or list(CHECKS)
    path = os.path.join(RES, "t14_checks.json")
    out = yaml.safe_load(open(path)) if os.path.exists(path) else {}
    for c in which:
        t0 = time.time()
        r = CHECKS[c]()
        r["seconds"] = round(time.time() - t0, 2)
        out[c] = r
        short = {k: v for k, v in r.items() if k not in ("all_hunks", "doi", "per_file", "other_hunks")}
        print(c, "PASS" if r["pass"] else "FAIL", str(short)[:700], flush=True)
    save_json(out, "t14_checks.json")


if __name__ == "__main__":
    main()
