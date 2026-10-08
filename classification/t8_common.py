"""Shared model, sweeps and the generic failure-set classifier for Task 8 (PREREG_t8.md)."""
import json
import os

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FIG = os.path.join(HERE, "figures")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

LAM, C, SIG = 1.0, 1.0, 0.01          # worked example
COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]

# classifier settings (pre-registered)
GRID_LO, GRID_HI, PPD = -60.0, 60.0, 40
LIM_LO, LIM_HI = -250.0, 250.0         # log10 theta used for the endpoint limits
LIM_CHK_LO, LIM_CHK_HI = -200.0, 200.0
BIG = 1e200
EQ_RTOL = 1e-12
XTOL = 1e-14
XGRID = np.linspace(GRID_LO, GRID_HI, int(round((GRID_HI - GRID_LO) * PPD)) + 1)


# ---------------------------------------------------------------- model
def sigma2(G, Pi, lam=LAM, sig=SIG):
    return (sig + G**2 / (2 * Pi)) / (lam + G)


def dsigma2_dG(G, Pi, lam=LAM, sig=SIG):
    """Lemma 3.1 (verified symbolically in T8.1(a))."""
    return (G**2 + 2 * lam * G - 2 * sig * Pi) / (2 * Pi * (lam + G)**2)


def g_star(Pi, lam=LAM, sig=SIG):
    return -lam + np.sqrt(lam**2 + 2 * sig * Pi)


def gain_sweep(gain, dgain, Pi, lam=LAM, sig=SIG):
    """sigma^2(theta) and its derivative for a gain map theta -> G(theta) at fixed Pi."""
    def f(th):
        with np.errstate(over="ignore", invalid="ignore"):
            return sigma2(gain(th), Pi, lam, sig)

    def df(th):
        with np.errstate(over="ignore", invalid="ignore", under="ignore"):
            return dsigma2_dG(gain(th), Pi, lam, sig) * dgain(th)
    return f, df


def prior_sweep(Pi, c, lam=LAM, sig=SIG):
    """theta = Pi_0, G = c Pi/(Pi + Pi_0)."""
    return gain_sweep(lambda p0: c * Pi / (Pi + p0), lambda p0: -c * Pi / (Pi + p0)**2, Pi, lam, sig)


def coupling_sweep(Pi, Pi0, lam=LAM, sig=SIG):
    """theta = c, G = c K, K = Pi/(Pi + Pi_0)."""
    K = Pi / (Pi + Pi0)
    return gain_sweep(lambda c: c * K, lambda c: K + 0 * c, Pi, lam, sig)


def tanh_sweep(Pi, c, lam=LAM, sig=SIG):
    def g(p0):
        return c * np.tanh(Pi / p0)

    def dg(p0):
        x = Pi / p0
        return -c / np.cosh(np.minimum(x, 700.0))**2 * Pi / p0**2
    return gain_sweep(g, dg, Pi, lam, sig)


def exp_sweep(Pi, c, lam=LAM, sig=SIG):
    return gain_sweep(lambda p0: -c * np.expm1(-Pi / p0),
                      lambda p0: -c * np.exp(-Pi / p0) * Pi / p0**2, Pi, lam, sig)


def hill_sweep(Pi, c, lam=LAM, sig=SIG):
    return gain_sweep(lambda p0: c * Pi**2 / (Pi**2 + p0**2),
                      lambda p0: -2 * c * Pi**2 * p0 / (Pi**2 + p0**2)**2, Pi, lam, sig)


def precision_sweep(Pi0, c=C, lam=LAM, sig=SIG):
    """Paper 1: theta = Pi, G = c Pi/(Pi + Pi_0); both G and the curve move with Pi."""
    def f(p):
        return sigma2(c * p / (p + Pi0), p, lam, sig)

    def df(p):
        G = c * p / (p + Pi0)
        dG = c * Pi0 / (p + Pi0)**2
        dPi = -G**2 / (2 * p**2 * (lam + G))          # explicit dependence on Pi
        return dsigma2_dG(G, p, lam, sig) * dG + dPi
    return f, df


# ---------------------------------------------------------------- classifier
def _t(x):
    return np.float64(10.0)**x


def _fin(v):
    v = float(v)
    return 1e300 if v == np.inf else (-1e300 if v == -np.inf else v)


def _eq(a, b):
    if not (np.isfinite(a) and np.isfinite(b)):
        return a == b
    return abs(a - b) <= EQ_RTOL * max(abs(a), abs(b))


def _lim(f, x):
    with np.errstate(all="ignore"):
        v = float(f(_t(x)))
    return np.inf if (not np.isfinite(v) or v > BIG) else v


def analyse(f, df):
    """Turning points, endpoint limits and monotone pieces of sigma^2 on (0, inf)."""
    def g(x):
        with np.errstate(all="ignore"):
            return _fin(df(_t(x)))
    d = np.asarray(df(10.0**XGRID), dtype=float)
    sg = np.sign(np.nan_to_num(d, nan=0.0))
    nz = np.nonzero(sg)[0]
    turns = []
    for i, j in zip(nz[:-1], nz[1:]):
        if sg[i] != sg[j]:
            x = brentq(g, XGRID[i], XGRID[j], xtol=XTOL)
            turns.append({"x": x, "theta": float(_t(x)), "value": float(f(_t(x))),
                          "kind": "max" if sg[i] > 0 else "min"})
    Lm, Lp = _lim(f, LIM_LO), _lim(f, LIM_HI)
    chk = []
    for L, xc in ((Lm, LIM_CHK_LO), (Lp, LIM_CHK_HI)):
        v = _lim(f, xc)
        chk.append(bool(_eq(L, v) or abs(L - v) <= 1e-9 * max(abs(L), abs(v))))
    # piece directions: sign on the grid points of each piece
    bounds = [LIM_LO] + [t["x"] for t in turns] + [LIM_HI]
    vals = [Lm] + [t["value"] for t in turns] + [Lp]
    pieces = []
    for p in range(len(bounds) - 1):
        m = (XGRID > bounds[p]) & (XGRID < bounds[p + 1]) & (sg != 0)
        s = sg[m]
        direction = int(s[0]) if len(s) else 0
        if len(s) and np.any(s != s[0]):
            direction = 0                                     # should not happen
        pieces.append({"lo": bounds[p], "hi": bounds[p + 1], "a": vals[p], "b": vals[p + 1], "dir": direction})
    return {"f": f, "turns": turns, "L_minus": Lm, "L_plus": Lp, "limit_check": chk, "pieces": pieces,
            # C4 definition: "from above" iff sigma^2 > L on the adjacent piece, i.e. the first piece
            # increases away from L_- and the last piece decreases towards L_+.
            "approach_minus": ("n/a (infinite)" if Lm == np.inf else "above" if pieces[0]["dir"] > 0 else "below"),
            "approach_plus": ("n/a (infinite)" if Lp == np.inf else "above" if pieces[-1]["dir"] < 0 else "below")}


def critical(A):
    """C6: finite endpoint limits and turning-point values."""
    c = [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]]
    return [v for v in c if np.isfinite(v)]


def classify(A, R2, crossings=True):
    """Class of F(R2) = {sigma^2 > R2} from the piece end values (Theorem 1.2 construction)."""
    f = A["f"]
    parts = []                      # (touch_left, touch_right, crossing x or None)
    for P in A["pieces"]:
        lo_v, hi_v = (P["a"], P["b"]) if P["dir"] > 0 else (P["b"], P["a"])
        if _eq(R2, hi_v) or R2 > hi_v:
            parts.append((False, False, None))
        elif _eq(R2, lo_v) or R2 < lo_v:
            parts.append((True, True, None))
        else:
            xc = None
            if crossings:
                with np.errstate(all="ignore"):
                    xc = brentq(lambda x: _fin(f(_t(x))) - R2, P["lo"], P["hi"], xtol=XTOL)
            parts.append((P["dir"] < 0, P["dir"] > 0, xc))
    comps, cur = [], None
    for j, (tl, tr, xc) in enumerate(parts):
        if tl and cur is not None:
            pass                                               # continues across the joint
        elif tl or tr:
            cur = {"start": j, "touch_lo": j == 0 and tl,
                   "lo": (A["pieces"][j]["lo"] if tl else xc)}
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
    if len(comps) == 1 and ell and u:
        cls = "All"
    else:
        cls = (ell, u, k)
    return {"class": cls, "components": [(c["lo"], c["hi"]) for c in comps]}


NAMES = {(0, 0, 0): "Empty", (1, 0, 0): "lower ray", (0, 1, 0): "upper ray", (1, 1, 0): "two rays",
         (0, 0, 1): "window", "All": "All"}


def name(cls):
    if cls in NAMES:
        return NAMES[cls]
    ell, u, k = cls
    return f"multi-window ({k})" if ell + u == 0 else f"mixed {cls}"


def sf_match(x, stated, n=4):
    e = np.floor(np.log10(abs(stated)))
    return bool(abs(x - stated) <= 0.5 * 10**(e - n + 1))


def save_json(obj, fname):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, tuple):
            return list(o)
        raise TypeError(type(o))
    with open(os.path.join(RES, fname), "w") as fh:
        json.dump(obj, fh, indent=1, default=conv)
