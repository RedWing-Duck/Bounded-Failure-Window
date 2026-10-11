"""Referee point 5 (post hoc): endpoint limits of the M-I posterior p(x, u) (reduced units, F = 1) for Theorem 35, by series.
x -> 0: E = e^{-x} expanded; x -> oo: E = e^{-x} set to 0 beyond all orders, t = 1/x. Positive root of the cleared quadratic."""
import sympy as sp

from t13_common import Store, save_json

S = Store()
x, E, u, p, t = sp.symbols("x E u p t", positive=True)
R1 = sp.Integer(1)


def coeffs(xx, EE):
    lam, Sig, Pi = R1, R1, u / 2
    F = R1
    q11 = F * (1 - EE**2)
    q12 = 2 * ((1 - EE) - (1 - EE**2) / 2)
    q22 = 2 * (xx - 2 * (1 - EE) + (1 - EE**2) / 2)
    h = (1 - EE) / xx
    re = q22 / xx**2 + 1 / (Pi * xx)
    g = q12 / xx
    return h**2, re * (1 - EE**2) - q11 * h**2 + 2 * EE * h * g, -(q11 * re - g**2)


a2, a1, a0 = coeffs(x, E)
S.note("A3lim", "quadratic coefficients (reduced units lam = Sig = 1, Pi = u/2, E = e^{-x})",
       f"a2 = {sp.factor(a2)}; a1 = {sp.factor(sp.together(a1))}; a0 = {sp.factor(sp.together(a0))}")
# x -> oo
b2, b1, b0 = (sp.simplify(c.subs(E, 0).subs(x, 1 / t)) for c in (a2, a1, a0))
root = (-b1 + sp.sqrt(b1**2 - 4 * b2 * b0)) / (2 * b2)
lim_inf = sp.limit(sp.simplify(root), t, 0, "+")
S.zero("A3lim", "x -> oo: p -> 1 (= F)", lim_inf - 1)
# x -> 0
ser = [sp.series(c.subs(E, sp.exp(-x)), x, 0, 3).removeO() for c in (a2, a1, a0)]
c2, c1, c0 = (sp.simplify(s_.subs(x, 0)) for s_ in ser)
S.note("A3lim", "x -> 0 leading coefficients", f"{c2}, {c1}, {c0}")
lead = [sp.limit(sp.simplify(c.subs(E, sp.exp(-x))), x, 0, "+") for c in (a2, a1, a0)]
S.note("A3lim", "x -> 0 limits of a2, a1, a0", str(lead))
r0 = (-lead[1] + sp.sqrt(lead[1]**2 - 4 * lead[0] * lead[2])) / (2 * lead[0]) if lead[0] != 0 else -lead[2] / lead[1]
S.zero("A3lim", "x -> 0: p -> 2/(1 + sqrt(1 + u)) (= sigma*^2/F)", sp.simplify(r0 - 2 / (1 + sp.sqrt(1 + u))))
items = [r_ for v in S.R.values() for r_ in v]
S.R["pass"] = all(r_["pass"] for r_ in items)
S.out(f"A3 limits: {'verified' if S.R['pass'] else 'NOT verified'}")
save_json(S.R, "t13_A3_limits.json")
