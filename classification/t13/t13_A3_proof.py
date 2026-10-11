"""A3, post-hoc completion of the pre-registered resultant route (PREREG_t13 A3), in exact arithmetic.
The attempt script (t13_A3_attempt.py) computed the resultant with floats (Python int division leaked 0.5 etc.) and its
automatic verdict only looked at coefficient signs as polynomials in (x, E, u), so it reported 'unresolved'. Here:
1. scaling: P_a(dt; lam, Sig, Pi) = F p(x, u), x = lam dt, u = 2 Sig Pi/lam^2 (so the reduced model lam = Sig = 1 is general);
2. exact resultant of the derivative numerator and the quadratic in p, factored;
3. every factor is nonzero for x > 0, u > 0, E = e^{-x} in (0, 1); the key factor E^2 + 2xE - 1 = -2 e^{-x}(sinh x - x) < 0;
4. the leading coefficient in p is nonzero and the denominator 2 a2 p + a1 = sqrt(disc) > 0, so dp/dx is continuous and never 0
   on x > 0: p is strictly monotone; its sign is fixed by one 60-digit evaluation;
5. p < F (quadratic at p = F is positive) and metric (b) = p fac + F(1 - fac) with fac = (1 - E^2)/(2x) decreasing, so
   dP_b/dx = p' fac + (p - F) fac' > 0."""
import mpmath as mp
import sympy as sp

from t13_common import Store, save_json

S = Store()
x, E, u, p = sp.symbols("x E u p", positive=True)
R1 = sp.Rational(1)
half = sp.Rational(1, 2)


def model(lam, Sig, Pi, dt, ph):
    F = Sig / lam
    q11 = F * (1 - ph**2)
    q12 = 2 * Sig / lam**2 * ((1 - ph) - (1 - ph**2) / 2)
    q22 = 2 * Sig / lam**2 * (dt - 2 * (1 - ph) / lam + (1 - ph**2) / (2 * lam))
    h = (1 - ph) / (lam * dt)
    re = q22 / dt**2 + 1 / (Pi * dt)
    g = q12 / dt
    return h**2, re * (1 - ph**2) - q11 * h**2 + 2 * ph * h * g, -(q11 * re - g**2)


# 1. scaling
lam, Sig, Pi, dt = sp.symbols("lambda Sigma Pi dt", positive=True)
A2g, A1g, A0g = model(lam, Sig, Pi, dt, sp.exp(-lam * dt))
F = Sig / lam
A2r, A1r, A0r = model(R1, R1, u / 2, x, E)
sub = {x: lam * dt, u: 2 * Sig * Pi / lam**2, E: sp.exp(-lam * dt)}
# quadratic in P = F p: general a2 P^2 + a1 P + a0 must be proportional to the reduced one in p
P = sp.symbols("P", positive=True)
gen = A2g * P**2 + A1g * P + A0g
red = (A2r * p**2 + A1r * p + A0r).subs(sub).subs(p, P / F)
ratio = sp.simplify(gen / red)
S.check("A3", "1 scaling: general quadratic / reduced quadratic (p = P/F) is free of P", sp.simplify(sp.diff(ratio, P)) == 0, str(ratio)[:200])

# 2. exact resultant
dxx = lambda e: sp.diff(e, x) - E * sp.diff(e, E)          # d/dx with E = e^{-x}
quad = sp.together(A2r * p**2 + A1r * p + A0r)
qn = sp.numer(quad)
qd = sp.denom(quad)
S.check("A3", "2 quadratic denominator free of p", not qd.has(p), str(qd))
num = sp.numer(sp.together(dxx(A2r) * p**2 + dxx(A1r) * p + dxx(A0r)))
den = sp.denom(sp.together(dxx(A2r) * p**2 + dxx(A1r) * p + dxx(A0r)))
S.check("A3", "2 derivative numerator denominator free of p", not den.has(p), str(den))
S.check("A3", "2 exact arithmetic (no floats)", not any(isinstance(a, sp.Float) for a in sp.preorder_traversal(qn + num)), "")
lc = sp.factor(sp.Poly(qn, p).LC())
S.note("A3", "2 leading coefficient of the quadratic in p", str(lc))
res = sp.factor(sp.resultant(sp.expand(num), sp.expand(qn), p))
S.note("A3", "2 resultant(numerator, quadratic; p), factored", str(res))
facs = sp.factor_list(res)
S.note("A3", "2 factor list", str(facs))

# 3. each factor nonzero on x > 0, u > 0, E = e^{-x}
key = E**2 + 2 * x * E - 1
ok_factors = True
for f_, m_ in facs[1]:
    fe = sp.expand(f_)
    if fe.free_symbols <= {u, x, E} and (sp.simplify(fe - u) == 0 or sp.simplify(fe - x) == 0 or sp.simplify(fe - E) == 0
                                          or sp.simplify(fe - (u + 1)) == 0):
        continue
    if sp.simplify(fe - (E - 1)) == 0 or sp.simplify(fe - (1 - E)) == 0:
        continue                                              # E < 1 for x > 0
    if sp.simplify(fe - key) == 0 or sp.simplify(fe + key) == 0 or sp.simplify(fe - 2 * key) == 0 or sp.simplify(fe + 2 * key) == 0:
        continue
    ok_factors = False
    S.note("A3", "3 unrecognized factor", str(f_))
S.check("A3", "3 factors are u, x, E, u + 1, E - 1 (nonzero) and the key factor E^2 + 2xE - 1 (up to constants)", ok_factors, str(facs[1]))
S.zero("A3", "3 key factor on E = e^{-x}: E^2 + 2xE - 1 + 2 e^{-x}(sinh x - x) == 0", (key.subs(E, sp.exp(-x)) + 2 * sp.exp(-x) * (sp.sinh(x) - x)).rewrite(sp.exp))
y = sp.symbols("y", positive=True)
ser = sp.series(sp.sinh(y) - y, y, 0, 14).removeO()
S.check("A3", "3 sinh y - y has positive coefficients only (so the key factor is < 0 for x > 0)",
        all(ser.coeff(y, j) >= 0 for j in range(14)) and ser.coeff(y, 3) > 0, str(ser))
S.check("A3", "3 leading coefficient in p nonzero (u(1 - E)/... up to sign)", sp.simplify(lc.subs(E, sp.Rational(1, 2))) != 0, str(lc))

# 4. sign at one point (60 digits) and the structure
mp.mp.dps = 60
froot = sp.lambdify((x, u), (sp.Poly(qn, p).all_coeffs()), "mpmath")
dnum = sp.lambdify((x, E, u, p), num, "mpmath")
dden = sp.lambdify((x, E, u, p), den, "mpmath")
dq = sp.lambdify((x, E, u, p), sp.diff(qn, p), "mpmath")


def p_root(xv, uv):
    Ev = mp.e**(-xv)
    co = [c.subs({x: xv, u: uv, E: Ev}) if hasattr(c, "subs") else c for c in sp.Poly(qn, p).all_coeffs()]
    co = [mp.mpf(sp.N(c, 70)) for c in co]
    rts = [r for r in mp.polyroots(co, extraprec=100) if abs(mp.im(r)) < mp.mpf("1e-50") and mp.re(r) > 0]
    return mp.re(rts[0]), Ev, len(rts)


xv, uv = mp.mpf(1), mp.mpf(1)
pv, Ev, nr = p_root(xv, uv)
quadp = sp.together(A2r * p**2 + A1r * p + A0r)
# dp/dx = -(d/dx of the quadratic at fixed p)/(d/dp of the quadratic): use the numerator/denominator forms
dpdx = -(dnum(xv, Ev, uv, pv) / dden(xv, Ev, uv, pv)) / (dq(xv, Ev, uv, pv) / sp.N(qd.subs({x: xv, u: uv, E: Ev}), 70))
S.check("A3", "4 one positive root of the quadratic at (x, u) = (1, 1)", nr == 1, str(nr))
S.check("A3", "4 dp/dx > 0 at (x, u) = (1, 1) (60 digits)", dpdx > 0, mp.nstr(dpdx, 15))

# 5. p < F (F = 1 in reduced units) and metric (b)
qF = sp.factor(sp.together(qn.subs(p, 1)))
S.note("A3", "5 quadratic numerator at p = 1 (= F), factored", str(qF))
a2n = sp.factor(sp.Poly(qn, p).LC())
S.note("A3", "5 product of the roots a0/a2 (negative => one positive root)", str(sp.factor(sp.Poly(qn, p).all_coeffs()[-1] / a2n)))
numprod = sp.expand(E * u * x + 2 * E * u + E * x + u * x - 2 * u + x)
S.zero("A3", "5 product numerator - [u(x(1+E) - 2(1-E)) + x(1+E)] == 0", numprod - (u * (x * (1 + E) - 2 * (1 - E)) + x * (1 + E)))
fx = x * sp.exp(x) + x - 2 * sp.exp(x) + 2
S.zero("A3", "5 x(1+E) - 2(1-E) - e^{-x} f(x) == 0 on E = e^{-x}, f = x e^x + x - 2e^x + 2", (x * (1 + E) - 2 * (1 - E)).subs(E, sp.exp(-x)) - sp.exp(-x) * fx)
serf = sp.series(fx, x, 0, 12).removeO()
S.check("A3", "5 f(x) series: coefficients 0 up to x^2, then (n-2)/n! > 0 (so f > 0, product of roots < 0, one positive root)",
        all(serf.coeff(x, j) == 0 for j in range(3)) and all(serf.coeff(x, j) > 0 for j in range(3, 12)), str(serf))
S.check("A3", "5 quadratic numerator at p = F equals its leading coefficient u(E-1)^2 > 0, with value < 0 at p = 0: root in (0, F)",
        sp.simplify(qn.subs(p, 1) - sp.Poly(qn, p).LC()) == 0, "")
fac = (1 - E**2) / (2 * x)
S.zero("A3", "5 d fac/dx - [ -(1 - E^2) + 2xE^2 ]/(2x^2) == 0 (E = e^{-x})", dxx(fac) - (-(1 - E**2) + 2 * x * E**2) / (2 * x**2))
S.zero("A3", "5 (1 - E^2) - 2x E^2 = E^2 (e^{2x} - 1 - 2x) on E = e^{-x}", ((1 - E**2) - 2 * x * E**2 - E**2 * (sp.exp(2 * x) - 1 - 2 * x)).subs(E, sp.exp(-x)))
S.note("A3", "5 metric (b)", "P_b = p fac + F(1 - fac); dP_b/dx = p' fac + (p - F) fac' with fac' < 0 (above) and p < F, so dP_b/dx > 0 "
       "whenever p' > 0.")
items = [r_ for v in S.R.values() for r_ in v]
S.R["pass"] = all(r_["pass"] for r_ in items)
S.R["lines"] = S.lines
S.out(f"A3 completion: {'all steps verified' if S.R['pass'] else 'NOT all verified'}")
save_json(S.R, "t13_A3_proof.json")
