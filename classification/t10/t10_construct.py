"""A1 constructions: target curves v(Pi) >= sigma*^2 and the gain G = G_+(v, Pi) (or G_- where stated)."""
import mpmath as mp

from t10_common import MPN, Curve, N_of, T, ZREL, gstar, sig2

LN10 = mp.log(10)


class PL:
    """Piecewise-linear w(x) on nodes x0, x0+1, ... with exponential tails (PREREG_t10 T10.2)."""

    def __init__(self, nodes, left_lim, right_lim, x0=6, xs=None):
        self.v = [mp.mpf(a) for a in nodes]
        self.x = [mp.mpf(a) for a in xs] if xs is not None else [mp.mpf(x0 + i) for i in range(len(nodes))]
        self.L, self.Rl = mp.mpf(left_lim), mp.mpf(right_lim)

    def __call__(self, x):
        X, V = self.x, self.v
        if x <= X[0]:
            return self.L - (self.L - V[0]) * mp.exp(x - X[0])
        if x >= X[-1]:
            return self.Rl - (self.Rl - V[-1]) * mp.exp(X[-1] - x)
        for i in range(len(X) - 1):
            if X[i] <= x <= X[i + 1]:
                return V[i] + (V[i + 1] - V[i]) * (x - X[i]) / (X[i + 1] - X[i])

    def d(self, x):
        X, V = self.x, self.v
        if x <= X[0]:
            return -(self.L - V[0]) * mp.exp(x - X[0])
        if x >= X[-1]:
            return (self.Rl - V[-1]) * mp.exp(X[-1] - x)
        for i in range(len(X) - 1):
            if X[i] <= x <= X[i + 1]:
                return (V[i + 1] - V[i]) / (X[i + 1] - X[i])


def v0(Pi, lam, Sig):
    s2 = gstar(Pi, lam, Sig) / Pi
    F = Sig / lam
    return s2 + s2 * (F - s2) / (2 * F)


def v0_dx(Pi, lam, Sig):
    """d v0 / dx (x = log10 Pi)."""
    s = mp.sqrt(lam**2 + 2 * Sig * Pi)
    s2 = gstar(Pi, lam, Sig) / Pi
    ds2_dPi = (Sig / s - s2) / Pi            # d(G*/Pi)/dPi with dG*/dPi = Sig/s
    F = Sig / lam
    dv_ds2 = 1 + (F - 2 * s2) / (2 * F)
    return dv_ds2 * ds2_dPi * Pi * LN10


class Target:
    """v(x) given by callables val(x), dval(x) (d/dx), with optional breakpoints; branch '+' or a switch."""

    def __init__(self, lam, Sig, val, dval, breaks=(), branch=None):
        self.lam, self.Sig, self.val, self.dval, self.breaks = mp.mpf(lam), mp.mpf(Sig), val, dval, list(breaks)
        self.branch = branch or (lambda Pi: 1)       # +1 upper, -1 lower

    def G(self, Pi):
        x = mp.log10(Pi)
        v = self.val(x)
        D = Pi**2 * v**2 - 2 * Pi * (self.Sig - self.lam * v)
        b = self.branch(Pi)
        return Pi * v + b * mp.sqrt(D), v, D, b

    def Gp(self, Pi):
        """dG/dPi by the chain rule through G_+-(v, Pi)."""
        x = mp.log10(Pi)
        G, v, D, b = self.G(Pi)
        lam, Sig = self.lam, self.Sig
        sD = mp.sqrt(D)
        dGdv = Pi + b * Pi * (Pi * v + lam) / sD
        dGdPi = v + b * (Pi * v**2 - Sig + lam * v) / sD
        dv_dPi = self.dval(x) / (Pi * LN10)
        return dGdv * dv_dPi + dGdPi

    def curve(self, name="constructed"):
        lam, Sig = self.lam, self.Sig

        def f(Pi):
            return sig2(self.G(Pi)[0], Pi, lam, Sig)

        def d(Pi):
            G = self.G(Pi)[0]
            return N_of(G, Pi * self.Gp(Pi) / G, Pi, lam, Sig)

        def z(Pi):
            G = self.G(Pi)[0]
            return ZREL * G * (lam + G)
        return Curve(f, d, z, 0, self.breaks, None, name)


def envelope_target(lam, Sig, w):
    """v = max(v0, w) with the crossing points of v0 and w added as breakpoints."""
    lam, Sig = mp.mpf(lam), mp.mpf(Sig)
    br = list(w.x)
    # crossings of v0 and w (scan then bisect)
    xs = [mp.mpf(-30) + mp.mpf(i) / 4 for i in range(241)]
    h = lambda x: w(x) - v0(T(x), lam, Sig)
    hv = [h(x) for x in xs]
    for i in range(len(xs) - 1):
        if (hv[i] > 0) != (hv[i + 1] > 0):
            br.append(mp.findroot(h, (xs[i], xs[i + 1]), solver="bisect", tol=mp.mpf("1e-45")))

    def val(x):
        return max(v0(T(x), lam, Sig), w(x))

    def dval(x):
        return w.d(x) if w(x) >= v0(T(x), lam, Sig) else v0_dx(T(x), lam, Sig)
    return Target(lam, Sig, val, dval, br)
