"""Task 12 shared code: Delta-t sweep (M-P families, M-I) and Sigma sweep (B2-B5); curves for the two-route classifier."""
import json
import math
import os
import sys

import mpmath as mp
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "t10"))
sys.path.insert(0, os.path.join(HERE, "..", "t11"))
from classify import classify, name, route_i, route_ii  # noqa: E402,F401
from t10_common import ZREL, Curve, T  # noqa: E402,F401
from t11_common import analyse_with_limits, samp_metrics, sstar  # noqa: E402,F401

mp.mp.dps = 50
RES = os.path.join(HERE, "results")
FIGS = os.path.join(HERE, "figs")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)
COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]


def dps_for(z):
    """Working precision for an argument z whose smallness drives cancellation (z = lam*dt or u)."""
    z = mp.mpf(z)
    return 60 + (int(-2 * mp.log10(z)) + 10 if z < 1 else 0)


# ---------------------------------------------------------------- symbolic Delta-t metrics
x, lam, Sig, Pi, G, c, P0, rho = sp.symbols("x lambda Sigma Pi G c Pi_0 rho", positive=True)
Fs = Sig / lam
a2 = sp.exp(-2 * lam * x)
s_ = 1 - a2
q_ = Fs * s_
r_ = 1 / (Pi * x)


def metrics_from_L(L):
    den = L * (2 - L) + (1 - L)**2 * s_          # = 1 - (1-L)^2 a^2, written without cancellation
    post = ((1 - L)**2 * q_ + L**2 * r_) / den
    prior = a2 * post + q_
    avg = post * s_ / (2 * lam * x) + Fs * (1 - s_ / (2 * lam * x))
    return {"post": post, "prior": prior, "avg": avg}


def kalman_L(rho_):
    psi = rho_ * Fs * Pi * x
    m_lo = 2 * s_ * psi / (s_ * (1 - psi) + sp.sqrt(s_**2 * (1 - psi)**2 + 4 * s_ * psi))   # stable for psi <= 1
    m_hi = (s_ * (psi - 1) + sp.sqrt(s_**2 * (1 - psi)**2 + 4 * s_ * psi)) / 2             # stable for psi > 1
    return m_lo / (1 + m_lo), m_hi / (1 + m_hi)


L_D1 = 1 - sp.exp(-G * x)
L_D2 = c * Pi * x / (Pi * x + P0)
L_D3 = kalman_L(rho)
L_OPT = kalman_L(1)

SYM = {"D1": metrics_from_L(L_D1), "D2": metrics_from_L(L_D2),
       "D3": (metrics_from_L(L_D3[0]), metrics_from_L(L_D3[1])),
       "opt": (metrics_from_L(L_OPT[0]), metrics_from_L(L_OPT[1]))}
ARGS = (x, lam, Sig, Pi, G, c, P0, rho)
_NUM = {}


def _lamb(fam, metric):
    key = (fam, metric)
    if key not in _NUM:
        if fam in ("D3", "opt"):
            e_lo, e_hi = SYM[fam][0][metric], SYM[fam][1][metric]
            _NUM[key] = (sp.lambdify(ARGS, e_lo, "mpmath"), sp.lambdify(ARGS, sp.diff(e_lo, x), "mpmath", cse=True),
                         sp.lambdify(ARGS, e_hi, "mpmath"), sp.lambdify(ARGS, sp.diff(e_hi, x), "mpmath", cse=True))
        else:
            e = SYM[fam][metric]
            f, d = sp.lambdify(ARGS, e, "mpmath", cse=True), sp.lambdify(ARGS, sp.diff(e, x), "mpmath", cse=True)
            _NUM[key] = (f, d, f, d)
    return _NUM[key]


def dt_funcs(fam, metric, p):
    """mp value and derivative in dt for a Delta-t family; p has lam, Sig, Pi and G / c, Pi0 / rho."""
    f_lo, d_lo, f_hi, d_hi = _lamb(fam, metric)
    lam_, Sig_, Pi_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    a = [lam_, Sig_, Pi_, mp.mpf(p.get("G", 1)), mp.mpf(p.get("c", 1)), mp.mpf(p.get("Pi0", 1)), mp.mpf(p.get("rho", 1))]
    rho_ = a[6] if fam == "D3" else mp.mpf(1)

    def pick(t):
        return (f_hi, d_hi) if (fam in ("D3", "opt") and rho_ * Sig_ / lam_ * Pi_ * t > 1) else (f_lo, d_lo)

    def f(t):
        with mp.workdps(dps_for(lam_ * t)):
            return +pick(t)[0](mp.mpf(t), *a)

    def d(t):
        with mp.workdps(dps_for(lam_ * t)):
            return +pick(t)[1](mp.mpf(t), *a)
    return f, d


def mi_funcs(metric, p):
    lam_, Sig_, Pi_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    idx = 0 if metric == "a" else 1

    def f(t):
        with mp.workdps(dps_for(lam_ * t) + 40):
            return +samp_metrics(mp.mpf(t), lam_, Sig_, Pi_)[idx]

    def d(t):
        with mp.workdps(dps_for(lam_ * t) + 40):
            return +mp.diff(lambda y: samp_metrics(y, lam_, Sig_, Pi_)[idx], mp.mpf(t))
    return f, d


def sig2(G_, Pi_, lam_, Sig_):
    return (Sig_ + G_**2 / (2 * Pi_)) / (lam_ + G_)


def dt_limits(fam, metric, p):
    lam_, Sig_, Pi_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    F = Sig_ / lam_
    if fam == "D1":
        Lm = sig2(mp.mpf(p["G"]), Pi_, lam_, Sig_)
        Lp = mp.mpf(0) if metric == "post" else F
    elif fam == "D2":
        cc = mp.mpf(p["c"])
        Lm = sig2(cc * Pi_ / mp.mpf(p["Pi0"]), Pi_, lam_, Sig_)
        Lp = (1 - cc)**2 * F if metric == "post" else F
    elif fam == "D3":
        Gr = -lam_ + mp.sqrt(lam_**2 + 2 * mp.mpf(p["rho"]) * Sig_ * Pi_)
        Lm = sig2(Gr, Pi_, lam_, Sig_)
        Lp = mp.mpf(0) if metric == "post" else F
    elif fam == "opt":
        Lm = sstar(lam_, Sig_, Pi_)
        Lp = mp.mpf(0) if metric == "post" else F
    else:                                  # M-I
        Lm, Lp = sstar(lam_, Sig_, Pi_), F
    l10 = mp.log10(lam_)
    return Lm, Lp, -80 - l10, 80 - l10


def dt_curve(fam, metric, p):
    f, d = mi_funcs(metric, p) if fam == "MI" else dt_funcs(fam, metric, p)
    lam_ = mp.mpf(p["lam"])
    ffl = mi_float(metric, p) if fam == "MI" else dt_float(fam, metric, p)
    return Curve(f, d, lambda t: ZREL * abs(f(t)) / t, -mp.log10(lam_), [], ffl, f"{fam} {metric}")


def analyse_dt(fam, metric, p):
    Lm, Lp, xm, xp = dt_limits(fam, metric, p)
    return analyse_with_limits(dt_curve(fam, metric, p), Lm, Lp, xm, xp)


# ---------------------------------------------------------------- float64 Delta-t metrics (route (ii) in the blind search)
def _k(y):
    """1 - (1 - e^{-y})/y, stable."""
    return y / 2 - y**2 / 6 + y**3 / 24 if y < 1e-4 else 1 - (-math.expm1(-y)) / y


def dt_float(fam, metric, p):
    if fam == "MI":
        return None
    lam_, Sig_, Pi_ = (float(p[k]) for k in ("lam", "Sig", "Pi"))
    F = Sig_ / lam_

    def f(t):
        t = float(t)
        if not math.isfinite(t) or t <= 0:
            return float("nan")
        s = -math.expm1(-2 * lam_ * t)
        a2_ = math.exp(-2 * lam_ * t)
        r = 1 / (Pi_ * t)
        if fam == "D1":
            L = -math.expm1(-float(p["G"]) * t)
        elif fam == "D2":
            L = float(p["c"]) * Pi_ * t / (Pi_ * t + float(p["Pi0"]))
        else:
            rh = float(p["rho"]) if fam == "D3" else 1.0
            psi = rh * F * Pi_ * t
            sq = math.sqrt(s * s * (1 - psi)**2 + 4 * s * psi) if psi < 1e150 else s * psi * math.sqrt(1 + 4 / (s * psi))
            m = 2 * s * psi / (s * (1 - psi) + sq) if psi <= 1 else (s * (psi - 1) + sq) / 2
            L = m / (1 + m) if math.isfinite(m) else 1.0
        den = L * (2 - L) + (1 - L)**2 * s
        post = ((1 - L)**2 * F * s + L * L * r) / den
        if metric == "post":
            return post
        if metric == "prior":
            return a2_ * post + F * s
        y = 2 * lam_ * t
        return post * (1 - _k(y)) + F * _k(y)
    return f


# ---------------------------------------------------------------- Sigma sweep (x = log10 u, u = 2 Sigma Pi / lam^2)
_u, _l, _P, _G, _rho, _l1 = sp.symbols("u lambda Pi G rho lambda1", positive=True)
_Sg = _u * _l**2 / (2 * _P)
_sig2 = lambda Gv: (_Sg + Gv**2 / (2 * _P)) / (_l + Gv)
_GAIN = {"B2": _G, "B3": 2 * _rho * _Sg * _P / (_l + sp.sqrt(_l**2 + 2 * _rho * _Sg * _P)),
         "B5": 2 * _Sg * _P / (_l + sp.sqrt(_l**2 + 2 * _Sg * _P)),
         "B4": 2 * _Sg * _P / (_l1 + sp.sqrt(_l1**2 + 2 * _Sg * _P))}
_SARGS = (_u, _l, _P, _G, _rho, _l1)
_SNUM = {}


def _slamb(fam, conv):
    key = (fam, conv)
    if key not in _SNUM:
        e = _sig2(_GAIN[fam])
        if conv == "rel":
            e = e / (_Sg / _l)
        _SNUM[key] = (sp.lambdify(_SARGS, e, "mpmath"), sp.lambdify(_SARGS, sp.diff(e, _u), "mpmath"),
                      sp.lambdify(_SARGS, e, "math"))
    return _SNUM[key]


def sig_funcs(fam, conv, p):
    fm, dm, ff = _slamb(fam, conv)
    a = [mp.mpf(p["lam"]), mp.mpf(p["Pi"]), mp.mpf(p.get("G", 1)), mp.mpf(p.get("rho", 1)), mp.mpf(p.get("lam1", 1))]
    af = [float(v) for v in a]

    def f(u):
        with mp.workdps(dps_for(u)):
            return +fm(mp.mpf(u), *a)

    def d(u):
        with mp.workdps(dps_for(u)):
            return +dm(mp.mpf(u), *a)

    def ffl(u):
        try:
            return ff(float(u), *af)
        except (OverflowError, ZeroDivisionError, ValueError):
            return float("inf")
    return f, d, ffl


def sig_limits(fam, conv, p):
    lam_, Pi_ = mp.mpf(p["lam"]), mp.mpf(p["Pi"])
    if fam == "B2":
        Gv = mp.mpf(p["G"])
        return (Gv**2 / (2 * Pi_ * (lam_ + Gv)), mp.inf) if conv == "abs" else (mp.inf, lam_ / (lam_ + Gv))
    return (mp.mpf(0), mp.inf) if conv == "abs" else (mp.mpf(1), mp.mpf(0))


def analyse_sig(fam, conv, p):
    f, d, ffl = sig_funcs(fam, conv, p)
    c_ = Curve(f, d, lambda u: ZREL * abs(f(u)) / u, 0, [], ffl, f"{fam} {conv}")
    Lm, Lp = sig_limits(fam, conv, p)
    return analyse_with_limits(c_, Lm, Lp, mp.mpf(-80), mp.mpf(80))


def mi_float(metric, p):
    lam_, Sig_, Pi_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    idx = 0 if metric == "a" else 1

    def ffl(t):
        t = mp.mpf(float(t))
        with mp.workdps(dps_for(lam_ * t) - 30):
            return float(samp_metrics(t, lam_, Sig_, Pi_)[idx])
    return ffl


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


def sf_match(x_, stated):
    st = stated.strip()
    dec = len(st.split(".")[1]) if "." in st else 0
    return bool(abs(mp.mpf(x_) - mp.mpf(st)) <= mp.mpf(5) * mp.power(10, -(dec + 1)))
