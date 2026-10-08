"""T11.4: delay counterexample (Prop. 4.7) — MC, theta sweep, regression."""
import time

import mpmath as mp
import numpy as np

from t11_common import Curve, P_delay, ZREL, analyse_with_limits, classify, name, save_json, sf_match, sstar

t0 = time.time()
lam, Sig, Pi = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1)
F, s2 = Sig / lam, sstar(lam, Sig, Pi)
R = {}

# ---------------- Monte Carlo
rng = np.random.default_rng(11004)
NT, dt = 2000, 1e-3
ds = [0.0, 0.2, float(1 / mp.e), 1.0]
steps = [int(round(d / dt)) for d in ds]
L = max(steps) + 1
nb, ns = int(round(10 / dt)), int(round(20 / dt))
lf, Sf, Pf = 1.0, 0.01, 1.0
Gs = float(Pi * s2)
s = rng.standard_normal(NT) * np.sqrt(Sf / lf)
ring = np.zeros((L, NT))
ring[:] = s
sh = [np.zeros(NT) for _ in ds]
acc = [np.zeros(NT) for _ in ds]
for k in range(nb + ns):
    z = rng.standard_normal((2, NT))
    s = s - lf * s * dt + np.sqrt(2 * Sf * dt) * z[0]
    ring[k % L] = s
    for i, m in enumerate(steps):
        sd = ring[(k - m) % L]                       # s(t - d)
        dy = sd * dt + np.sqrt(dt / Pf) * z[1]
        sh[i] = sh[i] - lf * sh[i] * dt + Gs * (dy - sh[i] * dt)
        if k >= nb:
            acc[i] += (s - np.exp(-lf * m * dt) * sh[i])**2
mc = []
for i, (d, m) in enumerate(zip(ds, steps)):
    per = acc[i] / ns
    est, se = per.mean(), per.std(ddof=1) / np.sqrt(NT)
    tgt = float(P_delay(mp.mpf(m) * mp.mpf(dt), lam, Sig, Pi))
    mc.append({"d": d, "d_realized": m * dt, "estimate": est, "SE": se, "formula": tgt, "z": (est - tgt) / se,
               "pass": bool(abs(est - tgt) <= 3 * se and se <= 0.01 * tgt)})
    print(f"MC d = {d:.4f}: {est:.7g} +/- {se:.2g} vs {tgt:.7g} (z = {(est - tgt) / se:+.2f})", flush=True)
R["mc"] = {"rows": mc, "pass": all(r["pass"] for r in mc)}

# ---------------- theta sweep
f = lambda th: P_delay(th * mp.exp(-th), lam, Sig, Pi)
d_ = lambda th: 2 * lam * mp.exp(-2 * lam * th * mp.exp(-th)) * (F - s2) * (1 - th) * mp.exp(-th)
c = Curve(f, d_, lambda th: ZREL * abs(f(th)) / th, 0, [mp.mpf(0)], None, "delay theta")
A = analyse_with_limits(c, s2, s2, mp.mpf(-80), mp.mpf(80))
Pmax = P_delay(1 / mp.e, lam, Sig, Pi)
rows = []
for q in ("0.1", "0.5", "0.9"):
    R2 = s2 + mp.mpf(q) * (Pmax - s2)
    r = classify(A, R2)
    ok = r["route_i"] == (0, 0, 1) and r["route_ii"] == (0, 0, 1)
    rel = None
    if ok:
        a, b = r["ends"][0]
        rel = abs(a * mp.exp(-a) - b * mp.exp(-b)) / (a * mp.exp(-a))
        ok = rel <= mp.mpf("1e-12")
    rows.append({"q": q, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]), "ends": r["ends"], "d_rel_err": rel,
                 "pass": bool(ok)})
for lab, R2 in (("P(1/e)", Pmax), ("P(1/e)(1+1e-6)", Pmax * (1 + mp.mpf("1e-6")))):
    r = classify(A, R2)
    rows.append({"q": lab, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]),
                 "pass": r["route_i"] == (0, 0, 0) and r["route_ii"] == (0, 0, 0)})
R["sweep"] = {"turns": [(t["theta"], t["value"], t["kind"]) for t in A["turns"]], "limit_check": A["limit_check"], "rows": rows,
              "pass": all(x["pass"] for x in rows) and len(A["turns"]) == 1}
print("sweep:", [(x["q"], x["route_i"], x["route_ii"], x.get("d_rel_err")) for x in rows])

# ---------------- regression
reg = [("P(0)", P_delay(mp.mpf(0), lam, Sig, Pi), "0.0099505"), ("P(1/e)", Pmax, "0.0099763")]
R["regression"] = {"rows": [{"q": a, "computed": b, "stated": c_, "pass": sf_match(b, c_)} for a, b, c_ in reg]}
R["regression"]["pass"] = all(x["pass"] for x in R["regression"]["rows"])
print("regression:", [(x["q"], mp.nstr(x["computed"], 9), x["pass"]) for x in R["regression"]["rows"]])
R["pass"] = R["mc"]["pass"] and R["sweep"]["pass"] and R["regression"]["pass"]
R["seconds"] = time.time() - t0
print(f"T11.4: {'PASS' if R['pass'] else 'FAIL'}")
save_json(R, "t11_4.json")
