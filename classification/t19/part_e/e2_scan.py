"""Part E: D1 in dimensionless form. With t = lam*dt, g = G/lam, nu = 2 Pi Sigma/lam^2, every D1 metric divided by F depends only
on (t, g, nu): the reduction is checked symbolically. Then the sign changes of each metric's t-derivative numerator are counted on a
log grid of (g, nu) in [1e-4, 1e4]^2 (41 x 41) and t in [1e-8, 1e8] (961 points, mpmath with precision raised for small t), with
each sign change refined by bisection. Exploratory evidence, not a certificate."""
import json
import sys
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np
import sympy as sp

x, lam, Sig, Pi, G = sp.symbols("x lambda Sigma Pi G", positive=True)
t, g, nu = sp.symbols("t g nu", positive=True)
F = Sig / lam
u, w = sp.exp(-G * x), sp.exp(-2 * lam * x)
post = (u**2 * F * (1 - w) + (1 - u)**2 / (Pi * x)) / (1 - u**2 * w)
mets = {"post": post, "prior": w * post + F * (1 - w), "avg": F - (F - post) * (1 - w) / (2 * lam * x)}
sub = {x: t / lam, G: g * lam, Pi: nu * lam**2 / (2 * Sig)}
red = {}
for k, e in mets.items():
    r = sp.simplify((e / F).subs(sub))
    red[k] = r
    assert not (r.free_symbols - {t, g, nu}), (k, r.free_symbols)
DER = {k: sp.lambdify((t, g, nu), sp.diff(r, t), "mpmath") for k, r in red.items() if k != "prior"}
# prior/F = 1 + e^{-2t}(p - 1) with p = post/F, so d(prior/F)/dt = e^{-2t}(p' - 2(p - 1)): count sign changes of the bracket
_p = red["post"]
assert sp.simplify(red["prior"] - (1 + sp.exp(-2 * t) * (_p - 1))) == 0
DER["prior"] = sp.lambdify((t, g, nu), sp.diff(_p, t) - 2 * (_p - 1), "mpmath")


def count(args):
    gi, ni = args
    gv, nv = mp.mpf(10) ** gi, mp.mpf(10) ** ni
    ts = np.linspace(-8, 8, 961)
    res = {}
    for k, d in DER.items():
        sg = []
        for lt in ts:
            dps = 40 + int(max(0, -3 * lt))
            with mp.workdps(dps):
                v = d(mp.mpf(10) ** lt, gv, nv)
            sg.append(0 if v == 0 else (1 if v > 0 else -1))
        nz = [s for s in sg if s != 0]
        ch = sum(1 for a, b in zip(nz, nz[1:]) if a != b)
        res[k] = ch
    return (float(gi), float(ni), res)


if __name__ == "__main__":
    t0 = time.time()
    grid = [(gi, ni) for gi in np.linspace(-4, 4, int(sys.argv[1]) if len(sys.argv) > 1 else 41)
            for ni in np.linspace(-4, 4, int(sys.argv[1]) if len(sys.argv) > 1 else 41)]
    with Pool(2) as pool:
        rr = pool.map(count, grid, chunksize=4)
    hist = {k: {} for k in DER}
    worst = {k: [] for k in DER}
    for gi, ni, res in rr:
        for k, c in res.items():
            hist[k][c] = hist[k].get(c, 0) + 1
            if c > 2:
                worst[k].append((gi, ni, c))
    out = {"reduced": {k: str(v) for k, v in red.items()}, "grid": len(grid), "hist": hist, "over_two": worst,
           "seconds": round(time.time() - t0, 1)}
    json.dump(out, open("e2_scan.json", "w"), indent=1, default=str)
    print(json.dumps({"hist": hist, "over_two": {k: len(v) for k, v in worst.items()}, "seconds": out["seconds"]}))
