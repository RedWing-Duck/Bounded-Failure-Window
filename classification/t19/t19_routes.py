"""Task 19 Part C: corrected re-checks of the failures diagnosed but never re-checked (PREREG_t19.md, Part C).
New checking routes only; every original artifact and input is used unchanged (imported or read, never written).
Each re-check runs in its own interpreter, because the task directories share module names.
Usage: python3 t19_routes.py [--dry] [H-6.C5 H-9.2 ...]     (default: all IDs below except H-13.D, which has its own driver)
--dry shrinks every sample (crash test only; outputs go to results/dry/ and are not results)."""
import json
import math
import os
import random
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
DRY = "--dry" in sys.argv
RES = os.path.join(HERE, "results", "dry" if DRY else "", "h")


def dump(name, obj):
    os.makedirs(RES, exist_ok=True)
    json.dump(obj, open(os.path.join(RES, name + ".json"), "w"), indent=1, ensure_ascii=False, default=str)


def use(*dirs):
    sys.path[:0] = [os.path.join(CLS, d) if not d.startswith("/") else d for d in dirs]


def N(full, dry):
    return dry if DRY else full


# ============================================================================================================ H-6.C5
def H_6_C5():
    """Peaks of the coloured relay at lam = c = 1, Sigma = 0.01, P = 1, tau in {0.01, 0.1, 1, 10}, located by root-finding
    on dC_xx/dPi (no grid), by two routes: (i) the Task 6 symbolic C_xx (Lyapunov solution, re-derived here as in
    t6_colored_symbolic.py), (ii) the Task 4b semi-analytic formula var_tau with the Kalman gain of verification/common.py.
    Pass: the two routes agree on height and location to 3 s.f. at every tau, and the Task 6 fine-grid values recorded in
    verification/results/t6.json round to the same 3 s.f."""
    import mpmath as mp
    import sympy as sp
    use("/" + os.path.join(REPO, "verification"))
    import common as C4  # verification/common.py (Task 4 module, unchanged)
    mp.mp.dps = 50
    lam, c, S, P, Pi, tau, G = sp.symbols("lambda c Sigma P Pi tau G", positive=True)
    a = lam + G
    A = sp.Matrix([[-a, G], [0, -1 / tau]])
    B = sp.diag(sp.sqrt(2 * S), 1 / (tau * sp.sqrt(Pi)))
    cxx, cxe, cee = sp.symbols("C_xx C_xe C_ee")
    Cm = sp.Matrix([[cxx, cxe], [cxe, cee]])
    L = A * Cm + Cm * A.T + B * B.T
    Cxx = sp.simplify(sp.solve([L[0, 0], L[0, 1], L[1, 1]], [cxx, cxe, cee], dict=True)[0][cxx])
    # gain of verification/common.g_kalman, c Pi/(Pi + P) (the Task 4b/6 gain), written symbolically and in mp
    import inspect
    src_g = inspect.getsource(C4.g_kalman)
    Gk = c * Pi / (Pi + P)
    vals = {lam: 1, c: 1, S: sp.Rational(1, 100), P: 1}
    expr = Cxx.subs(G, Gk).subs(vals)
    f6 = sp.lambdify((Pi, tau), expr, "mpmath")
    d6 = sp.lambdify((Pi, tau), sp.diff(expr, Pi), "mpmath")

    def gk_mp(pi_):
        return pi_ / (pi_ + 1)

    def f4b(pi_, t):
        # verification/t4b_colored.var_tau, in mp: (SIG + g^2/(2 pi (1 + a tau)))/a, a = LAM + g
        g = gk_mp(pi_)
        aa = 1 + g
        return (mp.mpf("0.01") + g**2 / (2 * pi_ * (1 + aa * t))) / aa

    t6 = json.load(open(os.path.join(REPO, "verification", "results", "t6.json")))
    t6rows = {r["tau"]: r for r in t6["c5"]}
    r3 = lambda v: float(mp.nstr(mp.mpf(v), 3))  # noqa: E731
    rows, ok = [], True
    for tv in (0.01, 0.1, 1, 10):
        t = mp.mpf(str(tv))
        x6 = mp.findroot(lambda u: d6(mp.exp(u), t), mp.log(mp.mpf("0.5")))
        P6 = mp.exp(x6)
        H6 = f6(P6, t)
        x4 = mp.findroot(lambda u: mp.diff(lambda y: f4b(mp.exp(y), t), u), mp.log(mp.mpf("0.5")))
        P4 = mp.exp(x4)
        H4 = f4b(P4, t)
        # gain check: the float g_kalman and the mp form agree at the peak
        gchk = abs(float(gk_mp(P4)) - float(C4.g_kalman(float(P4), 1.0))) <= 1e-12 * float(gk_mp(P4))
        rec = t6rows.get(tv) or t6rows.get(float(tv)) or {}
        m = {"tau": tv, "Pi_star_T6": mp.nstr(P6, 12), "peak_T6": mp.nstr(H6, 12), "Pi_star_4b": mp.nstr(P4, 12),
             "peak_4b": mp.nstr(H4, 12), "rel_diff_Pi": mp.nstr(abs(P6 / P4 - 1), 3), "rel_diff_peak": mp.nstr(abs(H6 / H4 - 1), 3),
             "loc_3sf": [r3(P6), r3(P4)], "height_3sf": [r3(H6), r3(H4)], "gain_form_matches_common": gchk,
             "t6_grid": {"peak": rec.get("peak"), "peak_Pi": rec.get("peak_Pi")}}
        m["routes_agree_3sf"] = r3(P6) == r3(P4) and r3(H6) == r3(H4)
        m["grid_rounds_same"] = (rec.get("peak_Pi") is not None and r3(rec["peak_Pi"]) == r3(P6)
                                 and r3(rec["peak"]) == r3(H6))
        ok &= m["routes_agree_3sf"] and m["grid_rounds_same"] and gchk
        rows.append(m)
    out = {"rows": rows, "g_kalman_source": src_g, "pass": bool(ok)}
    dump("H-6.C5", out)
    return out


# ============================================================================================================ H-9.2
def H_9_2():
    """ARE route in extended precision: the 2x2 regularised ARE of T9.2 solved by the Hamiltonian stable subspace (the function
    are_mp of t9_filter_diag.py, its definition executed unchanged; the module itself is not imported because importing it runs
    the diagnosis) at 100 digits, at eps = 1e-30 and 1e-40, on the 2,001 pre-registered cases (seed 9002). Pass: relative error to
    Proposition 3.1 <= 1e-5 at eps = 1e-40 in every case, and O(sqrt(eps)) convergence: the log-slope of the gap between
    eps = 1e-30 and 1e-40 lies in [0.45, 0.55] wherever the gap at 1e-30 exceeds 1e-60 relative."""
    import mpmath as mp
    import numpy as np
    use("t9")
    from t9_common import P_opt
    mp.mp.dps = 100
    src = open(os.path.join(CLS, "t9", "t9_filter_diag.py")).read()
    ns = {"mp": mp}
    exec(src[src.index("def are_mp"):src.index("def wiener_closed")], ns)   # the function definition only, unchanged
    are_mp = ns["are_mp"]
    rng = np.random.default_rng(9002)
    S = 10.0**rng.uniform(-3, 3, size=(1000, 4))
    lt = 10.0**rng.uniform(-3, 3, size=1000)
    cases = [(S[i, 0], S[i, 1], S[i, 2], t) for i in range(1000) for t in (lt[i] / S[i, 0], 1.0 / S[i, 0])]
    cases.append((1.0, 0.01, 1.0, 1.0))
    cases = cases[:N(len(cases), 12)]
    worst, n_over, slopes_bad, slopes, n_slope = 0.0, 0, [], [], 0
    for lam, Sig, Pi, tau in cases:
        mp.mp.dps = 100
        ref = P_opt(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))
        g30 = abs(are_mp(lam, Sig, Pi, tau, mp.mpf("1e-30")) - ref) / ref
        g40 = abs(are_mp(lam, Sig, Pi, tau, mp.mpf("1e-40")) - ref) / ref
        worst = max(worst, float(g40))
        n_over += int(g40 > mp.mpf("1e-5"))
        if g30 > mp.mpf("1e-60"):
            n_slope += 1
            s = float((mp.log10(g30) - mp.log10(g40)) / 10)
            slopes.append(s)
            if not 0.45 <= s <= 0.55:
                slopes_bad.append({"case": (lam, Sig, Pi, tau), "slope": s, "gap30": float(g30), "gap40": float(g40)})
    out = {"n": len(cases), "dps": 100, "max_rel_err_eps_1e-40": worst, "n_over_1e-5": n_over, "n_slope_tested": n_slope,
           "slope_range": [min(slopes), max(slopes)] if slopes else None, "slope_bad": slopes_bad[:20], "n_slope_bad": len(slopes_bad)}
    out["pass"] = n_over == 0 and not slopes_bad
    dump("H-9.2", out)
    return out


# ============================================================================================================ H-9.5
def _h95_set(i):
    import mpmath as mp
    import numpy as np
    use("t9")
    from t9_common import P_opt, V_best, draw_sets
    mp.mp.dps = 50
    sets = draw_sets(np.random.default_rng(9004), 2000)
    lam, Sig, Pi, _ = (float(x) for x in sets[i])
    lm, Sm, Pm = mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi)

    def s2(G, t):
        a = lm + G
        return (Sm + G**2 / (2 * Pm * (1 + a * t))) / a

    def ds2(G, t):
        a = lm + G
        d = 1 + a * t
        return (G / (Pm * d) - G**2 * t / (2 * Pm * d**2)) / a - (Sm + G**2 / (2 * Pm * d)) / a**2

    taus = np.logspace(-6, 6, 200) / lam
    res = {"set": i, "not_decreasing": [], "V_le_P": [], "grid_above": [], "n_local": 0}
    prev = None
    for j, t in enumerate(taus):
        tm = mp.mpf(t)
        xs = np.linspace(np.log10(lam) - 20, np.log10(lam) + 20, 401)

        def f(x):
            G = 10.0**x
            a = lam + G
            return (Sig + G**2 / (2 * Pi * (1 + a * t))) / a
        v = np.array([f(x) for x in xs])
        loc = [k for k in range(1, 400) if v[k] <= v[k - 1] and v[k] <= v[k + 1]]
        res["n_local"] += len(loc)
        cand = [1 / (2 * Pm * tm), Sm / lm]
        for k in loc:
            try:
                g = mp.findroot(lambda u: ds2(mp.exp(u), tm), mp.log(10) * mp.mpf(xs[k]))
                if mp.im(g) == 0:
                    cand.append(s2(mp.exp(g), tm))
            except (ValueError, ZeroDivisionError):
                pass
        V = min(cand)
        if V > mp.mpf(float(v.min())) * (1 + mp.mpf("1e-12")):
            res["grid_above"].append({"j": j, "lam_tau": lam * t})
        P = P_opt(tm, lm, Sm, Pm)
        if not V > P:
            res["V_le_P"].append({"j": j, "lam_tau": lam * t, "rel": float((V - P) / P)})
        if prev is not None and not V < prev:
            res["not_decreasing"].append({"j": j, "lam_tau": lam * t, "rel": float((prev - V) / prev)})
        prev = V
    return res


def H_9_5():
    """Monotonicity and ordering of V(tau) = inf_G sigma^2 in extended precision at every one of the 400,000 pre-registered samples
    (2,000 sets, seed 9004, 200 log-spaced tau): V in mpmath at 50 digits as the least of the G -> oo limit 1/(2 Pi tau), the
    G = 0 value F and the stationary values refined by findroot from every local minimum of the 401-point float grid in log10 G.
    Pass (Propositions 6.8, 6.9): V strictly decreasing along every grid, V > P at every sample, and V never above the float
    grid minimum by more than 1e-12 relative (no basin missed)."""
    from multiprocessing import Pool
    n = N(2000, 4)
    with Pool(4) as pool:
        rr = pool.map(_h95_set, range(n), chunksize=10)
    out = {"sets": n, "samples": 200 * n, "dps": 50,
           "n_not_decreasing": sum(len(r["not_decreasing"]) for r in rr), "n_V_le_P": sum(len(r["V_le_P"]) for r in rr),
           "n_grid_above": sum(len(r["grid_above"]) for r in rr), "local_minima_refined": sum(r["n_local"] for r in rr),
           "examples": [r for r in rr if r["not_decreasing"] or r["V_le_P"] or r["grid_above"]][:10]}
    out["pass"] = out["n_not_decreasing"] == 0 and out["n_V_le_P"] == 0 and out["n_grid_above"] == 0
    dump("H-9.5", out)
    return out


# ============================================================================================================ T17 helpers
def _t17():
    use("t17", "t16", "t15", "register")
    import t17_checks as T17
    return T17


def _fallback(lhs, rhs, syms, sampler, seed, dps_of, n=1000):
    """Pre-registered numerical fallback: n random sets, stated seed, relative residual < 1e-35 at the working precision dps_of(vals)."""
    import mpmath as mp
    import sympy as sp
    rng = random.Random(seed)
    f, g = sp.lambdify(syms, lhs, "mpmath"), sp.lambdify(syms, rhs, "mpmath")
    worst, maxd = mp.mpf(0), 0
    for _ in range(N(n, 20)):
        vals = sampler(rng)
        d = dps_of(vals)
        maxd = max(maxd, d)
        with mp.workdps(d):
            v = [mp.mpf(x) for x in vals]
            a_, b_ = f(*v), g(*v)
            r = abs(a_ - b_) / max(abs(a_), abs(b_), mp.mpf(10)**(-d))
            worst = max(worst, r)
    return {"seed": seed, "n": N(n, 20), "max_rel": float(worst), "max_digits": maxd, "pass": bool(worst < mp.mpf(10)**-35)}


def _lu(rng, lo=-3, hi=3):
    return 10 ** rng.uniform(lo, hi)


# ============================================================================================================ H-10.1a, H-10.1b
def H_10_1a():
    """Misspecified inverse (Proposition 5.9's proof): G(Pi(G)) - G = 0 for G = -lam' + sqrt(lam'^2 + 2 Sig' Pi) and
    Pi(G) = (G^2 + 2 lam' G)/(2 Sig'). Denesting: the radicand factors as (G + lam')^2 and G + lam' > 0 (sum of positives), so
    sqrt = G + lam'. Pass: the residual reduces to 0 after denesting, and the fallback (seed 19004) holds."""
    import sympy as sp
    T17 = _t17()
    G, l1, S1, Pi = sp.symbols("G lambda1 Sigma1 Pi", positive=True)
    GM = -l1 + sp.sqrt(l1**2 + 2 * S1 * Pi)
    e = GM.subs(Pi, (G**2 + 2 * l1 * G) / (2 * S1)) - G
    rads = [p for p in e.atoms(sp.Pow) if p.exp == sp.S.Half]
    fac = [str(sp.factor(r.base)) for r in rads]
    Y = G + l1
    sign = bool(Y.is_positive)
    den = e.subs({r: Y for r in rads if sp.expand(r.base - Y**2) == 0})
    z = T17.zero(den)
    fb = _fallback(GM.subs(Pi, (G**2 + 2 * l1 * G) / (2 * S1)), G, (G, l1, S1),
                   lambda r: [_lu(r), _lu(r), _lu(r)], 19004, lambda v: 60)
    out = {"radicands_factored": fac, "Y": str(Y), "Y_positive": sign, "residual_after_denesting": z, "fallback": fb}
    out["pass"] = bool(sign and z["zero"] and fb["pass"])
    dump("H-10.1a", out)
    return out


def H_10_1b():
    """Forced ray (Corollary 5.2): sigma*^2(pi_R) = R^2 at pi_R = 2 lam (F - R^2)/R^4, 0 < R^2 < F. With Sigma = lam F and
    R^2 = F/(1 + w), w > 0 (exactly 0 < R^2 < F), the radicand is a perfect square c Y^2 with Y = 2F - R^2 > 0 (since R^2 < F).
    Pass: the residual reduces to 0 after denesting with that sign, and the fallback (seed 19004 + 1, R^2 uniform in (0, F))
    holds."""
    import mpmath as mp
    import sympy as sp
    T17 = _t17()
    lam, F, w, R2 = sp.symbols("lambda F w R2", positive=True)
    Sig = lam * F
    piR = 2 * lam * (F - R2) / R2**2
    sstar = 2 * Sig / (lam + sp.sqrt(lam**2 + 2 * Sig * piR))
    e = sp.simplify((sstar - R2).subs(R2, F / (1 + w)))
    rads = [p for p in e.atoms(sp.Pow) if p.exp == sp.S.Half]
    info = []
    rep = {}
    for r in rads:
        f = sp.factor(r.base)
        info.append({"radicand": str(f)})
        # explicit square root: Y = sqrt(numerator)/sqrt(denominator) with powers denested; kept only if Y**2 == f and Y > 0
        num, dnm = sp.fraction(sp.together(f))
        Yn = sp.sqrt(sp.factor(num))
        Yd = sp.sqrt(sp.factor(dnm))
        Yn, Yd = sp.powdenest(Yn, force=True), sp.powdenest(Yd, force=True)
        Ycand = sp.simplify(Yn / Yd)
        ok_sq = sp.simplify(Ycand**2 - f) == 0
        info[-1].update({"Y": str(Ycand), "Y_squared_equals_radicand": bool(ok_sq), "Y_positive": bool(Ycand.is_positive)})
        if ok_sq and Ycand.is_positive:
            rep[r] = Ycand
    z = T17.zero(e.subs(rep)) if rep else {"zero": False}
    # sign argument stated in the dimensional variables: 2F - R^2 > 0 because R^2 < F
    Yd_dim = sp.simplify((2 * F - R2).subs(R2, F / (1 + w)))
    sgn = bool(Yd_dim.is_positive)

    def samp(r):
        l_, F_ = _lu(r), _lu(r)
        return [l_, F_, F_ * r.uniform(1e-6, 1 - 1e-6)]
    fb = _fallback(sstar, R2, (lam, F, R2), samp, 19005, lambda v: 60)
    out = {"residual_after_substitution": str(e)[:400], "radicands": info, "two_F_minus_R2_positive": sgn,
           "residual_after_denesting": z, "fallback": fb}
    out["pass"] = bool(rep and all(i["Y_positive"] for i in info) and sgn and z["zero"] and fb["pass"])
    dump("H-10.1b", out)
    return out


# ============================================================================================================ H-10.5
def H_10_5():
    """Pair birth (Proposition 2.7) for the Hill gain n = 2 at lam = c = 1, Sigma = 0.01, with the T10.5 code unchanged
    (t10_census.pair_birth, hill_count). Pass: on the pre-registered delta = 1e-6..1e-12, M - m -> 0 monotonically, the slope of
    log(M - m) lies in [1.45, 1.55] (values ~ delta^(3/2)) and the slope of the position separation in [0.45, 0.55]
    (~ delta^(1/2)); (M - m)/sep^3 varies by less than 1e-3 relative (the fold constant |a|/6); and on the diagnosis's
    delta = 1e-4..1e-14 the fitted exponents round to the printed 1.50007 and 0.50002."""
    import mpmath as mp
    import numpy as np
    use("t10")
    from t10_census import hill_count, pair_birth
    pb = pair_birth(2)["transitions"][0]
    P0p = pb["Pi0_double_root"] or pb["Pi0_bisect"]

    def fit(es):
        rows = []
        for e in es:
            d = mp.power(10, -e)
            ts = hill_count(2, P0p * (1 - d))["turns"]
            if len(ts) == 2:
                dv, dx = ts[1]["value"] - ts[0]["value"], ts[1]["x"] - ts[0]["x"]
                rows.append({"delta": d, "M_minus_m": dv, "x_sep": dx, "ratio": dv / dx**3})
            else:
                rows.append({"delta": d, "n_tp": len(ts)})
        good = [r for r in rows if "M_minus_m" in r]
        ld = np.log10([float(r["delta"]) for r in good])
        sv = float(np.polyfit(ld, np.log10([float(r["M_minus_m"]) for r in good]), 1)[0]) if len(good) > 1 else None
        sx = float(np.polyfit(ld, np.log10([float(r["x_sep"]) for r in good]), 1)[0]) if len(good) > 1 else None
        return rows, good, sv, sx
    rows, good, sv, sx = fit(range(6, 13))
    mono = len(good) == 7 and all(good[i + 1]["M_minus_m"] < good[i]["M_minus_m"] for i in range(6))
    rat = [r["ratio"] for r in good]
    const = bool(rat) and max(abs(x / rat[0] - 1) for x in rat) < mp.mpf("1e-3")
    rows2, good2, sv2, sx2 = fit(range(4, 15)) if not DRY else ([], [], None, None)
    use("t16")
    import t16_checks as T16
    pv = sv2 is not None and T16.printed_match("1.50007", sv2) and T16.printed_match("0.50002", sx2)
    out = {"Pi0_pair": mp.nstr(P0p, 15), "rows": rows, "slope_values": sv, "slope_positions": sx, "monotone": mono,
           "ratio_constant_1e-3": const, "diag_range_slopes": [sv2, sx2], "printed_1.50007_0.50002": bool(pv)}
    out["pass"] = bool(mono and sv is not None and 1.45 <= sv <= 1.55 and 0.45 <= sx <= 0.55 and const and (pv or DRY))
    dump("H-10.5", out)
    return out


# ============================================================================================================ H-10.6
def H_10_6():
    """Zero limits of P(tau) at matched variance, corrected per the T10 diagnosis, on the T10.6 sets (seed 10006, 1,000 sets):
    P < 1e-6 P_max at lam tau = 1e-24 and 1e24; the log-slope of P between lam tau = 10^(+-10) and 10^(+-12) within 1e-3 of
    +-0.5; and P/P_max at lam tau = 1e-+12 equal to the asymptote 2e-6 (Sigma + lam v)/sqrt(lam Sigma v) within 1e-3 relative.
    t10_tau.P_rat is used unchanged, at 60 digits."""
    import mpmath as mp
    import numpy as np
    use("t10")
    from t10_tau import P_rat
    mp.mp.dps = 60
    rng = np.random.default_rng(10006)
    S = 10.0**rng.uniform(-2, 2, size=(1000, 4))
    bad = []
    mins = {"z24": mp.mpf(0), "slope_dev": mp.mpf(0), "asym_dev": mp.mpf(0)}
    for i in range(N(1000, 10)):
        lam, Sig, v = (mp.mpf(x) for x in S[i, :3])
        Pmax = Sig * v / (Sig + lam * v)
        z24 = [P_rat(mp.power(10, s) / lam, lam, Sig, v) / Pmax for s in (-24, 24)]
        sl = [(mp.log10(P_rat(mp.power(10, s * 12) / lam, lam, Sig, v)) - mp.log10(P_rat(mp.power(10, s * 10) / lam, lam, Sig, v)))
              / (2 * s) for s in (-1, 1)]
        pred = 2 * mp.mpf("1e-6") * (Sig + lam * v) / mp.sqrt(lam * Sig * v)
        asy = [abs(P_rat(mp.power(10, s) / lam, lam, Sig, v) / Pmax / pred - 1) for s in (-12, 12)]
        mins["z24"] = max(mins["z24"], max(z24))
        mins["slope_dev"] = max(mins["slope_dev"], abs(sl[0] - mp.mpf("0.5")), abs(sl[1] + mp.mpf("0.5")))
        mins["asym_dev"] = max(mins["asym_dev"], max(asy))
        ok = (all(z < mp.mpf("1e-6") for z in z24) and abs(sl[0] - mp.mpf("0.5")) <= mp.mpf("1e-3")
              and abs(sl[1] + mp.mpf("0.5")) <= mp.mpf("1e-3") and max(asy) <= mp.mpf("1e-3"))
        if not ok:
            bad.append(i)
    out = {"sets": N(1000, 10), "max_P_over_Pmax_at_1e+-24": mp.nstr(mins["z24"], 4), "max_slope_dev": mp.nstr(mins["slope_dev"], 4),
           "max_asymptote_dev": mp.nstr(mins["asym_dev"], 4), "failing_sets": bad, "pass": not bad}
    dump("H-10.6", out)
    return out


# ============================================================================================================ H-11.3
BETA_KEYS = None


def _h113_job(args):
    import mpmath as mp
    import numpy as np
    use("t11")
    from t11_common import P_pow, analyse_with_limits, classify, limits_pow, name, power_curve, sstar
    from t11_power import BETAS
    bi, p, seed = args
    beta = BETAS[bi]
    K, lam, Sig = (mp.mpf(p[k]) for k in ("K", "lam", "Sig"))
    Lm, Lp, xm, xp = limits_pow(beta, K, lam, Sig)
    if beta == 2:
        Lp = sstar(lam, Sig, lam**2 / K)                        # corrected limit (T11 diagnosis)
    elif beta > 2:
        xp = max(mp.mpf(80), 50 / (beta - 2)) - mp.log10(lam)    # corrected outer bracket (T11 diagnosis)
    A = analyse_with_limits(power_curve(beta, K, lam, Sig), Lm, Lp, xm, xp)
    tps = A["turns"]
    rg = "le0" if beta <= 0 else ("ge2" if beta >= 2 else "mid")
    if rg == "mid":
        Pmax = max(t["value"] for t in tps) if tps else None
        Pref = Pmax if Pmax is not None else max(Lm, Lp)
    else:
        Pref = Lm if rg == "le0" else Lp
    r_ = np.random.default_rng(seed)
    tols = [Pref * mp.power(10, mp.mpf(float(x))) for x in r_.uniform(-3, float(mp.log10(2)), 7)]
    tols += [Pref * (1 - mp.mpf("1e-6")), Pref, Pref * (1 + mp.mpf("1e-6"))]
    allowed = {"le0": {(1, 0, 0), (0, 0, 0)}, "ge2": {(0, 1, 0), (0, 0, 0)}}.get(rg)
    bad, counts = [], {}
    for R2 in tols:
        r = classify(A, R2)
        c1, c2 = r["route_i"], r["route_ii"]
        okc = c1 == c2 and (c1 in allowed if rg != "mid" else (c1 == (0, 0, 0) or (c1 != "All" and c1[0] == 0 and c1[1] == 0 and c1[2] >= 1)))
        counts[name(c1)] = counts.get(name(c1), 0) + 1
        if not okc:
            bad.append({"R2": mp.nstr(R2, 20), "route_i": name(c1), "route_ii": name(c2)})
    return {"bi": bi, "beta": mp.nstr(beta, 10), "classes": counts, "bad": bad}


def H_11_3():
    """T11.3 classes with the corrected limits and brackets of the T11 diagnosis, on all 129 beta values x 300 sets x 10 tolerances
    (the pre-registered sets and tolerance seeds, rng 11003 drawn as in t11_power.main). Pass (Theorem 7.8): beta <= 0 -> lower
    ray or Empty; beta >= 2 -> upper ray or Empty; 0 < beta < 2 -> (0, 0, k) with k >= 1 or Empty; route (i) = route (ii) in
    every classification."""
    from multiprocessing import Pool
    import numpy as np
    use("t11")
    from t11_power import BETAS, NSET
    rng = np.random.default_rng(11003)
    jobs = []
    for bi in range(len(BETAS)):
        for _ in range(NSET):
            p = {k: float(10.0**rng.uniform(-2, 2)) for k in ("lam", "Sig", "K")}
            jobs.append((bi, p, int(rng.integers(2**63))))
    if DRY:
        jobs = [j for j in jobs if j[0] in (0, 40, 60, 80, 121, 125)][:24]
    with Pool(4) as pool:
        rr = pool.map(_h113_job, jobs, chunksize=20)
    by = {}
    for r in rr:
        b = by.setdefault(r["beta"], {"classifications": 0, "failures": 0, "classes": {}})
        b["classifications"] += sum(r["classes"].values())
        b["failures"] += len(r["bad"])
        for k, v in r["classes"].items():
            b["classes"][k] = b["classes"].get(k, 0) + v
    out = {"betas": len(by), "classifications": sum(b["classifications"] for b in by.values()),
           "failures": sum(b["failures"] for b in by.values()), "by_beta": by,
           "fail_examples": [x for r in rr for x in r["bad"]][:20]}
    out["pass"] = out["failures"] == 0 and (out["betas"] == 129 or DRY)
    dump("H-11.3", out)
    return out


# ============================================================================================================ H-12.A5
def H_12_A5():
    """D2 post at dt -> oo (Table 6.x): dt (P+ - (1-c)^2 F) -> c[c + 2(1-c)F Pi0]/Pi. Series route: e^{-2 lam dt} -> 0 (beyond all
    orders), dt = 1/t, limit t -> 0+ of the T12 symbolic expression (t12_common.SYM, unchanged); the difference from the stated
    coefficient must reduce to 0. Limit sequence: 1,000 random sets (seed 19003; lam, Sigma, Pi, Pi0 log-uniform on [1e-2, 1e2],
    c = 2 * 10^U(-4, 0)) at dt = 1e10, 1e20, 1e40, working precision 60 + 2D digits for dt = 10^D (the cancellation in
    P+ - (1-c)^2 F is of relative size 10^-D; e^{-2 lam dt} is not resolved because it is beyond all orders): relative error
    below 10^(-D+6). Pass: both."""
    import mpmath as mp
    import sympy as sp
    use("t12")
    from t12_common import SYM, P0, Pi, Sig, c, _lamb, lam, x
    Fs = Sig / lam
    target = c * (c + 2 * (1 - c) * Fs * P0) / Pi
    e = x * (SYM["D2"]["post"] - (1 - c)**2 * Fs)
    t, E = sp.symbols("t E", positive=True)
    e_t = e.subs(sp.exp(-2 * lam * x), E).subs(x, 1 / t).subs(E, 0)
    lim_t = sp.limit(sp.simplify(e_t), t, 0, "+")
    ser = sp.series(sp.simplify(e_t), t, 0, 1).removeO()
    z_lim = sp.simplify(lim_t - target) == 0
    z_ser = sp.simplify(ser - target) == 0
    rng = random.Random(19003)
    fl = _lamb("D2", "post")[0]
    worst = {}
    for _ in range(N(1000, 10)):
        p = {"lam": 10 ** rng.uniform(-2, 2), "Sig": 10 ** rng.uniform(-2, 2), "Pi": 10 ** rng.uniform(-2, 2),
             "c": 2 * 10 ** rng.uniform(-4, 0), "Pi0": 10 ** rng.uniform(-2, 2)}
        for D in (10, 20, 40):
            with mp.workdps(60 + 2 * D):
                l_, S_, P_, c_, Q_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi", "c", "Pi0"))
                F = S_ / l_
                tg = c_ * (c_ + 2 * (1 - c_) * F * Q_) / P_
                dt = mp.power(10, D)
                v = dt * (fl(dt, l_, S_, P_, mp.mpf(1), c_, Q_, mp.mpf(1)) - (1 - c_)**2 * F)
                worst[D] = max(worst.get(D, mp.mpf(0)), abs(v / tg - 1))
    ok_seq = all(worst[D] < mp.power(10, -D + 6) for D in worst)
    out = {"series_route_limit": str(sp.factor(lim_t)), "limit_minus_stated_is_0": bool(z_lim), "series_minus_stated_is_0": bool(z_ser),
           "sequence_worst_rel": {f"dt=1e{D}": mp.nstr(v, 3) for D, v in worst.items()}, "sequence_pass": bool(ok_seq),
           "seed": 19003, "sets": N(1000, 10)}
    out["pass"] = bool(z_lim and z_ser and ok_seq)
    dump("H-12.A5", out)
    return out


# ============================================================================================================ H-12.A7
def _h12a7_set(p):
    import mpmath as mp
    import numpy as np
    import sympy as sp
    use("t12")
    from t12_common import SYM, ARGS, dps_for, dt_funcs
    post = SYM["D1"]["post"]
    lam_s, Sig_s = ARGS[1], ARGS[2]
    g_expr = 2 * lam_s * (Sig_s / lam_s - post) + sp.diff(post, ARGS[0])
    g_num = sp.lambdify(ARGS, g_expr, "mpmath", cse=True)
    lam, Sig, Pi, G = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi", "G"))
    F = Sig / lam
    xs = [mp.mpf(v) - mp.log10(lam) for v in np.linspace(-8, 8, 801)]
    sg = []
    for xx in xs:
        t = mp.power(10, xx)
        with mp.workdps(dps_for(lam * t) + 20):
            sg.append(mp.sign(g_num(t, lam, Sig, Pi, G, 1, 1, 1)))
    fpost, _ = dt_funcs("D1", "post", p)
    mins = []
    for i in range(len(xs) - 1):
        if sg[i] < 0 < sg[i + 1]:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(120):
                m = (lo + hi) / 2
                with mp.workdps(dps_for(lam * mp.power(10, m)) + 20):
                    v = g_num(mp.power(10, m), lam, Sig, Pi, G, 1, 1, 1)
                lo, hi = (m, hi) if v < 0 else (lo, m)
            t = mp.power(10, (lo + hi) / 2)
            with mp.workdps(dps_for(lam * t) + 20):
                gap = F - fpost(t)                                  # F - P+ (no cancellation of the exponential)
                dip = mp.exp(-2 * lam * t) * gap / F                 # (F - prior)/F, factored exact form
            mins.append({"lam_dt": lam * t, "F_minus_post_rel": gap / F, "rel_dip": dip})
    with mp.workdps(60):
        Lm = (Sig + G**2 / (2 * Pi)) / (lam + G)                      # prior at dt -> 0: sigma^2(G, Pi)
    deep = max((m["rel_dip"] for m in mins), default=None)
    res = {"p": p, "n_min": len(mins), "start_above_F": bool(Lm > F), "dips_positive": all(m["rel_dip"] > 0 for m in mins),
           "lam_dt": [mp.nstr(m["lam_dt"], 6) for m in mins], "log10_deepest_rel_dip": mp.nstr(mp.log10(deep), 8) if deep else None}
    # class at R^2 = (lowest minimum + F)/2: prior - R^2 = F (dip_rel/2) - e^{-2 lam dt}(F - P+) ... evaluated in the factored form
    if mins:
        R2_rel = deep / 2                                            # (F - R^2)/F
        ell = Lm > F * (1 - R2_rel)                                  # prior(0+) = sigma^2(G, Pi) > R^2
        u = True                                                     # prior -> F > R^2 (approached from below, Prop. 6.20)
        notall = deep > R2_rel                                       # prior(t_min) < R^2
        res.update({"ell": bool(ell), "u": u, "not_All": bool(notall)})
    return res


def H_12_A7():
    """Proposition 6.20 (prior half; the avg half passed in the recorded T12 run, 907/907): on every D1 set of the T12 A8 census
    (t12/results/t12_a8.json, unchanged) with G > 2F Pi, the prior has an interior minimum below F, found as a - to + sign change
    of the scaled derivative g = 2 lam (F - P+) + dP+/ddt (d prior/ddt = e^{-2 lam dt} g, exact), scanned on 801 points of
    log10(lam dt) in [-8, 8] at dps_for(lam dt) + 20 digits and bisected 120 times; the dip is evaluated in the factored form
    (F - prior)/F = e^{-2 lam dt}(F - P+)/F, so the zero tolerance scales with the dip (a direct evaluation of prior - F would need
    more than 2 lam dt/ln 10 digits, up to 3.3e7). The class at R^2 = (deepest minimum + F)/2 is read from the endpoint limits and
    that minimum: l = 1 (prior(0+) = sigma^2(G, Pi) > F > R^2), u = 1 (prior -> F > R^2), not All (minimum < R^2).
    Pass: every set has a minimum below F, every dip positive, and l = u = 1, not All, in every set. A symbolic prerequisite: the
    T12 prior equals F + e^{-2 lam dt}(P+ - F) (residual 0)."""
    import sympy as sp
    from multiprocessing import Pool
    use("t12")
    from t12_common import SYM, x, lam, Sig
    T17 = _t17()
    pre = T17.zero(SYM["D1"]["prior"] - (Sig / lam + sp.exp(-2 * lam * x) * (SYM["D1"]["post"] - Sig / lam)))
    a8 = json.load(open(os.path.join(CLS, "t12", "results", "t12_a8.json")))
    sets = [s["p"] for s in a8["sets"] if s["fam"] == "D1" and s["p"]["G"] > 2 * s["p"]["Sig"] / s["p"]["lam"] * s["p"]["Pi"]]
    sets = sets[:N(len(sets), 6)]
    with Pool(4) as pool:
        rr = pool.map(_h12a7_set, sets, chunksize=4)
    out = {"prior_identity": pre, "sets": len(sets), "with_min": sum(r["n_min"] >= 1 for r in rr),
           "n_min_hist": {str(k): sum(r["n_min"] == k for r in rr) for k in sorted({r["n_min"] for r in rr})},
           "all_dips_positive": all(r["dips_positive"] for r in rr), "all_start_above_F": all(r["start_above_F"] for r in rr),
           "two_rays_not_All": sum(bool(r.get("ell") and r.get("u") and r.get("not_All")) for r in rr),
           "log10_deepest_rel_dip_range": [min((float(r["log10_deepest_rel_dip"]) for r in rr if r["log10_deepest_rel_dip"]), default=None),
                                           max((float(r["log10_deepest_rel_dip"]) for r in rr if r["log10_deepest_rel_dip"]), default=None)],
           "failures": [r for r in rr if not (r["n_min"] >= 1 and r["dips_positive"] and r.get("ell") and r.get("not_All"))][:10]}
    out["pass"] = bool(pre["zero"] and out["with_min"] == len(sets) and out["all_dips_positive"] and out["two_rays_not_All"] == len(sets))
    dump("H-12.A7", out)
    return out


# ============================================================================================================ H-12.A8
def H_12_A8():
    """Worked example of §6.5 (D1, G = 0.5, lam = 1, Sigma = 0.01, Pi = 1), recomputed by new code written from the thesis's §6.3
    formulas only (P+ = ((1-L)^2 q + L^2 r)/(1 - (1-L)^2 a^2), a^2 = e^{-2 lam dt}, q = F(1 - a^2), r = 1/(Pi dt),
    L = 1 - e^{-G dt}; avg = F - (F - P+) s/(2 lam dt)); derivatives by mpmath numerical differentiation; no Task 12 code.
    Precision: int(2 lam dt_max/ln 10) + 60 digits with dt_max the largest dt of the evaluation (here dt <= 1e3: 929 digits).
    Pass: every printed figure is reproduced at its printed digits: post(0+) = 0.09; post has exactly one turning point, a maximum
    0.20457 at dt = 2.4645, and post -> 0; avg crosses F once, at dt_E = 100 to 20 significant digits; avg has exactly one
    turning point after dt_E, a minimum 0.0099875 at dt = 200; the dip (F - min)/F is 0.125 %; avg < F after dt_E and -> F."""
    import mpmath as mp
    use("t16")
    import t16_checks as T16
    lam, Sig, Pi, G = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1), mp.mpf("0.5")
    dps = int(2 * 1 * 1000 / math.log(10)) + 60
    mp.mp.dps = dps if not DRY else 80
    F = Sig / lam

    def post(dt):
        a2 = mp.exp(-2 * lam * dt)
        q, r, L = F * (1 - a2), 1 / (Pi * dt), 1 - mp.exp(-G * dt)
        return ((1 - L)**2 * q + L**2 * r) / (1 - (1 - L)**2 * a2)

    def avg(dt):
        s = 1 - mp.exp(-2 * lam * dt)
        return F - (F - post(dt)) * s / (2 * lam * dt)

    def turns(f, lo, hi, n):
        xs = [lo + (hi - lo) * mp.mpf(i) / n for i in range(n + 1)]
        d = [mp.diff(lambda u: f(mp.power(10, u)), x0) for x0 in xs]
        out = []
        for i in range(n):
            if d[i] * d[i + 1] < 0:
                xr = mp.findroot(lambda u: mp.diff(lambda w: f(mp.power(10, w)), u), (xs[i], xs[i + 1]), solver="anderson")
                out.append(("max" if d[i] > 0 else "min", mp.power(10, xr)))
        return out
    n_grid = N(240, 40)
    tp = turns(post, mp.mpf(-4), mp.mpf(3), n_grid)
    p0 = post(mp.mpf("1e-30"))
    pend = [post(mp.power(10, k)) for k in (3, 4, 5, 6)]
    ok_post = (len(tp) == 1 and tp[0][0] == "max" and T16.printed_match("0.09", p0)
               and T16.printed_match("0.20457", post(tp[0][1])) and T16.printed_match("2.4645", tp[0][1])
               and all(pend[i + 1] < pend[i] for i in range(3)) and pend[-1] < mp.mpf("1e-5"))
    xs = [mp.mpf(-4) + mp.mpf(7) * i / n_grid for i in range(n_grid + 1)]
    sg = [mp.sign(avg(mp.power(10, x0)) - F) for x0 in xs]
    cr = [i for i in range(n_grid) if sg[i] * sg[i + 1] < 0]
    dtE = mp.power(10, mp.findroot(lambda u: avg(mp.power(10, u)) - F, (xs[cr[0]], xs[cr[0] + 1]), solver="anderson")) if cr else None
    ta = [t for t in turns(avg, mp.mpf(-4), mp.mpf(3), n_grid) if dtE is not None and t[1] > dtE]
    mn = avg(ta[0][1]) if ta else None
    after = [avg(mp.power(10, x0)) for x0 in xs if dtE is not None and mp.power(10, x0) > dtE]
    ok_avg = (len(cr) == 1 and abs(dtE / 100 - 1) < mp.mpf("5e-20") and len(ta) == 1 and ta[0][0] == "min"
              and T16.printed_match("0.0099875", mn) and T16.printed_match("200", ta[0][1])
              and T16.printed_match("0.125%", (F - mn) / F) and all(v < F for v in after)
              and F - avg(mp.mpf(10)**6) < F - mn)
    out = {"dps": mp.mp.dps, "post_0": mp.nstr(p0, 12), "post_turns": [(k, mp.nstr(t, 12), mp.nstr(post(t), 12)) for k, t in tp],
           "post_tail": [mp.nstr(v, 6) for v in pend], "avg_crossings": len(cr), "dt_E": mp.nstr(dtE, 30) if dtE else None,
           "avg_turns_after_dtE": [(k, mp.nstr(t, 12), mp.nstr(avg(t), 12)) for k, t in ta],
           "dip_percent": mp.nstr(100 * (F - mn) / F, 8) if mn else None, "post_ok": bool(ok_post), "avg_ok": bool(ok_avg)}
    out["pass"] = bool(ok_post and ok_avg)
    dump("H-12.A8", out)
    return out


# ============================================================================================================ H-13.A-sym
def H_13_A_sym():
    """The two Task 13 Part A items. A1 item 2: -sFr < 0 with s = 1 - e^{-2x}, r = k/x (x, F, k > 0): sign argument
    s = e^{-2x}(e^{2x} - 1) and e^y - 1 = sum_{j>=1} y^j/j! with positive coefficients; the rewrite must reduce to 0 and the
    series coefficients must be positive. A2 item 6: (1 - x s'/s)(2/s) - 1 - 2e^{-2x}(sinh 2x - 2x)/s^2 = 0 after .rewrite(exp).
    Denesting step: neither expression contains a square root (recorded). Fallback (seed 19006): 1,000 sets, x log-uniform on
    [1e-8, 50], F, k log-uniform on [1e-3, 1e3], at 60 + ceil(-2 log10 x) + ceil(4x/ln 10) digits; both identities to 1e-35 and
    -sFr < 0 at every set. Pass: all."""
    import mpmath as mp
    import sympy as sp
    T17 = _t17()
    x, F, k, y = sp.symbols("x F k y", positive=True)
    E2 = sp.exp(-2 * x)
    s = 1 - E2
    sp_ = sp.diff(s, x)
    r = k / x
    i2 = -s * F * r + (F * k / x) * E2 * (sp.exp(2 * x) - 1)
    z2 = T17.zero(i2)
    ser = sp.series(sp.exp(y) - 1, y, 0, 12).removeO()
    pos = all(ser.coeff(y, j) > 0 for j in range(1, 12)) and ser.coeff(y, 0) == 0
    e6 = (1 - x * sp_ / s) * (2 / s) - 1 - 2 * E2 * (sp.sinh(2 * x) - 2 * x) / s**2
    z6 = T17.zero(e6.rewrite(sp.exp))
    nsqrt = sum(1 for p in list(i2.atoms(sp.Pow)) + list(e6.atoms(sp.Pow)) if p.exp == sp.S.Half)
    rng = random.Random(19006)
    worst2, worst6, neg_fail, maxd = mp.mpf(0), mp.mpf(0), 0, 0
    f2 = sp.lambdify((x, F, k), -s * F * r, "mpmath")
    g2 = sp.lambdify((x, F, k), -(F * k / x) * E2 * (sp.exp(2 * x) - 1), "mpmath")
    l6 = sp.lambdify(x, (1 - x * sp_ / s) * (2 / s), "mpmath")
    r6 = sp.lambdify(x, 1 + 2 * E2 * (sp.sinh(2 * x) - 2 * x) / s**2, "mpmath")
    for _ in range(N(1000, 20)):
        xv = 10 ** rng.uniform(-8, math.log10(50))
        Fv, kv = 10 ** rng.uniform(-3, 3), 10 ** rng.uniform(-3, 3)
        d = 60 + math.ceil(-2 * math.log10(xv)) + math.ceil(4 * xv / math.log(10))
        maxd = max(maxd, d)
        with mp.workdps(d):
            X, Fm, Km = mp.mpf(xv), mp.mpf(Fv), mp.mpf(kv)
            a_, b_ = f2(X, Fm, Km), g2(X, Fm, Km)
            worst2 = max(worst2, abs(a_ - b_) / abs(b_))
            neg_fail += int(not a_ < 0)
            a6, b6 = l6(X), r6(X)
            worst6 = max(worst6, abs(a6 - b6) / abs(b6))
    out = {"A1_item2_rewrite": z2, "exp_series_positive": bool(pos), "A2_item6_rewrite_exp": z6, "square_roots_present": nsqrt,
           "fallback": {"seed": 19006, "n": N(1000, 20), "max_digits": maxd, "item2_max_rel": float(worst2), "item6_max_rel": float(worst6),
                        "negativity_failures": neg_fail}}
    out["pass"] = bool(z2["zero"] and pos and z6["zero"] and worst2 < mp.mpf("1e-35") and worst6 < mp.mpf("1e-35") and neg_fail == 0)
    dump("H-13.A-sym", out)
    return out


# ============================================================================================================ H-13.A2
def _h13a2(i):
    import mpmath as mp
    use("t13")
    import t13_partA_numeric as NUM
    r = NUM.a12_job(13001 * 100000 + i)
    xv = r["x"]
    extra = int(mp.ceil(2 * xv / mp.log(10))) + 30
    with mp.workdps(100 + extra):
        lam, Sig, Pi = r["lam"], r["Sig"], r["Pi"]
        F, k = Sig / lam, lam / Pi
        rr = k / xv
        s = -mp.expm1(-2 * xv)
        b = s * (rr - F)
        disc = mp.sqrt(b**2 + 4 * s * F * rr)
        M = 2 * s * F * rr / (b + disc) if b > 0 else (-b + disc) / 2
        phi = F * Pi * xv / lam
        ps = phi / s
        d2 = mp.sqrt((1 - phi)**2 + 4 * ps)
        mu = 2 * ps / ((1 - phi) + d2) if phi <= 1 else ((phi - 1) + d2) / 2
        Q = mu * s / ((1 + mu) * xv)
        rel = abs((F - F / 2 * Q) / (F - (F - M) * mp.expm1(2 * xv) / (2 * xv)) - 1)
    return {"i": i, "x": float(xv), "digits": 100 + extra, "link_fails": [f for f in r["fails"] if f != "Pbar(mu) = Pbar(M)"],
            "cross_rel": float(rel) if rel > 0 else 0.0, "cross_ok": bool(rel < mp.mpf("1e-80"))}


def H_13_A2():
    """Task 13 A2 numerical, all 10,000 A1 sets (seeds 13001*100000 + i, t13_partA_numeric.a12_job unchanged for the
    pre-registered links at 100 digits), with the auxiliary cross-check Pbar(mu) = Pbar(M) recomputed at 100 + ceil(2x/ln 10) + 30
    digits (the cancellation in F - M costs about 2x/ln 10 digits). Pass: 0 link failures and the cross-check within 1e-80 in
    every set."""
    from multiprocessing import Pool
    with Pool(4) as pool:
        rr = pool.map(_h13a2, range(N(10000, 40)), chunksize=50)
    out = {"sets": len(rr), "link_failures": sum(len(r["link_fails"]) for r in rr), "cross_failures": sum(not r["cross_ok"] for r in rr),
           "max_cross_rel": max(r["cross_rel"] for r in rr), "max_digits": max(r["digits"] for r in rr),
           "examples": [r for r in rr if r["link_fails"] or not r["cross_ok"]][:10]}
    out["pass"] = out["link_failures"] == 0 and out["cross_failures"] == 0
    dump("H-13.A2", out)
    return out


# ============================================================================================================ H-13.C2-12
EQ2 = "1e-300"


def _route_ii_tol(A, R2, tol):
    """Route (ii) of t10/classify.py (mp branch), with the equality tolerance as a parameter; otherwise line for line."""
    import mpmath as mp
    use("t10")
    from classify import _eq, _cls
    from t10_common import WIDTH, T
    c = A["curve"]
    turns, bounds = A["turns"], A["bounds"]
    f = lambda x: c.f(T(x))  # noqa: E731
    eq = lambda a, b: _eq(a, b, tol)  # noqa: E731
    pos = lambda v: v - R2 > tol * R2  # noqa: E731
    vals = [A["L_minus"]] + [t["value"] for t in turns] + [A["L_plus"]]
    splits = []
    for j in range(len(bounds) - 1):
        a, b = vals[j], vals[j + 1]
        ga = 0 if eq(a, R2) else (1 if a > R2 else -1)
        gb = 0 if eq(b, R2) else (1 if b > R2 else -1)
        if ga * gb < 0:
            lo, hi = bounds[j], bounds[j + 1]
            fa = ga
            while hi - lo > WIDTH:
                m = (lo + hi) / 2
                v = f(m) - R2
                if (v > 0) == (fa > 0):
                    lo = m
                else:
                    hi = m
            splits.append((lo + hi) / 2)
    for t in turns:
        if eq(t["value"], R2):
            splits.append(t["x"])
    splits = sorted(splits)
    xs = [c.shift] if not splits else [splits[0] - 1] + [(splits[i] + splits[i + 1]) / 2 for i in range(len(splits) - 1)] + [splits[-1] + 1]
    inside = [pos(f(x)) for x in xs]
    edges = [None] + splits + [None]
    comps = [(edges[i] is None, edges[i + 1] is None) for i, ins in enumerate(inside) if ins]
    return _cls(comps, len(inside) == 1 and inside[0])


def _h1312_job(args):
    import mpmath as mp
    use("t13", "t10")
    import t13_audit_classes as AC
    from classify import EQ, name, route_i, route_ii
    row, i, p, seed = args
    import numpy as np
    rng = np.random.default_rng(seed)
    allowed = AC.ROWS[row][1]
    A = AC.analyse_row(row, p)
    R2s, _ = AC.tolerances(A, rng)
    has_fl = A["curve"].ffl is not None
    counts, flagged, persist = {}, 0, []
    for R2 in R2s:
        ci = route_i(A, R2, EQ)
        if has_fl:
            try:
                cii, _ = route_ii(A, R2, prec="fl")
            except Exception as e:  # noqa: BLE001
                cii = f"float error: {type(e).__name__}"
        else:
            cii, _ = route_ii(A, R2, prec="mp")
        if ci != cii or ci not in allowed or cii not in allowed:
            flagged += 1
            tol = mp.mpf(EQ2)
            with mp.workdps(400):
                ci2 = route_i(A, R2, tol)
                cii2 = _route_ii_tol(A, R2, tol)
            if ci2 != cii2 or ci2 not in allowed:
                persist.append({"i": i, "R2": mp.nstr(R2, 25), "route_i": name(ci2), "route_ii": name(cii2)})
            ci = ci2
        counts[name(ci)] = counts.get(name(ci), 0) + 1
    return {"i": i, "counts": counts, "flagged": flagged, "persist": persist}


def H_13_C2_12():
    """Task 13 C2 row 12 (Pi0 sweep of the tanh, exponential and Hill-type gains, sets and tolerances exactly as pre-registered,
    seed 13100 + 12, t13_audit_classes unchanged for the draws, analysis and first pass), with every flagged case re-run at 400
    digits with an equality tolerance of 1e-300 relative in both routes (route (ii) re-implemented line for line with the tolerance
    as a parameter), below the scale of the exponentially flat approach to the exact limit (the T13 diagnosis measured gaps up to
    2.49e-41 at the route (ii) sample point). Pass (C2 per-row rule): 0 persisting classes outside the stated set, 0 persisting
    route disagreements, and every stated class observed."""
    from multiprocessing import Pool
    import numpy as np
    use("t13", "t10")
    import t13_audit_classes as AC
    rng = np.random.default_rng(13100 + 12)
    jobs = []
    for i in range(1000):
        p = AC.draw(12, rng, i)
        jobs.append((12, i, p, int(rng.integers(2**63))))
    jobs = jobs[:N(1000, 8)]
    with Pool(4) as pool:
        rr = pool.map(_h1312_job, jobs, chunksize=5)
    cnt = {}
    for r in rr:
        for k, v in r["counts"].items():
            cnt[k] = cnt.get(k, 0) + v
    stated = AC.ROWS[12][1]
    use("t10")
    from classify import name
    missing = [name(c) for c in stated if name(c) not in cnt]
    out = {"sets": len(rr), "classes": cnt, "flagged": sum(r["flagged"] for r in rr), "persisting": sum(len(r["persist"]) for r in rr),
           "persist_examples": [x for r in rr for x in r["persist"]][:10], "stated": [name(c) for c in stated], "missing_stated": missing,
           "equality_tolerance": EQ2, "dps": 400}
    out["pass"] = out["persisting"] == 0 and (not missing or DRY)
    dump("H-13.C2-12", out)
    return out


# ============================================================================================================ H-14.C4
T14_ARTIFACTS = "45b0058"


def H_14_C4():
    """T14 C4 with the type change accepted in Task 15 as an allowed difference: at the Task 14 artifacts commit (45b0058, a clean
    worktree), the v1-number render of the source is compared with archive/Stages_0_4_Consolidated_v1.md exactly as t14_checks.c4
    does (its code, unchanged, run in that worktree); hunks are then re-categorised: (a) numbering (t14_checks' own numbering
    check), (b) the split, (c) rows 25-26, (d) the excess identity's type: a hunk whose new lines equal its old lines after
    replacing "Corollary" by "Proposition" where the line names the excess identity (its heading, label line, section-12 row,
    number-map row, or a reference "Corollary 4"). Pass: 0 numbering mismatches and no hunk outside (a)-(d)."""
    import difflib
    import shutil
    wt = os.path.join(os.environ.get("T19_SCRATCH", "/tmp/claude-0/t19"), "wt_t14")
    if os.path.exists(wt):
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO, capture_output=True)
        shutil.rmtree(wt, ignore_errors=True)
    os.makedirs(os.path.dirname(wt), exist_ok=True)
    subprocess.run(["git", "worktree", "add", "--detach", wt, T14_ARTIFACTS], cwd=REPO, check=True, capture_output=True)
    try:
        code = ("import sys, json; sys.path.insert(0, 't14'); import t14_checks as C; r = C.c4(); "
                "print(json.dumps({'numbering_mismatches': r['numbering_mismatches'], 'hunks': r['hunks'], 'by_category': r['by_category']}, default=str))")
        pr = subprocess.run([sys.executable, "-c", code], cwd=os.path.join(wt, "classification"), capture_output=True, text=True)
        base = json.loads(pr.stdout.strip().split("\n")[-1])
        a = open(os.path.join(wt, "classification", "archive", "Stages_0_4_Consolidated_v1.md")).read().split("\n")
        b = open(os.path.join(wt, "classification", "t14", "results", "scratch", "v1check.md")).read().split("\n")
        cats, other = {}, []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag == "equal":
                continue
            old, new = a[i1:i2], b[j1:j2]
            txt = "\n".join(old + new)
            if re.search(r"^\| 2[56] \| \$\\Delta t\$", txt, re.M) and all(re.match(r"^\| 2[56] \|", l) for l in old + new):
                cat = "c (rows 25-26)"
            elif "6+" in txt or "addendum" in txt or (170 <= i1 + 1 <= 186):
                cat = "b (split)"
            elif len(old) == len(new) and all(o == n.replace("Corollary", "Proposition") for o, n in zip(old, new)) and \
                    any(re.search(r"Corollary 4\b|excess", n, re.I) for n in new):
                cat = "d (excess identity type)"
            else:
                cat = "other"
                other.append({"v1_lines": f"{i1 + 1}-{i2}", "old": old[:4], "new": new[:4]})
            cats[cat] = cats.get(cat, 0) + 1
        out = {"commit": T14_ARTIFACTS, "t14_c4_as_run": base, "categories": cats, "other_hunks": other}
        out["pass"] = not base["numbering_mismatches"] and not other
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", wt], cwd=REPO, capture_output=True)
    dump("H-14.C4", out)
    return out


# ============================================================================================================ H-14.C10
def H_14_C10():
    """T14 C10 with a resolver that builds each literal the way its script builds it: Task 15's c13 (t15/t15_checks.py, unchanged),
    run on the current reproduce_all.sh and scripts. Pass: 0 unresolved paths."""
    use("t15", "register")
    import t15_checks as T15
    r = T15.c13()
    out = {"result": r, "pass": bool(r.get("pass"))}
    dump("H-14.C10", out)
    return out


# ============================================================================================================ H-16.D1
def H_16_D1():
    """T16 D1 items 2(b) and 9 as the thesis states them (Proposition 3.5's proof and Lemma 3.6; Corollary 5.2).
    2(b): d sigma^2/dG = (G^2 + 2 lam G - 2 Sigma Pi)/(2 Pi (lam + G)^2) (identity); the numerator's roots have product
    -2 Sigma Pi < 0, so exactly one is positive; it is G* = -lam + sqrt(lam^2 + 2 Sigma Pi) (identity), and G* > 0 because the
    radicand minus lam^2 is 2 Sigma Pi > 0 and sqrt(lam^2) = lam (denesting, lam > 0). Numerical: 1,000 sets (seed 19007): the
    numerator has exactly one positive real root, equal to G* to 1e-40 relative, at 60 digits.
    9: sigma*^2(pi_R) = R^2, pi_R = 2 lam (F - R^2)/R^4, with Sigma = lam (R^2 + d), d > 0 (exactly R^2 < F): the radicand
    R^4 + 4d(R^2 + d) = (R^2 + 2d)^2 and R^2 + 2d > 0, so the root denests to R^2 + 2d; residual 0. Fallback (seed 19008).
    Pass: every part holds."""
    import mpmath as mp
    import sympy as sp
    T17 = _t17()
    lam, Sig, Pi, G, R2, d = sp.symbols("lambda Sigma Pi G R2 d", positive=True)
    s2 = (Sig + G**2 / (2 * Pi)) / (lam + G)
    i_der = T17.zero(sp.diff(s2, G) - (G**2 + 2 * lam * G - 2 * Sig * Pi) / (2 * Pi * (lam + G)**2))
    Gs = -lam + sp.sqrt(lam**2 + 2 * Sig * Pi)
    i_root = T17.zero((G**2 + 2 * lam * G - 2 * Sig * Pi).subs(G, Gs))
    prod = sp.Poly(G**2 + 2 * lam * G - 2 * Sig * Pi, G).all_coeffs()
    prod_roots = sp.simplify(prod[2] / prod[0])
    prod_neg = bool((-prod_roots).is_positive)
    rad_minus = sp.simplify((lam**2 + 2 * Sig * Pi) - lam**2)
    gpos = bool(rad_minus.is_positive) and sp.sqrt(lam**2) == lam
    rng = random.Random(19007)
    nbad = 0
    mp.mp.dps = 60
    for _ in range(N(1000, 20)):
        l_, S_, P_ = (mp.mpf(_lu(rng)) for _ in range(3))
        roots = mp.polyroots([1, 2 * l_, -2 * S_ * P_], extraprec=100)
        posr = [r_ for r_ in roots if abs(mp.im(r_)) < mp.mpf("1e-50") and mp.re(r_) > 0]
        gs = -l_ + mp.sqrt(l_**2 + 2 * S_ * P_)
        if len(posr) != 1 or abs(mp.re(posr[0]) / gs - 1) > mp.mpf("1e-40"):
            nbad += 1
    item2 = {"derivative_identity": i_der, "G_star_root": i_root, "product_of_roots": str(prod_roots), "product_negative": prod_neg,
             "radicand_minus_lam2": str(rad_minus), "G_star_positive": gpos, "numeric": {"seed": 19007, "n": N(1000, 20), "failures": nbad}}
    item2["holds"] = bool(i_der["zero"] and i_root["zero"] and prod_neg and gpos and nbad == 0)
    Sg = lam * (R2 + d)
    F = Sg / lam
    piR = 2 * lam * (F - R2) / R2**2
    sstar = 2 * Sg / (lam + sp.sqrt(lam**2 + 2 * Sg * piR))
    e = sp.simplify(sstar - R2)
    rads = [p for p in e.atoms(sp.Pow) if p.exp == sp.S.Half]
    Y = R2 + 2 * d
    rep, info = {}, []
    for r_ in rads:
        num, den = sp.fraction(sp.together(sp.factor(r_.base)))
        # the radicand, possibly times lam^2/R2^4: compare with Y^2 times that factor
        ratio = sp.simplify(r_.base / Y**2)
        okr = ratio.is_positive and all(sp.sqrt(ratio).is_positive for _ in [0])
        cand = sp.sqrt(ratio) * Y
        cand = sp.powdenest(sp.simplify(cand), force=False)
        info.append({"radicand": str(sp.factor(r_.base)), "ratio_to_Y2": str(ratio), "replacement": str(cand)})
        if okr and sp.simplify(cand**2 - r_.base) == 0 and cand.is_positive:
            rep[r_] = cand
    z9 = T17.zero(e.subs(rep)) if rep else {"zero": False}

    def samp(r):
        return [_lu(r), _lu(r), _lu(r)]
    fb = _fallback(sstar, R2, (lam, R2, d), samp, 19008, lambda v: 60)
    item9 = {"radicands": info, "Y": str(Y), "Y_positive": bool(Y.is_positive), "residual_after_denesting": z9, "fallback": fb}
    item9["holds"] = bool(rep and Y.is_positive and z9["zero"] and fb["pass"])
    out = {"item_2b": item2, "item_9": item9, "pass": item2["holds"] and item9["holds"]}
    dump("H-16.D1", out)
    return out


# ============================================================================================================ H-16.D2
def H_16_D2():
    """Extraction for the manual reading of Propositions 3.1 and 3.5: the thesis render's statements (Stages_0_4_Thesis.md, now the
    Task 17 thesis-only imports) side by side with the draft's (t19/input/Thesis_Draft_full.md), from the bold label to the proof or
    the next heading or result. The verdict is computed after the run from t19/results/h16d2_classification.yaml (kinds a-d)."""
    def stmt(L, label):
        i = next(k for k, l in enumerate(L) if l.startswith(label))
        j = next(k for k in range(i + 1, len(L)) if L[k].startswith(("*Proof", "**", "#")))
        return "\n".join(L[i:j]).strip()
    th = open(os.path.join(CLS, "Stages_0_4_Thesis.md")).read().split("\n")
    dr = open(os.path.join(HERE, "input", "Thesis_Draft_full.md")).read().split("\n")
    pairs = {}
    for no in ("3.1", "3.5"):
        pairs[no] = {"draft": stmt(dr, f"**Proposition {no}"), "render": stmt(th, f"**Proposition {no}")}
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "dry" if DRY else "", "h16d2_pairs.md") if DRY else os.path.join(HERE, "results", "h16d2_pairs.md"), "w") as fh:
        for no, p in pairs.items():
            fh.write(f"## Proposition {no}\n\n### Draft\n\n{p['draft']}\n\n### Thesis render\n\n{p['render']}\n\n")
    out = {"pairs": pairs, "identical_after_strip": {no: _norm(p["draft"]) == _norm(p["render"]) for no, p in pairs.items()},
           "note": "verdict from the manual classification (kinds a-d); pass iff no kind (c) or (d)"}
    dump("H-16.D2", out)
    return out


def _norm(s):
    import html
    s = html.unescape(s).replace("\\", "").replace("`", "").replace("*", "")
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


IDS = {"H-6.C5": H_6_C5, "H-9.2": H_9_2, "H-9.5": H_9_5, "H-10.1a": H_10_1a, "H-10.1b": H_10_1b, "H-10.5": H_10_5,
       "H-10.6": H_10_6, "H-11.3": H_11_3, "H-12.A5": H_12_A5, "H-12.A7": H_12_A7, "H-12.A8": H_12_A8, "H-13.A-sym": H_13_A_sym,
       "H-13.A2": H_13_A2, "H-13.C2-12": H_13_C2_12, "H-14.C4": H_14_C4, "H-14.C10": H_14_C10, "H-16.D1": H_16_D1, "H-16.D2": H_16_D2}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if os.environ.get("T19_ONE"):
        k = os.environ["T19_ONE"]
        t0 = time.time()
        r = IDS[k]()
        print(json.dumps({"id": k, "pass": r.get("pass"), "seconds": round(time.time() - t0, 1)}))
        return
    ids = args or list(IDS)
    summary = {}
    for k in ids:
        t0 = time.time()
        env = dict(os.environ, T19_ONE=k)
        pr = subprocess.run([sys.executable, os.path.abspath(__file__)] + (["--dry"] if DRY else []), env=env, capture_output=True,
                            text=True, cwd=HERE)
        last = pr.stdout.strip().split("\n")[-1] if pr.stdout.strip() else ""
        try:
            summary[k] = json.loads(last)
        except json.JSONDecodeError:
            summary[k] = {"id": k, "error": (pr.stderr or pr.stdout)[-3000:], "seconds": round(time.time() - t0, 1)}
        summary[k]["wall_seconds"] = round(time.time() - t0, 1)
        print(k, summary[k].get("pass"), summary[k].get("wall_seconds"), "ERROR" if "error" in summary[k] else "", flush=True)
        os.makedirs(RES, exist_ok=True)
        old = json.load(open(os.path.join(RES, "summary.json"))) if os.path.exists(os.path.join(RES, "summary.json")) else {}
        old.update({k: summary[k]})
        json.dump(old, open(os.path.join(RES, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
