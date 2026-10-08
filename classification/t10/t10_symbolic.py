"""T10.1: symbolic checks (exact reduction to 0, no numeric fallback)."""
import sympy as sp

from t10_common import save_json

lam, Sig, Pi, Pi0, c, G, t, v, R2, tau, P, g = sp.symbols("lambda Sigma Pi Pi_0 c G t v R2 tau P g", positive=True)
l1, S1, u = sp.symbols("lambda1 Sigma1 u", positive=True)
F = Sig / lam
s = sp.sqrt(lam**2 + 2 * Sig * Pi)
Gs = -lam + s
sig2 = lambda GG, PP: (Sig + GG**2 / (2 * PP)) / (lam + GG)
Nf = lambda GG, ee, PP: ee * (GG**2 + 2 * lam * GG - 2 * Sig * PP) - GG * (lam + GG)
R, LINES = {}, []


def out(x):
    print(x)
    LINES.append(x)


def zero(key, desc, e):
    route, ok = None, False
    if sp.simplify(e) == 0:
        route, ok = "simplify", True
    elif sp.simplify(sp.together(sp.expand(e))) == 0:
        route, ok = "simplify(together(expand))", True
    else:
        roots = [p for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)]
        if len(roots) == 1:
            r = roots[0]
            num = sp.numer(sp.together(e.subs(r, u)))
            if sp.simplify(sp.rem(sp.expand(num), u**2 - r.base, u)) == 0:
                route, ok = "sqrt-remainder", True
    rec = {"desc": desc, "route": route or "none", "pass": ok}
    if not ok:
        rec["sympy_verbatim"] = str(sp.simplify(e))
    R.setdefault(key, []).append(rec)
    out(f"  [{'PASS' if ok else 'FAIL'}] ({rec['route']}) {desc}" + ("" if ok else f"  SymPy: {rec['sympy_verbatim']}"))


# (a) elasticity lemma, general G(Pi)
out("(a) elasticity lemma")
Gf = sp.Function("G")(Pi)
eps = Pi * sp.diff(Gf, Pi) / Gf
zero("a", "d sigma2/dPi - G N/(2 Pi^2 (lam+G)^2) == 0 for general G(Pi)",
     sp.diff(sig2(Gf, Pi), Pi) - Gf * Nf(Gf, eps, Pi) / (2 * Pi**2 * (lam + Gf)**2))

# (b) Bayesian
out("(b) Bayesian-weight")
GB = c * Pi / (Pi + Pi0)
zero("b", "Pi G'/G - (1 - G/c) == 0 for G = c Pi/(Pi+Pi0)", Pi * sp.diff(GB, Pi) / GB - (1 - GB / c))
PiB = Pi0 * G / (c - G)
zero("b", "G(Pi(G)) - G == 0 for Pi = Pi0 G/(c - G)", GB.subs(Pi, PiB) - G)
zero("b", "c N + G (G^2 + 2 lam G + 2 Sig Pi0 - lam c) == 0",
     c * Nf(G, 1 - G / c, PiB) + G * (G**2 + 2 * lam * G + 2 * Sig * Pi0 - lam * c))

# (c) misspecified Kalman
out("(c) misspecified Kalman")
GM = -l1 + sp.sqrt(l1**2 + 2 * S1 * Pi)
PiM = (G**2 + 2 * l1 * G) / (2 * S1)
zero("c", "G(Pi(G)) - G == 0 for Pi = (G^2 + 2 lam' G)/(2 Sig')", GM.subs(Pi, PiM) - G)
zero("c", "Pi G'/G - (G + 2 lam')/(2 (G + lam')) == 0 (G = misspecified gain)",
     (Pi * sp.diff(GM, Pi) / GM - (GM + 2 * l1) / (2 * (GM + l1))))
r = Sig / S1
quadM = (1 + r) * G**2 + 4 * r * l1 * G - 2 * lam * l1 + 4 * r * l1**2
zero("c", "2 (G + lam') N / G + [(1+r) G^2 + 4 r lam' G - 2 lam lam' + 4 r lam'^2] == 0",
     2 * (G + l1) * Nf(G, (G + 2 * l1) / (2 * (G + l1)), PiM) / G + quadM)
Fp = S1 / l1
zero("c", "constant term + 2 lam lam' (1 - 2F/F') == 0", (-2 * lam * l1 + 4 * r * l1**2) + 2 * lam * l1 * (1 - 2 * F / Fp))

# (d) capped
out("(d) capped")
zero("d", "d/dPi sigma2(g Pi, Pi) - g (g lam/2 - Sig)/(lam + g Pi)^2 == 0",
     sp.diff(sig2(g * Pi, Pi), Pi) - g * (g * lam / 2 - Sig) / (lam + g * Pi)**2)
zero("d", "sigma2(2 F Pi, Pi) - F == 0 (plateau)", sig2(2 * F * Pi, Pi) - F)

# (e) Hill n = 2
out("(e) Hill n = 2")
GH = c * t**2 / (1 + t**2)
epsH = sp.simplify((Pi * sp.diff(c * Pi**2 / (Pi**2 + Pi0**2), Pi) / (c * Pi**2 / (Pi**2 + Pi0**2))).subs(Pi, Pi0 * t))
Q = (-c * (lam + c) * t**5 - 4 * Sig * Pi0 * t**4 + c * (c + 2 * lam) * t**3 - 8 * Sig * Pi0 * t**2
     + 3 * lam * c * t - 4 * Sig * Pi0)
zero("e", "N - t Q(t)/(1 + t^2)^3 == 0 (positive factor t/(1+t^2)^3)", Nf(GH, epsH, Pi0 * t) - t * Q / (1 + t**2)**3)
P4 = -(lam + c) * t**4 + (c + 2 * lam) * t**2 + 3 * lam
zero("e", "Q - [c t P4(t) - 4 Sig Pi0 (1 + t^2)^2] == 0", Q - (c * t * P4 - 4 * Sig * Pi0 * (1 + t**2)**2))

# (f) realizability inverse
out("(f) realizability inverse")
disc = Pi**2 * v**2 - 2 * Pi * (Sig - lam * v)
Gp = Pi * v + sp.sqrt(disc)
zero("f", "sigma2(G+, Pi) - v == 0", sig2(Gp, Pi) - v)
zero("f", "disc - Pi (Pi v^2 + 2 lam v - 2 Sig) == 0", disc - Pi * (Pi * v**2 + 2 * lam * v - 2 * Sig))
zero("f", "Pi v^2 + 2 lam v - 2 Sig - Pi (v - sigma*^2)(v + (lam + s)/Pi) == 0",
     Pi * v**2 + 2 * lam * v - 2 * Sig - Pi * (v - Gs / Pi) * (v + (lam + s) / Pi))
zero("f", "Pi sigma*^2 - G* == 0", Pi * (Gs / Pi) - Gs)

# (g) forced ray
out("(g) forced lower ray")
piR = 2 * lam * (F - R2) / R2**2
zero("g", "sigma*^2(pi_R) - R^2 == 0", sp.simplify((Gs / Pi).subs(Pi, piR)) - R2)

# (h) matched variance
out("(h) matched variance")
h = 1 / tau - lam
Rv = 2 * Sig + 2 * v / tau
Ric = -2 * lam * P + 2 * Sig - (h * P + 2 * Sig)**2 / Rv
Aq = (1 - lam * tau)**2 / tau
Bq = 4 * (Sig + lam * v)
zero("h", "-tau R_v Ric - [A P^2 + 4(Sig + lam v) P - 4 Sig v] == 0", -tau * Rv * Ric - (Aq * P**2 + Bq * P - 4 * Sig * v))
zero("h", "A(tau) - A(1/(lam^2 tau)) == 0", Aq - Aq.subs(tau, 1 / (lam**2 * tau)))
Ps = sp.symbols("P_s", positive=True)
Asym = sp.symbols("A", nonnegative=True)
Prat = 8 * Sig * v / (Bq + sp.sqrt(Bq**2 + 16 * Sig * v * Asym))
zero("h", "rationalized P satisfies A P^2 + B P - 4 Sig v = 0", Asym * Prat**2 + Bq * Prat - 4 * Sig * v)
zero("h", "P(A = 0) - Sig v/(Sig + lam v) == 0", Prat.subs(Asym, 0) - Sig * v / (Sig + lam * v))
AR = (4 * Sig * v - Bq * R2) / R2**2
taus = sp.solve(sp.Eq(lam**2 * tau**2 - (2 * lam + AR) * tau + 1, 0), tau)
zero("h", "(1 - lam tau)^2 - A_R tau == lam^2 tau^2 - (2 lam + A_R) tau + 1", sp.expand((1 - lam * tau)**2 - AR * tau - (lam**2 * tau**2 - (2 * lam + AR) * tau + 1)))
zero("h", "tau_- tau_+ - 1/lam^2 == 0", sp.Mul(*taus) - 1 / lam**2)
zero("h", "A_R defined by A P^2 + B P - C = 0 at P = R^2", AR * R2**2 + Bq * R2 - 4 * Sig * v)
a = lam + G
x11, x12, x22 = sp.symbols("x11 x12 x22")
Am = sp.Matrix([[-a, G], [0, -1 / tau]])
X = sp.Matrix([[x11, x12], [x12, x22]])
L = Am * X + X * Am.T + sp.diag(2 * Sig, 2 * v / tau)
sol = sp.solve([L[0, 0], L[0, 1], L[1, 1]], [x11, x12, x22], dict=True)[0]
zero("h", "Lyapunov X11 - (Sig + G^2 v tau/(1 + a tau))/a == 0", sol[x11] - (Sig + G**2 * v * tau / (1 + a * tau)) / a)
zero("h", "Lyapunov X22 - v == 0", sol[x22] - v)

items = [x for k, vv in R.items() for x in vv]
R["pass"] = all(x["pass"] for x in items)
R["n"] = len(items)
R["lines"] = LINES
out(f"T10.1: {'PASS' if R['pass'] else 'FAIL'} ({sum(x['pass'] for x in items)}/{len(items)})")
save_json(R, "t10_1.json")
