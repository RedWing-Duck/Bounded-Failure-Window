"""Shared parameters, closed forms and the vectorised EM engine."""
import json
import os
import time

import numpy as np
from scipy.signal import lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
FIG = os.path.join(HERE, "figures")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

LAM, C, SIG = 1.0, 1.0, 0.01
F = SIG / LAM
H = SIG / (LAM + C)

# pre-registered simulation settings
DT = 1e-3
NTRAJ = 256
T_BURN = 20.0
T_SAMP = 200.0
T_BATCH = 10.0
GRID = np.sort(np.concatenate([np.logspace(-2, 2, 40), [1 / 9, 0.687, 4.0]]))

# categorical palette (slots 1-3 of the reference palette)
COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]


def g_kalman(pi, P, c=C):
    return c * pi / (pi + P)


def g_opt(pi, lam=LAM, sig=SIG):
    return -lam + np.sqrt(lam**2 + 2 * sig * pi)


def var_cf(pi, G, lam=LAM, sig=SIG):
    """Closed form (2)."""
    return (sig + G**2 / (2 * pi)) / (lam + G)


def var_em(pi, G, dt=DT, lam=LAM, sig=SIG):
    """Exact stationary variance of the EM recursion: D/(2a - a^2 dt)."""
    a = lam + G
    D = G**2 / pi + 2 * sig
    return D / (2 * a - a**2 * dt)


def ar1(u, rho, z):
    """y[n] = rho*y[n-1] + u[n] along axis 1, state carried in z (shape (ntraj,1))."""
    y, zf = lfilter([1.0], [1.0, -rho], u, axis=1, zi=z)
    return y, zf


def run_em(specs, seed, ntraj=NTRAJ, dt=DT, t_burn=T_BURN, t_samp=T_SAMP,
           t_batch=T_BATCH, drive=None, sensory=None):
    """Simulate many linear relays on common noise.

    specs: list of (a, gs, gsim) with  dx = -a x dt + gs dW_s + gsim dW_sim  (+ extras)
    drive: optional f(t_array, k) -> deterministic/extra additive increment array
           (ntraj, nstep) multiplied by spec-specific factor spec[3] if present.
    sensory: optional callable(chunk_index, dWs) -> replacement sensory increments
             (used for coloured noise); default is white dW_s.
    Returns batch-mean array of x^2 with shape (len(specs), ntraj * nbatch).
    """
    rng = np.random.default_rng(seed)
    n_chunk = int(round(t_batch / dt))
    n_burn = int(round(t_burn / t_batch))
    n_samp = int(round(t_samp / t_batch))
    sq = np.sqrt(dt)
    z = [np.zeros((ntraj, 1)) for _ in specs]
    bm = np.empty((len(specs), ntraj, n_samp))
    for k in range(n_burn + n_samp):
        dWs = rng.standard_normal((ntraj, n_chunk)) * sq
        dWm = rng.standard_normal((ntraj, n_chunk)) * sq
        if sensory is not None:
            dWs = sensory(k, dWs)
        extra = drive(k, n_chunk, ntraj, rng) if drive is not None else None
        for i, sp in enumerate(specs):
            a, gs, gm = sp[:3]
            u = gs * dWs + gm * dWm
            if extra is not None:
                u += sp[3] * extra
            y, z[i] = ar1(u, 1.0 - a * dt, z[i])
            if k >= n_burn:
                bm[i, :, k - n_burn] = np.mean(y * y, axis=1)
    return bm.reshape(len(specs), -1)


def est(b):
    """Mean and batch-means SE (works along last axis)."""
    n = b.shape[-1]
    return b.mean(-1), b.std(-1, ddof=1) / np.sqrt(n)


def crossings(x, y, level):
    """Sign changes of y-level on sorted grid, located by linear interp in log x."""
    d = y - level
    out = []
    for i in range(len(x) - 1):
        if d[i] == 0:
            out.append(float(x[i]))
        elif d[i] * d[i + 1] < 0:
            lx = np.log(x[i]) + (np.log(x[i + 1]) - np.log(x[i])) * d[i] / (d[i] - d[i + 1])
            out.append(float(np.exp(lx)))
    return out


def intervals(mask):
    """Number of disjoint True runs and their index bounds."""
    m = np.asarray(mask, dtype=int)
    dm = np.diff(np.concatenate([[0], m, [0]]))
    starts = np.where(dm == 1)[0]
    ends = np.where(dm == -1)[0] - 1
    return list(zip(starts.tolist(), ends.tolist()))


def dump(name, obj):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    with open(os.path.join(RES, name), "w") as f:
        json.dump(obj, f, indent=1, default=conv)


class Timer:
    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, *a):
        self.dt = time.time() - self.t0
