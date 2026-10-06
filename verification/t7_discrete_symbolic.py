"""T7.1: discrete-time fixed-gain filter identities (PREREG_t7.md)."""
from fractions import Fraction

import numpy as np
import sympy as sp

from common import Timer, dump
from t7_common import identity

R = {}
lines = []


def out(s=""):
    print(s)
    lines.append(s)


def record(key, desc, res, extra=None):
    res = dict(res)
    res["desc"] = desc
    if extra:
        res.update(extra)
    R[key] = res
    out(f"[{res['verdict'] if 'verdict' in res else ('PASS' if res['pass'] else 'FAIL')}] {key}: {desc}"
        + (f" | numeric max rel {res['numeric_max_rel']:.1e}" if "numeric_max_rel" in res else "")
        + (f" | residual: {res['residual']}" if res.get("residual") else ""))


with Timer() as T:
    phi, q, r, L, M_, e, v, w = sp.symbols("phi q r L M e v w", positive=True)
    s = 1 - phi**2
    F = q / (1 - phi**2)
    Pid = 1 / r

    # (a) derive stationary prior variance from the recursion
    e_next = phi * ((1 - L) * e + L * v) - w
    sq = sp.expand(e_next**2)
    moments = {e**2: M_, v**2: r, w**2: q}
    poly = sp.Poly(sq, e, v, w)
    Ee2 = 0
    for monom, coef in poly.terms():
        term = sp.Integer(1)
        for var, k in zip((e, v, w), monom):
            if k == 1:          # zero-mean, independent -> any odd power kills the term
                term = 0
                break
            if k == 2:
                term *= moments[var**2]
        Ee2 += coef * term
    Msol = sp.solve(sp.Eq(M_, Ee2), M_)[0]
    M_stated = (phi**2 * L**2 * r + q) / (1 - phi**2 * (1 - L) ** 2)
    out(f"(a) E[(e-_(k+1))^2] = {sp.factor(Ee2)};  fixed point M = {sp.factor(Msol)}")
    record("T7.1a", "stationary prior variance derived from recursion == (phi^2 L^2 r + q)/(1 - phi^2(1-L)^2)",
           identity(Msol, M_stated))
    M = Msol

    # (b) posterior
    post = sp.expand(((1 - L) * e + L * v) ** 2)
    pp = sp.Poly(post, e, v)
    S = sum(coef * (0 if 1 in mon else (M if mon[0] == 2 else 1) * (r if mon[1] == 2 else 1))
            for mon, coef in pp.terms())
    record("T7.1b", "posterior variance S == (1-L)^2 M + L^2 r", identity(S, (1 - L) ** 2 * M + L**2 * r))

    # (c)
    record("T7.1c", "S - F == (M - F)/phi^2", identity(S - F, (M - F) / phi**2))

    # (d)
    fac = sp.factor(M - F)
    target_d = phi**2 * L * (L * (r * (1 - phi**2) + q) - 2 * q) / (
        (1 - phi**2) * (1 + phi * (1 - L)) * (1 - phi * (1 - L)))
    out(f"(d) sympy.factor(M - F) = {fac}")
    out(f"    LaTeX: {sp.latex(fac)}")
    record("T7.1d", "M - F == phi^2 L [L(r(1-phi^2)+q) - 2q] / [(1-phi^2)(1+phi(1-L))(1-phi(1-L))]",
           identity(M - F, target_d), {"factor": str(fac), "factor_latex": sp.latex(fac)})

    # (e) algebraic equivalence
    alg = identity(L * (r * s + q) - 2 * q, (2 - L) * r * s * (L / (2 - L) - F * Pid))
    u, wv = sp.symbols("u w_", positive=True)
    sub = {phi: 1 / (1 + u), L: 1 / (1 + wv)}
    factors = {"phi^2 L": phi**2 * L, "(2-L) r s": (2 - L) * r * s, "1-phi^2": 1 - phi**2,
               "1+phi(1-L)": 1 + phi * (1 - L), "1-phi(1-L)": 1 - phi * (1 - L)}
    pos = {}
    for name, f_ in factors.items():
        g_ = sp.factor(sp.together(f_.subs(sub)))
        nmr, dnm = sp.fraction(g_)
        pos[name] = bool(sp.ask(sp.Q.positive(sp.expand(nmr))) and sp.ask(sp.Q.positive(sp.expand(dnm))))
        # L = 1 endpoint
        g1 = sp.factor(sp.together(f_.subs(L, 1).subs(phi, 1 / (1 + u))))
        n1, d1 = sp.fraction(g1)
        pos[name] &= bool(sp.ask(sp.Q.positive(sp.expand(n1))) and sp.ask(sp.Q.positive(sp.expand(d1))))
    # numeric: exact rational arithmetic at 10,000 random sets
    rng = np.random.default_rng(7001)
    mism = 0
    n_exc = 0
    for _ in range(10000):
        ph = Fraction(rng.uniform(0.01, 0.99))
        qq = Fraction(10 ** rng.uniform(-3, 3))
        rr = Fraction(10 ** rng.uniform(-3, 3))
        LL = Fraction(rng.uniform(0.001, 0.999))
        Mv = (ph * ph * LL * LL * rr + qq) / (1 - ph * ph * (1 - LL) ** 2)
        Fv = qq / (1 - ph * ph)
        lhs = Mv > Fv
        rhs = LL / (2 - LL) > Fv / rr
        n_exc += lhs
        mism += lhs != rhs
    ok_e = alg["pass"] and all(pos.values()) and mism == 0
    R["T7.1e"] = {"desc": "M > F  <=>  L/(2-L) > F Pi_d (algebraic + 10,000 exact random sets)", "pass": ok_e,
                  "verdict": "PASS" if ok_e else "FAIL", "algebraic": alg, "positive_factors": pos,
                  "n_sets": 10000, "mismatches": mism, "n_excess_true": int(n_exc)}
    out(f"[{'PASS' if ok_e else 'FAIL'}] T7.1e: algebraic identity {alg['verdict']}; prefactors positive {pos}; "
        f"10,000 exact sets: {mism} mismatches ({n_exc} with M > F)")

    # (f) optimal gain
    Mx, rx, sx = sp.symbols("M r s", positive=True)
    lhs_f = (Mx + rx * sx) * (Mx + 2 * rx) - 2 * rx * sx * (Mx + rx)
    f1 = identity(lhs_f, Mx**2 + rx * Mx * (2 - sx))
    diff_latex = sp.latex(sp.expand(lhs_f))
    # eliminate q via Riccati, s = 1 - phi^2
    q_ric = sp.solve(sp.Eq(M_, phi**2 * M_ * r / (M_ + r) + q), q)[0]
    Lstar = M_ / (M_ + r)
    gap = sp.Rational(1, 2) * (q_ric / (1 - phi**2)) * (1 / r) - Lstar / (2 - Lstar)
    gap_target = M_**2 * (M_ + r * (2 - s)) / (2 * r * s * (M_ + r) * (M_ + 2 * r))
    f2 = identity(gap, gap_target)
    gt = sp.factor(sp.together(gap_target.subs(phi, 1 / (1 + u))))
    gn, gd = sp.fraction(gt)
    gap_pos = bool(sp.ask(sp.Q.positive(sp.expand(gn))) and sp.ask(sp.Q.positive(sp.expand(gd))))
    # informational: L* in (a) recovers the Riccati M
    ric_consistent = sp.simplify(M_stated.subs(L, Lstar).subs(q, q_ric) - M_) == 0
    # numeric 20,000 sets
    rng = np.random.default_rng(7002)
    ph = rng.uniform(0.01, 0.99, 20000)
    qq = 10 ** rng.uniform(-3, 3, 20000)
    rr = 10 ** rng.uniform(-3, 3, 20000)
    ss = 1 - ph**2
    b = rr * ss - qq
    disc = np.sqrt(b * b + 4 * qq * rr)
    Mv = np.where(b > 0, 2 * qq * rr / (b + disc), (-b + disc) / 2)
    Ls = Mv / (Mv + rr)
    ratio = (Ls / (2 - Ls)) / (0.5 * (qq / ss) / rr)
    ric_res = np.max(np.abs(Mv - (ph**2 * Mv * rr / (Mv + rr) + qq)) / Mv)
    imax = int(np.argmax(ratio))
    ok_f = f1["pass"] and f2["pass"] and gap_pos and bool(np.all(ratio < 1))
    R["T7.1f"] = {"desc": "(M+rs)(M+2r) - 2rs(M+r) = M^2 + rM(2-s); hence L*/(2-L*) < F Pi_d / 2", "pass": ok_f,
                  "verdict": "PASS" if ok_f else "FAIL", "difference_identity": f1, "gap_identity": f2,
                  "gap_positive": gap_pos, "difference_latex": diff_latex,
                  "difference_rhs_latex": sp.latex(Mx**2 + rx * Mx * (2 - sx)),
                  "riccati_consistent_with_a": bool(ric_consistent), "n_sets": 20000,
                  "max_ratio": float(ratio.max()), "max_ratio_at": {"phi": ph[imax], "q": qq[imax], "r": rr[imax]},
                  "n_ratio_ge_1": int(np.sum(ratio >= 1)), "max_riccati_residual": float(ric_res)}
    out(f"[{'PASS' if ok_f else 'FAIL'}] T7.1f: difference identity {f1['verdict']}; gap identity {f2['verdict']}; "
        f"gap > 0 proven {gap_pos}; L* in (a) recovers Riccati M: {ric_consistent}; 20,000 sets: max ratio "
        f"{ratio.max():.12f} (at q/r = {qq[imax]/rr[imax]:.3g}), # >= 1: {int(np.sum(ratio >= 1))}")
    out(f"    expanded (M+rs)(M+2r) - 2rs(M+r) = {sp.latex(sp.expand(lhs_f))}")

    # (g) continuum limit
    lam, Sig, dt, Pi, G = sp.symbols("lambda Sigma Delta_t Pi G", positive=True)
    phg = sp.exp(-lam * dt)
    qg = Sig * (1 - phg**2) / lam
    Fg = qg / (1 - phg**2)
    Dg = (G * dt) / (2 - G * dt) - Fg * Pi * dt
    ser = sp.series(Dg, dt, 0, 3).removeO()
    c0 = sp.simplify(ser.coeff(dt, 0))
    c1 = sp.simplify(ser.coeff(dt, 1))
    g1 = identity(c1, G / 2 - Sig / lam * Pi)
    ok_g = g1["pass"] and c0 == 0
    R["T7.1g"] = {"desc": "continuum limit: D = dt (G/2 - F Pi) + O(dt^2)  => G > 2 F Pi", "pass": ok_g,
                  "verdict": "PASS" if ok_g else "FAIL", "coef0": str(c0), "coef1": str(c1),
                  "coef2": str(sp.simplify(ser.coeff(dt, 2))), "coef1_identity": g1, "F_exact": str(sp.simplify(Fg))}
    out(f"[{'PASS' if ok_g else 'FAIL'}] T7.1g: series D = {c0} + ({c1})*dt + ({sp.simplify(ser.coeff(dt, 2))})*dt^2 + ...; "
        f"F = {sp.simplify(Fg)}")

all_ok = all(v["pass"] for v in R.values())
out(f"T7.1 overall: {'PASS' if all_ok else 'FAIL'}  ({T.dt:.1f}s)")
dump("t7_1.json", {"criteria": R, "pass": all_ok, "runtime_s": T.dt, "lines": lines})
