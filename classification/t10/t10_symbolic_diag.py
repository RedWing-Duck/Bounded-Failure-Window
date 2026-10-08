"""T10.1 diagnosis (post hoc, not a pass criterion): the two items that did not reduce under the fixed route."""
import sympy as sp

from t10_common import save_json

lam, Sig, Pi, G, R2, w = sp.symbols("lambda Sigma Pi G R2 w", positive=True)
l1, S1 = sp.symbols("lambda1 Sigma1", positive=True)
out = {}
# (c) G(Pi(G)) - G: the radicand is a perfect square
GM = -l1 + sp.sqrt(l1**2 + 2 * S1 * Pi)
e = GM.subs(Pi, (G**2 + 2 * l1 * G) / (2 * S1)) - G
rad = [p for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)][0]
e2 = e.subs(rad, sp.sqrt(sp.factor(rad.base)))
out["c"] = {"radicand": str(rad.base), "factored": str(sp.factor(rad.base)), "after_factoring_radicand": str(sp.simplify(e2)),
            "reduces": sp.simplify(e2) == 0}
# (g) forced ray: needs R^2 < F (here R^2 = F/(1+w), w > 0)
F = Sig / lam
s = sp.sqrt(lam**2 + 2 * Sig * Pi)
piR = 2 * lam * (F - R2) / R2**2
e = ((-lam + s) / Pi).subs(Pi, piR) - R2
rad = [p for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)][0]
eg = sp.simplify(e.subs(R2, F / (1 + w)))
r2 = [p for p in eg.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)][0]
eg2 = sp.simplify(eg.subs(r2, sp.sqrt(sp.factor(r2.base))))
out["g"] = {"radicand": str(sp.factor(rad.base)), "with_R2_eq_F_over_1_plus_w": str(eg),
            "inner_radicand_factored": str(sp.factor(r2.base)), "after_factoring": str(eg2),
            "reduces_under_R2_lt_F": eg2 == 0,
            "note": "sqrt((lam R2 - 2 Sig)^2/R2^4) = (2 Sig - lam R2)/R2^2 needs lam R2 < 2 Sig, i.e. R2 < 2F"}
for k, v in out.items():
    print(k, v)
save_json(out, "t10_1_diag.json")
