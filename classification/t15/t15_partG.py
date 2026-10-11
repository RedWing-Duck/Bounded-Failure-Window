"""Task 15 Part G (PREREG_t15.md checks C11, C12), with the existing classifier: t11_common.analyse_with_limits (T10 turning-point
method on x = log10 theta) and t10/classify.py routes (i) and (ii).
C11 Corollary 2.8 (reparameterisation): 1,000 curves sigma^2 = P(tanh x), x = log10 theta; one map phi per curve,
  x = psi(x'), psi smooth (a x + b sin x) or piecewise linear, increasing or decreasing (250 each). >= 50 tolerances per curve.
C12 Proposition 2.9 (structural stability): 500 curves x 2 tolerances; N_i, eta exactly as stated; perturbations with
  sup|delta| < eta and sigma~^2 strictly monotone on each N_i; class compared. Plus one illustration violating only condition 2.
Usage: python3 t15_partG.py [C11|C12|ILL ...] [--n N]"""
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(CLS, "t10"), os.path.join(CLS, "t11")]
from classify import EQ, name, route_i, route_ii  # noqa: E402
from t10_common import ZREL, Curve  # noqa: E402
from t11_common import analyse_with_limits  # noqa: E402

XM, XP = mp.mpf(-80), mp.mpf(80)
LN10 = mp.log(10)


# ---------------------------------------------------------------- curves
def draw_poly(rng):
    while True:
        deg = int(rng.integers(6, 10))
        c = rng.standard_normal(deg + 1)
        s = np.linspace(-1, 1, 4001)
        v = np.polyval(c, s)
        c[-1] += -v.min() + 0.5 + rng.uniform(0, 1)          # P > 0 on [-1, 1]
        d1 = np.polyder(c)
        r = [z.real for z in np.roots(d1) if abs(z.imag) < 1e-9 and -1 < z.real < 1]
        d2 = np.polyder(d1)
        if r and all(abs(np.polyval(d2, z)) > 1e-6 for z in r):   # stationary points are all turning points
            return [float(x) for x in c]


def draw_cheb(rng):
    """EXPLORATORY (not pre-registered): degree 9-12 Chebyshev series, for curves with more turning points."""
    while True:
        deg = int(rng.integers(9, 13))
        a = rng.standard_normal(deg + 1)
        c = np.polynomial.chebyshev.cheb2poly(a)[::-1]
        s = np.linspace(-1, 1, 4001)
        v = np.polyval(c, s)
        c[-1] += -v.min() + 0.5 + rng.uniform(0, 1)
        d1 = np.polyder(c)
        r = [z.real for z in np.roots(d1) if abs(z.imag) < 1e-9 and -1 < z.real < 1]
        d2 = np.polyder(d1)
        if r and all(abs(np.polyval(d2, z)) > 1e-6 for z in r):
            return [float(x) for x in c]


def pval(c, s):
    v = mp.mpf(0)
    for a in c:
        v = v * s + a
    return v


def pder(c, s):
    n = len(c) - 1
    v = mp.mpf(0)
    for i, a in enumerate(c[:-1]):
        v = v * s + (n - i) * a
    return v


def base_curve(c):
    cm = [mp.mpf(x) for x in c]
    scale = sum(abs(x) for x in cm)
    f = lambda th: pval(cm, mp.tanh(mp.log10(th)))
    d = lambda th: pder(cm, mp.tanh(mp.log10(th)))            # sign of d sigma^2 / d theta
    return Curve(f, d, lambda th: ZREL * scale, 0, [], None, "P(tanh x)"), pval(cm, -1), pval(cm, 1)


# ---------------------------------------------------------------- reparameterisations psi (x' -> x)
def draw_psi(rng, kind):
    if kind.startswith("smooth"):
        a = rng.uniform(0.5, 2.0)
        b = rng.uniform(-0.9, 0.9) * a
        off = rng.uniform(-1, 1)
        psi = lambda x: a * x + b * mp.sin(x) + off
        dpsi = lambda x: a + b * mp.cos(x)
        kinks = []
        desc = {"a": a, "b": b, "off": off}
    else:
        m = int(rng.integers(3, 7))
        kinks = sorted(rng.uniform(-3, 3, m))
        slopes = rng.uniform(0.5, 2.0, m + 1)
        off = rng.uniform(-1, 1)
        K = [mp.mpf(k) for k in kinks]
        S = [mp.mpf(s) for s in slopes]          # S[j] is the slope after j kinks
        V = [mp.mpf(off)]                        # psi at each kink, anchored at the first
        for j in range(1, m):
            V.append(V[-1] + S[j] * (K[j] - K[j - 1]))

        def psi(x):
            j = sum(1 for kk in K if kk <= x)
            return V[0] + S[0] * (x - K[0]) if j == 0 else V[j - 1] + S[j] * (x - K[j - 1])

        def dpsi(x):
            return S[sum(1 for kk in K if kk <= x)]
        desc = {"kinks": [float(k) for k in kinks], "slopes": [float(s) for s in slopes], "off": off}
    sign = -1 if kind.endswith("dec") else 1
    return (lambda x: sign * psi(x)), (lambda x: sign * dpsi(x)), [float(k) for k in kinks], desc


def composite(c, psi, dpsi, kinks, dec):
    cm = [mp.mpf(x) for x in c]
    scale = sum(abs(x) for x in cm)
    f = lambda th: pval(cm, mp.tanh(psi(mp.log10(th))))
    d = lambda th: pder(cm, mp.tanh(psi(mp.log10(th)))) * dpsi(mp.log10(th))
    Lm, Lp = pval(cm, -1), pval(cm, 1)
    if dec:
        Lm, Lp = Lp, Lm
    return Curve(f, d, lambda th: ZREL * scale * 4, 0, kinks, None, "composite"), Lm, Lp


def transform(cls, dec):
    if not dec or cls == "All":
        return cls
    return (cls[1], cls[0], cls[2])


def tolerances(A, rng):
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]] if mp.isfinite(v) and v > 0]
    out = list(crit) + [v * (1 + s * mp.mpf("1e-6")) for v in crit for s in (-1, 1)]
    lo, hi = float(mp.log10(min(crit) / 2)), float(mp.log10(2 * max(crit)))
    while len(out) < 50:
        out.append(mp.power(10, mp.mpf(float(rng.uniform(lo, hi)))))
    return out, len(crit)


def c11_job(args):
    i, c, kind, seed = args
    rng = np.random.default_rng(seed)
    cur, Lm, Lp = base_curve(c)
    A = analyse_with_limits(cur, Lm, Lp, XM, XP)
    psi, dpsi, kinks, desc = draw_psi(rng, kind)
    dec = kind.endswith("dec")
    cc, Lm2, Lp2 = composite(c, psi, dpsi, kinks, dec)
    B = analyse_with_limits(cc, Lm2, Lp2, XM, XP)
    R2s, ncrit = tolerances(A, rng)
    cls_mis, route_dis, exs = 0, 0, []
    for R2 in R2s:
        for r in ("i", "ii"):
            a = route_i(A, R2, EQ) if r == "i" else route_ii(A, R2, prec="mp")[0]
            b = route_i(B, R2, EQ) if r == "i" else route_ii(B, R2, prec="mp")[0]
            if b != transform(a, dec):
                cls_mis += 1
                if len(exs) < 3:
                    exs.append({"R2": mp.nstr(R2, 20), "route": r, "orig": name(a), "reparam": name(b)})
        if route_i(A, R2, EQ) != route_ii(A, R2, prec="mp")[0] or route_i(B, R2, EQ) != route_ii(B, R2, prec="mp")[0]:
            route_dis += 1
    va = [t["value"] for t in A["turns"]]
    vb = [t["value"] for t in B["turns"]]
    if dec:
        vb = vb[::-1]
    sig_ok = len(va) == len(vb) and all(abs(x - y) <= mp.mpf("1e-25") * abs(x) for x, y in zip(va, vb))
    if dec:
        dir_ok = (B["approach_minus"], B["approach_plus"]) == (A["approach_plus"], A["approach_minus"])
    else:
        dir_ok = (B["approach_minus"], B["approach_plus"]) == (A["approach_minus"], A["approach_plus"])
    return {"i": i, "kind": kind, "n_turns": len(va), "n_tol": len(R2s), "n_crit": ncrit, "class_mismatches": cls_mis,
            "signature_ok": bool(sig_ok and dir_ok), "route_disagreements": route_dis, "examples": exs, "psi": desc}


def run_c11(n, cheb=False):
    rng = np.random.default_rng(15301 if cheb else 15001)
    rng2 = np.random.default_rng(15302 if cheb else 15002)
    kinds = ["smooth-inc", "pl-inc", "smooth-dec", "pl-dec"]
    jobs = [(i, (draw_cheb if cheb else draw_poly)(rng), kinds[i % 4], int(rng2.integers(2**63))) for i in range(n)]
    t0 = time.time()
    with Pool(4) as p:
        res = p.map(c11_job, jobs, chunksize=4)
    out = {"curves": len(res), "tolerances": sum(r["n_tol"] for r in res), "classifications": 4 * sum(r["n_tol"] for r in res),
           "by_kind": {k: sum(r["kind"] == k for r in res) for k in kinds},
           "turning_points_hist": {str(k): sum(r["n_turns"] == k for r in res) for k in sorted({r["n_turns"] for r in res})},
           "class_mismatches": sum(r["class_mismatches"] for r in res), "signature_mismatches": sum(not r["signature_ok"] for r in res),
           "route_disagreements": sum(r["route_disagreements"] for r in res),
           "examples": [e for r in res for e in r["examples"]][:10] + [r for r in res if not r["signature_ok"]][:5],
           "min_tolerances_per_curve": min(r["n_tol"] for r in res), "seconds": time.time() - t0}
    out["pass"] = out["class_mismatches"] == 0 and out["signature_mismatches"] == 0
    return out


# ---------------------------------------------------------------- C12
def bump(x):
    u = x / 20
    return mp.e * mp.exp(-1 / (1 - u * u)) if abs(u) < 1 else mp.mpf(0)


def dbump(x):
    u = x / 20
    if abs(u) >= 1:
        return mp.mpf(0)
    return bump(x) * (-2 * u / (1 - u * u)**2) / 20


def setup_case(c, R2, rng, A):
    """Crossings, neighbourhoods N_i and the exact margin eta (Proposition 2.9)."""
    cm = [mp.mpf(x) for x in c]
    g = lambda x: pval(cm, mp.tanh(x)) - R2
    tx = [t["x"] for t in A["turns"]]
    edges = [mp.mpf(-25)] + tx + [mp.mpf(25)]
    cross = []
    for a, b in zip(edges[:-1], edges[1:]):
        ga, gb = g(a), g(b)
        if ga * gb < 0:
            cross.append(mp.findroot(g, (a, b), solver="bisect", tol=mp.mpf("1e-40")))
    N = []
    for j, x in enumerate(cross):
        lim = min([abs(x - t) for t in tx] + [mp.mpf(25) - abs(x)] +
                  [abs(x - y) / 2 for k, y in enumerate(cross) if k != j])
        h = lim * mp.mpf(float(rng.uniform(0.1, 0.9)))
        N.append((x - h, x + h))
    vals = [abs(t["value"] - R2) for t in A["turns"]] + [abs(A["L_minus"] - R2), abs(A["L_plus"] - R2)]
    vals += [abs(g(e)) for n in N for e in n]
    return cross, N, min(vals)


def clock(N):
    def cx(x):
        v = x
        for a, b in N:
            v -= max(mp.mpf(0), min(x, b) - a)
        return v

    def dcx(x):
        return mp.mpf(0) if any(a <= x <= b for a, b in N) else mp.mpf(1)
    return cx, dcx


def perturbed(c, delta, ddelta, breaks):
    cm = [mp.mpf(x) for x in c]
    scale = sum(abs(x) for x in cm)
    f = lambda th: pval(cm, mp.tanh(mp.log10(th))) + delta(mp.log10(th))
    def d(th):
        x = mp.log10(th)
        return pder(cm, mp.tanh(x)) / mp.cosh(x)**2 + ddelta(x)
    return Curve(f, d, lambda th: ZREL * scale * 10, 0, breaks, None, "perturbed"), pval(cm, -1), pval(cm, 1)


def monotone_ok(c, N, ddelta):
    cm = [mp.mpf(x) for x in c]
    for a, b in N:
        xs = [a + (b - a) * k / 1999 for k in range(2000)]
        sg = [mp.sign(pder(cm, mp.tanh(x)) / mp.cosh(x)**2 + ddelta(x)) for x in xs]
        if any(s == 0 for s in sg) or len(set(sg)) != 1:
            return False
    return True


def c12_job(args):
    i, c, kind, seed = args
    rng = np.random.default_rng(seed)
    cur, Lm, Lp = base_curve(c)
    A = analyse_with_limits(cur, Lm, Lp, XM, XP)
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]]]
    lo, hi = float(mp.log10(min(crit))), float(mp.log10(max(crit)))
    out = []
    for rep in range(2):
        while True:
            R2 = mp.power(10, mp.mpf(float(rng.uniform(lo, hi))))
            if all(abs(R2 - v) > mp.mpf("1e-6") * v for v in crit):
                break
        cross, N, eta = setup_case(c, R2, rng, A)
        k = kind if rep == 0 else ("b" if kind == "a" else "a")
        for attempt in range(200):
            Aamp = eta * mp.mpf(float(rng.uniform(0.05, 0.95)))
            if k == "a":
                om, ph = rng.uniform(0.5, 3), rng.uniform(0, 2 * math.pi)
                cx, dcx = clock(N)
                delta = lambda x, cx=cx, om=om, ph=ph, Aamp=Aamp: Aamp * bump(cx(x)) * mp.sin(om * cx(x) + ph)
                ddelta = lambda x, cx=cx, dcx=dcx, om=om, ph=ph, Aamp=Aamp: Aamp * dcx(x) * (
                    dbump(cx(x)) * mp.sin(om * cx(x) + ph) + bump(cx(x)) * om * mp.cos(om * cx(x) + ph))
                ok = True
            else:
                m = int(rng.integers(2, 5))
                a_ = rng.standard_normal(m)
                om_ = rng.uniform(0.3, 3, m)
                ph_ = rng.uniform(0, 2 * math.pi, m)
                norm = float(np.sum(np.abs(a_)))
                delta = lambda x, a_=a_, om_=om_, ph_=ph_, norm=norm, Aamp=Aamp: Aamp * bump(x) * sum(
                    mp.mpf(float(a)) * mp.sin(mp.mpf(float(o)) * x + mp.mpf(float(p))) for a, o, p in zip(a_, om_, ph_)) / norm
                ddelta = lambda x, a_=a_, om_=om_, ph_=ph_, norm=norm, Aamp=Aamp: Aamp * (dbump(x) * sum(
                    mp.mpf(float(a)) * mp.sin(mp.mpf(float(o)) * x + mp.mpf(float(p))) for a, o, p in zip(a_, om_, ph_)) + bump(x) * sum(
                    mp.mpf(float(a * o)) * mp.cos(mp.mpf(float(o)) * x + mp.mpf(float(p))) for a, o, p in zip(a_, om_, ph_))) / norm
                ok = monotone_ok(c, N, ddelta)
            if ok:
                break
        else:
            out.append({"i": i, "rep": rep, "kind": k, "skipped": "no admissible perturbation in 200 draws"})
            continue
        breaks = [float(e) for n in N for e in n] + [-20.0, 20.0]
        pc, Lm2, Lp2 = perturbed(c, delta, ddelta, breaks)
        B = analyse_with_limits(pc, Lm2, Lp2, XM, XP)
        mis = []
        for r in ("i", "ii"):
            a = route_i(A, R2, EQ) if r == "i" else route_ii(A, R2, prec="mp")[0]
            b = route_i(B, R2, EQ) if r == "i" else route_ii(B, R2, prec="mp")[0]
            if a != b:
                mis.append({"route": r, "orig": name(a), "perturbed": name(b)})
        out.append({"i": i, "rep": rep, "kind": k, "n_cross": len(cross), "eta": mp.nstr(eta, 6), "amp_over_eta": mp.nstr(Aamp / eta, 4),
                    "mismatch": bool(mis), "detail": mis, "orig_class": name(route_i(A, R2, EQ)), "n_turns_perturbed": len(B["turns"])})
    return out


def run_c12(n):
    rng = np.random.default_rng(15101)
    rng2 = np.random.default_rng(15102)
    jobs = [(i, draw_poly(rng), "a" if i % 2 == 0 else "b", int(rng2.integers(2**63))) for i in range(n)]
    t0 = time.time()
    with Pool(4) as p:
        res = [x for r in p.map(c12_job, jobs, chunksize=4) for x in r]
    done = [r for r in res if "skipped" not in r]
    out = {"curves": n, "cases": len(res), "cases_run": len(done), "skipped": [r for r in res if "skipped" in r],
           "by_kind": {k: sum(r["kind"] == k for r in done) for k in ("a", "b")},
           "mismatches": sum(r["mismatch"] for r in done), "examples": [r for r in done if r["mismatch"]][:10],
           "classes_seen": sorted({r["orig_class"] for r in done}), "crossings_hist": {str(k): sum(r["n_cross"] == k for r in done) for k in sorted({r["n_cross"] for r in done})},
           "seconds": time.time() - t0}
    out["pass"] = out["mismatches"] == 0 and not out["skipped"]
    return out


def run_illustration():
    rng = np.random.default_rng(15201)
    for _ in range(200):
        c = draw_poly(rng)
        cur, Lm, Lp = base_curve(c)
        A = analyse_with_limits(cur, Lm, Lp, XM, XP)
        crit = [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]]
        R2 = mp.power(10, mp.mpf(float(rng.uniform(float(mp.log10(min(crit))), float(mp.log10(max(crit)))))))
        cross, N, eta = setup_case(c, R2, rng, A)
        if not cross:
            continue
        x1, (a, b) = cross[0], N[0]
        h = (b - a) / 2
        amp = eta * mp.mpf("0.9")
        om = 40 / h
        delta = lambda x: amp * mp.exp(-((x - x1) / (h / 2))**2) * mp.sin(om * (x - x1))
        ddelta = lambda x: amp * mp.exp(-((x - x1) / (h / 2))**2) * (om * mp.cos(om * (x - x1)) - 2 * (x - x1) / (h / 2)**2 * mp.sin(om * (x - x1)))
        fine = [float(a + (b - a) * k / 800) for k in range(801)]
        pc, Lm2, Lp2 = perturbed(c, delta, ddelta, fine)
        B = analyse_with_limits(pc, Lm2, Lp2, XM, XP)
        ca, cb = route_i(A, R2, EQ), route_i(B, R2, EQ)
        cb2 = route_ii(B, R2, prec="mp")[0]
        if ca != cb and cb == cb2:
            return {"poly": c, "R2": mp.nstr(R2, 12), "eta": mp.nstr(eta, 6), "amplitude_over_eta": 0.9, "x1": mp.nstr(x1, 10),
                    "N1": [mp.nstr(a, 8), mp.nstr(b, 8)], "sup_delta_lt_eta": True, "monotone_on_N1": monotone_ok(c, [N[0]], ddelta),
                    "class_before": name(ca), "class_after": name(cb), "class_after_route_ii": name(cb2)}
    return {"found": False}


def main():
    args = sys.argv[1:]
    n = int(args[args.index("--n") + 1]) if "--n" in args else None
    which = [a for a in args if a in ("C11", "C12", "ILL", "C11X")] or ["C11", "C12", "ILL"]
    path = os.path.join(HERE, "results", "t15_partG.json")
    R = json.load(open(path)) if os.path.exists(path) else {}
    for w in which:
        t0 = time.time()
        r = (run_c11(n or 1000) if w == "C11" else run_c12(n or 500) if w == "C12" else
             run_c11(n or 1000, cheb=True) if w == "C11X" else run_illustration())
        r["seconds"] = round(time.time() - t0, 1)
        R[w if n is None else f"{w}_n{n}"] = r
        print(w, json.dumps({k: v for k, v in r.items() if k not in ("examples",)}, default=str)[:900], flush=True)
        with open(path, "w") as fh:
            json.dump(R, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
