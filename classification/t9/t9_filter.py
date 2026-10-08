"""T9.2: optimal filter computed without measurement differencing (ARE + eps -> 0) and by Wiener factorization."""
import time

import mpmath as mp
import numpy as np
from scipy.linalg import solve_continuous_are

from t9_common import P_opt, save_json

EPS = np.array([1e-4, 1e-6, 1e-8, 1e-10])
t0 = time.time()


def p_eps(lam, Sig, Pi, tau, eps):
    A = np.diag([-lam, -1.0 / tau])
    Q = np.diag([2 * Sig, 1.0 / (Pi * tau**2)])
    C = np.array([[1.0, 1.0]])
    X = solve_continuous_are(A.T, C.T, Q, np.array([[eps]]))
    return X[0, 0]


def extrap(eps_list, vals):
    """Cubic in sqrt(eps) through the four points, evaluated at 0."""
    r = np.sqrt(eps_list)
    V = np.vander(r, 4)
    return np.linalg.solve(V, vals)[-1]


def compare(lam, Sig, Pi, tau, eps_list=EPS):
    try:
        vals = np.array([p_eps(lam, Sig, Pi, tau, e) for e in eps_list])
        ex = extrap(eps_list, vals)
    except Exception as exc:                       # record solver failures as failures
        return {"err": float("inf"), "exc": repr(exc)}
    ref = P_opt(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))
    return {"err": float(abs(mp.mpf(ex) - ref) / ref), "ex": ex, "ref": float(ref), "P_eps_1e-10": vals[-1]}


# ---------------- Wiener route (worked example)
def wiener(lam, Sig, Pi, tau):
    lam, Sig, Pi, tau = (mp.mpf(x) for x in (lam, Sig, Pi, tau))
    # S_y in s = i omega: S_y = N(s)/((lam^2 - s^2)(1 - tau^2 s^2)); N(s) = 2 Sig (1 - tau^2 s^2) + (lam^2 - s^2)/Pi
    num = [-(2 * Sig * tau**2 + 1 / Pi), 0, 2 * Sig + lam**2 / Pi]          # coefficients in s
    rts = [mp.polyroots(num, maxsteps=200, extraprec=200)[k] for k in range(2)]
    lhp = [r for r in rts if mp.re(r) < 0][0]                             # numerator root -beta
    k2 = 2 * Sig * tau**2 + 1 / Pi
    # S_y+(s) = sqrt(k2)(s - lhp)/((s + lam)(1 + tau s));  S_y-(s) = S_y+(-s)
    Syp = lambda z: mp.sqrt(k2) * (z - lhp) / ((z + lam) * (1 + tau * z))
    Sym = lambda z: Syp(-z)
    Ss = lambda z: 2 * Sig / ((lam + z) * (lam - z))
    f = lambda z: Ss(z) / Sym(z)
    # causal part: residues of f at its LHP poles (here only s = -lam)
    poles = [-lam]
    res = [mp.limit(lambda z: (z - p) * f(z), p) for p in poles]
    causal = lambda z: sum(r / (z - p) for r, p in zip(res, poles))
    integ = mp.quad(lambda om: abs(causal(1j * om))**2, [-mp.inf, 0, mp.inf]) / (2 * mp.pi)
    return Sig / lam - integ



def main():
    rng = np.random.default_rng(9002)
    S = 10.0**rng.uniform(-3, 3, size=(1000, 4))
    lt = 10.0**rng.uniform(-3, 3, size=1000)
    rows, diag = [], []
    for i in range(1000):
        lam, Sig, Pi, _ = S[i]
        for kind, tau in (("random tau", lt[i] / lam), ("lam tau = 1", 1.0 / lam)):
            r = compare(lam, Sig, Pi, tau)
            rows.append({"set": i, "kind": kind, "lam": lam, "Sig": Sig, "Pi": Pi, "tau": tau, **r})
            e0 = (2 * Sig + 1 / (Pi * tau**2)) / (lam + 1 / tau)**2
            d = compare(lam, Sig, Pi, tau, EPS * e0)
            diag.append({"set": i, "kind": kind, "err": d["err"]})
    we = compare(1.0, 0.01, 1.0, 1.0)
    rows.append({"set": "worked", "kind": "lam tau = 1", "lam": 1.0, "Sig": 0.01, "Pi": 1.0, "tau": 1.0, **we})

    errs = np.array([r["err"] for r in rows])
    fails = [r for r in rows if not r["err"] <= 1e-5]
    ok_are = len(fails) == 0
    derrs = np.array([d["err"] for d in diag])
    print(f"ARE route: {len(rows)} cases, max rel err {errs.max():.3g}, median {np.median(errs):.3g}, "
          f"failures (> 1e-5): {len(fails)}; worked example err {we['err']:.3g}")
    print(f"  diagnostic (scaled eps): max rel err {derrs.max():.3g}, failures {int((derrs > 1e-5).sum())}")
    for f in sorted(fails, key=lambda r: -r["err"])[:10]:
        print(f"  fail: {f['kind']} lam={f['lam']:.3g} Sig={f['Sig']:.3g} Pi={f['Pi']:.3g} tau={f['tau']:.3g} "
              f"err={f['err']:.3g} {f.get('exc', '')}")


    wrows = []
    for tau in (0.1, 1.0, 10.0):
        pw = wiener(1.0, 0.01, 1.0, tau)
        ref = P_opt(mp.mpf(tau), mp.mpf(1), mp.mpf("0.01"), mp.mpf(1))
        e = float(abs(pw - ref) / ref)
        wrows.append({"tau": tau, "wiener": float(pw), "prop31": float(ref), "rel_err": e, "pass": e <= 1e-6})
        print(f"Wiener tau={tau}: {float(pw):.12g} vs Prop 3.1 {float(ref):.12g}, rel err {e:.3g}")
    ok_w = all(r["pass"] for r in wrows)
    ok = ok_are and ok_w
    print(f"T9.2: {'PASS' if ok else 'FAIL'} (ARE {'PASS' if ok_are else 'FAIL'}, Wiener {'PASS' if ok_w else 'FAIL'})")
    save_json({"are": {"n": len(rows), "max_err": errs.max(), "median_err": float(np.median(errs)), "n_fail": len(fails),
                       "fails": fails[:50], "worked": we, "pass": ok_are},
               "are_scaled_diagnostic": {"max_err": derrs.max(), "n_fail": int((derrs > 1e-5).sum())},
               "wiener": wrows, "wiener_pass": ok_w, "pass": ok, "seconds": time.time() - t0}, "t9_2.json")


if __name__ == "__main__":
    main()
