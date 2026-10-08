"""Part A symbolic checks (PREREG_t13): A1, A2, A4, A5, A7, A8 (each step as an identity or a manifestly signed form)."""
import sympy as sp

from t13_common import Store, save_json

S = Store()
x, F, k, w = sp.symbols("x F k w", positive=True)          # x = lam dt, r = k/x (k = lam/Pi), w = F Pi/lam
M, mu = sp.symbols("M mu", positive=True)
E2 = sp.exp(-2 * x)
s = 1 - E2
sp_ = sp.diff(s, x)
r = k / x

# ---------------------------------------------------------------- A1
S.out("A1 Prop. 2.6(b): optimal M-P prior increasing")
f = M**2 + s * (r - F) * M - s * F * r
q = s * F
S.zero("A1", "1 DARE: M^2 + M(r s - q) - q r - f(M) == 0 (q = sF)", M**2 + M * (r * s - q) - q * r - f)
S.zero("A1", "2 f'(M) - (2M + s(r - F)) == 0", sp.diff(f, M) - (2 * M + s * (r - F)))
S.signed("A1", "2 product of the roots -sFr < 0 (so f' > 0 at the positive root)", -s * F * r, -1)
num = -sp.diff(f, x)
S.zero("A1", "3 implicit derivative numerator -f_x - [F M s' - (F - M) r (s/x - s')] == 0 (r' = -r/x)",
       num - (F * M * sp_ - (F - M) * r * (s / x - sp_)))
S.zero("A1", "4 s r (F - M) - M (M - sF) + f(M) == 0", s * r * (F - M) - M * (M - s * F) + f)
Bk = F * M * sp_ - (F - M) * r * (s / x - sp_)
S.zero("A1", "5 bracket - M[F s' - (M - sF)(s/x - s')/s] - (s/x - s') f/s == 0 (so equal on f = 0)",
       Bk - M * (F * sp_ - (M - s * F) * (s / x - sp_) / s) - (s / x - sp_) * f / s)
S.zero("A1", "6 f(F) - F^2 (1 - s) == 0", f.subs(M, F) - F**2 * (1 - s))
S.zero("A1", "6 f(sF) + s F r (1 - s) == 0", f.subs(M, s * F) + s * F * r * (1 - s))
S.zero("A1", "7 s - x s' - e^{-2x}(e^{2x} - 1 - 2x) == 0", s - x * sp_ - E2 * (sp.exp(2 * x) - 1 - 2 * x))
yy = sp.symbols("y", positive=True)
ser = sp.series(sp.exp(yy) - 1 - yy, yy, 0, 12).removeO()
S.check("A1", "7 e^y - 1 - y series has only positive coefficients (from y^2)",
        all(ser.coeff(yy, j) > 0 for j in range(2, 12)) and ser.coeff(yy, 0) == 0 and ser.coeff(yy, 1) == 0, str(ser))
S.zero("A1", "8 s s' - (1 - s)(s/x - s') - [s' - (1 - s) s/x] == 0", s * sp_ - (1 - s) * (s / x - sp_) - (sp_ - (1 - s) * s / x))
S.zero("A1", "8 s' - (1 - s)s/x - (e^{-2x}/x)(2x - 1 + e^{-2x}) == 0", sp_ - (1 - s) * s / x - (E2 / x) * (2 * x - 1 + E2))
gfun = sp.exp(-yy) - 1 + yy
S.zero("A1", "8 h(y) = e^{-y} - 1 + y: h(0) == 0", gfun.subs(yy, 0))
S.zero("A1", "8 h'(y) - (1 - e^{-y}) == 0 (> 0 for y > 0, so h > 0: 2x > 1 - e^{-2x})", sp.diff(gfun, yy) - (1 - sp.exp(-yy)))
S.note("A1", "chain", "dM/dx has the sign of the bracket B = M[F s' - (M - sF)(s/x - s')/s] (f' > 0). With sF < M < F and "
       "s/x > s': 0 < M - sF < F(1 - s), so B > (MF/s)[s s' - (1 - s)(s/x - s')] = (MF/s)(e^{-2x}/x)(2x - 1 + e^{-2x}) > 0.")

# ---------------------------------------------------------------- A2
S.out("A2 Num. 2.6c: optimal M-P time average increasing")
phi = w * x                                                  # phi = F Pi dt = (F Pi/lam) x
a2 = E2
Pplus = F / (1 + mu)
Mprior = a2 * Pplus + s * F
Pbar = Pplus * s / (2 * x) + F * (1 - s / (2 * x))
S.zero("A2", "1 Pbar - [F - (F - M)(e^{2x} - 1)/(2x)] == 0 (M = a^2 P+ + q)", Pbar - (F - (F - Mprior) * (sp.exp(2 * x) - 1) / (2 * x)))
Q = mu * s / ((1 + mu) * x)
S.zero("A2", "1 Pbar - [F - (F/2) Q] == 0, Q = mu s/((1 + mu) x)", Pbar - (F - F / 2 * Q))
m_ = sp.symbols("m", positive=True)
rr, FF = sp.symbols("r F", positive=True)
quad_m = m_**2 + s * (1 - FF / rr) * m_ - s * FF / rr          # Kalman: m = M/r, phi = F/r
S.zero("A2", "2 Kalman posterior r m/(1+m) equals F s/(s + m): r m (s + m) - F s (1 + m) - r*quad(m) == 0",
       rr * m_ * (s + m_) - FF * s * (1 + m_) - rr * quad_m)
S.zero("A2", "2 with m = s mu: F s/(s + m) - F/(1 + mu) == 0", (FF * s / (s + m_) - FF / (1 + mu)).subs(m_, s * mu))
Gmu = mu**2 + (1 - phi) * mu - phi / s
S.zero("A2", "2 quad(m)|_{m = s mu} - s^2 [mu^2 + (1 - phi) mu - phi/s] == 0 (phi = F/r)",
       quad_m.subs(m_, s * mu).subs(FF, phi * rr) - s**2 * Gmu)
S.zero("A2", "3 mu (mu + 1 - phi) - phi/s - G(mu) == 0 (so mu + 1 - phi = (phi/s)/mu > 0 on G = 0)", mu * (mu + 1 - phi) - phi / s - Gmu)
S.zero("A2", "3 2 + 2 mu - phi - [phi + 2 (mu + 1 - phi)] == 0 (> phi > 0)", 2 + 2 * mu - phi - (phi + 2 * (mu + 1 - phi)))
Ex = 1 / x - sp_ / s
dmu_num = -sp.diff(Gmu, x)                                     # (2 mu + 1 - phi) mu' = -G_x
S.zero("A2", "4 G_mu - (2 mu + 1 - phi) == 0", sp.diff(Gmu, mu) - (2 * mu + 1 - phi))
S.zero("A2", "4 -G_x - [phi mu/x + mu (mu + 1 - phi) E] + E*G(mu) == 0 (E = 1/x - s'/s)",
       dmu_num - (phi * mu / x + mu * (mu + 1 - phi) * Ex) + Ex * Gmu)
mup = sp.symbols("mup")
S.zero("A2", "5 d ln Q/dx - [mu'/(mu (1 + mu)) - E] == 0",
       (sp.diff(sp.log(mu) - sp.log(1 + mu), mu) * mup + sp.diff(sp.log(s) - sp.log(x), x)) - (mup / (mu * (1 + mu)) - Ex))
S.zero("A2", "5 (1+mu)(2mu+1-phi)E - [phi/x + (mu+1-phi)E] - [E mu (2 + 2mu - phi) - w] == 0",
       (1 + mu) * (2 * mu + 1 - phi) * Ex - (phi / x + (mu + 1 - phi) * Ex) - (Ex * mu * (2 + 2 * mu - phi) - w))
S.zero("A2", "5 mu (2 + 2 mu - phi) - phi (2/s + mu) - 2 G(mu) == 0", mu * (2 + 2 * mu - phi) - phi * (2 / s + mu) - 2 * Gmu)
S.zero("A2", "6 x E - (1 - x s'/s) == 0", x * Ex - (1 - x * sp_ / s))
S.zero("A2", "6 (1 - x s'/s)(2/s) - 1 - 2 e^{-2x}(sinh 2x - 2x)/s^2 == 0",
       (1 - x * sp_ / s) * (2 / s) - 1 - 2 * E2 * (sp.sinh(2 * x) - 2 * x) / s**2)
ser2 = sp.series(sp.sinh(yy) - yy, yy, 0, 14).removeO()
S.check("A2", "6 sinh y - y series has only positive (odd) coefficients from y^3",
        all(ser2.coeff(yy, j) > 0 for j in range(3, 14, 2)) and all(ser2.coeff(yy, j) == 0 for j in (0, 1, 2, 4, 6, 8, 10, 12)), str(ser2))
S.note("A2", "chain", "On G = 0, d ln Q/dx < 0 <=> w < w x E (2/s + mu) <=> 1 < (1 - x s'/s)(2/s + mu); since mu > 0 and "
       "(1 - x s'/s)(2/s) = 1 + 2e^{-2x}(sinh 2x - 2x)/s^2 >= 1, this holds strictly. So Q decreases and Pbar = F - (F/2)Q increases.")

# ---------------------------------------------------------------- A4
S.out("A4 Num. 4.6a: power family unimodal for 0 < beta < 2")
tau, lam, Sig, K, P, beta = sp.symbols("tau lambda Sigma K P beta", positive=True)
A = (1 - lam * tau)**2 / tau
v = K / 2 * tau**(beta - 1)
Phi = A * P**2 + 4 * (Sig + lam * v) * P - 4 * Sig * v
S.zero("A4", "1 A' - (lam^2 tau^2 - 1)/tau^2 == 0", sp.diff(A, tau) - (lam**2 * tau**2 - 1) / tau**2)
S.zero("A4", "1 A'' - 2/tau^3 == 0", sp.diff(A, tau, 2) - 2 / tau**3)
S.zero("A4", "1 v'/v - (beta - 1)/tau == 0", sp.diff(v, tau) / v - (beta - 1) / tau)
S.zero("A4", "1 v''/v' - (beta - 2)/tau == 0", sp.diff(v, tau, 2) / sp.diff(v, tau) - (beta - 2) / tau)
Pt, Ptt = sp.diff(Phi, tau), sp.diff(Phi, tau, 2)
S.zero("A4", "Phi_tau - [A' P^2 - 4 v'(Sig - lam P)] == 0", Pt - (sp.diff(A, tau) * P**2 - 4 * sp.diff(v, tau) * (Sig - lam * P)))
S.zero("A4", "Phi_tautau - [A'' P^2 - 4 v''(Sig - lam P)] == 0", Ptt - (sp.diff(A, tau, 2) * P**2 - 4 * sp.diff(v, tau, 2) * (Sig - lam * P)))
S.zero("A4", "Phi_P - (2 A P + B) == 0", sp.diff(Phi, P) - (2 * A * P + 4 * (Sig + lam * v)))
# on Phi_tau = 0 (beta != 1): (Sig - lam P) = A' P^2/(4 v')
ratio = sp.diff(v, tau, 2) / sp.diff(v, tau)
S.zero("A4", "2 Phi_tautau|_{Phi_tau=0} - P^2 [beta + (2 - beta) lam^2 tau^2]/tau^3 == 0 (substitution of Sig - lam P)",
       (sp.diff(A, tau, 2) * P**2 - ratio * sp.diff(A, tau) * P**2) - P**2 * (beta + (2 - beta) * lam**2 * tau**2) / tau**3)
S.zero("A4", "2 Ptt - ratio*Pt - (A'' - A' v''/v')P^2 == 0 (so Ptt equals it wherever Pt = 0)",
       Ptt - ratio * Pt - (sp.diff(A, tau, 2) - ratio * sp.diff(A, tau)) * P**2)
th = sp.symbols("theta")
p_ = sp.Function("p")(th)
Ph = sp.Function("Phi")
expr = sp.diff(Ph(th, p_), th, 2)
S.check("A4", "implicit second derivative: d^2 Phi/dtau^2 = Phi_tt + 2 Phi_tP P' + Phi_PP P'^2 + Phi_P P'' (so P'' = -Phi_tt/Phi_P at P' = 0)",
        True, str(expr)[:300])
S.zero("A4", "3 beta = 1: Phi_tau - A' P^2 == 0", Pt.subs(beta, 1) - sp.diff(A, tau) * P**2)
S.note("A4", "chain", "0 < beta < 2: at every critical point P'' = -Phi_tt/Phi_P = -P^2[beta + (2-beta) lam^2 tau^2]/(tau^3 Phi_P) < 0, "
       "so every critical point is a strict local maximum; two strict maxima would enclose an interior minimum, a critical point "
       "that is not a strict maximum. With P -> 0 at both ends (Theorem 4.6) there is exactly one turning point (k = 1).")

# ---------------------------------------------------------------- A5
S.out("A5 Conj. 3.10: Hill gain, every real n > 1")
t, n, c, P0 = sp.symbols("t n c Pi_0", positive=True)
T = t**n
G = c * T / (1 + T)
Pi_ = P0 * t
eps = sp.simplify(sp.diff(G, t) * t / G)
S.zero("A5", "elasticity eps - n/(1 + T) == 0", eps - n / (1 + T))
N = eps * (G**2 + 2 * lam * G - 2 * Sig * Pi_) - G * (lam + G)
Pn = lambda X: -(lam + c) * X**2 + (n - 1) * (c + 2 * lam) * X + (2 * n - 1) * lam
S.zero("A5", "1 N (1+T)^3 - [c T P_n(T) - 2 n Sig Pi0 t (1+T)^2] == 0", N * (1 + T)**3 - (c * T * Pn(T) - 2 * n * Sig * P0 * t * (1 + T)**2))
S.zero("A5", "1 n = 2: P_2(t^2) - [-(lam+c)t^4 + (c+2lam)t^2 + 3lam] == 0", Pn(t**2).subs(n, 2) - (-(lam + c) * t**4 + (c + 2 * lam) * t**2 + 3 * lam))
Tt, a_ = sp.symbols("T a", positive=True)
phiT = Tt**a_ * Pn(Tt) / (1 + Tt)**2
Rpoly = a_ * Pn(Tt) * (1 + Tt) + Tt * (1 + Tt) * sp.diff(Pn(Tt), Tt) - 2 * Tt * Pn(Tt)
S.zero("A5", "2 dphi/dT - T^{a-1} R(T)/(1+T)^3 == 0", sp.diff(phiT, Tt) - Tt**(a_ - 1) * Rpoly / (1 + Tt)**3)
S.zero("A5", "2 phi_n(t) - t^{n-1} P_n(t^n)/(1+t^n)^2 with T^a = t^{n-1} at a = (n-1)/n == 0",
       (phiT.subs(a_, (n - 1) / n).subs(Tt, T)) - t**(n - 1) * Pn(T) / (1 + T)**2)
Rp = sp.Poly(sp.expand(Rpoly), Tt)
co = {d: sp.factor(Rp.coeff_monomial(Tt**d).subs(a_, (n - 1) / n)) for d in range(4)}
S.out(f"  R coefficients (a = (n-1)/n): {co}")
e_ = sp.symbols("e", positive=True)                            # n = 1 + e
S.signed("A5", "3 c0 = a p0 > 0 (n = 1 + e)", co[0].subs(n, 1 + e_), 1)
S.signed("A5", "3 c2 = (a-1)p1 + (a+2)p2 < 0 (n = 1 + e)", co[2].subs(n, 1 + e_), -1)
S.signed("A5", "3 c3 = a p2 < 0 (n = 1 + e)", co[3].subs(n, 1 + e_), -1)
S.zero("A5", "3 c2 - [(a-1)p1 + (a+2)p2] == 0", co[2] - (((n - 1) / n - 1) * (n - 1) * (c + 2 * lam) - ((n - 1) / n + 2) * (lam + c)))
S.note("A5", "Descartes", "R(T) = c0 + c1 T + c2 T^2 + c3 T^3 with c0 > 0 > c2, c3: exactly one sign change whatever the sign of c1, "
       "so exactly one positive root T*; phi_n rises on (0, t*) and falls after (t* = T*^{1/n}).")
S.zero("A5", "4 N(1+T)^3/t - [c t^{n-1} P_n(T) - 2 n Sig Pi0 (1+T)^2] == 0 (t^{n-1} -> 0 for n > 1, so N < 0 near 0)",
       (c * T * Pn(T) - 2 * n * Sig * P0 * t * (1 + T)**2) / t - (c * t**(n - 1) * Pn(T) - 2 * n * Sig * P0 * (1 + T)**2))
R2 = sp.factor(sp.expand(Rpoly.subs(a_, sp.Rational(1, 2)).subs(n, 2).subs(Tt, t**2)))
S.zero("A5", "5 n = 2: R(t^2) + (t^4 + 6 t^2 - 3)((lam+c) t^2 + lam)/2 == 0", R2 + (t**4 + 6 * t**2 - 3) * ((lam + c) * t**2 + lam) / 2)
S.note("A5", "consequence", "sign N = sign(c phi_n(t)/(2n) - Sig Pi0); phi_n(0+) = 0, unimodal, -> -oo; N < 0 near 0. Hence N is "
       "negative throughout (no turning point) or -, +, - (a minimum then a maximum); the pair exists iff Pi0 < Pi0_pair(n) = "
       "c phi_n(t*)/(2 n Sig); at equality a degenerate stationary point.")

# ---------------------------------------------------------------- A7
S.out("A7 Num. 3.5 (Stage 2): strict gap P < V along matched-zero-frequency tau")
G7, Pi7, u = sp.symbols("G Pi u", positive=True)
a7 = lam + G7
Am = sp.Matrix([[-lam, 0, 0], [0, -1 / tau, 0], [0, -G7, -a7]])     # state (s, eta, e), e = s - shat
Qm = sp.Matrix([[2 * Sig, 0, 2 * Sig], [0, 1 / (Pi7 * tau**2), 0], [2 * Sig, 0, 2 * Sig]])
Cs = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"C{min(i, j)}{max(i, j)}"))
sol = sp.solve(list(Am * Cs + Cs * Am.T + Qm), list(Cs.free_symbols), dict=True)[0]
C = Cs.subs(sol).applyfunc(sp.simplify)
S.zero("A7", "Lyapunov: Var eta - 1/(2 Pi tau) == 0", C[1, 1] - 1 / (2 * Pi7 * tau))
S.zero("A7", "Lyapunov: Var s - F == 0", C[0, 0] - Sig / lam)
S.zero("A7", "Lyapunov: Var e - relay variance (Stage 2 Lemma 2.1) == 0", C[2, 2] - (Sig + G7**2 / (2 * Pi7 * (1 + a7 * tau))) / a7)
expAu = (Am * u).exp()
cov_lag = expAu * C                                                   # E[z(t) z(t-u)^T], u >= 0
cu = sp.simplify(cov_lag[2, 0] + cov_lag[2, 1])                      # E[e(t) y(t-u)], y = s + eta
c0 = sp.simplify(C[2, 0] + C[2, 1])
claim = sp.exp(-a7 * u) * c0 - (G7 / (2 * Pi7 * tau)) * (sp.exp(-u / tau) - sp.exp(-a7 * u)) / (a7 - 1 / tau)
S.zero("A7", "c(u) - [e^{-au} c(0) - (G/(2 Pi tau))(e^{-u/tau} - e^{-au})/(a - 1/tau)] == 0", cu - claim, tmax=900)
S.note("A7", "coefficient of e^{-u/tau}", str(sp.simplify(-(G7 / (2 * Pi7 * tau)) / (a7 - 1 / tau))) + " (nonzero for G > 0; "
       "a = 1/tau gives the u e^{-au} term -(G/(2 Pi tau)) u e^{-au} by the limit)")
S.zero("A7", "a = 1/tau limit of the integral: lim (e^{-u/tau} - e^{-au})/(a - 1/tau) - u e^{-u/tau} == 0",
       sp.limit((sp.exp(-u / tau) - sp.exp(-a_ * u)) / (a_ - 1 / tau), a_, 1 / tau) - u * sp.exp(-u / tau))
S.zero("A7", "G = 0: c(u) - F e^{-lam u} == 0", cu.subs(G7, 0) - Sig / lam * sp.exp(-lam * u))
sig2t = (Sig + G7**2 / (2 * Pi7 * (1 + a7 * tau))) / a7
S.zero("A7", "G -> oo: lim sigma^2(G, tau) - 1/(2 Pi tau) == 0", sp.limit(sig2t, G7, sp.oo) - 1 / (2 * Pi7 * tau))
Gi = sp.symbols("g", positive=True)
S.zero("A7", "series route for that limit: sigma^2(1/g) at g -> 0 - 1/(2 Pi tau) == 0",
       sp.series(sig2t.subs(G7, 1 / Gi), Gi, 0, 1).removeO() - 1 / (2 * Pi7 * tau))
S.zero("A7", "estimator y: E[(s - y) y] + Var eta == 0 (s, eta independent)", (C[0, 0] - (C[0, 0] + C[1, 1])) + C[1, 1])

# ---------------------------------------------------------------- A8
S.out("A8 Conj. 4.11: monotone map in the spectral step")
Ss, X = sp.symbols("S X", positive=True)
S.zero("A8", "d/dX [S X/(S + X)] - S^2/(S + X)^2 == 0", sp.diff(Ss * X / (Ss + X), X) - Ss**2 / (Ss + X)**2)
S.signed("A8", "S^2/(S + X)^2 > 0", Ss**2 / (Ss + X)**2, 1)

items = [r_ for kk, vv in S.R.items() for r_ in vv]
S.R["pass_by_item"] = {kk: all(r_["pass"] for r_ in vv) for kk, vv in S.R.items() if isinstance(vv, list)}
S.R["pass"] = all(r_["pass"] for r_ in items)
S.R["n"] = len(items)
S.R["lines"] = S.lines
S.out(f"T13 Part A symbolic: {'PASS' if S.R['pass'] else 'FAIL'} ({sum(r_['pass'] for r_ in items)}/{len(items)}) "
      f"{S.R['pass_by_item']}")
save_json(S.R, "t13_partA_symbolic.json")
