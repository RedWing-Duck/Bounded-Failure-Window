"""T11.3: power-normalized OU family — turning points, unimodality, limits, classes, duality, independent routes,
spectral dominance."""
import os
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t11_common import (P_are, P_pow, P_wiener, analyse_with_limits, bound_pow, classify, limits_pow, name, omega_star,
                        power_curve, save_json, sign_changes_spectra, v_pow)

NSET = int(os.environ.get("T11_NSET", "300"))
BETAS = [mp.mpf(k) / 20 for k in range(-40, 81)] + [c + s * mp.mpf(e) for c in (0, 2) for e in ("1e-6", "1e-3") for s in (-1, 1)]


def regime(beta):
    return "le0" if beta <= 0 else ("ge2" if beta >= 2 else "mid")


def job(args):
    bi, p, seed = args
    beta = BETAS[bi]
    K, lam, Sig = (mp.mpf(x) for x in (p["K"], p["lam"], p["Sig"]))
    Lm, Lp, xm, xp = limits_pow(beta, K, lam, Sig)
    A = analyse_with_limits(power_curve(beta, K, lam, Sig), Lm, Lp, xm, xp)
    tps = A["turns"]
    rg = regime(beta)
    tp_ok = (len(tps) == 0) if rg != "mid" else (len(tps) >= 1 and tps[0]["kind"] == "max")
    out = {"beta": beta, "p": p, "n_tp": len(tps), "kinds": [t["kind"] for t in tps], "tp_ok": tp_ok,
           "limit_check": A["limit_check"]}
    # limits (mid only)
    if rg == "mid":
        Pmax = max(t["value"] for t in tps) if tps else None
        P1 = P_pow(1 / lam, beta, K, lam, Sig)
        lim = []
        for rho in (mp.mpf("1e-10"), mp.mpf("1e10")):
            tau = rho / lam
            Pv, bd = P_pow(tau, beta, K, lam, Sig), bound_pow(tau, beta, K, lam, Sig)
            appl = bd < mp.mpf("1e-3") * P1
            ok = Pv <= bd and (not appl or (Pmax is not None and Pv < mp.mpf("1e-3") * Pmax))
            lim.append({"rho": rho, "P": Pv, "bound": bd, "applicable": bool(appl), "pass": bool(ok)})
        out["limits"] = lim
        Pref = Pmax if Pmax is not None else max(Lm, Lp)
    else:
        Pref = Lm if rg == "le0" else Lp
    # classes
    rng = np.random.default_rng(seed)
    tols = [Pref * mp.power(10, mp.mpf(float(x))) for x in rng.uniform(-3, float(mp.log10(2)), 7)]
    tols += [Pref * (1 - mp.mpf("1e-6")), Pref, Pref * (1 + mp.mpf("1e-6"))]
    allowed = {"le0": {(1, 0, 0), (0, 0, 0)}, "ge2": {(0, 1, 0), (0, 0, 0)}}.get(rg)
    cls_bad, counts = [], {}
    for R2 in tols:
        r = classify(A, R2)
        c1, c2 = r["route_i"], r["route_ii"]
        okc = c1 == c2 and (c1 in allowed if rg != "mid" else (c1 == (0, 0, 0) or (c1 != "All" and c1[0] == 0 and c1[1] == 0 and c1[2] >= 1)))
        counts[name(c1)] = counts.get(name(c1), 0) + 1
        if not okc:
            cls_bad.append({"R2": R2, "route_i": name(c1), "route_ii": name(c2)})
    out["classes"] = counts
    out["class_bad"] = cls_bad
    return out


def dual_job(seed):
    rng = np.random.default_rng(seed)
    beta = mp.mpf(float(rng.uniform(-2, 4)))
    K, lam, Sig = (mp.mpf(float(10.0**rng.uniform(-2, 2))) for _ in range(3))
    tau = mp.mpf(float(10.0**rng.uniform(-10, 10))) / lam
    a = P_pow(tau, beta, K, lam, Sig)
    b = P_pow(1 / (lam**2 * tau), 2 - beta, K * lam**(2 - 2 * beta), lam, Sig)
    return abs(a - b) / a


def route_job(args):
    beta, seed = args
    rng = np.random.default_rng(seed)
    K, lam, Sig = (mp.mpf(float(10.0**rng.uniform(-2, 2))) for _ in range(3))
    rows = []
    for lab, tau in (("random", mp.mpf(float(10.0**rng.uniform(-4, 4))) / lam), ("lam tau = 1", 1 / lam)):
        v = v_pow(tau, beta, K)
        p1 = P_pow(tau, beta, K, lam, Sig)
        p2, j, conv = P_are(tau, lam, Sig, v)
        p3 = P_wiener(tau, lam, Sig, v)
        e = max(abs(p1 - p2) / p1, abs(p1 - p3) / p1)
        rows.append({"beta": beta, "tau": lab, "err": e, "conv": conv, "pass": bool(conv and e <= mp.mpf("1e-8"))})
    return rows


def spec_job(args):
    beta, seed = args
    rng = np.random.default_rng(seed)
    K, lam = (mp.mpf(float(10.0**rng.uniform(-2, 2))) for _ in range(2))
    a, b = sorted(rng.uniform(-10, 10, 2))
    t1, t2 = mp.power(10, mp.mpf(float(a))) / lam, mp.power(10, mp.mpf(float(b))) / lam
    n, br = sign_changes_spectra(t1, t2, beta, K)
    want = 1 if 0 < beta < 2 else 0
    ok = n == want
    if ok and want == 1:
        ws = omega_star(t1, t2, beta)
        ok = ws is not None and br[0] <= ws <= br[1]
    return {"beta": beta, "n": n, "pass": bool(ok)}


def main():
    t0 = time.time()
    rng = np.random.default_rng(11003)
    jobs = []
    for bi in range(len(BETAS)):
        for _ in range(NSET):
            p = {k: float(10.0**rng.uniform(-2, 2)) for k in ("lam", "Sig", "K")}
            jobs.append((bi, p, int(rng.integers(2**63))))
    dual_seeds = [int(rng.integers(2**63)) for _ in range(1000)]
    route_args = [(mp.mpf(b), int(rng.integers(2**63))) for b in ("-1", "0.5", "1.5", "3") for _ in range(100)]
    spec_args = [(mp.mpf(k) / 4, int(rng.integers(2**63))) for k in range(-8, 17) for _ in range(1000)]
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=20)
        print(f"  families done {time.time() - t0:.0f}s", flush=True)
        dual = pool.map(dual_job, dual_seeds, chunksize=50)
        routes = [r for rr in pool.map(route_job, route_args, chunksize=5) for r in rr]
        print(f"  routes done {time.time() - t0:.0f}s", flush=True)
        spec = pool.map(spec_job, spec_args, chunksize=50)
    R = {"by_beta": [], "tp_fail": 0, "class_fail": 0, "limit_fail": 0, "limit_applicable": 0}
    hist_mid = {}
    for bi, beta in enumerate(BETAS):
        rr = [r for r in res if r["beta"] == beta]
        h = {}
        for r in rr:
            h[r["n_tp"]] = h.get(r["n_tp"], 0) + 1
        cl = {}
        for r in rr:
            for k, v in r["classes"].items():
                cl[k] = cl.get(k, 0) + v
        tpf = sum(not r["tp_ok"] for r in rr)
        cf = sum(len(r["class_bad"]) for r in rr)
        lf = sum(sum(not x["pass"] for x in r.get("limits", [])) for r in rr)
        la = sum(sum(x["applicable"] for x in r.get("limits", [])) for r in rr)
        R["tp_fail"] += tpf
        R["class_fail"] += cf
        R["limit_fail"] += lf
        R["limit_applicable"] += la
        if 0 < beta < 2:
            for k, v in h.items():
                hist_mid[k] = hist_mid.get(k, 0) + v
        R["by_beta"].append({"beta": beta, "regime": regime(beta), "tp_hist": h, "classes": cl, "tp_fail": tpf, "class_fail": cf,
                             "limit_fail": lf, "limit_applicable": la,
                             "limit_check_fail": sum(not all(r["limit_check"]) for r in rr),
                             "class_bad_examples": [x for r in rr for x in r["class_bad"]][:5],
                             "tp_bad_examples": [{"p": r["p"], "n_tp": r["n_tp"], "kinds": r["kinds"]} for r in rr if not r["tp_ok"]][:5]})
    R["unimodality_hist_0_lt_beta_lt_2"] = hist_mid
    R["duality_max_rel"] = max(dual)
    R["duality_pass"] = max(dual) <= mp.mpf("1e-30")
    R["routes"] = {"n": len(routes), "max_err": max(r["err"] for r in routes), "n_fail": sum(not r["pass"] for r in routes),
                   "fails": [r for r in routes if not r["pass"]][:10]}
    R["routes"]["pass"] = R["routes"]["n_fail"] == 0
    sp_by = {}
    for s in spec:
        k = str(s["beta"])
        e = sp_by.setdefault(k, {"n": 0, "fail": 0, "changes": {}})
        e["n"] += 1
        e["fail"] += int(not s["pass"])
        e["changes"][s["n"]] = e["changes"].get(s["n"], 0) + 1
    R["spectral"] = {"by_beta": sp_by, "n_fail": sum(not s["pass"] for s in spec)}
    R["spectral"]["pass"] = R["spectral"]["n_fail"] == 0
    R["pass_tp"] = R["tp_fail"] == 0
    R["pass_classes"] = R["class_fail"] == 0
    R["pass_limits"] = R["limit_fail"] == 0
    R["pass"] = all([R["pass_tp"], R["pass_classes"], R["pass_limits"], R["duality_pass"], R["routes"]["pass"], R["spectral"]["pass"]])
    R["seconds"] = time.time() - t0
    for e in R["by_beta"]:
        if e["tp_fail"] or e["class_fail"] or e["limit_fail"]:
            print(f"beta={mp.nstr(e['beta'], 8)}: tp_fail {e['tp_fail']}, class_fail {e['class_fail']}, limit_fail {e['limit_fail']}, "
                  f"examples {e['class_bad_examples'][:2]} {e['tp_bad_examples'][:2]}")
    print(f"unimodality histogram (0 < beta < 2): {hist_mid}")
    print(f"turning points fail {R['tp_fail']}; classes fail {R['class_fail']}; limits fail {R['limit_fail']} "
          f"(applicable {R['limit_applicable']}); duality max rel {mp.nstr(R['duality_max_rel'], 3)}; routes max err "
          f"{mp.nstr(R['routes']['max_err'], 3)} fails {R['routes']['n_fail']}; spectral fails {R['spectral']['n_fail']}")
    print(f"T11.3: {'PASS' if R['pass'] else 'FAIL'}")
    save_json(R, "t11_3.json")


if __name__ == "__main__":
    main()
