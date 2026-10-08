"""Task 11 shared code: power-normalized OU family, Stage 2 filter, delay, sampling; reuses the Task 10 classifier."""
import json
import os
import sys

import mpmath as mp
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "t10"))
from classify import classify, name, route_i, route_ii  # noqa: E402,F401
from t10_common import ZREL, Curve, T, turning_points  # noqa: E402,F401

mp.mp.dps = 50
RES = os.path.join(HERE, "results")
FIGS = os.path.join(HERE, "figs")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)
COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]

# ---------------------------------------------------------------- power family
_t, _b, _K, _l, _S = sp.symbols("tau beta K lambda Sigma", positive=True)
_v = _K / 2 * _t**(_b - 1)
_A = (1 - _l * _t)**2 / _t
_B = 4 * (_S + _l * _v)
_C = 4 * _S * _v
P_SYM = 2 * _C / (_B + sp.sqrt(_B**2 + 4 * _A * _C))
_dP = sp.lambdify((_t, _b, _K, _l, _S), sp.diff(P_SYM, _t), "mpmath")


def v_pow(tau, beta, K):
    return K / 2 * mp.power(tau, beta - 1)


def P_pow(tau, beta, K, lam, Sig):
    v = v_pow(tau, beta, K)
    A = (1 - lam * tau)**2 / tau
    B = 4 * (Sig + lam * v)
    C = 4 * Sig * v
    return 2 * C / (B + mp.sqrt(B**2 + 4 * A * C))


def dP_pow(tau, beta, K, lam, Sig):
    return _dP(tau, beta, K, lam, Sig)


def bound_pow(tau, beta, K, lam, Sig):
    return mp.sqrt(2 * Sig * K) * mp.power(tau, beta / 2) / abs(1 - lam * tau)


def sstar(lam, Sig, Pi):
    return 2 * Sig / (lam + mp.sqrt(lam**2 + 2 * Sig * Pi))


def limits_pow(beta, K, lam, Sig):
    """Proved limits (PREREG_t11 table) and extended outer brackets x_end (log10 tau)."""
    F = Sig / lam
    l10 = mp.log10(lam)
    if beta < 0:
        Lm, Lp = F, mp.mpf(0)
        xm = -max(mp.mpf(80), 50 / abs(beta)) - l10
        xp = mp.mpf(80) - l10
        xp = max(xp, 100 / (2 - beta) - l10)
    elif beta == 0:
        Lm, Lp = sstar(lam, Sig, 1 / K), mp.mpf(0)
        xm, xp = mp.mpf(-80) - l10, max(mp.mpf(80), 100 / mp.mpf(2)) - l10
    elif beta < 2:
        Lm, Lp = mp.mpf(0), mp.mpf(0)
        xm = -max(mp.mpf(80), 100 / beta) - l10
        xp = max(mp.mpf(80), 100 / (2 - beta)) - l10
    else:
        Lm, Lp = mp.mpf(0), F
        xm = -max(mp.mpf(80), 100 / beta) - l10
        xp = mp.mpf(80) - l10          # pre-registered default (PREREG_t11: "otherwise -+80")
    return Lm, Lp, xm, xp


def power_curve(beta, K, lam, Sig):
    f = lambda t: P_pow(t, beta, K, lam, Sig)
    d = lambda t: dP_pow(t, beta, K, lam, Sig)
    z = lambda t: ZREL * abs(f(t)) / t
    return Curve(f, d, z, -mp.log10(lam), [-mp.log10(lam)], None, f"power beta={beta}")


def analyse_with_limits(c, Lm, Lp, xm, xp):
    """T10 turning points + proved limits; outer brackets extended to xm, xp."""
    turns, dirs, bounds = turning_points(c)
    bounds = [xm] + bounds[1:-1] + [xp]
    vm, vp = c.f(T(xm)), c.f(T(xp))
    chk = [bool(abs(vm - Lm) <= (mp.mpf("1e-30") if Lm == 0 else mp.mpf("1e-20") * Lm)),
           bool(abs(vp - Lp) <= (mp.mpf("1e-30") if Lp == 0 else mp.mpf("1e-20") * Lp))]
    return {"curve": c, "turns": turns, "dirs": dirs, "bounds": bounds, "L_minus": Lm, "L_plus": Lp,
            "limit_check": chk, "approach_minus": "above" if dirs[0] > 0 else "below",
            "approach_plus": "above" if dirs[-1] < 0 else "below"}


# ---------------------------------------------------------------- Stage 2 filter (beta = 0)
def P_stage2(tau, lam, Sig, Pi):
    b = 4 * Sig * tau + 2 * lam / Pi
    D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
    return 4 * Sig / (Pi * (b + mp.sqrt(D)))


# ---------------------------------------------------------------- independent routes (matched variance with v(tau))
def P_wiener(tau, lam, Sig, v):
    k2 = 2 * Sig * tau**2 + 2 * v * tau
    bw = mp.sqrt((2 * Sig + 2 * v * tau * lam**2) / k2)
    Aw = 2 * Sig * (1 + lam * tau) / (mp.sqrt(k2) * (bw + lam))
    return Sig / lam - Aw**2 / (2 * lam)


def P_are(tau, lam, Sig, v):
    with mp.workdps(100):
        lam, Sig, v, tau = (mp.mpf(x) for x in (lam, Sig, v, tau))
        e0 = (2 * Sig + 2 * v / tau) / (lam + 1 / tau)**2
        prev = None
        for j in range(2, 26):
            eps = e0 * mp.power(10, -4 * j)
            H = mp.matrix(4, 4)
            A = [[-lam, 0], [0, -1 / tau]]
            Q = [[2 * Sig, 0], [0, 2 * v / tau]]
            for i in range(2):
                for k in range(2):
                    H[i, k] = A[k][i]
                    H[i, k + 2] = -1 / eps
                    H[i + 2, k] = -Q[i][k]
                    H[i + 2, k + 2] = -A[i][k]
            E, V = mp.eig(H)
            idx = [k for k in range(4) if mp.re(E[k]) < 0]
            U1 = mp.matrix([[V[i, k] for k in idx] for i in range(2)])
            U2 = mp.matrix([[V[i + 2, k] for k in idx] for i in range(2)])
            P = mp.re((U2 * U1**-1)[0, 0])
            if prev is not None and abs(P - prev) / abs(P) < mp.mpf("1e-12"):
                return +P, j, True
            prev = P
        return +P, j, False


# ---------------------------------------------------------------- spectra
def S_pow(omega, tau, beta, K):
    return K * mp.power(tau, beta) / (1 + tau**2 * omega**2)


def sign_changes_spectra(t1, t2, beta, K):
    """Signs of S_t1 - S_t2 on a 10/decade log-omega grid over [1e-40, 1e40]; returns (count, bracket)."""
    sgn, last, count, br = [], None, 0, None
    for i in range(801):
        w = mp.power(10, mp.mpf(-40) + mp.mpf(i) / 10)
        s1, s2 = S_pow(w, t1, beta, K), S_pow(w, t2, beta, K)
        dlt = s1 - s2
        s = 0 if abs(dlt) <= mp.mpf("1e-40") * max(s1, s2) else (1 if dlt > 0 else -1)
        if s != 0:
            if last is not None and s != last[0]:
                count += 1
                br = (last[1], w)
            last = (s, w)
    return count, br


def omega_star(t1, t2, beta):
    num = mp.power(t2, beta) - mp.power(t1, beta)
    den = t1**2 * t2**2 * (mp.power(t1, beta - 2) - mp.power(t2, beta - 2))
    return mp.sqrt(num / den) if num / den > 0 else None


# ---------------------------------------------------------------- delay
def P_delay(d, lam, Sig, Pi):
    F = Sig / lam
    return F - mp.exp(-2 * lam * d) * (F - sstar(lam, Sig, Pi))


# ---------------------------------------------------------------- sampling (integrate-and-dump)
def samp_Q(dt, lam, Sig):
    phi = mp.exp(-lam * dt)
    F = Sig / lam
    q11 = F * (1 - phi**2)
    q12 = 2 * Sig / lam**2 * ((1 - phi) - (1 - phi**2) / 2)
    q22 = 2 * Sig / lam**2 * (dt - 2 * (1 - phi) / lam + (1 - phi**2) / (2 * lam))
    return phi, q11, q12, q22


def samp_p(dt, lam, Sig, Pi):
    phi, q11, q12, q22 = samp_Q(dt, lam, Sig)
    h = (1 - phi) / (lam * dt)
    re = q22 / dt**2 + 1 / (Pi * dt)
    g = q12 / dt
    a2 = h**2
    a1 = re * (1 - phi**2) - q11 * h**2 + 2 * phi * h * g
    a0 = -(q11 * re - g**2)
    return 2 * (-a0) / (a1 + mp.sqrt(a1**2 - 4 * a2 * a0))


def samp_metrics(dt, lam, Sig, Pi):
    p = samp_p(dt, lam, Sig, Pi)
    F = Sig / lam
    fac = (1 - mp.exp(-2 * lam * dt)) / (2 * lam * dt)
    return p, p * fac + F * (1 - fac)


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


def sf_match(x, stated):
    s = stated.strip()
    dec = len(s.split(".")[1]) if "." in s else 0
    return bool(abs(mp.mpf(x) - mp.mpf(s)) <= mp.mpf(5) * mp.power(10, -(dec + 1)))
