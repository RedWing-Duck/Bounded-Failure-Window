"""Task 6: derive the coloured-noise stationary variance from the 2-D Lyapunov equation
and check the small-Pi rise condition c/P > 2F(1 + lambda tau)."""
import ast
import json
import os
import re

import numpy as np
import sympy as sp

from common import DT, HERE, NTRAJ, RES, Timer, dump

lines, crit = [], {}


def out(s=""):
    print(s)
    lines.append(s)


def check(key, desc, ok, detail=""):
    crit[key] = {"desc": desc, "pass": bool(ok), "detail": str(detail)}
    out(f"[{'PASS' if ok else 'FAIL'}] {key}: {desc} -- {detail}")


def r3(x):
    return float(f"{x:.3g}")


with Timer() as T:
    # ------------------------------------------------------------------ Step 1: t4b normalisation
    src_path = os.path.join(HERE, "t4b_colored.py")
    src = open(src_path).read()
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "make_sensory")
    fn_src = ast.get_source_segment(src, fn)
    spec_line = next(ln.strip() for ln in src.splitlines() if ln.strip().startswith("specs ="))
    out("== Step 1: sensory-noise normalisation in t4b_colored.py (read-only) ==")
    out("make_sensory source:")
    out("\n".join("    " + ln for ln in fn_src.splitlines()))
    out("relay specs line (gs = sensory coefficient, 2nd entry):  " + spec_line)
    out("common.run_em: u = gs * dWs + gm * dWm, with dWs replaced by the value returned by sensory().")
    from scipy.signal import lfilter
    ns = {"np": np, "lfilter": lfilter, "DT": DT, "NTRAJ": NTRAJ}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), src_path, "exec"), ns)
    norm = {}
    for tau in (0.01, 0.1, 1.0, 10.0):
        sens = ns["make_sensory"](tau, 0)
        state = next(c.cell_contents for c in sens.__closure__ if isinstance(c.cell_contents, dict))
        state["z"] = np.zeros((1, 1))
        imp = np.zeros((1, 6))
        imp[0, 0] = np.sqrt(DT)                     # xi_0 = 1
        eta = sens(0, imp)[0] / DT                  # eta_n = innov * rho^n
        innov, rho = eta[0], eta[1] / eta[0]
        var_u = innov**2 / (1 - rho**2)             # stationary variance of the unit process
        iac_u = var_u * (1 + rho) / (1 - rho) * DT  # sum of discrete autocov x dt
        norm[tau] = {"rho": rho, "rho_expected": np.exp(-DT / tau), "innov": innov, "var_unit": var_u,
                     "var_unit_expected": 1 / (2 * tau), "int_autocov_unit_discrete": iac_u,
                     "int_autocov_unit_continuous": 2 * var_u * tau}
        out(f"  tau={tau:5g}: rho={rho:.12f} (exp(-dt/tau)={np.exp(-DT/tau):.12f}), stationary var={var_u:.10g} "
            f"(1/(2tau)={1/(2*tau):.10g}), int autocov (continuous 2*var*tau)={2*var_u*tau:.10g}, "
            f"(discrete sum*dt)={iac_u:.6g}")
    norm_ok = all(abs(v["var_unit"] / v["var_unit_expected"] - 1) < 1e-12 and
                  abs(v["rho"] / v["rho_expected"] - 1) < 1e-12 for v in norm.values()) and \
        "g / np.sqrt(p)" in spec_line
    norm_stmt = ("t4b generates a unit OU process eta_u by exact AR(1) discretisation, rho = exp(-dt/tau), "
                 "innovation sd = sqrt((1/(2tau))(1-rho^2)), started from its stationary law, so eta_u has "
                 "stationary variance 1/(2tau) and integrated autocovariance 2*tau*(1/(2tau)) = 1, i.e. "
                 "d eta_u = -eta_u/tau dt + (1/tau) dW_s. The relay multiplies eta_u*dt by gs = G/sqrt(Pi), so "
                 "the effective sensory noise is eta = eta_u/sqrt(Pi): stationary variance 1/(2 Pi tau), "
                 "integrated autocovariance 1/Pi, d eta = -eta/tau dt + (1/(tau sqrt(Pi))) dW_s. "
                 + ("This MATCHES the expected normalisation." if norm_ok else
                    "This does NOT match the expected normalisation (see numbers above)."))
    out(norm_stmt)
    out("(The discrete sum of the AR(1) autocovariance times dt differs from 1 by O((dt/tau)^2) from discretisation; "
        "the continuous-time integral 2*var*tau is exactly 1.)")

    # ------------------------------------------------------------------ Step 2: Lyapunov solution
    lam, c, S, P, Pi, tau, G = sp.symbols("lambda c Sigma P Pi tau G", positive=True)
    a = lam + G
    A = sp.Matrix([[-a, G], [0, -1 / tau]])
    B = sp.diag(sp.sqrt(2 * S), 1 / (tau * sp.sqrt(Pi)))
    cxx, cxe, cee = sp.symbols("C_xx C_xe C_ee")
    Cm = sp.Matrix([[cxx, cxe], [cxe, cee]])
    L = A * Cm + Cm * A.T + B * B.T
    sol = sp.solve([L[0, 0], L[0, 1], L[1, 1]], [cxx, cxe, cee], dict=True)[0]
    Cxx = sp.simplify(sol[cxx])
    out("\n== Step 2: stationary Lyapunov solution ==")
    out(f"C_xx = {Cxx}")
    out(f"C_xeta = {sp.simplify(sol[cxe])},  C_etaeta = {sp.simplify(sol[cee])}")
    out("LaTeX C_xx: " + sp.latex(Cxx))
    Fs = S / lam

    rng = np.random.default_rng(6006)
    rand_sets = []
    for _ in range(20):
        v = 10 ** rng.uniform(-2, 2, 7)
        rand_sets.append({s_: sp.Rational(str(float(x_))) for s_, x_ in zip((lam, c, S, P, Pi, tau, G), v)})

    def numeric(lhs, rhs):
        worst = 0.0
        for d in rand_sets:
            Lv, Rv = sp.N(lhs.subs(d), 50), sp.N(rhs.subs(d), 50)
            den = max(abs(Lv), abs(Rv))
            rel = 0.0 if den == 0 else float(abs(Lv - Rv) / den)
            worst = max(worst, rel)
        return worst <= 1e-12, worst

    def identity(key, desc, lhs, rhs, extra_ok=True, extra=""):
        sym = sp.simplify(lhs - rhs) == 0
        num_ok, worst = numeric(lhs, rhs)
        detail = f"simplify(diff)==0: {sym}; numeric 20 sets @50 digits: max rel err {worst:.2e} ({'ok' if num_ok else 'FAIL'})"
        if extra:
            detail += "; " + extra
        if sym and num_ok and extra_ok:
            check(key, desc, True, detail)
        elif (not sym) and num_ok and extra_ok:
            crit[key] = {"desc": desc, "pass": True, "numeric_only": True, "detail": detail}
            out(f"[PASS (numeric only; simplification inconclusive)] {key}: {desc} -- {detail}")
        else:
            check(key, desc, False, detail)
        return sym, num_ok, worst

    out("\n== Criteria ==")
    # C1
    target1 = (S + G**2 / (2 * Pi * (1 + a * tau))) / a
    identity("C1", "C_xx == (Sigma + G^2/(2 Pi (1+a tau)))/a", Cxx, target1)

    # C2
    white = (S + G**2 / (2 * Pi)) / (lam + G)
    lim0 = sp.limit(Cxx, tau, 0)
    sub0 = sp.simplify(Cxx.subs(tau, 0))
    identity("C2", "lim_{tau->0} C_xx == (Sigma + G^2/(2Pi))/(lambda+G)", lim0, white,
             extra_ok=sp.simplify(sub0 - white) == 0, extra=f"direct tau=0 substitution matches: {sp.simplify(sub0 - white) == 0}")

    # C3
    fac = sp.factor(Cxx - Fs)
    out(f"C3 factorisation as returned by sympy.factor(C_xx - F):\n    {fac}\n    LaTeX: {sp.latex(fac)}")
    target3 = G * (lam * G / (2 * Pi * (1 + a * tau)) - S) / (lam * a)
    bracket = lam * G / (2 * Pi * (1 + a * tau)) - S
    cond = G / Pi - 2 * Fs * (1 + a * tau)
    mult = 2 * (1 + a * tau) / lam
    s_a = sp.simplify(Cxx - Fs - target3) == 0
    n_a = numeric(Cxx - Fs, target3)
    s_b = sp.simplify(bracket * mult - cond) == 0
    n_b = numeric(bracket * mult, cond)
    pos = sp.ask(sp.Q.positive(mult)) is True and sp.ask(sp.Q.positive(G / (lam * a))) is True
    ok3 = (s_a or n_a[0]) and (s_b or n_b[0]) and pos and n_a[0] and n_b[0]
    det3 = (f"C_xx-F == G(lam G/(2Pi(1+a tau)) - Sigma)/(lam a): simplify {s_a}, numeric max rel {n_a[1]:.2e}; "
            f"bracket*2(1+a tau)/lam == G/Pi - 2F(1+a tau): simplify {s_b}, numeric max rel {n_b[1]:.2e}; "
            f"multipliers 2(1+a tau)/lam and G/(lam a) proven positive: {pos}")
    if ok3 and not (s_a and s_b):
        crit["C3"] = {"desc": "coloured excess identity; C_xx > F iff G/Pi > 2F(1+a tau)", "pass": True,
                      "numeric_only": True, "detail": det3}
        out(f"[PASS (numeric only; simplification inconclusive)] C3: {det3}")
    else:
        check("C3", "coloured excess identity; C_xx > F iff G/Pi > 2F(1+a tau)", ok3, det3)

    # C4
    Gk = c * Pi / (Pi + P)
    CxxK = Cxx.subs(G, Gk)
    ser = sp.series(CxxK, Pi, 0, 2).removeO()
    s0 = sp.simplify(ser.subs(Pi, 0))
    s1 = sp.simplify(sp.diff(ser, Pi))
    s1_target = c * (c * lam - 2 * P * S * (1 + lam * tau)) / (2 * P**2 * lam**2 * (1 + lam * tau))
    s1_ok = sp.simplify(s1 - s1_target) == 0
    n4 = numeric(s1, s1_target)
    ratio = sp.factor(sp.simplify(s1 / (c / P - 2 * Fs * (1 + lam * tau))))
    ratio_pos = sp.ask(sp.Q.positive(ratio)) is True
    out(f"C4 series: C_xx = {s0} + ({sp.factor(s1)})*Pi + O(Pi^2)")
    out(f"    LaTeX: {sp.latex(s0)} + {sp.latex(sp.factor(s1))}\\,\\Pi + O(\\Pi^2)")
    out(f"    s1 / (c/P - 2F(1+lam tau)) = {ratio}  (proven positive: {ratio_pos})")
    ok4 = sp.simplify(s0 - Fs) == 0 and (s1_ok or n4[0]) and n4[0] and ratio_pos
    det4 = (f"constant term == F: {sp.simplify(s0 - Fs) == 0}; s1 == stated: simplify {s1_ok}, numeric max rel "
            f"{n4[1]:.2e}; sign(s1) == sign(c/P - 2F(1+lam tau)): {ratio_pos}")
    if not s1_ok:
        det4 += f"; SymPy s1 verbatim: {s1}"
    check("C4", "series F + s1 Pi, s1 = c(c lam - 2P Sigma(1+lam tau))/(2P^2 lam^2(1+lam tau)); rise iff c/P > 2F(1+lam tau)",
          ok4, det4)

    # C5
    vals = {lam: 1, c: 1, S: sp.Rational(1, 100), P: 1}
    f_cxx = sp.lambdify((Pi, tau), CxxK.subs(vals), "numpy")
    grid = np.logspace(-4, 4, 200001)
    t4b = json.load(open(os.path.join(RES, "t4b.json")))
    t4b_grid = np.logspace(-3, 4, 4001)
    c5_rows, ok5 = [], True
    for r in t4b["rows"]:
        tv = r["tau"]
        v = f_cxx(grid, tv)
        i = int(np.argmax(v))
        ph, pl = float(v[i]), float(grid[i])
        sh, sl = r["semi"]["peak"], r["semi"]["peak_Pi"]
        mh, ml = r3(ph) == r3(sh), r3(pl) == r3(sl)
        vb = f_cxx(t4b_grid, tv)
        j = int(np.argmax(vb))
        repro = abs(vb[j] / sh - 1) < 1e-12 and abs(t4b_grid[j] / sl - 1) < 1e-12
        ok5 &= mh and ml
        c5_rows.append({"tau": tv, "peak": ph, "peak_Pi": pl, "t4b_peak": sh, "t4b_peak_Pi": sl,
                        "match_height": mh, "match_loc": ml, "t4b_grid_reproduced": bool(repro)})
    out("C5 table (tau | peak here | t4b peak | 3sf match | Pi* here | t4b Pi* | 3sf match | t4b grid reproduced):")
    for r in c5_rows:
        out(f"    {r['tau']:5g} | {r['peak']:.6f} | {r['t4b_peak']:.6f} | {r['match_height']} | {r['peak_Pi']:.5f} | "
            f"{r['t4b_peak_Pi']:.5f} | {r['match_loc']} | {r['t4b_grid_reproduced']}")
    # post-hoc diagnostic (NOT pre-registered): exact stationary point of C_xx in Pi
    dC = sp.diff(CxxK.subs(vals), Pi)
    for r in c5_rows:
        root = sp.nsolve(dC.subs(tau, sp.Rational(str(r["tau"]))), Pi, r["peak_Pi"], prec=30)
        r["exact_peak_Pi"] = float(root)
        r["exact_peak"] = float(CxxK.subs(vals).subs({tau: sp.Rational(str(r["tau"])), Pi: root}).evalf(30))
    out("C5 post-hoc diagnostic (not pre-registered): exact peak from dC_xx/dPi = 0 (sympy.nsolve, 30 digits):")
    for r in c5_rows:
        out(f"    tau={r['tau']:5g}: Pi* = {r['exact_peak_Pi']:.6f} (3 s.f. {r3(r['exact_peak_Pi'])}), "
            f"peak = {r['exact_peak']:.6f}; 200,001-pt grid Pi* {r['peak_Pi']:.5f}; t4b grid Pi* {r['t4b_peak_Pi']:.5f}")
    check("C5", "peaks on 200,001-pt grid match t4b semi-analytic peaks to 3 s.f. (height and location)", ok5,
          "; ".join(f"tau={r['tau']:g}: {r3(r['peak'])} at {r3(r['peak_Pi'])} vs {r3(r['t4b_peak'])} at "
                    f"{r3(r['t4b_peak_Pi'])}" for r in c5_rows))

    # C6
    eps = sp.Rational(1, 10**10)
    c6_rows, ok6 = [], True
    for tv in ("48", "48.9", "49.1", "50"):
        tr = sp.Rational(tv)
        slope = sp.N((CxxK.subs(vals).subs(tau, tr).subs(Pi, eps) - sp.Rational(1, 100)) / eps, 50)
        s1v = sp.N(s1.subs(vals).subs(tau, tr), 30)
        pred = float(tr) < 49
        match = (slope > 0) == pred
        ok6 &= bool(match)
        c6_rows.append({"tau": float(tr), "numeric_slope": float(slope), "s1": float(s1v), "predicted_rise": pred,
                        "match": bool(match)})
    check("C6", "sign of numeric slope at Pi->0 matches 'rise iff tau < 49' (P=1)", ok6,
          "; ".join(f"tau={r['tau']:g}: slope={r['numeric_slope']:.4e} (s1={r['s1']:.4e})" for r in c6_rows))
    info6 = []
    f_ex = sp.lambdify((Pi, tau), sp.factor(target3.subs(G, Gk).subs(vals)), "numpy")
    f_cond = sp.lambdify((Pi, tau), cond.subs(G, Gk).subs(vals), "numpy")
    for tv in (50.0, 100.0, 1000.0):
        ex = f_ex(grid, tv)
        cd = f_cond(grid, tv)
        i, k = int(np.argmax(ex)), int(np.argmax(cd))
        info6.append({"tau": tv, "max_excess": float(ex[i]), "max_excess_Pi": float(grid[i]),
                      "sup_cond": float(cd[k]), "sup_cond_Pi": float(grid[k]),
                      "cond_limit_Pi0": float(1 - 0.02 * (1 + tv))})
    dcond = sp.simplify(sp.diff(cond.subs(G, Gk), Pi))
    dcond_neg = sp.ask(sp.Q.negative(dcond)) is True
    out("C6 informational (P=1, grid 1e-4..1e4): tau | max(C_xx)-F | at Pi | sup[G/Pi-2F(1+a tau)] | at Pi | limit Pi->0")
    for r in info6:
        out(f"    {r['tau']:6g} | {r['max_excess']:.4e} | {r['max_excess_Pi']:.4g} | {r['sup_cond']:.6f} | "
            f"{r['sup_cond_Pi']:.4g} | {r['cond_limit_Pi0']:.6f}")
    out(f"    d/dPi [G/Pi - 2F(1+a tau)] (Kalman gain) = {dcond}; proven negative for all positive parameters: {dcond_neg}")

all_pass = all(v["pass"] for v in crit.values())
out(f"\nT6 overall: {'PASS' if all_pass else 'FAIL'}   runtime {T.dt:.1f}s")
with open(os.path.join(RES, "t6_colored.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
dump("t6.json", {"criteria": crit, "pass": all_pass, "runtime_s": T.dt, "normalisation": norm_stmt,
                 "normalisation_ok": bool(norm_ok), "norm_numbers": {str(k): v for k, v in norm.items()},
                 "Cxx": str(Cxx), "Cxx_latex": sp.latex(Cxx), "C3_factor": str(fac), "C3_factor_latex": sp.latex(fac),
                 "C4_s1": str(sp.factor(s1)), "C4_series_latex": f"{sp.latex(s0)} + {sp.latex(sp.factor(s1))}\\,\\Pi + O(\\Pi^2)",
                 "C4_ratio": str(ratio), "c5": c5_rows, "c6": c6_rows, "c6_info": info6,
                 "dcond": str(dcond), "dcond_negative": dcond_neg})
