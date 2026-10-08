"""Post-hoc diagnosis of the two route failures in t13_partA_symbolic (not pass criteria).
A1 item 2: -sFr written as -F k (1 - e^{-2x})/x; SymPy's assumptions cannot sign 1 - e^{-2x}. Manifest form:
1 - e^{-2x} = e^{-2x}(e^{2x} - 1) with e^y - 1 = sum_{j>=1} y^j/j! > 0.
A2 item 6: the identity contains sinh; the pre-registered routes do not rewrite sinh into exponentials. Route used here:
.rewrite(sp.exp) then simplify."""
import sympy as sp

from t13_common import Store, save_json

S = Store()
x, F, k = sp.symbols("x F k", positive=True)
E2 = sp.exp(-2 * x)
s = 1 - E2
sp_ = sp.diff(s, x)
r = k / x
S.zero("A1", "2 -sFr + (F k/x) e^{-2x}(e^{2x} - 1) == 0", -s * F * r + (F * k / x) * E2 * (sp.exp(2 * x) - 1))
y = sp.symbols("y", positive=True)
ser = sp.series(sp.exp(y) - 1, y, 0, 10).removeO()
S.check("A1", "2 e^y - 1 series: all coefficients from y^1 positive (so -sFr < 0)", all(ser.coeff(y, j) > 0 for j in range(1, 10)), str(ser))
e = (1 - x * sp_ / s) * (2 / s) - 1 - 2 * E2 * (sp.sinh(2 * x) - 2 * x) / s**2
S.zero("A2", "6 same identity after .rewrite(exp)", e.rewrite(sp.exp))
S.zero("A2", "6 exp form: 2s - 2x s' - s^2 - (1 - 4x e^{-2x} - e^{-4x}) == 0", 2 * s - 2 * x * sp_ - s**2 - (1 - 4 * x * E2 - sp.exp(-4 * x)))
items = [r_ for v in S.R.values() for r_ in v]
S.R["pass"] = all(r_["pass"] for r_ in items)
S.R["attribution"] = "criterion/route: both identities hold; the pre-registered routes cannot sign 1 - e^{-2x} or rewrite sinh"
S.out(f"diag: {'all verified' if S.R['pass'] else 'NOT verified'}")
save_json(S.R, "t13_partA_symbolic_diag.json")
