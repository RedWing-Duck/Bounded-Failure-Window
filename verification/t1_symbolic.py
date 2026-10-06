"""Task 1: symbolic checks of closed forms (2)-(4), Prop 4 and the worked example."""
import math

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from common import RES, Timer, dump, g_kalman, g_opt, var_cf

lines, crit = [], {}


def out(s=""):
    print(s)
    lines.append(s)


def check(key, desc, ok, detail=""):
    crit[key] = {"desc": desc, "pass": bool(ok), "detail": str(detail)}
    out(f"[{'PASS' if ok else 'FAIL'}] {key}: {desc} {detail}")


with Timer() as T:
    lam, c, S, P, Pi, G, a, t = sp.symbols("lambda c Sigma P Pi G a t", positive=True)
    g0, g1 = sp.symbols("g0 g1", real=True)
    m2 = sp.Function("m2")

    # ---- T1.1 OU stationary variance from the Ito second-moment equation
    # d(x^2) = 2x dx + (dx)^2 ->  dm2/dt = -2(lam+G) m2 + G^2/Pi + 2 Sigma
    D = G**2 / Pi + 2 * S
    ode = sp.Eq(m2(t).diff(t), -2 * (lam + G) * m2(t) + D)
    stat = sp.solve(sp.Eq(ode.rhs.subs(m2(t), sp.Symbol("m")), 0), sp.Symbol("m"))[0]
    sig2_G = (S + G**2 / (2 * Pi)) / (lam + G)
    check("T1.1", "OU stationary variance - (2) == 0", sp.simplify(stat - sig2_G) == 0, f"stat={stat}")
    # long-time limit of the ODE solution also equals it
    sol = sp.dsolve(ode, m2(t), ics={m2(0): 0}).rhs
    check("T1.1b", "lim_{t->inf} of ODE solution with m2(0)=0 equals (2)",
          sp.simplify(sp.limit(sol, t, sp.oo) - sig2_G) == 0)

    # ---- Kalman gain
    Gk = c * Pi / (Pi + P)
    sig2 = sig2_G.subs(G, Gk)
    Fl, Hl = sp.limit(sig2, Pi, 0), sp.limit(sig2, Pi, sp.oo)
    check("T1.2", "F = Sigma/lambda and H = Sigma/(lambda+c)",
          sp.simplify(Fl - S / lam) == 0 and sp.simplify(Hl - S / (lam + c)) == 0, f"F={Fl}, H={Hl}")

    # ---- T1.3 derivative numerator -> quadratic
    d = sp.together(sp.diff(sig2, Pi))
    num, den = sp.fraction(d)
    num = sp.expand(num)
    A = 2 * P * S + c**2 + c * lam
    B = 4 * P**2 * S
    Cq = P**2 * (2 * P * S - c * lam)
    quad = A * Pi**2 + B * Pi + Cq
    k = sp.factor(sp.cancel(-num / quad))
    resid = sp.simplify(num + k * quad)
    k_pos = all(sp.ask(sp.Q.positive(f)) for f in sp.Mul.make_args(sp.factor(k)) if not f.is_number) and \
        all(f > 0 for f in sp.Mul.make_args(sp.factor(k)) if f.is_number)
    den_f = sp.factor(den)
    check("T1.3", "numerator = -k(Pi)*(A Pi^2+B Pi+C), A,B,C as stated, k>0",
          resid == 0 and k_pos and sp.cancel(-num / quad).is_polynomial(Pi) is not None,
          f"k={k}, denominator={den_f}")
    out("Expanded numerator of d sigma^2/dPi (over the denominator %s):" % sp.latex(den_f))
    out("LaTeX: " + sp.latex(num))
    out("Factored: " + sp.latex(sp.factor(num)))

    # ---- T1.4 slope at 0
    slope0 = sp.simplify(sp.limit(sp.diff(sig2, Pi), Pi, 0))
    target = c * (c * lam - 2 * P * S) / (2 * P**2 * lam**2)
    check("T1.4", "slope at Pi->0 equals c(c lam - 2PSigma)/(2P^2 lam^2)", sp.simplify(slope0 - target) == 0,
          f"slope0={sp.factor(slope0)}")
    # positive iff P < c lam/(2 Sigma): all factors except (c lam - 2 P Sigma) are positive symbols
    sgn_factor = sp.factor(slope0 / (c * lam - 2 * P * S))
    ok_sign = sp.ask(sp.Q.positive(sgn_factor)) is True
    sol_root = sp.solve(sp.Eq(c * lam - 2 * P * S, 0), P)
    check("T1.4b", "slope>0 iff P < c lam/(2 Sigma)", ok_sign and sp.simplify(sol_root[0] - c * lam / (2 * S)) == 0,
          f"slope/(c lam-2P Sigma)={sgn_factor}")

    # ---- T1.5 interior max iff C<0
    # A>0, B>0 (positive symbols). Product of roots C/A; sum -B/A<0.
    # => exactly one positive root iff C<0; derivative sign = -sign(quad): + below root, - above -> max.
    okA = sp.ask(sp.Q.positive(A)) is True and sp.ask(sp.Q.positive(B)) is True
    # C = P^2 (2 P Sigma - c lam): its only sign-changing factor vanishes at P = c lam/(2 Sigma)
    Cneg_iff = sp.simplify(sp.solve(sp.Eq(Cq, 0), P)[0] - c * lam / (2 * S)) == 0 and \
        sp.simplify(Cq / (2 * P * S - c * lam) - P**2) == 0
    # Descartes: coefficient signs (+,+,sign C) -> one positive root iff C<0. Positive root:
    root = (-B + sp.sqrt(B**2 - 4 * A * Cq)) / (2 * A)
    ok_root = sp.simplify(quad.subs(Pi, root)) == 0
    # numerical: derivative + below the root, - above (P=1); always - for P=100
    dnum = sp.lambdify((Pi, P), (-k * quad).subs({lam: 1, c: 1, S: sp.Rational(1, 100)}))
    r1 = float(root.subs({lam: 1, c: 1, S: sp.Rational(1, 100), P: 1}))
    pg = np.logspace(-6, 6, 2001)
    ok_num = np.all(dnum(pg[pg < r1], 1.0) > 0) and np.all(dnum(pg[pg > r1], 1.0) < 0) and \
        np.all(dnum(pg, 100.0) < 0)
    check("T1.5", "A,B>0; one positive root iff C<0 iff P<c lam/(2 Sigma); derivative +->- (max)",
          okA and Cneg_iff and ok_root and ok_num, f"positive root={root}")

    # ---- T1.6 optimum over free G
    dG = sp.diff(sig2_G, G)
    roots = sp.solve(sp.numer(sp.together(dG)), G)
    Gstar = -lam + sp.sqrt(lam**2 + 2 * S * Pi)
    ok_root = any(sp.simplify(r - Gstar) == 0 for r in roots)
    d2 = sp.simplify(sp.diff(sig2_G, G, 2).subs(G, Gstar))
    s_star = sp.simplify(sig2_G.subs(G, Gstar))
    ok_val = sp.simplify(s_star - Gstar / Pi) == 0 and \
        sp.simplify(s_star - 2 * S / (lam + sp.sqrt(lam**2 + 2 * S * Pi))) == 0
    dstar = sp.simplify(sp.diff(2 * S / (lam + sp.sqrt(lam**2 + 2 * S * Pi)), Pi))
    ok_dec = sp.ask(sp.Q.negative(dstar)) is True
    check("T1.6", "G* = -lam+sqrt(lam^2+2 Sigma Pi) is stationary min; sigma*^2 = G*/Pi = 2Sigma/(lam+sqrt(..)); d/dPi<0",
          ok_root and sp.ask(sp.Q.positive(d2)) is not False and ok_val and ok_dec,
          f"roots={roots}; d2sig/dG2 at G*={d2}; dsig*/dPi={dstar}")
    # numeric confirmation that d2 > 0 on a grid (in case sympy cannot decide)
    f_d2 = sp.lambdify((lam, S, Pi), d2)
    grid = np.logspace(-4, 4, 50)
    d2_ok = all(f_d2(l_, s_, p_) > 0 for l_ in (0.1, 1, 10) for s_ in (1e-3, 0.01, 1) for p_ in grid)
    check("T1.6b", "second derivative at G* positive on numeric grid", d2_ok)

    # ---- T1.7 general small-Pi slope
    Gser = g0 * Pi + g1 * Pi**2
    sl = sp.limit(sp.diff(sig2_G.subs(G, Gser), Pi), Pi, 0)
    check("T1.7", "slope at 0 for G=g0 Pi+O(Pi^2) equals g0^2/(2 lam) - Sigma g0/lam^2",
          sp.simplify(sl - (g0**2 / (2 * lam) - S * g0 / lam**2)) == 0, f"slope={sl}")

    # ---- T1.8 excess identity
    ex = sp.simplify(sig2_G - S / lam - G * (lam * G / (2 * Pi) - S) / (lam * (lam + G)))
    check("T1.8", "sigma^2 - F = G(lam G/(2Pi) - Sigma)/(lam(lam+G))  => excess iff G/Pi > 2Sigma/lam", ex == 0)

    # ---- T1.9 worked example
    vals = {lam: 1, c: 1, S: sp.Rational(1, 100)}
    qn = sp.Poly(quad.subs(vals).subs(P, 1), Pi)
    pstar = [r for r in qn.nroots(n=30) if r.is_real and r > 0]
    pstar = float(pstar[0])
    s1 = lambda p: var_cf(p, g_kalman(p, 1.0))
    peak = s1(pstar)
    xlo = brentq(lambda p: s1(p) - 0.05, 1e-3, pstar, xtol=1e-15, rtol=1e-15)
    xhi = brentq(lambda p: s1(p) - 0.05, pstar, 1e3, xtol=1e-15, rtol=1e-15)
    thr = brentq(lambda p: s1(p) - 0.008, 1.0, 1e4, xtol=1e-13, rtol=1e-15)
    cal = [var_cf(p, g_kalman(p, 100.0)) for p in (0.01, 1, 100)]
    opt = [var_cf(p, g_opt(p)) for p in (0.01, 1, 100)]
    opt2 = [g_opt(p) / p for p in (0.01, 1, 100)]
    # exact rational crossing check
    s1sym = sig2.subs(vals).subs(P, 1)
    exact_cross = [sp.nsimplify(sp.simplify(s1sym.subs(Pi, v)) - sp.Rational(1, 20)) for v in (sp.Rational(1, 9), 4)]

    def sig_digits(s):
        s = s.lstrip("0.").replace(".", "")
        return len(s)

    table = [  # (name, computed, stated string or exact value, n_sig)
        ("peak sigma^2", peak, "0.0929"), ("Pi* (peak location)", pstar, "0.687"),
        ("R2=0.05 lower crossing", xlo, 1 / 9), ("R2=0.05 upper crossing", xhi, 4.0),
        ("R2=0.008 threshold", thr, "82.67"),
        ("calibrated Pi=0.01", cal[0], "0.0100"), ("calibrated Pi=1", cal[1], "0.00995"),
        ("calibrated Pi=100", cal[2], "0.0075"),
        ("optimal Pi=0.01", opt[0], "0.0100"), ("optimal Pi=1", opt[1], "0.00995"),
        ("optimal Pi=100", opt[2], "0.00732"),
    ]
    out("")
    out(f"{'quantity':28s} {'computed':>14s} {'stated':>10s} {'n':>2s} {'tol':>10s}  res  strict4sf")
    num_ok = True
    numbers = {}
    for name, comp, st in table:
        if isinstance(st, str):
            sv, n = float(st), min(4, sig_digits(st))
        else:
            sv, n = st, 4
        e = math.floor(math.log10(abs(sv)))
        tol = 0.5 * 10 ** (e - n + 1)
        ok = abs(comp - sv) <= tol
        strict = abs(comp - sv) <= 0.5 * 10 ** (e - 3)
        num_ok &= ok
        numbers[name] = {"computed": comp, "stated": sv, "n_sig": n, "pass": ok, "strict4sf": strict}
        out(f"{name:28s} {comp:14.8g} {sv:10.6g} {n:2d} {tol:10.2e}  {'ok' if ok else 'XX'}   {'ok' if strict else 'differs'}")
    out(f"exact symbolic: sigma^2(1/9)-1/20 = {exact_cross[0]}, sigma^2(4)-1/20 = {exact_cross[1]}")
    out(f"optimal sigma*^2 via G*/Pi: {opt2}  (max |diff| vs (2) at G*: {max(abs(x - y) for x, y in zip(opt, opt2)):.2e})")
    check("T1.9", "worked-example numbers match at stated precision (<=4 s.f.)",
          num_ok and all(e == 0 for e in exact_cross))

all_pass = all(v["pass"] for v in crit.values())
out(f"\nT1 overall: {'PASS' if all_pass else 'FAIL'}   runtime {T.dt:.1f}s")
with open(f"{RES}/t1_symbolic.txt", "w") as f:
    f.write("\n".join(lines) + "\n")
dump("t1.json", {"criteria": crit, "numbers": numbers, "pass": all_pass, "runtime_s": T.dt,
                 "latex_numerator": sp.latex(num), "Pi_star": pstar, "peak": peak,
                 "cross_lo": xlo, "cross_hi": xhi, "thr_0008": thr})
