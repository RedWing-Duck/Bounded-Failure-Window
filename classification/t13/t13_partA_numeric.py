"""Part A numerical checks (PREREG_t13): A1/A2 (10,000 sets, 100 digits), A3 (10,000 sets), A4 (10,000 power curves),
A5 (Pi0_pair regression + 5,000 Hill sets), A7 (10,000 sets, 60 digits). Usage: python3 t13_partA_numeric.py [ITEM ...]"""
import sys
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np
import sympy as sp

from t13_common import logu, save_json

ITEMS = sys.argv[1:] or ["A12", "A3", "A4", "A5", "A7"]


# ---------------------------------------------------------------- A1 / A2
def a12_job(seed):
    rng = np.random.default_rng(seed)
    lam, Sig, Pi = (mp.mpf(logu(rng)) for _ in range(3))
    xv = mp.mpf(10.0**rng.uniform(-8, np.log10(50)))
    fails = []
    with mp.workdps(100):
        F, k = Sig / lam, lam / Pi
        x = xv
        r = k / x
        s = -mp.expm1(-2 * x)
        s1 = 2 * mp.exp(-2 * x)
        b = s * (r - F)
        disc = mp.sqrt(b**2 + 4 * s * F * r)
        M = 2 * s * F * r / (b + disc) if b > 0 else (-b + disc) / 2
        fM = 2 * M + b
        B = F * M * s1 - (F - M) * r * (s / x - s1)
        br2 = F * s1 - (M - s * F) * (s / x - s1) / s
        links1 = {"f_M > 0": fM > 0, "dM/dx > 0": B / fM > 0, "sF < M": s * F < M, "M < F": M < F,
                  "s/x > s'": s / x - s1 > 0, "0 < M - sF < F(1-s)": 0 < M - s * F < F * (1 - s),
                  "bracket > 0": br2 > 0, "2x >= 1 - e^{-2x}": 2 * x - s >= 0}
        # A2
        phi = F * Pi * x / lam
        ps = phi / s
        d2 = mp.sqrt((1 - phi)**2 + 4 * ps)
        mu = 2 * ps / ((1 - phi) + d2) if phi <= 1 else ((phi - 1) + d2) / 2
        E = 1 / x - s1 / s
        dmu = (phi * mu / x + ps * E) / (2 * mu + 1 - phi)
        dlnQ = dmu / (mu * (1 + mu)) - E
        Q = mu * s / ((1 + mu) * x)
        Pbar_mu = F - F / 2 * Q
        Pbar_M = F - (F - M) * mp.expm1(2 * x) / (2 * x)
        links2 = {"mu > 0": mu > 0, "mu > phi - 1": mu > phi - 1, "E > 0": E > 0,
                  "(1 - x s'/s)(2/s) >= 1": (1 - x * s1 / s) * (2 / s) >= 1, "dPbar/dx > 0": -F / 2 * Q * dlnQ > 0,
                  "Pbar(mu) = Pbar(M)": abs(Pbar_mu / Pbar_M - 1) < mp.mpf("1e-80")}
        for kk, v in list(links1.items()) + list(links2.items()):
            if not v:
                fails.append(kk)
    return {"lam": lam, "Sig": Sig, "Pi": Pi, "x": xv, "fails": fails, "dM": B / fM, "dPbar": -F / 2 * Q * dlnQ}


# ---------------------------------------------------------------- A3 (M-I closed form, analytic derivative)
_dt, _l, _S, _P = sp.symbols("dt lambda Sigma Pi", positive=True)


def _mi_expr():
    ph = sp.exp(-_l * _dt)
    F = _S / _l
    q11 = F * (1 - ph**2)
    q12 = 2 * _S / _l**2 * ((1 - ph) - (1 - ph**2) / 2)
    q22 = 2 * _S / _l**2 * (_dt - 2 * (1 - ph) / _l + (1 - ph**2) / (2 * _l))
    h = (1 - ph) / (_l * _dt)
    re = q22 / _dt**2 + 1 / (_P * _dt)
    g = q12 / _dt
    a2, a1, a0 = h**2, re * (1 - ph**2) - q11 * h**2 + 2 * ph * h * g, -(q11 * re - g**2)
    p = 2 * (-a0) / (a1 + sp.sqrt(a1**2 - 4 * a2 * a0))
    fac = (1 - ph**2) / (2 * _l * _dt)
    return p, p * fac + F * (1 - fac)


_MI = None


def a3_job(seed):
    global _MI
    if _MI is None:
        pa, pb = _mi_expr()
        _MI = [sp.lambdify((_dt, _l, _S, _P), sp.diff(e, _dt), "mpmath", cse=True) for e in (pa, pb)]
    rng = np.random.default_rng(seed)
    lam, Sig, Pi = (logu(rng) for _ in range(3))
    xv = 10.0**rng.uniform(-8, np.log10(50))
    with mp.workdps(100 + int(6 * max(0, -np.log10(xv)))):
        lm, Sm, Pm = mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi)
        dt = mp.mpf(xv) / lm
        da, db = _MI[0](dt, lm, Sm, Pm), _MI[1](dt, lm, Sm, Pm)
    return {"lam": lam, "Sig": Sig, "Pi": Pi, "x": xv, "dPa": da, "dPb": db, "ok": bool(da > 0 and db > 0)}


# ---------------------------------------------------------------- A4 (power family, 0 < beta < 2)
def a4_job(seed):
    from t11_common import P_pow, analyse_with_limits, limits_pow, power_curve
    rng = np.random.default_rng(seed)
    beta = mp.mpf(float(rng.uniform(0, 2)))
    while beta == 0:
        beta = mp.mpf(float(rng.uniform(0, 2)))
    K, lam, Sig = (mp.mpf(logu(rng)) for _ in range(3))
    Lm, Lp, xm, xp = limits_pow(beta, K, lam, Sig)
    A = analyse_with_limits(power_curve(beta, K, lam, Sig), Lm, Lp, xm, xp)
    kinds = [t["kind"] for t in A["turns"]]
    out = {"beta": beta, "K": K, "lam": lam, "Sig": Sig, "kinds": kinds, "limit_check": A["limit_check"]}
    if kinds == ["max"]:
        tau = A["turns"][0]["theta"]
        P = P_pow(tau, beta, K, lam, Sig)
        v = K / 2 * tau**(beta - 1)
        v1, v2 = (beta - 1) * v / tau, (beta - 1) * (beta - 2) * v / tau**2
        A1, A2 = lam**2 - 1 / tau**2, 2 / tau**3
        Ptt = A2 * P**2 - 4 * v2 * (Sig - lam * P)
        Pt = A1 * P**2 - 4 * v1 * (Sig - lam * P)
        out.update({"tau": tau, "Phi_tautau": Ptt, "Phi_tau_rel": abs(Pt) / (abs(A1) * P**2 + abs(4 * v1 * (Sig - lam * P))),
                    "closed": P**2 * (beta + (2 - beta) * lam**2 * tau**2) / tau**3})
    out["ok"] = bool(kinds == ["max"] and out.get("Phi_tautau", -1) > 0 and all(A["limit_check"]))
    return out


# ---------------------------------------------------------------- A5 (Hill, general n)
def phi_star(n, lam, c):
    """t* and phi_n(t*) from the positive root T* of R(T) (Descartes: exactly one)."""
    a = (n - 1) / n
    p0, p1, p2 = (2 * n - 1) * lam, (n - 1) * (c + 2 * lam), -(lam + c)
    co = [a * p2, a * (p1 + p2) - p1 + 2 * p2, a * (p0 + p1) + p1 - 2 * p0, a * p0]     # T^3 .. T^0
    roots = [rt.real for rt in mp.polyroots(co, maxsteps=200, extraprec=200) if abs(rt.imag) < mp.mpf("1e-40") and rt.real > 0]
    T = roots[0]
    t = T**(1 / n)
    return t, t**(n - 1) * (p2 * T**2 + p1 * T + p0) / (1 + T)**2, len(roots)


def pi0_pair(n, lam, c, Sig):
    t, ph, nr = phi_star(n, lam, c)
    return c * ph / (2 * n * Sig), nr


def a5_job(seed):
    from t10_common import pi_curve
    from t11_common import analyse_with_limits
    rng = np.random.default_rng(seed)
    with mp.workdps(50):
        n = mp.mpf(10.0**rng.uniform(np.log10(1.01), 1))
        lam, c, Sig = (mp.mpf(logu(rng)) for _ in range(3))
        pp, nr = pi0_pair(n, lam, c, Sig)
        P0 = pp * mp.mpf(10.0**rng.uniform(np.log10(0.5), np.log10(2)))
        p = {"lam": lam, "Sig": Sig, "c": c, "Pi0": P0, "n": n}
        A = analyse_with_limits(pi_curve("hill", p), Sig / lam, Sig / (lam + c), mp.mpf(-80), mp.mpf(80))
        kinds = [t["kind"] for t in A["turns"]]
        pred = [] if P0 > pp else ["min", "max"]
    return {"n": n, "lam": lam, "c": c, "Sig": Sig, "Pi0_over_pair": P0 / pp, "kinds": kinds, "pred": pred,
            "n_roots_R": nr, "ok": bool(kinds == pred and nr == 1 and all(A["limit_check"]))}


# ---------------------------------------------------------------- A7 (strict gap P < V, matched zero-frequency tau)
_G, _t = sp.symbols("G tau", positive=True)
_sig2 = (_S + _G**2 / (2 * _P * (1 + (_l + _G) * _t))) / (_l + _G)
_num = sp.Poly(sp.numer(sp.together(sp.diff(_sig2, _G))), _G)
_NUMC = [sp.lambdify((_l, _S, _P, _t), cf, "mpmath") for cf in _num.all_coeffs()]


def a7_job(seed):
    rng = np.random.default_rng(seed)
    lam, Sig, Pi = (mp.mpf(logu(rng)) for _ in range(3))
    with mp.workdps(60):
        tau = mp.mpf(10.0**rng.uniform(-8, 8)) / lam
        b = 4 * Sig * tau + 2 * lam / Pi
        D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
        P = 4 * Sig / (Pi * (b + mp.sqrt(D)))
        co = [f(lam, Sig, Pi, tau) for f in _NUMC]
        while co and co[0] == 0:
            co = co[1:]
        roots = [rt.real for rt in mp.polyroots(co, maxsteps=300, extraprec=300) if abs(rt.imag) < mp.mpf("1e-30") * (1 + abs(rt)) and rt.real > 0]
        s2 = lambda G: (Sig + G**2 / (2 * Pi * (1 + (lam + G) * tau))) / (lam + G)
        cands = [s2(mp.mpf(0)), 1 / (2 * Pi * tau)] + [s2(g) for g in roots]
        V = min(cands)
    return {"lam": lam, "Sig": Sig, "Pi": Pi, "tau": tau, "P": P, "V": V, "rel_gap": (V - P) / P, "ok": bool(V > P)}


def run(job, seeds, chunks=20):
    with Pool(4) as pool:
        return pool.map(job, seeds, chunksize=chunks)


def main():
    R = {}
    for it in ITEMS:
        t0 = time.time()
        if it == "A12":
            res = run(a12_job, [13001 * 100000 + i for i in range(10000)])
            fl = {}
            for r in res:
                for f in r["fails"]:
                    fl[f] = fl.get(f, 0) + 1
            a1keys = {"f_M > 0", "dM/dx > 0", "sF < M", "M < F", "s/x > s'", "0 < M - sF < F(1-s)", "bracket > 0", "2x >= 1 - e^{-2x}"}
            R["A1"] = {"n": len(res), "fail_counts": {k: v for k, v in fl.items() if k in a1keys},
                       "pass": not any(k in a1keys for k in fl), "min_dM": min(r["dM"] for r in res),
                       "examples": [r for r in res if any(f in a1keys for f in r["fails"])][:5]}
            R["A2"] = {"n": len(res), "fail_counts": {k: v for k, v in fl.items() if k not in a1keys},
                       "pass": not any(k not in a1keys for k in fl), "min_dPbar": min(r["dPbar"] for r in res),
                       "examples": [r for r in res if any(f not in a1keys for f in r["fails"])][:5]}
            R["A1"]["seconds"] = R["A2"]["seconds"] = time.time() - t0
            print("A1", R["A1"]["pass"], R["A1"]["fail_counts"], "A2", R["A2"]["pass"], R["A2"]["fail_counts"], flush=True)
        elif it == "A3":
            res = run(a3_job, [13003 * 100000 + i for i in range(10000)])
            bad = [r for r in res if not r["ok"]]
            R["A3"] = {"n": len(res), "n_violations": len(bad), "examples": bad[:10], "pass": not bad,
                       "min_dPa": min(r["dPa"] for r in res), "min_dPb": min(r["dPb"] for r in res), "seconds": time.time() - t0}
            print("A3", R["A3"]["pass"], len(bad), flush=True)
        elif it == "A4":
            res = run(a4_job, [13004 * 100000 + i for i in range(10000)], chunks=10)
            bad = [r for r in res if not r["ok"]]
            hist = {}
            for r in res:
                kk = "-".join(r["kinds"]) or "none"
                hist[kk] = hist.get(kk, 0) + 1
            R["A4"] = {"n": len(res), "kinds_hist": hist, "n_fail": len(bad), "examples": bad[:10], "pass": not bad,
                       "max_Phi_tau_rel": max(r.get("Phi_tau_rel", 0) for r in res),
                       "max_closed_vs_direct_rel": max(abs(r["Phi_tautau"] / r["closed"] - 1) for r in res if "closed" in r),
                       "seconds": time.time() - t0}
            print("A4", R["A4"]["pass"], hist, flush=True)
        elif it == "A5":
            table = {"1.5": "30.2430947474", "2": "31.4750497595", "3": "37.8200022316", "4": "44.1796834278", "8": "62.7113145769"}
            rows = []
            with mp.workdps(50):
                for nn, st in table.items():
                    v, nr = pi0_pair(mp.mpf(nn), mp.mpf(1), mp.mpf(1), mp.mpf("0.01"))
                    rows.append({"n": nn, "closed_form": v, "task10": st, "rel": abs(v / mp.mpf(st) - 1), "n_roots": nr,
                                 "pass": bool(abs(v / mp.mpf(st) - 1) <= mp.mpf("1e-9"))})
                n2 = 2 * (mp.sqrt(3) * 2 - 3)
            res = run(a5_job, [13005 * 100000 + i for i in range(5000)], chunks=10)
            bad = [r for r in res if not r["ok"]]
            R["A5"] = {"regression": rows, "regression_pass": all(r["pass"] for r in rows), "n": len(res), "n_fail": len(bad),
                       "n_pair_pred": sum(r["pred"] == ["min", "max"] for r in res), "examples": bad[:10],
                       "pass": all(r["pass"] for r in rows) and not bad, "seconds": time.time() - t0}
            print("A5", R["A5"]["pass"], [(r["n"], mp.nstr(r["closed_form"], 15)) for r in rows], len(bad), flush=True)
        elif it == "A7":
            res = run(a7_job, [13007 * 100000 + i for i in range(10000)])
            bad = [r for r in res if not r["ok"]]
            R["A7"] = {"n": len(res), "n_fail": len(bad), "min_rel_gap": min(r["rel_gap"] for r in res), "examples": bad[:10],
                       "pass": not bad, "seconds": time.time() - t0}
            print("A7", R["A7"]["pass"], len(bad), mp.nstr(R["A7"]["min_rel_gap"], 5), flush=True)
        save_json(R, "t13_partA_numeric_" + "_".join(ITEMS) + ".json")


if __name__ == "__main__":
    main()
