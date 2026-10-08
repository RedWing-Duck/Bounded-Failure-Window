"""T9.1: symbolic checks of Stage 2 (exact reduction to 0, no numeric fallback)."""
import sympy as sp

from t9_common import save_json

lam, Sig, Pi, G, tau, R2, P, u = sp.symbols("lambda Sigma Pi G tau R2 P u", positive=True)
w = sp.symbols("omega", real=True)
uu = sp.symbols("t", real=True)
a = lam + G
F = Sig / lam
sig2 = (Sig + G**2 / (2 * Pi * (1 + a * tau))) / a
Vw = (Sig + G**2 / (2 * Pi)) / a
HG = Sig / a
s = sp.sqrt(lam**2 + 2 * Sig * Pi)
Gs = -lam + s
h = 1 / tau - lam
Rv = 2 * Sig + 1 / (Pi * tau**2)
b = 4 * Sig * tau + 2 * lam / Pi
D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
Popt = 4 * Sig / (Pi * (b + sp.sqrt(D)))
quad = lambda PP, tt: (1 - lam * tt)**2 * PP**2 + (4 * Sig * tt + 2 * lam / Pi) * PP - 2 * Sig / Pi
tauR = (G**2 / (2 * Pi * (a * R2 - Sig)) - 1) / a
tauF = (G / (2 * F * Pi) - 1) / a
Delta = 16 * Sig**2 - 16 * lam * Sig * R2 + 8 * lam**2 * (Sig - lam * R2) / Pi
taus = (2 * lam * R2 - 4 * Sig + sp.sqrt(Delta)) / (2 * lam**2 * R2)

R, LINES = {}, []


def out(t):
    print(t)
    LINES.append(t)


def zero(key, desc, e):
    """Fixed route: simplify; simplify(together(expand)); single-sqrt remainder. No numeric fallback."""
    route, ok = None, False
    if sp.simplify(e) == 0:
        route, ok = "simplify", True
    elif sp.simplify(sp.together(sp.expand(e))) == 0:
        route, ok = "simplify(together(expand))", True
    else:
        roots = [p for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)]
        if len(roots) == 1:
            r = roots[0]
            X = r.base
            num = sp.numer(sp.together(e.subs(r, u)))
            rem = sp.rem(sp.expand(num), u**2 - X, u)
            if sp.simplify(rem) == 0:
                route, ok = "sqrt-remainder", True
    rec = {"desc": desc, "route": route or "none", "pass": ok}
    if not ok:
        rec["sympy_verbatim"] = str(sp.simplify(e))
    R.setdefault(key, []).append(rec)
    out(f"  [{'PASS' if ok else 'FAIL'}] ({rec['route']}) {desc}" + ("" if ok else f"  SymPy: {rec['sympy_verbatim']}"))
    return ok


# (a) Lemma 2.1 by the 2x2 Lyapunov equation
out("(a) Lemma 2.1, augmented-state Lyapunov route")
x11, x12, x22 = sp.symbols("x11 x12 x22")
A = sp.Matrix([[-a, G], [0, -1 / tau]])
X = sp.Matrix([[x11, x12], [x12, x22]])
Q = sp.diag(2 * Sig, 1 / (Pi * tau**2))
L = A * X + X * A.T + Q
sol = sp.solve([L[0, 0], L[0, 1], L[1, 1]], [x11, x12, x22], dict=True)[0]
out(f"  Var x = {sp.factor(sol[x11])}")
zero("a", "Var x (Lyapunov) - Lemma 2.1 == 0", sol[x11] - sig2)
zero("a", "Var eta (Lyapunov) - 1/(2 Pi tau) == 0", sol[x22] - 1 / (2 * Pi * tau))
Ceta = sp.exp(-sp.Abs(uu) / tau) / (2 * Pi * tau)
I0 = 2 * sp.integrate(sp.exp(-uu / tau) / (2 * Pi * tau), (uu, 0, sp.oo))
zero("a", "integral of C_eta over R - 1/Pi == 0 (S_eta(0) = 1/Pi)", I0 - 1 / Pi)
Sw = 2 * sp.integrate(sp.exp(-uu / tau) * sp.cos(w * uu) / (2 * Pi * tau), (uu, 0, sp.oo), conds="none")
zero("a", "Fourier transform of C_eta - (1/Pi)/(1 + tau^2 omega^2) == 0", Sw - (1 / Pi) / (1 + tau**2 * w**2))

# (b) excess identity
out("(b) excess identity")
zero("b", "sigma2 - F - G(lam G/(2 Pi(1+a tau)) - Sig)/(lam a) == 0",
     sig2 - F - G * (lam * G / (2 * Pi * (1 + a * tau)) - Sig) / (lam * a))
zero("b", "lam G/(2 Pi(1+a tau)) - Sig - (lam/2)(G/Pi - 2F(1+a tau))/(1+a tau) == 0",
     lam * G / (2 * Pi * (1 + a * tau)) - Sig - (lam / 2) * (G / Pi - 2 * F * (1 + a * tau)) / (1 + a * tau))
zero("b", "d sigma2/d tau + G^2/(2 Pi (1+a tau)^2) == 0", sp.diff(sig2, tau) + G**2 / (2 * Pi * (1 + a * tau)**2))

# (c) tau_R, tau_F
out("(c) tau_R and tau_F")
zero("c", "sigma2(tau_R) - R^2 == 0", sig2.subs(tau, tauR) - R2)
zero("c", "sigma2(tau_F) - F == 0", sig2.subs(tau, tauF) - F)
zero("c", "tau_R(R^2 = F) - tau_F == 0", tauR.subs(R2, F) - tauF)
zero("c", "a tau_R 2 Pi (a R^2 - Sig) - 2 Pi a (V_w - R^2) == 0",
     a * tauR * 2 * Pi * (a * R2 - Sig) - 2 * Pi * a * (Vw - R2))

# (d) Riccati expansion
out("(d) Riccati expansion")
Ric = -2 * lam * P + 2 * Sig - (h * P + 2 * Sig)**2 / Rv
ok_d = zero("d", "-tau^2 R_v Ric - quadratic == 0", -tau**2 * Rv * Ric - quad(P, tau))
zero("d", "tau^2 (S^2 - Q R_v) + 2 Sig/Pi == 0", tau**2 * ((2 * Sig)**2 - 2 * Sig * Rv) + 2 * Sig / Pi)
zero("d", "tau^2 (2 h S + 2 lam R_v) - b == 0", tau**2 * (2 * h * 2 * Sig + 2 * lam * Rv) - b)
lit = sp.simplify(tau**2 * Ric - quad(P, tau))
R["d_literal"] = {"desc": "literal reading 'tau^2 x Riccati' minus quadratic (informational)", "sympy": str(sp.factor(lit))}
out(f"  info: tau^2*Ric - quadratic = {sp.factor(lit)}  (nonzero: the factor -R_v is needed)")

# (e) rationalized root
out("(e) rationalized root")
zero("e", "quadratic at P = 4 Sig/(Pi(b + sqrt D)) == 0", quad(Popt, tau))
zero("e", "at lam tau = 1: P - (2 Sig/Pi)/b == 0", (Popt - (2 * Sig / Pi) / b).subs(tau, 1 / lam))

# (f) dD/dtau
out("(f) dD/dtau")
zero("f", "dD/dtau - (32 Sig^2 tau + 16 Sig lam^2 tau/Pi) == 0", sp.diff(D, tau) - (32 * Sig**2 * tau + 16 * Sig * lam**2 * tau / Pi))
zero("f", "dD/dtau - (8 Sig b - 16 Sig lam (1 - lam tau)/Pi) == 0", sp.diff(D, tau) - (8 * Sig * b - 16 * Sig * lam * (1 - lam * tau) / Pi))

# (g) limits
out("(g) limits")
for desc, got, want in [("P(0+) = G*/Pi", sp.limit(Popt, tau, 0, "+"), Gs / Pi),
                        ("tau P -> 1/(Pi(1 + sqrt(1 + lam^2/(2 Sig Pi))))", sp.limit(tau * Popt, tau, sp.oo),
                         1 / (Pi * (1 + sp.sqrt(1 + lam**2 / (2 * Sig * Pi))))),
                        ("relay tau -> 0+: V_w", sp.limit(sig2, tau, 0, "+"), Vw),
                        ("relay tau -> oo: H_G", sp.limit(sig2, tau, sp.oo), HG)]:
    out(f"  sympy limit: {got}")
    zero("g", desc, got - want)

# (h) tau*_R
out("(h) tau*_R")
zero("h", "quadratic at P = R^2, tau = tau*_R == 0", quad(R2, taus))
qt = sp.Poly(sp.expand(quad(R2, tau)), tau)
c2, c1, c0 = qt.all_coeffs()
zero("h", "leading coefficient - lam^2 R^4 == 0", c2 - lam**2 * R2**2)
zero("h", "discriminant - R^4 Delta == 0", c1**2 - 4 * c2 * c0 - R2**2 * Delta)
zero("h", "constant - (R^2 - G*/Pi)(R^2 + (lam + s)/Pi) == 0", c0 - (R2 - Gs / Pi) * (R2 + (lam + s) / Pi))

# (i) white-noise limit = Paper 1
out("(i) Paper 1 white-noise formula")
zero("i", "lim_{tau->0} sigma2 - (Sig + G^2/(2 Pi))/(lam + G) == 0",
     sp.limit(sig2, tau, 0, "+") - (Sig + G**2 / (2 * Pi)) / (lam + G))

items = [r for k, v in R.items() if isinstance(v, list) for r in v]
R["pass"] = all(r["pass"] for r in items)
R["n_items"] = len(items)
R["routes"] = {r["route"]: sum(1 for x in items if x["route"] == r["route"]) for r in items}
R["lines"] = LINES
out(f"T9.1: {'PASS' if R['pass'] else 'FAIL'} ({sum(r['pass'] for r in items)}/{len(items)}); routes {R['routes']}")
save_json(R, "t9_1.json")
