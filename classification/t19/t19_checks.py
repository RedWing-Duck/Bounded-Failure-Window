"""Task 19 checks G1-G7 (PREREG_t19.md, commit 7b6bd60). Manual readings after the run live in t19/results/ (G1 judgements, G3
examples and claims, G4 claim table); their verdicts are combined with this script's output by make_results_t19.py.
Usage: python3 t19_checks.py [G1 ... G7]   (default: all)"""
import html
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from fractions import Fraction

import mpmath as mp
import sympy as sp
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
RES = os.environ.get("T19_RES") or os.path.join(HERE, "results")
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_full.md")
sys.path[:0] = [os.path.join(CLS, "t18"), os.path.join(CLS, "t17"), os.path.join(CLS, "t16"), os.path.join(CLS, "t15"),
                os.path.join(CLS, "register")]
import t16_checks as T16  # noqa: E402
import t17_checks as T17  # noqa: E402
import t18_checks as T18  # noqa: E402
T18.DRAFT = DRAFT          # Task 18's helpers read the current draft
mp.mp.dps = 50
OLDKEY = "sahomasugi2016"


def T(*p):
    return open(os.path.join(CLS, *p)).read()


def J(*p):
    return json.load(open(os.path.join(CLS, *p)))


def lines():
    return open(DRAFT).read().split("\n")


def unesc(t):
    return T18.unesc(html.unescape(t))


def sentences_with(text, pat):
    return [s for s in re.split(r"(?<=[.!?])\s+", text) if re.search(pat, s)]


def norm(s):
    """Part A.4 normaliser: Task 18's formatting removal plus math delimiters $...$ (delimiters only, content kept)."""
    s = html.unescape(s)
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    return T18.norm(s)


# ------------------------------------------------------------------------------------------------------------------ G1
def G1():
    L = lines()
    text = unesc("\n".join(L))
    a, v = sp.symbols("alpha v", positive=True)
    lhs, rhs = a**2 * v / (1 - (1 - a)**2), a * v / (2 - a)
    z = T17.zero(lhs - rhs)
    den = sp.factor(1 - (1 - a)**2)
    rng = random.Random(19001)
    worst = mp.mpf(0)
    f, g = sp.lambdify((a, v), lhs, "mpmath"), sp.lambdify((a, v), rhs, "mpmath")
    with mp.workdps(60):
        for _ in range(1000):
            av, vv = mp.mpf(rng.uniform(1e-9, 2 - 1e-9)), mp.mpf(10 ** rng.uniform(-3, 3))
            x, y = f(av, vv), g(av, vv)
            worst = max(worst, abs(x - y) / abs(y))
    ident = {"sympy": z, "denominator_factored": str(den),
             "sign": "1 - (1 - alpha)^2 = alpha (2 - alpha) > 0 for 0 < alpha < 2; no square root occurs",
             "fallback": {"seed": 19001, "n": 1000, "digits": 60, "max_rel": float(worst), "pass": bool(worst < mp.mpf("1e-35"))}}
    ident["holds"] = bool(z["zero"] and ident["fallback"]["pass"])
    bib = T("references.bib")
    ent = {k: (re.search(r"@\w+\{" + k + r",.*?\n\}", bib, re.S).group(0) if re.search(r"@\w+\{" + k + ",", bib) else None)
           for k in ("roberts1959", "jazwinski1970", "andersonmoore1979", "yuksellinder2012")}
    out = {"identity_6_3": ident,
           "sentence_26": sentences_with(text, r"\[26\]"), "sentence_29_40": sentences_with(text, r"\[29, 40\]"),
           "sentences_21": sentences_with(text, r"\[21\]"), "bib_entries": ent,
           "note": "the four source judgements are manual (results/g1_citations.md); G1 passes only if all hold and the identity holds"}
    return out


# ------------------------------------------------------------------------------------------------------------------ G2
def rule_class(vals, R2):
    """Theorem 2.2 as stated: directions from the sequence; piece contributions; joins at shared values above R^2."""
    n = len(vals) - 1
    parts = []
    for j in range(n):
        a, b = vals[j], vals[j + 1]
        lo, hi = min(a, b), max(a, b)
        if R2 >= hi:
            parts.append((False, False))
        elif R2 <= lo:
            parts.append((True, True))
        else:                      # one-sided at the larger end
            parts.append((a > b, b > a))
    comps, cur = [], None
    for j, (tl, tr) in enumerate(parts):
        if not (tl or tr):                                   # empty piece: closes any open component
            if cur is not None:
                comps.append(tuple(cur))
                cur = None
            continue
        joined = cur is not None and tl and parts[j - 1][1] and vals[j] > R2
        if not joined:
            if cur is not None:
                comps.append(tuple(cur))
            cur = [j == 0 and tl, False]
        if tr:
            cur[1] = j == n - 1
        else:                                                # the contribution ends inside this piece
            cur[1] = False
            comps.append(tuple(cur))
            cur = None
    if cur is not None:
        comps.append(tuple(cur))
    if len(comps) == 1 and comps[0] == (True, True):
        return "All"
    return (int(any(c[0] for c in comps)), int(any(c[1] for c in comps)), sum(1 for c in comps if not c[0] and not c[1]))


def direct_class(vals, R2):
    """{f > R^2} for the piecewise-linear f through (j, vals[j]) on the open interval (0, n), exactly in rationals."""
    n = len(vals) - 1
    iv = []
    for j in range(n):
        a, b = Fraction(vals[j]), Fraction(vals[j + 1])
        if a > R2 and b > R2:
            iv.append((Fraction(j), Fraction(j + 1)))
        elif a > R2 or b > R2:
            c = j + (R2 - a) / (b - a)            # crossing point
            iv.append((Fraction(j), c) if a > R2 else (c, Fraction(j + 1)))
    # the nodes j = 1..n-1 belong to the set iff vals[j] > R^2; merge intervals sharing an endpoint that is in the set
    merged = []
    for lo, hi in iv:
        if merged and merged[-1][1] == lo and lo == int(lo) and 0 < lo < n and vals[int(lo)] > R2:
            merged[-1] = (merged[-1][0], hi)
        else:
            merged.append((lo, hi))
    if len(merged) == 1 and merged[0] == (0, n):
        return "All"
    ell = int(any(lo == 0 for lo, hi in merged))
    u = int(any(hi == n for lo, hi in merged))
    return (ell, u, sum(1 for lo, hi in merged if lo != 0 and hi != n))


def gen_sequence(rng):
    while True:
        n = rng.randint(1, 8)
        first_max = rng.random() < 0.5
        tp = []
        for j in range(n):
            kind_max = (j % 2 == 0) == first_max
            tp.append((kind_max, rng.randint(0, 6)))
        ok = all((tp[j][1] > tp[j + 1][1]) if tp[j][0] else (tp[j][1] < tp[j + 1][1]) for j in range(n - 1))
        if not ok:
            continue
        k0, v0 = tp[0]
        lm = rng.randint(0, 6)
        if not ((lm < v0) if k0 else (lm > v0)):
            continue
        kl, vl = tp[-1]
        lp = rng.randint(0, 6)
        if not ((lp < vl) if kl else (lp > vl)):
            continue
        return [lm] + [v for _, v in tp] + [lp]


def G2():
    src = T("source", "Stages_0_4_Source.md")
    i = src.index("At a tolerance equal to an interior turning-point value")
    repo = src[i:src.index("$\\square$", i)]
    L = lines()
    pf = unesc(L[164])
    dr = pf[pf.index("At a tolerance equal to an interior turning-point value"):pf.rindex("∎")]

    def flat(s):
        s = re.sub(r"\\mathcal F", "𝓕", s)
        s = s.replace("$R^2$", "R²").replace("$L_-$", "L₋").replace("$L_+ > L_-$", "L₊ > L₋").replace("$\\sigma^2(t_1) > L_-$", "σ²(t₁) > L₋")
        s = s.replace("$", "").replace("\n", " ")
        s = re.sub(r"[():.,;]", " ", s)
        return re.sub(r"\s+", " ", s).strip()
    text = {"repository": repo.strip(), "draft": dr.strip(), "flat_repository": flat(repo), "flat_draft": flat(dr),
            "identical_after_flattening": flat(repo) == flat(dr)}
    rng = random.Random(19002)
    mism, n, ex = [], 0, {}
    for _ in range(10000):
        vals = gen_sequence(rng)
        k = rng.randint(1, len(vals) - 2)
        R2 = Fraction(vals[k])
        a, b = rule_class(vals, R2), direct_class(vals, R2)
        n += 1
        key = str(a)
        ex[key] = ex.get(key, 0) + 1
        if a != b:
            mism.append({"vals": vals, "R2": str(R2), "rule": str(a), "direct": str(b)})
    out = {"text": text, "kind": "(a) equivalent" if text["identical_after_flattening"] else "manual reading needed",
           "random": {"seed": 19002, "n": n, "mismatches": len(mism), "examples": mism[:10], "class_counts": ex}}
    out["pass"] = text["identical_after_flattening"] and not mism
    return out


# ------------------------------------------------------------------------------------------------------------------ G3
TASKFILES = {**T18.TASKFILES, 18: "classification/RESULTS_t18.md"}


def counted_rows(n):
    t = open(os.path.join(REPO, TASKFILES[n])).read()
    L = t.split("\n")
    res = []
    if n <= 7:
        if n == 6:
            sec = t.split("## Task 6")[1].split("## Task 7")[0].split("\n")
            rows = [l for l in sec if re.match(r"^\| C\d", l)]
        else:
            rows = [l for l in L if re.match(rf"^\| T{n}\.\d", l)]
        for r in rows:
            cells = [c.strip().replace("*", "").strip() for c in r.strip().strip("|").split("|")]
            v = next((c for c in cells[1:] if c.startswith(("PASS", "FAIL"))), None)
            if v:
                res.append((cells[0], v[:4], v))
        return res
    i = next(k for k, l in enumerate(L) if l.startswith("|") and re.search(r"\b[Vv]erdict\b|\bResult\b", l))
    hdr = [c.strip() for c in L[i].strip().strip("|").split("|")]
    col = next(k for k, c in enumerate(hdr) if re.search(r"[Vv]erdict|Result", c))
    for l in L[i + 2:]:
        if not l.startswith("|"):
            break
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if col < len(cells):
            v = cells[col].replace("*", "").strip()
            if v.startswith(("PASS", "FAIL")):
                res.append((cells[0], v[:4], v))
    return res


def G3():
    per, tot, fail, none = {}, 0, 0, []
    for n in range(1, 19):
        r = counted_rows(n)
        p, f = sum(v == "PASS" for _, v, _ in r), sum(v == "FAIL" for _, v, _ in r)
        per[n] = {"checks": p + f, "fail": f, "failed": [c for c, v, _ in r if v == "FAIL"],
                  "qualified": [(c, full) for c, _, full in r if full not in ("PASS", "FAIL")]}
        tot += p + f
        fail += f
        if p + f == 0:
            none.append(n)
    recount = {"per_task": per, "total": tot, "failed": fail, "no_criteria": none,
               "match_151_32": tot == 151 and fail == 32 and none == [4, 5]}
    ad = T("Appendix_D_Verification.md")
    blocks = re.split(r"^\*\*Task (\d+)\.\*\*", ad, flags=re.M)
    fails = []
    for k in range(1, len(blocks), 2):
        for x in re.findall(r"^- Failure — (.*)$", blocks[k + 1], re.M):
            fails.append({"task": int(blocks[k]), "line": x})
    atts = ("criterion", "code", "document", "input", "prediction", "route", "plan's construction")
    for x in fails:
        m = re.search(r":\s*([^—]+?)\s+—", x["line"]) or re.search(r":\s*([a-z /'’]+?)\.?$", x["line"])
        lab = (m.group(1) if m else "").lower()
        x["attribution"] = lab
        x["covered"] = any(a in lab for a in atts)
    cover = {"failures": fails, "n": len(fails), "uncovered": [x for x in fails if not x["covered"]]}
    f3 = T18.F3()
    L = lines()
    s82 = "\n".join(T18.section(L, "### 8.2", "### 8.3"))
    s85 = "\n".join(T18.section(L, "### 8.5", "## 9."))
    s84 = "\n".join(T18.section(L, "### 8.4", "### 8.5"))
    clf = T("t10", "classify.py")
    routes = {"route_i_doc": re.search(r'def route_i\(.*?\n    vals', clf, re.S).group(0)[:400],
              "route_ii_doc": re.search(r'def route_ii\(.*?"""(.*?)"""', clf, re.S).group(1),
              "module_doc": clf.split('"""')[1]}
    ref = T("t13", "referee_report.md")
    npoints = len(re.findall(r"^\s*(?:\*\*)?\d+\.", ref, re.M))
    return {"recount": recount, "appendix_d_coverage": cover, "persistent_route_disagreements": f3["persistent_route_disagreements"],
            "referee_mentions_files": f3["files_with_referee_mentions"], "referee_mentions": f3["referee_mentions"],
            "section_8_2": s82, "section_8_4": s84, "section_8_5": s85, "classify_routes": routes,
            "referee_report_head": ref[:1500], "referee_report_numbered_items": npoints,
            "note": "pass also needs the manual readings (results/g3_examples.md, results/g3_claims.md)"}


# ------------------------------------------------------------------------------------------------------------------ G4
def G4():
    out = T18.F4()                                    # 9.3F, 17.6F, 5e-4, dips, avg 0.125 %, window statements, source section 11
    reg = {e["thesis_no"]: e for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))}
    out["register"] = {k: {"type": reg[k]["type"], "title": reg[k]["title"]} for k in ("5.8", "5.9", "5.13", "7.6", "7.8", "8.2")}
    # Hill gain: sup q against c/(F Pi0)
    c, F, P0, P, n = sp.symbols("c F Pi0 Pi n", positive=True)
    t = sp.symbols("t", positive=True)
    h2 = sp.Max(*[sp.simplify((t / (t**2 + 1)).subs(t, 1))])
    crit2 = sp.solve(sp.diff(t / (1 + t**2), t), t)
    hill = {"n2_sup_t_over_1_plus_t2": str(h2), "n2_stationary": [str(x) for x in crit2],
            "n2_equivalence": "q = (c/(F Pi0)) t/(1 + t^2), sup = c/(2 F Pi0); sup q > 2 iff c/(F Pi0) > 4"}
    rng = random.Random(19009)
    per_n = {}
    for nv in (mp.mpf("1.5"), mp.mpf(2), mp.mpf(3), mp.mpf(4)):
        hmax = mp.findroot(lambda u: mp.diff(lambda y: mp.power(mp.e, (nv - 1) * y) / (1 + mp.power(mp.e, nv * y)), u), 0.1)
        hv = mp.power(mp.e, (nv - 1) * hmax) / (1 + mp.power(mp.e, nv * hmax))
        dis = 0
        for _ in range(1000):
            r = mp.mpf(10 ** rng.uniform(-1, 1)) * 4          # c/(F Pi0) around the threshold
            supq = r * hv
            dis += int((supq > 2) != (r > 4))
        per_n[mp.nstr(nv, 3)] = {"sup_of_t^(n-1)/(1+t^n)": mp.nstr(hv, 12), "threshold_c_over_FPi0": mp.nstr(2 / hv, 12),
                                 "disagreements_with_c/(FPi0)>4_in_1000": dis}
    hill["per_n"] = per_n
    hill["worked_example"] = {"supq_at_Pi0_25": mp.nstr(mp.mpf(100) / (2 * 25), 6), "supq_at_Pi0_31.475": mp.nstr(mp.mpf(100) / (2 * mp.mpf("31.475")), 6),
                              "Pi0_pair_T10": T("t10", "RESULTS_t10.md").count("31.4750497595392")}
    out["hill"] = hill
    t5 = J("t10", "results", "t10_5.json")["narrow"]
    out["narrow_8_2"] = {k: v for k, v in t5.items() if k != "rows"}
    r10 = T("t10", "RESULTS_t10.md")
    out["two_stage_census"] = [l for l in r10.split("\n") if l.startswith(("| bayes2 |", "| hill2 |"))]
    L = lines()
    s9 = "\n".join(T18.section(L, "## 9.", "## Appendices"))
    out["section_9"] = s9
    out["op4_expectation"] = "is expected to split into scalar copies" in s9
    src = T("source", "Stages_0_4_Source.md")
    i = src.index("## 11. Open problems")
    out["open_problems_source"] = src[i:src.index("\n## ", i + 5)]
    return out


# ------------------------------------------------------------------------------------------------------------------ G5
def G5():
    T18.TASKFILES = TASKFILES
    orig = T18.F5.__globals__["TASKFILES"]
    T18.F5.__globals__["TASKFILES"] = TASKFILES
    src = T18.F5.__code__
    try:
        # Task 18's F5 accepts tasks 1-17; Task 19 accepts 1-18 (the draft covers Tasks 1-18)
        code = open(os.path.join(CLS, "t18", "t18_checks.py")).read()
        start, end = code.index("def valid_checks():"), code.index("# ------------------------------------------------------------------------------------------------------------------ F6")
        body = code[start:end].replace("1 <= k <= 17", "1 <= k <= 18")
        ns = dict(T18.__dict__)
        ns["TASKFILES"] = TASKFILES
        exec(body, ns)
        res = ns["F5"]()
    finally:
        T18.F5.__globals__["TASKFILES"] = orig
    del src
    # chapter of first citation of [46]-[53]
    L = lines()
    end = next(k for k, l in enumerate(L) if l.startswith("## Appendices"))
    chap, first = None, {}
    for l in L[:end]:
        m = re.match(r"^## (\d+)\.", l)
        if m:
            chap = int(m.group(1))
        for g in re.findall(r"\\\[([\d,\s–]+)\\\]", l):
            for part in g.split(","):
                part = part.strip()
                if "–" in part:
                    a, b = part.split("–")
                    nums = range(int(a), int(b) + 1)
                else:
                    nums = [int(part)] if part.isdigit() else []
                for x in nums:
                    first.setdefault(x, chap)
    res["first_chapter_46_53"] = {x: first.get(x) for x in range(46, 54)}
    res["claim_46_53_in_chapters_6_7"] = all(first.get(x) in (6, 7) for x in range(46, 54))
    return res


# ------------------------------------------------------------------------------------------------------------------ G6
def records(lines_, kind):
    out = []
    for l in lines_:
        n = norm(l)
        if not n or re.fullmatch(r"[-| :]+", n):
            continue
        if kind == "A" and re.match(r"^\d+\.\d+ \| ", n):
            out.append(n)
        elif kind == "C" and re.match(r"^\[\d+\]", n):
            out.append(n)
        elif kind == "D" and (re.match(r"^Task \d+\.", n) or n.startswith("- Failure") or n.startswith("Failure —")):
            out.append(n.lstrip("- ").strip())
    return out


def G6():
    out = {}
    for letter, f in (("A", "Appendix_A_Register.md"), ("C", "Appendix_C_References.md"), ("D", "Appendix_D_Verification.md")):
        d = records(T18.draft_appendix(letter), letter)
        r = records(open(os.path.join(CLS, f)).read().split("\n"), letter)
        diffs = [{"index": k, "draft": d[k] if k < len(d) else None, "render": r[k] if k < len(r) else None}
                 for k in range(max(len(d), len(r))) if (d[k] if k < len(d) else None) != (r[k] if k < len(r) else None)]
        dl = T18.draft_appendix(letter)
        rl = [l for l in open(os.path.join(CLS, f)).read().split("\n") if l.strip()][:2]
        out[letter] = {"draft_records": len(d), "render_records": len(r), "differences": diffs,
                       "intro_draft": norm(" ".join(dl[:2]))[:600], "intro_render": norm(" ".join(rl))[:600]}
    out["pass"] = all(not out[x]["differences"] for x in "ACD")
    return out


# ------------------------------------------------------------------------------------------------------------------ G7
def G7():
    g = subprocess.run(["git", "grep", "-c", OLDKEY, "HEAD", "--", "."], cwd=REPO, capture_output=True, text=True).stdout
    hits = {}
    for l in g.strip().split("\n"):
        if l:
            _, path, cnt = l.split(":")
            hits[path] = int(cnt)
    excl = {"classification/PREREG_t19.md", "classification/t19/t19_checks.py"}
    counted = {p: c for p, c in hits.items() if p not in excl and not p.startswith("classification/t19/input/")}
    live = {p: c for p, c in counted.items() if p in {"classification/references.bib", "classification/register/references.yaml",
                                                      "classification/register/results.yaml", "classification/Appendix_C_References.md",
                                                      "classification/Stages_0_4_Thesis.md", "classification/Stages_0_4_Paper2.md",
                                                      "classification/source/Stages_0_4_Source.md"}}
    th = T("Stages_0_4_Thesis.md").split("\n")
    i = next(k for k, l in enumerate(th) if l.startswith("**Theorem 2.2.**"))
    pf_r = next(th[k] for k in range(i, i + 12) if th[k].startswith("*Proof.*"))
    pf_d = unesc(lines()[164])
    proof_eq = norm(pf_r) == norm(pf_d)
    src = T("source", "Stages_0_4_Source.md")
    k = src.index("## 11. Open problems")
    sec = src[k:src.index("\n## ", k + 5)]
    items = re.findall(r"^(\d+)\. \*\*", sec, re.M)
    d = records(T18.draft_appendix("A"), "A")
    r = records(T("Appendix_A_Register.md").split("\n"), "A")
    adiff = sum(1 for a, b in zip(d, r) if a != b) + abs(len(d) - len(r))
    out = {"occurrences_counted": counted, "n_counted": sum(counted.values()), "live_occurrences": live,
           "excluded": sorted(set(hits) - set(counted)), "theorem_2_2_proof_equal": proof_eq,
           "proof_render": pf_r[-400:], "proof_draft": pf_d[-400:], "source_11_items": items, "appendix_A_differences": adiff}
    out["pass"] = out["n_counted"] == 0 and proof_eq and items == [str(x) for x in range(1, 7)] and adiff == 0
    return out


CHECKS = {"G1": G1, "G2": G2, "G3": G3, "G4": G4, "G5": G5, "G6": G6, "G7": G7}


def main():
    os.makedirs(RES, exist_ok=True)
    which = [a for a in sys.argv[1:] if a in CHECKS] or list(CHECKS)
    path = os.path.join(RES, "t19_checks.json")
    out = json.load(open(path)) if os.path.exists(path) and sys.argv[1:] else {}
    out["commit"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    for k in which:
        t0 = time.time()
        r = CHECKS[k]()
        r.setdefault("seconds", round(time.time() - t0, 2))
        out[k] = r
        print(k, {"pass": r.get("pass")} if "pass" in r else "", f"{r['seconds']} s", flush=True)
        json.dump(out, open(path, "w"), indent=1, ensure_ascii=False, default=str)


if __name__ == "__main__":
    main()
