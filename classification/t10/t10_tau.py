"""T10.6: optimal filter and relay along matched-variance tau (Plan A6)."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np
import sympy as sp

from classify import classify, name
from t10_common import ZREL, Curve, T, _sgn, analyse, grid, save_json, sf_match

_t, _l, _S, _v = sp.symbols("tau lambda Sigma v", positive=True)
_A = (1 - _l * _t)**2 / _t
_B = 4 * (_S + _l * _v)
P_SYM = 8 * _S * _v / (_B + sp.sqrt(_B**2 + 16 * _S * _v * _A))
P_f = sp.lambdify((_t, _l, _S, _v), P_SYM, "mpmath")
dP_f = sp.lambdify((_t, _l, _S, _v), sp.diff(P_SYM, _t), "mpmath")


def P_rat(tau, lam, Sig, v):
    A = (1 - lam * tau)**2 / tau
    B = 4 * (Sig + lam * v)
    return 8 * Sig * v / (B + mp.sqrt(B**2 + 16 * Sig * v * A))


def P_are(tau, lam, Sig, v):
    """Regularized 2-state ARE in mp (dps 100), eps scaled per set, converged to 1e-12 relative step change."""
    with mp.workdps(100):
        lam, Sig, v, tau = (mp.mpf(x) for x in (lam, Sig, v, tau))
        e0 = (2 * Sig + 2 * v / tau) / (lam + 1 / tau)**2
        prev = None
        for j in range(2, 26):
            eps = e0 * mp.power(10, -4 * j)
            H = mp.matrix(4, 4)
            A = [[-lam, 0], [0, -1 / tau]]
            Q = [[2 * Sig, 0], [0, 2 * v / tau]]
            for i in range(2):
                for k in range(2):
                    H[i, k] = A[k][i]
                    H[i, k + 2] = -1 / eps
                    H[i + 2, k] = -Q[i][k]
                    H[i + 2, k + 2] = -A[i][k]
            E, V = mp.eig(H)
            idx = [k for k in range(4) if mp.re(E[k]) < 0]
            U1 = mp.matrix([[V[i, k] for k in idx] for i in range(2)])
            U2 = mp.matrix([[V[i + 2, k] for k in idx] for i in range(2)])
            X = U2 * U1**-1
            P = mp.re(X[0, 0])
            if prev is not None and abs(P - prev) / abs(P) < mp.mpf("1e-12"):
                return +P, j, True
            prev = P
        return +P, j, False


def P_wiener(tau, lam, Sig, v):
    k2 = 2 * Sig * tau**2 + 2 * v * tau
    beta = mp.sqrt((2 * Sig + 2 * v * tau * lam**2) / k2)
    Aw = 2 * Sig * (1 + lam * tau) / (mp.sqrt(k2) * (beta + lam))
    return Sig / lam - Aw**2 / (2 * lam)


def opt_curve(lam, Sig, v):
    f = lambda t: P_rat(t, lam, Sig, v)
    d = lambda t: dP_f(t, lam, Sig, v)
    z = lambda t: ZREL * abs(f(t)) / t
    return Curve(f, d, z, -mp.log10(lam), [mp.log10(1 / lam)], None, "P_mv")


def relay_curve(lam, Sig, v, G):
    a = lam + G
    f = lambda t: (Sig + G**2 * v * t / (1 + a * t)) / a
    d = lambda t: G**2 * v / (a * (1 + a * t)**2)
    z = lambda t: ZREL * abs(f(t)) / t
    return Curve(f, d, z, -mp.log10(lam), [], None, "relay_mv")


def job(p):
    lam, Sig, v, G, lt = (mp.mpf(x) for x in (p["lam"], p["Sig"], p["v"], p["G"], p["lt"]))
    out = {"p": p}
    # three routes
    routes = []
    for lab, tau in (("random", lt / lam), ("lam tau = 1", 1 / lam), ("1 - 1e-12", (1 - mp.mpf("1e-12")) / lam),
                     ("1 + 1e-12", (1 + mp.mpf("1e-12")) / lam)):
        p1, (p2, jj, conv), p3 = P_rat(tau, lam, Sig, v), P_are(tau, lam, Sig, v), P_wiener(tau, lam, Sig, v)
        e = max(abs(p1 - p2) / p1, abs(p1 - p3) / p1, abs(p2 - p3) / p1)
        routes.append({"tau": lab, "err": e, "are_steps": jj, "are_converged": conv,
                       "pass": bool(conv and e <= mp.mpf("1e-8"))})
    out["routes"] = routes
    # shape
    Pmax = Sig * v / (Sig + lam * v)
    A = analyse(opt_curve(lam, Sig, v))
    tps = A["turns"]
    one = len(tps) == 1 and tps[0]["kind"] == "max"
    pos = abs(tps[0]["theta"] - 1 / lam) * lam if one else None
    peak = abs(P_rat(1 / lam, lam, Sig, v) - Pmax) / Pmax
    tr = lt / lam
    sym = abs(P_rat(tr, lam, Sig, v) - P_rat(1 / (lam**2 * tr), lam, Sig, v)) / P_rat(tr, lam, Sig, v)
    z12 = [P_rat(mp.power(10, s) / lam, lam, Sig, v) / Pmax for s in (-12, 12)]
    z24 = [P_rat(mp.power(10, s) / lam, lam, Sig, v) / Pmax for s in (-24, 24)]
    slopes = [(mp.log10(P_rat(mp.power(10, s * 12) / lam, lam, Sig, v)) - mp.log10(P_rat(mp.power(10, s * 10) / lam, lam, Sig, v))) / (2 * s)
              for s in (-1, 1)]
    out["shape"] = {"one_max": one, "pos_rel_err": pos, "peak_rel_err": peak, "sym_rel_err": sym,
                    "P_over_Pmax_at_1e-12_1e12": z12, "P_over_Pmax_at_1e-24_1e24": z24, "log_slopes_ends": slopes,
                    "pass_core": bool(one and pos <= mp.mpf("1e-10") and peak <= mp.mpf("1e-40") and sym <= mp.mpf("1e-12")),
                    "pass_zero_literal": bool(all(z < mp.mpf("1e-6") for z in z12)),
                    "pass_zero_supp": bool(all(z < mp.mpf("1e-6") for z in z24)
                                           and abs(slopes[0] - mp.mpf("0.5")) <= mp.mpf("1e-3")
                                           and abs(slopes[1] + mp.mpf("0.5")) <= mp.mpf("1e-3"))}
    # classes
    crows, cok = [], True
    for lab, R2, want in (("1e-3 Pmax", Pmax / 1000, (0, 0, 1)), ("0.5 Pmax", Pmax / 2, (0, 0, 1)),
                          ("0.9 Pmax", Pmax * mp.mpf("0.9"), (0, 0, 1)), ("Pmax(1-1e-6)", Pmax * (1 - mp.mpf("1e-6")), (0, 0, 1)),
                          ("Pmax", Pmax, (0, 0, 0)), ("Pmax(1+1e-6)", Pmax * (1 + mp.mpf("1e-6")), (0, 0, 0)),
                          ("1.5 Pmax", 1.5 * Pmax, (0, 0, 0))):
        r = classify(A, R2)
        ok = r["route_i"] == want and r["route_ii"] == want
        prod = None
        if ok and want == (0, 0, 1):
            a_, b_ = r["ends"][0]
            prod = abs(a_ * b_ * lam**2 - 1)
            ok = prod <= mp.mpf("1e-10")
        cok &= ok
        crows.append({"R2": lab, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]), "prod_err": prod, "pass": bool(ok)})
    out["classes"] = {"rows": crows, "pass": bool(cok)}
    # relay
    Ar = analyse(relay_curve(lam, Sig, v, G))
    a = lam + G
    pos_all = all(_sgn(Ar["curve"], x)[0] == 1 for x in grid(Ar["curve"]))
    lm_ok = abs(Ar["L_minus"] - Sig / a) <= mp.mpf("1e-30") * Sig / a
    Lp = (Sig + G**2 * v / a) / a
    lp_ok = abs(Ar["L_plus"] - Lp) <= mp.mpf("1e-30") * Lp
    ge = all(Ar["curve"].f(mp.power(10, s) / lam) >= P_rat(mp.power(10, s) / lam, lam, Sig, v)
             for s in np.linspace(-6, 6, 200))
    out["relay"] = {"n_tp": len(Ar["turns"]), "deriv_positive_on_grid": pos_all, "L_minus_ok": bool(lm_ok),
                    "L_plus_ok": bool(lp_ok), "relay_ge_P": bool(ge),
                    "pass": bool(len(Ar["turns"]) == 0 and pos_all and lm_ok and lp_ok and ge)}
    return out


def monte_carlo():
    lam, Sig, v, G = 1.0, 0.01, 0.05, 0.5
    a = lam + G
    rng = np.random.default_rng(10061)
    NT, rows = 2000, []
    for tau in (0.1, 1.0, 10.0):
        dt = min(tau / 100, 2e-3)
        nb, ns = int(round(10 * max(tau, 1) / dt)), int(round(20 * max(tau, 1) / dt))
        h = 1 / tau - lam
        Rv = 2 * Sig + 2 * v / tau
        P = float(P_rat(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(v)))
        K = (h * P + 2 * Sig) / Rv
        x = np.zeros(NT)
        eta = rng.standard_normal(NT) * np.sqrt(v)
        s = rng.standard_normal(NT) * np.sqrt(Sig / lam)
        sh = np.zeros(NT)
        ax, ae = np.zeros(NT), np.zeros(NT)
        q2, qe = np.sqrt(2 * Sig * dt), np.sqrt(2 * v * dt / tau)
        for n in range(nb + ns):
            z = rng.standard_normal((3, NT))
            x = x + (-a * x + G * eta) * dt + q2 * z[0]
            y0 = s + eta
            s1 = s - lam * s * dt + q2 * z[1]
            e1 = eta - eta * dt / tau + qe * z[2]
            zdt = (s1 + e1) - y0 + y0 * dt / tau
            sh = sh - lam * sh * dt + K * (zdt - h * sh * dt)
            s, eta = s1, e1
            if n >= nb:
                ax += x * x
                ae += (s - sh)**2
        for kind, acc, fml in (("relay", ax, (Sig + G**2 * v * tau / (1 + a * tau)) / a), ("optimal", ae, P)):
            per = acc / ns
            est, se = per.mean(), per.std(ddof=1) / np.sqrt(NT)
            rows.append({"tau": tau, "filter": kind, "estimate": est, "SE": se, "formula": fml, "z": (est - fml) / se,
                         "se_rel": se / fml, "pass": bool(se <= 0.02 * fml and abs(est - fml) <= 3 * se)})
    return rows


def main():
    t0 = time.time()
    rng = np.random.default_rng(10006)
    S = 10.0**rng.uniform(-2, 2, size=(1000, 4))
    lt = 10.0**rng.uniform(-4, 4, size=1000)
    jobs = [{"lam": S[i, 0], "Sig": S[i, 1], "v": S[i, 2], "G": S[i, 3], "lt": lt[i]} for i in range(1000)]
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=10)
    print(f"  sets done {time.time() - t0:.0f}s", flush=True)
    rt = [r for o in res for r in o["routes"]]
    R = {"routes": {"n": len(rt), "max_err": max(r["err"] for r in rt), "n_fail": sum(not r["pass"] for r in rt),
                    "n_not_converged": sum(not r["are_converged"] for r in rt), "max_steps": max(r["are_steps"] for r in rt),
                    "fails": [dict(r, p=o["p"]) for o in res for r in o["routes"] if not r["pass"]][:20]}}
    R["routes"]["pass"] = R["routes"]["n_fail"] == 0
    sh = [o["shape"] for o in res]
    R["shape"] = {"n_core_fail": sum(not s["pass_core"] for s in sh),
                  "max_pos_rel_err": max(s["pos_rel_err"] for s in sh if s["pos_rel_err"] is not None),
                  "max_sym_rel_err": max(s["sym_rel_err"] for s in sh), "max_peak_rel_err": max(s["peak_rel_err"] for s in sh),
                  "zero_literal_pass": sum(s["pass_zero_literal"] for s in sh),
                  "min_P_over_Pmax_at_1e12": min(min(s["P_over_Pmax_at_1e-12_1e12"]) for s in sh),
                  "zero_supp_pass": sum(s["pass_zero_supp"] for s in sh)}
    R["shape"]["pass"] = R["shape"]["n_core_fail"] == 0 and R["shape"]["zero_literal_pass"] == len(sh)
    R["shape"]["pass_supplementary"] = R["shape"]["n_core_fail"] == 0 and R["shape"]["zero_supp_pass"] == len(sh)
    R["classes"] = {"n_sets": len(res), "n_fail": sum(not o["classes"]["pass"] for o in res),
                    "fails": [o for o in res if not o["classes"]["pass"]][:10]}
    R["classes"]["pass"] = R["classes"]["n_fail"] == 0
    R["relay"] = {"n_fail": sum(not o["relay"]["pass"] for o in res), "fails": [o["relay"] for o in res if not o["relay"]["pass"]][:10]}
    R["relay"]["pass"] = R["relay"]["n_fail"] == 0
    R["mc"] = {"rows": monte_carlo()}
    R["mc"]["pass"] = all(r["pass"] for r in R["mc"]["rows"])
    l, S_, v = mp.mpf(1), mp.mpf("0.01"), mp.mpf("0.05")
    reg = [("P(1)", P_rat(mp.mpf(1), l, S_, v), "0.0083333"), ("P(0.3)", P_rat(mp.mpf("0.3"), l, S_, v), "0.0079078"),
           ("P(0.01)", P_rat(mp.mpf("0.01"), l, S_, v), "0.0034559"), ("P(100)", P_rat(mp.mpf(100), l, S_, v), "0.0034559")]
    R["regression"] = {"rows": [{"q": a, "computed": b, "stated": c, "pass": sf_match(b, c)} for a, b, c in reg]}
    R["regression"]["pass"] = all(r["pass"] for r in R["regression"]["rows"])
    parts = ("routes", "shape", "classes", "relay", "mc", "regression")
    R["pass"] = all(R[k]["pass"] for k in parts)
    R["seconds"] = time.time() - t0
    print(f"routes: {R['routes']['n']} evaluations, max pairwise rel err {mp.nstr(R['routes']['max_err'], 3)}, failures "
          f"{R['routes']['n_fail']}, ARE not converged {R['routes']['n_not_converged']}")
    print(f"shape: core failures {R['shape']['n_core_fail']}; literal zero-limit passes in {R['shape']['zero_literal_pass']}/1000 "
          f"(min P/Pmax at 1e+-12: {mp.nstr(R['shape']['min_P_over_Pmax_at_1e12'], 3)}); supplementary {R['shape']['zero_supp_pass']}/1000")
    print(f"classes failures {R['classes']['n_fail']}; relay failures {R['relay']['n_fail']}")
    for r in R["mc"]["rows"]:
        print(f"MC tau={r['tau']} {r['filter']}: {r['estimate']:.6g} +/- {r['SE']:.2g} vs {r['formula']:.6g}, z={r['z']:+.2f}")
    print("regression:", [(r["q"], mp.nstr(r["computed"], 8), r["pass"]) for r in R["regression"]["rows"]])
    print(f"T10.6: {'PASS' if R['pass'] else 'FAIL'} " + str({k: R[k]["pass"] for k in parts}))
    save_json(R, "t10_6.json")


if __name__ == "__main__":
    main()
