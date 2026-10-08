"""T11.2: causal garbling realized by Monte Carlo (Prop. 4.4 / 4.5(b))."""
import time

import mpmath as mp
import numpy as np

from t11_common import P_stage2, save_json

lam, Sig, Pi = 1.0, 0.01, 1.0
NT = 4000
rng = np.random.default_rng(11002)
t0 = time.time()
R = {"pairs": []}
for t1, t2 in ((0.5, 2.0), (1.0, 10.0)):
    dt = min(t1, 1 / lam) / 200
    nb, ns = int(round(10 * max(t2, 1) / dt)), int(round(40 * max(t1, 1) / dt))
    a, b = 1 / t1, 1 / t2
    c = np.sqrt((t2**2 - t1**2) / Pi)
    kx = c / (t1 * t2 * (b - a))
    P1, P2 = (float(P_stage2(mp.mpf(t), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))) for t in (t1, t2))
    h1, h2 = 1 / t1 - lam, 1 / t2 - lam
    Rv1, Rv2 = 2 * Sig + 1 / (Pi * t1**2), 2 * Sig + 1 / (Pi * t2**2)
    K1, K2 = (h1 * P1 + 2 * Sig) / Rv1, (h2 * P2 + 2 * Sig) / Rv2
    lags = [0, int(round(t1 / 2 / dt)), int(round(t1 / dt)), int(round(2 * t1 / dt))]
    L = lags[-1] + 1
    ring = np.zeros((L, NT))
    s = rng.standard_normal(NT) * np.sqrt(Sig / lam)
    eta = rng.standard_normal(NT) * np.sqrt(1 / (2 * Pi * t2))
    xa, xb = np.zeros(NT), np.zeros(NT)
    sh1, sh2 = np.zeros(NT), np.zeros(NT)
    q_s, q_e, q_w = np.sqrt(2 * Sig * dt), np.sqrt(dt / (Pi * t2**2)), np.sqrt(dt)
    acc = {l: np.zeros(NT) for l in lags}
    e1, e2 = np.zeros(NT), np.zeros(NT)
    n_old = eta + kx * (b * xb - a * xa)
    for k in range(nb + ns):
        z = rng.standard_normal((3, NT))
        Y1_old, Y2_old = s + n_old, s + eta
        s_new = s - lam * s * dt + q_s * z[0]
        eta_new = eta - eta * dt / t2 + q_e * z[1]
        xa = xa - a * xa * dt + q_w * z[2]
        xb = xb - b * xb * dt + q_w * z[2]
        n_new = eta_new + kx * (b * xb - a * xa)
        Y1, Y2 = s_new + n_new, s_new + eta_new
        zd1 = (Y1 - Y1_old) + Y1_old * dt / t1
        zd2 = (Y2 - Y2_old) + Y2_old * dt / t2
        sh1 = sh1 - lam * sh1 * dt + K1 * (zd1 - h1 * sh1 * dt)
        sh2 = sh2 - lam * sh2 * dt + K2 * (zd2 - h2 * sh2 * dt)
        s, eta, n_old = s_new, eta_new, n_new
        ring[k % L] = n_new
        if k >= nb:
            for l in lags:
                acc[l] += n_new * ring[(k - l) % L]
            e1 += (s - sh1)**2
            e2 += (s - sh2)**2
    C0 = 1 / (2 * Pi * t1)
    ac = []
    for l in lags:
        per = acc[l] / ns
        m, se = per.mean(), per.std(ddof=1) / np.sqrt(NT)
        tgt = C0 * np.exp(-l * dt / t1)
        ac.append({"lag": l * dt, "estimate": m, "SE": se, "target": tgt, "z": (m - tgt) / se,
                   "pass": bool(abs(m - tgt) <= 3 * se and se <= 0.01 * C0)})
    m1, m2 = e1 / ns, e2 / ns
    mse1, se1 = m1.mean(), m1.std(ddof=1) / np.sqrt(NT)
    mse2, se2 = m2.mean(), m2.std(ddof=1) / np.sqrt(NT)
    dd = m1 - m2
    dm, dse = dd.mean(), dd.std(ddof=1) / np.sqrt(NT)
    ok2 = abs(mse1 - P1) <= 3 * se1 and se1 <= 0.01 * P1
    ok3 = dm > 3 * dse
    rec = {"tau1": t1, "tau2": t2, "dt": dt, "autocov": ac, "MSE1_on_Yprime": mse1, "SE1": se1, "P_tau1": P1,
           "z1": (mse1 - P1) / se1, "MSE2_on_y_tau2": mse2, "SE2": se2, "P_tau2": P2, "diff": dm, "diff_SE": dse,
           "pass_i": all(x["pass"] for x in ac), "pass_ii": bool(ok2), "pass_iii": bool(ok3)}
    rec["pass"] = rec["pass_i"] and rec["pass_ii"] and rec["pass_iii"]
    R["pairs"].append(rec)
    print(f"(tau1, tau2) = ({t1}, {t2}), dt = {dt}: autocov z = {[round(x['z'], 2) for x in ac]}; MSE1 = {mse1:.6g} +/- {se1:.2g} "
          f"vs P(tau1) = {P1:.6g} (z = {(mse1 - P1) / se1:+.2f}); MSE2 = {mse2:.6g} vs P(tau2) = {P2:.6g}; diff = {dm:.4g} "
          f"+/- {dse:.2g} -> {'PASS' if rec['pass'] else 'FAIL'}  ({time.time() - t0:.0f}s)", flush=True)
R["pass"] = all(p["pass"] for p in R["pairs"])
R["seconds"] = time.time() - t0
print(f"T11.2: {'PASS' if R['pass'] else 'FAIL'}")
save_json(R, "t11_2.json")
