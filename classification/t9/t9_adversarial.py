"""T9.6: adversarial checks — linear case, extremes, near-critical tolerances, G -> 0+, Monte Carlo."""
import time

import mpmath as mp
import numpy as np

from t9_common import (P_opt, analyse, classify, crit, name, opt_sweep, relay, relay_sweep, save_json, tau_R,
                       tau_star_R)

t0 = time.time()
R = {}


def P_rat_f(tau, lam, Sig, Pi):
    b = 4 * Sig * tau + 2 * lam / Pi
    D = b * b + 8 * Sig * (1 - lam * tau)**2 / Pi
    return 4 * Sig / (Pi * (b + np.sqrt(D)))


def P_naive_f(tau, lam, Sig, Pi):
    A = (1 - lam * tau)**2
    b = 4 * Sig * tau + 2 * lam / Pi
    with np.errstate(all="ignore"):
        return (-b + np.sqrt(b * b + 8 * Sig * A / Pi)) / (2 * A)


def relay_f(tau, lam, Sig, Pi, G):
    a = lam + G
    return (Sig + G**2 / (2 * Pi * (1 + a * tau))) / a


# ---------------- (a) linear case
rng = np.random.default_rng(9006)
sets = [(1.0, 0.01, 1.0)] + [tuple(10.0**rng.uniform(-3, 3, size=3)) for _ in range(100)]
worst_rat, worst_naive, n = 0.0, 0.0, 0
for lam, Sig, Pi in sets:
    for k in range(-10, 11):
        lt = mp.mpf(1) + k * mp.mpf("1e-13")
        tau = float(lt / mp.mpf(lam))
        ref = P_opt(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))
        e = float(abs(mp.mpf(P_rat_f(tau, lam, Sig, Pi)) - ref) / ref)
        worst_rat = max(worst_rat, e)
        pn = P_naive_f(tau, lam, Sig, Pi)
        en = float(abs(mp.mpf(pn) - ref) / ref) if np.isfinite(pn) else float("inf")
        worst_naive = max(worst_naive, en)
        n += 1
scan = []
for e10 in range(-16, 0):
    lt = 1 + 10.0**e10
    tau = lt
    ref = P_opt(mp.mpf(tau), mp.mpf(1), mp.mpf("0.01"), mp.mpf(1))
    pn = P_naive_f(tau, 1.0, 0.01, 1.0)
    en = float(abs(mp.mpf(pn) - ref) / ref) if np.isfinite(pn) else float("inf")
    er = float(abs(mp.mpf(P_rat_f(tau, 1.0, 0.01, 1.0)) - ref) / ref)
    scan.append({"one_minus_lam_tau": float(abs(1 - mp.mpf(tau))), "naive_rel_err": en, "rational_rel_err": er})
fail_naive = [s["one_minus_lam_tau"] for s in scan if not s["naive_rel_err"] <= 1e-6]
R["a"] = {"n": n, "worst_rational": worst_rat, "worst_naive": worst_naive, "scan": scan,
          "naive_fails_up_to": max(fail_naive) if fail_naive else None, "pass": worst_rat <= 1e-12}
print(f"(a) linear case: {n} evaluations; rationalized float64 worst rel err {worst_rat:.3g}; naive worst {worst_naive:.3g}; "
      f"naive rel err > 1e-6 for |1 - lam tau| up to {R['a']['naive_fails_up_to']}")
for s_ in scan:
    print(f"    |1-lam tau| = {s_['one_minus_lam_tau']:.1e}: naive {s_['naive_rel_err']:.2e}, rationalized {s_['rational_rel_err']:.2e}")


# ---------------- shared: T9.4 tolerance lists and predictions
def relay_rows(lam, Sig, Pi, G):
    c = crit(lam, Sig, Pi, G)
    H, Vw, F = c["H_G"], c["V_w"], c["F"]
    d = mp.mpf("1e-6")
    rows = [H / 2, H, H * (1 - d), H * (1 + d), (H + Vw) / 2, Vw, Vw * (1 - d), Vw * (1 + d), 1.5 * Vw, F]
    pred = lambda r2: "All" if r2 <= H else ("lower ray" if r2 < Vw else "Empty")
    return [(r2, pred(r2)) for r2 in rows]


def opt_rows(lam, Sig, Pi):
    s2 = crit(lam, Sig, Pi, mp.mpf(1))["s2"]
    d = mp.mpf("1e-6")
    rows = [s2 * mp.mpf("1e-3"), s2 / 2, s2, s2 * (1 - d), s2 * (1 + d), 1.5 * s2]
    return [(r2, "lower ray" if r2 < s2 else "Empty") for r2 in rows]


def check_classes(A, rows):
    mism = []
    for r2, want in rows:
        got = name(classify(A, r2)["class"])
        if got != want:
            mism.append({"R2": float(r2), "got": got, "expected": want})
    return mism


# ---------------- (b) extremes
bm, bfloat, nb = [], 0.0, 0
for Sig in (1e-12, 1e12):
    lam, Pi = 1.0, 1.0
    for G in (1e-3, 1.0, 1e3):
        lm, Sm, Pm, Gm = (mp.mpf(x) for x in (lam, Sig, Pi, G))
        for tau in (1e-9, 1e9):
            tm = mp.mpf(tau)
            e1 = float(abs(mp.mpf(P_rat_f(tau, lam, Sig, Pi)) - P_opt(tm, lm, Sm, Pm)) / P_opt(tm, lm, Sm, Pm))
            e2 = float(abs(mp.mpf(relay_f(tau, lam, Sig, Pi, G)) - relay(tm, lm, Sm, Pm, Gm)) / relay(tm, lm, Sm, Pm, Gm))
            bfloat = max(bfloat, e1, e2)
            nb += 1
        bm += check_classes(analyse(*relay_sweep(lm, Sm, Pm, Gm), lm), relay_rows(lm, Sm, Pm, Gm))
    bm += check_classes(analyse(*opt_sweep(lm, Sm, Pm), lm), opt_rows(lm, Sm, Pm))
R["b"] = {"float_vs_mp_worst": bfloat, "n_float": nb, "class_mismatches": bm, "pass": bfloat <= 1e-12 and not bm}
print(f"(b) extremes: float64 vs mp worst rel err {bfloat:.3g} over {nb} evaluations; class mismatches {len(bm)}")

# ---------------- (c) near-critical tolerances, worked example
lm, Sm, Pm, Gm = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1), mp.mpf("0.5")
c = crit(lm, Sm, Pm, Gm)
Arel = analyse(*relay_sweep(lm, Sm, Pm, Gm), lm)
Aopt = analyse(*opt_sweep(lm, Sm, Pm), lm)
cm, nc = [], 0
for key in ("H_G", "V_w", "s2"):
    for dl in ("1e-6", "1e-9", "1e-12"):
        for sgn in (-1, 1):
            r2 = c[key] * (1 + sgn * mp.mpf(dl))
            if key == "s2":
                want = "lower ray" if r2 < c["s2"] else "Empty"
                A = Aopt
            else:
                want = "All" if r2 <= c["H_G"] else ("lower ray" if r2 < c["V_w"] else "Empty")
                A = Arel
            got = name(classify(A, r2)["class"])
            nc += 1
            if got != want:
                cm.append({"crit": key, "delta": sgn * float(dl), "got": got, "expected": want})
R["c"] = {"n": nc, "mismatches": cm, "pass": not cm}
print(f"(c) near-critical: {nc} tolerances, mismatches {len(cm)}")

# ---------------- (d) G -> 0+
F = Sm / lm
dtab, dpass = [], True
for k in range(1, 13):
    G = mp.power(10, -k)
    A = analyse(*relay_sweep(lm, Sm, Pm, G), lm)
    got = [name(classify(A, r2)["class"]) for r2 in (F * (1 - mp.mpf("1e-3")), F * (1 - mp.mpf("1e-6")), F,
                                                      F * (1 + mp.mpf("1e-6")))]
    dtab.append({"G": float(G), "classes": got})
    if k >= 8 and got != ["All", "All", "Empty", "Empty"]:
        dpass = False
    print(f"(d) G = 1e-{k}: {got}")
R["d"] = {"table": dtab, "pass": dpass}

# ---------------- (e) Monte Carlo
lam, Sig, Pi, G = 1.0, 0.01, 1.0, 0.5
a = lam + G
mc = []
rng = np.random.default_rng(9061)
NT = 2000
for tau in (0.1, 1.0, 10.0):
    dt = min(tau / 100, 2e-3)
    Tb, Ts = 10 * max(tau, 1), 20 * max(tau, 1)
    nb_, ns_ = int(round(Tb / dt)), int(round(Ts / dt))
    h = 1 / tau - lam
    Rv = 2 * Sig + 1 / (Pi * tau**2)
    P = float(P_opt(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi)))
    K = (h * P + 2 * Sig) / Rv
    x = np.zeros(NT)
    eta = rng.standard_normal(NT) * np.sqrt(1 / (2 * Pi * tau))
    s = rng.standard_normal(NT) * np.sqrt(Sig / lam)
    shat = np.zeros(NT)
    acc_x, acc_e = np.zeros(NT), np.zeros(NT)
    qs, qe, qx = np.sqrt(2 * Sig * dt), np.sqrt(dt / (Pi * tau**2)), np.sqrt(2 * Sig * dt)
    for n_ in range(nb_ + ns_):
        z = rng.standard_normal((3, NT))
        # relay error
        x = x + (-a * x + G * eta) * dt + qx * z[0]
        # signal and optimal (differenced) filter
        y0 = s + eta
        s_new = s - lam * s * dt + qs * z[1]
        eta_new = eta - eta * dt / tau + qe * z[2]
        dy = (s_new + eta_new) - y0
        zdt = dy + y0 * dt / tau
        shat = shat - lam * shat * dt + K * (zdt - h * shat * dt)
        s, eta = s_new, eta_new
        if n_ >= nb_:
            acc_x += x * x
            acc_e += (s - shat)**2
    for kind, acc, formula in (("relay", acc_x, float(relay(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi),
                                                            mp.mpf(G)))),
                               ("optimal", acc_e, P)):
        per = acc / ns_
        est, se = per.mean(), per.std(ddof=1) / np.sqrt(NT)
        ok_ = se <= 0.02 * formula and abs(est - formula) <= 3 * se
        mc.append({"tau": tau, "filter": kind, "estimate": est, "SE": se, "formula": formula,
                   "z": (est - formula) / se, "se_rel": se / formula, "dt": dt, "pass": bool(ok_)})
        print(f"(e) tau = {tau}, {kind}: MC {est:.6g} +/- {se:.2g} (SE {100 * se / formula:.2f}%), formula {formula:.6g}, "
              f"z = {(est - formula) / se:+.2f} {'ok' if ok_ else 'FAIL'}")
R["e"] = {"rows": mc, "pass": all(r["pass"] for r in mc)}

R["pass"] = all(R[k]["pass"] for k in "abcde")
R["seconds"] = time.time() - t0
print(f"T9.6: {'PASS' if R['pass'] else 'FAIL'}  parts {{{', '.join(k + ': ' + str(R[k]['pass']) for k in 'abcde')}}}")
save_json(R, "t9_6.json")
