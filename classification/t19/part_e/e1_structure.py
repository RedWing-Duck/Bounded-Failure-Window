"""Part E (exploratory, not pass/fail): structure of the D1 metrics' derivatives along dt as exponential polynomials.
With x = dt, u = e^{-G x}, w = e^{-2 lam x}: P+ = (u^2 F (1 - w) + (1 - u)^2/(Pi x)) / (1 - u^2 w).
The derivative's numerator (over a positive denominator) is a sum of terms p_ij(x) u^i w^j with polynomial p_ij; the
Polya-Szego bound gives #zeros <= sum (deg p_ij + 1) - 1 over the distinct exponents i G + 2 j lam (generic G, lam)."""
import json
import sympy as sp

x, lam, Sig, Pi, G = sp.symbols("x lambda Sigma Pi G", positive=True)
u, w = sp.symbols("u w", positive=True)
F = Sig / lam
post = (u**2 * F * (1 - w) + (1 - u)**2 / (Pi * x)) / (1 - u**2 * w)
prior = w * post + F * (1 - w)
avg = F - (F - post) * (1 - w) / (2 * lam * x)
du, dw = -G * u, -2 * lam * w            # d/dx of u and w


def ddx(e):
    return sp.diff(e, x) + sp.diff(e, u) * du + sp.diff(e, w) * dw


out = {}
for name, e in (("post", post), ("prior", prior), ("avg", avg)):
    d = sp.together(ddx(e))
    num, den = sp.fraction(d)
    num = sp.expand(num)
    P = sp.Poly(num, u, w)
    terms = {}
    for (i, j), c in zip(P.monoms(), P.coeffs()):
        deg = sp.Poly(sp.expand(c * x**4), x).degree() if c.has(x) else 0
        terms[f"u^{i} w^{j}"] = {"coeff": str(sp.factor(c)), "deg_x_after_x^4": deg}
    bound = sum(sp.Poly(sp.expand(c * x**6), x).length() for c in P.coeffs()) - 1
    out[name] = {"denominator": str(sp.factor(den)), "n_exponential_terms": len(P.monoms()), "terms": terms,
                 "polya_bound_monomial_count_minus_1": bound}
    print(name, "terms:", len(P.monoms()), "Polya-type bound (monomials x^k u^i w^j minus 1):", bound)
json.dump(out, open("e1_structure.json", "w"), indent=1)
