"""Task 13 shared helpers: result store, SymPy identity routes (Tasks 10-12), JSON output, paths to earlier tasks."""
import json
import os
import signal
import sys

import mpmath as mp
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)
for d in ("t10", "t11", "t12"):
    sys.path.insert(0, os.path.join(CLS, d))


class Store:
    """Collects check records (Task 12 format) and printed lines."""

    def __init__(self):
        self.R, self.lines = {}, []

    def out(self, t):
        print(t, flush=True)
        self.lines.append(t)

    def zero(self, key, desc, e, tmax=300):
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
        self.R.setdefault(key, []).append(rec)
        self.out(f"  [{'PASS' if ok else 'FAIL'}] ({rec['route']}) {desc}")
        return ok

    def signed(self, key, desc, e, want):
        s = sp.simplify(e)
        ok = bool(s.is_positive if want > 0 else s.is_negative)
        self.R.setdefault(key, []).append({"desc": desc, "route": "assumptions", "pass": ok, "expr": str(s)})
        self.out(f"  [{'PASS' if ok else 'FAIL'}] (assumptions) {desc}: {s}")
        return ok

    def check(self, key, desc, ok, info=""):
        self.R.setdefault(key, []).append({"desc": desc, "route": "check", "pass": bool(ok), "info": str(info)})
        self.out(f"  [{'PASS' if ok else 'FAIL'}] (check) {desc} {info}")
        return ok

    def note(self, key, desc, text):
        self.R.setdefault(key, []).append({"desc": desc, "route": "record", "pass": True, "text": text})
        self.out(f"  [record] {desc}: {text}")


class _TO(Exception):
    pass


def _alarm(*_):
    raise _TO()


def _sqrt_factor(e):
    return e.xreplace({p: sp.sqrt(sp.factor(p.base)) for p in e.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)})


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


def logu(rng, lo=-2, hi=2):
    return float(10.0**rng.uniform(lo, hi))
