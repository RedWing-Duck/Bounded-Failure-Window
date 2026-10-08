"""T10.7: blind search for unpredicted classes (10^6 classifications, both routes)."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np
import sympy as sp

from classify import route_i, route_ii, name, EQ, EQF
from t10_common import ZREL, Curve, analyse, dsig2_dG, mpize, pi_curve, save_json, sig2
from t10_tau import P_rat, dP_f

# Stage 2 (matched zero-frequency power) optimal filter and its derivative
_t, _l, _S, _P = sp.symbols("tau lambda Sigma Pi", positive=True)
_b = 4 * _S * _t + 2 * _l / _P
_D = _b**2 + 8 * _S * (1 - _l * _t)**2 / _P
PZ = 4 * _S / (_P * (_b + sp.sqrt(_D)))
PZ_mp = sp.lambdify((_t, _l, _S, _P), PZ, "mpmath")
dPZ_mp = sp.lambdify((_t, _l, _S, _P), sp.diff(PZ, _t), "mpmath")
PZ_fl = sp.lambdify((_t, _l, _S, _P), PZ, "numpy")
_v = sp.symbols("v", positive=True)
PV_fl = sp.lambdify((_t, _l, _S, _v), 8 * _S * _v / (4 * (_S + _l * _v) + sp.sqrt(16 * (_S + _l * _v)**2
                                                                               + 16 * _S * _v * (1 - _l * _t)**2 / _t)), "numpy")

A_ = {"All"}
LR, UR, TR, WIN, EMP, MIX = (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (0, 0, 0), (1, 0, 1)
PRED = {"Pi bayes": {"All", LR, WIN, EMP}, "Pi misspec": {LR, WIN, EMP}, "Pi capped": {"All", LR, WIN, EMP},
        "Pi blind": {"All", LR}, "Pi hill": {"All", LR, MIX, TR, WIN, EMP},
        "Pi0 bayes": {"All", TR, UR, LR, EMP}, "c bayes": {"All", TR, UR},
        "tau ZF relay": {"All", LR, EMP}, "tau ZF optimal": {LR, EMP},
        "tau var relay": {"All", UR, EMP}, "tau var optimal": {WIN, EMP}}


def f2(x):
    return np.float64(x)


def make(kind, p):
    q = mpize(p)
    lam, Sig = q["lam"], q["Sig"]
    if kind.startswith("Pi "):
        return pi_curve(kind.split()[1], q)
    if kind == "Pi0 bayes":
        Pi, c = q["Pi"], q["c"]
        f = lambda P0: sig2(c * Pi / (Pi + P0), Pi, lam, Sig)
        d = lambda P0: dsig2_dG(c * Pi / (Pi + P0), Pi, lam, Sig) * (-c * Pi / (Pi + P0)**2)
        ffl = lambda P0: sig2(f2(p["c"]) * p["Pi"] / (p["Pi"] + P0), f2(p["Pi"]), f2(p["lam"]), f2(p["Sig"]))
    elif kind == "c bayes":
        Pi, P0 = q["Pi"], q["Pi0"]
        K = Pi / (Pi + P0)
        f = lambda c: sig2(c * K, Pi, lam, Sig)
        d = lambda c: dsig2_dG(c * K, Pi, lam, Sig) * K
        Kf = f2(p["Pi"]) / (p["Pi"] + p["Pi0"])
        ffl = lambda c: sig2(c * Kf, f2(p["Pi"]), f2(p["lam"]), f2(p["Sig"]))
    elif kind == "tau ZF relay":
        Pi, G = q["Pi"], q["G"]
        a = lam + G
        f = lambda t: (Sig + G**2 / (2 * Pi * (1 + a * t))) / a
        d = lambda t: -G**2 / (2 * Pi * (1 + a * t)**2)
        af = f2(p["lam"]) + p["G"]
        ffl = lambda t: (p["Sig"] + p["G"]**2 / (2 * p["Pi"] * (1 + af * t))) / af
    elif kind == "tau ZF optimal":
        Pi = q["Pi"]
        f = lambda t: PZ_mp(t, lam, Sig, Pi)
        d = lambda t: dPZ_mp(t, lam, Sig, Pi)
        ffl = lambda t: PZ_fl(f2(t), f2(p["lam"]), f2(p["Sig"]), f2(p["Pi"]))
    elif kind == "tau var relay":
        v, G = q["v"], q["G"]
        a = lam + G
        f = lambda t: (Sig + G**2 * v * t / (1 + a * t)) / a
        d = lambda t: G**2 * v / (a * (1 + a * t)**2)
        af = f2(p["lam"]) + p["G"]
        ffl = lambda t: (p["Sig"] + p["G"]**2 * p["v"] * t / (1 + af * t)) / af
    elif kind == "tau var optimal":
        v = q["v"]
        f = lambda t: P_rat(t, lam, Sig, v)
        d = lambda t: dP_f(t, lam, Sig, v)
        ffl = lambda t: PV_fl(f2(t), f2(p["lam"]), f2(p["Sig"]), f2(p["v"]))
    shift = -mp.log10(lam) if kind.startswith("tau") else 0
    return Curve(f, d, lambda th: ZREL * abs(f(th)) / th, shift, [], ffl, kind)


def params(kind, rng):
    U = lambda: float(10.0**rng.uniform(-2, 2))
    p = {"lam": U(), "Sig": U()}
    extra = {"Pi bayes": ("c", "Pi0"), "Pi misspec": ("lam1", "Sig1"), "Pi capped": ("g", "c"), "Pi blind": ("G0",),
             "Pi hill": ("c", "Pi0"), "Pi0 bayes": ("Pi", "c"), "c bayes": ("Pi", "Pi0"), "tau ZF relay": ("Pi", "G"),
             "tau ZF optimal": ("Pi",), "tau var relay": ("v", "G"), "tau var optimal": ("v",)}[kind]
    for k in extra:
        p[k] = U()
    return p


def job(args):
    kind, p, seed = args
    rng = np.random.default_rng(seed)
    A = analyse(make(kind, p))
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]] if mp.isfinite(v) and v > 0]
    lo, hi = float(mp.log10(min(crit) / 2)), float(mp.log10(2 * max(crit)))
    tols = [mp.mpf(10) ** mp.mpf(float(x)) for x in rng.uniform(lo, hi, 50)]
    for i in range(50):
        cv = crit[int(rng.integers(len(crit)))]
        tols.append(cv if i < 10 else cv * (1 + mp.mpf(float(rng.uniform(-1, 1))) * mp.mpf("1e-6")))
    counts, flagged, persist = {}, 0, []
    for R2 in tols:
        ci = route_i(A, R2, EQF)
        cii, _ = route_ii(A, R2, prec="fl")
        bad = ci != cii or ci not in PRED[kind] or cii not in PRED[kind]
        if bad:
            flagged += 1
            with mp.workdps(60):
                ci2 = route_i(A, R2, EQ)
                cii2, _ = route_ii(A, R2, prec="mp")
            if ci2 != cii2 or ci2 not in PRED[kind]:
                persist.append({"kind": kind, "p": p, "R2": R2, "route_i": name(ci2), "route_ii": name(cii2),
                                "float_route_i": name(ci), "float_route_ii": name(cii)})
            ci = ci2
        counts[name(ci)] = counts.get(name(ci), 0) + 1
    return {"kind": kind, "counts": counts, "flagged": flagged, "persist": persist, "n_tp": len(A["turns"]),
            "limit_ok": A["limit_ok"]}


PLAN = [("Pi bayes", 1000), ("Pi misspec", 1000), ("Pi capped", 1000), ("Pi blind", 500), ("Pi hill", 2000),
        ("Pi0 bayes", 1000), ("c bayes", 1000), ("tau ZF relay", 625), ("tau ZF optimal", 625),
        ("tau var relay", 625), ("tau var optimal", 625)]
HILL_N = [1.5, 2, 3, 4, 8]


def main():
    t0 = time.time()
    rng = np.random.default_rng(10007)
    jobs = []
    for kind, n in PLAN:
        for i in range(n):
            p = params(kind, rng)
            if kind == "Pi hill":
                p["n"] = HILL_N[i % 5]
            jobs.append((kind, p, int(rng.integers(2**63))))
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=25)
    R = {"by_kind": {}, "persist": [], "total": 0, "flagged": 0}
    for kind, _ in PLAN:
        rr = [r for r in res if r["kind"] == kind]
        cnt = {}
        for r in rr:
            for k, v in r["counts"].items():
                cnt[k] = cnt.get(k, 0) + v
        tot = sum(cnt.values())
        R["by_kind"][kind] = {"curves": len(rr), "classifications": tot, "classes": cnt,
                              "predicted": sorted(name(c) for c in PRED[kind]),
                              "flagged": sum(r["flagged"] for r in rr), "persisting": sum(len(r["persist"]) for r in rr),
                              "tp_hist": {str(k): sum(1 for r in rr if r["n_tp"] == k) for k in sorted({r["n_tp"] for r in rr})}}
        R["total"] += tot
        R["flagged"] += R["by_kind"][kind]["flagged"]
        R["persist"] += [x for r in rr for x in r["persist"]]
        print(f"{kind}: {len(rr)} curves, {tot} classifications, classes {cnt}, flagged {R['by_kind'][kind]['flagged']}, "
              f"persisting {R['by_kind'][kind]['persisting']}", flush=True)
    R["n_persist"] = len(R["persist"])
    R["persist"] = R["persist"][:50]
    R["pass"] = R["n_persist"] == 0
    R["seconds"] = time.time() - t0
    print(f"T10.7: {'PASS' if R['pass'] else 'FAIL'}: {R['total']} classifications, flagged {R['flagged']}, persisting {R['n_persist']}")
    save_json(R, "t10_7.json")


if __name__ == "__main__":
    main()
