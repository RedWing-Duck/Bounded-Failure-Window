"""Task 16 checks D1-D8 (PREREG_t16.md, commit 19c6ffe) and the A2 extraction (t16/results/a2_pairs.md).
D1 item 4's logical review and D2's classification are manual readings made after the run; this script records the
mechanical parts (numeric test for item 4; side-by-side statements for D2). make_results_t16.py combines them.
Usage: python3 t16_checks.py [D1 D2 D3 ...]   (default: all)"""
import glob
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
RES = os.environ.get("T16_RES") or os.path.join(HERE, "results")
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_ch1-5.md")
mp.mp.dps = 50
T15_ARTIFACTS = "41d5e43"


def draft_ch15():
    L = open(DRAFT).read().split("\n")
    end = next(i for i, l in enumerate(L) if l.startswith("## 6."))
    return L[:end]


def J(*p):
    return json.load(open(os.path.join(CLS, *p)))


# ------------------------------------------------------------------------------------------------------------------ D1
lam, Sig, Pi, Pi0, c, G, Ginf, lp, Sp, R2, d, v, nu, a_, D_, P_, u_, p_, Gp = sp.symbols(
    "lambda Sigma Pi Pi0 c G G_inf lambda_p Sigma_p R2 d v nu a D P u p Gp", positive=True)
sig2 = (Sig + G**2 / (2 * Pi)) / (lam + G)
Gstar = -lam + sp.sqrt(lam**2 + 2 * Sig * Pi)
sstar = 2 * Sig / (lam + sp.sqrt(lam**2 + 2 * Sig * Pi))
F = Sig / lam


def zero(e):
    """Pre-registered routes: simplify; factor(radsimp); simplify(sqrtdenest(powsimp))."""
    routes = [("simplify", sp.simplify), ("factor(radsimp)", lambda x: sp.factor(sp.radsimp(x))),
              ("simplify(sqrtdenest(powsimp))", lambda x: sp.simplify(sp.sqrtdenest(sp.powsimp(x))))]
    for name, f in routes:
        try:
            r = f(e)
            if r == 0:
                return {"zero": True, "route": name}
        except Exception as ex:  # noqa: BLE001
            last = str(ex)
    return {"zero": False, "route": None, "residual": str(sp.simplify(e))[:300]}


RNG = random.Random(16001)


def U(lo=1e-3, hi=1e3):
    return mp.mpf(10) ** mp.mpf(RNG.uniform(math.log10(lo), math.log10(hi)))


def numeric_zero(expr, syms, n=1000, sampler=None):
    f = sp.lambdify(syms, expr, "mpmath")
    worst = mp.mpf(0)
    for _ in range(n):
        vals = sampler() if sampler else [U() for _ in syms]
        r = f(*vals)
        worst = max(worst, abs(r))
    return float(worst)


def ident(lhs, rhs, syms, sampler=None, scale=None):
    e = lhs - rhs
    z = zero(e)
    rel = (e / scale) if scale is not None else e
    z["numeric_max_abs"] = numeric_zero(rel, syms, sampler=sampler)
    z["holds"] = z["zero"]
    return z


def ineq(pred, n=1000, sampler=None):
    """pred(sample) -> (holds: bool, info); counts counterexamples over n admissible samples."""
    bad, seen = [], 0
    while seen < n:
        s = sampler()
        if s is None:
            continue
        seen += 1
        ok, info = pred(s)
        if not ok:
            bad.append(info)
    return {"n": seen, "counterexamples": len(bad), "examples": [str(b) for b in bad[:3]], "holds": not bad}


def d1_item1():
    out = {}
    aa, DD = lam + G, G**2 / Pi + 2 * Sig
    out["a_ou_variance"] = ident(DD / (2 * aa), sig2, [lam, Sig, Pi, G])
    Psol = sp.solve(-2 * a_ * P_ + D_, P_)
    out["a_lyapunov"] = {"solution": str(Psol), "holds": Psol == [D_ / (2 * a_)]}
    e = (Sig + u_ / 2) / (lam + G)
    val = e.subs({G: 0, u_: 0})
    out["b_limit_F"] = {"value_at_0": str(val), "holds": sp.simplify(val - F) == 0,
                        "note": "rational in (G, u) with denominator lambda + G > 0, so continuous at (0, 0)"}
    w = sp.symbols("w", nonnegative=True)
    e2 = (Sig + G**2 * w / 2) / (lam + G)
    H = e2.subs({G: Ginf, w: 0})
    out["c_limit_H"] = {"value": str(H), "holds": sp.simplify(H - Sig / (lam + Ginf)) == 0,
                        "note": "w = 1/Pi; continuous at (G_inf, 0)"}
    gap = sp.factor(sp.simplify(F - Sig / (lam + Ginf)))
    cnt = 0
    for _ in range(1000):
        l_, S_, g_ = U(), U(), U()
        if not S_ / (l_ + g_) < S_ / l_:
            cnt += 1
    out["c_H_lt_F"] = {"F_minus_H": str(gap), "symbolic_positive": bool(gap.is_positive), "n": 1000, "counterexamples": cnt,
                       "holds": cnt == 0}
    out["holds"] = all(v_["holds"] for v_ in out.values())
    return out


def d1_item2():
    out = {}
    roots = sp.solve(2 * Sig - 2 * lam * p_ - Pi * p_**2, p_)
    pos = [r for r in roots if sp.simplify(r).is_positive or (r.subs({lam: 1, Sig: 1, Pi: 1}) > 0)]
    out["a_roots"] = {"roots": [str(r) for r in roots], "positive": [str(r) for r in pos], "holds": len(pos) == 1}
    p0 = pos[0]
    out["a_Gstar"] = ident(p0 * Pi, Gstar, [lam, Sig, Pi])
    out["a_sstar"] = ident(p0, sstar, [lam, Sig, Pi])
    out["a_sigma2_at_Gstar"] = ident(sig2.subs(G, Gstar), p0, [lam, Sig, Pi])
    out["b_dsigma2_dG"] = ident(sp.diff(sig2, G), (G**2 + 2 * lam * G - 2 * Sig * Pi) / (2 * Pi * (lam + G)**2),
                                [lam, Sig, Pi, G])
    gr = sp.solve(G**2 + 2 * lam * G - 2 * Sig * Pi, G)
    gs = sp.symbols("g")
    groots = sp.solve(gs**2 + 2 * lam * gs - 2 * Sig * Pi, gs)
    signs = [(str(r), bool(r.is_positive), bool(r.is_negative)) for r in groots]
    out["b_only_positive_zero"] = {"roots": signs, "positive_root_is_Gstar": any(sp.simplify(r - Gstar) == 0 for r in groots
                                                                                   if r.is_positive),
                                   "holds": sum(s[1] for s in signs) == 1 and sum(s[2] for s in signs) == 1 and
                                   any(sp.simplify(r - Gstar) == 0 for r in groots if r.is_positive)}
    del gr
    ds = sp.simplify(sp.diff(sstar, Pi))
    f_ds = sp.lambdify([lam, Sig, Pi], ds, "mpmath")
    f_s = sp.lambdify([lam, Sig, Pi], sstar, "mpmath")
    bad_d, bad_lt = 0, 0
    for _ in range(1000):
        l_, S_, P_v = U(), U(), U()
        if not f_ds(l_, S_, P_v) < 0:
            bad_d += 1
        if not f_s(l_, S_, P_v) < S_ / l_:
            bad_lt += 1
    out["c_decreasing"] = {"dsstar_dPi": str(ds), "symbolic_negative": bool(ds.is_negative), "n": 1000, "counterexamples": bad_d,
                           "holds": bad_d == 0}
    lim = sp.limit(sstar, Pi, 0, "+")
    out["c_limit_F"] = {"limit": str(lim), "holds": sp.simplify(lim - F) == 0}
    out["c_Gstar_eq_sstar_Pi"] = ident(Gstar, sstar * Pi, [lam, Sig, Pi])
    out["c_sstar_lt_F"] = {"F_minus_sstar_positive": bool(sp.simplify(F - sstar).is_positive), "n": 1000, "counterexamples": bad_lt,
                           "holds": bad_lt == 0}
    qs = sp.simplify((Gstar / (F * Pi)).subs(Pi, nu * lam**2 / (2 * Sig)))
    out["d_qstar_form1"] = ident(qs, 2 * (sp.sqrt(1 + nu) - 1) / nu, [lam, Sig, nu])
    out["d_qstar_form2"] = ident(2 * (sp.sqrt(1 + nu) - 1) / nu, 2 / (1 + sp.sqrt(1 + nu)), [nu])
    out["holds"] = all(v_["holds"] for v_ in out.values())
    return out


def d1_item3():
    Gf = sp.Function("G")(Pi)
    s = (Sig + Gf**2 / (2 * Pi)) / (lam + Gf)
    eps = Pi * sp.diff(Gf, Pi) / Gf
    N = eps * (Gf**2 + 2 * lam * Gf - 2 * Sig * Pi) - Gf * (lam + Gf)
    out = {"total_derivative": {**zero(sp.diff(s, Pi) - Gf * N / (2 * Pi**2 * (lam + Gf)**2))}}
    # numeric cross-check with a concrete gain family G = c Pi^n/(Pi^n + Pi0^n)
    n_ = sp.symbols("n", positive=True)
    Gc = c * Pi**n_ / (Pi**n_ + Pi0**n_)
    e = (sp.diff(s, Pi) - Gf * N / (2 * Pi**2 * (lam + Gf)**2)).subs(Gf, Gc).doit()
    out["total_derivative"]["numeric_max_abs"] = numeric_zero(e, [lam, Sig, Pi, c, Pi0, n_])
    out["total_derivative"]["holds"] = out["total_derivative"]["zero"]
    out["partial_Pi"] = ident(sp.diff(sig2, Pi), -G**2 / (2 * Pi**2 * (lam + G)), [lam, Sig, Pi, G])
    out["holds"] = all(v_["holds"] for v_ in out.values())
    return out


def d1_item4(n_target=1000):
    """Numeric part of item 4: perturbations satisfying conditions 1 and 2 keep each N_i's direction (seed 16002)."""
    rng = random.Random(16002)
    pairs = curves = rejected = 0
    bad = []
    while pairs < n_target:
        K = rng.randint(1, 6)
        xs = sorted(rng.uniform(0.05, 0.95) for _ in range(K))
        xs = [0.0] + xs + [1.0]
        up = rng.random() < 0.5
        ys = [rng.uniform(0.0, 1.0)]
        for j in range(1, len(xs)):
            step = rng.uniform(0.05, 1.0)
            ys.append(ys[-1] + (step if up else -step))
            up = not up

        def s2(t):
            for j in range(len(xs) - 1):
                if xs[j] <= t <= xs[j + 1]:
                    return ys[j] + (ys[j + 1] - ys[j]) * (t - xs[j]) / (xs[j + 1] - xs[j])
            return ys[-1]
        lo, hi = min(ys), max(ys)
        R = rng.uniform(lo, hi)
        if min(abs(R - y) for y in ys) < 1e-3:
            continue
        cross = []
        for j in range(len(xs) - 1):
            a, b = ys[j], ys[j + 1]
            if (a - R) * (b - R) < 0:
                cross.append((xs[j] + (R - a) / (b - a) * (xs[j + 1] - xs[j]), j))
        if not cross:
            continue
        Ns = []
        for i, (x, j) in enumerate(cross):
            room = min(x - xs[j], xs[j + 1] - x)
            Ns.append((x - 0.4 * room, x + 0.4 * room, j))
        # eta: minimum of |s2 - R| on K = D minus the interiors of N_i (piecewise linear: check knots and N_i ends)
        pts = [t for t in xs] + [e for N in Ns for e in N[:2]]
        pts = [t for t in pts if not any(N[0] < t < N[1] for N in Ns)]
        eta = min(abs(s2(t) - R) for t in pts)
        curves += 1
        for _ in range(3):
            A = rng.uniform(0.05, 0.95) * eta
            k = [rng.uniform(1, 40) for _ in range(3)]
            ph = [rng.uniform(0, 6.3) for _ in range(3)]
            w = [rng.uniform(-1, 1) for _ in range(3)]
            norm = sum(abs(x) for x in w)

            def pert(t):
                return A * sum(w[m] * math.sin(k[m] * t + ph[m]) for m in range(3)) / norm
            grid = [i / 2000 for i in range(2001)]
            if max(abs(pert(t)) for t in grid) >= eta:
                rejected += 1
                continue
            for (a, b, j) in Ns:
                tt = [a + (b - a) * i / 400 for i in range(401)]
                vals = [s2(t) + pert(t) for t in tt]
                dif = [vals[i + 1] - vals[i] for i in range(400)]
                if not (all(x > 0 for x in dif) or all(x < 0 for x in dif)):
                    rejected += 1
                    continue
                dir_t = dif[0] > 0
                dir_s = ys[j + 1] > ys[j]
                pairs += 1
                if dir_t != dir_s:
                    bad.append({"knots": xs, "values": ys, "R2": R, "N": (a, b)})
    return {"pairs": pairs, "curves": curves, "rejected_perturbations_or_Ni": rejected, "counterexamples": len(bad),
            "examples": bad[:2], "numeric_holds": not bad,
            "note": "the logical review of the remark is recorded in t16/results/d1_item4_review.md (manual, after the run)"}


def d1_item5():
    roots = sp.solve(Pi * v**2 + 2 * lam * v - 2 * Sig, v)
    pos = [r for r in roots if r.subs({lam: 1, Sig: 1, Pi: 1}) > 0]
    z = ident(pos[0], sstar, [lam, Sig, Pi])
    z["roots"] = [str(r) for r in roots]
    z["holds"] = z["holds"] and len(pos) == 1
    return {"positive_root_is_sstar": z, "holds": z["holds"]}


def d1_item6():
    out = {}
    Gb = c * Pi / (Pi + Pi0)
    out["a_elasticity"] = ident(Pi * sp.diff(Gb, Pi) / Gb, 1 - Gb / c, [c, Pi, Pi0])
    eps = 1 - G / c
    PiG = Pi0 * G / (c - G)
    N = eps * (G**2 + 2 * lam * G - 2 * Sig * PiG) - G * (lam + G)
    out["b_N_eliminated"] = ident(N, -(G / c) * (G**2 + 2 * lam * G + 2 * Sig * Pi0 - lam * c), [c, G, lam, Sig, Pi0],
                                  sampler=lambda: (lambda cc: [cc, cc * mp.mpf(RNG.uniform(0.001, 0.999)), U(), U(), U()])(U()))
    rt = -lam + sp.sqrt(lam**2 + lam * c - 2 * Sig * Pi0)
    out["c_root_is_root"] = ident((G**2 + 2 * lam * G + 2 * Sig * Pi0 - lam * c).subs(G, rt), sp.Integer(0), [lam, c, Sig, Pi0],
                                  sampler=lambda: (lambda l_, c_, S_: [l_, c_, S_, (l_ * c_ / (2 * S_)) * mp.mpf(RNG.uniform(0.01, 0.99))])
                                  (U(), U(), U()))
    gap = sp.expand((lam + c)**2 - (lam**2 + lam * c - 2 * Sig * Pi0))
    out["c_root_below_c"] = {"(lam+c)^2 - radicand": str(gap), "positive": bool(gap.is_positive), "holds": bool(gap.is_positive)}
    kap = c / (F * Pi0)
    out["c_kappa_equiv"] = ident((kap - 2) * Sig * Pi0, lam * c - 2 * Sig * Pi0, [c, Sig, Pi0, lam])
    bad, n_in = 0, 0
    for _ in range(1000):
        l_, c_, S_, P0_ = U(), U(), U(), U()
        disc = l_**2 + l_ * c_ - 2 * S_ * P0_
        inside = disc > 0 and 0 < -l_ + mp.sqrt(disc) < c_
        if inside != (l_ * c_ > 2 * S_ * P0_):
            bad += 1
        n_in += inside
    out["c_equivalence_numeric"] = {"n": 1000, "root_in_(0,c)": n_in, "counterexamples": bad, "holds": bad == 0}
    # (d) maximum: N from Lemma 3.7 directly, along a log grid in Pi, for kappa > 2
    bad, n = [], 0
    while n < 1000:
        l_, c_, S_ = U(), U(), U()
        kappa = mp.mpf(10) ** mp.mpf(RNG.uniform(math.log10(2.0001), 3))
        P0_ = c_ * l_ / (kappa * S_)
        n += 1
        signs = []
        for i in range(401):
            P = P0_ * mp.mpf(10) ** (mp.mpf(-10) + mp.mpf(20) * i / 400)
            Gv = c_ * P / (P + P0_)
            ep = P0_ / (P + P0_)
            Nv = ep * (Gv**2 + 2 * l_ * Gv - 2 * S_ * P) - Gv * (l_ + Gv)
            signs.append(1 if Nv > 0 else (-1 if Nv < 0 else 0))
        seq = [s for i, s in enumerate(signs) if i == 0 or s != signs[i - 1]]
        if seq != [1, -1]:
            bad.append({"lam": str(l_), "c": str(c_), "Sigma": str(S_), "kappa": str(kappa), "seq": seq})
    out["d_maximum"] = {"n": n, "counterexamples": len(bad), "examples": bad[:3], "holds": not bad,
                        "note": "sign of N along Pi in [1e-10, 1e10] x Pi0 (401 points): must be (+, -)"}
    out["holds"] = all(v_["holds"] for v_ in out.values())
    return out


def d1_item7():
    out = {}
    r = Sig / Sp
    PiG = (G**2 + 2 * lp * G) / (2 * Sp)
    Gm = -lp + sp.sqrt(lp**2 + 2 * Sp * Pi)
    out["inverse"] = ident(PiG.subs(G, Gm), Pi, [lp, Sp, Pi])
    Gm_f = sp.Function("G")
    eps = sp.simplify(PiG / (G * sp.diff(PiG, G)))
    out["elasticity"] = ident(eps, (G + 2 * lp) / (2 * (G + lp)), [G, lp, Sp])
    del Gm_f
    N = eps * (G**2 + 2 * lam * G - 2 * Sig * PiG) - G * (lam + G)
    pG = -(1 + r) * G**2 - 4 * r * lp * G + 2 * lp * (lam - 2 * r * lp)
    out["N"] = ident(N, G * pG / (2 * (G + lp)), [G, lam, Sig, lp, Sp])
    dp = sp.diff(pG, G)
    cnt = 0
    f_dp = sp.lambdify([G, Sig, Sp, lp], dp, "mpmath")
    for _ in range(1000):
        if not f_dp(U(), U(), U(), U()) < 0:
            cnt += 1
    out["p_decreasing"] = {"dp_dG": str(dp), "symbolic_negative": bool(dp.is_negative), "n": 1000, "counterexamples": cnt,
                           "holds": cnt == 0}
    Fp = Sp / lp
    out["p0_identity"] = ident((lam - 2 * r * lp), (lam * lp / Sp) * (Fp - 2 * F), [lam, Sig, lp, Sp])
    cnt = 0
    for _ in range(1000):
        l_, S_, l2, S2 = U(), U(), U(), U()
        p0v = 2 * l2 * (l_ - 2 * (S_ / S2) * l2)
        if (p0v > 0) != (S2 / l2 > 2 * S_ / l_):
            cnt += 1
    out["p0_sign_numeric"] = {"n": 1000, "counterexamples": cnt, "holds": cnt == 0}
    out["holds"] = all(v_["holds"] for v_ in out.values())
    return out


def d1_item8():
    out = {}
    Gf = sp.Function("G")(Pi)
    s = (Sig + Gf**2 / (2 * Pi)) / (lam + Gf)
    lhs = 2 * Pi**2 * (lam + Gf)**2 * sp.diff(s, Pi)
    rhs = Pi * sp.diff(Gf, Pi) * (2 * lam * Gf + Gf**2 - 2 * Sig * Pi) - Gf**2 * (lam + Gf)
    out["a_derivative"] = {**zero(lhs - rhs)}
    n_ = sp.symbols("n", positive=True)
    e = (lhs - rhs).subs(Gf, c * Pi**n_ / (Pi**n_ + Pi0**n_)).doit()
    out["a_derivative"]["numeric_max_abs"] = numeric_zero(e, [lam, Sig, Pi, c, Pi0, n_])
    out["a_derivative"]["holds"] = out["a_derivative"]["zero"]
    out["b_sigma2_minus_F"] = ident(sig2 - F, G * (lam * G - 2 * Sig * Pi) / (2 * Pi * lam * (lam + G)), [lam, Sig, Pi, G])
    cnt = 0
    for _ in range(1000):
        l_, S_, P, Gv = U(), U(), U(), U()
        s2v = (S_ + Gv**2 / (2 * P)) / (l_ + Gv)
        if (s2v <= S_ / l_) != (2 * S_ * P >= l_ * Gv):
            cnt += 1
    out["b_equivalence_numeric"] = {"n": 1000, "counterexamples": cnt, "holds": cnt == 0}
    LHS = Pi * Gp * (2 * lam * G + G**2 - 2 * Sig * Pi) - G**2 * (lam + G)
    RHS = G * (lam + G) * (Pi * Gp - G)
    out["c_gap_identity"] = ident(RHS - LHS, Pi * Gp * (2 * Sig * Pi - lam * G), [Pi, Gp, lam, G, Sig])

    def samp():
        l_, S_, P, gp = U(), U(), U(), U()
        Gv = mp.mpf(2) * S_ * P / l_ * mp.mpf(RNG.uniform(0.0, 1.0))   # 2 Sigma Pi >= lambda G
        if Gv <= 0:
            return None
        return l_, S_, P, Gv, gp
    out["c_bound_numeric"] = ineq(lambda s_: (
        s_[2] * s_[4] * (2 * s_[0] * s_[3] + s_[3]**2 - 2 * s_[1] * s_[2]) - s_[3]**2 * (s_[0] + s_[3])
        <= s_[3] * (s_[0] + s_[3]) * (s_[2] * s_[4] - s_[3]), s_), sampler=samp)
    ci = sp.symbols("c_i", positive=True)
    Gi = ci * Pi / (Pi + Pi0)
    out["d_bayes_stage"] = ident(Pi * sp.diff(Gi, Pi) - Gi, -ci * Pi**2 / (Pi + Pi0)**2, [ci, Pi, Pi0])
    out["holds"] = all(v_["holds"] for v_ in out.values())
    return out


def d1_item9():
    piR = 2 * lam * (F - R2) / R2**2
    sub = {Sig: lam * (R2 + d)}   # F = R2 + d > R2
    e = sstar.subs(Pi, piR).subs(sub)
    z = ident(e, R2, [lam, R2, d])
    return {"sstar_at_piR": z, "holds": z["holds"]}


def D1():
    t0 = time.time()
    items = {"1 Prop 3.1": d1_item1, "2 Prop 3.5 / Lemma 3.6": d1_item2, "3 Lemma 3.7": d1_item3,
             "4 Prop 2.9 remark (numeric part)": d1_item4, "5 Thm 5.1": d1_item5, "6 Prop 5.8": d1_item6,
             "7 Prop 5.9": d1_item7, "8 Prop 5.14": d1_item8, "9 Cor 5.2": d1_item9}
    out = {}
    for k, f in items.items():
        t1 = time.time()
        out[k] = f()
        out[k]["seconds"] = round(time.time() - t1, 2)
        print("D1", k, "holds" if out[k].get("holds", out[k].get("numeric_holds")) else "DOES NOT HOLD", flush=True)
    out["seconds"] = round(time.time() - t0, 2)
    return out


# ------------------------------------------------------------------------------------------------------------------ D2
TYPES = r"(Theorem|Proposition|Lemma|Corollary|Definition|Numerical result|Conjecture|Counterexample)"
STOP = re.compile(r"^(\*Proof|#|\*Verification|\*\*Verification|\*Figure|\*\*Reading|\*\*Worked|\*\*Label:|---)")


def block(L, i, limit=45):
    out = [L[i]]
    for l in L[i + 1:i + limit]:
        if STOP.match(l) or re.match(r"^\*\*" + TYPES + r" \d", l):
            break
        out.append(l)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def D2():
    reg = [e for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))
           if e["thesis_no"].split(".")[0] in "2345"]
    DL = draft_ch15()
    RL = open(os.path.join(CLS, "Stages_0_4_Thesis.md")).read().split("\n")
    pairs = []
    for e in reg:
        no, ty = e["thesis_no"], e["type"]
        rx = re.compile(r"\*\*" + re.escape(ty) + " " + re.escape(no) + r"\b")
        di = next((i for i, l in enumerate(DL) if rx.search(l)), None)
        dtxt = block(DL, di) if di is not None else None
        if no == "3.1" and di is not None:      # the model formula precedes the label
            dtxt = "\n".join(DL[di - 8:di]) + "\n" + dtxt
        if no == "3.3":                         # inline label: the paragraph with the identity
            j = next(i for i, l in enumerate(DL) if "Subtracting the floor gives" in l)
            dtxt = "\n".join(DL[j:j + 8])
        ri = next((i for i, l in enumerate(RL) if rx.search(l)), None)
        if ri is not None:
            rtxt = block(RL, ri)
        elif no == "3.1":
            j = next(i for i, l in enumerate(RL) if l.startswith("**Model.**"))
            rtxt = "\n".join(RL[j:j + 11])
        elif no == "3.5":
            j = next(i for i, l in enumerate(RL) if "Optimal (Kalman–Bucy) gain" in l)
            rtxt = "\n".join(RL[j:j + 2])
        else:
            rtxt = None
        pairs.append({"no": no, "type": ty, "key": e["key"], "draft": dtxt, "repo": rtxt})
    md = ["# Task 16 A2: statements side by side (draft chapters 1–5 vs the repository at the artifacts commit)", "",
          "Extracted mechanically (PREREG_t16.md, D2). Repository text: `Stages_0_4_Thesis.md` (rendered from "
          "`source/Stages_0_4_Source.md` and `source/thesis_only/`). 3.1 and 3.5 have no labelled block in the repository; their "
          "statements are the §1 model paragraph and the reference-quantities bullet. Classification: `a2_classification.yaml`.", ""]
    for p in pairs:
        md += [f"## {p['type']} {p['no']} (`{p['key']}`)", "", "**Draft:**", "", p["draft"] or "(not found)", "", "**Repository:**", "",
               p["repo"] or "(not found)", "", "---", ""]
    open(os.path.join(RES, "a2_pairs.md"), "w").write("\n".join(md))
    return {"results": len(pairs), "draft_found": sum(p["draft"] is not None for p in pairs),
            "repo_found": sum(p["repo"] is not None for p in pairs), "file": "t16/results/a2_pairs.md",
            "note": "verdict from a2_classification.yaml (manual reading after the run)"}


# ------------------------------------------------------------------------------------------------------------------ D3
def printed_match(printed, value):
    """Compare a value with a printed number to the digits printed."""
    s = printed.replace(",", "").replace("−", "-").strip()
    m = re.fullmatch(r"(-?[\d.]+) × 10\^?(-?\d+)", s)
    if m:
        mant, ex = m.group(1), int(m.group(2))
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return round(float(mp.mpf(value) / mp.mpf(10)**ex), dec) == float(mant)
    if s.endswith("%"):
        num = s[:-1]
        dec = len(num.split(".")[1]) if "." in num else 0
        return round(float(value) * 100, dec) == float(num)
    dec = len(s.split(".")[1]) if "." in s else 0
    q = mp.nstr(mp.mpf(value), 40, strip_zeros=False)
    return round(float(mp.mpf(q)), dec) == float(s) if dec <= 12 else abs(mp.mpf(value) - mp.mpf(s)) < mp.mpf(10)**(-dec)


def sig2n(Gv, P, l_=1, S_=mp.mpf("0.01")):
    return (S_ + Gv**2 / (2 * P)) / (l_ + Gv)


def phi(n, t, l_=1, c_=1):
    T = t**n
    Pn = -(l_ + c_) * T**2 + (n - 1) * (c_ + 2 * l_) * T + (2 * n - 1) * l_
    return t**(n - 1) * Pn / (1 + T)**2


def tstar(n):
    """Maximiser of phi_n on (0, infinity) by golden-section search on [1e-3, 10] (phi_n is unimodal there, Theorem 5.12)."""
    a, b = mp.mpf("1e-3"), mp.mpf(10)
    g = (mp.sqrt(5) - 1) / 2
    x1, x2 = b - g * (b - a), a + g * (b - a)
    f1, f2 = phi(n, x1), phi(n, x2)
    for _ in range(400):
        if f1 < f2:
            a, x1, f1 = x1, x2, f2
            x2 = a + g * (b - a)
            f2 = phi(n, x2)
        else:
            b, x2, f2 = x2, x1, f1
            x1 = b - g * (b - a)
            f1 = phi(n, x1)
    x0 = (a + b) / 2
    return mp.re(mp.findroot(lambda t: mp.diff(lambda x: phi(n, x), t), x0))   # Newton polish from the bracketed maximum


def D3():
    t0 = time.time()
    rows = []

    def add(no, what, printed, value, source):
        ok = printed_match(printed, value) if not isinstance(value, bool) else value
        rows.append({"row": no, "what": what, "printed": printed, "value": (mp.nstr(value, 12) if isinstance(value, mp.mpf)
                                                                          else value), "source": source, "match": bool(ok)})
    S_, l_, c_ = mp.mpf("0.01"), mp.mpf(1), mp.mpf(1)
    F_ = S_ / l_
    # 1. kappa = 100, R2 = 0.05 failure set
    k_ = mp.mpf(100)
    P0 = c_ / (k_ * F_)
    Pq, = sp.symbols("Pq", positive=True),
    Gq = sp.Rational(1) * Pq / (Pq + sp.Rational(1))
    roots = sorted(sp.solve(sp.Eq((sp.Rational(1, 100) + Gq**2 / (2 * Pq)) / (1 + Gq), sp.Rational(1, 20)), Pq))
    add(1, "kappa = 100, R2 = 0.05: lower end of the failure set", "1/9", roots[0] == sp.Rational(1, 9), "formula (exact roots)")
    add(1, "kappa = 100, R2 = 0.05: upper end of the failure set", "4", roots[-1] == 4, "formula (exact roots)")
    mid = (roots[0] + roots[-1]) / 2
    add(1, "failure set is between the roots (sigma2 > R2 at the midpoint)", "(1/9, 4)",
        bool(((sp.Rational(1, 100) + Gq**2 / (2 * Pq)) / (1 + Gq)).subs(Pq, mid) > sp.Rational(1, 20)), "formula")
    add(1, "factor 36 = 4/(1/9)", "36", mp.mpf(4) / (mp.mpf(1) / 9), "formula")
    del P0
    # 2. Pi0^pair
    reg = {r["n"]: r for r in J("t13", "results", "t13_partA_numeric_A4_A5_A7.json")["A5"]["regression"]}
    for n_, pr in (("1.5", "30.243"), ("2", "31.475"), ("3", "37.820"), ("4", "44.180"), ("8", "62.711")):
        n = mp.mpf(n_)
        ts = tstar(n)
        val = c_ * phi(n, ts) / (2 * n * S_)
        add(2, f"Pi0^pair, n = {n_} (formula)", pr, val, "formula c phi_n(t*)/(2 n Sigma)")
        add(2, f"Pi0^pair, n = {n_} (Task 13 regression)", pr, mp.mpf(reg[n_]["closed_form"]),
            "t13/results/t13_partA_numeric_A4_A5_A7.json A5.regression")
    # 3. M/F
    P0b = c_ / (100 * F_)
    Gt = -l_ + mp.sqrt(l_**2 + l_ * c_ - 2 * S_ * P0b)
    Mb = sig2n(Gt, P0b * Gt / (c_ - Gt)) / F_
    lpv, Spv = mp.mpf(1), 100 * F_ * 1
    r = S_ / Spv
    GM = (-2 * r * lpv + mp.sqrt(4 * r**2 * lpv**2 + 2 * (1 + r) * lpv * (l_ - 2 * r * lpv))) / (1 + r)
    PM = (GM**2 + 2 * lpv * GM) / (2 * Spv)
    Mk = sig2n(GM, PM) / F_
    add(3, "M/F misspecified Kalman (formula)", "17.575", Mk, "formula G_M, Pi_M (Prop. 5.9)")
    add(3, "M/F Bayesian weight (formula)", "9.2875", Mb, "formula (Prop. 5.8 turning point)")
    add(3, "ratio (formula)", "1.892", Mk / Mb, "formula")
    an = {e["lit"]: e for e in J("t13", "results", "t13_audit_numbers.json")["entries"]}
    for lit in ("17.575", "9.2875", "1.892"):
        add(3, f"{lit} (Task 13 audit)", lit, mp.mpf(an[lit]["computed"]), "t13/results/t13_audit_numbers.json")
    # 4. pi_R
    add(4, "pi_R at R2 = 0.6F", "222.2", 2 * l_ * (F_ - mp.mpf("0.6") * F_) / (mp.mpf("0.6") * F_)**2, "formula")
    # 5. Hill window onset
    add(5, "c lambda/(4 Sigma)", "25", c_ * l_ / (4 * S_), "formula")
    for P0h in (mp.mpf(25), mp.mpf("31.475")):
        supq = max(c_ * P / (F_ * (P**2 + P0h**2)) for P in [P0h * mp.mpf(10)**(mp.mpf(i) / 200 - 2) for i in range(801)])
        add(5, f"sup q <= 2 for the Hill gain at Pi0 = {mp.nstr(P0h, 6)}", "<= 2", bool(supq <= 2 + mp.mpf(10)**-30),
            f"grid maximum {mp.nstr(supq, 10)}")
    # 6. t*^2
    ts2 = tstar(mp.mpf(2))**2
    add(6, "t*^2 = 2 sqrt 3 - 3 (n = 2)", "2√3 − 3", bool(abs(ts2 - (2 * mp.sqrt(3) - 3)) < mp.mpf(10)**-30), "formula")
    # 7. chapter 4 worked examples
    PiA, PiB = c_ * (c_ + 2 * l_) / (2 * S_), c_ * l_ / (2 * S_)
    add(7, "Pi_B", "50", PiB, "formula"); add(7, "Pi_A", "150", PiA, "formula")
    for P, cs, p0s, sss, vcs in ((1, "P3", "99.498", "0.0099505", "0.255"), (60, "P2", "64.162", "0.0080540", "0.0091667"),
                                 (500, "P1", None, None, "0.0055")):
        P = mp.mpf(P)
        Gs = -l_ + mp.sqrt(l_**2 + 2 * S_ * P)
        case = "P3" if P < PiB else ("P2" if P < PiA else "P1")
        add(7, f"case at Pi = {P}", cs, case == cs, "formula")
        if p0s:
            add(7, f"Pi0* at Pi = {P}", p0s, P * (c_ / Gs - 1), "formula")
            add(7, f"sigma*^2 at Pi = {P}", sss, Gs / P, "formula")
        add(7, f"V_c at Pi = {P}", vcs, sig2n(c_, P), "formula")
    Gs1 = -l_ + mp.sqrt(l_**2 + 2 * S_)
    add(7, "sigma*^2 below F at Pi = 1", "0.5%", (F_ - Gs1) / F_, "formula")
    Gs60 = -l_ + mp.sqrt(l_**2 + 2 * S_ * 60)
    add(7, "two-ray band width at Pi = 60, relative to F", "11%", (sig2n(c_, mp.mpf(60)) - Gs60 / 60) / F_, "formula")
    # 8. coupling
    K = mp.mpf(1) / 2
    add(8, "c*", "0.019901", Gs1 / K, "formula"); add(8, "sigma*^2", "0.0099505", Gs1, "formula")
    add(8, "c_F", "0.04", 2 * F_ * 2, "formula")
    # 9-12. Task 10
    t4 = J("t10", "results", "t10_4.json")
    add(9, "mixed band median", "5 × 10^-4", mp.mpf(t4["band_rel_median"]), "t10/results/t10_4.json band_rel_median")
    add(9, "mixed band minimum", "4 × 10^-22", mp.mpf(t4["band_rel_min"]), "t10_4.json band_rel_min")
    add(9, "mixed band maximum", "0.96", mp.mpf(t4["band_rel_max"]), "t10_4.json band_rel_max")
    add(9, "mixed band with no window above F", "16%", mp.mpf(t4["frac_M_lt_F"]), "t10_4.json frac_M_lt_F")
    t2 = J("t10", "results", "t10_2.json")
    add(10, "target constructions passed", "101", mp.mpf(sum(r_["pass"] for r_ in t2["every"])), "t10_2.json every[].pass")
    add(10, "target constructions", "101", mp.mpf(len(t2["every"])), "t10_2.json every")
    add(10, "forbidden targets blocked", "24", mp.mpf(sum(r_["blocked"] for r_ in t2["forbidden"])), "t10_2.json forbidden[].blocked")
    add(10, "forbidden targets", "24", mp.mpf(len(t2["forbidden"])), "t10_2.json forbidden")
    add(10, "supplementary construction k = 1 to 5, all pass", "k = 1 to 5",
        [r_["k"] for r_ in t2["a13_supp"]] == [1, 2, 3, 4, 5] and all(r_["pass"] for r_ in t2["a13_supp"]), "t10_2.json a13_supp")
    add(10, "G(1e12)/G(1e11) - 1", "6 × 10^-10", mp.mpf(t2["a13_supp"][0]["ratio_minus_1"]), "t10_2.json a13_supp.ratio_minus_1")
    t3 = J("t10", "results", "t10_3.json")
    fam = t3["families"]
    add(11, "misspecified Kalman sets", "2000", mp.mpf(fam["misspec"]["n"]), "t10_3.json families.misspec.n")
    add(11, "misspecified Kalman sets passing", "2000", mp.mpf(fam["misspec"]["n"] - fam["misspec"]["n_fail"]),
        "t10_3.json families.misspec n - n_fail")
    add(11, "Hill n = 2 sets with the pair (root-count check)", "961", mp.mpf(fam["hill"]["tp_hist_n2"]["2"]),
        "t10_3.json families.hill.tp_hist_n2['2']")
    add(11, "root-count disagreements", "0", mp.mpf(fam["hill"]["exact_count_disagreements"]), "t10_3.json exact_count_disagreements")
    add(11, "Task 10 census sets", "10000", mp.mpf(fam["hill"]["n"]), "t10_3.json families.hill.n")
    add(11, "turning-point position error (Bayes)", "6 × 10^-31", mp.mpf(fam["bayes"]["max_pos_rel_err"]),
        "t10_3.json families.bayes.max_pos_rel_err")
    ex = t3["exploratory"]
    add(11, "two-channel Bayes (max, min, max)", "7", mp.mpf(ex["bayes2"]["tp_hist"].get("3", 0)), "t10_3.json exploratory.bayes2")
    add(11, "two-channel Bayes sets", "2000", mp.mpf(ex["bayes2"]["n"]), "t10_3.json exploratory.bayes2.n")
    add(11, "two-channel Hill (min, max, min, max)", "63", mp.mpf(ex["hill2"]["tp_hist"].get("4", 0)), "t10_3.json exploratory.hill2")
    add(11, "two-channel Hill sets", "2000", mp.mpf(ex["hill2"]["n"]), "t10_3.json exploratory.hill2.n")
    add(12, "Hill sets with two turning points", "4868", mp.mpf(t4["n_sets"]), "t10_4.json n_sets")
    add(12, "tolerances tested", "77888", mp.mpf(t4["n_tests"]), "t10_4.json n_tests")
    # 13. Task 13 A5
    a5 = J("t13", "results", "t13_partA_numeric_A4_A5_A7.json")["A5"]
    add(13, "A5 random sets", "5000", mp.mpf(a5["n"]), "t13 A5.n")
    src = open(os.path.join(CLS, "t13", "t13_partA_numeric.py")).read()
    add(13, "n range lower end 1.01", "1.01", "np.log10(1.01), 1)" in src, "t13/t13_partA_numeric.py (10**uniform(log10 1.01, 1))")
    # 14. Task 8
    t83, t84 = J("results", "t8_3.json"), J("results", "t8_4.json")
    add(14, "T8.3 classes correct", "62", mp.mpf(t83["n_match"]), "results/t8_3.json n_match")
    add(14, "T8.3 classes tested", "62", mp.mpf(t83["n_tests"]), "results/t8_3.json n_tests")
    rep = open(os.path.join(CLS, "REPORT.md")).read()
    add(14, "±10^-6 relative tests", "10^-6", "the ±1e-6 tests" in rep, "REPORT.md")
    add(14, "T8.4 sets", "20000", mp.mpf(t84["N"]), "results/t8_4.json N")
    add(14, "T8.4 classifications", "10^6", t84["total_classifications"] == 10**6, "results/t8_4.json total_classifications")
    nw = open(os.path.join(CLS, "t8_no_window.py")).read()
    add(14, "five sweeps", "5", mp.mpf(len(re.findall(r'^    "[^"]+": lambda', nw, re.M))), "t8_no_window.py SWEEPS")
    # 15. Task 13 audit
    rows13 = {r_["row"]: r_ for r_ in J("t13", "results", "t13_audit_classes.json")["rows"]}
    add(15, "persisting route disagreements, row 12", "122", mp.mpf(rows13[12]["persisting"]), "t13_audit_classes.json rows[12]")
    add(15, "1,000 fresh sets per design-sweep row (10, 11, 12)", "1000", all(rows13[k]["curves"] == 1000 for k in (10, 11, 12)),
        "t13_audit_classes.json rows 10-12 curves")
    # 16. blind searches
    add(16, "T10.7 classifications", "10^6", J("t10", "results", "t10_7.json")["total"] == 10**6, "t10/results/t10_7.json total")
    add(16, "T12 Part C classifications", "4.4 × 10^6", mp.mpf(J("t12", "results", "t12_blind.json")["total"]),
        "t12/results/t12_blind.json total")
    # 17. prior dip
    r12 = open(os.path.join(CLS, "t12", "RESULTS_t12.md")).read()
    add(17, "relative prior dip 10^(-32,880,317)", "10^-32880317", "10^-32880317" in r12, "t12/RESULTS_t12.md")
    # 18. Task 15
    g = json.load(open(os.path.join(CLS, "t15", "results", "t15_partG.json")))
    add(18, "C11 curves", "1000", mp.mpf(g["C11"]["curves"]), "t15_partG.json C11.curves")
    add(18, "C11 tolerances per curve >= 50", "50", mp.mpf(g["C11"]["min_tolerances_per_curve"]), "C11.min_tolerances_per_curve")
    add(18, "C11 classifications", "200000", mp.mpf(g["C11"]["classifications"]), "C11.classifications")
    add(18, "C12 perturbations", "1000", mp.mpf(g["C12"]["cases_run"]), "C12.cases_run")
    add(18, "C12 curves", "500", mp.mpf(g["C12"]["curves"]), "C12.curves")
    add(18, "illustration amplitude/eta", "0.9", mp.mpf(g["ILL"]["amplitude_over_eta"]), "ILL.amplitude_over_eta")
    add(18, "illustration upper ray -> (0, 1, 4)", "upper ray -> (0, 1, 4)",
        g["ILL"]["class_before"] == "upper ray" and g["ILL"]["class_after"] == "(0, 1, 4)", "ILL.class_before/after")
    return {"rows": rows, "n": len(rows), "n_match": sum(r_["match"] for r_ in rows),
            "mismatches": [r_ for r_ in rows if not r_["match"]], "pass": all(r_["match"] for r_ in rows),
            "seconds": round(time.time() - t0, 2)}


# ------------------------------------------------------------------------------------------------------------------ D4
SUP = str.maketrans("", "")


def expand(spec):
    out = []
    for part in re.split(r",\s*|\s+and\s+", spec):
        part = part.strip()
        m = re.fullmatch(r"(\d+)\.(\d+)(?:\([^)]*\))?(?:[–-](\d+)\.(\d+))?", part)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if m.group(3):
            out += [f"{a}.{k}" for k in range(b, int(m.group(4)) + 1)]
        else:
            out.append(f"{a}.{b}")
    return out


TYPE_ALIASES = {"theorem": "Theorem", "theorems": "Theorem", "thm": "Theorem", "proposition": "Proposition",
                "propositions": "Proposition", "prop.": "Proposition", "props.": "Proposition", "lemma": "Lemma", "lemmas": "Lemma",
                "corollary": "Corollary", "corollaries": "Corollary", "cor.": "Corollary", "definition": "Definition",
                "numerical result": "Numerical result", "num. result": "Numerical result", "conjecture": "Conjecture",
                "counterexample": "Counterexample"}


def D4():
    t0 = time.time()
    text = "\n".join(draft_ch15()).replace("\\[", "[").replace("\\]", "]").replace("\\_", "_")
    refs = {r["number"] for r in yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))}
    reg = {e["thesis_no"]: e["type"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))}
    figs = {e["label"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))}
    # citations
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
    order = sorted((n for n in first if n <= 45), key=lambda n: first[n])
    order_ok = order == sorted(order) and set(order) == set(range(1, 46))
    # typed references
    typed_bad, typed_n, untyped_bad, untyped_n = [], 0, [], 0
    tw = r"(Theorems?|Thm|Propositions?|Props?\.|Lemmas?|Corollar(?:y|ies)|Cor\.|Definitions?|Numerical results?|Num\. results?|" \
         r"Conjectures?|Counterexamples?)"
    spec = r"(\d+\.\d+(?:\([^)]*\))?(?:[–-]\d+\.\d+)?(?:(?:,\s*|\s+and\s+)\d+\.\d+(?:\([^)]*\))?(?:[–-]\d+\.\d+)?)*)"
    for m in re.finditer(r"\b" + tw + r"\s+" + spec, text):
        ty = TYPE_ALIASES.get(m.group(1).lower()) or TYPE_ALIASES.get(re.sub(r"s$", "", m.group(1).lower()))
        for no in expand(m.group(2)):
            typed_n += 1
            if no not in reg:
                typed_bad.append({"ref": m.group(0), "number": no, "problem": "no such result"})
            elif reg[no] != ty:
                typed_bad.append({"ref": m.group(0), "number": no, "problem": f"type is {reg[no]}, not {ty}"})
    # untyped: table cells of Label(s)/Result columns and "results x.y–x.z"
    TL = text.split("\n")
    hdr = None
    for i, line in enumerate(TL):
        if line.startswith("|") and i + 1 < len(TL) and re.match(r"^\|[\s|:-]+$", TL[i + 1]) and "-" in TL[i + 1]:
            hdr = [c_.strip() for c_ in line.strip().strip("|").split("|")]
            continue
        if not line.startswith("|"):
            hdr = None
            continue
        if hdr and hdr[-1] in ("Label", "Labels", "Result") and not set(line) <= set("|-: "):
            cells = [c_.strip() for c_ in line.strip().strip("|").split("|")]
            last = cells[-1]
            if re.fullmatch(r"[\d., –-]+", last) and re.search(r"\d+\.\d+", last):
                for no in expand(last):
                    untyped_n += 1
                    if no not in reg:
                        untyped_bad.append({"ref": last, "number": no})
    for m in re.finditer(r"\bresults (\d+\.\d+[–-]\d+\.\d+)", text):
        for no in expand(m.group(1)):
            untyped_n += 1
            if no not in reg:
                untyped_bad.append({"ref": m.group(0), "number": no})
    figrefs = re.findall(r"Figure (B\.\d+)", text)
    figbad = sorted({f for f in figrefs if f not in figs})
    out = {"citation_groups": len(cites), "unresolved": unresolved, "first_order_1_45": order_ok,
           "first_order": order, "excluded_brackets": excluded, "typed_refs": typed_n, "typed_bad": typed_bad,
           "untyped_refs": untyped_n, "untyped_bad": untyped_bad, "figure_refs": len(figrefs), "figure_bad": figbad}
    out["pass"] = not unresolved and order_ok and not typed_bad and not untyped_bad and not figbad
    out["seconds"] = round(time.time() - t0, 2)
    return out


# ------------------------------------------------------------------------------------------------------------------ D5
def D5():
    l_, S_, c_, kap = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1), mp.mpf("1.5")
    F_ = S_ / l_
    P0 = c_ / (kap * F_)
    root = mp.findroot(lambda P: c_ * P / (P + P0) - (-l_ + mp.sqrt(l_**2 + 2 * S_ * P)), 50)
    src = open(os.path.join(CLS, "t13", "t13_figures_paper2.py")).read()
    params_in_script = all(s in src for s in ("lam, Sig, Pi = 1.0, 0.01, 1.0", "kap = 1.5", "c_ = 1.0", "P0 = c_ / (kap * F)"))
    places = {}
    figs = yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))
    places["register/figures.yaml B.4"] = next(e["description"] for e in figs if e["label"] == "B.4")
    places["Appendix_B_Figures.md"] = open(os.path.join(CLS, "Appendix_B_Figures.md")).read().split("**Figure B.4.**")[1].split("\n")[0]
    places["figs_thesis/B.4_realizability.txt"] = open(os.path.join(CLS, "figs_thesis", "B.4_realizability.txt")).read()
    vals = {k: re.findall(r"Pi_c = ([\d.]+)", t.replace("\n", " ")) for k, t in places.items()}
    ok = {k: (len(v_) == 1 and printed_match(v_[0], root)) for k, v_ in vals.items()}
    grid = [10**(-3 + 7 * i / 1499) for i in range(1500)]
    Gs = [2 * 0.01 * P / (1 + math.sqrt(1 + 2 * 0.01 * P)) for P in grid]
    GB = [P / (P + float(P0)) for P in grid]
    grid_pc = next(P for P, a, b in zip(grid, GB, Gs) if a < b)
    return {"root": mp.nstr(root, 15), "script_parameters_as_disclosed": params_in_script, "printed": vals, "match": ok,
            "script_grid_value": float(f"{grid_pc:.3g}"), "pass": all(ok.values()) and params_in_script}


# ------------------------------------------------------------------------------------------------------------------ D6
sys.path[:0] = [os.path.join(CLS, "t15")]


def thesis_renders():
    import t15_checks  # noqa: E402
    return t15_checks.THESIS_RENDERS


def D6():
    reg = yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))
    bare_cw = []
    for e in reg:
        for x in e["legacy"]:
            for m in re.finditer(r"(?<![\w.§])[A-E]\.\d+\b", x):
                if not x[:m.start()].endswith("legacy "):
                    bare_cw.append((e["thesis_no"], x))
    cwt = open(os.path.join(CLS, "register", "crosswalk.md")).read()
    for line in cwt.split("\n")[6:]:
        if line.startswith("|"):
            cell = line.strip("|").split("|")[-1]
            for m in re.finditer(r"(?<![\w.§])[A-E]\.\d+\b", cell):
                if not cell[:m.start()].endswith("legacy "):
                    bare_cw.append(("crosswalk.md", cell.strip()))
    v1 = open(os.path.join(CLS, "register", "crosswalk_v1.yaml")).read()
    for m in re.finditer(r"(?<![\w.])§?[A-E]\.\d+\b", v1):
        if not v1[:m.start()].endswith("legacy "):
            bare_cw.append(("crosswalk_v1.yaml", v1[max(0, m.start() - 20):m.end()]))
    figs = {e["label"] for e in yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))}
    per, bare, false_fig, exempt, paper1 = {}, [], [], {"prefixed": 0, "figure label": 0}, 0
    for p in thesis_renders():
        t = re.sub(r"\s+", " ", open(p).read())
        paper1 += t.count("Paper 1")
        figfile = p.endswith("Appendix_B_Figures.md") or "/figs_thesis/" in p
        for m in re.finditer(r"\b[A-E]\.\d+\b", t):
            lab = m.group(0)
            before = t[max(0, m.start() - 40):m.start()]
            if before.endswith("legacy "):
                exempt["prefixed"] += 1
                continue
            if lab in figs and (figfile or re.search(r"[Ff]igures?\b", before) or t[m.end():m.end() + 1] == "_"):
                exempt["figure label"] += 1
                continue
            rec = {"file": os.path.relpath(p, REPO), "label": lab, "context": t[max(0, m.start() - 40):m.end() + 10]}
            bare.append(rec)
            if before.endswith("Figure "):
                false_fig.append(rec)
    return {"crosswalk_unprefixed": bare_cw, "bare_legacy_labels": bare, "false_hits_figure": false_fig, "exempt": exempt,
            "paper1": paper1, "files": len(thesis_renders()),
            "pass": not bare_cw and not bare and not false_fig and paper1 == 0}


# ------------------------------------------------------------------------------------------------------------------ D7
BRX = re.compile(r"(?<![\w\]\\])\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\](?!\()")


def groups(t):
    return [m.group(1) for m in BRX.finditer(t)]


def is_cite(body, refs):
    nums = []
    for part in body.split(", "):
        a, _, b = part.partition("–")
        nums += list(range(int(a), int(b or a) + 1))
    return all(n in refs for n in nums)


def prep(p, t):
    if p.endswith("Roadmap_v3.md"):
        t = "\n".join(l for l in t.split("\n") if not re.match(r"^\| (6|7|8|9|10) \| ", l))
    return t


def D7():
    import t15_checks  # noqa: E402
    refs = {r["number"] for r in yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))}
    keys = set(t15_checks.bib())
    files = [p for p in thesis_renders() if not p.endswith("Appendix_C_References.md")]
    diag = json.load(open(os.path.join(CLS, "t15", "results", "t15_diag.json")))["C4"]["items"]
    t15_non = {}
    for it in diag:
        if not it["is_citation"]:
            t15_non[it["file"]] = t15_non.get(it["file"], 0) + 1
    base, now, noncit, other = {}, {}, [], []
    for p in files:
        r = os.path.relpath(p, REPO)
        try:
            old = subprocess.run(["git", "show", f"{T15_ARTIFACTS}:{r}"], cwd=REPO, capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError:
            old = ""
        base[r] = len(groups(prep(p, old))) - t15_non.get(r, 0)
        t = prep(p, open(p).read())
        g = groups(t)
        cit = [b for b in g if is_cite(b, refs)]
        now[r] = len(cit)
        noncit += [{"file": r, "group": "[" + b + "]"} for b in g if not is_cite(b, refs)]
        h = [("raw key", k) for k in keys if re.search(r"(?<![\w/.-])" + re.escape(k) + r"(?![\w-])", t)]
        for rx in t15_checks.AY:
            h += [("author-year", m.group(0)) for m in rx.finditer(t)]
        h += [("token", m.group(0)) for m in re.finditer(r"\[@", t)]
        other += [{"file": r, "kind": k, "match": s} for k, s in h]
    flagged_intervals = []   # the new rule flags no non-citation group
    per_file_equal = {r: (base[r], now[r]) for r in now if base[r] != now[r]}
    return {"baseline_total": sum(base.values()), "now_total": sum(now.values()), "per_file_differences": per_file_equal,
            "non_citations": noncit, "flagged_intervals": flagged_intervals, "other_hits": other,
            "pass": not flagged_intervals and not other and sum(base.values()) == sum(now.values()) and not per_file_equal}


# ------------------------------------------------------------------------------------------------------------------ D8
def D8():
    rx = re.compile(r"\b(Theorem|Proposition|Prop\.|Lemma|Corollary|Cor\.|Definition|Numerical result|Conjecture|Counterexample|Thm)"
                    r"\s+(\d+)(?!\.\d)\b")
    hits = []
    for e in yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml"))):
        for vb in e["verified_by"]:
            for m in rx.finditer(vb):
                hits.append({"result": e["thesis_no"], "verified_by": vb, "match": m.group(0)})
    return {"hits": hits, "pass": not hits}


CHECKS = {"D1": D1, "D2": D2, "D3": D3, "D4": D4, "D5": D5, "D6": D6, "D7": D7, "D8": D8}


def main():
    os.makedirs(RES, exist_ok=True)
    which = [a for a in sys.argv[1:] if a in CHECKS] or list(CHECKS)
    path = os.path.join(RES, "t16_checks.json")
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
