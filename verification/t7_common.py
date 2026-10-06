"""Shared helpers for Task 7 (see PREREG_t7.md, 'Conventions')."""
import math

import numpy as np
import sympy as sp

FALLBACK_SEED = 7003


def sf_match(computed, stated, n):
    """|computed - stated| <= half a unit in the n-th significant figure of the stated value."""
    e = math.floor(math.log10(abs(stated)))
    return abs(computed - stated) <= 0.5 * 10 ** (e - n + 1)


def _draw(sym, rng):
    name = sym.name
    if name in ("phi",):
        v = rng.uniform(0.01, 0.99)
    elif name == "L":
        v = rng.uniform(0.001, 0.999)
    else:
        v = 10 ** rng.uniform(-2, 2)
    return sp.Rational(repr(float(v)))


def identity(lhs, rhs, n_points=20, tol=1e-12):
    """Return dict: symbolic (bool), numeric max rel err, verdict string, pass bool."""
    diff = sp.simplify(lhs - rhs)
    sym_ok = diff == 0
    rng = np.random.default_rng(FALLBACK_SEED)
    syms = sorted((lhs - rhs).free_symbols, key=lambda s: s.name)
    worst = 0.0
    for _ in range(n_points):
        d = {s: _draw(s, rng) for s in syms}
        Lv, Rv = sp.N(sp.sympify(lhs).subs(d), 50), sp.N(sp.sympify(rhs).subs(d), 50)
        den = max(abs(Lv), abs(Rv))
        worst = max(worst, 0.0 if den == 0 else float(abs(Lv - Rv) / den))
    num_ok = worst <= tol
    if sym_ok:
        verdict = "PASS (symbolic)"
    elif num_ok:
        verdict = "PASS (numeric only; simplify inconclusive)"
    else:
        verdict = "FAIL"
    return {"symbolic": bool(sym_ok), "numeric_max_rel": worst, "numeric_ok": bool(num_ok),
            "verdict": verdict, "pass": bool(sym_ok or num_ok),
            "residual": None if sym_ok else str(diff)}


def pi0_of(kappa, c=1.0, F=0.01):
    """Prior precision Pi_0 for over-weighting ratio kappa = (c/Pi_0)/F."""
    return c / (kappa * F)


def peak(Pi_0, lam=1.0, c=1.0, sig=0.01):
    """Peak of (2) with G = c Pi/(Pi+Pi_0): positive root of A Pi^2 + B Pi + C = 0; M = F if none."""
    A = 2 * Pi_0 * sig + c**2 + c * lam
    B = 4 * Pi_0**2 * sig
    Cq = Pi_0**2 * (2 * Pi_0 * sig - c * lam)
    if Cq >= 0:
        return 0.0, sig / lam
    p = 2 * (-Cq) / (B + np.sqrt(B * B - 4 * A * Cq))     # stable form of (-B + sqrt(B^2-4AC))/(2A)
    g = c * p / (p + Pi_0)
    return p, (sig + g * g / (2 * p)) / (lam + g)
