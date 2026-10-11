"""A3 symbolic attempt (PREREG_t13): M-I optimal error monotone in dt. Scalar reduction: p is the positive root of
a2 p^2 + a1 p + a0 (Task 11 closed form). With E = e^{-x} (x = lam dt), u = 2 Sig Pi/lam^2 and p scaled by F, the
implicit derivative dp/dx = -(a2' p^2 + a1' p + a0')/(2 a2 p + a1) (' = d/dx with dE/dx = -E). Attempt: eliminate p by
the resultant of the numerator and the quadratic, factor, and look for a manifestly signed form. 1,800 s per step."""
import signal
import time

import sympy as sp

from t13_common import Store, save_json

S = Store()


class TO(Exception):
    pass


def alarm(*_):
    raise TO()


def timed(f, tmax=1800):
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(tmax)
    t0 = time.time()
    try:
        return f(), time.time() - t0
    except TO:
        return None, time.time() - t0
    finally:
        signal.alarm(0)


x, E, u, p = sp.symbols("x E u p", positive=True)       # dimensionless: lam = 1, F = 1 (Sig = 1), Pi = u/2
lam, Sig, Pi = 1, 1, u / 2
ph = E
F = sp.Integer(1)
q11 = F * (1 - ph**2)
q12 = 2 * Sig / lam**2 * ((1 - ph) - (1 - ph**2) / 2)
q22 = 2 * Sig / lam**2 * (x - 2 * (1 - ph) + (1 - ph**2) / 2)
h = (1 - ph) / x
re = q22 / x**2 + 1 / (Pi * x)
g = q12 / x
a2, a1, a0 = h**2, re * (1 - ph**2) - q11 * h**2 + 2 * ph * h * g, -(q11 * re - g**2)
quad = sp.together(a2 * p**2 + a1 * p + a0)
qn = sp.numer(quad)
dx = lambda e: sp.diff(e, x) + sp.diff(e, E) * (-E)          # total x-derivative with E = e^{-x}
numer = sp.numer(sp.together(dx(a2) * p**2 + dx(a1) * p + dx(a0)))
den = sp.numer(sp.together(2 * a2 * p + a1))
S.note("A3", "sizes", f"quadratic numerator ops {sp.count_ops(qn)}, derivative numerator ops {sp.count_ops(numer)}")
res, sec = timed(lambda: sp.factor(sp.resultant(sp.expand(numer), sp.expand(qn), p)))
S.note("A3", "resultant(numerator, quadratic) in p", f"{'done' if res is not None else 'timeout'} in {sec:.0f} s"
       + (f"; factors: {len(sp.factor_list(res)[1])}, ops {sp.count_ops(res)}" if res is not None else ""))
result = "unresolved"
if res is not None:
    fl = sp.factor_list(res)
    signs = []
    for fac, mult in fl[1]:
        poly = sp.Poly(sp.expand(fac), x, E, u)
        coeffs = poly.coeffs()
        signs.append({"factor_ops": sp.count_ops(fac), "mult": mult, "n_terms": len(coeffs),
                      "all_coeffs_same_sign": all(c > 0 for c in coeffs) or all(c < 0 for c in coeffs)})
    S.note("A3", "factor sign structure (as polynomials in x, E, u)", str(signs)[:3000])
    S.note("A3", "why not decisive", "E = e^{-x} ties E and x; a polynomial in (x, E, u) with mixed-sign coefficients is not "
           "manifestly signed on the curve E = e^{-x}, and the resultant only locates where the derivative can vanish.")
S.R["outcome"] = result
S.R["lines"] = S.lines
save_json(S.R, "t13_A3_attempt.json")
S.out(f"A3 symbolic attempt: {result}")
