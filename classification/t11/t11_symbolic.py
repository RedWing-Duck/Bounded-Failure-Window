"""T11.1: symbolic checks for Stage 4 (exact reduction to 0; radicands may be factored)."""
import sympy as sp

from t11_common import save_json

tau, w, b, K, lam, Sig, Pi, t1, t2, d, u, wq = sp.symbols("tau omega beta K lambda Sigma Pi tau1 tau2 d u w", positive=True)
v = sp.symbols("v", positive=True)
R, LINES = {}, []


def out(x):
    print(x)
    LINES.append(x)


def _sqrt_factor(e):
    reps = {p: sp.sqrt(sp.factor(p.base)) for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)}
    return e.xreplace(reps)


def zero(key, desc, e):
    route = None
    if sp.simplify(e) == 0:
        route = "simplify"
    elif sp.simplify(sp.together(sp.expand(e))) == 0:
        route = "simplify(together(expand))"
    elif sp.simplify(_sqrt_factor(e)) == 0 or sp.simplify(_sqrt_factor(sp.simplify(e))) == 0:
        route = "factor radicands"
    else:
        roots = [p for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)]
        if len(roots) == 1:
            r = roots[0]
            num = sp.numer(sp.together(e.subs(r, u)))
            if sp.simplify(sp.rem(sp.expand(num), u**2 - r.base, u)) == 0:
                route = "sqrt-remainder"
    ok = route is not None
    rec = {"desc": desc, "route": route or "none", "pass": ok}
    if not ok:
        rec["sympy_verbatim"] = str(sp.simplify(e))
    R.setdefault(key, []).append(rec)
    out(f"  [{'PASS' if ok else 'FAIL'}] ({rec['route']}) {desc}" + ("" if ok else f"  SymPy: {rec['sympy_verbatim']}"))


def signed(key, desc, e, want):
    s = sp.simplify(e)
    q = s.is_positive if want > 0 else s.is_negative
    ok = bool(q)
    R.setdefault(key, []).append({"desc": desc, "route": "assumptions", "pass": ok, "expr": str(s)})
    out(f"  [{'PASS' if ok else 'FAIL'}] (assumptions) {desc}: {s}")


S = K * tau**b / (1 + tau**2 * w**2)
out("(a) ordering derivative")
zero("a", "d/dtau log S - [beta/tau - 2 tau w^2/(1 + tau^2 w^2)] == 0", sp.diff(sp.log(S), tau) - (b / tau - 2 * tau * w**2 / (1 + tau**2 * w**2)))
zero("a", "2/tau - 2 tau w^2/(1+tau^2 w^2) - 2/(tau (1 + tau^2 w^2)) == 0",
     2 / tau - 2 * tau * w**2 / (1 + tau**2 * w**2) - 2 / (tau * (1 + tau**2 * w**2)))
signed("a", "2/(tau (1 + tau^2 w^2)) > 0 (second term < 2/tau)", 2 / (tau * (1 + tau**2 * w**2)), +1)

out("(b) matched zero-frequency garbling")
S0 = lambda tt: (1 / Pi) / (1 + tt**2 * w**2)
Hx = lambda s_: sp.sqrt((t2**2 - t1**2) / Pi) * s_ / ((1 + t1 * s_) * (1 + t2 * s_))
I = sp.I
absH2 = sp.expand(Hx(I * w) * Hx(-I * w))
zero("b", "S_tau1 - S_tau2 - |H_xi(i w)|^2 == 0", S0(t1) - S0(t2) - absH2)
zero("b", "S_tau1 - S_tau2 - (tau2^2 - tau1^2) w^2/(Pi (1+tau1^2 w^2)(1+tau2^2 w^2)) == 0",
     S0(t1) - S0(t2) - (t2**2 - t1**2) * w**2 / (Pi * (1 + t1**2 * w**2) * (1 + t2**2 * w**2)))

out("(c) bound P <= sqrt(C/A)")
A = (1 - lam * tau)**2 / tau
vv = K / 2 * tau**(b - 1)
B = 4 * (Sig + lam * vv)
C = 4 * Sig * vv
zero("c", "2C/sqrt(4AC) - sqrt(C/A) == 0", 2 * C / sp.sqrt(4 * A * C) - sp.sqrt(C / A))
for lab, tt in (("lam tau < 1", 1 / (lam * (1 + wq))), ("lam tau > 1", (1 + wq) / lam)):
    zero("c", f"sqrt(C/A) - sqrt(2 Sig K) tau^(b/2)/|1 - lam tau| == 0 ({lab})",
         (sp.sqrt(C / A) - sp.sqrt(2 * Sig * K) * tau**(b / 2) / sp.Abs(1 - lam * tau)).subs(tau, tt))
Ab, Bb, Cb = sp.symbols("A_s B_s C_s", positive=True)
zero("c", "2C/(B + sqrt(B^2+4AC)) * (B + sqrt(B^2+4AC)) - 2C == 0", 2 * Cb / (Bb + sp.sqrt(Bb**2 + 4 * Ab * Cb)) * (Bb + sp.sqrt(Bb**2 + 4 * Ab * Cb)) - 2 * Cb)
# bug fix (documented): the pre-registered method proves signs via an identity with a manifestly signed right side
rhs = Bb + Bb**2 / (sp.sqrt(Bb**2 + 4 * Ab * Cb) + sp.sqrt(4 * Ab * Cb))
zero("c", "B + sqrt(B^2+4AC) - sqrt(4AC) - [B + B^2/(sqrt(B^2+4AC) + sqrt(4AC))] == 0",
     Bb + sp.sqrt(Bb**2 + 4 * Ab * Cb) - sp.sqrt(4 * Ab * Cb) - rhs)
signed("c", "B + B^2/(sqrt(B^2+4AC) + sqrt(4AC)) > 0 (so P <= sqrt(C/A))", rhs, +1)

out("(d) duality")
x = 1 / (lam**2 * tau)
Kp = K * lam**(2 - 2 * b)
zero("d", "A(tau) - A(1/(lam^2 tau)) == 0", A - A.subs(tau, x))
zero("d", "v_{b,K}(tau) - v_{2-b,K lam^(2-2b)}(1/(lam^2 tau)) == 0", vv - (Kp / 2 * x**((2 - b) - 1)))
Pf = lambda AA, VV: 2 * (4 * Sig * VV) / (4 * (Sig + lam * VV) + sp.sqrt(16 * (Sig + lam * VV)**2 + 16 * AA * Sig * VV))
zero("d", "P_{b,K}(tau) - P_{2-b,K'}(1/(lam^2 tau)) == 0", Pf(A, vv) - Pf(A.subs(tau, x), Kp / 2 * x**((2 - b) - 1)))

out("(e) delay")
F = Sig / lam
s2 = 2 * Sig / (lam + sp.sqrt(lam**2 + 2 * Sig * Pi))
zero("e", "Var(s(t) - e^{-lam d} s(t-d)) - F(1 - e^{-2 lam d}) == 0",
     F - 2 * sp.exp(-lam * d) * F * sp.exp(-lam * d) + sp.exp(-2 * lam * d) * F - F * (1 - sp.exp(-2 * lam * d)))
zero("e", "e^{-2 lam d} s*^2 + F(1 - e^{-2 lam d}) - [F - e^{-2 lam d}(F - s*^2)] == 0",
     sp.exp(-2 * lam * d) * s2 + F * (1 - sp.exp(-2 * lam * d)) - (F - sp.exp(-2 * lam * d) * (F - s2)))

out("(f) signal-sweep signs")
sq = sp.sqrt(lam**2 + 2 * Sig * Pi)
zero("f", "d s*^2/dSig - 2(lam sq + lam^2 + Sig Pi)/(sq (lam + sq)^2) == 0",
     sp.diff(s2, Sig) - 2 * (lam * sq + lam**2 + Sig * Pi) / (sq * (lam + sq)**2))
signed("f", "2(lam sq + lam^2 + Sig Pi)/(sq (lam + sq)^2) > 0 (increasing in Sigma)", 2 * (lam * sq + lam**2 + Sig * Pi) / (sq * (lam + sq)**2), +1)
zero("f", "d s*^2/dlam + 2 Sig (1 + lam/sq)/(lam + sq)^2 == 0", sp.diff(s2, lam) + 2 * Sig * (1 + lam / sq) / (lam + sq)**2)
signed("f", "-2 Sig (1 + lam/sq)/(lam + sq)^2 < 0 (decreasing in lambda at fixed Sigma)", -2 * Sig * (1 + lam / sq) / (lam + sq)**2, -1)
Fs = sp.symbols("F", positive=True)
gF = 2 * Fs / (1 + sp.sqrt(1 + 2 * Fs * Pi / lam))
zero("f", "2F/(1 + sqrt(1 + 2 F Pi/lam)) - s*^2 at Sigma = F lam == 0", gF - s2.subs(Sig, Fs * lam))
rt = sp.sqrt(1 + 2 * Fs * Pi / lam)
zero("f", "d/dlam [2F/(1+rt)] - 2 F^2 Pi/(lam^2 rt (1 + rt)^2) == 0", sp.diff(gF, lam) - 2 * Fs**2 * Pi / (lam**2 * rt * (1 + rt)**2))
signed("f", "2 F^2 Pi/(lam^2 rt (1+rt)^2) > 0 (increasing in lambda at fixed F)", 2 * Fs**2 * Pi / (lam**2 * rt * (1 + rt)**2), +1)

items = [x_ for k, vv_ in R.items() for x_ in vv_]
R["pass"] = all(x_["pass"] for x_ in items)
R["n"] = len(items)
R["lines"] = LINES
out(f"T11.1: {'PASS' if R['pass'] else 'FAIL'} ({sum(x_['pass'] for x_ in items)}/{len(items)})")
save_json(R, "t11_1.json")
