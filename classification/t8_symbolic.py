"""T8.1: analytic checks of Lemma 3.1, Props 4.1/5.1, limits, approach directions; Paper 1 limiting case."""
import numpy as np
import sympy as sp

from t8_common import C, LAM, SIG, analyse, classify, name, precision_sweep, save_json, sf_match

lam, Sig, Pi, Pi0, G, c = sp.symbols("lambda Sigma Pi Pi_0 G c", positive=True)
SYMS = [lam, Sig, Pi, Pi0, G, c]
F = Sig / lam
s = sp.sqrt(lam**2 + 2 * Sig * Pi)
Gs = -lam + s
sig2 = lambda g, p=Pi: (Sig + g**2 / (2 * p)) / (lam + g)
PiA = c * (c + 2 * lam) / (2 * Sig)
PiB = c * lam / (2 * Sig)
Vc = sig2(c)
K = Pi / (Pi + Pi0)

rng = np.random.default_rng(8001)
POINTS = [{x: sp.Rational(float(10.0**rng.uniform(-2, 2))) for x in SYMS} for _ in range(20)]
R = {}
LINES = []


def out(t):
    print(t)
    LINES.append(t)


def identity(key, desc, lhs, rhs=0):
    """PASS if simplify(lhs - rhs) == 0, else numeric fallback at 20 rational points."""
    rhs = sp.sympify(rhs)
    simp = sp.simplify(lhs - rhs)
    if simp == 0:
        rec = {"desc": desc, "route": "simplify", "pass": True}
    else:
        ok, worst = True, 0.0
        for P in POINTS:
            a, b = lhs.subs(P).evalf(50), rhs.subs(P).evalf(50)
            err = abs(a - b) / max(abs(a), abs(b), sp.Float("1e-300"))
            worst = max(worst, float(err))
            ok &= bool(abs(a - b) <= sp.Float("1e-12") * max(abs(a), abs(b), sp.Float("1e-300")))
        rec = {"desc": desc, "route": "numeric only", "pass": bool(ok), "max_rel": worst,
               "sympy_simplify_verbatim": str(simp)}
    R.setdefault(key, []).append(rec)
    out(f"  [{'PASS' if rec['pass'] else 'FAIL'}] ({rec['route']}) {desc}"
        + ("" if rec["route"] == "simplify" else f"  simplify gave: {rec['sympy_simplify_verbatim']}"))
    return rec["pass"]


def sign(key, desc, expr, want):
    """Sign claim: SymPy assumption query on an expression in positive symbols."""
    q = sp.simplify(expr).is_positive if want > 0 else sp.simplify(expr).is_negative
    route = "assumptions"
    ok = bool(q)
    if q is None:
        route = "numeric only"
        vals = [float(expr.subs(P).evalf(50)) for P in POINTS]
        ok = all(v > 0 for v in vals) if want > 0 else all(v < 0 for v in vals)
    R.setdefault(key, []).append({"desc": desc, "route": route, "pass": ok})
    out(f"  [{'PASS' if ok else 'FAIL'}] ({route}) {desc}")
    return ok


# (a)
out("(a) derivative")
identity("a", "d sigma2/dG - (G^2+2 lam G-2 Sig Pi)/(2 Pi (lam+G)^2) == 0",
         sp.diff(sig2(G), G), (G**2 + 2 * lam * G - 2 * Sig * Pi) / (2 * Pi * (lam + G)**2))

# (b)
out("(b) unique positive root, minimum value, below F")
Gx = sp.symbols("G_x", real=True)
roots = sp.solve(Gx**2 + 2 * lam * Gx - 2 * Sig * Pi, Gx)
out(f"  solve(G^2+2 lam G-2 Sig Pi) = {roots}")
ok_roots = len(roots) == 2 and {sp.simplify(r - (-lam + s)) == 0 or sp.simplify(r - (-lam - s)) == 0
                                for r in roots} == {True} and sp.simplify(sum(roots) + 2 * lam) == 0
R.setdefault("b", []).append({"desc": "roots are exactly -lam +/- s", "route": "solve", "pass": bool(ok_roots)})
out(f"  [{'PASS' if ok_roots else 'FAIL'}] (solve) roots are exactly -lam +/- s")
sign("b", "-lam - s < 0", -lam - s, -1)
identity("b", "G* - 2 Sig Pi/(lam+s) == 0", Gs, 2 * Sig * Pi / (lam + s))
sign("b", "2 Sig Pi/(lam+s) > 0 (so G* > 0: exactly one positive root)", 2 * Sig * Pi / (lam + s), +1)
identity("b", "sigma2(G*, Pi) - G*/Pi == 0", sig2(Gs), Gs / Pi)
identity("b", "F - G*/Pi - 2 Sig^2 Pi/(lam (lam+s)^2) == 0", F - Gs / Pi, 2 * Sig**2 * Pi / (lam * (lam + s)**2))
sign("b", "2 Sig^2 Pi/(lam (lam+s)^2) > 0 (so G*/Pi < F)", 2 * Sig**2 * Pi / (lam * (lam + s)**2), +1)

# (c)
out("(c) excess identity")
identity("c", "sigma2 - F - G (lam G/(2 Pi) - Sig)/(lam (lam+G)) == 0",
         sig2(G) - F, G * (lam * G / (2 * Pi) - Sig) / (lam * (lam + G)))
num = sp.numer(sp.together(G * (lam * G / (2 * Pi) - Sig)))
zs = sp.solve(num.subs(G, Gx), Gx)
ok_z = len(zs) == 2 and sorted([sp.simplify(z) for z in zs], key=str) == sorted([sp.Integer(0), sp.simplify(2 * F * Pi)], key=str)
R.setdefault("c", []).append({"desc": "zeros of the excess at G = 0 and G = 2 F Pi", "route": "solve",
                              "pass": bool(ok_z), "sympy": str(zs)})
out(f"  [{'PASS' if ok_z else 'FAIL'}] (solve) zeros: {zs}  (2 F Pi = {2 * F * Pi})")

# (d)
out("(d) prior sweep")
P0s = Pi * (c / Gs - 1)
identity("d", "G(Pi0*) - G* == 0 at Pi0* = Pi (c/G* - 1)", c * Pi / (Pi + P0s), Gs)
identity("d", "c - G* - 2 Sig (Pi_A - Pi)/(c+lam+s) == 0", c - Gs, 2 * Sig * (PiA - Pi) / (c + lam + s))
sign("d", "c + lam + s > 0", c + lam + s, +1)
identity("d", "c - 2 F Pi - 2 F (Pi_B - Pi) == 0", c - 2 * F * Pi, 2 * F * (PiB - Pi))
identity("d", "Pi_A - Pi_B - c (c+lam)/(2 Sig) == 0", PiA - PiB, c * (c + lam) / (2 * Sig))
sign("d", "c (c+lam)/(2 Sig) > 0 (Pi_B < Pi_A)", c * (c + lam) / (2 * Sig), +1)
identity("d", "V_c - F - c (c - 2 F Pi)/(2 Pi (lam+c)) == 0", Vc - F, c * (c - 2 * F * Pi) / (2 * Pi * (lam + c)))
sign("d", "c/(2 Pi (lam+c)) > 0 (V_c > F iff c > 2 F Pi)", c / (2 * Pi * (lam + c)), +1)

# (e)
out("(e) coupling sweep")
cst = Gs / K
identity("e", "c* K - G* == 0", cst * K, Gs)
identity("e", "c* - (Pi+Pi0)(s - lam)/Pi == 0", cst, (Pi + Pi0) * (s - lam) / Pi)
cF = 2 * F * Pi / K
identity("e", "c_F - 2 F (Pi+Pi0) == 0", cF, 2 * F * (Pi + Pi0))
identity("e", "sigma2(c_F K, Pi) - F == 0", sig2(cF * K), F)

# (f)
out("(f) limits")
prior = sig2(c * Pi / (Pi + Pi0))
coup = sig2(c * K)
lims = [("prior, Pi0 -> 0+", sp.limit(prior, Pi0, 0, "+"), Vc),
        ("prior, Pi0 -> oo", sp.limit(prior, Pi0, sp.oo), F),
        ("coupling, c -> 0+", sp.limit(coup, c, 0, "+"), F),
        ("coupling, c -> oo", sp.limit(coup, c, sp.oo), sp.oo)]
for d, got, want in lims:
    ok = (got == want) if want == sp.oo else sp.simplify(got - want) == 0
    R.setdefault("f", []).append({"desc": d, "route": "limit", "pass": bool(ok), "sympy": str(got)})
    out(f"  [{'PASS' if ok else 'FAIL'}] (limit) {d}: {got}")

# (g)
out("(g) approach directions")
dprior = sp.diff(prior, Pi0)
l_inf = sp.limit(Pi0**2 * dprior, Pi0, sp.oo)
identity("g", f"lim_{{Pi0->oo}} Pi0^2 d sigma2/dPi0 - c Pi Sig/lam^2 == 0 (sympy: {l_inf})", l_inf, c * Pi * Sig / lam**2)
sign("g", "c Pi Sig/lam^2 > 0 (F approached from below)", c * Pi * Sig / lam**2, +1)
l0 = sp.limit(dprior, Pi0, 0, "+")
identity("g", "lim_{Pi0->0} d sigma2/dPi0 + c (c^2+2 lam c-2 Sig Pi)/(2 Pi^2 (lam+c)^2) == 0",
         l0, -c * (c**2 + 2 * lam * c - 2 * Sig * Pi) / (2 * Pi**2 * (lam + c)**2))
identity("g", "c^2+2 lam c-2 Sig Pi - (c - G*)(c+lam+s) == 0 (sign = sign(c - G*))",
         c**2 + 2 * lam * c - 2 * Sig * Pi, (c - Gs) * (c + lam + s))
lc = sp.limit(sp.diff(coup, c), c, 0, "+")
identity("g", "lim_{c->0} d sigma2/dc + K Sig/lam^2 == 0", lc, -K * Sig / lam**2)
sign("g", "-K Sig/lam^2 < 0 (F approached from below)", -K * Sig / lam**2, -1)

# (h) Paper 1 limiting case
out("(h) Paper 1 precision sweep, Pi0 = 1 (kappa = 100)")
F0, H0 = SIG / LAM, SIG / (LAM + C)
A = analyse(*precision_sweep(1.0))
turns = A["turns"]
hrec = {"turns": [(t["theta"], t["value"], t["kind"]) for t in turns], "L_minus": A["L_minus"],
        "L_plus": A["L_plus"], "approach_minus": A["approach_minus"], "approach_plus": A["approach_plus"]}
ok_struct = (len(turns) == 1 and turns[0]["kind"] == "max" and abs(A["L_minus"] - F0) <= 1e-12 * F0
             and abs(A["L_plus"] - H0) <= 1e-12 * H0 and A["approach_minus"] == "above" and A["approach_plus"] == "above")
M = turns[0]["value"] if turns else float("nan")
pst = turns[0]["theta"] if turns else float("nan")
ok_vals = sf_match(M, 0.09288) and sf_match(pst, 0.6867)
out(f"  turning points: {hrec['turns']}; L- = {A['L_minus']!r} ({A['approach_minus']}), "
    f"L+ = {A['L_plus']!r} ({A['approach_plus']})")
out(f"  [{'PASS' if ok_struct else 'FAIL'}] sequence (F, M, H), one max, both ends approached from above")
out(f"  [{'PASS' if ok_vals else 'FAIL'}] M = {M:.6g} (stated 0.09288), Pi* = {pst:.6g} (stated 0.6867)")
# C4 wording check: sample the first and last pieces directly and compare with the limits
x1 = turns[0]["x"] - 1.0 if turns else 0.0
x2 = turns[-1]["x"] + 1.0 if turns else 0.0
f_prec = precision_sweep(1.0)[0]
c4 = {"first_piece_dir": A["pieces"][0]["dir"], "last_piece_dir": A["pieces"][-1]["dir"],
      "sigma2_first_piece_minus_Lminus": float(f_prec(10.0**x1) - A["L_minus"]),
      "sigma2_last_piece_minus_Lplus": float(f_prec(10.0**x2) - A["L_plus"])}
out(f"  C4 check: first piece dir {c4['first_piece_dir']:+d}, sigma2 - L- = {c4['sigma2_first_piece_minus_Lminus']:.3g}; "
    f"last piece dir {c4['last_piece_dir']:+d}, sigma2 - L+ = {c4['sigma2_last_piece_minus_Lplus']:.3g}")
d = 1e-6
table = [(H0, "All"), (H0 * (1 - d), "All"), (H0 * (1 + d), "lower ray"),
         (F0, "lower ray"), (F0 * (1 - d), "lower ray"), (F0 * (1 + d), "window"),
         (M, "Empty"), (M * (1 - d), "window"), (M * (1 + d), "Empty"),
         (H0 / 2, "All"), ((H0 + F0) / 2, "lower ray"), ((F0 + M) / 2, "window"), (1.5 * M, "Empty")]
rows = []
for r2, want in table:
    got = name(classify(A, r2)["class"])
    rows.append({"R2": r2, "expected": want, "got": got, "match": got == want})
    out(f"    R2 = {r2:.8g}: {got} (expected {want}) {'ok' if got == want else 'MISMATCH'}")
ok_tab = all(r["match"] for r in rows)
R["h"] = [{"desc": "Paper 1 structure", "pass": ok_struct, **hrec, "C4_check": c4},
          {"desc": "M = 0.09288 at Pi* = 0.6867 (4 s.f.)", "pass": ok_vals, "M": M, "Pi_star": pst},
          {"desc": "four-regime table via the classifier", "pass": ok_tab, "rows": rows}]

summary = {k: all(r["pass"] for r in v) for k, v in R.items()}
routes = sorted({r.get("route", "-") for v in R.values() for r in v})
R["summary"] = summary
R["pass"] = all(summary.values())
R["numeric_only"] = [r["desc"] for v in R.values() if isinstance(v, list) for r in v if r.get("route") == "numeric only"]
R["lines"] = LINES
out(f"T8.1: {'PASS' if R['pass'] else 'FAIL'}  parts: {summary}; numeric-only identities: {len(R['numeric_only'])}")
save_json(R, "t8_1.json")
