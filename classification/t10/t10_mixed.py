"""T10.4: mixed class (1, 0, 1) in the Hill family, on the T10.3 Hill sets with two turning points."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from classify import classify, name
from t10_census import N_HILL, NSET, draw
from t10_common import analyse, mpize, pi_curve, save_json

D6 = mp.mpf("1e-6")


def hill_sets():
    """Same RNG stream and order as t10_census.main()."""
    rng = np.random.default_rng(10003)
    for fam in ("bayes", "misspec", "capped", "blind"):
        draw(rng, fam, NSET)
    sets = []
    for n in N_HILL:
        sets += [{**p, "n": n, "c": 10.0**rng.uniform(-2, 2), "Pi0": 10.0**rng.uniform(-2, 2)}
                 for p in draw(rng, "blind", NSET)]
    return sets


def predict(R2, F, m, M, H):
    """Explicit enumeration for F(below) -> m -> M -> H(above)."""
    L = R2 < F
    U = R2 <= H
    hump = R2 < M
    jl = R2 < m
    jr = R2 <= H
    if L and U and hump and jl and jr:
        return "All"
    k = 1 if (hump and not (L and jl) and not jr) else 0
    return (int(L), int(U), k)


def job(p):
    q = mpize(p)
    A = analyse(pi_curve("hill", q))
    if len(A["turns"]) != 2:
        return None
    lam, Sig, c = q["lam"], q["Sig"], q["c"]
    F, H = Sig / lam, Sig / (lam + c)
    m, M = A["turns"][0]["value"], A["turns"][1]["value"]
    lo, hi = max(m, H), min(M, F)
    tols = [lo + (i + mp.mpf("0.5")) * (hi - lo) / 10 for i in range(10)]
    tols += [lo, hi, lo * (1 - D6), lo * (1 + D6), hi * (1 - D6), hi * (1 + D6)]
    rows, ok = [], True
    for j, R2 in enumerate(tols):
        want = predict(R2, F, m, M, H)
        r = classify(A, R2)
        good = r["route_i"] == want and r["route_ii"] == want
        ok &= good
        if not good:
            rows.append({"j": j, "R2": R2, "expected": name(want), "route_i": name(r["route_i"]),
                         "route_ii": name(r["route_ii"])})
    return {"p": p, "m": m, "M": M, "F": F, "H": H, "band_rel": (hi - lo) / F, "M_lt_F": bool(M < F),
            "lo_is": "m" if m > H else "H", "hi_is": "M" if M < F else "F", "n_tests": len(tols), "pass": bool(ok),
            "bad": rows}


def main():
    t0 = time.time()
    with Pool(4) as pool:
        res = [r for r in pool.map(job, hill_sets(), chunksize=20) if r is not None]
    bw = np.array([float(r["band_rel"]) for r in res])
    R = {"n_sets": len(res), "n_tests": sum(r["n_tests"] for r in res), "n_fail_sets": sum(not r["pass"] for r in res),
         "fails": [r for r in res if not r["pass"]][:30],
         "band_rel_median": float(np.median(bw)), "band_rel_min": float(bw.min()), "band_rel_max": float(bw.max()),
         "frac_M_lt_F": float(np.mean([r["M_lt_F"] for r in res])),
         "lo_counts": {k: sum(r["lo_is"] == k for r in res) for k in ("m", "H")},
         "hi_counts": {k: sum(r["hi_is"] == k for r in res) for k in ("M", "F")},
         "by_n": {str(n): sum(1 for r in res if r["p"]["n"] == n) for n in N_HILL}}
    R["pass"] = R["n_fail_sets"] == 0
    R["seconds"] = time.time() - t0
    print(f"{R['n_sets']} two-TP Hill sets, {R['n_tests']} tolerances, failing sets {R['n_fail_sets']}; band width "
          f"(rel. F) median {R['band_rel_median']:.3g}, min {R['band_rel_min']:.3g}, max {R['band_rel_max']:.3g}; "
          f"fraction with M < F {R['frac_M_lt_F']:.3f}; lo = m/H {R['lo_counts']}, hi = M/F {R['hi_counts']}")
    print(f"T10.4: {'PASS' if R['pass'] else 'FAIL'}")
    save_json(R, "t10_4.json")


if __name__ == "__main__":
    main()
