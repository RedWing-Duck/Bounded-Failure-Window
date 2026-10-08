"""A6 (optimal M-P: regression, limits, numerical monotonicity), A10 (pairs (dt, 2 dt)) and the A8 qualitative
regression (D1, lam = 1, Sig = 0.01, Pi = 1, G = 0.5). Seed 12006 (A6 grid, then A10 pairs from the same stream)."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t12_common import analyse_dt, classify, dt_funcs, name, save_json, sf_match, sstar
from t12_a8 import root_D1

SIGN = {"post": -1, "prior": 1, "avg": 1}


def mono_job(args):
    p, xs = args
    lam = mp.mpf(p["lam"])
    bad = []
    with mp.workdps(60):
        fd = {m: dt_funcs("opt", m, p) for m in SIGN}
        for x in xs:
            t = mp.power(10, mp.mpf(float(x))) / lam
            for m, sg in SIGN.items():
                dv = fd[m][1](t)
                if not (dv * sg > 0):
                    bad.append({"metric": m, "lam_dt": float(x), "deriv": dv})
        F = mp.mpf(p["Sig"]) / lam
        s2 = sstar(lam, mp.mpf(p["Sig"]), mp.mpf(p["Pi"]))
        lim0 = max(abs(fd[m][0](mp.mpf("1e-60") / lam) / s2 - 1) for m in SIGN)
        liminf = [abs(fd["post"][0](mp.mpf("1e60") / lam)), max(abs(fd[m][0](mp.mpf("1e60") / lam) / F - 1) for m in ("prior", "avg"))]
    return {"p": p, "bad": bad, "lim0_rel": lim0, "liminf": liminf}


def pair_job(args):
    p, t = args
    with mp.workdps(60):
        fp, _ = dt_funcs("opt", "post", p)
        fa, _ = dt_funcs("opt", "avg", p)
        t = mp.mpf(t)
        return {"p": p, "dt": t, "post_dec": bool(fp(2 * t) < fp(t)), "avg_inc": bool(fa(2 * t) > fa(t)),
                "post_ratio": fp(2 * t) / fp(t), "avg_ratio": fa(2 * t) / fa(t)}


def main():
    t0 = time.time()
    R = {}
    # ---------------- A6 regression
    p1 = {"lam": 1, "Sig": "0.01", "Pi": 1}
    stated = {("post", 1): "0.0098858", ("avg", 1): "0.0099506", ("post", 10): "0.0090909", ("avg", 10): "0.0099545",
              ("post", 100): "0.0050000", ("avg", 100): "0.0099750"}
    rows = []
    for (m, dt), st in stated.items():
        f, _ = dt_funcs("opt", m, p1)
        v = f(mp.mpf(dt))
        rows.append({"metric": m, "dt": dt, "value": mp.nstr(v, 12), "stated": st, "pass": sf_match(v, st)})
    R["A6_regression"] = {"rows": rows, "pass": all(r["pass"] for r in rows)}
    print("A6 regression", R["A6_regression"]["pass"], [(r["metric"], r["dt"], r["value"]) for r in rows], flush=True)
    # ---------------- A6 numerical monotonicity
    rng = np.random.default_rng(12006)
    U = lambda: float(10.0**rng.uniform(-2, 2))
    sets = [{"lam": U(), "Sig": U(), "Pi": U()} for _ in range(1000)]
    xs = np.linspace(-8, 8, 400)
    with Pool(4) as pool:
        mono = pool.map(mono_job, [(p, xs) for p in sets], chunksize=10)
    nb = [m for m in mono if m["bad"]]
    R["A6_monotone"] = {"n_sets": len(mono), "n_points": 400 * len(mono), "lam_dt_range": [1e-8, 1e8],
                        "n_violating_sets": len(nb),
                        "n_violations": {m: sum(1 for r in mono for b in r["bad"] if b["metric"] == m) for m in SIGN},
                        "examples": nb[:10], "max_lim0_rel": max(m["lim0_rel"] for m in mono),
                        "max_post_at_1e60": max(m["liminf"][0] for m in mono),
                        "max_prior_avg_rel_at_1e60": max(m["liminf"][1] for m in mono)}
    print("A6 monotone violations", R["A6_monotone"]["n_violations"], flush=True)
    # ---------------- A10 pairs (dt, 2 dt), same stream
    pairs = []
    for _ in range(1000):
        p = {"lam": U(), "Sig": U(), "Pi": U()}
        pairs.append((p, float(10.0**rng.uniform(-4, 4)) / p["lam"]))
    with Pool(4) as pool:
        pr = pool.map(pair_job, pairs, chunksize=10)
    R["A10"] = {"n_pairs": len(pr), "n_post_dec": sum(r["post_dec"] for r in pr), "n_avg_inc": sum(r["avg_inc"] for r in pr),
                "max_post_ratio": max(r["post_ratio"] for r in pr), "min_avg_ratio": min(r["avg_ratio"] for r in pr),
                "fails": [r for r in pr if not (r["post_dec"] and r["avg_inc"])][:10]}
    R["A10"]["pass"] = R["A10"]["n_post_dec"] == len(pr) and R["A10"]["n_avg_inc"] == len(pr)
    print("A10", R["A10"]["pass"], flush=True)
    # ---------------- A8 qualitative regression (prompt's values)
    q = {"lam": 1, "Sig": "0.01", "Pi": 1, "G": "0.5"}
    F = mp.mpf("0.01")
    Ap = analyse_dt("D1", "post", q)
    Aa = analyse_dt("D1", "avg", q)
    mx = [t for t in Ap["turns"] if t["kind"] == "max"]
    post_ok = len(Ap["turns"]) == 1 and len(mx) == 1
    v_ok = post_ok and abs(mx[0]["value"] / mp.mpf("0.166") - 1) <= mp.mpf("0.02")
    th_ok = post_ok and mp.mpf("0.5") <= mx[0]["theta"] <= 2
    Ca = classify(Aa, F)
    cross = [e[1] for e in Ca["ends"] if e[1] is not None]
    dtE = root_D1(mp.mpf("0.5"), F, mp.mpf(1))
    cross_ok = len(cross) == 1 and mp.mpf(50) / mp.mpf("1.5") <= cross[0] <= 50 * mp.mpf("1.5")
    mins = [t for t in Aa["turns"] if t["kind"] == "min"]
    after_ok = (len(cross) == 1 and len(mins) >= 1 and mins[-1]["theta"] > cross[0] and mins[-1]["value"] < F
                and Aa["approach_plus"] == "below")
    post1 = dt_funcs("D1", "post", q)[0](mp.mpf(1))
    R["A8_regression"] = {"post_turns": [(t["kind"], t["theta"], t["value"]) for t in Ap["turns"]], "post_at_1": post1,
                          "post_single_max": post_ok, "max_value_within_2pct_of_0.166": bool(v_ok),
                          "max_at_dt_within_factor_2_of_1": bool(th_ok), "avg_crossings_of_F": cross, "dtE_A2": dtE,
                          "crossing_within_factor_1.5_of_50": bool(cross_ok),
                          "avg_turns": [(t["kind"], t["theta"], t["value"]) for t in Aa["turns"]],
                          "then_min_below_F_and_returns_from_below": bool(after_ok)}
    R["A8_regression"]["pass"] = bool(post_ok and v_ok and th_ok and cross_ok and after_ok)
    print("A8 regression", {k: v for k, v in R["A8_regression"].items() if k != "avg_turns"}, flush=True)
    R["seconds"] = time.time() - t0
    save_json(R, "t12_dt.json")


if __name__ == "__main__":
    main()
