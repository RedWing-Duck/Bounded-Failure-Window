"""Shared classifier (Task 10): route (i) Theorem 1.2 on the turning-point sequence; route (ii) direct
root-finding of sigma^2 = R^2 on monotone pieces. Both return the class (l, u, k) or "All"."""
import math

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

from t10_common import WIDTH, T

EQ = mp.mpf("1e-40")
EQF = 1e-12


def _eq(a, b, tol=EQ):
    if a in (mp.inf, math.inf) or b in (mp.inf, math.inf):
        return a == b
    return abs(a - b) <= tol * max(abs(a), abs(b))


def _cls(comps_touch, n_parts_all):
    ell = int(any(lo for lo, hi in comps_touch))
    u = int(any(hi for lo, hi in comps_touch))
    k = sum(1 for lo, hi in comps_touch if not lo and not hi)
    if n_parts_all:
        return "All"
    return (ell, u, k)


# ---------------------------------------------------------------- route (i)
def route_i(A, R2, tol=EQ):
    vals = [A["L_minus"]] + [t["value"] for t in A["turns"]] + [A["L_plus"]]
    dirs = A["dirs"]
    parts = []
    for j, d in enumerate(dirs):
        a, b = vals[j], vals[j + 1]
        lo_v, hi_v = (a, b) if d > 0 else (b, a)
        if _eq(R2, hi_v, tol) or R2 > hi_v:
            parts.append((False, False))
        elif _eq(R2, lo_v, tol) or R2 < lo_v:
            parts.append((True, True))
        else:
            parts.append((d < 0, d > 0))
    comps, cur = [], None
    for j, (tl, tr) in enumerate(parts):
        if not (tl and cur is not None) and (tl or tr):
            cur = [j == 0 and tl, False]
        if cur is None:
            continue
        tv = vals[j + 1]
        joins = tr and j + 1 < len(parts) and parts[j + 1][0] and tv > R2 and not _eq(tv, R2, tol)
        if not joins:
            cur[1] = (j == len(parts) - 1) and tr
            comps.append(tuple(cur))
            cur = None
    allc = len(comps) == 1 and comps[0] == (True, True)
    return _cls(comps, allc)


# ---------------------------------------------------------------- route (ii)
def route_ii(A, R2, prec="mp"):
    """Direct: roots of f - R2 on each monotone piece, split points, interior sign tests."""
    c = A["curve"]
    turns, bounds = A["turns"], A["bounds"]
    if prec == "mp":
        f = lambda x: c.f(T(x))
        eq = lambda a, b: _eq(a, b, EQ)
        pos = lambda v: v - R2 > EQ * R2
    else:
        R2 = float(R2)
        f = lambda x: float(c.ffl(np.float64(10.0) ** float(x)))
        eq = lambda a, b: _eq(a, b, EQF)
        pos = lambda v: v - R2 > EQF * R2
    vals = [A["L_minus"]] + [t["value"] for t in turns] + [A["L_plus"]]
    vals = [v if prec == "mp" else (math.inf if v == mp.inf else float(v)) for v in vals]
    splits = []
    for j in range(len(bounds) - 1):
        a, b = vals[j], vals[j + 1]
        ga = 0 if eq(a, R2) else (1 if a > R2 else -1)
        gb = 0 if eq(b, R2) else (1 if b > R2 else -1)
        if ga * gb < 0:
            lo, hi = bounds[j], bounds[j + 1]
            if prec == "mp":
                fa = ga
                while hi - lo > WIDTH:
                    m = (lo + hi) / 2
                    v = f(m) - R2
                    if (v > 0) == (fa > 0):
                        lo = m
                    else:
                        hi = m
                splits.append((lo + hi) / 2)
            else:
                g = lambda x: (f(x) - R2) if math.isfinite(f(x)) else 1e300
                splits.append(mp.mpf(brentq(g, float(lo), float(hi), xtol=1e-14)))
    for t in turns:
        tv = t["value"] if prec == "mp" else float(t["value"])
        if eq(tv, R2):
            splits.append(t["x"])
    splits = sorted(splits)
    if not splits:
        xs = [c.shift]
    else:
        xs = [splits[0] - 1] + [(splits[i] + splits[i + 1]) / 2 for i in range(len(splits) - 1)] + [splits[-1] + 1]
    inside = [pos(f(x)) for x in xs]
    edges = [None] + splits + [None]
    comps = []
    for i, ins in enumerate(inside):
        if ins:
            comps.append((edges[i] is None, edges[i + 1] is None, edges[i], edges[i + 1]))
    allc = len(inside) == 1 and inside[0]
    cls = _cls([(a, b) for a, b, _, _ in comps], allc)
    ends = [(None if lo is None else T(lo), None if hi is None else T(hi)) for _, _, lo, hi in comps]
    return cls, ends


def classify(A, R2, prec="mp"):
    c1 = route_i(A, R2, EQ if prec == "mp" else EQF)
    c2, ends = route_ii(A, R2, prec)
    return {"route_i": c1, "route_ii": c2, "agree": c1 == c2, "ends": ends}


NAMES = {(0, 0, 0): "Empty", (1, 0, 0): "lower ray", (0, 1, 0): "upper ray", (1, 1, 0): "two rays",
         (0, 0, 1): "window", "All": "All"}


def name(cls):
    return NAMES.get(cls, str(tuple(cls)) if not isinstance(cls, str) else cls)
