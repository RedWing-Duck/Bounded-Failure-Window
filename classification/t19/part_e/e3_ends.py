"""Part E: endpoint behaviour of the D1 post derivative (dimensionless). N(t) = numerator of d(post/F)/dt over the positive
denominator; its leading terms at t -> 0 and t -> oo give the signs at the ends, hence the parity of the number of sign changes."""
import sympy as sp
t, g, nu = sp.symbols("t g nu", positive=True)
u, w = sp.exp(-g * t), sp.exp(-2 * t)
p = (u**2 * (1 - w) + 2 * (1 - u)**2 / (nu * t)) / (1 - u**2 * w)       # post/F (Pi = nu lam^2/(2 Sigma), F = Sigma/lam)
dp = sp.together(sp.diff(p, t))
num, den = sp.fraction(dp)
print("denominator:", sp.factor(den))
s0 = sp.series(num, t, 0, 4).removeO()
print("t -> 0 leading:", sp.factor(sp.collect(sp.expand(s0), t)))
# t -> oo: drop exponentially small terms
U, W = sp.symbols("U W", positive=True)
numUW = sp.expand(num.subs({sp.exp(-g * t): U, sp.exp(-2 * t): W}).subs({sp.exp(-2 * g * t): U**2}))
print("t -> oo (U, W -> 0) leading:", sp.factor(numUW.subs({U: 0, W: 0})))
p0 = sp.limit(p, t, 0)
print("post/F at 0+:", sp.simplify(p0), " ; excess condition p0 > 1 iff", sp.solve(sp.Eq(p0, 1), nu))
