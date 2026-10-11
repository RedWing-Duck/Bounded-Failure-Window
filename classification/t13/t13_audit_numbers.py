"""C1 (PREREG_t13): every decimal literal (and a x 10^b form) in Sections 1-11 of Stages_0_4_Consolidated.md must be matched
by exactly one registry entry, and every entry must reproduce its literal to the stated precision (half a unit in the last
stated digit) from its formula at 50 digits. Entry kinds: 'formula' (recomputed), 'given' (an input parameter, checked equal),
'record' (a verification record, checked against the cited results file), 'task_id' (a check identifier such as T10.3, checked
to exist in that task's report), 'section' (a heading number), 'old_id' (an old result number, checked in the stage document)."""
import os
import re
import sys

import mpmath as mp

from t13_common import CLS, save_json

sys.path.insert(0, os.path.join(CLS, "t12"))
mp.mp.dps = 50
DOC = os.path.join(CLS, "Stages_0_4_Consolidated.md")
if not os.path.exists(DOC):  # moved unchanged by Task 14 (git mv to archive/)
    DOC = os.path.join(CLS, "archive", "Stages_0_4_Consolidated_v1.md")
PAT = re.compile(r"\d+\.\d+(?:\\times10\^\{-?\d+\})?|\d+\\times10\^\{-?[\d{},]+\}|10\^\{-?[\d{},]+\}")
M = mp.mpf
F001 = M("0.01")


def gstar(Pi, lam=M(1), Sig=F001):
    return -lam + mp.sqrt(lam**2 + 2 * Sig * Pi)


def s2(G, Pi, lam=M(1), Sig=F001):
    return (Sig + G**2 / (2 * Pi)) / (lam + G)


def sstar(Pi, lam=M(1), Sig=F001):
    return gstar(Pi, lam, Sig) / Pi


def relay_tau(tau, G=M("0.5"), Pi=M(1), lam=M(1), Sig=F001):
    a = lam + G
    return (Sig + G**2 / (2 * Pi * (1 + a * tau))) / a


def P_zf(tau, lam=M(1), Sig=F001, Pi=M(1)):
    b = 4 * Sig * tau + 2 * lam / Pi
    D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
    return 4 * Sig / (Pi * (b + mp.sqrt(D)))


def V_tau(tau, lam=M(1), Sig=F001, Pi=M(1)):
    f = lambda G: (Sig + G**2 / (2 * Pi * (1 + (lam + G) * tau))) / (lam + G)
    g = mp.findroot(lambda G: mp.diff(f, G), M("0.02"))
    return min(f(g), F001 / M(1), 1 / (2 * Pi * tau))


def d1():
    from t12_common import analyse_dt, classify
    q = {"lam": 1, "Sig": "0.01", "Pi": 1, "G": "0.5"}
    Ap, Aa = analyse_dt("D1", "post", q), analyse_dt("D1", "avg", q)
    mx = Ap["turns"][0]
    mn = [t for t in Aa["turns"] if t["kind"] == "min"][-1]
    return {"max": mx["value"], "argmax": mx["theta"], "min": mn["value"], "argmin": mn["theta"], "L0": Ap["L_minus"]}


_D1 = None


def D1(k):
    global _D1
    if _D1 is None:
        _D1 = d1()
    return _D1[k]


def peak_bayes(kap, lam=M(1), Sig=F001, c=M(1)):
    P0 = c * lam / (kap * Sig)
    Gr = -lam + mp.sqrt(lam**2 + lam * c - 2 * Sig * P0)
    Pr = P0 * Gr / (c - Gr)
    return s2(Gr, Pr, lam, Sig) / (Sig / lam)


def peak_mis(x, lam=M(1), Sig=F001, l1=M(1)):
    F = Sig / lam
    S1 = x * F * l1
    r = Sig / S1
    a2, b1, c0 = 1 + r, 4 * r * l1, 2 * lam * l1 - 4 * r * l1**2
    G = 2 * c0 / (b1 + mp.sqrt(b1**2 + 4 * a2 * c0))
    Pr = (G**2 + 2 * l1 * G) / (2 * S1)
    return s2(G, Pr, lam, Sig) / F


def pi0pair(n):
    sys.path.insert(0, os.path.join(CLS, "t13"))
    from t13_partA_numeric import pi0_pair
    return pi0_pair(M(n), M(1), M(1), F001)[0]


def dpdx_MI():
    import json
    d = json.load(open(os.path.join(CLS, "t13", "results", "t13_A3_proof.json")))
    for it in d["A3"]:
        if it["desc"].startswith("4 dp/dx > 0"):
            return M(it["info"])


def P_delay(d, lam=M(1), Sig=F001, Pi=M(1)):
    F = Sig / lam
    return F - mp.exp(-2 * lam * d) * (F - sstar(Pi, lam, Sig))


def d1_small():
    """G = 0.019 < 2 F Pi = 0.02: D1 avg has a maximum then a minimum below its Delta t -> 0 limit (two rays below that value)."""
    from t12_common import analyse_dt
    A = analyse_dt("D1", "avg", {"lam": 1, "Sig": "0.01", "Pi": 1, "G": "0.019"})
    k = [t["kind"] for t in A["turns"]]
    return M("0.019") < 2 * F001 and k == ["max", "min"] and A["turns"][1]["value"] < A["L_minus"]


def d2_c3():
    """c = 3: P+ > F on a grid of Delta t and P+ -> 4F."""
    from t12_common import dt_funcs
    f, _ = dt_funcs("D2", "post", {"lam": 1, "Sig": "0.01", "Pi": 1, "c": 3, "Pi0": 1})
    return all(f(M(10)**e) > F001 for e in range(-6, 9)) and abs(f(M(10)**12) / F001 - 4) < M("1e-6")


def rec(path, needle):
    """record check: the cited results file contains the needle string."""
    def chk():
        return needle in open(os.path.join(CLS, path)).read()
    return chk


# (literal, anchor substring on the same line, kind, formula/value or check)
REG = [
    ("0.01", "Worked example** ($\\lambda = c = 1$, $\\Sigma = 0.01$): $\\Pi_B = 50$", "given", F001),
    ("0.0099505", "(P3): $G^\\star = 0.0099505$", "formula", lambda: gstar(M(1))),
    ("99.498", "\\Pi_0^\\star = 99.498", "formula", lambda: M(1) * (1 / gstar(M(1)) - 1)),
    ("0.0099505", "\\sigma_\\star^2 = 0.0099505$, $V_c = 0.255", "formula", lambda: sstar(M(1))),
    ("0.255", "$V_c = 0.255$", "formula", lambda: s2(M(1), M(1))),
    ("64.162", "\\Pi_0^\\star = 64.162", "formula", lambda: M(60) * (1 / gstar(M(60)) - 1)),
    ("0.0080540", "\\sigma_\\star^2 = 0.0080540", "formula", lambda: sstar(M(60))),
    ("0.0091667", "$V_c = 0.0091667$", "formula", lambda: s2(M(1), M(60))),
    ("0.0055", "$V_c = 0.0055$", "formula", lambda: s2(M(1), M(500))),
    ("0.01", "$\\Sigma = 0.01$, $\\Pi = \\Pi_0 = 1$): $c^\\star", "given", F001),
    ("0.019901", "c^\\star = 0.019901", "formula", lambda: gstar(M(1)) / M("0.5")),
    ("0.0099505", "c^\\star = 0.019901$, $\\sigma_\\star^2 = 0.0099505", "formula", lambda: sstar(M(1))),
    ("0.04", "$c_F = 0.04$", "formula", lambda: 2 * F001 * 2),
    ("0.01", "so $G = 0.5$): $V_w", "given", F001),
    ("0.5", "so $G = 0.5$): $V_w", "formula", lambda: M(1) * 1 / (1 + 1)),
    ("0.09", "$V_w = 0.09$", "formula", lambda: s2(M("0.5"), M(1))),
    ("0.0066667", "$H_G = 0.0066667$, $\\tau_F = 16$", "formula", lambda: F001 / M("1.5")),
    ("0.04", "$\\sigma^2(1) = 0.04$", "formula", lambda: relay_tau(M(1))),
    ("0.011875", "$\\sigma^2(10) = 0.011875$", "formula", lambda: relay_tau(M(10))),
    ("0.01", "$\\sigma^2(16) = 0.01$", "formula", lambda: relay_tau(M(16))),
    ("2\\times10^{-17}", "Wiener route to $2\\times10^{-17}$", "record", rec("t9/RESULTS_t9.md", "rel. err 2.1e-17, 2.0e-17, 1.5e-17")),
    ("0.01", "**Worked example** ($\\lambda = 1$, $\\Sigma = 0.01$, $\\Pi = 1$): $\\sigma_\\star^2 = 0.0099505$; $P(1)", "given", F001),
    ("0.0099505", "$\\sigma_\\star^2 = 0.0099505$; $P(1) = 0.0098039$", "formula", lambda: sstar(M(1))),
    ("0.0098039", "$P(1) = 0.0098039$", "formula", lambda: P_zf(M(1))),
    ("0.0099010", "$V(1) = 0.0099010$; $P(10)", "formula", lambda: V_tau(M(1))),
    ("0.0067813", "$P(10) = 0.0067813$", "formula", lambda: P_zf(M(10))),
    ("0.5", "The fixed relay with $G = 0.5$ gives $0.04$", "given", M("0.5")),
    ("0.04", "The fixed relay with $G = 0.5$ gives $0.04$", "formula", lambda: relay_tau(M(1))),
    ("0.011875", "and $0.011875$; as $\\tau \\to \\infty$", "formula", lambda: relay_tau(M(10))),
    ("0.0066667", "$H_G = 0.0066667$ while $P \\to 0$", "formula", lambda: F001 / M("1.5")),
    ("1.0\\times10^{-14}", "three routes agree to $1.0\\times10^{-14}$", "record", rec("t10/RESULTS_t10.md", "max pairwise relative difference 1.01e-14")),
    ("10^{-50}", "shape exact to $10^{-50}$", "record", rec("t10/RESULTS_t10.md", "max turning-point position error 8.81e-51; max symmetry error 4.87e-51")),
    ("8\\times10^{-51}", "T11.3 to $8\\times10^{-51}$", "record", rec("t11/RESULTS_t11.md", "max relative difference 7.79e-51")),
    ("10^{-30}", "$\\Delta t_E$ to $10^{-30}$", "record", rec("t12/RESULTS_t12.md", "max rel. error of Δt_E 1.14e-30")),
    ("0.031263", "($dp/dx = 0.031263$ at $x = u = 1$)", "formula", dpdx_MI),
    ("10^{-17}", "relative dips from $10^{-17}$", "record", rec("t12/RESULTS_t12.md", "between 10^-32880317 and 10^-17")),
    ("10^{-32{,}880{,}317}", "down to $10^{-32{,}880{,}317}$", "record", rec("t12/RESULTS_t12.md", "between 10^-32880317 and 10^-17")),
    ("0.5", "**Worked example** (D1, $G = 0.5$", "given", M("0.5")),
    ("0.01", "**Worked example** (D1, $G = 0.5$, $\\lambda = 1$, $\\Sigma = 0.01$", "given", F001),
    ("0.09", "post rises from $0.09$ to a single maximum", "formula", lambda: D1("L0")),
    ("0.20457", "single maximum\n$0.20457$", "formula", lambda: D1("max")),
    ("2.4645", "at $\\Delta t = 2.4645$", "formula", lambda: D1("argmax")),
    ("0.09", "a window for $R^2 \\in (0.09, 0.20457)$", "formula", lambda: D1("L0")),
    ("0.20457", "a window for $R^2 \\in (0.09, 0.20457)$", "formula", lambda: D1("max")),
    ("0.0099875", "dips to $0.0099875$", "formula", lambda: D1("min")),
    ("0.125", "(a dip of $0.125\\%$)", "formula", lambda: (F001 - D1("min")) / F001 * 100),
    ("6\\times10^{-31}", "maximum position to $6\\times10^{-31}$", "record", rec("t12/RESULTS_t12.md", "max error of the maximum's position 6.05e-31")),
    ("1.25", "failure set at\n$R^2 = 1.25F$", "given", M("1.25")),
    ("1.5", "peak value $1.5F$ and strictly decreasing", "given", M("1.5")),
    ("1.25", "so it crosses $1.25F$ exactly twice", "given", M("1.25")),
    ("10^{12}", "$G(10^{12})/G(10^{11}) - 1", "given", M(10)**12),
    ("10^{11}", "$G(10^{12})/G(10^{11}) - 1", "given", M(10)**11),
    ("6\\times10^{-10}", "$G(10^{12})/G(10^{11}) - 1 = 6\\times10^{-10}$", "record", rec("t10/RESULTS_t10.md", "G(1e12)/G(1e11) − 1 = 6e-10")),
    ("0.01", "($F'/F = \\kappa = 100$, with $\\lambda = \\lambda' = c = 1$, $\\Sigma = 0.01$)", "given", F001),
    ("17.575", "the peak is $M/F = 17.575$", "formula", lambda: peak_mis(M(100))),
    ("9.2875", "against $9.2875$", "formula", lambda: peak_bayes(M(100))),
    ("1.892", "a ratio of $1.892$", "formula", lambda: peak_mis(M(100)) / peak_bayes(M(100))),
    ("1.5", "regression against Task 10's table for $n = 1.5, 2, 3, 4, 8$", "given", M("1.5")),
    ("1.01", "with real $n \\in [1.01, 10]$", "given", M("1.01")),
    ("0.01", "At $\\lambda = c = 1$, $\\Sigma = 0.01$: $\\Pi_0^{\\text{pair}} = 30.243", "given", F001),
    ("30.243", "$\\Pi_0^{\\text{pair}} = 30.243", "formula", lambda: pi0pair("1.5")),
    ("31.475", "= 30.243, 31.475", "formula", lambda: pi0pair("2")),
    ("37.820", "31.475, 37.820", "formula", lambda: pi0pair("3")),
    ("44.180", "37.820, 44.180", "formula", lambda: pi0pair("4")),
    ("62.711", "44.180, 62.711", "formula", lambda: pi0pair("8")),
    ("1.5", "62.711$ for $n = 1.5, 2, 3, 4, 8$", "given", M("1.5")),
    ("5\\times10^{-4}", "has median $5\\times10^{-4}$", "record", rec("t10/RESULTS_t10.md", "median 0.000498")),
    ("4\\times10^{-22}", "$4\\times10^{-22}$ to $0.96$", "record", rec("t10/RESULTS_t10.md", "min 4.43e-22")),
    ("0.96", "$4\\times10^{-22}$ to $0.96$", "record", rec("t10/RESULTS_t10.md", "max 0.962")),
    ("1.50007", "fitted exponents $1.50007$", "record", rec("t10/RESULTS_t10.md", "slopes 1.50007 and 0.50002")),
    ("0.50002", "$0.50002$ (positions)", "record", rec("t10/RESULTS_t10.md", "slopes 1.50007 and 0.50002")),
    ("10^{-8}", "Windows of relative width $10^{-8}$", "record", rec("t10/RESULTS_t10.md", "Narrow windows (relative width 1e-8)")),
    ("4.4", "$4.4\\times10^6$ over the", "record", rec("t12/RESULTS_t12.md", "4,400,000 classifications")),
    ("6\\times10^{-31}", "reduction T10.3, position error $6\\times10^{-31}$", "record", rec("t10/RESULTS_t10.md", "Bayesian 6.04e-31")),
    ("1.91", "Monte Carlo $|z| \\le 1.91$", "record", rec("t11/RESULTS_t11.md", "MC |z| ≤ 1.91")),
    ("0.01", "Example ($\\lambda = 1$, $\\Sigma = 0.01$,", "given", F001),
    ("0.0099505", "$P(0) = 0.0099505$", "formula", lambda: P_delay(M(0))),
    ("0.0099763", "$P(1/e) = 0.0099763$", "formula", lambda: P_delay(1 / mp.e)),
    ("0.01", "$\\Sigma = 0.01$, $\\Pi = \\Pi_0 = 1$,\n$c = 3$", "record", d2_c3),
    ("0.019", "(e.g. $G = 0.019$, $\\lambda = 1$", "record", lambda: d1_small()),
    ("0.01", "(e.g. $G = 0.019$, $\\lambda = 1$, $\\Sigma = 0.01$", "given", F001),
]
TASKFILE = {"8": "REPORT.md", "9": "t9/RESULTS_t9.md", "10": "t10/RESULTS_t10.md", "11": "t11/RESULTS_t11.md",
            "12": "t12/RESULTS_t12.md"}
STAGE_DOCS = ["Stage_2_Completion_Results.md", "Stage_4_Optimality_Results.md", "Stage_3_Falsification_Results.md"]


def stated_ok(lit, val):
    """Half a unit in the last stated digit."""
    if "times10" in lit or lit.startswith("10^"):
        m_ = re.match(r"(?:(\d+(?:\.\d+)?)\\times)?10\^\{?(-?[\d{},]+)\}?", lit)
        mant = m_.group(1) or "1"
        ex = int(m_.group(2).replace("{,}", "").replace(",", "").strip("{}"))
        dec = len(mant.split(".")[1]) if "." in mant else 0
        target = M(mant) * M(10)**ex
        return abs(val - target) <= M(5) * M(10)**(ex - dec - 1)
    dec = len(lit.split(".")[1])
    return abs(val - M(lit)) <= M(5) * M(10)**(-(dec + 1))


def main():
    doc = open(DOC).read()
    body = doc.split("\n## 12. Verification appendix")[0]
    lines = body.split("\n")
    occ = []
    for m_ in PAT.finditer(body):
        ln = body[:m_.start()].count("\n")
        line = lines[ln]
        col = m_.start() - (body.rfind("\n", 0, m_.start()) + 1)
        occ.append({"lit": m_.group(), "line": ln + 1, "text": line, "col": col,
                    "ctx": body[max(0, m_.start() - 200):m_.end() + 200]})
    used = [0] * len(REG)
    res = {"unmatched": [], "ambiguous": [], "entries": [], "ids": []}
    for o in occ:
        lit, line, col = o["lit"], o["text"], o["col"]
        prev = line[max(0, col - 1):col]
        if prev == "T" and re.match(r"\d+\.\d+$", lit):                      # task check id
            task = lit.split(".")[0]
            ok = task in TASKFILE and f"T{lit}" in open(os.path.join(CLS, TASKFILE[task])).read()
            res["ids"].append({"kind": "task_id", "lit": "T" + lit, "line": o["line"], "pass": bool(ok)})
            continue
        if line.lstrip().startswith("#") and re.match(r"\d+\.\d+$", lit):   # section heading
            res["ids"].append({"kind": "section", "lit": lit, "line": o["line"], "pass": True})
            continue
        if re.search(r"(It was (Numerical result|Conjecture) )[\d./ ]*$", line[:col]) or "Numerical result 2.8 / 4.10a" in line \
                and lit in ("2.8", "4.10"):
            ok = any(lit in open(os.path.join(CLS, d_)).read() for d_ in STAGE_DOCS)
            res["ids"].append({"kind": "old_id", "lit": lit, "line": o["line"], "pass": bool(ok)})
            continue
        cands = [i for i, (l_, anc, _, _) in enumerate(REG) if l_ == lit and anc in o["ctx"]]
        if not cands:
            res["unmatched"].append({"lit": lit, "line": o["line"], "text": line[:160]})
        elif len(cands) > 1:
            # prefer an unused candidate whose anchor is on the literal's own line
            own = [i for i in cands if REG[i][1] in line and not used[i]] or [i for i in cands if not used[i]]
            if not own:
                res["ambiguous"].append({"lit": lit, "line": o["line"], "cands": cands})
                continue
            used[own[0]] += 1
        else:
            used[cands[0]] += 1
    for i, (lit, anc, kind, f) in enumerate(REG):
        e = {"lit": lit, "anchor": anc[:80], "kind": kind, "uses": used[i]}
        try:
            if kind == "formula":
                v = f()
                e["computed"] = mp.nstr(v, 20)
                e["pass"] = bool(stated_ok(lit, v))
            elif kind == "given":
                e["pass"] = bool(stated_ok(lit, f))
            else:
                e["pass"] = bool(f())
        except Exception as ex:  # noqa: BLE001
            e["pass"], e["error"] = False, repr(ex)
        if used[i] != 1:
            e["pass"] = False
            e["use_error"] = f"used {used[i]} times"
        res["entries"].append(e)
    res["n_literals"] = len(occ)
    res["n_formula"] = sum(e["kind"] == "formula" for e in res["entries"])
    res["n_fail_entries"] = sum(not e["pass"] for e in res["entries"])
    res["n_fail_ids"] = sum(not x["pass"] for x in res["ids"])
    res["pass"] = not res["unmatched"] and not res["ambiguous"] and res["n_fail_entries"] == 0 and res["n_fail_ids"] == 0
    for e in res["entries"]:
        if not e["pass"]:
            print("FAIL", e)
    for u_ in res["unmatched"]:
        print("UNMATCHED", u_)
    print(f"C1: {'PASS' if res['pass'] else 'FAIL'}; literals {len(occ)}, registry {len(REG)} ({res['n_formula']} formulas), ids "
          f"{len(res['ids'])}, unmatched {len(res['unmatched'])}, failing entries {res['n_fail_entries']}, failing ids {res['n_fail_ids']}")
    save_json(res, "t13_audit_numbers.json")


if __name__ == "__main__":
    main()
