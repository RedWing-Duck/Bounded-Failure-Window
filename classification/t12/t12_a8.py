"""A8 census (D1, D2, D3 x post/prior/avg; 2,000 sets each, seed 12008) with, on the same sets, the A2/A3/A4 numerical
checks (excess set at R^2 = F, post; first 1,000 sets of each family) and A7 (D1 sets with G > 2 F Pi, prior and avg)."""
import sys
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t12_common import analyse_dt, classify, dps_for, name, save_json

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
N_EXC = min(1000, N)
FAMS = ("D1", "D2", "D3")
METRICS = ("post", "prior", "avg")
EXTRA = {"D1": ("G",), "D2": ("c", "Pi0"), "D3": ("rho",)}


def draw(rng, fam):
    U = lambda: float(10.0**rng.uniform(-2, 2))
    p = {"lam": U(), "Sig": U(), "Pi": U()}
    for k in EXTRA[fam]:
        p[k] = float(2 * 10.0**rng.uniform(-4, 0)) if k == "c" else U()
    return p


def tolerances(A, rng):
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]] if mp.isfinite(v) and v > 0]
    tols = []
    for cv in crit:
        tols += [cv, cv * (1 + mp.mpf("1e-6")), cv * (1 - mp.mpf("1e-6"))]
    lo, hi = float(mp.log10(min(crit) / 2)), float(mp.log10(2 * max(crit)))
    while len(tols) < 10:
        tols.append(mp.power(10, mp.mpf(float(rng.uniform(lo, hi)))))
    return tols


def root_D1(G, F, Pi):
    """Delta t_E: tanh(G dt / 2) = F Pi dt, i.e. h(y) = tanh(y/2)/y = F Pi / G with y = G dt (bisection in log y)."""
    k = F * Pi / G
    lo, hi = mp.log(mp.mpf("1e-30")), mp.log(1 / k + 1)
    for _ in range(400):
        m = (lo + hi) / 2
        y = mp.exp(m)
        if mp.tanh(y / 2) / y > k:
            lo = m
        else:
            hi = m
        if hi - lo < mp.mpf("1e-50"):
            break
    return mp.exp((lo + hi) / 2) / G


def d3_cond(t, p):
    """Exact D3 excess condition (PREREG A4): phi < 1 and s(1 - phi)(rho(1 + phi) - 2) - 4 phi > 0; returns (bool, E)."""
    lam, Sig, Pi, rho = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi", "rho"))
    with mp.workdps(dps_for(lam * t)):
        phi = Sig / lam * Pi * t
        s = -mp.expm1(-2 * lam * t)
        E = s * (1 - phi) * (rho * (1 + phi) - 2) - 4 * phi
        return bool(phi < 1 and E > 0), E, s * (1 - phi) * abs(rho * (1 + phi) - 2) + 4 * phi


def excess_check(fam, p, A):
    """A2/A3/A4: classifier's excess set at R^2 = F (post metric) vs the prediction."""
    lam, Sig, Pi = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    F = Sig / lam
    C = classify(A, F)
    out = {"route_i": name(C["route_i"]), "route_ii": name(C["route_ii"]), "agree": C["agree"],
           "ends": [[None if e is None else float(e) for e in en] for en in C["ends"]]}
    if fam in ("D1", "D2"):
        if fam == "D1":
            G = mp.mpf(p["G"])
            nonempty = G > 2 * F * Pi
            dtE = root_D1(G, F, Pi) if nonempty else None
            out["G_over_2FPi"] = G / (2 * F * Pi)
        else:
            cc, P0 = mp.mpf(p["c"]), mp.mpf(p["Pi0"])
            kap = cc / (F * P0)
            nonempty = kap > 2
            dtE = (cc - 2 * F * P0) / ((2 - cc) * F * Pi) if nonempty else None
            out["kappa"] = kap
        pred = (1, 0, 0) if nonempty else (0, 0, 0)
        ok = C["route_i"] == pred and C["route_ii"] == pred
        if nonempty and ok:
            end = C["ends"][0][1]
            out["dtE"], out["end"] = dtE, end
            out["rel_err"] = abs(end - dtE) / dtE
            ok = out["rel_err"] <= mp.mpf("1e-12")
        out["pred"], out["pass"] = name(pred), bool(ok)
        return out
    # D3: compare membership with the exact condition at test points, and the condition at the ends
    rho = mp.mpf(p["rho"])
    u = 2 * Sig * Pi / lam**2
    xs_end = sorted(mp.log10(e) for en in C["ends"] for e in en if e is not None)
    l10 = mp.log10(lam)
    test = [mp.mpf(v) - l10 for v in np.linspace(-20, 20, 201)]
    test = [x for x in test if all(abs(x - xe) > mp.mpf("1e-8") for xe in xs_end)]
    if xs_end:
        test += [xs_end[0] - 1, xs_end[-1] + 1] + [(xs_end[i] + xs_end[i + 1]) / 2 for i in range(len(xs_end) - 1)]
    from t12_common import dt_funcs
    f, _ = dt_funcs("D3", "post", p)
    dis = 0
    for x in test:
        t = mp.power(10, x)
        cond, _, _ = d3_cond(t, p)
        with mp.workdps(dps_for(lam * t)):
            ins = bool(f(t) > F)
        dis += int(cond != ins)
    end_E = [abs(e[1]) / e[2] for e in (d3_cond(mp.power(10, xe), p) for xe in xs_end)]
    onset_pred = rho > 2 + u
    onset_obs = C["route_ii"] not in ("All",) and isinstance(C["route_ii"], tuple) and C["route_ii"][0] == 1
    out.update({"rho": rho, "u": u, "n_test": len(test), "n_disagree": dis, "max_rel_E_at_ends": max(end_E) if end_E else None,
                "onset_pred": bool(onset_pred), "onset_obs": bool(onset_obs), "rho_gt_2": bool(rho > 2),
                "pass": bool(dis == 0 and onset_pred == onset_obs and C["agree"])})
    return out


def job(args):
    fam, i, p, seed = args
    rng = np.random.default_rng(seed)
    t0 = time.time()
    lam, Sig, Pi = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    F = Sig / lam
    res = {"fam": fam, "i": i, "p": p, "metrics": {}}
    for met in METRICS:
        A = analyse_dt(fam, met, p)
        cls, agree_all = {}, True
        for R2 in tolerances(A, rng):
            C = classify(A, R2)
            agree_all &= C["agree"]
            k = name(C["route_i"])
            cls[k] = cls.get(k, 0) + 1
            if not C["agree"]:
                res.setdefault("disagree", []).append({"metric": met, "R2": R2, "route_i": name(C["route_i"]),
                                                      "route_ii": name(C["route_ii"])})
        res["metrics"][met] = {"kinds": [t["kind"] for t in A["turns"]], "thetas": [t["theta"] for t in A["turns"]],
                               "values": [t["value"] for t in A["turns"]], "limit_check": A["limit_check"],
                               "classes": cls, "agree": bool(agree_all)}
        if met == "post" and i < N_EXC:
            res["excess"] = excess_check(fam, p, A)
        if fam == "D1" and met in ("prior", "avg") and mp.mpf(p["G"]) > 2 * F * Pi:
            mins = [t["value"] for t in A["turns"] if t["kind"] == "min"]
            a7 = {"n_min": len(mins), "min_below_F": bool(mins and min(mins) < F)}
            if a7["min_below_F"]:
                C = classify(A, (min(mins) + F) / 2)
                a7.update({"class_i": name(C["route_i"]), "class_ii": name(C["route_ii"]),
                           "pass": C["route_i"] == (1, 1, 0) and C["route_ii"] == (1, 1, 0)})
            else:
                a7["pass"] = False
            res.setdefault("a7", {})[met] = a7
    res["seconds"] = time.time() - t0
    return res


def main():
    t0 = time.time()
    rng = np.random.default_rng(12008)
    jobs = []
    for fam in FAMS:
        for i in range(N):
            jobs.append((fam, i, draw(rng, fam), int(rng.integers(2**63))))
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=5)
    R = {"N": N, "families": {}}
    for fam in FAMS:
        rr = [r for r in res if r["fam"] == fam]
        F = {}
        for met in METRICS:
            hist, cls = {}, {}
            for r in rr:
                k = "-".join(r["metrics"][met]["kinds"]) or "none"
                hist[k] = hist.get(k, 0) + 1
                for c_, v in r["metrics"][met]["classes"].items():
                    cls[c_] = cls.get(c_, 0) + v
            F[met] = {"kinds_hist": hist, "classes": cls,
                      "n_disagree_sets": sum(not r["metrics"][met]["agree"] for r in rr),
                      "n_limit_fail": sum(not all(r["metrics"][met]["limit_check"]) for r in rr)}
        ex = [r["excess"] for r in rr if "excess" in r]
        F["excess"] = {"n": len(ex), "n_pass": sum(e["pass"] for e in ex),
                       "shapes": {s: sum(e["route_ii"] == s for e in ex) for s in {e["route_ii"] for e in ex}},
                       "fails": [dict(e, p=r["p"]) for r, e in ((r, r["excess"]) for r in rr if "excess" in r) if not e["pass"]][:20]}
        if fam in ("D1", "D2"):
            errs = [e["rel_err"] for e in ex if "rel_err" in e]
            F["excess_points"] = [{"p": r["p"], "F": mp.mpf(r["p"]["Sig"]) / mp.mpf(r["p"]["lam"]), "end": r["excess"]["end"],
                                   **({"G_over_2FPi": r["excess"]["G_over_2FPi"]} if fam == "D1" else {"kappa": r["excess"]["kappa"]})}
                                  for r in rr if "excess" in r and "end" in r["excess"]]
            F["excess"]["n_nonempty_pred"] = sum(e["pred"] == "lower ray" for e in ex)
            F["excess"]["max_rel_err"] = max(errs) if errs else None
        else:
            F["excess"]["n_onset_pred"] = sum(e["onset_pred"] for e in ex)
            F["excess"]["n_onset_obs"] = sum(e["onset_obs"] for e in ex)
            F["excess"]["n_rho_gt_2_no_onset"] = sum(e["rho_gt_2"] and not e["onset_obs"] for e in ex)
            F["excess"]["n_disagree_points"] = sum(e["n_disagree"] for e in ex)
            F["excess"]["n_test_points"] = sum(e["n_test"] for e in ex)
            me = [e["max_rel_E_at_ends"] for e in ex if e["max_rel_E_at_ends"] is not None]
            F["excess"]["max_rel_E_at_ends"] = max(me) if me else None
        if fam == "D1":
            for met in ("prior", "avg"):
                a7 = [r["a7"][met] for r in rr if "a7" in r]
                F["a7_" + met] = {"n_sets": len(a7), "n_pass": sum(a["pass"] for a in a7),
                                  "n_min_hist": {str(k): sum(a["n_min"] == k for a in a7) for k in sorted({a["n_min"] for a in a7})},
                                  "n_no_min_below_F": sum(not a["min_below_F"] for a in a7),
                                  "classes": {c_: sum(a.get("class_i") == c_ for a in a7) for c_ in {a.get("class_i") for a in a7}}}
        F["disagreements"] = [dict(d, p=r["p"]) for r in rr for d in r.get("disagree", [])][:50]
        F["seconds_total"] = sum(r["seconds"] for r in rr)
        R["families"][fam] = F
    R["census_pass"] = all(R["families"][f][m]["n_disagree_sets"] == 0 for f in FAMS for m in METRICS)
    R["A2_pass"] = R["families"]["D1"]["excess"]["n_pass"] == R["families"]["D1"]["excess"]["n"]
    R["A3_pass"] = R["families"]["D2"]["excess"]["n_pass"] == R["families"]["D2"]["excess"]["n"]
    R["A4_census_pass"] = R["families"]["D3"]["excess"]["n_pass"] == R["families"]["D3"]["excess"]["n"]
    R["A7_pass"] = all(R["families"]["D1"]["a7_" + m]["n_pass"] == R["families"]["D1"]["a7_" + m]["n_sets"] for m in ("prior", "avg"))
    R["sets"] = [{"fam": r["fam"], "p": r["p"], **{m: {k: r["metrics"][m][k] for k in ("kinds", "thetas", "values")} for m in METRICS}}
                 for r in res]
    R["seconds"] = time.time() - t0
    for k in ("census_pass", "A2_pass", "A3_pass", "A4_census_pass", "A7_pass"):
        print(k, R[k])
    for fam in FAMS:
        for met in METRICS:
            print(fam, met, R["families"][fam][met]["kinds_hist"], R["families"][fam][met]["classes"])
    save_json(R, "t12_a8.json" if N == 2000 else f"t12_a8_n{N}.json")


if __name__ == "__main__":
    main()
