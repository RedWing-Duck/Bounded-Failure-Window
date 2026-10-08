"""Part C: blind search, 22 combos x 1,000 curves x 200 tolerances (seed 12100). Route (i) mp on the dps-50 turning points,
route (ii) float64; every flagged case (disagreement, or a class outside the allowed set) re-run in mp at dps 60."""
import json
import os
import sys
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t12_common import RES, analyse_dt, analyse_sig, name, route_i, route_ii, save_json  # sets sys.path for t10/t11
from classify import EQ  # noqa: E402
from t12_sigma import ALLOWED as SIG_ALLOWED

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
LR, UR, EMP = (1, 0, 0), (0, 1, 0), (0, 0, 0)
DT_COMBOS = [(f, m) for f in ("opt", "D1", "D2", "D3") for m in ("post", "prior", "avg")] + [("MI", "a"), ("MI", "b")]
SIG_COMBOS = [(f, c) for f in ("B2", "B3", "B4", "B5") for c in ("abs", "rel")]
EXTRA = {"opt": (), "MI": (), "D1": ("G",), "D2": ("c", "Pi0"), "D3": ("rho",), "B2": ("G",), "B3": ("rho",), "B4": ("lam1",),
         "B5": ()}


def _parse(k):
    if k == "All":
        return "All"
    inv = {"Empty": (0, 0, 0), "lower ray": (1, 0, 0), "upper ray": (0, 1, 0), "two rays": (1, 1, 0), "window": (0, 0, 1)}
    return inv[k] if k in inv else tuple(int(v) for v in k.strip("()").split(","))


def allowed_sets():
    A = {("opt", "post"): {LR, EMP}, ("opt", "prior"): {"All", UR, EMP}, ("opt", "avg"): {"All", UR, EMP},
         ("MI", "a"): {"All", UR, EMP}, ("MI", "b"): {"All", UR, EMP}}
    a8 = json.load(open(os.path.join(RES, "t12_a8.json")))
    for f in ("D1", "D2", "D3"):
        for m in ("post", "prior", "avg"):
            A[(f, m)] = {_parse(k) for k in a8["families"][f][m]["classes"]}
    A.update(SIG_ALLOWED)
    return A


ALLOWED = allowed_sets()


def draw(rng, fam):
    U = lambda: float(10.0**rng.uniform(-2, 2))
    p = {"lam": U(), "Pi": U()} if fam.startswith("B") else {"lam": U(), "Sig": U(), "Pi": U()}
    for k in EXTRA[fam]:
        p[k] = float(2 * 10.0**rng.uniform(-4, 0)) if k == "c" else U()
    return p


def tols(A, rng):
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]] if mp.isfinite(v) and v > 0]
    if not crit:      # monotone 0 -> oo (not covered by the pre-registration): curve values at log-uniform sweep points
        sh = A["curve"].shift
        return [A["curve"].f(mp.power(10, sh + mp.mpf(float(x)))) for x in rng.uniform(-20, 20, 200)], 0
    lo, hi = float(mp.log10(min(crit) / 2)), float(mp.log10(2 * max(crit)))
    out = [mp.power(10, mp.mpf(float(x))) for x in rng.uniform(lo, hi, 100)]
    for i in range(100):
        cv = crit[int(rng.integers(len(crit)))]
        out.append(cv if i < 20 else cv * (1 + mp.mpf(float(rng.uniform(-1, 1))) * mp.mpf("1e-6")))
    return out, len(crit)


def job(args):
    fam, met, p, seed = args
    rng = np.random.default_rng(seed)
    t0 = time.time()
    A = analyse_sig(fam, met, p) if fam.startswith("B") else analyse_dt(fam, met, p)
    al = ALLOWED[(fam, met)]
    R2s, ncrit = tols(A, rng)
    counts, flagged, persist = {}, 0, []
    for R2 in R2s:
        ci = route_i(A, R2, EQ)
        try:
            cii, _ = route_ii(A, R2, prec="fl")
        except Exception as e:  # noqa: BLE001  (float failure counts as a flag)
            cii = f"float error: {type(e).__name__}"
        if ci != cii or ci not in al or cii not in al:
            flagged += 1
            with mp.workdps(60):
                ci2 = route_i(A, R2, EQ)
                cii2, _ = route_ii(A, R2, prec="mp")
            if ci2 != cii2 or ci2 not in al:
                persist.append({"p": p, "R2": R2, "route_i": name(ci2), "route_ii": name(cii2), "float_route_i": name(ci),
                                "float_route_ii": name(cii) if not isinstance(cii, str) or cii == "All" else cii})
            ci = ci2
        counts[name(ci)] = counts.get(name(ci), 0) + 1
    return {"combo": f"{fam} {met}", "counts": counts, "flagged": flagged, "persist": persist, "n_tp": len(A["turns"]),
            "kinds": "-".join(t["kind"] for t in A["turns"]) or "none", "limit_ok": all(A["limit_check"]),
            "n_crit": ncrit, "seconds": time.time() - t0}


def main():
    t0 = time.time()
    rng = np.random.default_rng(12100)
    jobs = []
    for fam, met in DT_COMBOS + SIG_COMBOS:
        for _ in range(N):
            jobs.append((fam, met, draw(rng, fam), int(rng.integers(2**63))))
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=5)
    R = {"N": N, "by": {}, "persist": []}
    for fam, met in DT_COMBOS + SIG_COMBOS:
        k = f"{fam} {met}"
        rr = [r for r in res if r["combo"] == k]
        cnt, kh = {}, {}
        for r in rr:
            for c_, v in r["counts"].items():
                cnt[c_] = cnt.get(c_, 0) + v
            kh[r["kinds"]] = kh.get(r["kinds"], 0) + 1
        per = [x for r in rr for x in r["persist"]]
        R["by"][k] = {"curves": len(rr), "classifications": sum(cnt.values()), "classes": cnt, "kinds_hist": kh,
                      "allowed": sorted(name(c) for c in ALLOWED[(fam, met)]), "flagged": sum(r["flagged"] for r in rr),
                      "persisting": len(per), "n_limit_fail": sum(not r["limit_ok"] for r in rr),
                      "n_no_crit_curves": sum(r["n_crit"] == 0 for r in rr), "seconds": sum(r["seconds"] for r in rr),
                      "pass": len(per) == 0}
        R["persist"] += per[:20]
        print(k, R["by"][k]["classes"], "flagged", R["by"][k]["flagged"], "persisting", len(per), flush=True)
    R["total"] = sum(v["classifications"] for v in R["by"].values())
    R["pass"] = all(v["pass"] for v in R["by"].values())
    R["seconds"] = time.time() - t0
    print("Part C", "PASS" if R["pass"] else "FAIL", R["total"])
    save_json(R, "t12_blind.json" if N == 1000 else f"t12_blind_n{N}.json")


if __name__ == "__main__":
    main()
