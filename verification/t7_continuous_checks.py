"""T7.2: continuous-time closed-form checks (PREREG_t7.md). Notation: Pi_0 = prior precision, kappa = (c/Pi_0)/F."""
import numpy as np
import sympy as sp
from scipy.optimize import brentq

from common import C, F, LAM, SIG, Timer, dump
from t7_common import identity, peak, pi0_of, sf_match

R, lines = {}, []


def out(s=""):
    print(s)
    lines.append(s)


with Timer() as T:
    # (a) Kalman-Bucy Riccati
    lam, S, Pi, p = sp.symbols("lambda Sigma Pi p", positive=True)
    roots = sp.solve(sp.Eq(2 * S - 2 * lam * p - Pi * p**2, 0), p)
    pos = [r_ for r_ in roots if sp.ask(sp.Q.positive(r_)) is not False and not sp.simplify(r_).could_extract_minus_sign()]
    proot = pos[0]
    Gstar = -lam + sp.sqrt(lam**2 + 2 * S * Pi)
    i1 = identity(proot * Pi, Gstar)
    i2 = identity(proot, 2 * S / (lam + sp.sqrt(lam**2 + 2 * S * Pi)))
    i3 = identity(proot, (S + Gstar**2 / (2 * Pi)) / (lam + Gstar))
    ok_a = i1["pass"] and i2["pass"] and i3["pass"] and len(pos) == 1
    R["T7.2a"] = {"desc": "Kalman-Bucy: p Pi = G* = -lam + sqrt(lam^2 + 2 Sigma Pi) and p = sigma*^2 (Eq. 4)",
                  "pass": ok_a, "verdict": "PASS" if ok_a else "FAIL", "positive_root": str(proot),
                  "pPi_eq_Gstar": i1, "p_eq_sigma_star": i2, "p_eq_closed_form_at_Gstar": i3}
    out(f"[{R['T7.2a']['verdict']}] T7.2a: positive root p = {proot}; pPi==G*: {i1['verdict']}; "
        f"p==2Sigma/(lam+sqrt(..)): {i2['verdict']}; p==(2) at G*: {i3['verdict']}")

    # (b) peak heights vs kappa
    expected = {2: 1.000, 3: 1.036, 5: 1.175, 10: 1.584, 20: 2.432, 50: 5.000, 100: 9.288}
    rows = []
    for k, ev in expected.items():
        pst, M = peak(pi0_of(k))
        rows.append({"kappa": k, "Pi_0": pi0_of(k), "Pi_star": pst, "M": M, "M_over_F": M / F, "expected": ev,
                     "match": sf_match(M / F, ev, 4)})
    ok_b = all(r_["match"] for r_ in rows)
    R["T7.2b"] = {"desc": "peak M/F at kappa in {2,3,5,10,20,50,100} matches 1.000,1.036,1.175,1.584,2.432,5.000,9.288 (4 s.f.)",
                  "pass": ok_b, "verdict": "PASS" if ok_b else "FAIL", "rows": rows}
    out(f"[{R['T7.2b']['verdict']}] T7.2b: " + "; ".join(
        f"kappa={r_['kappa']}: M/F={r_['M_over_F']:.6f} (exp {r_['expected']:.3f}, {'ok' if r_['match'] else 'MISMATCH'})"
        for r_ in rows))

    # (c) exact rationals at kappa = 50
    P0 = sp.Rational(C) / (50 * sp.Rational(1, 100))
    l_, c_, s_ = sp.Integer(1), sp.Integer(1), sp.Rational(1, 100)
    A = 2 * P0 * s_ + c_**2 + c_ * l_
    B = 4 * P0**2 * s_
    Cq = P0**2 * (2 * P0 * s_ - c_ * l_)
    X = sp.Symbol("X")
    rts = [r_ for r_ in sp.solve(A * X**2 + B * X + Cq, X) if r_.is_positive]
    pst = rts[0]
    g = c_ * pst / (pst + P0)
    Mx = sp.cancel((s_ + g**2 / (2 * pst)) / (l_ + g))     # exact Rational arithmetic throughout
    ok_c = P0 == 2 and pst == sp.Rational(4, 3) and Mx == sp.Rational(1, 20)
    R["T7.2c"] = {"desc": "kappa = 50 (Pi_0 = 2): Pi* = 4/3 and M = 0.05 exactly (rational arithmetic)", "pass": ok_c,
                  "verdict": "PASS" if ok_c else "FAIL", "Pi_0": str(P0), "Pi_star": str(pst), "M": str(Mx)}
    out(f"[{R['T7.2c']['verdict']}] T7.2c: Pi_0 = {P0}, Pi* = {pst}, M = {Mx}")

    # (d) smallest kappa with M >= 0.05
    fM = lambda k: peak(pi0_of(k))[1] - 0.05
    kroot = brentq(fM, 2.5, 1000, xtol=1e-14)
    kg = np.logspace(np.log10(2.5), 3, 10001)
    Mg = np.array([peak(pi0_of(k))[1] for k in kg])
    mono = bool(np.all(np.diff(Mg) > 0))
    ok_d = abs(kroot - 50) <= 1e-8 and mono
    R["T7.2d"] = {"desc": "smallest kappa with M >= 0.05 is 50 (brentq, |err| <= 1e-8; M increasing in kappa)",
                  "pass": ok_d, "verdict": "PASS" if ok_d else "FAIL", "kappa_root": kroot,
                  "abs_err": abs(kroot - 50), "monotone": mono}
    out(f"[{R['T7.2d']['verdict']}] T7.2d: kappa_root = {kroot:.15f} (|err| = {abs(kroot-50):.2e}); M increasing: {mono}")

    # (e) Hill gain
    grid = np.logspace(-6, 6, 600001)
    hill = {}
    for P0h in (24.0, 25.0, 26.0):
        G = C * grid**2 / (grid**2 + P0h**2)
        direct = (SIG + G**2 / (2 * grid)) / (LAM + G) - F
        clean = G * (LAM * G / (2 * grid) - SIG) / (LAM * (LAM + G))
        i, j = int(np.argmax(direct)), int(np.argmax(clean))
        hill[P0h] = {"max_direct": float(direct[i]), "at_Pi_direct": float(grid[i]),
                     "max_clean": float(clean[j]), "at_Pi_clean": float(grid[j])}
    ok_e = hill[24.0]["max_direct"] > 0 and sf_match(hill[24.0]["max_direct"], 1.40e-4, 3) and \
        hill[26.0]["max_direct"] <= 1e-15
    R["T7.2e"] = {"desc": "Hill gain: Pi_0=24 max(sigma^2-F) ~ 1.40e-4 (>0, 3 s.f.); Pi_0=26 max <= 1e-15; Pi_0=25 reported",
                  "pass": ok_e, "verdict": "PASS" if ok_e else "FAIL", "hill": {str(k): v for k, v in hill.items()}}
    out(f"[{R['T7.2e']['verdict']}] T7.2e: " + "; ".join(
        f"Pi_0={k:g}: max direct {v['max_direct']:.6e} at Pi={v['at_Pi_direct']:.5g}, cancellation-free "
        f"{v['max_clean']:.6e} at Pi={v['at_Pi_clean']:.5g}" for k, v in hill.items()))

all_ok = all(v["pass"] for v in R.values())
out(f"T7.2 overall: {'PASS' if all_ok else 'FAIL'}  ({T.dt:.1f}s)")
dump("t7_2.json", {"criteria": R, "pass": all_ok, "runtime_s": T.dt, "lines": lines})
