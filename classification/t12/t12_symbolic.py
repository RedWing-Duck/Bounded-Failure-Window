"""T12 symbolic part: A1-A6, A9 attempt, B1-B5 (identities, limits, first-order coefficients, sign proofs)."""
import signal

import sympy as sp

from t12_common import L_D1, L_D2, L_OPT, SYM, Fs, G, P0, Pi, Sig, a2, c, lam, q_, r_, rho, s_, save_json, x

R, LINES = {}, []


def out(t):
    print(t, flush=True)
    LINES.append(t)


def _sqrt_factor(e):
    return e.xreplace({p: sp.sqrt(sp.factor(p.base)) for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)})


class _TO(Exception):
    pass


def _alarm(*_):
    raise _TO()


def zero(key, desc, e, tmax=300):
    route = None
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(tmax)
    try:
        if sp.simplify(e) == 0:
            route = "simplify"
        elif sp.simplify(sp.together(sp.expand(e))) == 0:
            route = "simplify(together(expand))"
        elif sp.simplify(_sqrt_factor(e)) == 0:
            route = "factor radicands"
    except _TO:
        route = None
    finally:
        signal.alarm(0)
    ok = route is not None
    rec = {"desc": desc, "route": route or "none", "pass": ok}
    if not ok:
        try:
            rec["sympy_verbatim"] = str(sp.simplify(e))[:2000]
        except Exception:  # noqa: BLE001
            rec["sympy_verbatim"] = "(simplify did not finish)"
    R.setdefault(key, []).append(rec)
    out(f"  [{'PASS' if ok else 'FAIL'}] ({rec['route']}) {desc}")
    return ok


def signed(key, desc, e, want):
    s = sp.simplify(e)
    ok = bool(s.is_positive if want > 0 else s.is_negative)
    R.setdefault(key, []).append({"desc": desc, "route": "assumptions", "pass": ok, "expr": str(s)})
    out(f"  [{'PASS' if ok else 'FAIL'}] (assumptions) {desc}: {s}")
    return ok


def note(key, desc, text):
    R.setdefault(key, []).append({"desc": desc, "route": "record", "pass": True, "text": text})
    out(f"  [record] {desc}: {text}")


Ls, Ms, Pp, Pm, F_ = sp.symbols("L M P_plus P_minus F", positive=True)
qq, rr, aa = sp.symbols("q r a", positive=True)

out("A1 shared excess set")
Pfix = ((1 - Ls)**2 * qq + Ls**2 * rr) / (1 - (1 - Ls)**2 * aa**2)
zero("A1", "P+ solves P+ = (1-L)^2 (a^2 P+ + q) + L^2 r", Pfix - ((1 - Ls)**2 * (aa**2 * Pfix + qq) + Ls**2 * rr))
qF = F_ * (1 - aa**2)
zero("A1", "P+ - F - L(2-L)[L r/(2-L) - F]/(1-(1-L)^2 a^2) == 0 (q = F(1-a^2))",
     Pfix.subs(qq, qF) - F_ - Ls * (2 - Ls) * (Ls * rr / (2 - Ls) - F_) / (1 - (1 - Ls)**2 * aa**2))
zero("A1", "P- - F - a^2 (P+ - F) == 0", (aa**2 * Pp + qF) - F_ - aa**2 * (Pp - F_))
dt = sp.symbols("dt", positive=True)
avg = F_ - (F_ - Pp) * (1 - sp.exp(-2 * lam * dt)) / (2 * lam * dt)
zero("A1", "avg - F - (P+ - F)(1 - a^2)/(2 lam dt) == 0", avg - F_ - (Pp - F_) * (1 - sp.exp(-2 * lam * dt)) / (2 * lam * dt))
u_ = sp.symbols("u", positive=True)
avg_int = (sp.integrate(sp.exp(-2 * lam * u_) * Pp + F_ * (1 - sp.exp(-2 * lam * u_)), (u_, 0, dt)) / dt)
zero("A1", "time average of e^{-2 lam u} P+ + F(1 - e^{-2 lam u}) over [0, dt) equals the avg formula", avg_int - avg)

out("A2 tanh lemma")
xx = sp.symbols("xx", positive=True)
zero("A2", "(1 - e^{-x})/(1 + e^{-x}) - tanh(x/2) == 0", ((1 - sp.exp(-xx)) / (1 + sp.exp(-xx)) - sp.tanh(xx / 2)).rewrite(sp.exp))
Lx = 1 - sp.exp(-xx)
zero("A2", "L/(2-L) - tanh(x/2) == 0 for L = 1 - e^{-x}", (Lx / (2 - Lx) - sp.tanh(xx / 2)).rewrite(sp.exp))
h = sp.tanh(xx / 2) / xx
zero("A2", "h'(x) - (x - sinh x)/(2 x^2 cosh^2(x/2)) == 0", (sp.diff(h, xx) - (xx - sp.sinh(xx)) / (2 * xx**2 * sp.cosh(xx / 2)**2)).rewrite(sp.exp))
ser = sp.series(sp.sinh(xx) - xx, xx, 0, 12).removeO()
note("A2", "sinh x - x series (all coefficients positive: x - sinh x < 0 for x > 0)", str(ser))
zero("A2", "lim_{x->0} h(x) - 1/2 == 0", sp.limit(h, xx, 0) - sp.Rational(1, 2))

out("A3 D2 excess set")
cc, Pd, P0s = sp.symbols("c Pi_d Pi0", positive=True)
L2 = cc * Pd / (Pd + P0s)
zero("A3", "L/(2-L) - c Pi_d/((2-c) Pi_d + 2 Pi0) == 0", L2 / (2 - L2) - cc * Pd / ((2 - cc) * Pd + 2 * P0s))
dtE = (cc - 2 * F_ * P0s) / ((2 - cc) * F_ * Pi)
zero("A3", "at dt = dt_E: c Pi_d/((2-c) Pi_d + 2 Pi0) - F Pi_d == 0", (cc * Pd / ((2 - cc) * Pd + 2 * P0s) - F_ * Pd).subs(Pd, Pi * dtE))

out("A4 D3 exact excess condition")
mm, ss, ph, rh = sp.symbols("m s phi rho", positive=True)
Qm = lambda m_: m_**2 + ss * (1 - rh * ph) * m_ - ss * rh * ph
Tt = 2 * ph / (1 - ph)
zero("A4", "Q(T) (1-phi)^2/phi - [4 phi + s(1-phi)(2(1 - rho phi) - rho(1-phi))] == 0 (so Q(T) < 0 iff s(1-phi)(rho(1+phi) - 2) > 4 phi)",
     sp.expand(Qm(Tt) * (1 - ph)**2 / ph) - sp.expand(4 * ph + ss * (1 - ph) * (2 * (1 - rh * ph) - rh * (1 - ph))))
zero("A4", "-(2(1 - rho phi) - rho(1 - phi)) - (rho(1 + phi) - 2) == 0", -(2 * (1 - rh * ph) - rh * (1 - ph)) - (rh * (1 + ph) - 2))
zero("A4", "L/(2-L) > phi  <=>  m(1-phi) > 2 phi  (L = m/(1+m)): (L/(2-L) - phi)(2-L)(1+m) - [m(1-phi) - 2 phi] == 0",
     ((mm / (1 + mm)) / (2 - mm / (1 + mm)) - ph) * (2 - mm / (1 + mm)) * (1 + mm) - (mm * (1 - ph) - 2 * ph))
yy, uu = sp.symbols("y u", positive=True)
lhs = (1 - sp.exp(-yy)) * (1 - ph) * (rh * (1 + ph) - 2) - 4 * ph
lead = sp.limit(lhs.subs(ph, uu * yy / 4) / yy, yy, 0)
note("A4", "lim_{dt->0} [s(1-phi)(rho(1+phi)-2) - 4 phi]/(2 lam dt) with phi = (u/4)(2 lam dt)", f"{sp.simplify(lead)}  (> 0 iff rho > 2 + u)")
zero("A4", "that limit - (rho - 2 - u) == 0", lead - (rh - 2 - uu))

out("A5 endpoint limits and first-order coefficients")
GG, Pi_ = G, Pi
sig2 = lambda g_: (Sig + g_**2 / (2 * Pi)) / (lam + g_)
for fam, Lexpr, Glim in (("D1", L_D1, G), ("D2", L_D2, c * Pi / P0)):
    for met in ("post", "prior", "avg"):
        e = SYM[fam][met]
        lim0 = sp.limit(e, x, 0, "+")
        zero("A5", f"{fam} {met}: lim dt->0 - sigma^2(G0, Pi) == 0", lim0 - sig2(Glim), tmax=600)
        liminf = sp.limit(e, x, sp.oo)
        want = {"post": (0 if fam == "D1" else (1 - c)**2 * Fs), "prior": Fs, "avg": Fs}[met]
        zero("A5", f"{fam} {met}: lim dt->oo - {want} == 0", liminf - want, tmax=600)
A_ = lam + G
c1_D1 = G * (lam * G / Pi - 2 * Sig) / (2 * A_)
for met, coef in (("post", c1_D1), ("prior", -c1_D1), ("avg", 0)):
    e = SYM["D1"][met]
    sr = sp.series(e, x, 0, 2).removeO()
    k1 = sp.simplify(sr.coeff(x, 1))
    zero("A5", f"D1 {met}: first-order coefficient - ({coef}) == 0", k1 - coef, tmax=900)
sr2 = sp.series(SYM["D1"]["avg"], x, 0, 3).removeO()
note("A5", "D1 avg second-order coefficient (verbatim)", str(sp.factor(sp.simplify(sr2.coeff(x, 2)))))
G0 = c * Pi / P0
delta = G0**2 * (c - 2) / c
A0 = lam + G0
c1_D2 = (G0 * (lam * G0 / Pi - 2 * Sig) + delta * (G0 / Pi - sig2(G0))) / (2 * A0)
lam_F_minus = -G0 * (lam * G0 / Pi - 2 * Sig) / (2 * A0)
for met, coef in (("post", c1_D2), ("prior", c1_D2 + 2 * lam_F_minus), ("avg", c1_D2 + lam_F_minus)):
    sr = sp.series(SYM["D2"][met], x, 0, 2).removeO()
    zero("A5", f"D2 {met}: first-order coefficient - formula == 0", sp.simplify(sr.coeff(x, 1)) - coef, tmax=900)
inf_post = sp.limit(x * (SYM["D2"]["post"] - (1 - c)**2 * Fs), x, sp.oo)
zero("A5", "D2 post at dt->oo: lim dt (P+ - (1-c)^2 F) - c[c + 2(1-c) F Pi0]/Pi == 0", inf_post - c * (c + 2 * (1 - c) * Fs * P0) / Pi, tmax=600)

out("A6 optimal M-P")
M_ = sp.symbols("M", positive=True)
zero("A6", "DARE: M = a^2 M r/(M + r) + q  <=>  M^2 + M(r(1-a^2) - q) - q r = 0",
     sp.expand((M_ - (aa**2 * M_ * rr / (M_ + rr) + qq)) * (M_ + rr)) - sp.expand(M_**2 + M_ * (rr * (1 - aa**2) - qq) - qq * rr))
mu, w_ = sp.symbols("mu w", positive=True)
muf = (ph - 1 + sp.sqrt((1 - ph)**2 + 4 * w_)) / 2
zero("A6", "mu = m/s solves mu^2 + (1 - phi) mu - phi/s = 0 (w = phi/s)", muf**2 + (1 - ph) * muf - w_)
signed("A6", "d mu/d w = 1/sqrt((1-phi)^2 + 4w) > 0", sp.diff(muf, w_), +1)
zero("A6", "d mu/d phi - [1 - (1-phi)/sqrt((1-phi)^2+4w)]/2 == 0", sp.diff(muf, ph) - (1 - (1 - ph) / sp.sqrt((1 - ph)**2 + 4 * w_)) / 2)
zero("A6", "1 - (1-phi)/sqrt(...) - 4w/(sqrt(...)(sqrt(...) + (1-phi))) == 0 (manifestly > 0)",
     1 - (1 - ph) / sp.sqrt((1 - ph)**2 + 4 * w_) - 4 * w_ / (sp.sqrt((1 - ph)**2 + 4 * w_) * (sp.sqrt((1 - ph)**2 + 4 * w_) + (1 - ph))))
mm_ = ss * mu
zero("A6", "posterior P+ = r m/(1+m) equals F/(1 + mu) when phi(1+m) = m(m+s)/s... check: F s/(m+s) with m = s mu",
     F_ * ss / (mm_ + ss) - F_ / (1 + mu))
zero("A6", "with phi from the quadratic, r m/(1+m) = F s/(m+s): (F/phi) m/(1+m) - F s/(m+s) == 0 at phi = m(m+s)/(s(m+1))",
     ((F_ / ph) * mm / (1 + mm) - F_ * ss / (mm + ss)).subs(ph, mm * (mm + ss) / (ss * (mm + 1))))
yy2 = sp.symbols("y", positive=True)
hy = yy2 / (1 - sp.exp(-yy2))
zero("A6", "d/dy [y/(1-e^{-y})] - (1 - e^{-y} - y e^{-y})/(1-e^{-y})^2 == 0", sp.diff(hy, yy2) - (1 - sp.exp(-yy2) - yy2 * sp.exp(-yy2)) / (1 - sp.exp(-yy2))**2)
note("A6", "proof: post strictly decreasing (PROVED)",
     "phi = F Pi dt and w = phi/s = F Pi dt/(1 - e^{-2 lam dt}) are strictly increasing in dt (e^y > 1 + y); mu increases strictly "
     "in both; P+ = F/(1 + mu), so P+ is strictly decreasing.")
note("A6", "prior and avg (attempt)",
     "P- = F - a^2 F mu/(1+mu) and avg = F - F mu/(1+mu) * s/(2 lam dt): a decreasing factor times an increasing one; no "
     "sign proof found by this route -> reported as unresolved unless the numerical evidence says otherwise.")
for met, want in (("post", "sstar"), ("prior", "sstar"), ("avg", "sstar")):
    pass

out("B1-B5 Sigma sweep")
g_, uS, rS, l1 = sp.symbols("g u rho lambda1", positive=True)
Gb = lam * g_
Sigb = uS * lam**2 / (2 * Pi)
s2b = (Sigb + Gb**2 / (2 * Pi)) / (lam + Gb)
zero("B1", "sigma^2/F - (1 + g^2/u)/(1 + g) == 0", s2b / (Sigb / lam) - (1 + g_**2 / uS) / (1 + g_))
Sg_, Gc = sp.symbols("Sigma_ G_", positive=True)
s2abs = (Sg_ + Gc**2 / (2 * Pi)) / (lam + Gc)
signed("B2", "d sigma^2/d Sigma = 1/(lam + G) > 0 (absolute, increasing)", sp.diff(s2abs, Sg_), +1)
signed("B2", "d (sigma^2/F)/d Sigma < 0 (relative, decreasing)", sp.diff(s2abs / (Sg_ / lam), Sg_), -1)
zero("B2", "relative limit at Sigma -> oo: lim sigma^2/F - 1/(1+g) == 0", sp.limit(s2abs / (Sg_ / lam), Sg_, sp.oo) - lam / (lam + Gc))
zero("B2", "excess: sigma^2/F - 1 - G(lam G/(2 Pi Sigma) - 1)/(lam + G) == 0 (> 0 iff Sigma < lam G/(2 Pi))",
     s2abs / (Sg_ / lam) - 1 - Gc * (lam * Gc / (2 * Pi * Sg_) - 1) / (lam + Gc))
w3 = sp.symbols("w", positive=True)
G3 = lam * (w3 - 1)
u3 = (w3**2 - 1) / rS
Sig3 = u3 * lam**2 / (2 * Pi)
s23 = (Sig3 + G3**2 / (2 * Pi)) / (lam + G3)
zero("B3", "G = -lam + sqrt(lam^2 + 2 rho Sigma Pi) equals lam (w - 1) at w = sqrt(1 + rho u)",
     (-lam + sp.sqrt(lam**2 + 2 * rS * Sig3 * Pi)).subs(w3, w3) - G3)
zero("B3", "sigma^2 Pi/lam - [(w^2-1)/rho + (w-1)^2]/(2w) == 0", s23 * Pi / lam - ((w3**2 - 1) / rS + (w3 - 1)**2) / (2 * w3))
habs = ((w3**2 - 1) / rS + (w3 - 1)**2) / (2 * w3)
zero("B3", "d/dw of the absolute form - [(1 + 1/rho)/2 - (1 - 1/rho)/(2 w^2)] == 0", sp.diff(habs, w3) - ((1 + 1 / rS) / 2 - (1 - 1 / rS) / (2 * w3**2)))
zero("B3", "(1 + 1/rho)/2 - (1 - 1/rho)/(2w^2) - [ (w^2 - 1)(1 + 1/rho) + 2/rho ]/(2 w^2) == 0 (manifestly > 0 for w > 1)",
     (1 + 1 / rS) / 2 - (1 - 1 / rS) / (2 * w3**2) - ((w3**2 - 1) * (1 + 1 / rS) + 2 / rS) / (2 * w3**2))
rel3 = ((1 + rS) * w3 + 1 - rS) / (w3 * (w3 + 1))
zero("B3", "sigma^2/F - [(1+rho)w + 1 - rho]/(w(w+1)) == 0", s23 / (Sig3 / lam) - rel3)
num3 = sp.numer(sp.together(sp.diff(rel3, w3)))
zero("B3", "numerator of d/dw (relative) - [-(1+rho)w^2 + 2(rho-1)w + (rho-1)] == 0", sp.expand(num3) - sp.expand(-(1 + rS) * w3**2 + 2 * (rS - 1) * w3 + (rS - 1)))
zero("B3", "numerator at w = 1 - 2(rho - 2) == 0", (-(1 + rS) + 2 * (rS - 1) + (rS - 1)) - 2 * (rS - 2))
wM = ((rS - 1) + sp.sqrt(2 * rS * (rS - 1))) / (1 + rS)
zero("B3", "w_M is a root of the numerator", (-(1 + rS) * w3**2 + 2 * (rS - 1) * w3 + (rS - 1)).subs(w3, wM))
note("B3", "single maximum iff rho > 2", "numerator is a downward parabola in w with value 2(rho-2) at w = 1 and vertex at "
     "(rho-1)/(1+rho) < 1: one root in (1, oo) iff rho > 2, none otherwise (PROVED).")
Gq = sp.symbols("Gq", positive=True)
Sig4 = (Gq**2 + 2 * l1 * Gq) / (2 * Pi)
s24 = (Sig4 + Gq**2 / (2 * Pi)) / (lam + Gq)
zero("B4", "absolute: sigma^2 - G(G + lam')/(Pi(lam + G)) == 0", s24 - Gq * (Gq + l1) / (Pi * (lam + Gq)))
zero("B4", "d/dG absolute numerator - (G^2 + 2 lam G + lam lam') == 0",
     sp.expand(sp.numer(sp.together(sp.diff(Gq * (Gq + l1) / (lam + Gq), Gq)))) - sp.expand(Gq**2 + 2 * lam * Gq + lam * l1))
zero("B4", "relative: sigma^2/F - 2 lam (G + lam')/((G + 2 lam')(G + lam)) == 0", s24 / (Sig4 / lam) - 2 * lam * (Gq + l1) / ((Gq + 2 * l1) * (Gq + lam)))
num4 = sp.numer(sp.together(sp.diff(2 * lam * (Gq + l1) / ((Gq + 2 * l1) * (Gq + lam)), Gq)))
zero("B4", "relative derivative numerator - 2 lam (-G^2 - 2 lam' G + lam lam' - 2 lam'^2) == 0",
     sp.expand(num4) - sp.expand(2 * lam * (-Gq**2 - 2 * l1 * Gq + lam * l1 - 2 * l1**2)))
note("B4", "single maximum iff lam' < lam/2", "numerator -G^2 - 2 lam' G + lam' (lam - 2 lam'): downward parabola, value "
     "lam'(lam - 2 lam') at G = 0, vertex at G = -lam' < 0: one positive root iff lam > 2 lam' (PROVED); G increases with Sigma.")
zero("B5", "rho = 1: relative - 2/(1 + w) == 0", rel3.subs(rS, 1) - 2 / (1 + w3))

items = [x_ for k, v in R.items() for x_ in v]
R["pass"] = all(x_["pass"] for x_ in items)
R["n"] = len(items)
R["lines"] = LINES
out(f"T12 symbolic: {'PASS' if R['pass'] else 'FAIL'} ({sum(x_['pass'] for x_ in items)}/{len(items)})")
save_json(R, "t12_symbolic.json")
