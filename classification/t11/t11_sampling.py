"""T11.6: integrate-and-dump sampling interval (Cor. 4.9) and the Delta-t continuum (record only)."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t11_common import samp_Q, samp_metrics, samp_p, save_json, sstar

t0 = time.time()
rng = np.random.default_rng(11006)


def vanloan_Q(dt, lam, Sig):
    M = mp.matrix(4, 4)
    Fm = [[-lam, 0], [1, 0]]
    Qc = [[2 * Sig, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            M[i, j] = -Fm[i][j] * dt
            M[i, j + 2] = Qc[i][j] * dt
            M[i + 2, j + 2] = Fm[j][i] * dt
    E = mp.expm(M)
    Phi = mp.matrix([[E[2 + j, 2 + i] for j in range(2)] for i in range(2)])     # transpose of block22
    B12 = mp.matrix([[E[i, 2 + j] for j in range(2)] for i in range(2)])
    return Phi * B12, Phi


def kf_fixed_point(dt, lam, Sig, Pi):
    phi, q11, q12, q22 = samp_Q(dt, lam, Sig)
    Phi = mp.matrix([[phi, 0], [(1 - phi) / lam, 0]])                          # I is reset each sample
    Q = mp.matrix([[q11, q12], [q12, q22]])
    H = mp.matrix([[0, 1 / dt]])
    Rn = 1 / (Pi * dt)
    P = Q.copy()
    for _ in range(100000):
        Pp = Phi * P * Phi.T + Q
        S = (H * Pp * H.T)[0, 0] + Rn
        Kg = Pp * H.T / S
        Pn = Pp - Kg * H * Pp
        if abs(Pn[0, 0] - P[0, 0]) < mp.mpf("1e-45") * abs(Pn[0, 0]):
            return Pn[0, 0]
        P = Pn
    return Pn[0, 0]


R = {}
# ---------------- internal check
ic = []
for i in range(20):
    lam, Sig, Pi = (mp.mpf(float(10.0**rng.uniform(-2, 2))) for _ in range(3))
    dt = mp.mpf(float(10.0**rng.uniform(-3, 2))) / lam
    p = samp_p(dt, lam, Sig, Pi)
    pk = kf_fixed_point(dt, lam, Sig, Pi)
    Qv, Phi = vanloan_Q(dt, lam, Sig)
    _, q11, q12, q22 = samp_Q(dt, lam, Sig)
    qerr = max(abs(Qv[0, 0] - q11) / q11, abs(Qv[0, 1] - q12) / abs(q12), abs(Qv[1, 1] - q22) / q22)
    perr = abs(p - pk) / p
    ic.append({"p_vs_kf_rel": perr, "Q_vs_vanloan_rel": qerr, "pass": bool(perr <= mp.mpf("1e-30") and qerr <= mp.mpf("1e-30"))})
R["internal"] = {"rows": ic, "pass": all(x["pass"] for x in ic), "max_p_err": max(x["p_vs_kf_rel"] for x in ic),
                 "max_Q_err": max(x["Q_vs_vanloan_rel"] for x in ic)}
print(f"internal: scalar p vs 2-state KF max rel {mp.nstr(R['internal']['max_p_err'], 3)}, Q vs Van Loan max rel "
      f"{mp.nstr(R['internal']['max_Q_err'], 3)}", flush=True)

# ---------------- MC validation
lam_f, Sig_f, Pi_f = 1.0, 0.01, 1.0
NT = 2000
mcrows = []
for Dt in (0.1, 1.0, 5.0):
    dt = min(Dt, 1 / lam_f) / 200
    per_int = int(round(Dt / dt))
    nb_int, ns_int = int(np.ceil(20 / Dt)), int(np.ceil(200 / Dt))
    pa, pb = (float(x) for x in samp_metrics(mp.mpf(Dt), mp.mpf(lam_f), mp.mpf(Sig_f), mp.mpf(Pi_f)))
    phi, q11, q12, q22 = (float(x) for x in samp_Q(mp.mpf(Dt), mp.mpf(lam_f), mp.mpf(Sig_f)))
    h = (1 - phi) / (lam_f * Dt)
    re = q22 / Dt**2 + 1 / (Pi_f * Dt)
    g = q12 / Dt
    Kg = (phi * h * pa + g) / (h**2 * pa + re)
    s = rng.standard_normal(NT) * np.sqrt(Sig_f / lam_f)
    sh = np.zeros(NT)
    acc_a, acc_b, nA, nB = np.zeros(NT), np.zeros(NT), 0, 0
    for k in range(nb_int + ns_int):
        I, W, s_prev = np.zeros(NT), np.zeros(NT), s.copy()
        sh_prev = sh.copy()
        for j in range(per_int):
            z = rng.standard_normal((2, NT))
            I += s * dt
            W += np.sqrt(dt) * z[1]
            s = s - lam_f * s * dt + np.sqrt(2 * Sig_f * dt) * z[0]
            if k >= nb_int:
                u = (j + 1) * dt if j + 1 < per_int else None
                if u is not None:                     # prediction from the previous sample, time u after it
                    acc_b += (s - np.exp(-lam_f * u) * sh_prev)**2
        zk = (I + W / np.sqrt(Pi_f)) / Dt
        sh = phi * sh_prev + Kg * (zk - h * sh_prev)
        if k >= nb_int:
            acc_a += (s - sh)**2
            acc_b += (s - sh)**2                      # u = 0 at the sample time itself
            nA += 1
            nB += per_int
    ea, eb = acc_a / nA, acc_b / nB
    ma, sa = ea.mean(), ea.std(ddof=1) / np.sqrt(NT)
    mb, sb = eb.mean(), eb.std(ddof=1) / np.sqrt(NT)
    rec = {"Dt": Dt, "a_est": ma, "a_SE": sa, "a_formula": pa, "a_z": (ma - pa) / sa, "b_est": mb, "b_SE": sb, "b_formula": pb,
           "b_z": (mb - pb) / sb,
           "pass": bool(abs(ma - pa) <= 3 * sa and sa <= 0.02 * pa and abs(mb - pb) <= 3 * sb and sb <= 0.02 * pb)}
    mcrows.append(rec)
    print(f"MC Dt = {Dt}: (a) {ma:.6g} +/- {sa:.2g} vs {pa:.6g} (z {rec['a_z']:+.2f}); (b) {mb:.6g} +/- {sb:.2g} vs {pb:.6g} "
          f"(z {rec['b_z']:+.2f})  ({time.time() - t0:.0f}s)", flush=True)
R["mc"] = {"rows": mcrows, "pass": all(r["pass"] for r in mcrows)}

# ---------------- Cor. 4.9
cv = {"a": 0, "b": 0}
worst = {"a": mp.mpf(1), "b": mp.mpf(1)}
for i in range(1000):
    lam, Sig, Pi = (mp.mpf(float(10.0**rng.uniform(-2, 2))) for _ in range(3))
    dt = mp.mpf(float(10.0**rng.uniform(-3, 2))) / lam
    a1, b1 = samp_metrics(dt, lam, Sig, Pi)
    for m in range(2, 11):
        am, bm = samp_metrics(m * dt, lam, Sig, Pi)
        cv["a"] += int(not am >= a1 * (1 - mp.mpf("1e-12")))
        cv["b"] += int(not bm >= b1 * (1 - mp.mpf("1e-12")))
        worst["a"] = min(worst["a"], am / a1)
        worst["b"] = min(worst["b"], bm / b1)
R["cor49"] = {"violations_a": cv["a"], "violations_b": cv["b"], "min_ratio_a": worst["a"], "min_ratio_b": worst["b"],
              "pass": cv["a"] == 0 and cv["b"] == 0}
print(f"Cor 4.9: violations (a) {cv['a']}, (b) {cv['b']}; min ratio P(m dt)/P(dt): (a) {mp.nstr(worst['a'], 12)}, "
      f"(b) {mp.nstr(worst['b'], 12)}", flush=True)


# ---------------- continuum (record only)
def cont_job(seed):
    with mp.workdps(60):
        r = np.random.default_rng(seed)
        lam, Sig, Pi = (mp.mpf(float(10.0**r.uniform(-2, 2))) for _ in range(3))
        nonmono = []
        for x in np.linspace(-3, 2, 400):
            dt = mp.power(10, mp.mpf(float(x))) / lam
            da = mp.diff(lambda y: samp_metrics(y, lam, Sig, Pi)[0], dt)
            db = mp.diff(lambda y: samp_metrics(y, lam, Sig, Pi)[1], dt)
            if da <= 0 or db <= 0:
                nonmono.append({"lam_dt": float(x), "dPa": da, "dPb": db})
        lim = samp_metrics(mp.mpf("1e-8") / lam, lam, Sig, Pi)[0] / sstar(lam, Sig, Pi) - 1
        return {"lam": lam, "Sig": Sig, "Pi": Pi, "nonmono": nonmono, "limit_rel": lim}


with Pool(4) as pool:
    cont = pool.map(cont_job, [int(rng.integers(2**63)) for _ in range(1000)], chunksize=10)
nm = [c for c in cont if c["nonmono"]]
R["continuum"] = {"n_sets": len(cont), "n_points": 400 * len(cont), "n_nonmonotone_sets": len(nm),
                  "n_nonpositive_derivatives": sum(len(c["nonmono"]) for c in cont), "examples": nm[:10],
                  "limit_rel_max": max(abs(c["limit_rel"]) for c in cont), "limit_rel_min": min(c["limit_rel"] for c in cont)}
print(f"continuum: {len(nm)} non-monotone sets out of {len(cont)}; Delta t -> 0 limit P_a/s*^2 - 1 in "
      f"[{mp.nstr(R['continuum']['limit_rel_min'], 3)}, {mp.nstr(R['continuum']['limit_rel_max'], 3)}]")
R["pass"] = R["internal"]["pass"] and R["mc"]["pass"] and R["cor49"]["pass"]
R["seconds"] = time.time() - t0
print(f"T11.6: {'PASS' if R['pass'] else 'FAIL'}")
save_json(R, "t11_6.json")
