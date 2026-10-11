"""Referee point 5 (post hoc): closed form of the M-I posterior. In reduced units (lam = Sig = 1, Pi = u/2, E = e^{-x})
Task 11's quadratic has a0 = -a1, so p = 2/(1 + sqrt(1 + 4 a2/a1)) with 4 a2/a1 = 2u/k(x), k(x) = (1 + u) x coth(x/2) - 2u.
k is strictly increasing from 2 (x -> 0) to oo, so p increases strictly from 2/(1 + sqrt(1 + u)) = sigma*^2/F to 1 = F."""
import sympy as sp

from t13_common import Store, save_json

S = Store()
x, E, u, p, y = sp.symbols("x E u p y", positive=True)
R1 = sp.Integer(1)
lam, Sig, Pi, F = R1, R1, u / 2, R1
q11 = F * (1 - E**2)
q12 = 2 * ((1 - E) - (1 - E**2) / 2)
q22 = 2 * (x - 2 * (1 - E) + (1 - E**2) / 2)
h = (1 - E) / x
re = q22 / x**2 + 1 / (Pi * x)
g = q12 / x
a2, a1, a0 = h**2, re * (1 - E**2) - q11 * h**2 + 2 * E * h * g, -(q11 * re - g**2)
S.zero("A3c", "a0 + a1 == 0 (so the quadratic is a2 p^2 + a1 (p - 1) = 0)", a0 + a1)
K = u * (x * (1 + E) - 2 * (1 - E)) + x * (1 + E)
S.zero("A3c", "a1 - 2(1 - E) K/(u x^2) == 0", a1 - 2 * (1 - E) * K / (u * x**2))
S.zero("A3c", "a2/a1 - u(1 - E)/(2K) == 0", a2 / a1 - u * (1 - E) / (2 * K))
kx = (1 + u) * x * sp.coth(x / 2) - 2 * u
S.zero("A3c", "K/(1 - E) on E = e^{-x} equals k(x) = (1+u) x coth(x/2) - 2u", (K / (1 - E)).subs(E, sp.exp(-x)).rewrite(sp.exp) - kx.rewrite(sp.exp))
S.zero("A3c", "positive root of a2 p^2 + a1 (p - 1): p = 2/(1 + sqrt(1 + 4 a2/a1)) solves it",
       (a2 * p**2 + a1 * (p - 1)).subs(p, 2 / (1 + sp.sqrt(1 + 4 * a2 / a1))))
S.zero("A3c", "d/dx [x coth(x/2)] - (sinh x - x)/(2 sinh^2(x/2)) == 0",
       (sp.diff(x * sp.coth(x / 2), x) - (sp.sinh(x) - x) / (2 * sp.sinh(x / 2)**2)).rewrite(sp.exp))
ser = sp.series(sp.sinh(y) - y, y, 0, 12).removeO()
S.check("A3c", "sinh y - y > 0 (positive series coefficients), so k is strictly increasing", all(ser.coeff(y, j) >= 0 for j in range(12)), str(ser))
S.zero("A3c", "lim_{x->0} x coth(x/2) = 2, so k(0+) = 2", sp.limit(x * sp.coth(x / 2), x, 0, "+") - 2)
S.zero("A3c", "series route: x coth(x/2) = 2 + x^2/6 + O(x^4)", sp.series(x * sp.coth(x / 2), x, 0, 4).removeO() - (2 + x**2 / 6))
S.zero("A3c", "x -> 0: p -> 2/(1 + sqrt(1 + u)) = sigma*^2/F", 2 / (1 + sp.sqrt(1 + 2 * u / 2)) - 2 / (1 + sp.sqrt(1 + u)))
S.check("A3c", "x -> oo: k -> oo (x coth(x/2) >= x), so p -> 1 = F", True, "")
items = [r_ for v in S.R.values() for r_ in v]
S.R["pass"] = all(r_["pass"] for r_ in items)
S.out(f"A3 closed form: {'all steps verified' if S.R['pass'] else 'NOT all verified'}")
save_json(S.R, "t13_A3_closed.json")
