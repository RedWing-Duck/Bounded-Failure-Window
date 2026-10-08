"""A9: M-I optimal along Delta t: SymPy sign attempt on the closed form, numerical monotonicity (1,000 sets x 400 points,
dps 60, seed 12009), regression against Task 11's results/t11_6.json."""
import json
import os
import signal
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np
import sympy as sp

from t12_common import HERE, mi_funcs, samp_metrics, save_json


class _TO(Exception):
    pass


def _alarm(*_):
    raise _TO()


def sympy_attempt(tmax=900):
    dt, l, S, P = sp.symbols("dt lambda Sigma Pi", positive=True)
    ph = sp.exp(-l * dt)
    F = S / l
    q11 = F * (1 - ph**2)
    q12 = 2 * S / l**2 * ((1 - ph) - (1 - ph**2) / 2)
    q22 = 2 * S / l**2 * (dt - 2 * (1 - ph) / l + (1 - ph**2) / (2 * l))
    h = (1 - ph) / (l * dt)
    re = q22 / dt**2 + 1 / (P * dt)
    g = q12 / dt
    a2, a1, a0 = h**2, re * (1 - ph**2) - q11 * h**2 + 2 * ph * h * g, -(q11 * re - g**2)
    p = 2 * (-a0) / (a1 + sp.sqrt(a1**2 - 4 * a2 * a0))
    fac = (1 - ph**2) / (2 * l * dt)
    out = {}
    for key, e in (("a", p), ("b", p * fac + F * (1 - fac))):
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(tmax)
        t0 = time.time()
        try:
            d = sp.simplify(sp.diff(e, dt))
            pos = d.is_positive
            out[key] = {"result": "proved" if pos else "unresolved", "is_positive": str(pos), "seconds": time.time() - t0}
        except _TO:
            out[key] = {"result": "unresolved", "is_positive": "timeout", "seconds": time.time() - t0}
        finally:
            signal.alarm(0)
    return out


def mono_job(args):
    p, xs = args
    lam = mp.mpf(p["lam"])
    bad = []
    with mp.workdps(60):
        fa, da = mi_funcs("a", p)
        fb, db = mi_funcs("b", p)
        for x in xs:
            t = mp.power(10, mp.mpf(float(x))) / lam
            va, vb = da(t), db(t)
            if not (va > 0 and vb > 0):
                bad.append({"lam_dt": float(x), "dPa": va, "dPb": vb})
    return {"p": p, "bad": bad}


def main():
    t0 = time.time()
    R = {}
    # regression vs Task 11
    t11 = json.load(open(os.path.join(HERE, "..", "t11", "results", "t11_6.json")))
    rows = []
    for r in t11["mc"]["rows"]:
        a, b = samp_metrics(mp.mpf(r["Dt"]), mp.mpf(1), mp.mpf("0.01"), mp.mpf(1))
        ea, eb = abs(a / mp.mpf(r["a_formula"]) - 1), abs(b / mp.mpf(r["b_formula"]) - 1)
        rows.append({"dt": r["Dt"], "a": a, "a_t11": r["a_formula"], "rel_a": ea, "b": b, "b_t11": r["b_formula"], "rel_b": eb,
                     "pass": bool(ea <= mp.mpf("1e-12") and eb <= mp.mpf("1e-12"))})
    R["regression"] = {"rows": rows, "pass": all(r["pass"] for r in rows)}
    print("A9 regression", R["regression"]["pass"], flush=True)
    rng = np.random.default_rng(12009)
    U = lambda: float(10.0**rng.uniform(-2, 2))
    sets = [{"lam": U(), "Sig": U(), "Pi": U()} for _ in range(1000)]
    xs = np.linspace(-8, 8, 400)
    with Pool(4) as pool:
        mono = pool.map(mono_job, [(p, xs) for p in sets], chunksize=10)
    nb = [m for m in mono if m["bad"]]
    R["monotone"] = {"n_sets": len(mono), "n_points": 400 * len(mono), "lam_dt_range": [1e-8, 1e8], "n_violating_sets": len(nb),
                     "n_violations": sum(len(m["bad"]) for m in mono), "examples": nb[:10]}
    print("A9 monotone violating sets", len(nb), flush=True)
    R["sympy"] = sympy_attempt()
    print("A9 sympy", R["sympy"], flush=True)
    R["seconds"] = time.time() - t0
    save_json(R, "t12_mi.json")


if __name__ == "__main__":
    main()
