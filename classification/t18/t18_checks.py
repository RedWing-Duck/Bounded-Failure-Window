"""Task 18 checks F1-F7 (PREREG_t18.md, commit 97e1889). Manual readings after the run live in t18/results/.
Usage: python3 t18_checks.py [F1 ... F7]   (default: all)"""
import glob
import html
import json
import math
import os
import random
import re
import subprocess
import sys
import time

import mpmath as mp
import sympy as sp
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
RES = os.environ.get("T18_RES") or os.path.join(HERE, "results")
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_full.md")
sys.path[:0] = [os.path.join(CLS, "t17"), os.path.join(CLS, "t16"), os.path.join(CLS, "t15"), os.path.join(CLS, "register")]
import t16_checks as T16  # noqa: E402
import t17_checks as T17  # noqa: E402
mp.mp.dps = 50


def T(*p):
    return open(os.path.join(CLS, *p)).read()


def J(*p):
    return json.load(open(os.path.join(CLS, *p)))


def draft_lines():
    return open(DRAFT).read().split("\n")


def section(L, start, stop):
    i = next(k for k, l in enumerate(L) if l.startswith(start))
    j = next(k for k in range(i + 1, len(L)) if L[k].startswith(stop))
    return L[i:j]


def unesc(t):
    return t.replace("\\[", "[").replace("\\]", "]").replace("\\_", "_").replace("\\~", "~")


# ------------------------------------------------------------------------------------------------------------------ F1
def F1():
    L = draft_lines()
    text = unesc("\n".join(L))
    out = {}
    # Corollary 7.4's proof
    i = next(k for k, l in enumerate(L) if l.startswith("**Corollary 7.4"))
    pf = next(L[k] for k in range(i, i + 6) if L[k].startswith("*Proof"))
    lam, Sig, Pi = sp.symbols("lambda Sigma Pi", positive=True)
    lim = sp.limit(2 * Sig / (lam + sp.sqrt(lam**2 + 2 * Sig * Pi)), Pi, sp.oo)
    c74 = {"proof": pf, "cites_limit": "→ 0 as Π → ∞" in pf and "Proposition 3.5" in pf, "cites_5_1": "Theorem 5.1" in pf,
           "sympy_limit": str(lim)}
    c74["resolved"] = c74["cites_limit"] and c74["cites_5_1"] and lim == 0
    out["cor_7_4"] = c74
    # beta count
    m = re.search(r"over (\d+) values of β", text)
    nb = len({x["beta"] for x in J("t11", "results", "t11_3.json")["by_beta"]})
    out["beta"] = {"draft": int(m.group(1)) if m else None, "t11_3_distinct": nb, "resolved": bool(m) and int(m.group(1)) == nb}
    # section 6.7 label
    row = next(l for l in L if l.startswith("| τ, matched variance |"))
    reg = {e["thesis_no"]: e["type"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))}
    refs = re.findall(r"(Prop\.|Cex\.) (\d+\.\d+)", row)
    alias = {"Prop.": "Proposition", "Cex.": "Counterexample"}
    out["s67_label"] = {"row": row, "refs": refs, "types": {n: reg.get(n) for _, n in refs},
                        "resolved": bool(refs) and all(reg.get(n) == alias[a] for a, n in refs)}
    # [47] sentences
    ss = [s for s in re.split(r"(?<=[.!?])\s+", text) if "[47]" in s]
    out["s47"] = {"sentences": ss, "resolved": len(ss) == 2 and all("model error" in s for s in ss)}
    s21 = [s for s in re.split(r"(?<=[.!?])\s+", text) if re.search(r"\[21\]", s)]
    out["s21"] = {"sentences": s21, "resolved": len(s21) == 1 and "observation channels" in s21[0] and "[21–23]" not in text}
    # Proposition 6.13: f(F) = F^2 a^2 and P- < F
    M, F, r, a = sp.symbols("M F r a", positive=True)
    s = 1 - a**2
    f = M**2 + s * (r - F) * M - s * F * r
    z = T17.zero(f.subs(M, F) - F**2 * a**2)
    i = next(k for k, l in enumerate(L) if l.startswith("**Proposition 6.13"))
    pf = next(L[k] for k in range(i, i + 15) if L[k].startswith("*Proof"))
    rng = random.Random(18001)
    bad, maxd = 0, 0
    for _ in range(1000):
        l_, S_, P_ = (10 ** rng.uniform(-3, 3) for _ in range(3))
        dt = 10 ** rng.uniform(-4, 2)
        d = int(2 * l_ * dt / math.log(10)) + 60
        maxd = max(maxd, d)
        with mp.workdps(d):
            ll, SS, PP, tt = mp.mpf(l_), mp.mpf(S_), mp.mpf(P_), mp.mpf(dt)
            Fv = SS / ll
            a2 = mp.e ** (-2 * ll * tt)
            q, rr = Fv * (1 - a2), 1 / (PP * tt)
            bb = rr * (1 - a2) - q
            Mv = (-bb + mp.sqrt(bb**2 + 4 * q * rr)) / 2
            if not Mv < Fv:
                bad += 1
    out["p613"] = {"proof_states_it": "f(F) = F²a² > 0" in pf, "identity": z,
                   "sign": "f is monic (opens upward) with f(0) = -sFr < 0, so its positive root M is below F iff f(F) > 0; f(F) = F^2 a^2 > 0.",
                   "numeric": {"seed": 18001, "n": 1000, "counterexamples": bad, "max_digits": maxd}}
    out["p613"]["resolved"] = out["p613"]["proof_states_it"] and z["zero"] and bad == 0
    out["pass"] = all(v["resolved"] for v in out.values() if isinstance(v, dict))
    return out


# ------------------------------------------------------------------------------------------------------------------ F2
TASKFILES = {1: "verification/REPORT.md", 2: "verification/REPORT.md", 3: "verification/REPORT.md", 4: "verification/REPORT.md",
             5: "verification/REPORT.md", 6: "verification/REPORT.md", 7: "verification/REPORT.md", 8: "classification/REPORT.md",
             9: "classification/t9/RESULTS_t9.md", 10: "classification/t10/RESULTS_t10.md", 11: "classification/t11/RESULTS_t11.md",
             12: "classification/t12/RESULTS_t12.md", 13: "classification/t13/RESULTS_t13.md", 14: "classification/t14/RESULTS_t14.md",
             15: "classification/RESULTS_t15.md", 16: "classification/RESULTS_t16.md", 17: "classification/RESULTS_t17.md"}


def verdict_cells(rows, col):
    out = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if col < len(cells):
            v = cells[col].replace("*", "").strip()
            if v in ("PASS", "FAIL"):
                out.append((cells[0], v, r))
    return out


def task_rows(n):
    t = open(os.path.join(REPO, TASKFILES[n])).read()
    L = t.split("\n")
    if n <= 7:
        if n == 6:
            sec = t.split("## Task 6")[1].split("## Task 7")[0].split("\n")
            rows = [l for l in sec if re.match(r"^\| C\d", l)]
        else:
            rows = [l for l in L if re.match(rf"^\| T{n}\.\d", l)]
        # verdict column: the cell equal to PASS/FAIL (first such)
        res = []
        for r in rows:
            cells = [c.strip().replace("*", "") for c in r.strip().strip("|").split("|")]
            v = next((c for c in cells if c in ("PASS", "FAIL")), None)
            if v:
                res.append((cells[0], v, r))
        return res
    i = next(k for k, l in enumerate(L) if l.startswith("|") and re.search(r"\b[Vv]erdict\b|\bResult\b", l))
    hdr = [c.strip() for c in L[i].strip().strip("|").split("|")]
    col = next(k for k, c in enumerate(hdr) if re.search(r"[Vv]erdict|Result", c))
    rows = []
    for l in L[i + 2:]:
        if not l.startswith("|"):
            break
        rows.append(l)
    return verdict_cells(rows, col)


def F2():
    per, tot, fail, none = {}, 0, 0, []
    for n in range(1, 18):
        r = task_rows(n)
        p, f = sum(v == "PASS" for _, v, _ in r), sum(v == "FAIL" for _, v, _ in r)
        per[n] = {"checks": p + f, "pass": p, "fail": f, "failed": [c for c, v, _ in r if v == "FAIL"]}
        tot += p + f
        fail += f
        if p + f == 0:
            none.append(n)
    out = {"per_task": per, "total": tot, "failed": fail, "no_criteria": none,
           "counts_match": tot == 144 and fail == 28 and none == [4, 5]}
    # failures listed in the Appendix D render, for the attribution mapping (manual table in results/f2_examples.md)
    ad = T("Appendix_D_Verification.md")
    out["appendix_d_failures"] = re.findall(r"^- Failure — (.*)$", ad, re.M)
    atts = {"criterion", "code", "document", "input", "prediction", "route", "plan's construction"}
    unmapped = []
    for x in out["appendix_d_failures"]:
        m = re.search(r":\s*([^—]+?)\s+—", x)
        lab = (m.group(1) if m else "").lower()
        if not any(a in lab for a in atts):
            unmapped.append(x)
    out["appendix_d_unmapped"] = unmapped
    out["note"] = "pass also needs the manual §8.4 example mapping (results/f2_examples.md)"
    return out


# ------------------------------------------------------------------------------------------------------------------ F3
def F3():
    persist = []
    for p in glob.glob(os.path.join(CLS, "t*", "results", "*.json")) + glob.glob(os.path.join(CLS, "results", "*.json")):
        try:
            d = json.load(open(p))
        except Exception:  # noqa: BLE001
            continue

        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ("persisting", "n_persist", "persistent") and isinstance(v, (int, float)) and v > 0:
                        persist.append({"file": os.path.relpath(p, REPO), "path": path + "/" + k, "value": v,
                                        "name": o.get("name")})
                    walk(v, path + "/" + k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, f"{path}/{i}")
        walk(d, "")
    ref = []
    for p in glob.glob(os.path.join(CLS, "**", "*.md"), recursive=True) + glob.glob(os.path.join(REPO, "verification", "**", "*.md"),
                                                                                       recursive=True):
        if "/input/" in p or "/archive/" in p or "/t18/" in p:
            continue
        for k, l in enumerate(open(p).read().split("\n")):
            if re.search(r"referee|external review|independent review", l, re.I):
                ref.append({"file": os.path.relpath(p, REPO), "line": k + 1, "text": l[:200]})
    return {"persistent_route_disagreements": persist, "referee_mentions": ref,
            "files_with_referee_mentions": sorted({r["file"] for r in ref}),
            "note": "verdicts for the two claims are manual (results/f3_claims.md)"}


# ------------------------------------------------------------------------------------------------------------------ F4
def F4():
    out = {}
    S_, l_, c_ = mp.mpf("0.01"), mp.mpf(1), mp.mpf(1)
    F_ = S_ / l_
    P0b = c_ / (100 * F_)
    Gt = -l_ + mp.sqrt(l_**2 + l_ * c_ - 2 * S_ * P0b)
    Mb = T17.sig2(Gt, P0b * Gt / (c_ - Gt)) / F_
    r = S_ / 1
    GM = (-2 * r + mp.sqrt(4 * r**2 + 2 * (1 + r) * (1 - 2 * r))) / (1 + r)
    PM = (GM**2 + 2 * GM) / 2
    Mk = T17.sig2(GM, PM) / F_
    out["peaks"] = {"bayes_M_over_F": mp.nstr(Mb, 8), "kalman_M_over_F": mp.nstr(Mk, 8),
                    "9.3F": T16.printed_match("9.3", Mb), "17.6F": T16.printed_match("17.6", Mk)}
    t4 = J("t10", "results", "t10_4.json")
    out["median_band"] = {"value": t4["band_rel_median"], "match_5e-4": T16.printed_match("5 × 10^-4", t4["band_rel_median"])}
    src = T("source", "Stages_0_4_Source.md")
    out["narrow"] = {"source": T17.find(src, r"(\*\*\[\[narrow-windows\]\][^\n]*\n[^\n]*)", 1)}
    out["dip"] = {"in_t12": "10^-32880317" in T("t12", "RESULTS_t12.md")}
    Gr = mp.mpf("0.5")
    av = T17.mp_avg(1 - mp.e ** (-Gr * 200), mp.mpf(200))
    out["avg_dip"] = {"avg_200": mp.nstr(av, 10), "match_0.125%": T16.printed_match("0.125%", (F_ - av) / F_)}
    conds = {}
    for key in ("bayesian-weight", "misspecified-kalman", "capped-gain", "sigma-overtrust", "sigma-misspecified-lambda"):
        m = re.search(r"\*\*\[\[" + key + r"\]\][^\n]*(?:\n(?!\*\*\[\[)[^\n]*){0,8}", src)
        conds[key] = m.group(0)[:600] if m else None
    out["window_condition_statements"] = conds
    i = src.index("## 11. Open problems")
    out["open_problems_source"] = src[i:src.index("\n## ", i + 5)]
    return out


# ------------------------------------------------------------------------------------------------------------------ F5
def valid_checks():
    v = {}
    for n, f in TASKFILES.items():
        t = open(os.path.join(REPO, f)).read()
        ids = set(re.findall(r"^\| (?:\*\*)?(T\d+\.\d+)", t, re.M)) | set(re.findall(r"^\| (?:\*\*)?([A-H]\d+)\b", t, re.M))
        ids |= set(re.findall(r"\b(T\d+\.\d+)\b", t))
        v[n] = ids
    return v


def F5():
    t0 = time.time()
    L = draft_lines()
    end = next(k for k, l in enumerate(L) if l.startswith("## Appendices"))
    body = L[:end]
    # Task 17 E4 machinery on the whole body (its typed-reference list is re-run below with "Cex." added)
    orig = T17.draft_upto
    T17.draft_upto = lambda heading: body
    try:
        base = T17.E4()
    finally:
        T17.draft_upto = orig
    text = unesc("\n".join(body))
    reg = {e["thesis_no"]: e["type"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))}
    aliases = dict(T16.TYPE_ALIASES, **{"cex.": "Counterexample"})
    tw = r"(Theorems?|Thm|Propositions?|Props?\.|Lemmas?|Corollar(?:y|ies)|Cor\.|Definitions?|Numerical results?|Num\. results?|" \
         r"Conjectures?|Counterexamples?|Cex\.)"
    spec = r"(\d+\.\d+(?:\([^)]*\))?(?:[–-]\d+\.\d+)?(?:(?:,\s*|\s+and\s+)\d+\.\d+(?:\([^)]*\))?(?:[–-]\d+\.\d+)?)*)"
    typed_bad, typed_n = [], 0
    for m in re.finditer(r"\b" + tw + r"\s+" + spec, text):
        ty = aliases.get(m.group(1).lower()) or aliases.get(re.sub(r"s$", "", m.group(1).lower()))
        for no in T16.expand(m.group(2)):
            typed_n += 1
            if no not in reg:
                typed_bad.append({"ref": m.group(0), "number": no, "problem": "no such result"})
            elif reg[no] != ty:
                typed_bad.append({"ref": m.group(0), "number": no, "problem": f"type is {reg[no]}, not {ty}"})
    res = {**base, "typed_refs": typed_n, "typed_bad": typed_bad}
    # task and check references
    vc = valid_checks()
    bad_tasks, bad_checks, n_t, n_c = [], [], 0, 0
    for m in re.finditer(r"\bTasks? (\d+)(?:[–-](\d+))?", text):
        for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
            n_t += 1
            if not (1 <= k <= 17) or (k not in TASKFILES):
                bad_tasks.append(m.group(0))
    for m in re.finditer(r"\bT(\d+)\.(\d+)\b", text):
        n_c += 1
        k = int(m.group(1))
        if k not in vc or m.group(0) not in vc[k]:
            bad_checks.append(m.group(0))
    for m in re.finditer(r"\bT(\d+) \(?([A-H]\d+)\b", text):
        n_c += 1
        k = int(m.group(1))
        if k not in vc or m.group(2) not in vc[k]:
            bad_checks.append(m.group(0))
    res.update({"task_refs": n_t, "task_bad": sorted(set(bad_tasks)), "check_refs": n_c, "check_bad": sorted(set(bad_checks))})
    res["pass"] = (not res["unresolved"] and res["first_order_1_53"] and not res["typed_bad"] and not res["untyped_bad"]
                   and not res["figure_bad"] and not res["task_bad"] and not res["check_bad"])
    res["seconds"] = round(time.time() - t0, 2)
    return res


# ------------------------------------------------------------------------------------------------------------------ F6
def norm(s):
    s = html.unescape(s)
    s = s.replace("\\", "").replace("`", "").replace("*", "")
    s = re.sub(r"\s*\|\s*", " | ", s).strip()
    return re.sub(r"\s+", " ", s).strip(" |").strip()


def draft_appendix(letter):
    L = draft_lines()
    i = next(k for k, l in enumerate(L) if l.startswith(f"**Appendix {letter} —"))
    j = next((k for k in range(i + 1, len(L)) if L[k].startswith("**Appendix ")), len(L))
    return L[i:j]


def records(lines, kind):
    out = []
    for l in lines:
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


def F6():
    out = {}
    for letter, f in (("A", "Appendix_A_Register.md"), ("C", "Appendix_C_References.md"), ("D", "Appendix_D_Verification.md")):
        d = records(draft_appendix(letter), letter)
        r = records(open(os.path.join(CLS, f)).read().split("\n"), letter)
        diffs = []
        for k in range(max(len(d), len(r))):
            a = d[k] if k < len(d) else None
            b = r[k] if k < len(r) else None
            if a != b:
                diffs.append({"index": k, "draft": a, "render": b})
        dl = draft_appendix(letter)
        intro_d = norm(" ".join(dl[:2]))
        rl = [l for l in open(os.path.join(CLS, f)).read().split("\n") if l.strip()][:2]
        out[letter] = {"draft_records": len(d), "render_records": len(r), "differences": diffs,
                       "intro_draft": intro_d[:600], "intro_render": norm(" ".join(rl))[:600]}
    out["pass"] = all(not out[x]["differences"] for x in "ACD")
    return out


# ------------------------------------------------------------------------------------------------------------------ F7
def F7():
    t = T("Stages_0_4_Thesis.md")
    pats = [r"Theorem 2\.2\s*\([a-d]\)", r"Thm\.? 2\.2\s*\([a-d]\)", r"2\.2\([a-d]\),\s*\(?[a-d]\)?", r"^\([a-d]\) \*(Local constancy|Rays|Windows|Determining data)"]
    hits = []
    for p in pats:
        for m in re.finditer(p, t, re.M):
            hits.append({"pattern": p, "match": m.group(0), "context": t[max(0, m.start() - 40):m.end() + 20]})
    return {"hits": hits, "pass": not hits}


CHECKS = {"F1": F1, "F2": F2, "F3": F3, "F4": F4, "F5": F5, "F6": F6, "F7": F7}


def main():
    os.makedirs(RES, exist_ok=True)
    which = [a for a in sys.argv[1:] if a in CHECKS] or list(CHECKS)
    path = os.path.join(RES, "t18_checks.json")
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
