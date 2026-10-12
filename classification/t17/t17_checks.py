"""Task 17 checks E1, E3, E4, E6, E7 and the E2 extraction (PREREG_t17.md, commit d23797b). E1 item 6, E2's classification and
E5 are manual readings made after the run (t17/results/). Usage: python3 t17_checks.py [E1 E2 E3 E4 E6 E7]   (default: all)"""
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
RES = os.environ.get("T17_RES") or os.path.join(HERE, "results")
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_ch1-7.md")
sys.path[:0] = [os.path.join(CLS, "t16"), os.path.join(CLS, "t15"), os.path.join(CLS, "register")]
import t16_checks as T16  # noqa: E402
mp.mp.dps = 50
T16_HEAD = "daae576"


def draft_upto(heading):
    L = open(DRAFT).read().split("\n")
    return L[:next(i for i, l in enumerate(L) if l.startswith(heading))]


def J(*p):
    return json.load(open(os.path.join(CLS, *p)))


def T(*p):
    return open(os.path.join(CLS, *p)).read()


# ------------------------------------------------------------------------------------------------------------------ E1
R1, R2 = random.Random(17001), random.Random(17002)


def U(rng=R1, lo=1e-3, hi=1e3):
    return mp.mpf(10) ** mp.mpf(rng.uniform(math.log10(lo), math.log10(hi)))


def denest(e):
    """Denesting step: sqrt(X) with factor(X) = c*Y**2, c > 0 a number and Y positive under the stated positivity, becomes sqrt(c)*Y.
    Only perfect squares are touched; the sign of Y is argued in each item."""
    def rep(x):
        f = sp.factor(x.base)
        c, rest = f.as_coeff_Mul()
        if c > 0 and rest.is_Pow and rest.exp == 2:
            return sp.sqrt(c) * rest.base
        if c > 0 and rest.is_Mul and all(a.is_Pow and a.exp % 2 == 0 for a in rest.args):
            return sp.sqrt(c) * sp.Mul(*[a.base ** (a.exp // 2) for a in rest.args])
        return x
    return e.replace(lambda x: x.is_Pow and x.exp == sp.S.Half, rep)


def zero(e):
    for name, f in (("simplify", sp.simplify), ("factor(radsimp)", lambda x: sp.factor(sp.radsimp(x))),
                    ("denest+simplify", lambda x: sp.simplify(denest(x)))):
        try:
            if f(e) == 0:
                return {"zero": True, "route": name}
        except Exception:  # noqa: BLE001
            pass
    return {"zero": False, "route": None, "residual": str(sp.simplify(e))[:300]}


def ident(lhs, rhs, syms, sampler=None, rel=True):
    """Identity with the pre-registered numerical fallback (seed 17002, 1,000 sets, relative residual < 1e-35)."""
    z = zero(lhs - rhs)
    f, g = sp.lambdify(syms, lhs, "mpmath"), sp.lambdify(syms, rhs, "mpmath")
    worst = mp.mpf(0)
    for _ in range(1000):
        vals = sampler(R2) if sampler else [U(R2) for _ in syms]
        a_, b_ = f(*vals), g(*vals)
        d = abs(a_ - b_) / (max(abs(a_), abs(b_)) if rel and max(abs(a_), abs(b_)) > 0 else 1)
        worst = max(worst, d)
    z["fallback_max_rel"] = float(worst)
    z["fallback_pass"] = worst < mp.mpf(10) ** -35
    z["holds"] = z["zero"] or z["fallback_pass"]
    return z


def numeric(pred, sampler, n=1000):
    bad, seen = [], 0
    while seen < n:
        s = sampler()
        if s is None:
            continue
        seen += 1
        if not pred(*s):
            bad.append([mp.nstr(x, 8) for x in s])
    return {"n": seen, "counterexamples": len(bad), "examples": bad[:3], "holds": not bad}


lam, Sig, Pi, tau, G, q, K, x, w, a_s, b_s, dl = sp.symbols("lambda Sigma Pi tau G q K x w a b delta", positive=True)
beta = sp.symbols("beta", real=True)
F = Sig / lam


def e1_item1():
    nu, t = 2 * Sig * Pi / lam**2, lam * tau
    b = 4 * Sig * tau + 2 * lam / Pi
    D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
    W = (1 + nu * t)**2 + nu * (1 - t)**2
    out = {"Pi_b": ident(Pi * b, 2 * lam * (1 + nu * t), [lam, Sig, Pi, tau]),
           "Pi2_D": ident(Pi**2 * D, 4 * lam**2 * W, [lam, Sig, Pi, tau])}
    out["sign"] = {"text": "Pi > 0, D > 0 and W > 0 (sums of squares and positive terms), so Pi*sqrt(D) = sqrt(Pi^2 D) = "
                           "sqrt(4 lambda^2 W) = 2 lambda sqrt(W).", "holds": True}
    P = 4 * Sig / (Pi * (b + 2 * lam * sp.sqrt(W) / Pi))     # sqrt(D) replaced by its verified equal 2 lambda sqrt(W)/Pi
    out["P_over_F"] = ident(P / F, 2 / (1 + nu * t + sp.sqrt(W)), [lam, Sig, Pi, tau])
    Praw = 4 * Sig / (Pi * (b + sp.sqrt(D)))
    out["P_over_F_numeric_raw"] = ident(Praw / F, 2 / (1 + nu * t + sp.sqrt(W)), [lam, Sig, Pi, tau])
    nus = sp.symbols("nu", positive=True)
    at0 = (2 / (1 + nus * x + sp.sqrt((1 + nus * x)**2 + nus * (1 - x)**2))).subs(x, 0)
    out["t0"] = ident(at0, 2 / (1 + sp.sqrt(1 + nus)), [nus])
    out["holds"] = all(v["holds"] for v in out.values())
    return out


def e1_item2():
    a = lam + G
    s2 = (Sig + G**2 / (2 * Pi * (1 + a * tau))) / a
    qq = G / (F * Pi)
    nu, t = 2 * Sig * Pi / lam**2, lam * tau
    Vt = (1 + nu * qq**2 / (4 * (1 + t * (1 + nu * qq / 2)))) / (1 + nu * qq / 2)
    out = {"normal_form": ident(s2 / F, Vt, [lam, Sig, Pi, tau, G]),
           "excess_factorisation": ident(s2 - F, G * (G / (2 * Pi * (1 + a * tau)) - F) / a, [lam, Sig, Pi, tau, G])}
    out["excess_sign"] = {"text": "sigma^2 - F = (G/a)(G/(2 Pi (1 + a tau)) - F), G/a > 0, so sigma^2 > F iff G/Pi > 2F(1 + a tau), "
                                  "i.e. q = G/(F Pi) > 2(1 + a tau).", "holds": True}
    f = sp.lambdify([lam, Sig, Pi, tau, G], s2, "mpmath")

    def pred(l_, S_, P_, t_, G_):
        F_ = S_ / l_
        return (f(l_, S_, P_, t_, G_) > F_) == (G_ / (F_ * P_) > 2 * (1 + (l_ + G_) * t_))
    out["excess_numeric"] = numeric(pred, lambda: [U() for _ in range(5)])
    out["holds"] = all(v["holds"] for v in out.values())
    return out


def e1_item3():
    a, L, r, Fs, Pm = sp.symbols("a L r F Pm", positive=True)
    qq = Fs * (1 - a**2)
    sol = sp.solve(sp.Eq(Pm, a**2 * ((1 - L)**2 * Pm + L**2 * r) + qq), Pm)
    form = (a**2 * L**2 * r + qq) / (1 - a**2 * (1 - L)**2)
    samp = lambda rng: [mp.mpf(rng.uniform(0.01, 0.99)), mp.mpf(rng.uniform(0.01, 1.99)), U(rng), U(rng)]
    out = {"P_minus": ident(sol[0], form, [a, L, r, Fs], sampler=samp),
           "numerator": ident((a**2 * L**2 * r + qq) - Fs * (1 - a**2 * (1 - L)**2), a**2 * L * (L * r - Fs * (2 - L)),
                              [a, L, r, Fs], sampler=samp, rel=False)}
    out["denominator_sign"] = {"text": "for 0 <= L < 2, |1 - L| <= 1, so a^2 (1 - L)^2 <= a^2 < 1 when 0 < a < 1.", "holds": True}

    def pred_eq(a_, L_, r_, F_):
        Pm_ = (a_**2 * L_**2 * r_ + F_ * (1 - a_**2)) / (1 - a_**2 * (1 - L_)**2)
        return (Pm_ > F_) == (L_ / (2 - L_) > F_ / r_)
    out["excess_equivalence"] = numeric(pred_eq, lambda: samp(R1))
    out["P_plus"] = ident((Pm - qq) / a**2 - Fs, (Pm - Fs) / a**2, [Pm, a, Fs],
                          sampler=lambda rng: [U(rng), mp.mpf(rng.uniform(0.01, 0.99)), U(rng)])
    Ms = sp.symbols("M", positive=True)
    out["Lstar_ratio"] = ident((Ms / (Ms + r)) / (2 - Ms / (Ms + r)), Ms / (Ms + 2 * r), [Ms, r])
    out["Lstar_sign"] = {"text": "L*/(2 - L*) = M/(M + 2r) < F/(2r) iff M(2r - F) < 2rF; if 2r <= F it holds trivially, "
                                 "otherwise M < F < 2rF/(2r - F). Needs the optimal prior M < F (tested below).", "holds": True}

    def kalman():
        l_, S_, P_, dt = U(), U(), U(), U(R1, 1e-4, 1e2)
        F_ = S_ / l_
        a_ = mp.e ** (-l_ * dt)
        q_, r_ = F_ * (1 - a_**2), 1 / (P_ * dt)
        # steady prior M: M = a^2 M r/(M + r) + q  =>  M^2 + (r(1 - a^2) - q) M - q r = 0
        bb = r_ * (1 - a_**2) - q_
        M = (-bb + mp.sqrt(bb**2 + 4 * q_ * r_)) / 2
        Ls = M / (M + r_)
        return M, F_, Ls, F_ * P_ * dt
    out["Lstar_numeric"] = numeric(lambda M, F_, Ls, phi: M < F_ and Ls / (2 - Ls) < phi / 2, kalman)
    out["holds"] = all(v["holds"] for v in out.values())
    return out


def e1_item4():
    Pp, dt, tt = sp.symbols("Pp Delta_t t", positive=True)
    s = 1 - sp.exp(-2 * lam * dt)
    Pbar = F - (F - Pp) * s / (2 * lam * dt)
    out = {"identity": ident(Pbar - F, (Pp - F) * s / (2 * lam * dt), [lam, Sig, Pp, dt])}
    avg = sp.integrate(sp.exp(-2 * lam * tt) * Pp + F * (1 - sp.exp(-2 * lam * tt)), (tt, 0, dt)) / dt
    out["definition_is_time_average"] = ident(avg, Pbar, [lam, Sig, Pp, dt])
    out["holds"] = all(v["holds"] for v in out.values())
    return out


def e1_item5():
    u, g = sp.symbols("u g", positive=True)
    s2 = (Sig + G**2 / (2 * Pi)) / (lam + G)
    e = (s2 / F).subs(G, g * lam).subs(Sig, u * lam**2 / (2 * Pi))
    out = {"scaling": ident(e, (1 + g**2 / u) / (1 + g), [lam, Pi, g, u])}

    def samp():
        l_, uu = U(), U()
        A_, p_ = U(), mp.mpf(R1.uniform(0.2, 3))
        gam = A_ * uu**p_ / (1 + uu**p_)            # a smooth gain law in u: G = lambda * gamma(u)
        G_ = l_ * gam
        S1, S2 = U(), U()
        P1, P2 = uu * l_**2 / (2 * S1), uu * l_**2 / (2 * S2)
        v1 = (S1 + G_**2 / (2 * P1)) / (l_ + G_) / (S1 / l_)
        v2 = (S2 + G_**2 / (2 * P2)) / (l_ + G_) / (S2 / l_)
        return v1, v2
    out["same_u_same_ratio"] = numeric(lambda v1, v2: abs(v1 - v2) <= mp.mpf(10)**-40 * abs(v1), samp)
    out["argument"] = {"text": "u = 2 Sigma Pi/lambda^2 is a strictly increasing bijection of Sigma (fixed Pi) and of Pi (fixed "
                               "Sigma); sigma^2/F is a function of u alone, so {sigma^2/F > r} is the same set of u along both sweeps.",
                       "holds": True}
    out["holds"] = all(v["holds"] for v in out.values())
    return out


def e1_item7():
    a = sp.symbols("a", real=True, nonzero=True)
    roots = sp.solve(a * (x**2 - w), x)
    xs = sp.symbols("xs", real=True)
    roots = sp.solve(a * (xs**2 - w), xs)
    integral = sp.integrate(a * (xs**2 - w), (xs, -sp.sqrt(w), sp.sqrt(w)))
    out = {"roots": {"roots": [str(r_) for r_ in roots], "holds": set(roots) == {sp.sqrt(w), -sp.sqrt(w)}},
           "change": {"integral": str(sp.simplify(integral)), **zero(integral + sp.Rational(4, 3) * a * w**sp.Rational(3, 2))}}
    out["change"]["holds"] = out["change"]["zero"]
    out["abs"] = {"text": "|-(4/3) a w^(3/2)| = (4/3)|a| w^(3/2) for w = b*delta > 0.", "holds": True}
    out["holds"] = all(v["holds"] for v in out.values())
    return out


def e1_item8():
    A, B, C = sp.symbols("A B C", positive=True)

    def samp():
        return [U(), U(), U()]
    out = {"bound_numeric": numeric(lambda A_, B_, C_: 2 * C_ / (B_ + mp.sqrt(B_**2 + 4 * A_ * C_)) <= mp.sqrt(C_ / A_), samp)}
    out["bound_sign"] = {"text": "B > 0 gives B + sqrt(B^2 + 4AC) > sqrt(4AC) = 2 sqrt(AC), so 2C/(B + sqrt(B^2 + 4AC)) < "
                                 "2C/(2 sqrt(AC)) = sqrt(C/A).", "holds": True}
    v = K / 2 * tau**(beta - 1)
    Aexp, Cexp = (1 - lam * tau)**2 / tau, 4 * Sig * v
    out["C_over_A"] = ident(sp.powsimp(Cexp / Aexp, force=True), 2 * Sig * K * tau**beta / (1 - lam * tau)**2,
                            [Sig, K, tau, beta, lam],
                            sampler=lambda rng: [U(rng), U(rng), U(rng), mp.mpf(rng.uniform(-3, 5)), U(rng)])
    out["sqrt_form"] = {"text": "C/A = 2 Sigma K tau^beta/(1 - lambda tau)^2 > 0 for lambda tau != 1, and (sqrt(2 Sigma K) "
                                "tau^(beta/2)/|1 - lambda tau|)^2 equals it with both sides positive.", "holds": True}
    out["holds"] = all(vv["holds"] for vv in out.values())
    return out


def e1_item9():
    Af = lambda tt: (1 - lam * tt)**2 / tt
    out = {"A_invariant": ident(Af(1 / (lam**2 * tau)), Af(tau), [lam, tau], rel=True)}
    Kp = K * lam**(2 - 2 * beta)
    xx = 1 / (lam**2 * tau)
    v_dual = Kp / 2 * xx**(1 - (2 - beta) + 0)        # v_{2-beta,K'}(x) = (K'/2) x^((2 - beta) - 1)
    v_dual = Kp / 2 * xx**((2 - beta) - 1)
    v_orig = K / 2 * tau**(beta - 1)
    smp = lambda rng: [U(rng), U(rng), U(rng), mp.mpf(rng.uniform(-3, 5))]
    out["v_dual"] = ident(sp.powsimp(sp.expand_power_base(v_dual, force=True), force=True), v_orig, [K, lam, tau, beta], sampler=smp)

    def P(A_, v_, S_, l_):
        B_, C_ = 4 * (S_ + l_ * v_), 4 * S_ * v_
        return 2 * C_ / (B_ + mp.sqrt(B_**2 + 4 * A_ * C_))

    def pred():
        l_, S_, K_, t_ = U(), U(), U(), U()
        b_ = mp.mpf(R1.uniform(-3, 5))
        p1 = P((1 - l_ * t_)**2 / t_, K_ / 2 * t_**(b_ - 1), S_, l_)
        x_ = 1 / (l_**2 * t_)
        K2 = K_ * l_**(2 - 2 * b_)
        p2 = P((1 - l_ * x_)**2 / x_, K2 / 2 * x_**((2 - b_) - 1), S_, l_)
        return (abs(p1 - p2) / p1,)
    out["P_identity_numeric"] = numeric(lambda r_: r_ < mp.mpf(10)**-35, pred)
    out["holds"] = all(vv["holds"] for vv in out.values())
    return out


def E1():
    items = {"1 Cor 6.5": e1_item1, "2 Lemma 6.1 normal form": e1_item2, "3 Prop 6.13": e1_item3, "4 Lemma 6.14": e1_item4,
             "5 Lemma 6.23": e1_item5, "7 Prop 2.7": e1_item7, "8 Thm 7.8 bound": e1_item8, "9 Prop 7.10": e1_item9}
    out = {}
    t0 = time.time()
    for k, f in items.items():
        t1 = time.time()
        out[k] = f()
        out[k]["seconds"] = round(time.time() - t1, 2)
        print("E1", k, "holds" if out[k]["holds"] else "DOES NOT HOLD", flush=True)
    out["6 Cor 7.4"] = {"note": "logical review after the run: t17/results/e1_item6_review.md"}
    out["seconds"] = round(time.time() - t0, 2)
    return out


# ------------------------------------------------------------------------------------------------------------------ E2
def E2():
    import render  # noqa: E402
    reg = [e for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))
           if e["thesis_no"] in ("2.4", "2.5", "2.6", "2.7") or e["thesis_no"].split(".")[0] in "67"]
    DL = draft_upto("## 8.")
    RL = render.Renderer("thesis").render(T("source", "Stages_0_4_Source.md")).split("\n")   # no thesis overrides
    tau_nf = T("source", "thesis_only", "tau-optimal-normal-form.md").split("\n")
    pairs = []
    for e in reg:
        no, ty = e["thesis_no"], e["type"]
        rx = re.compile(r"\*\*" + re.escape(ty) + " " + re.escape(no) + r"\b")
        di = next((i for i, l in enumerate(DL) if rx.search(l)), None)
        dtxt = T16.block(DL, di) if di is not None else None
        ri = next((i for i, l in enumerate(RL) if rx.search(l)), None)
        rtxt = T16.block(RL, ri) if ri is not None else None
        if no == "6.5" and rtxt is None:
            rtxt = "\n".join(tau_nf)
        if no == "6.13":
            m = re.search(r"\*\*6\.13 = Proposition 6 \(p\. 7\)\.\*\* (.*)", T("RESULTS_t15.md"))
            rtxt = "(manuscript, Paper 1, Proposition 6, p. 7, as quoted in RESULTS_t15.md) " + (m.group(1) if m else "(not found)")
        dproof = None
        if di is not None:
            k = di + 1
            while k < len(DL) and not DL[k].startswith("*Proof") and not re.match(r"^\*\*" + T16.TYPES + r" \d|^#", DL[k]):
                k += 1
            if k < len(DL) and DL[k].startswith("*Proof"):
                dproof = DL[k][:400]
        rproof = None
        if ri is not None:
            k = ri + 1
            while k < len(RL) and not RL[k].startswith("*Proof") and not re.match(r"^\*\*" + T16.TYPES + r" \d|^#|^\*\*Label", RL[k]):
                k += 1
            rproof = "yes" if k < len(RL) and RL[k].startswith("*Proof") else None
        pairs.append({"no": no, "type": ty, "key": e["key"], "draft": dtxt, "repo": rtxt, "draft_proof": dproof,
                      "repo_has_proof": bool(rproof)})
    md = ["# Task 17 A2: statements side by side (draft vs repository source)", "",
          "Extracted mechanically (PREREG_t17.md, E2). Repository text: `source/Stages_0_4_Source.md` rendered with thesis numbering "
          "and no thesis overrides; 6.5 from `source/thesis_only/tau-optimal-normal-form.md`; 6.13 from the manuscript. "
          "Classification: `a2_classification.yaml`.", ""]
    for p in pairs:
        md += [f"## {p['type']} {p['no']} (`{p['key']}`)", "", "**Draft:**", "", p["draft"] or "(not found)", "",
               "**Repository:**", "", p["repo"] or "(not found)", "",
               f"*Proof in the draft:* {'yes' if p['draft_proof'] else 'no'}; *in the repository source:* "
               f"{'yes' if p['repo_has_proof'] else 'no'}", "", "---", ""]
    open(os.path.join(RES, "a2_pairs.md"), "w").write("\n".join(md))
    return {"results": len(pairs), "draft_found": sum(p["draft"] is not None for p in pairs),
            "repo_found": sum(p["repo"] is not None for p in pairs),
            "draft_proof_repo_none": [p["no"] for p in pairs if p["draft_proof"] and not p["repo_has_proof"]],
            "note": "verdict from a2_classification.yaml (manual reading after the run)"}


# ------------------------------------------------------------------------------------------------------------------ E3
S_, l_, c_ = mp.mpf("0.01"), mp.mpf(1), mp.mpf(1)
F_ = S_ / l_


def sig2(G_, P_, tau_=0):
    a = l_ + G_
    return (S_ + G_**2 / (2 * P_ * (1 + a * tau_))) / a


def Ptau(t_, P_=1):
    b = 4 * S_ * t_ + 2 * l_ / P_
    D = b**2 + 8 * S_ * (1 - l_ * t_)**2 / P_
    return 4 * S_ / (P_ * (b + mp.sqrt(D)))


def mp_post(L, dt, P_=1):
    a = mp.e ** (-l_ * dt)
    q, r = F_ * (1 - a**2), 1 / (P_ * dt)
    return ((1 - L)**2 * q + L**2 * r) / (1 - (1 - L)**2 * a**2)


def mp_avg(L, dt):
    s = 1 - mp.e ** (-2 * l_ * dt)
    return F_ - (F_ - mp_post(L, dt)) * s / (2 * l_ * dt)


def find(text, rx, grp=1):
    m = re.search(rx, text)
    return m.group(grp) if m else None


def E3():
    t0 = time.time()
    rows = []

    def add(no, what, printed, value, source):
        if value is None:
            ok, shown = False, "no source"
        elif isinstance(value, bool):
            ok, shown = value, value
        else:
            ok, shown = T16.printed_match(printed, value), mp.nstr(mp.mpf(value), 12)
        rows.append({"row": no, "what": what, "printed": printed, "value": shown, "source": source, "match": bool(ok)})
    # 1. section 6.1 relay example
    Gr = mp.mpf("0.5")
    a = l_ + Gr
    add(1, "V_w", "0.09", sig2(Gr, 1), "Prop. 6.2")
    add(1, "H_G", "0.0066667", S_ / a, "Prop. 6.2")
    add(1, "tau_F", "16", (Gr / (2 * F_) - 1) / a, "Prop. 6.3")
    for tv, pr in ((1, "0.04"), (10, "0.011875"), (16, "0.01")):
        add(1, f"sigma^2({tv})", pr, sig2(Gr, 1, tv), "Lemma 6.1")
    # 2. optimal and best constant gain
    add(2, "sigma*^2", "0.0099505", Ptau(mp.mpf("1e-60")), "Prop. 6.4 at tau -> 0")
    add(2, "P(1)", "0.0098039", Ptau(1), "Prop. 6.4")
    add(2, "P(10)", "0.0067813", Ptau(10), "Prop. 6.4")
    f = lambda g: sig2(g, 1, 1)
    gmin = mp.findroot(lambda g: mp.diff(f, g), mp.mpf("0.01"))
    V1 = min(f(gmin), mp.mpf(1) / 2)           # G -> infinity limit 1/(2 Pi tau)
    add(2, "V(1)", "0.0099010", V1, "min over G of Lemma 6.1 at tau = 1 (interior minimum vs the G -> infinity limit)")
    # 3. D1 example
    L1 = lambda dt: 1 - mp.e ** (-Gr * dt)
    post = lambda dt: mp_post(L1(dt), dt)
    add(3, "post at dt -> 0", "0.09", post(mp.mpf("1e-30")), "M-P formula")
    dtm = mp.findroot(lambda d: mp.diff(post, d), mp.mpf("2.4"))
    add(3, "post maximum", "0.20457", post(dtm), "M-P formula")
    add(3, "argmax", "2.4645", dtm, "M-P formula")
    add(3, "post at dt -> infinity is 0", "-> 0", post(mp.mpf(10)**6) < mp.mpf(10)**-5, "M-P formula")
    dtE = mp.findroot(lambda d: mp.tanh(Gr * d / 2) - F_ * d, 99)
    add(3, "dt_E = 100 to 20 digits", "100", abs(dtE - 100) < mp.mpf(10)**-18, f"tanh lemma root {mp.nstr(dtE, 25)}")
    avg = lambda dt: mp_avg(L1(dt), dt)
    add(3, "avg at dt = 200", "0.0099875", avg(200), "M-P formula")
    add(3, "dip at dt = 200", "0.125%", (F_ - avg(200)) / F_, "M-P formula")
    dmin = mp.findroot(lambda d: mp.diff(avg, d), 200)
    add(3, "avg minimiser (reported; the draft says 'at dt = 200')", "200", dmin, "M-P formula")
    # 4. D2 example c = 3
    LD2 = lambda dt: 3 * dt / (dt + 1)
    grid = [mp.mpf(10) ** (mp.mpf(-6) + 12 * mp.mpf(i) / 1999) for i in range(2000)]
    add(4, "D2 c = 3: P+ > F at every dt (2,000-point grid)", "P+ > F", all(mp_post(LD2(d), d) > F_ for d in grid), "M-P formula")
    add(4, "D2 c = 3: P+ -> 4F", "4", mp_post(LD2(mp.mpf(10)**8), mp.mpf(10)**8) / F_, "M-P formula at dt = 1e8")
    # 5. latency
    ss = Ptau(mp.mpf("1e-60"))
    Pd = lambda d: F_ - mp.e ** (-2 * l_ * d) * (F_ - ss)
    add(5, "P(0)", "0.0099505", Pd(0), "Prop. 7.11")
    add(5, "P(1/e)", "0.0099763", Pd(1 / mp.e), "Prop. 7.11")
    # 6. G = 0.019 example
    Gs = mp.mpf("0.019")
    av = lambda dt: mp_avg(1 - mp.e ** (-Gs * dt), dt)
    lg = [mp.mpf(10) ** (mp.mpf(-3) + 9 * mp.mpf(i) / 3000) for i in range(3001)]
    vals = [av(d) for d in lg]
    dif = [vals[i + 1] - vals[i] for i in range(3000)]
    sg = [1 if d > 0 else -1 for d in dif]
    seq = [s for i, s in enumerate(sg) if i == 0 or s != sg[i - 1]]
    imin = next(i for i in range(1, 3000) if sg[i - 1] < 0 and sg[i] > 0) if -1 in sg else None
    add(6, "G = 0.019 avg: maximum then minimum", "max, min", seq[:3] == [1, -1, 1], f"sign sequence {seq}")
    add(6, "minimum below the starting value", "below start", imin is not None and vals[imin] < sig2(Gs, 1), "M-P formula")
    # 7. census counts (Task 12)
    r12 = T("t12", "RESULTS_t12.md")
    add(7, "178 of 1,000 (2 < rho <= 2 + u, no onset)", "178", mp.mpf(find(r12, r"(\d+) have 2 < ρ ≤ 2 \+ u") or "nan"),
        "t12/RESULTS_t12.md")
    a8 = J("t12", "results", "t12_a8.json")
    add(7, "sets per family", "2000", mp.mpf(a8["N"]), "t12_a8.json N")
    add(7, "6,000 sets", "6000", mp.mpf(len(a8["sets"])), "t12_a8.json sets")
    add(7, "x 3 metrics", "3", mp.mpf(len(re.findall(r"D1 (post|prior|avg) 0", r12))), "t12/RESULTS_t12.md A8 row (metrics listed)")
    sh = find(r12, r"shapes \{'Empty': (\d+), 'lower ray': (\d+)\}", 0)
    nums = [int(x) for x in re.findall(r"\d+", sh)] if sh else []
    add(7, "D3 excess set at R2 = F: lower ray or Empty", "1000", mp.mpf(sum(nums)) if nums else None, "t12 A4 shapes")
    # 8. section 2.5 verification (Task 10)
    r10 = T("t10", "RESULTS_t10.md")
    add(8, "1,000 tolerances (degenerate point)", "1000", mp.mpf(find(r10, r"(\d+) tolerances, route disagreements 0") or "nan"),
        "t10/RESULTS_t10.md")
    add(8, "exponent (values)", "1.50007", mp.mpf(find(r10, r"slopes ([\d.]+) and") or "nan"), "t10/RESULTS_t10.md")
    add(8, "exponent (positions)", "0.50002", mp.mpf(find(r10, r"slopes [\d.]+ and ([\d.]+)") or "nan"), "t10/RESULTS_t10.md")
    # 9. chapter 6 verification, sections 6.1-6.2
    r9 = T("t9", "RESULTS_t9.md")
    add(9, "T9.4 classifications", "80000", mp.mpf(find(r9, r"T9\.4[^|]*\| \*\*PASS\*\* \| ([\d,]+)").replace(",", "")), "t9 RESULTS")
    e17 = [mp.mpf(x) for x in re.findall(r"rel\. err ([\d.]+e-17), ([\d.]+e-17), ([\d.]+e-17)", r9)[0]]
    add(9, "T9.2 Wiener route agreement", "2 × 10^-17", max(e17), "t9 RESULTS T9.2 (max of the three)")
    add(9, "T9.5 flags: not strictly decreasing", "285", mp.mpf(find(r9, r"V not strictly decreasing (\d+)") or "nan"), "t9 RESULTS")
    add(9, "T9.5 flags: V < P", "13", mp.mpf(find(r9, r"V < P (\d+) \|") or "nan"), "t9 RESULTS")
    r13 = T("t13", "RESULTS_t13.md")
    add(9, "T13 A7 sets", "10000", mp.mpf(find(r13, r"A7 numerical \(([\d,]+) sets").replace(",", "")), "t13 RESULTS")
    add(9, "T13 A7 digits", "60", mp.mpf(find(r13, r"A7 numerical \([\d,]+ sets, (\d+) digits")), "t13 RESULTS")
    add(9, "T10.6 three routes", "1.0 × 10^-14", mp.mpf(find(r10, r"max pairwise relative difference ([\d.e-]+)") or "nan"),
        "t10 RESULTS")
    add(9, "T10.6 shape exact to 1e-50", "<= 10^-50", J("t10", "results", "t10_6.json")["shape"]["max_pos_rel_err"] <= 1e-50,
        "t10_6.json shape.max_pos_rel_err")
    # 10. section 6.5 verification (Task 12, 13)
    for chk, what in (("A2", "D1"), ("A3", "D2")):
        mm = re.search(chk + r" " + what + r" excess set at R² = F \(1,000 sets\) \| \*\*PASS\*\* \| (\d+)/(\d+) match", r12)
        add(10, f"{chk} {what} sets matching", "1000", mp.mpf(mm.group(1)) if mm else None, "t12 RESULTS")
    add(10, "A2 dt_E to 1e-30", "1 × 10^-30", mp.mpf(find(r12, r"A2 D1[^\n]*max rel\. error of Δt_E ([\d.e-]+)") or "nan"), "t12")
    add(10, "A4 sets agreeing", "1000", mp.mpf(find(r12, r"A4 D3[^\n]*\| (\d+)/\d+ agree") or "nan"), "t12 RESULTS")
    add(10, "A4 membership tests", "201514", mp.mpf(find(r12, r"of (\d+) test points") or "nan"), "t12 RESULTS")
    add(10, "T13 A1 sets", "10000", mp.mpf(find(r13, r"A1 numerical \(([\d,]+) sets").replace(",", "")), "t13 RESULTS")
    add(10, "T13 A1 digits", "100", mp.mpf(find(r13, r"A1 numerical \([\d,]+ sets, (\d+) digits")), "t13 RESULTS")
    add(10, "T12 A6 points", "400000", mp.mpf(find(r12, r"A6 numerical monotonicity \(record\) \| record \| ([\d,]+)").replace(",", "")),
        "t12 RESULTS")
    # 11. section 6.6 verification
    add(11, "B4 census sets", "2000", mp.mpf(find(r12, r"B4 census \(([\d,]+)").replace(",", "")), "t12 RESULTS")
    add(11, "maximum's position error", "6 × 10^-31", mp.mpf(find(r12, r"max error of the maximum's position ([\d.e-]+)") or "nan"),
        "t12 RESULTS")
    # 12. chapter 7 verification
    r11 = T("t11", "RESULTS_t11.md")
    add(12, "T11.3 spectral pairs", "25000", mp.mpf(find(r11, r"failures 0 of (\d+) pairs") or "nan"), "t11 RESULTS")
    t113 = J("t11", "results", "t11_3.json")
    add(12, "T11.3 values of beta", "37", mp.mpf(len({x["beta"] for x in t113["by_beta"]})), "t11_3.json by_beta (distinct beta)")
    add(12, "T13 A4 curves", "10000", mp.mpf(find(r13, r"A4 numerical \(([\d,]+) curves").replace(",", "")), "t13 RESULTS")
    add(12, "T11 unimodality curves", "12900", mp.mpf(find(r11, r"\*\*\{'1': (\d+)\}\*\*") or "nan"), "t11 RESULTS")
    add(12, "T11.3 duality", "8 × 10^-51", mp.mpf(find(r11, r"duality \| \*\*PASS\*\* \| max relative difference ([\d.e-]+)") or "nan"),
        "t11 RESULTS")
    add(12, "T11.4 Monte Carlo |z|", "1.91", mp.mpf(find(r11, r"MC \|z\| ≤ ([\d.]+)") or "nan"), "t11 RESULTS")
    add(12, "T11.5 sets", "1000", mp.mpf(find(r11, r"P decreasing (\d+)/\d+") or "nan"), "t11 RESULTS")
    add(12, "T11.6 pairs", "9000", mp.mpf((find(r11, r"over ([\d,]+)") or "nan").replace(",", "")), "t11 RESULTS")
    add(12, "T13 A3 closed form and limits 11 of 11", "11", mp.mpf(find(r13, r"(\d+)/11\)") or "nan"), "t13 RESULTS")
    add(12, "T13 A3 sets", "10000", mp.mpf(find(r13, r"A3 numerical \(([\d,]+) sets").replace(",", "")), "t13 RESULTS")
    add(12, "T11.6 continuum points", "400000", mp.mpf(J("t11", "results", "t11_6.json")["continuum"]["n_points"]), "t11_6.json")
    add(12, "T12 A9 points", "400000", mp.mpf(find(r12, r"A9 numerical monotonicity \(record\) \| record \| ([\d,]+)").replace(",", "")),
        "t12 RESULTS")
    add(12, "T12 A10 pairs", "1000", mp.mpf(find(r12, r"post\(2Δt\) < post\(Δt\) in (\d+)/") or "nan"), "t12 RESULTS")
    # 13. audit rows
    rows13 = {r_["row"]: r_["name"] for r_ in J("t13", "results", "t13_audit_classes.json")["rows"]}
    expect = {13: "tau ZF relay", 14: "tau ZF optimal", 15: "tau var relay", 16: "tau var optimal", 17: "power", 18: "power",
              19: "power", 20: "delay", **{k: "dt" for k in range(24, 33)}, **{k: "Sigma" for k in range(35, 43)}}
    for k, v in expect.items():
        add(13, f"audit row {k} is '{v}…'", v, rows13.get(k, "").startswith(v), f"row name '{rows13.get(k)}'")
    return {"rows": rows, "n": len(rows), "n_match": sum(r_["match"] for r_ in rows),
            "mismatches": [r_ for r_ in rows if not r_["match"]], "pass": all(r_["match"] for r_ in rows),
            "seconds": round(time.time() - t0, 2)}


# ------------------------------------------------------------------------------------------------------------------ E4
def E4():
    t0 = time.time()
    text = "\n".join(draft_upto("## 8.")).replace("\\[", "[").replace("\\]", "]").replace("\\_", "_")
    refs = {r["number"] for r in yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))}
    reg = {e["thesis_no"]: e["type"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))}
    figs = {e["label"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))}
    cites, excluded, unresolved, first = [], [], [], {}
    for m in re.finditer(r"\[([^\[\]\n]{1,40})\]", text):
        body = m.group(1)
        pre = text[max(0, m.start() - 4):m.start()]
        if re.fullmatch(r"\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*", body) and not re.search(r"\bin\s*$", pre):
            nums = []
            for part in body.split(", "):
                a, _, b = part.partition("–")
                nums += list(range(int(a), int(b or a) + 1))
            if all(1 <= n <= 53 for n in nums):
                cites.append(body)
                for n in nums:
                    if n not in refs:
                        unresolved.append(n)
                    first.setdefault(n, m.start())
                continue
        if re.search(r"\d", body):
            excluded.append({"text": "[" + body + "]", "context": text[max(0, m.start() - 30):m.end() + 5].replace("\n", " ")})
    order = sorted(first, key=lambda n: first[n])
    order_ok = order == sorted(order) and set(order) == set(range(1, 54))
    typed_bad, typed_n = [], 0
    tw = r"(Theorems?|Thm|Propositions?|Props?\.|Lemmas?|Corollar(?:y|ies)|Cor\.|Definitions?|Numerical results?|Num\. results?|" \
         r"Conjectures?|Counterexamples?)"
    spec = r"(\d+\.\d+(?:\([^)]*\))?(?:[–-]\d+\.\d+)?(?:(?:,\s*|\s+and\s+)\d+\.\d+(?:\([^)]*\))?(?:[–-]\d+\.\d+)?)*)"
    for m in re.finditer(r"\b" + tw + r"\s+" + spec, text):
        ty = T16.TYPE_ALIASES.get(m.group(1).lower()) or T16.TYPE_ALIASES.get(re.sub(r"s$", "", m.group(1).lower()))
        for no in T16.expand(m.group(2)):
            typed_n += 1
            if no not in reg:
                typed_bad.append({"ref": m.group(0), "number": no, "problem": "no such result"})
            elif reg[no] != ty:
                typed_bad.append({"ref": m.group(0), "number": no, "problem": f"type is {reg[no]}, not {ty}"})
    TL = text.split("\n")
    hdr, untyped_bad, untyped_n = None, [], 0
    for i, line in enumerate(TL):
        if line.startswith("|") and i + 1 < len(TL) and re.match(r"^\|[\s|:-]+$", TL[i + 1]) and "-" in TL[i + 1]:
            hdr = [c.strip() for c in line.strip().strip("|").split("|")]
            continue
        if not line.startswith("|"):
            hdr = None
            continue
        if hdr and hdr[-1] in ("Label", "Labels", "Result") and not set(line) <= set("|-: "):
            last = [c.strip() for c in line.strip().strip("|").split("|")][-1]
            if re.fullmatch(r"[\d., –-]+", last) and re.search(r"\d+\.\d+", last):
                for no in T16.expand(last):
                    untyped_n += 1
                    if no not in reg:
                        untyped_bad.append({"ref": last, "number": no})
    for m in re.finditer(r"\bresults (\d+\.\d+[–-]\d+\.\d+)", text):
        for no in T16.expand(m.group(1)):
            untyped_n += 1
            if no not in reg:
                untyped_bad.append({"ref": m.group(0), "number": no})
    figrefs = re.findall(r"Figure (B\.\d+)", text)
    figbad = sorted({f for f in figrefs if f not in figs})
    out = {"citation_groups": len(cites), "unresolved": unresolved, "first_order_1_53": order_ok, "first_order": order,
           "excluded_brackets": excluded, "typed_refs": typed_n, "typed_bad": typed_bad, "untyped_refs": untyped_n,
           "untyped_bad": untyped_bad, "figure_refs": len(figrefs), "figure_bad": figbad}
    out["pass"] = not unresolved and order_ok and not typed_bad and not untyped_bad and not figbad
    out["seconds"] = round(time.time() - t0, 2)
    return out


# ------------------------------------------------------------------------------------------------------------------ E6
ESC = re.compile(r"\\\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\\\]")


def E6():
    refs = {r["number"] for r in yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))}
    files = [p for p in T16.thesis_renders() if not p.endswith("Appendix_C_References.md")]
    base, now, esc_now = {}, {}, {}
    for p in files:
        r = os.path.relpath(p, REPO)
        old = subprocess.run(["git", "show", f"{T16_HEAD}:{r}"], cwd=REPO, capture_output=True, text=True).stdout
        old = T16.prep(p, old)
        base[r] = sum(T16.is_cite(b, refs) for b in T16.groups(old)) + sum(T16.is_cite(b, refs) for b in ESC.findall(old))
        t = T16.prep(p, open(p).read())
        now[r] = sum(T16.is_cite(b, refs) for b in T16.groups(t))
        esc_now[r] = len(ESC.findall(t))
    new_files = ["stationary-variance.md", "optimal-envelope.md", "plateaus.md", "equal-height-maxima.md", "degenerate-points.md",
                 "pair-birth.md", "discrete-excess.md"]
    added = {f: sum(T16.is_cite(b, refs) for b in T16.groups(T("source", "thesis_only", f))) for f in new_files}
    tot_b, tot_n = sum(base.values()), sum(now.values())
    return {"escaped_now": {k: v for k, v in esc_now.items() if v}, "baseline_total": tot_b, "now_total": tot_n,
            "added_by_imports": added, "expected_total": tot_b + sum(added.values()),
            "per_file": {k: (base[k], now[k]) for k in now if base[k] != now[k]},
            "pass": sum(esc_now.values()) == 0 and tot_n == tot_b + sum(added.values())}


# ------------------------------------------------------------------------------------------------------------------ E7
def E7():
    figs = {e["label"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))}
    flagged, exempt, paper1 = [], {"prefixed": 0, "figure label": 0}, 0
    for p in T16.thesis_renders():
        raw = open(p).read()
        code = []
        if p.endswith("Appendix_E_Reproduction.md"):
            for m in re.finditer(r"```.*?```", raw, re.S):
                code.append((m.start(), m.end()))
        # keep a map from normalised positions back to raw positions for the code-block test
        idx, norm = [], []
        prev_ws = False
        for i, ch in enumerate(raw):
            if ch.isspace():
                if not prev_ws:
                    norm.append(" ")
                    idx.append(i)
                prev_ws = True
            else:
                norm.append(ch)
                idx.append(i)
                prev_ws = False
        t = "".join(norm)
        paper1 += t.count("Paper 1")
        figfile = p.endswith("Appendix_B_Figures.md") or "/figs_thesis/" in p
        for m in re.finditer(r"\b[A-E]\.\d+\b", t):
            lab = m.group(0)
            before = t[max(0, m.start() - 200):m.start()]
            if before.endswith("legacy "):
                exempt["prefixed"] += 1
                continue
            in_code = any(a <= idx[m.start()] < b for a, b in code)
            if lab in figs and (figfile or re.search(r"[Ff]igures?\b", before) or t[m.end():m.end() + 1] == "_" or in_code):
                exempt["figure label"] += 1
                continue
            flagged.append({"file": os.path.relpath(p, REPO), "label": lab, "context": t[max(0, m.start() - 50):m.end() + 10]})
    return {"flagged": flagged, "exempt": exempt, "paper1": paper1, "files": len(T16.thesis_renders()), "pass": not flagged}


CHECKS = {"E1": E1, "E2": E2, "E3": E3, "E4": E4, "E6": E6, "E7": E7}


def main():
    os.makedirs(RES, exist_ok=True)
    which = [a for a in sys.argv[1:] if a in CHECKS] or list(CHECKS)
    path = os.path.join(RES, "t17_checks.json")
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
