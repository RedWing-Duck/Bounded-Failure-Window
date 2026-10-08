"""Task 10 shared code: families, the T10 turning-point method (mpmath), limits (PREREG_t10.md)."""
import json
import os

import mpmath as mp
import numpy as np

mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FIGS = os.path.join(HERE, "figs")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

PPD = 12
XLO, XHI = -25, 25
LIM, LIM_CHK = 80, 70
ZERO_LIM, INF_LIM = mp.mpf("1e-30"), mp.mpf("1e30")
WIDTH = mp.mpf("1e-30")
ZREL = mp.mpf("1e-40")
COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]


class NS:
    """Numeric namespace: mpmath or float64 (numpy scalars, overflow -> inf)."""

    def __init__(self, kind):
        self.mp = kind == "mp"
        if self.mp:
            self.sqrt, self.exp, self.f = mp.sqrt, mp.exp, mp.mpf
            self.pw = lambda a, b: mp.power(a, b)
        else:
            self.sqrt, self.exp, self.f = np.sqrt, np.exp, np.float64
            self.pw = lambda a, b: np.power(np.float64(a), np.float64(b))


MPN, FLN = NS("mp"), NS("fl")


def T(x, m=MPN):
    return m.pw(10, x)


# ---------------------------------------------------------------- model
def sig2(G, Pi, lam, Sig):
    return (Sig + G**2 / (2 * Pi)) / (lam + G)


def dsig2_dG(G, Pi, lam, Sig):
    return (G**2 + 2 * lam * G - 2 * Sig * Pi) / (2 * Pi * (lam + G)**2)


def N_of(G, eps, Pi, lam, Sig):
    return eps * (G**2 + 2 * lam * G - 2 * Sig * Pi) - G * (lam + G)


def gstar(Pi, lam, Sig, m=MPN):
    return 2 * Sig * Pi / (lam + m.sqrt(lam**2 + 2 * Sig * Pi))


# ---------------------------------------------------------------- Pi-sweep gain families: (G, eps)
def fam_bayes(p, m):
    c, P0 = p["c"], p["Pi0"]
    return lambda Pi: (c * Pi / (Pi + P0), P0 / (Pi + P0))


def fam_misspec(p, m):
    l1, S1 = p["lam1"], p["Sig1"]

    def g(Pi):
        G = 2 * S1 * Pi / (l1 + m.sqrt(l1**2 + 2 * S1 * Pi))
        return G, (G + 2 * l1) / (2 * (G + l1))
    return g


def fam_capped(p, m):
    g_, c = p["g"], p["c"]
    return lambda Pi: (g_ * Pi, 1) if g_ * Pi < c else (c, 0)


def fam_blind(p, m):
    G0 = p["G0"]
    return lambda Pi: (G0, 0)


def fam_hill(p, m):
    c, P0, n = p["c"], p["Pi0"], p["n"]

    def g(Pi):
        r = m.pw(P0 / Pi, n)            # = t^-n
        return c / (1 + r), n * r / (1 + r)
    return g


def fam_bayes2(p, m):
    c1, c2, a1, a2 = p["c1"], p["c2"], p["Pi01"], p["Pi02"]

    def g(Pi):
        G1, G2 = c1 * Pi / (Pi + a1), c2 * Pi / (Pi + a2)
        d = c1 * a1 / (Pi + a1)**2 + c2 * a2 / (Pi + a2)**2
        return G1 + G2, Pi * d / (G1 + G2)
    return g


def fam_hill2(p, m):
    c1, c2, a1, a2 = p["c1"], p["c2"], p["Pi01"], p["Pi02"]

    def g(Pi):
        r1, r2 = (a1 / Pi)**2, (a2 / Pi)**2
        G1, G2 = c1 / (1 + r1), c2 / (1 + r2)
        # Pi G_i' = 2 c_i r_i/(1+r_i)^2
        return G1 + G2, (2 * c1 * r1 / (1 + r1)**2 + 2 * c2 * r2 / (1 + r2)**2) / (G1 + G2)
    return g


FAMILIES = {"bayes": fam_bayes, "misspec": fam_misspec, "capped": fam_capped, "blind": fam_blind,
            "hill": fam_hill, "bayes2": fam_bayes2, "hill2": fam_hill2}


class Curve:
    """A swept curve: f(theta), derivative numerator d(theta) with the same sign as d sigma2/d theta,
    zero scale z(theta) for d, grid shift, and construction breakpoints (log10 theta)."""

    def __init__(self, f, d, z, shift=0, breaks=(), ffl=None, name=""):
        self.f, self.d, self.z, self.shift, self.breaks, self.ffl, self.name = f, d, z, shift, list(breaks), ffl, name


def pi_curve(fam, p, name=""):
    lam, Sig = p["lam"], p["Sig"]
    gm, gf = FAMILIES[fam](p, MPN), FAMILIES[fam](p, FLN)

    def f(Pi):
        G, _ = gm(Pi)
        return sig2(G, Pi, lam, Sig)

    def d(Pi):
        G, e = gm(Pi)
        return N_of(G, e, Pi, lam, Sig)

    def z(Pi):
        G, _ = gm(Pi)
        return ZREL * G * (lam + G)

    def ffl(Pi):
        with np.errstate(all="ignore"):
            G, _ = gf(Pi)
            return sig2(G, Pi, float(lam), float(Sig))
    br = [mp.log10(p["c"] / p["g"])] if fam == "capped" else []
    return Curve(f, d, z, 0, br, ffl, name or fam)


def mpize(p):
    return {k: (mp.mpf(v) if isinstance(v, (float, int, np.floating)) and k != "n" else v) for k, v in p.items()} | (
        {"n": mp.mpf(p["n"])} if "n" in p else {})


# ---------------------------------------------------------------- the T10 turning-point method
def _sgn(c, x):
    th = T(x)
    v = c.d(th)
    if abs(v) <= c.z(th):
        return 0, v
    return (1 if v > 0 else -1), v


def _bisect_sign(c, a, b, sa):
    """Sign change of c.d between a (sign sa) and b (sign -sa); returns x to width WIDTH."""
    while b - a > WIDTH:
        mdl = (a + b) / 2
        s, _ = _sgn(c, mdl)
        if s == 0:
            return mdl
        if s == sa:
            a = mdl
        else:
            b = mdl
    return (a + b) / 2


def _golden_min(h, a, b):
    g = (mp.sqrt(5) - 1) / 2
    x1, x2 = b - g * (b - a), a + g * (b - a)
    h1, h2 = h(x1), h(x2)
    while b - a > WIDTH:
        if h1 < h2:
            b, x2, h2 = x2, x1, h1
            x1 = b - g * (b - a)
            h1 = h(x1)
        else:
            a, x1, h1 = x1, x2, h2
            x2 = a + g * (b - a)
            h2 = h(x2)
    return (a + b) / 2


def grid(c):
    xs = [mp.mpf(XLO) + mp.mpf(i) / PPD for i in range((XHI - XLO) * PPD + 1)]
    xs = [x + c.shift for x in xs] + [mp.mpf(b) for b in c.breaks]
    return sorted(set(xs))


def turning_points(c):
    xs = grid(c)
    sv = [_sgn(c, x) for x in xs]
    pts = list(zip(xs, [s for s, _ in sv], [v for _, v in sv]))
    # adaptive step: local minima of |d| with three agreeing signs
    extra = []
    for i in range(1, len(pts) - 1):
        (xa, sa, va), (xb, sb, vb), (xc, sc, vc) = pts[i - 1], pts[i], pts[i + 1]
        if sa == sb == sc != 0 and abs(vb) <= abs(va) and abs(vb) <= abs(vc):
            xm = _golden_min(lambda x: sb * c.d(T(x)), xa, xc)
            s, v = _sgn(c, xm)
            if s == -sb:
                extra.append((xm, s, v))
    pts = sorted(pts + extra, key=lambda q: q[0])
    nz = [q for q in pts if q[1] != 0]
    turns = []
    for (xa, sa, _), (xb, sb, _) in zip(nz[:-1], nz[1:]):
        if sa != sb:
            x = _bisect_sign(c, xa, xb, sa)
            turns.append({"x": x, "theta": T(x), "value": c.f(T(x)), "kind": "max" if sa > 0 else "min"})
    # piece directions
    bounds = [mp.mpf(-LIM) + c.shift] + [t["x"] for t in turns] + [mp.mpf(LIM) + c.shift]
    dirs = []
    for k in range(len(bounds) - 1):
        s = [q[1] for q in nz if bounds[k] < q[0] < bounds[k + 1]]
        if s:
            dirs.append(s[0] if all(v == s[0] for v in s) else 0)
        else:
            dirs.append(_sgn(c, (bounds[k] + bounds[k + 1]) / 2)[0])
    return turns, dirs, bounds


def limit(c, x, xchk):
    """Endpoint limit with absolute zero/infinity criteria; ok = consistency with the check point."""
    v, w = c.f(T(x)), c.f(T(xchk))
    if abs(v) <= ZERO_LIM:
        return mp.mpf(0), bool(abs(w) <= mp.mpf("1e-20"))
    if v >= INF_LIM:
        return mp.inf, bool(w >= mp.mpf("1e20"))
    return v, bool(abs(v - w) <= mp.mpf("1e-30") * abs(v))


def analyse(c):
    turns, dirs, bounds = turning_points(c)
    Lm, okm = limit(c, mp.mpf(-LIM) + c.shift, mp.mpf(-LIM_CHK) + c.shift)
    Lp, okp = limit(c, mp.mpf(LIM) + c.shift, mp.mpf(LIM_CHK) + c.shift)
    return {"curve": c, "turns": turns, "dirs": dirs, "bounds": bounds, "L_minus": Lm, "L_plus": Lp,
            "limit_ok": [okm, okp],
            "approach_minus": "above" if dirs[0] > 0 else "below",
            "approach_plus": "above" if dirs[-1] < 0 else "below"}


def sf_match(x, stated_str):
    """Half a unit in the last stated digit (stated given as a string)."""
    s = stated_str.strip()
    dec = len(s.split(".")[1]) if "." in s else 0
    return bool(abs(mp.mpf(x) - mp.mpf(s)) <= mp.mpf(5) * mp.power(10, -(dec + 1)))


def save_json(obj, fname):
    def conv(o):
        if isinstance(o, mp.mpf):
            return float(o) if mp.isfinite(o) else str(o)
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, tuple):
            return list(o)
        return str(o)
    with open(os.path.join(RES, fname), "w") as fh:
        json.dump(obj, fh, indent=1, default=conv)
