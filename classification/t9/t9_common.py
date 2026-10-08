"""Task 9 shared model (mpmath, 60 digits) and the root-finding classifier (PREREG_t9.md)."""
import json
import os

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)

EQ = mp.mpf("1e-40")
BIS_WIDTH = mp.mpf("1e-32")
NGRID = 200
COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]


def M(x):
    return mp.mpf(x) if not isinstance(x, mp.mpf) else x


# ---------------------------------------------------------------- model (document formulas)
def relay(tau, lam, Sig, Pi, G):
    a = lam + G
    return (Sig + G**2 / (2 * Pi * (1 + a * tau))) / a


def relay_d(tau, lam, Sig, Pi, G):
    a = lam + G
    return -G**2 / (2 * Pi * (1 + a * tau)**2)


def P_opt(tau, lam, Sig, Pi):
    b = 4 * Sig * tau + 2 * lam / Pi
    D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
    return 4 * Sig / (Pi * (b + mp.sqrt(D)))


# derivative of P from SymPy (independent of the document's dD/dtau)
_t, _l, _S, _P = sp.symbols("tau lambda Sigma Pi", positive=True)
_b = 4 * _S * _t + 2 * _l / _P
_D = _b**2 + 8 * _S * (1 - _l * _t)**2 / _P
P_SYM = 4 * _S / (_P * (_b + sp.sqrt(_D)))
_dP = sp.lambdify((_t, _l, _S, _P), sp.diff(P_SYM, _t), "mpmath")


def P_opt_d(tau, lam, Sig, Pi):
    return _dP(tau, lam, Sig, Pi)


def g_star(lam, Sig, Pi):
    return -lam + mp.sqrt(lam**2 + 2 * Sig * Pi)


def crit(lam, Sig, Pi, G):
    a = lam + G
    return {"F": Sig / lam, "V_w": (Sig + G**2 / (2 * Pi)) / a, "H_G": Sig / a,
            "s2": g_star(lam, Sig, Pi) / Pi}


def tau_R(R2, lam, Sig, Pi, G):
    a = lam + G
    return (G**2 / (2 * Pi * (a * R2 - Sig)) - 1) / a


def tau_F(lam, Sig, Pi, G):
    a = lam + G
    F = Sig / lam
    return (G / (2 * F * Pi) - 1) / a


def tau_star_R(R2, lam, Sig, Pi):
    Dl = 16 * Sig**2 - 16 * lam * Sig * R2 + 8 * lam**2 * (Sig - lam * R2) / Pi
    return (2 * lam * R2 - 4 * Sig + mp.sqrt(Dl)) / (2 * lam**2 * R2)


# ---------------------------------------------------------------- classifier
def _eq(a, b):
    if a == mp.inf or b == mp.inf:
        return a == b
    return abs(a - b) <= EQ * max(abs(a), abs(b))


def _bisect(g, lo, hi):
    """Root of g on [lo, hi] (log10 tau), g(lo), g(hi) of opposite sign; width 1e-32."""
    glo = g(lo)
    while hi - lo > BIS_WIDTH:
        mid = (lo + hi) / 2
        gm = g(mid)
        if gm == 0:
            return mid
        if (gm > 0) == (glo > 0):
            lo, glo = mid, gm
        else:
            hi = mid
    return (lo + hi) / 2


def analyse(f, df, lam):
    """f, df: callables of tau (mp). Returns turning points, limits and monotone pieces."""
    l10 = mp.log10(lam)
    X = [mp.mpf(-6) - l10 + mp.mpf(12) * i / (NGRID - 1) for i in range(NGRID)]
    sg = [int(mp.sign(df(mp.power(10, x)))) for x in X]
    turns = []
    nz = [i for i, s in enumerate(sg) if s != 0]
    for i, j in zip(nz[:-1], nz[1:]):
        if sg[i] != sg[j]:
            x = _bisect(lambda xx: df(mp.power(10, xx)), X[i], X[j])
            turns.append({"x": x, "tau": mp.power(10, x), "value": f(mp.power(10, x)),
                          "kind": "max" if sg[i] > 0 else "min"})
    xlo, xhi = -80 - l10, 80 - l10
    Lm, Lp = f(mp.power(10, xlo)), f(mp.power(10, xhi))
    chk = [_eq(Lm, f(mp.power(10, -70 - l10))), _eq(Lp, f(mp.power(10, 70 - l10)))]
    bounds = [xlo] + [t["x"] for t in turns] + [xhi]
    vals = [Lm] + [t["value"] for t in turns] + [Lp]
    pieces = []
    for p in range(len(bounds) - 1):
        s = [sg[i] for i in range(NGRID) if bounds[p] < X[i] < bounds[p + 1] and sg[i] != 0]
        d = s[0] if s and all(v == s[0] for v in s) else 0
        if not s:   # no grid point inside: sample the piece midpoint
            d = int(mp.sign(df(mp.power(10, (bounds[p] + bounds[p + 1]) / 2))))
        pieces.append({"lo": bounds[p], "hi": bounds[p + 1], "a": vals[p], "b": vals[p + 1], "dir": d})
    return {"f": f, "turns": turns, "L_minus": Lm, "L_plus": Lp, "limit_check": chk, "pieces": pieces,
            "approach_minus": "above" if pieces[0]["dir"] > 0 else "below",
            "approach_plus": "above" if pieces[-1]["dir"] < 0 else "below"}


def classify(A, R2):
    f = A["f"]
    parts = []
    for P in A["pieces"]:
        lo_v, hi_v = (P["a"], P["b"]) if P["dir"] > 0 else (P["b"], P["a"])
        if _eq(R2, hi_v) or R2 > hi_v:
            parts.append((False, False, None))
        elif _eq(R2, lo_v) or R2 < lo_v:
            parts.append((True, True, None))
        else:
            xc = _bisect(lambda x: f(mp.power(10, x)) - R2, P["lo"], P["hi"])
            parts.append((P["dir"] < 0, P["dir"] > 0, xc))
    comps, cur = [], None
    for j, (tl, tr, xc) in enumerate(parts):
        if not (tl and cur is not None) and (tl or tr):
            cur = {"touch_lo": j == 0 and tl, "lo": A["pieces"][j]["lo"] if tl else xc}
        if cur is None:
            continue
        joins = (tr and j + 1 < len(parts) and parts[j + 1][0]
                 and A["turns"][j]["value"] > R2 and not _eq(A["turns"][j]["value"], R2))
        if not joins:
            cur["touch_hi"] = (j == len(parts) - 1) and tr
            cur["hi"] = A["pieces"][j]["hi"] if tr else xc
            comps.append(cur)
            cur = None
    ell = int(any(c["touch_lo"] for c in comps))
    u = int(any(c["touch_hi"] for c in comps))
    k = sum(1 for c in comps if not c["touch_lo"] and not c["touch_hi"])
    cls = "All" if (len(comps) == 1 and ell and u) else (ell, u, k)
    return {"class": cls, "components": [(mp.power(10, c["lo"]), mp.power(10, c["hi"])) for c in comps]}


NAMES = {(0, 0, 0): "Empty", (1, 0, 0): "lower ray", (0, 1, 0): "upper ray", (1, 1, 0): "two rays",
         (0, 0, 1): "window", "All": "All"}


def name(cls):
    return NAMES.get(cls, str(cls))


def relay_sweep(lam, Sig, Pi, G):
    return (lambda t: relay(t, lam, Sig, Pi, G)), (lambda t: relay_d(t, lam, Sig, Pi, G))


def opt_sweep(lam, Sig, Pi):
    return (lambda t: P_opt(t, lam, Sig, Pi)), (lambda t: P_opt_d(t, lam, Sig, Pi))


def sf_match(x, stated, n=4):
    e = np.floor(np.log10(abs(stated)))
    return bool(abs(float(x) - stated) <= 0.5 * 10**(e - n + 1))


def draw_sets(rng, n):
    return 10.0**rng.uniform(-3, 3, size=(n, 4))       # lambda, Sigma, Pi, G


def save_json(obj, fname):
    def conv(o):
        if isinstance(o, mp.mpf):
            return float(o)
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, tuple):
            return list(o)
        return str(o)
    with open(os.path.join(RES, fname), "w") as fh:
        json.dump(obj, fh, indent=1, default=conv)


# ---------------------------------------------------------------- best constant-gain relay (float64)
def V_best(tau, lam, Sig, Pi):
    """V(tau) = inf_G sigma2(G, tau): 401-point bracket in log10 G in [log10 lam - 20, log10 lam + 20],
    bounded minimisation on the bracket (xatol 1e-12), then min with the G -> oo limit 1/(2 Pi tau)."""
    from scipy.optimize import minimize_scalar

    def f(x):
        G = 10.0**x
        a = lam + G
        return (Sig + G**2 / (2 * Pi * (1 + a * tau))) / a
    xs = np.linspace(np.log10(lam) - 20, np.log10(lam) + 20, 401)
    vals = np.array([f(x) for x in xs])
    i = int(np.argmin(vals))
    lo, hi = xs[max(i - 1, 0)], xs[min(i + 1, len(xs) - 1)]
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12})
    best = min(float(r.fun), float(vals[i]))
    nloc = int(np.sum((vals[1:-1] < vals[:-2]) & (vals[1:-1] < vals[2:])))
    return min(best, 1.0 / (2 * Pi * tau)), 10.0**r.x, nloc
